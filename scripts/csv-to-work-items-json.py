#!/usr/bin/env python3
"""
Transform Azure DevOps-style work item CSV into HeartStream work-items.json.

Usage:
  python scripts/csv-to-work-items-json.py <source.csv> [-o out.json]
  python scripts/csv-to-work-items-json.py --profile-only <source.csv>
  python scripts/csv-to-work-items-json.py --validate out.json --source <source.csv>
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED_COLUMNS = [
    "State",
    "ID",
    "Work Item Type",
    "Title",
    "Description",
    "Parent",
    "Related Link Count",
    "Area Path",
    "Iteration Path",
]

CODE_PREFIX_RE = re.compile(r"^([A-Z]{2}-[A-Z]{2}-[\dA-Za-z &\-]+?)\s*-\s*(.+)$", re.DOTALL)


def split_path(raw: str) -> dict[str, Any]:
    raw = (raw or "").strip()
    segments = [s.strip() for s in raw.split("\\") if s.strip()]
    return {"raw": raw, "segments": segments}


def decode_text(value: str) -> tuple[str, bool]:
    plain = (value or "").strip()
    decoded = html.unescape(plain)
    return decoded, decoded != plain


def first_paragraph(text: str, max_len: int = 320) -> str:
    if not text:
        return ""
    chunk = re.split(r"\n\s*\n", text.strip(), maxsplit=1)[0]
    chunk = re.sub(r"\s+", " ", chunk).strip()
    if len(chunk) > max_len:
        return chunk[: max_len - 1].rstrip() + "…"
    return chunk


def parse_title(raw_title: str) -> tuple[str | None, str, str]:
    title = (raw_title or "").strip()
    m = CODE_PREFIX_RE.match(title)
    if m:
        code = m.group(1).strip()
        short = m.group(2).strip()
        display = f"{code} — {short}"
        return code, short, display
    return None, title, title


def parse_int(value: str) -> int | None:
    v = (value or "").strip()
    if not v:
        return None
    try:
        return int(v)
    except ValueError:
        return None


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]], list[int]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row")
        columns = list(reader.fieldnames)
        rows: list[dict[str, str]] = []
        row_numbers: list[int] = []
        for i, row in enumerate(reader, start=2):
            rows.append({k: (v if v is not None else "") for k, v in row.items()})
            row_numbers.append(i)
    return columns, rows, row_numbers


def build_work_item(row: dict[str, str], row_number: int) -> dict[str, Any]:
    work_item_id = parse_int(row.get("ID", ""))
    if work_item_id is None:
        raise ValueError(f"Row {row_number}: invalid ID")

    code, short_title, display_title = parse_title(row.get("Title", ""))
    desc_plain, html_decoded = decode_text(row.get("Description", ""))

    return {
        "workItemId": work_item_id,
        "workItemCode": code,
        "title": short_title,
        "displayTitle": display_title,
        "workItemType": (row.get("Work Item Type") or "").strip(),
        "state": (row.get("State") or "").strip(),
        "parent": {"workItemId": parse_int(row.get("Parent", ""))},
        "relatedLinkCount": parse_int(row.get("Related Link Count", "")),
        "areaPath": split_path(row.get("Area Path", "")),
        "iterationPath": split_path(row.get("Iteration Path", "")),
        "description": {
            "plainText": desc_plain,
            "summary": first_paragraph(desc_plain),
            "htmlDecoded": html_decoded,
        },
        "source": {"rowNumber": row_number, "id": str(work_item_id)},
    }


def summarize(work_items: list[dict[str, Any]]) -> dict[str, Any]:
    by_state = Counter(w["state"] or "(empty)" for w in work_items)
    by_type = Counter(w["workItemType"] or "(empty)" for w in work_items)
    by_iter = Counter(
        (w.get("iterationPath") or {}).get("raw") or "(empty)" for w in work_items
    )
    return {
        "byState": dict(sorted(by_state.items())),
        "byWorkItemType": dict(sorted(by_type.items())),
        "byIterationPath": dict(sorted(by_iter.items())),
    }


def transform(source: Path) -> dict[str, Any]:
    columns, rows, row_numbers = read_csv_rows(source)
    missing = [c for c in REQUIRED_COLUMNS if c not in columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    work_items = []
    for row, rn in zip(rows, row_numbers):
        if not any((row.get(c) or "").strip() for c in ("ID", "Title")):
            continue
        work_items.append(build_work_item(row, rn))

    return {
        "meta": {
            "sourceFile": str(source.resolve()),
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "rowCount": len(work_items),
            "columns": columns,
        },
        "summary": summarize(work_items),
        "workItems": work_items,
    }


def profile(source: Path) -> dict[str, Any]:
    columns, rows, _ = read_csv_rows(source)
    missing = [c for c in REQUIRED_COLUMNS if c not in columns]
    extra = [c for c in columns if c not in REQUIRED_COLUMNS]
    states = Counter((r.get("State") or "").strip() or "(empty)" for r in rows)
    types = Counter((r.get("Work Item Type") or "").strip() or "(empty)" for r in rows)
    return {
        "sourceFile": str(source.resolve()),
        "rowCount": len(rows),
        "columns": columns,
        "required_missing": missing,
        "extra_columns": extra,
        "distinct_counts": {
            "State": dict(states),
            "Work Item Type": dict(types),
        },
    }


def validate_output(data: dict[str, Any], source: Path) -> dict[str, Any]:
    issues: list[str] = []
    work_items = data.get("workItems") or []
    meta = data.get("meta") or {}
    _, rows, _ = read_csv_rows(source)
    csv_data_rows = [r for r in rows if (r.get("ID") or "").strip()]
    if len(work_items) != len(csv_data_rows):
        issues.append(
            f"row count mismatch: JSON {len(work_items)} vs CSV {len(csv_data_rows)}"
        )

    ids = [w.get("workItemId") for w in work_items]
    if len(ids) != len(set(ids)):
        issues.append("duplicate workItemId values in JSON")

    for w in work_items:
        for field in ("workItemId", "title", "workItemType", "state", "source"):
            if field not in w:
                issues.append(f"missing field {field} on item {w.get('workItemId')}")

    verdict = "PASS" if not issues else "FAIL"
    return {
        "verdict": verdict,
        "issues": issues,
        "jsonRowCount": len(work_items),
        "csvRowCount": len(csv_data_rows),
        "metaRowCount": meta.get("rowCount"),
    }


def write_summary_md(data: dict[str, Any], out_path: Path) -> None:
    meta = data["meta"]
    summary = data["summary"]
    lines = [
        f"# Work Items Summary",
        "",
        f"- **Source:** `{meta['sourceFile']}`",
        f"- **Generated:** {meta['generatedAt']}",
        f"- **Total items:** {meta['rowCount']}",
        "",
        "## By state",
        "",
    ]
    for k, v in summary.get("byState", {}).items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## By work item type", ""])
    for k, v in summary.get("byWorkItemType", {}).items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Sample (first 10)", "", "| ID | Code | Title | State | Type |", "|---|---|---|---|---|"])
    for w in data["workItems"][:10]:
        code = w.get("workItemCode") or ""
        title = (w.get("title") or "").replace("|", "/")[:60]
        lines.append(
            f"| {w['workItemId']} | {code} | {title} | {w.get('state', '')} | {w.get('workItemType', '')} |"
        )
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="CSV → work-items.json")
    parser.add_argument("source", nargs="?", help="Source CSV path")
    parser.add_argument("-o", "--output", default="artifacts/work-items/work-items.json")
    parser.add_argument("--profile-only", action="store_true")
    parser.add_argument("--profile-out", help="Write schema profile JSON path")
    parser.add_argument("--validate", metavar="JSON", help="Validate existing JSON")
    parser.add_argument("--source-for-validate", "--source", dest="validate_source")
    parser.add_argument("--summary-md", help="Write markdown summary path")
    args = parser.parse_args()

    if args.validate:
        json_path = Path(args.validate)
        src = Path(args.validate_source or args.source)
        if not src.is_file():
            print("validate requires --source <csv>", file=sys.stderr)
            return 1
        data = json.loads(json_path.read_text(encoding="utf-8"))
        report = validate_output(data, src)
        report_path = json_path.parent / f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-validation-report.json"
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 0 if report["verdict"] == "PASS" else 1

    if not args.source:
        parser.print_help()
        return 1

    source = Path(args.source)
    if not source.is_file():
        print(f"source not found: {source}", file=sys.stderr)
        return 1

    if args.profile_only:
        prof = profile(source)
        out = Path(args.profile_out) if args.profile_out else source.parent / f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-schema-profile.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(prof, indent=2), encoding="utf-8")
        print(json.dumps(prof, indent=2))
        return 0

    data = transform(source)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out_path} ({data['meta']['rowCount']} items)")

    prof = profile(source)
    prof_path = out_path.parent / f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-schema-profile.json"
    prof_path.write_text(json.dumps(prof, indent=2), encoding="utf-8")

    report = validate_output(data, source)
    report_path = out_path.parent / f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-validation-report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if report["verdict"] != "PASS":
        print(json.dumps(report, indent=2), file=sys.stderr)
        return 1

    summary_path = Path(args.summary_md) if args.summary_md else out_path.parent / "work-items-summary.md"
    write_summary_md(data, summary_path)
    print(f"wrote {summary_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
