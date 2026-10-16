# User story source analysis report

> Shape of `artifacts/evaluation/.pipeline/<date>-manual-source-analysis.json` and
> `<date>-ai-source-analysis.json`.
> `scripts/generate_user_story_source_analysis.py render` is the only writer of the HTML.

| Field | Value |
|-------|-------|
| schema_version | `1.0` |
| kind | `user-story-source-analysis` |
| side | `manual` \| `generated` |
| status | `Draft — Pending Method Review` |
| assumption_id | `ASSUMPTION-USHTML-001` |

## inputs
- `user_story_csv` — rulebook-shaped CSV for this side only
- `transcript_paths[]`, `mom_paths[]`, `preread_paths[]`, `sow_json`
- `unified_knowledge_base` — path to unified KB JSON from source-knowledge-base-unifier

## executive_summary
Counts and `overall_traceability_score` (0–100 display string allowed).

## stories[]
One row per User Story in the CSV (ADO row order). Fields per command contract:
`user_story_id`, `user_story_title`, `feature_name`, `match_type` (USHTML-MATCH-001: No Match iff no supporting excerpt), `derived_sources[]`,
`source_references[]` (`source_type`, `locator`, `excerpt` or `No Supporting Evidence Found`),
`why_generated`, `why_mapped_to_feature`, `supporting_business_context`,
`coverage_assessment`,
`confidence_score`, `recommended_action`.

## feature_traceability_matrix[]
`feature_name`, `workshop_code` (optional), `mapped_user_stories[]`, `coverage_percent` (% of sourced requirements for that annexure covered by stories in this CSV), `missing_requirements[]` (short labels), `requirements_not_in_stories[]` with `requirement`, `source_type`, `source_locator`, `why_not_converted` (shown under each feature topic in HTML).

## source_coverage_summary
`transcript_percent`, `mom_percent`, `preread_percent`, `feature_list_percent` (0–100).

## coverage_gap_analysis
- `feature_requirements_not_in_stories[]`
- `source_requirements_not_captured[]`
- `unmapped_user_stories[]`
- `missing_business_scenarios[]`

Each gap item: `{statement, source_type, source_path, source_locator, confidence}`.

## open_items[]
Pending `ASSUMPTION-USHTML-001` and any `BLOCKED_CONFLICT`.

## HTML sections
Executive summary, per-story detail (expandable), feature traceability matrix,
source coverage summary, coverage and gap analysis, open items.

Manual (`side: manual`) HTML omits **Why generated** and **Why mapped to feature** (fields remain in JSON).
AI-generated HTML shows both; **Why generated** uses multi-paragraph `why_generated` text.
