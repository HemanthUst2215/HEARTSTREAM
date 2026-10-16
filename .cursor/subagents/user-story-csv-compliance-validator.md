## Purpose
Run `scripts/validate-user-story-csv.py` against generated CSV and rulebook; return PASS/FAIL for parent gate.

## Parent
business-analyst-agent (mode `transcript-ado-csv`)

## Must / Must NOT
- Must: execute `python scripts/validate-user-story-csv.py --csv <path> --rulebook docs/intake/user-story-csv-rulebook.yaml --report <json>`; persist JSON report under `artifacts/intake/`. Validator enforces `ado_export_layout` (section order, Title 1/2/3 split, multiline AC, Issue/Risk shape).
- Must: return findings verbatim; map critical count to pass/fail.
- Must NOT: invent a score or waive FAIL without parent human gate; read bootstrap setup CSV.

## Inputs
- Path to generated CSV
- Optional report path

## Outputs
- `artifacts/intake/<date>-user-story-csv-validation.json`
- pass | fail in subagent IO
- Confidence: high when script exit 0

## Failure modes
Script missing, PyYAML missing, or non-zero exit → fail with stderr excerpt; parent Reflect.

## Quality gate
Script exit code 0 required for parent Done.

## Ask-backs
If CSV path missing → register Open DQ for parent.

## Loop
Plan → Act → Validate → Refine (max 3).
