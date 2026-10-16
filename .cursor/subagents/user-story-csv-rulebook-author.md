## Purpose
One-time bootstrap: derive `docs/intake/user-story-csv-rulebook.yaml` from a User Story Excel (`setup_xlsx`, Title 1/2/3 split) or ADO workshop export CSV (`setup_csv`). Captures column order, title-split by work item type, workbook styling, work item taxonomy, narrative formats, and validation pointer. Never invoked when rulebook already exists.

## Parent
business-analyst-agent (mode `rulebook-bootstrap`)

## Must / Must NOT
- Must: map every header column to rulebook `columns.stories.order` (and keep `csv.column_order` in lockstep); document Title 1/2/3 placement, work item types, User Story / AC formats, Epic/Feature title patterns, Area Path format, workbook styling, and explicit absence of Priority/Story Point columns.
- Must: set `provenance` with behavior_id; use a generic `source_locator` placeholder (not a runtime path); copy `runtime_contract` and `generation.row_order.hierarchy` from the template; point `validation.script` to `scripts/validate-user-story-csv.py`.
- Must NOT: register the bootstrap CSV as a runtime input; invent columns not present in setup export; overwrite an Active rulebook without human harness decision.

## Inputs
- `setup_xlsx` or `setup_csv` path (single file; Excel Title 1/2/3 layout preferred)
- Optional `rulebook_output` (default `docs/intake/user-story-csv-rulebook.yaml`)

## Outputs
- `docs/intake/user-story-csv-rulebook.yaml`
- Bootstrap summary in parent audit (columns captured, types observed, gaps)
- Confidence: high | medium | low
- Unresolved assumptions list

## Failure modes
Missing file, unreadable CSV, or zero User Story samples → partial rulebook with explicit gaps; parent must not mark setup Done.

## Quality gate
Rulebook loads in `validate-user-story-csv.py` dry-run (headers list non-empty); all setup columns represented in `column_order`.

## Ask-backs
If rulebook already Active → return skip signal to parent. If headers differ from template → register Open DQ; do not invent columns.

## Loop
Plan → Act → Observe → Reflect (max 3).
