## Purpose
Case objects (role keys) → MSD E2E xlsx via the canonical writer. Coverage metrics and ISV lookup sheets are derived by the script.

## Parent
test-agent (mode `from-user-story-excel`)

## Must / Must NOT
- Must: persist `artifacts/intake/<date>-msd-test-case-rows.json` using the shape in `msd-test-case-rows-json-template.md`, then run
  `python scripts/msd_test_case_xlsx.py write --json <rows.json> --out artifacts/intake/<date>-msd-e2e-test-cases.xlsx --working-csv artifacts/intake/.pipeline/<date>-msd-test-cases-working.csv`.
- Must: pass `project_label` from `.cursor/config.yaml` `project.name` when it is not a placeholder; otherwise omit and let the rulebook fallback apply.
- Must NOT: hand-build xlsx/csv text; add/remove sheets or columns; copy bootstrap workbook values; fill Actual Result, Defect ID, or non-default Status.

## Inputs
- Case array from msd-test-case-extractor
- MSD rulebook path

## Outputs
- Public xlsx at rulebook `output_paths.public_xlsx`
- Optional working register CSV
- Row/case/scenario counts in subagent IO
- Confidence: high when writer exit 0

## Failure modes
Writer cannot encode a row → fail with case/step index; parent must fix content, not schema.

## Quality gate
Writer exit 0; workbook exists; register row count equals the sum of steps.

## Ask-backs
If rulebook missing → escalate to parent for bootstrap; do not invent headers.

## Loop
Plan → Act → Validate → Refine (max 3).
