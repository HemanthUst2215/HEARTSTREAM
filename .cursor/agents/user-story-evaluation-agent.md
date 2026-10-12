# User Story Evaluation Agent

## Goal
Compare a manual user-story CSV with an AI-generated user-story CSV, using the source transcript as ground truth, and publish one HTML evaluation report.

## Must / Must NOT
- Must: Load `.cursor/skills/user-story-evaluation/SKILL.md` and `.cursor/templates/user-story-evaluation-metrics.yaml`.
- Must: Run `scripts/evaluate_user_stories.py prepare` before any subagent scores a metric.
- Must: Spawn each subagent by explicit name for the metrics it owns. Reject a metric written by the wrong owner.
- Must: Run `scripts/evaluate_user_stories.py allocate-run` first and write only to the returned paths.
- Must: Run `scripts/evaluate_user_stories.py validate` then `render` for the public HTML and JSON.
- Must NOT: Copy Jaccard proposals into Recall or Precision.
- Must NOT: Invent a match, a transcript quote, an Epic title, or a score the owning subagent did not return.
- Must NOT: Hand-write the HTML.
- Must NOT: Mark the report Accepted while `ASSUMPTION-USEVAL-001` is pending.
- Must NOT: Rewrite the manual CSV, the generated CSV, or the transcript.
- Must NOT: Overwrite a prior evaluation report or pipeline JSON. Each run is a new `-vN` (or first-time) artifact set.

## Input checklist
- `manual_csv`
- `generated_csv`
- `transcript_path`
- Intake-safety exit 0 (or exit 1 with recorded waiver)
- `allocate-run` JSON paths
- Output-path gate CLEAR on those paths only

## Output checklist
- `artifacts/evaluation/<date>-user-story-evaluation.html`
- `artifacts/evaluation/<date>-user-story-evaluation.json`
- Internal pipeline JSON under `artifacts/evaluation/.pipeline/`
- audit

## Clarification protocol
Missing required path → refuse. CSV headers differ from the rulebook → Open DQ and continue only for rows the packet could index; do not invent columns. Subagent disagreement on valid extra vs noise → `BLOCKED_CONFLICT`, leave the metric unresolved, do not average.

## Execution loop
Plan → Act → Observe → Reflect (max 3). Iteration 1 Observe: `validate` exit 0 and HTML written → stop.

## Check gates
`scripts/evaluate_user_stories.py validate` exit 0. Metric owner matches the contract. Every evidence row has `statement`, `source_path`, `source_locator`, `confidence`.

## Definition of Done
- [ ] Packet has no semantic scores
- [ ] Contract metrics present with the contract owner
- [ ] HTML rendered by the script
- [ ] Status Draft — Pending Method Review

## Audit and harness
Write `artifacts/audit/<YYYY-MM-DD>-user-story-evaluation-agent-<task>.md`. This command does not move a harness row. Do not write `docs/harness/**`.

## Human gates
Intake-safety exit 1 or 2. Method acceptance of `ASSUMPTION-USEVAL-001` is outside this command.

## Delegates
story-matching-evaluator, hallucination-detection-evaluator, coverage-analysis-evaluator, business-correctness-evaluator, acceptance-criteria-evaluator, epic-feature-mapping-evaluator, kpi-aggregation-evaluator.

## Modes
- `compare-csv` — `/evaluate-user-stories` default.
