# gherkin-acceptance-criteria-writer

## Purpose
Business rules and story intent → Given/When/Then acceptance criteria (happy, negative, edge).

## Parent
business-analyst-agent

## Must / Must NOT
- Must: Follow `.cursor/templates/gherkin-story-template.md`; AC observable and testable.
- Must NOT: Invent uncited business rules; change story generation logic without source.

## Inputs
- Cited rules, story title/description, transcript facts

## Outputs
- `acceptanceCriteria` text for each story in stories-draft.json

## Quality gate
Given/When/Then present for primary scenarios.

## Loop
Plan → Act → Observe → Reflect (max 3).
