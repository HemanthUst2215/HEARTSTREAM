---
name: acceptance-criteria-evaluation
description: >-
  Score acceptance-criteria count, quality, and negative or boundary coverage.
  Use for acceptance-criteria-evaluator during /evaluate-user-stories.
---

# Acceptance criteria evaluation

## Parent
user-story-evaluation-agent

## Inputs
- Packet stories (`acceptance_criteria`, `structural.ac_count`, `negative_boundary_signal_lines`)
- Transcript
- Story matches

## Procedure
1. **Acceptance Criteria Count** (`comparison`): manual mean, generated mean, and both totals. A bullet is one non-empty line. Display both means. This metric has no 0–100 score.
2. **Acceptance Criteria Quality** (`score`, 0–100): mean of per-story scores on generated rows. A bullet counts as quality only when it is one observable outcome, testable from the transcript, and the cell uses ASCII `- ` bullets (rulebook). Implementation steps do not raise the score.
3. **Negative and Boundary Coverage:** numerator is generated rows whose criteria include the negative or boundary the transcript states for that requirement. Denominator is generated rows whose transcript span states a negative or boundary. `negative_boundary_signal_lines` are hints, not the denominator. No such span in the transcript → `na` with `na_reason`.

## Output
`artifacts/evaluation/.pipeline/<date>-acceptance-criteria.json`. Owner: `acceptance-criteria-evaluator`.

## Do not
- Treat a lexical "not" as proof the transcript required a negative test.
- Score format compliance of the Description. That metric belongs to business-correctness-evaluator.
