#!/usr/bin/env python3
"""Validate MSD E2E test-case xlsx against docs/intake/msd-test-case-rulebook.yaml.

Usage:
  python scripts/validate-msd-test-case-xlsx.py --xlsx path/to/out.xlsx
  python scripts/validate-msd-test-case-xlsx.py --xlsx out.xlsx --report artifacts/intake/validation.json

Exit 0 when PASS; exit 1 when FAIL. Does not read the bootstrap execution-plan workbook.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from msd_test_case_xlsx_layout import load_rulebook, validate_workbook  # noqa: E402

DEFAULT_RULEBOOK = ROOT / "docs" / "intake" / "msd-test-case-rulebook.yaml"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xlsx", required=True, help="Generated MSD E2E workbook")
    parser.add_argument("--rulebook", default=str(DEFAULT_RULEBOOK))
    parser.add_argument("--report", help="Optional JSON report path")
    args = parser.parse_args()

    xlsx_path = Path(args.xlsx).resolve()
    rulebook_path = Path(args.rulebook).resolve()
    if not rulebook_path.is_file():
        print(f"FAIL: rulebook not found: {rulebook_path}", file=sys.stderr)
        return 1
    if not xlsx_path.is_file():
        print(f"FAIL: xlsx not found: {xlsx_path}", file=sys.stderr)
        return 1

    rulebook = load_rulebook(rulebook_path)
    findings, critical = validate_workbook(rulebook, xlsx_path)
    status = "FAIL" if critical else "PASS"
    result = {
        "status": status,
        "critical": critical,
        "findings": findings,
        "xlsx": str(xlsx_path),
        "rulebook": str(rulebook_path),
        "rulebook_id": rulebook.get("rulebook_id"),
    }
    if args.report:
        out = Path(args.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 1 if status == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
