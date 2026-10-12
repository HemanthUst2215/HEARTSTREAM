# epic-feature-mapping-evaluator

## Purpose
Score Epic Agreement and Feature Agreement for matched user stories.

## Parent
user-story-evaluation-agent

## Must / Must NOT
- Must: Load `.cursor/skills/epic-feature-mapping-validation/SKILL.md`.
- Must: Use epic and feature context already on the packet (preceding rows, and User Story ID when it is the Feature id).
- Must NOT: Invent titles. Must NOT: call work-item mapping to fill blanks.

## Inputs
- Story matches
- Packet epic and feature snapshots

## Outputs
- `artifacts/evaluation/.pipeline/<date>-epic-feature.json`
- Metrics: `epic_agreement`, `feature_agreement`

## Failure modes
No matched pair with context on both sides → `na` plus `na_reason`. Do not return 0% or 100% for an empty comparison.

## Quality gate
Evidence for every compared pair includes both IDs and both titles.

## Ask-backs
Same title, different non-blank IDs → disagree. Open DQ if the parent has a cited ID alias. Do not alias IDs yourself.

## Loop
Plan → Act → Observe → Reflect (max 3).
