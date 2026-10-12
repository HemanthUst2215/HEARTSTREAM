# Work Item Mapping Agent

## Goal
During `/generate-user-stories-from-transcript`, scan `artifacts/work-items/**/*.json`, match each User Story to **existing** Features, and write those catalog **Epic and Feature rows with their ADO `ID`**. Do not add `EPIC ID` or `FEATURE ID` columns. INVEST is **not** this agent's file.

## Must / Must NOT
- Must: Load every `*.json` under `artifacts/work-items/` that contains a `workItems[]` array.
- Must: Set every User Story ID to a catalog Feature workItemId. Leave it blank only when no catalog Feature relates.
- Must: Insert matched catalog Epic and Feature records as rows with their own `ID` + Title from JSON. On each matched User Story, set `ID` to that Feature's workItemId (do not invent titles; do not add EPIC ID / FEATURE ID columns).
- Must: Match a User Story to a catalog Feature only when that Feature uniquely matches **and** its parent Epic exists in the JSON.
- Must: Write exactly one workbook: `artifacts/intake/<date>-user-stories-from-transcript.xlsx`.
- Must: Run `python scripts/map-user-stories-to-work-items.py` (canonical).
- Must NOT: Write `*-mapped.csv`, a second `*-mapped.xlsx`, or a story CSV twin.
- Must NOT: Write or embed the INVEST scorecard (that stays `artifacts/intake/<date>-invest-scorecard.csv` from invest-scorecard-evaluator).
- Must NOT: Modify Title, Description, Acceptance Criteria, or other generated fields.
- Must NOT: Invent IDs.

## Input checklist
- Internal working CSV (validator PASS)
- `artifacts/work-items/*.json`
- Thresholds: `.cursor/config.yaml` → `work_item_mapping`

## Output checklist
- **Public:** `artifacts/intake/<date>-user-stories-from-transcript.xlsx`
- **Internal:** `artifacts/intake/.pipeline/<date>-work-item-mapping-log.json`

## Clarification protocol
Empty work-items catalog → still write the one Excel with blank IDs; Open DQ.

## Execution loop
Plan → Act → Observe → Reflect (max 3). Iteration 1 Observe: script exit 0 → stop.

## Check gates
- Output-path gate on the **one** xlsx
- Mapping log User Story count equals source User Story count

## Definition of Done
- [ ] One Excel written
- [ ] No `EPIC ID` / `FEATURE ID` columns; catalog IDs only in `ID`
- [ ] No extra story CSV/Excel twins
- [ ] INVEST not in this workbook

## Delegates
`work-item-hierarchy-matcher`

## Modes
- `map-transcript-csv` — after validator PASS
- `remap` — when work-items JSON was refreshed
