# Audit — `/generate-user-stories-from-transcript` (Marketing WS-03)

| Field | Value |
|-------|-------|
| Date | 2026-10-16 |
| Command | generate-user-stories-from-transcript |
| Task | marketing-ws03 (Day 03 Customer Insights) |

## What

Generated ADO user-story Excel and separate INVEST scorecard from workshop transcript, MoM PDF, and Marketing Day 03 pre-read PPTX.

## Why

Operator requested user stories for the 30-Sep-2026 Marketing / Customer Insights workshop with full prerequisite, MoM, and SOW feature mapping.

## How

1. Output-path gate: **CLEAR** (`2026-10-16` artifact set).
2. Normalized inputs:
   - Transcript: `scripts/extract-docx-text.py` → `artifacts/intake/2026-10-16-transcript.txt`
   - Prerequisite: PPTX extract → `artifacts/intake/.pipeline/2026-10-16-marketing-ws03-prerequisite.txt`
   - MoM: PDF extract → `artifacts/intake/.pipeline/2026-10-16-marketing-ws03-mom.txt`
3. Intake safety on extracted text: **exit 0 CLEAN** (binary sources scanned via extracts).
4. Prerequisite KB MD/JSON, extraction notes, 16-row `user-story-rows.json` (13 User Stories, 2 Issues, 1 Workshop) with `mom_locator` / `mom_source_path` on stories.
5. `ado_user_story_csv.py write` → working CSV; scope + entity + CSV validators **PASS**.
6. INVEST scorecard via `user_story_pipeline.invest_scorecard`.
7. `map-user-stories-to-sow-features.py` → public Excel.

## Validation

| Gate | Result |
|------|--------|
| Output-path gate | CLEAR |
| Intake safety | PASS (0) |
| Workshop scope + MoM fields | PASS |
| MSD365 business entity | PASS |
| CSV rulebook | PASS |
| SOW mapping | 12 matched / 1 unmatched |

## Public outputs

- `artifacts/intake/2026-10-16-user-stories-from-transcript.xlsx`
- `artifacts/intake/2026-10-16-invest-scorecard.csv`

## Open items

| ID | Item | Owner |
|----|------|-------|
| DQ-MAP-001 | User story *Identify distributors serving multiple vertical markets* unmatched to SOW feature (token score 17.3 &lt; 62.0); appears in Excel unmatched block | BA / mapping review |
| DQ-INV-001 | INVEST Testable dimension = 4 on multiple stories (Needs Refinement); consider stronger Given/When/Then AC in a refinement pass | BA |

## Next command

`/generate-test-cases-from-user-stories` with `artifacts/intake/2026-10-16-user-stories-from-transcript.xlsx`, or `/plan-governed-stories` / `/plan-sprint`.
