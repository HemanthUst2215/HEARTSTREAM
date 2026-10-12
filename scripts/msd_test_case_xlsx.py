#!/usr/bin/env python3
"""CLI: extract User Story Excel → write MSD E2E workbook from case JSON → validate.

  python scripts/msd_test_case_xlsx.py extract-stories --in stories.xlsx --out stories.json
  python scripts/msd_test_case_xlsx.py write --json cases.json --out artifacts/intake/out.xlsx
  python scripts/msd_test_case_xlsx.py validate --xlsx out.xlsx

Agents: persist case objects to JSON → `write` → `validate`. Never hand-build the workbook.
Column names and sheet layout come only from docs/intake/msd-test-case-rulebook.yaml.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RULEBOOK = ROOT / "docs" / "intake" / "msd-test-case-rulebook.yaml"
DEFAULT_SOURCE_RULEBOOK = ROOT / "docs" / "intake" / "user-story-csv-rulebook.yaml"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from msd_test_case_xlsx_layout import (  # noqa: E402
    cell_str,
    load_rulebook,
    write_workbook,
)


def _load_config_project_name(config_path: Path) -> str | None:
    try:
        import yaml  # type: ignore
    except ImportError:
        return None
    if not config_path.is_file():
        return None
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    name = ((data.get("project") or {}).get("name")) if isinstance(data, dict) else None
    return str(name) if name else None


def _read_tabular(path: Path) -> list[list[str]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as f:
            return [[cell_str(c) for c in row] for row in csv.reader(f)]
    if suffix in {".xlsx", ".xlsm"}:
        try:
            from openpyxl import load_workbook
        except ImportError:
            raise SystemExit("FAIL: openpyxl required (pip install openpyxl)")
        wb = load_workbook(path, data_only=True)
        ws = wb.active
        rows: list[list[str]] = []
        for r in range(1, ws.max_row + 1):
            rows.append([cell_str(ws.cell(r, c).value) for c in range(1, ws.max_column + 1)])
        return rows
    raise SystemExit(f"FAIL: unsupported input suffix {suffix}")


def _find_header_row(grid: list[list[str]], expected: list[str]) -> int:
    for i, row in enumerate(grid):
        sliced = row[: len(expected)]
        if sliced == expected:
            return i
    # Prefix match: header row contains all expected names in order as a subsequence
    for i, row in enumerate(grid):
        idx = 0
        positions: list[int] = []
        for cell in row:
            if idx < len(expected) and cell == expected[idx]:
                positions.append(0)
                idx += 1
        if idx == len(expected):
            return i
    raise SystemExit(
        "FAIL: could not find a header row matching source rulebook csv.column_order"
    )


def _row_dict(header: list[str], cells: list[str]) -> dict[str, str]:
    out = {h: "" for h in header}
    for i, h in enumerate(header):
        if i < len(cells):
            out[h] = cells[i]
    return out


def extract_stories(source: Path, source_rulebook: dict[str, Any], msd_rulebook: dict[str, Any]) -> dict[str, Any]:
    expected = list(source_rulebook.get("csv", {}).get("column_order") or [])
    if not expected:
        raise SystemExit("FAIL: source rulebook csv.column_order missing")
    grid = _read_tabular(source)
    header_idx = _find_header_row(grid, expected)
    header = expected
    type_col = msd_rulebook["input"]["row_filter"]["type_column"]
    include_key = msd_rulebook["input"]["row_filter"]["include_type_from_source"]
    include_type = source_rulebook.get("work_item_types", {}).get(include_key) or "User Story"
    feature_type = msd_rulebook["input"]["grouping"]["nearest_preceding_feature"]["type_value"]
    bind = msd_rulebook["input"]["field_bind"]

    last_feature = {"title": "", "id": "", "row": None}
    last_epic = {"title": "", "id": "", "row": None}
    stories: list[dict[str, Any]] = []
    context_rows: list[dict[str, Any]] = []

    for offset, cells in enumerate(grid[header_idx + 1 :], start=header_idx + 2):
        if all(c == "" for c in cells[: len(header)]):
            continue
        row = _row_dict(header, cells)
        wit = cell_str(row.get(type_col))
        if wit == "Epic":
            last_epic = {
                "title": cell_str(row.get(bind["title"])),
                "id": cell_str(row.get(bind["id"])),
                "row": offset,
            }
            context_rows.append({"work_item_type": wit, "row": offset, **last_epic})
            continue
        if wit == feature_type:
            last_feature = {
                "title": cell_str(row.get(bind["title"])),
                "id": cell_str(row.get(bind["id"])),
                "row": offset,
            }
            context_rows.append({"work_item_type": wit, "row": offset, **last_feature})
            continue
        if wit != include_type:
            continue
        stories.append(
            {
                "row": offset,
                "id": cell_str(row.get(bind["id"])),
                "work_item_type": wit,
                "title": cell_str(row.get(bind["title"])),
                "description": cell_str(row.get(bind["description"])),
                "acceptance_criteria": cell_str(row.get(bind["acceptance_criteria"])),
                "area_path": cell_str(row.get(bind["area_path"])),
                "nearest_feature_title": last_feature["title"],
                "nearest_feature_id": last_feature["id"],
                "nearest_epic_title": last_epic["title"],
                "nearest_epic_id": last_epic["id"],
                "source_path": str(source),
                "source_locator": f"{source.name}#row-{offset}",
            }
        )

    features_by_id = {
        cell_str(r.get("id")): r
        for r in context_rows
        if r.get("work_item_type") == feature_type and cell_str(r.get("id"))
    }
    grouping_key = []
    for s in stories:
        mapped = features_by_id.get(s["id"])
        if mapped:
            s["nearest_feature_title"] = mapped["title"]
            s["nearest_feature_id"] = mapped["id"]
            key = mapped["title"]
        else:
            key = s["nearest_feature_title"] or s["area_path"] or s["title"]
        grouping_key.append(key)
        s["grouping_key"] = key

    return {
        "source": str(source),
        "header_row": header_idx + 1,
        "include_type": include_type,
        "story_count": len(stories),
        "group_count": len({k for k in grouping_key if k}),
        "stories": stories,
        "context_rows": context_rows,
    }


def cmd_extract(args: argparse.Namespace) -> int:
    msd = load_rulebook(Path(args.rulebook))
    source_rb = load_rulebook(Path(args.source_rulebook))
    payload = extract_stories(Path(args.input), source_rb, msd)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out} ({payload['story_count']} stories, {payload['group_count']} groups)")
    return 0


def cmd_write(args: argparse.Namespace) -> int:
    rulebook = load_rulebook(Path(args.rulebook))
    payload = json.loads(Path(args.json).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        cases = payload
        meta: dict[str, Any] = {}
    elif isinstance(payload, dict):
        cases = payload.get("cases")
        if not isinstance(cases, list):
            raise SystemExit("JSON must contain a 'cases' array")
        meta = payload.get("meta") or {}
    else:
        raise SystemExit("JSON root must be an object with cases[] or an array")
    project = args.project or meta.get("project_label") or _load_config_project_name(ROOT / ".cursor" / "config.yaml")
    csv_path = Path(args.working_csv) if args.working_csv else None
    result = write_workbook(Path(args.out), rulebook, cases, project=project, also_csv=csv_path)
    print(json.dumps(result, indent=2))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    import subprocess

    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "validate-msd-test-case-xlsx.py"),
        "--xlsx",
        args.xlsx,
        "--rulebook",
        args.rulebook,
    ]
    if args.report:
        cmd.extend(["--report", args.report])
    return subprocess.call(cmd)


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    e = sub.add_parser("extract-stories", help="Read User Story Excel/CSV using source rulebook headers")
    e.add_argument("--in", dest="input", required=True)
    e.add_argument("--out", required=True)
    e.add_argument("--rulebook", default=str(DEFAULT_RULEBOOK))
    e.add_argument("--source-rulebook", default=str(DEFAULT_SOURCE_RULEBOOK))

    w = sub.add_parser("write", help="Write MSD E2E xlsx from case JSON")
    w.add_argument("--json", required=True)
    w.add_argument("--out", required=True)
    w.add_argument("--rulebook", default=str(DEFAULT_RULEBOOK))
    w.add_argument("--project")
    w.add_argument("--working-csv", help="Optional internal register CSV")

    v = sub.add_parser("validate", help="Validate generated workbook")
    v.add_argument("--xlsx", required=True)
    v.add_argument("--rulebook", default=str(DEFAULT_RULEBOOK))
    v.add_argument("--report")

    args = parser.parse_args()
    if args.command == "extract-stories":
        return cmd_extract(args)
    if args.command == "write":
        return cmd_write(args)
    return cmd_validate(args)


if __name__ == "__main__":
    sys.exit(main())
