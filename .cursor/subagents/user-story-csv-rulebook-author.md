## Purpose
One-time bootstrap: derive `docs/intake/user-story-csv-rulebook.yaml` from an ADO workshop export CSV (`setup_csv`). Captures column order, work item taxonomy, narrative formats, and validation pointer. Never invoked when rulebook already exists.

## Parent
business-analyst-agent (mode `rulebook-bootstrap`)

## Must / Must NOT
- Must: map every header column to rulebook `csv.column_order`; document work item types, User Story / AC formats, Epic/Feature title patterns, workshop governance columns, Area Path and date formats, and explicit absence of Priority/Story Point columns.
- Must: set `provenance` with behavior_id and bootstrap source locator; point `validation.script` to `scripts/validate-user-story-csv.py`.
- Must NOT: register the bootstrap CSV as a runtime input; invent columns not present in setup export; overwrite an Active rulebook without human harness decision.

## Inputs
- `setup_csv` path (single file)
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
