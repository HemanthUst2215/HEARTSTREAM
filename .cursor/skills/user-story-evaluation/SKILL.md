---
name: user-story-evaluation
description: >-
  Compare a manual user-story CSV with an AI-generated user-story CSV against
  the source transcript. Use for /evaluate-user-stories. Public output is one HTML report.
---

# User story evaluation

## When to use
- Command: `/evaluate-user-stories`
- Primary: **user-story-evaluation-agent**
- After intake-safety exit 0 on the transcript and both CSVs

## Metric owners
Load `.cursor/templates/user-story-evaluation-metrics.yaml`. Do not restate a formula that disagrees with that file.

| Metric | Subagent | Skill |
|--------|----------|-------|
| Granularity | story-matching-evaluator | `.cursor/skills/story-matching/SKILL.md` |
| Hallucination Rate (Generated), Hallucination Rate (Manual) | hallucination-detection-evaluator | `.cursor/skills/hallucination-detection/SKILL.md` |
| Recall, Precision, Manual-only Stories, Generated-only Stories | coverage-analysis-evaluator | `.cursor/skills/coverage-analysis/SKILL.md` |
| Title and Description Format Compliance, Role Specificity | business-correctness-evaluator | `.cursor/skills/business-correctness/SKILL.md` |
| Acceptance Criteria Count, Acceptance Criteria Quality, Negative and Boundary Coverage | acceptance-criteria-evaluator | `.cursor/skills/acceptance-criteria-evaluation/SKILL.md` |
| Epic Agreement, Feature Agreement | epic-feature-mapping-evaluator | `.cursor/skills/epic-feature-mapping-validation/SKILL.md` |
| Consolidation and render | kpi-aggregation-evaluator | `.cursor/skills/kpi-aggregation/SKILL.md` |

## Order
1. `python scripts/evaluate_user_stories.py allocate-run --date <YYYY-MM-DD> [--slug <output_slug>] --json` — use returned paths. **Never** overwrite an existing public HTML/JSON from a prior run.
2. Output-path gate on the **allocated** paths only.
3. `python scripts/evaluate_user_stories.py prepare --manual <manual.csv> --generated <generated.csv> --transcript <transcript> --out <packet from allocate-run>`
4. story-matching-evaluator writes `<story_matches>` from allocate-run.
5. hallucination-detection-evaluator writes `<hallucination>`.
6. In parallel after matching: business-correctness, acceptance-criteria, epic-feature. Coverage starts only after hallucination is written.
7. kpi-aggregation-evaluator writes `<evaluation>` in the shape of `user-story-evaluation-report-template.md`.
8. `python scripts/evaluate_user_stories.py validate --evaluation <evaluation>` — FAIL stays in Reflect.
9. `python scripts/evaluate_user_stories.py render --evaluation <evaluation> --html <public_html> --json <public_json>`

## Rules the parent enforces
- Proposals in the packet are not matches (`ASSUMPTION-USEVAL-003`).
- One metric, one owner. Wrong owner → reject.
- Valid extra vs noise cites the hallucination file. Conflict → `BLOCKED_CONFLICT`.
- Transcript quotes are copied from the transcript file. Do not smooth them into new requirements.
- Report status: **Draft — Pending Method Review** until a human accepts `ASSUMPTION-USEVAL-001`.

## Do not
- Hand-write HTML.
- Add a metric id that is not in the contract.
- Treat a layout specimen or a packet as the public report.
- Overwrite `artifacts/evaluation/*-user-story-evaluation*.html` or JSON from an earlier run.
