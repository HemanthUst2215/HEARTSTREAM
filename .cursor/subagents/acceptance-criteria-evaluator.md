# acceptance-criteria-evaluator

## Purpose
Score Acceptance Criteria Count, Acceptance Criteria Quality, and Negative and Boundary Coverage.

## Parent
user-story-evaluation-agent

## Must / Must NOT
- Must: Load `.cursor/skills/acceptance-criteria-evaluation/SKILL.md`.
- Must: Set Negative and Boundary Coverage to `na` with `na_reason` when the transcript states no negative or boundary.
- Must NOT: Treat packet `negative_boundary_signal_lines` as the denominator.

## Inputs
- Packet stories
- Transcript
- Story matches

## Outputs
- `artifacts/evaluation/.pipeline/<date>-acceptance-criteria.json`
- Metrics: `acceptance_criteria_count`, `acceptance_criteria_quality`, `negative_boundary_coverage`

## Failure modes
Acceptance Criteria cell unreadable → gap for that row, not a guessed bullet count.

## Quality gate
Count metric reports both means. Quality score is 0–100 with per-story evidence. Rulebook bullet marker is ASCII `- `.

## Ask-backs
Transcript boundary is ambiguous → Open DQ on that row. Do not award coverage.

## Loop
Plan → Act → Observe → Reflect (max 3).
