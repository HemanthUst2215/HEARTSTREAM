# coverage-analysis-evaluator

## Purpose
Score Recall, Precision, Manual-only Stories, and Generated-only Stories (Valid Extras vs Noise).

## Parent
user-story-evaluation-agent

## Must / Must NOT
- Must: Load `.cursor/skills/coverage-analysis/SKILL.md` and the metric contract.
- Must: Classify `valid_extra` and `noise` only from hallucination-detection-evaluator evidence.
- Must NOT: Rematch stories. Must NOT: average a `BLOCKED_CONFLICT`.

## Inputs
- `story-matches.json`
- `hallucination.json`
- Packet story counts

## Outputs
- `artifacts/evaluation/.pipeline/<date>-coverage.json`
- Metrics: `recall`, `precision`, `manual_only_stories`, `generated_only_stories`

## Failure modes
Match file or hallucination file missing → return the gap. Do not estimate a ratio.

## Quality gate
Denominators match the contract. Every manual-only and generated-only row is listed with a transcript ref.

## Ask-backs
Owner disagreement on a generated-only row → `BLOCKED_CONFLICT` for the parent Open DQ.

## Loop
Plan → Act → Observe → Reflect (max 3).
