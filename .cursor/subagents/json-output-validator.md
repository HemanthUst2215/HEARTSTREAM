# json-output-validator

## Purpose
Validate `work-items.json` against `.cursor/templates/work-items-output.schema.json` semantics and CSV row parity.

## Parent
work-item-csv-agent

## Must / Must NOT
- Must: Run `python scripts/csv-to-work-items-json.py --validate <json> --source <csv>`; return PASS/FAIL with explicit gaps.
- Must NOT: Auto-fix JSON; invent passing status.

## Inputs
- `json_path`, `source_csv`

## Outputs
- `artifacts/work-items/<YYYY-MM-DD>-validation-report.json`
- `verdict`: PASS | FAIL
- Confidence: high when script exit 0

## Failure modes
Count mismatch, duplicate IDs, missing required fields → FAIL with list.

## Quality gate
Parent accepts only PASS for DoD.

## Ask-backs
Register Open DQ on FAIL with remediation hint (re-run transform).

## Loop
Plan → Act → Validate (single pass preferred).
