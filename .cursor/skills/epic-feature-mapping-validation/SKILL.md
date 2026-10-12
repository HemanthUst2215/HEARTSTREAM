---
name: epic-feature-mapping-validation
description: >-
  Score Epic Agreement and Feature Agreement on matched user stories.
  Use for epic-feature-mapping-evaluator during /evaluate-user-stories.
---

# Epic and Feature mapping validation

## Parent
user-story-evaluation-agent

## Inputs
- Story matches
- Packet epic and feature context on each story (nearest preceding Epic row and Feature row; User Story `ID` when it carries the Feature work item id)

## Procedure
Apply `epic_agreement` and `feature_agreement` exactly as written in `.cursor/templates/user-story-evaluation-metrics.yaml`.

- Compare only matched pairs.
- Equal non-blank IDs agree.
- Both IDs blank and titles identical agree.
- Context on only one side disagrees.
- No comparable pair → `na` with `na_reason`.
- Do not invent an Epic or Feature title when the CSV has no preceding row.

Record the two IDs and titles in evidence for every compared pair.

## Output
`artifacts/evaluation/.pipeline/<date>-epic-feature.json`. Owner: `epic-feature-mapping-evaluator`.

## Do not
- Rematch stories.
- Search `artifacts/work-items` to fill a blank the CSV does not contain. Catalog lookup is `/generate-user-stories-from-transcript`, not this command.
