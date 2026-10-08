#!/usr/bin/env python3
"""Validate ADO user story CSV output against docs/intake/user-story-csv-rulebook.yaml.

Usage:
  python scripts/validate-user-story-csv.py --csv path/to/output.csv
  python scripts/validate-user-story-csv.py --csv out.csv --rulebook docs/intake/user-story-csv-rulebook.yaml
  python scripts/validate-user-story-csv.py --csv out.csv --report artifacts/intake/validation.json

Exit 0 when PASS; exit 1 when FAIL. Does not read bootstrap setup CSVs.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ado_user_story_csv_layout import validate_row_content, validate_structure  # noqa: E402

DEFAULT_RULEBOOK = ROOT / "docs" / "intake" / "user-story-csv-rulebook.yaml"


def load_rulebook(path: Path) -> dict:
    if yaml is None:
        print("FAIL: PyYAML required (pip install pyyaml)", file=sys.stderr)
        sys.exit(1)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print("FAIL: rulebook root must be a mapping", file=sys.stderr)
        sys.exit(1)
    return data


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return [], []
        headers = list(reader.fieldnames)
        rows = [{k: (v or "").strip() for k, v in row.items()} for row in reader]
    return headers, rows


def validate(rulebook: dict, headers: list[str], rows: list[dict[str, str]]) -> dict:
    findings: list[str] = []
    critical = 0

    expected_cols = rulebook.get("csv", {}).get("column_order", [])
    if headers != expected_cols:
        findings.append(
            f"header mismatch: expected {expected_cols!r}, got {headers!r}"
        )
        critical += 1

    allowed_types = set(rulebook.get("work_item_types", {}).get("allowed", []))

    struct_f, struct_c = validate_structure(rulebook, rows, row_offset=2)
    findings.extend(struct_f)
    critical += struct_c

    content_f, content_c = validate_row_content(rulebook, rows, row_offset=2)
    findings.extend(content_f)
    critical += content_c

    for idx, row in enumerate(rows, start=2):
        wit = row.get("Work Item Type", "")
        if not wit:
            continue
        if wit not in allowed_types:
            findings.append(f"row {idx}: disallowed Work Item Type '{wit}'")
            critical += 1

        task_type = row.get("Task Type1", "")
        allowed_task = rulebook.get("task_type1", {}).get("allowed_values", [])
        if task_type and task_type not in allowed_task:
            findings.append(f"row {idx}: Task Type1 '{task_type}' not in allowed list")

        for col in rulebook.get("workshop_governance_columns", {}).get("columns", []):
            val = row.get(col, "")
            if val and val not in rulebook.get("workshop_governance_columns", {}).get(
                "yes_no_values", ["Yes", ""]
            ):
                findings.append(f"row {idx}: column '{col}' must be Yes or empty, got '{val}'")

    extra_cols = set(headers) - set(expected_cols)
    if extra_cols:
        findings.append(f"unexpected columns: {sorted(extra_cols)}")
        critical += 1

    warnings = [f for f in findings if "should use" in f]
    errors = [f for f in findings if f not in warnings]
    if critical > 0 or errors:
        status = "FAIL"
    elif warnings:
        status = "PASS_WITH_WARNINGS"
    else:
        status = "PASS"

    return {
        "status": status,
        "critical": critical,
        "findings": findings,
        "row_count": len(rows),
        "rulebook_id": rulebook.get("rulebook_id"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Generated user story CSV to validate")
    parser.add_argument("--rulebook", default=str(DEFAULT_RULEBOOK))
    parser.add_argument("--report", help="Optional JSON report path")
    args = parser.parse_args()

    csv_path = Path(args.csv).resolve()
    rulebook_path = Path(args.rulebook).resolve()
    if not rulebook_path.is_file():
        print(f"FAIL: rulebook not found: {rulebook_path}", file=sys.stderr)
        return 1
    if not csv_path.is_file():
        print(f"FAIL: csv not found: {csv_path}", file=sys.stderr)
        return 1

    rulebook = load_rulebook(rulebook_path)
    headers, rows = read_csv_rows(csv_path)
    result = validate(rulebook, headers, rows)
    result["csv"] = str(csv_path)
    result["rulebook"] = str(rulebook_path)

    if args.report:
        out = Path(args.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))
    if result["status"] == "FAIL":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
