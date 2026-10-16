#!/usr/bin/env python3
"""Validate User Story rows JSON against MSD365 Business Entity scope catalog.

Usage:
  python scripts/validate-user-story-business-entity-scope.py --json artifacts/intake/<date>-user-story-rows.json
  python scripts/validate-user-story-business-entity-scope.py --json rows.json --report scope-validation.json

Exit 0 PASS; exit 1 FAIL. Skips Workshop, Issue, Risk, Feature, Epic rows.
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

from msd365_business_entity_scope import (  # noqa: E402
    DEFAULT_CATALOG,
    load_catalog,
    validate_user_story_rows,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, required=True, help="user-story-rows JSON")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--report", type=Path, help="write validation report JSON")
    args = parser.parse_args()

    if not args.json.is_file():
        print(f"FAIL: rows JSON not found: {args.json}", file=sys.stderr)
        sys.exit(1)
    if not args.catalog.is_file():
        print(f"FAIL: catalog not found: {args.catalog}", file=sys.stderr)
        sys.exit(1)

    rows = json.loads(args.json.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        print("FAIL: rows JSON must be a list", file=sys.stderr)
        sys.exit(1)

    catalog = load_catalog(args.catalog)
    findings, critical = validate_user_story_rows(rows, catalog)
    story_count = sum(
        1 for r in rows if isinstance(r, dict) and r.get("Work Item Type") == "User Story"
    )

    report = {
        "status": "PASS" if critical == 0 else "FAIL",
        "user_story_count": story_count,
        "finding_count": len(findings),
        "critical_count": critical,
        "findings": findings,
        "catalog": str(args.catalog),
        "rows_json": str(args.json),
    }

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if critical:
        for f in findings:
            print(f"FAIL: {f}", file=sys.stderr)
        print(f"FAIL: {critical} scope violation(s) on {story_count} User Story row(s)", file=sys.stderr)
        sys.exit(1)

    print(f"PASS: {story_count} User Story row(s) in MSD365 business entity scope")
    sys.exit(0)


if __name__ == "__main__":
    main()
