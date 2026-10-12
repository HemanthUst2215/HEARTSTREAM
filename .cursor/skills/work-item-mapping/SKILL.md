---
name: work-item-mapping
description: >-
  Map generated user stories to Epic/Feature/Workshop IDs from artifacts/work-items
  JSON using strong-match scoring only. Use during /generate-user-stories-from-transcript
  after CSV validation. Public output is one Excel; INVEST stays a separate CSV.
---

# Work item mapping

## When to use
- After `/generate-user-stories-from-transcript` working CSV validates PASS
- Primary: **work-item-mapping-agent**

## Phases
1. Confirm working CSV exists and validator PASS.
2. Confirm `artifacts/work-items/` has `workItems[]` JSON (else blank IDs + Open DQ).
3. Output-path gate on the **single** xlsx only.
4. Run:
   ```bash
   python scripts/map-user-stories-to-work-items.py \
     --csv artifacts/intake/.pipeline/<date>-user-stories-working.csv \
     --work-items-dir artifacts/work-items \
     --out-xlsx artifacts/intake/<date>-user-stories-from-transcript.xlsx \
     --log-json artifacts/intake/.pipeline/<date>-work-item-mapping-log.json
   ```
5. Do **not** write mapped CSV or a second workbook.
6. Do **not** write INVEST into the Excel (`invest-scorecard.csv` is separate).

## Strong-match policy
- Do **not** invent Epic/Feature titles from the transcript. Score each User Story against existing Feature titles in `artifacts/work-items` JSON.
- Write matched catalog Epics and Features into the Excel as rows with their existing `ID` values.
- Put catalog IDs in the rulebook `ID` column. Every User Story row `ID` is a catalog Feature workItemId. Epic and Feature rows keep their own IDs. Do **not** add `EPIC ID` or `FEATURE ID` columns.
- Include a Feature row when its `parent.workItemId` exists as an Epic in the same catalog.
- When several Features share a title, still map the User Story to one existing catalog Feature. Never invent an ID.
- Workshop ID is independent.
- Never invent IDs.

## Must NOT
- Leave a User Story `ID` blank when a related catalog Feature exists
- Edit story narrative fields
- Emit extra Excel/CSV twins of the stories
