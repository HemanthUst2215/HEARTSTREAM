# invest-scorecard-evaluator

## Purpose
Evaluate INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable) and produce scorecard rows for `/generate-user-stories-from-transcript` Phase 4. Write **only** `artifacts/intake/<date>-invest-scorecard.csv`. Do **not** add INVEST columns to the story Excel or the working CSV. INVEST stays a separate file.

## Parent
business-analyst-agent

## Must / Must NOT
- Must: Use the same six dimensions and Pass/Needs Refinement semantics as `.cursor/rules/13-business-analysis-invest.mdc`.
- Must NOT: Embed INVEST columns in the story Excel or the working CSV; invent scores without story text.

## Inputs
- stories in draft JSON (title, description, acceptanceCriteria)

## Outputs
- `artifacts/intake/<date>-invest-scorecard.csv`
- Suggested rewrites when `investStatus` is Needs Refinement (Reflect; do not invent copy)

## Quality gate
No critical dimension below 5; overall ≥ 7 for Pass (script defaults).

## Loop
Plan → Act → Observe → Reflect (max 3).
