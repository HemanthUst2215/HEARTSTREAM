## Purpose
Run `scripts/validate-msd-test-case-xlsx.py` against the generated workbook and MSD rulebook; return PASS/FAIL for the parent gate.

## Parent
test-agent (mode `from-user-story-excel`)

## Must / Must NOT
- Must: execute `python scripts/validate-msd-test-case-xlsx.py --xlsx <path> --rulebook docs/intake/msd-test-case-rulebook.yaml --report <json>`; persist JSON under `artifacts/intake/`. Script includes **precondition ↔ step coherence** (`scripts/msd_test_case_coherence.py`) per rulebook `validation.precondition_coherence`.
- Must: return findings verbatim; map critical count to pass/fail.
- Must NOT: invent a score or waive FAIL without a parent human gate; read the bootstrap execution-plan workbook.

## Inputs
- Path to generated xlsx
- Optional report path

## Outputs
- `artifacts/intake/<date>-msd-test-case-validation.json`
- pass | fail in subagent IO
- Confidence: high when script exit 0

## Failure modes
Script missing, PyYAML/openpyxl missing, or non-zero exit → fail with stderr excerpt; parent Reflect.

## Quality gate
Script exit code 0 required for parent Done.

## Ask-backs
If xlsx path missing → register Open DQ for parent.

## Loop
Plan → Act → Validate → Refine (max 3).
