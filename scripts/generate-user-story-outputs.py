#!/usr/bin/env python3
"""
Match generated user stories to work items, evaluate INVEST, write CSV outputs.

Usage:
  python scripts/generate-user-story-outputs.py \\
    --draft artifacts/user-stories/.pipeline/stories-draft.json \\
    --work-items-dir artifacts/work-items \\
    --out-dir artifacts/user-stories \\
    --threshold 50
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from user_story_pipeline.export_csv import export_invest_scorecard_csv, export_user_stories_csv
from user_story_pipeline.invest_scorecard import evaluate_all
from user_story_pipeline.matcher import match_all_stories


def main() -> int:
    parser = argparse.ArgumentParser(description="User story CSV + INVEST pipeline")
    parser.add_argument(
        "--draft",
        default="artifacts/user-stories/.pipeline/stories-draft.json",
        help="Internal draft JSON (not a public deliverable)",
    )
    parser.add_argument("--work-items-dir", default="artifacts/work-items")
    parser.add_argument(
        "--out-dir",
        default="artifacts/user-stories",
        help="Directory for user-stories.csv and invest-scorecard.csv",
    )
    parser.add_argument("--threshold", type=float, default=50.0)
    parser.add_argument("--source-transcript", default="")
    args = parser.parse_args()

    draft_path = Path(args.draft)
    if not draft_path.is_file():
        print(f"draft not found: {draft_path}", file=sys.stderr)
        return 1

    payload = json.loads(draft_path.read_text(encoding="utf-8"))
    stories = payload.get("stories") or []
    if not stories:
        print("no stories in draft", file=sys.stderr)
        return 1

    default_source = args.source_transcript or payload.get("sourceTranscript") or ""

    matched = match_all_stories(stories, Path(args.work_items_dir), threshold=args.threshold)
    invest_rows = evaluate_all(matched)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stories_csv = out_dir / "user-stories.csv"
    invest_csv = out_dir / "invest-scorecard.csv"

    export_user_stories_csv(matched, stories_csv, default_source=default_source)
    export_invest_scorecard_csv(invest_rows, invest_csv)

    report = {
        "storyCount": len(matched),
        "userStoriesCsv": str(stories_csv.resolve()),
        "investScorecardCsv": str(invest_csv.resolve()),
        "matchThreshold": args.threshold,
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
