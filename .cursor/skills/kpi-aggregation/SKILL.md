---
name: kpi-aggregation
description: >-
  Consolidate subagent metric files into one evaluation JSON and render the HTML
  report. Use for kpi-aggregation-evaluator during /evaluate-user-stories.
---

# KPI aggregation

## Parent
user-story-evaluation-agent

## Inputs
- Metric contract YAML
- Pipeline files from story matching, hallucination, coverage, business correctness, acceptance criteria, and epic/feature mapping

## Procedure
1. Build one JSON document in the shape of `.cursor/templates/user-story-evaluation-report-template.md`.
2. Copy each metric from its owner file. Do not rescore.
3. If a contract metric is missing, or `BLOCKED_CONFLICT` is set, stop and return the gap. Do not fill a score.
4. Set `status` to `Draft — Pending Method Review`.
5. Set `assumption_id` to `ASSUMPTION-USEVAL-001`.
6. Write `artifacts/evaluation/.pipeline/<date>-evaluation.json`.
7. Ask the parent to run validate/render on the **allocate-run** paths (never a prior run's HTML):
   ```bash
   python scripts/evaluate_user_stories.py validate --evaluation <evaluation>
   python scripts/evaluate_user_stories.py render \
     --evaluation <evaluation> \
     --html <public_html> \
     --json <public_json>
   ```
8. The script is the only HTML writer. Do not edit the HTML after render.

## Do not
- Change an owner, a formula, or a numerator.
- Add a metric that is not in the contract.
- Drop evidence or transcript refs while consolidating.
