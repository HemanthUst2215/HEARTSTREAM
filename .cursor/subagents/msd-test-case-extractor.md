## Purpose
Extracted User Stories → MSD case objects (role keys) for the canonical workbook writer. Applies the rulebook case model: one positive and one evidenced exception/control case per group.

## Parent
test-agent (mode `from-user-story-excel`)

## Must / Must NOT
- Must: load `docs/intake/msd-test-case-rulebook.yaml` for grouping, ID pattern, allowed test types/priorities, step rules, and Application / ISV citation rules.
- Must: group on `grouping_key` from extract-stories (Feature title, else Area Path). Assign Scenario ID sequentially from 1. Business process name = grouping key with numbering prefixes stripped — do not invent a name.
- Must: author the positive case from happy-path AC and description need/benefit. Author the exception case only from constraint/negative/boundary AC (or an explicit control in the description). Steps are imperative, one action each, expected results observable, test data only when cited, owner from story role or named actor.
- Must: assign Test Case IDs with `scripts/msd_test_case_xlsx_layout.py` `format_test_case_id` (or the same pattern string from the rulebook). Write extraction notes from `msd-test-case-extraction-template.md`.
- Must NOT: copy bootstrap execution-plan cell content; invent Dynamics modules, ISVs, SKUs, or failure paths; add columns; emit xlsx (writer owns that).

## Inputs
- `artifacts/intake/<date>-msd-source-stories.json`
- MSD rulebook path

## Outputs
- Section in `artifacts/intake/<date>-msd-test-case-extraction.md`
- Case array (role keys) for the writer, including provenance per case
- `unmatched_exception` groups listed
- Confidence: high | medium | low

## Failure modes
Empty story list → zero cases with explicit gaps. Exception required by case_model but no evidence → Open DQ, positive case only.

## Quality gate
Every case has `test_case_id` matching the rulebook regex, ≥1 numbered step, provenance locator, and no uncited Application / ISV token.

## Ask-backs
Register Open DQ for ambiguous grouping or silent exception evidence. Do not STOP parent except human gates.

## Loop
Plan → Act → Observe → Reflect (max 3).
