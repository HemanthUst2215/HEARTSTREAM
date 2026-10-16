#!/usr/bin/env python3
"""CLI: write ADO CSV from row JSON; validate layout + rulebook.

  python scripts/ado_user_story_csv.py write --json rows.json --out artifacts/intake/out.csv
  python scripts/ado_user_story_csv.py write --json rows.json --out out.csv --rulebook docs/intake/user-story-csv-rulebook.yaml
  python scripts/ado_user_story_csv.py validate --csv out.csv

Agents: build row dicts in memory → persist JSON → call `write` → call validate-user-story-csv.py or `validate` here.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RULEBOOK = ROOT / "docs" / "intake" / "user-story-csv-rulebook.yaml"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ado_user_story_csv_layout import (  # noqa: E402
    acceptance_criteria_cell,
    apply_generation_defaults,
    blank_row,
    headers_from_rulebook,
    issue_description_cell,
    validate_row_content,
    validate_structure,
    write_csv,
)


def load_rulebook(path: Path) -> dict:
    if yaml is None:
        print("FAIL: PyYAML required (pip install pyyaml)", file=sys.stderr)
        sys.exit(1)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("rulebook root must be a mapping")
    return data


def cmd_write(args: argparse.Namespace) -> int:
    rulebook = load_rulebook(Path(args.rulebook))
    headers = headers_from_rulebook(rulebook)
    payload = json.loads(Path(args.json).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise SystemExit("JSON root must be an array of row objects")
    rows: list[dict[str, str]] = []
    for item in payload:
        if not isinstance(item, dict):
            raise SystemExit("each row must be an object")
        base = blank_row(headers)
        for k, v in item.items():
            if k in base:
                base[k] = "" if v is None else str(v)
        if "Title" in item and "Title" not in headers:
            base["Title"] = "" if item.get("Title") is None else str(item.get("Title"))
        apply_generation_defaults(rulebook, base)
        if "Title" not in headers:
            base.pop("Title", None)
        rows.append(base)
    out = Path(args.out)
    write_csv(out, headers, rows)
    struct_f, struct_c = validate_structure(rulebook, rows)
    content_f, content_c = validate_row_content(rulebook, rows)
    findings = struct_f + content_f
    critical = struct_c + content_c
    if critical:
        print(json.dumps({"status": "FAIL", "findings": findings}, indent=2), file=sys.stderr)
        return 1
    print(f"wrote {out} ({len(rows)} rows)")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    # Delegate to validate-user-story-csv for single entrypoint in CI
    import subprocess

    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "validate-user-story-csv.py"),
        "--csv",
        args.csv,
        "--rulebook",
        args.rulebook,
    ]
    if args.report:
        cmd.extend(["--report", args.report])
    return subprocess.call(cmd)


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    w = sub.add_parser("write", help="Write CSV from row JSON using canonical layout writer")
    w.add_argument("--json", required=True)
    w.add_argument("--out", required=True)
    w.add_argument("--rulebook", default=str(DEFAULT_RULEBOOK))

    v = sub.add_parser("validate", help="Run full CSV validation")
    v.add_argument("--csv", required=True)
    v.add_argument("--rulebook", default=str(DEFAULT_RULEBOOK))
    v.add_argument("--report")

    args = parser.parse_args()
    if args.command == "write":
        return cmd_write(args)
    return cmd_validate(args)


# Re-export helpers for emit script and tests
__all__ = [
    "acceptance_criteria_cell",
    "issue_description_cell",
    "write_csv",
    "headers_from_rulebook",
    "blank_row",
]

if __name__ == "__main__":
    sys.exit(main())
