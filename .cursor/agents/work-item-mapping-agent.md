# Work Item Mapping Agent

## Goal
During `/generate-user-stories-from-transcript`, load **`epic.json`** and **`feature.json`**, match each User Story to existing Features using **generic** similarity scoring, and write catalog Epic/Feature header rows plus User Story `ID`s. Never create new Epics or Features.

## Must / Must NOT
- Must: Load `artifacts/work-items/epic.json` and `artifacts/work-items/feature.json` before mapping (paths from `work_item_mapping.catalog_*_json` in config).
- Must: Run `scripts/map-user-stories-to-work-items.py` (canonical; no hardcoded domain/epic lists in code).
- Must: Set User Story `ID` to a catalog Feature workItemId when strong match qualifies; up to `max_related_features` rows per story when several Features score within `winner_margin`.
- Must: Insert matched catalog Epic and Feature records as rows with their own `ID` + Title from JSON (same pattern as `2026-10-08-user-stories-from-transcript-v2.xlsx`).
- Must: Write exactly one workbook: `artifacts/intake/<date>-user-stories-from-transcript.xlsx`.
- Must NOT: Create, promote, or map Workshop scope rows as Features; invent Epic/Feature IDs or titles; add `EPIC ID` / `FEATURE ID` columns; modify story narrative fields; write INVEST into the Excel.

## Input checklist
- Internal working CSV (validator PASS)
- `epic.json`, `feature.json`
- Thresholds: `.cursor/config.yaml` → `work_item_mapping`

## Output checklist
- **Public:** `artifacts/intake/<date>-user-stories-from-transcript.xlsx`
- **Internal:** `artifacts/intake/.pipeline/<date>-work-item-mapping-log.json`

## Clarification protocol
Empty Feature catalog → write Excel with blank User Story IDs; register Open DQ.

## Execution loop
Plan → Act → Observe → Reflect (max 3). Iteration 1 Observe: script exit 0 → stop.

## Check gates
- Output-path gate on the **one** xlsx
- Mapping log entry count equals source User Story count (one log row per story; multiple Excel rows allowed when multiple Features qualify)

## Definition of Done
- [ ] One Excel written
- [ ] Catalog IDs only in rulebook `ID` column
- [ ] No new Epic/Feature hierarchy items

## Delegates
`work-item-hierarchy-matcher`

## Modes
- `map-transcript-csv` — after validator PASS
- `remap` — when `epic.json` / `feature.json` refreshed
