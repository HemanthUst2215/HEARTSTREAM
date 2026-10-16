# Work Item Mapping Agent



## Goal

During `/generate-user-stories-from-transcript`, load **`SOW.json`**, match each User Story to SOW features using generic similarity (and `prerequisite_refs` when row JSON is available), and write the public Excel in **Workshop → Feature → User Stories** hierarchy. **No Epic rows.** Do not use `epic.json` or `feature.json`.



## Must / Must NOT

- Must: Load `artifacts/work-items/SOW.json` (path from `work_item_mapping.sow_json` in config).

- Must: Run `scripts/map-user-stories-to-sow-features.py` (canonical for `feature_source: sow_json`).

- Must: Leave User Story `ID` blank; place each matched story immediately under its SOW Feature row.

- Must: Feature rows use Title 2 = `<Annexure ID minutes> - <topic>`, Description = topic, **blank ID**, Annexure ID1 = minutes. **Workshop** rows keep Annexure ID1 **empty**.

- Must: Write exactly one workbook: `artifacts/intake/<date>-user-stories-from-transcript.xlsx`.

- Must NOT: Load or reference `epic.json` / `feature.json` for mapping; insert Epic rows; put catalog numeric IDs in Feature `ID`; modify story narrative fields; write INVEST into the Excel.



## Input checklist

- Internal working CSV (validator PASS)

- `SOW.json`

- Optional `user-story-rows.json` for `prerequisite_refs`

- Thresholds: `.cursor/config.yaml` → `work_item_mapping`



## Output checklist

- **Public:** `artifacts/intake/<date>-user-stories-from-transcript.xlsx`

- **Internal:** `artifacts/intake/.pipeline/<date>-work-item-mapping-log.json`



## Clarification protocol

Missing or empty `SOW.json` → register Open DQ; write Excel without Feature hierarchy (stories only).



## Execution loop

Plan → Act → Observe → Reflect (max 3). Iteration 1 Observe: script exit 0 → stop.



## Check gates

- Output-path gate on the **one** xlsx

- Mapping log entry count equals source User Story count



## Definition of Done

- [ ] One Excel written (Workshop → SOW Feature → User Stories)

- [ ] Feature rows: blank `ID`, Annexure ID1 set, Title 2 / Description per SOW rulebook

- [ ] No Epic rows



## Delegates

`work-item-hierarchy-matcher` (SOW mode)



## Modes

- `map-transcript-csv` — after validator PASS

- `remap` — when `SOW.json` is refreshed


