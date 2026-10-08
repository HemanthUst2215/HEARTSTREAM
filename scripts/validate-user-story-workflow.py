#!/usr/bin/env python3
"""Validate generate-user-story workflow references and run a smoke pipeline test."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURSOR = ROOT / ".cursor"

REQUIRED = [
    CURSOR / "commands/generate-user-story.md",
    CURSOR / "agents/business-analyst-agent.md",
    CURSOR / "subagents/work-item-reference-matcher.md",
    CURSOR / "subagents/invest-scorecard-evaluator.md",
    CURSOR / "subagents/gherkin-acceptance-criteria-writer.md",
    CURSOR / "skills/user-story-generation/SKILL.md",
    ROOT / "scripts/generate-user-story-outputs.py",
]


def main() -> int:
    errors: list[str] = []
    for p in REQUIRED:
        if not p.is_file():
            errors.append(f"missing: {p.relative_to(ROOT)}")

    cmd = (CURSOR / "commands/generate-user-story.md").read_text(encoding="utf-8")
    if "generate-user-story-outputs.py" not in cmd:
        errors.append("command missing pipeline script reference")

    orch = (CURSOR / "agents/orchestrator-agent.md").read_text(encoding="utf-8")
    if "/generate-user-story" not in orch:
        errors.append("orchestrator missing generate-user-story route")

    draft_dir = ROOT / "artifacts/user-stories/.pipeline"
    draft_dir.mkdir(parents=True, exist_ok=True)
    draft = draft_dir / "stories-draft-smoke.json"
    draft.write_text(
        json.dumps(
            {
                "sourceTranscript": "smoke-test",
                "stories": [
                    {
                        "userStoryId": "US-SMOKE-001",
                        "title": "Reseller Portal",
                        "description": "As a reseller, I want a self-service portal so that I can track cases and service requests.",
                        "acceptanceCriteria": "Given a reseller user, When they open the portal, Then they can view open cases.",
                        "priority": "High",
                        "keywords": ["reseller", "portal", "D365 Customer Service"],
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    import subprocess

    r = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/generate-user-story-outputs.py"),
            "--draft",
            str(draft),
            "--work-items-dir",
            str(ROOT / "artifacts/work-items"),
            "--out-dir",
            str(ROOT / "artifacts/user-stories/.pipeline/smoke"),
            "--threshold",
            "50",
        ],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        errors.append(f"smoke pipeline failed: {r.stderr or r.stdout}")

    smoke_csv = ROOT / "artifacts/user-stories/.pipeline/smoke/user-stories.csv"
    if not smoke_csv.is_file():
        errors.append("smoke user-stories.csv not created")
    else:
        text = smoke_csv.read_text(encoding="utf-8-sig")
        if "US-SMOKE-001" not in text:
            errors.append("smoke CSV missing UserStoryID")

    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS: generate-user-story workflow references and smoke pipeline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
