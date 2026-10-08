# Audit: /generate-user-stories-from-transcript (resume — INVEST + mapping)

**Date:** 2026-10-08  
**Command:** `/generate-user-stories-from-transcript`  
**Source:** `01. Sales - CE Record to Report UST Led Workshop-20260928-en-US.docx`

## What
Completed remaining DoD on the existing validated ADO CSV: INVEST scorecard + work-item mapping (Excel/CSV + log). Did **not** overwrite the ADO CSV (output-path CONFLICT).

## Why
Operator re-ran the command after mapping/INVEST were added to the contract.

## How
1. Intake safety on docx → **CLEAN** (exit 0).
2. Rulebook present (`docs/intake/user-story-csv-rulebook.yaml`).
3. Output-path gate **CONFLICT** on extraction notes, rows JSON, ADO CSV, validation report. **CLEAR** on invest-scorecard and mapped artifacts.
4. Reused existing ADO CSV (57 rows). Re-validated: **PASS**.
5. INVEST: `invest_scorecard.py` on 29 User Stories → `2026-10-08-invest-scorecard.csv`.
6. Spawned mapping path: `map-user-stories-to-work-items.py` against `artifacts/work-items/` (epic.json, feature.json, work-items.json). Strong unique match only; IDs otherwise blank.

## Validation
- CSV validator: PASS, 57 rows, 0 critical
- Mapping: 29 User Stories in log = 29 User Story rows
- Matched: 1 (`Create install base record…` → FEATURE ID 67562, EPIC ID 67557 from feature parent)
- Unmatched: 28 (below threshold or ambiguous lookalikes, e.g. multiple Partner Onboarding features) — IDs left blank
- INVEST: 2 Pass / 27 Needs Refinement (mostly Testable: no Given/When/Then or must/should in `- ` AC). Did not invent AC copy to force Pass.

## Open Items
- Output-path CONFLICT on canonical ADO files — human may still choose **overwrite** or keep this CSV.
- DQ: INVEST Needs Refinement on 27 stories (rule 13); Reflect without invented microcopy.
- Partner/onboarding/lead stories left unmapped (multiple Features share similar titles across epics).

## Artifacts
- Reused: `artifacts/intake/2026-10-08-user-stories-from-transcript.csv`
- New: `artifacts/intake/2026-10-08-invest-scorecard.csv`
- New: `artifacts/intake/2026-10-08-user-stories-from-transcript-mapped.xlsx`
- New: `artifacts/intake/2026-10-08-user-stories-from-transcript-mapped.csv`
- New: `artifacts/intake/2026-10-08-work-item-mapping-log.json` / `.md`
- This audit: `-v2` (prior audit not overwritten)

## Next command
Human import of the ADO CSV to ADO, then `/plan-governed-stories` or `/plan-sprint`. Use the **mapped.xlsx** for Epic/Feature/Workshop IDs.
