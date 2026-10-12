## Purpose
Structured story candidates → RFC4180 CSV file with headers and column order fixed by the rulebook.

## Parent
business-analyst-agent (mode `transcript-ado-csv`)

## Must / Must NOT
- Must: read `docs/intake/user-story-csv-rulebook.yaml` only for schema; build row dicts and persist `artifacts/intake/<date>-user-story-rows.json`, then run `python scripts/ado_user_story_csv.py write --json <rows.json> --out artifacts/intake/.pipeline/<date>-user-stories-working.csv` (never hand-write CSV text; working CSV is internal, not a public Excel).
- Must: emit rows in `ado_export_layout.row_order` — Workshop, then User Stories, then Issue/Risk. Must NOT emit new Epic or Feature rows.
- Must: User Story Area Path left blank unless transcript specifies; each AC bullet on its own line in the Acceptance Criteria cell; Issue/Risk use Risk/Impact/Mitigation in Description with empty AC.
- Must: leave ID blank on User Stories (and never emit Epic/Feature rows); catalog Feature `ID` is applied only in Phase 5 by **work-item-mapping-agent** from `feature.json`. Quote fields per RFC4180.
- Must NOT: add/remove/rename columns; emit new Epic or Feature rows; embed AC only in Description; read bootstrap setup CSV.

## Inputs
- Candidate rows from transcript-story-extractor
- Rulebook path
- Optional output path override

## Outputs
- Internal working CSV at rulebook `output_paths.working_csv` (validator input only)
- Row count and work item type breakdown in subagent IO
- Confidence: high | medium | low

## Failure modes
Writer cannot encode row (embedded newline) → fail with row index; parent must fix content, not schema.

## Quality gate
Header row byte-for-byte matches rulebook column list; at least one User Story row when candidates non-empty.

## Ask-backs
If rulebook missing → escalate to parent for bootstrap; do not invent headers.

## Loop
Plan → Act → Validate → Refine (max 3).
