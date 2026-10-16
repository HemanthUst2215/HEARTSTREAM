#!/usr/bin/env python3
"""Validate User Story rows against workshop prerequisite knowledge base.

Usage:
  python scripts/validate-user-story-workshop-scope.py \\
    --json artifacts/intake/<date>-user-story-rows.json \\
    --knowledge-base artifacts/intake/<date>-workshop-prerequisite-knowledge-base.json
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

from workshop_prerequisite_scope import (  # noqa: E402
    load_knowledge_base,
    validate_user_story_rows,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--knowledge-base", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    parser.add_argument(
        "--require-mom",
        action="store_true",
        help="Require mom_locator and mom_source_path on each User Story row",
    )
    args = parser.parse_args()

    if not args.json.is_file():
        print(f"FAIL: rows JSON not found: {args.json}", file=sys.stderr)
        sys.exit(1)
    if not args.knowledge_base.is_file():
        print(f"FAIL: knowledge base not found: {args.knowledge_base}", file=sys.stderr)
        sys.exit(1)

    rows = json.loads(args.json.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        print("FAIL: rows JSON must be a list", file=sys.stderr)
        sys.exit(1)

    kb = load_knowledge_base(args.knowledge_base)
    findings, critical = validate_user_story_rows(
        rows, kb, require_mom_fields=args.require_mom
    )
    story_count = sum(
        1 for r in rows if isinstance(r, dict) and r.get("Work Item Type") == "User Story"
    )

    report = {
        "status": "PASS" if critical == 0 else "FAIL",
        "user_story_count": story_count,
        "finding_count": len(findings),
        "critical_count": critical,
        "findings": findings,
        "knowledge_base": str(args.knowledge_base),
        "rows_json": str(args.json),
    }

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if critical:
        for f in findings:
            print(f"FAIL: {f}", file=sys.stderr)
        sys.exit(1)

    print(f"PASS: {story_count} User Story row(s) aligned with prerequisite scope")
    sys.exit(0)


if __name__ == "__main__":
    main()
