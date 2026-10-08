# Audit: /generate-user-stories-from-transcript (one Excel + INVEST separate)

**Date:** 2026-10-08  
**Command:** `/generate-user-stories-from-transcript`  
**Iteration:** 1 of 3  
**Validation:** PASS for deliverable shape (one public Excel; INVEST as a separate CSV)

## What
- Restored `artifacts/intake/2026-10-08-invest-scorecard.csv` (29 User Stories; INVEST not on the workbook).
- Confirmed the only public workbook is `artifacts/intake/2026-10-08-user-stories-from-transcript.xlsx` (stories + EPIC/FEATURE/WORKSHOP ID; one sheet; no INVEST columns).
- Working CSV stays internal: `artifacts/intake/.pipeline/2026-10-08-user-stories-working.csv`.
- Aligned command agents, skills, rulebook `output_paths`, and pipeline C2 so a later run does not emit a public story CSV twin or `*-mapped.xlsx` / `*-mapped.csv`.

## Why
Operator: keep only INVEST as a separate file; one final Excel for stories and IDs.

## How
- INVEST via `invest_scorecard.py` + `export_invest_scorecard_csv` on User Story rows of the working CSV.
- Mapper already writes `--out-xlsx` only; docstring updated to match.
- Writer/skill/BA/orchestrator/rulebook/templates now point the ADO CSV at `.pipeline/<date>-user-stories-working.csv`.

## Validation
| Check | Result | Evidence |
|-------|--------|----------|
| Public Excel count | 1 | `2026-10-08-user-stories-from-transcript.xlsx` |
| INVEST separate | Yes | `2026-10-08-invest-scorecard.csv`; Excel shared strings have EPIC ID and no IndependentScore |
| INVEST scores | 2 Pass / 27 Needs Refinement | Did not invent AC copy to force Pass |
| Layout regression | PASS | `python scripts/test_ado_user_story_csv_layout.py` |
| Mapped twins | Absent | No `*-mapped.csv` / `*-mapped.xlsx` under `artifacts/intake/` |

## Open items
- 27 INVEST Needs Refinement (mostly Testable / Estimable). Reflect without invented microcopy.
- 28 User Stories unmatched (IDs blank). 1 mapped: FEATURE 67562 / EPIC 67557.
- Output-path CONFLICT on earlier canonical files was already resolved by reuse; human may still choose overwrite on a later run.

## Next command
Use `artifacts/intake/2026-10-08-user-stories-from-transcript.xlsx` and the separate INVEST CSV, then `/plan-governed-stories` or `/plan-sprint`.
