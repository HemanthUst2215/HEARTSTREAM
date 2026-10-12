## Purpose
One-time bootstrap: derive `docs/intake/msd-test-case-rulebook.yaml` from an E2E test-execution workbook (`setup_xlsx`). Captures sheet names, column order, column roles, ID patterns, case model, enums, and validation pointer. Never invoked when the rulebook already exists.

## Parent
test-agent (mode `rulebook-bootstrap`)

## Must / Must NOT
- Must: map every bootstrap header to rulebook `columns.*.order`; document sheet visibility, freeze panes, title/subtitle row numbers, register grain (one row per step), case-level vs step-level vs execution columns, ID regex, test-type/priority/status enums, and the Design Basis case model as generation logic.
- Must: set `provenance` with behavior_id and bootstrap source locator; point `validation.script` to `scripts/validate-msd-test-case-xlsx.py`.
- Must: record **patterns and rules only**. Do not copy bootstrap process names, step text, titles, or ISV product lists into the rulebook as runtime catalogs.
- Must NOT: register the bootstrap workbook as a runtime input; invent columns not present in the setup export; overwrite an Active rulebook without a human harness decision.

## Inputs
- `setup_xlsx` path (single workbook)
- Optional `rulebook_output` (default `docs/intake/msd-test-case-rulebook.yaml`)

## Outputs
- `docs/intake/msd-test-case-rulebook.yaml`
- Bootstrap summary in parent audit (sheets captured, headers, enums, gaps)
- Confidence: high | medium | low
- Unresolved assumptions list

## Failure modes
Missing file, unreadable xlsx, or zero register rows → partial rulebook with explicit gaps; parent must not mark setup Done.

## Quality gate
Rulebook loads in `validate-msd-test-case-xlsx.py` (file exists, `columns.register.order` non-empty); all setup register columns represented in `column_order`.

## Ask-backs
If rulebook already Active → return skip signal to parent. If headers differ from template → register Open DQ; do not invent columns.

## Loop
Plan → Act → Observe → Reflect (max 3).
