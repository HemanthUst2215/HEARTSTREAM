# Audit — User Story rulebook Excel layout alignment

| Field | Value |
|-------|-------|
| **Date** | 2026-10-13 |
| **Agent** | business-analyst-agent (rulebook refactor, not a public command run) |
| **Iteration** | 1 |
| **Status** | Done |

## What

Reorganized `docs/intake/user-story-csv-rulebook.yaml` (schema 2.0, `ado-user-story-xlsx-v2`) so the column contract, title split, sheet styling, and YAML sections match the User Story Excel layout (State, ID, Work Item Type, Title 1/2/3, Assigned To, Area Path, Description, Acceptance Criteria, Annexure ID1, Fit Gap Status, User Story Type).

Writers, validators, mapping, evaluation, and the bootstrap template now bind to that layout. Legacy JSON keys that still send `Title` are projected into the type-specific Title 1/2/3 cell.

## Why

The previous rulebook described a single `Title` column plus workshop-governance fields from an older CSV bootstrap. Generated work and downstream MSD extract need the same structure as the workshop User Story Excel, without copying that workbook's domain content.

## How

- Layout bootstrap: `Finance User Stories- Workshop -WS-02.xlsx` (not a runtime input).
- Preserved generation rules: As-a / I-need / so-that Description; ASCII `- ` AC bullets; catalog-only Epic/Feature; User Story ID = Feature workItemId after mapping; no Priority/Story Points; INVEST stays a separate CSV; working CSV → validate → map → public xlsx.
- Dropped from the column contract (not from anti-invention policy): Task Type1, Start Date, MoM / action-item / SOW / data-migration Yes-No columns.
- Public xlsx styling (Aptos Narrow 9pt, wrap, hidden Assigned To, workshop yellow highlight) lives in `workbook.styling` and `scripts/ado_user_story_csv_layout.py`.

## Validation

| Check | Result |
|-------|--------|
| `python scripts/test_ado_user_story_csv_layout.py` | PASS |
| `python scripts/test_map_user_stories_to_work_items.py` | PASS |
| `python scripts/test_msd_test_case_xlsx_layout.py` | PASS |
| `python scripts/test_evaluate_user_stories.py` | PASS |

## Open Items

- Existing dated working CSVs / public Excels that used a single `Title` column are not rewritten. New `/generate-user-stories-from-transcript` runs emit Title 1/2/3.
- Inbound numbered AC lists are accepted as source evidence; generated output still uses `- ` bullets (generation rule preserved).

## Next command

No pipeline phase change. Next user-story run: `/generate-user-stories-from-transcript`.
