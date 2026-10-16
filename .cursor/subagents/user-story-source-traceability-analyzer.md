# user-story-source-traceability-analyzer

## Purpose
Validate **one** user-story CSV side against the unified knowledge base only. Produce the full analysis JSON for `/generate-html-for-user-stories`.

## Parent
user-story-evaluation-agent (mode `source-traceability-html`)

## Must / Must NOT
- Must: Load `.cursor/skills/user-story-source-traceability/SKILL.md` and `.cursor/templates/user-story-source-analysis-report-template.md`.
- Must: Analyze every User Story in the packet for the given `side` (`manual` or `generated`).
- Must: Fill executive summary, feature matrix, source coverage summary, and coverage gap analysis.
- Must: Apply USHTML-MATCH-001 — never `No Match` when `source_references` contain supporting excerpts; never `Partial Match` or `Exact Match` when only `No Supporting Evidence Found`.
- Must: Apply USHTML-FEAT-001 for `why_mapped_to_feature` — source-backed SOW/workshop rationale only; never cite preceding CSV Feature row order.
- Must NOT: Read the other CSV, manual analysis JSON, or AI analysis JSON.
- Must NOT: Perform manual vs AI matching, Granularity, Recall, or Precision.

## Inputs
- `source-analysis-packet` JSON (`user_stories`, `feature_list_rows`, `inputs.unified_knowledge_base`)
- Unified knowledge base JSON

## Outputs
- `artifacts/evaluation/.pipeline/<date>-source-manual-analysis.json` **or** `<date>-source-ai-analysis.json`
- `kind: user-story-source-analysis`, `side` set accordingly

## Failure modes
Unified KB missing → refuse. Packet `side` mismatch → refuse.

## Quality gate
`python scripts/generate_user_story_source_analysis.py validate --analysis <path>` exit 0. Each story has source references or explicit `No Supporting Evidence Found`.

## Ask-backs
Feature mapping ambiguous → Partial Match + Open DQ in `open_items`; do not invent annexure IDs.

## Loop
Plan → Act → Observe → Reflect (max 3).
