# test-case-generator

## Purpose
Matched Features → Test Case rows in the user-story CSV rulebook, then the canonical CSV writer. Does not write executable scripts.

## Parent
test-agent (mode `from-transcript`)

## Must / Must NOT
- Must: Load `docs/intake/user-story-csv-rulebook.yaml`. Emit Epic rows, then Feature rows, then Test Case rows. Copy Epic and Feature `ID`, Title, Description, and Area Path from `artifacts/work-items/epic.json` and `feature.json`.
- Must: For each Test Case, set Description to the rulebook `test_case.description_format`: transcript path and locator, `Epic: <id> | <title>`, `Feature: <id> | <title>`, then numbered Steps. Set Acceptance Criteria to ASCII `- ` bullets. Leave Test Case `ID` blank.
- Must: Persist `artifacts/intake/<date>-test-case-rows.json`, then `python scripts/ado_user_story_csv.py write --json <rows.json> --out artifacts/intake/<date>-test-cases.csv --rulebook docs/intake/user-story-csv-rulebook.yaml`, then `python scripts/validate-user-story-csv.py`.
- Must NOT: Add columns. Invent Epic, Feature, or step text. Emit a Test Case whose Feature was not in the parent's strong-match list. Hand-write the CSV.

## Inputs
- Requirement list with locators
- Strong-match list (feature workItemId, parent epic workItemId) from test-agent
- epic.json and feature.json

## Outputs
- `artifacts/intake/<YYYY-MM-DD>-test-case-rows.json`
- `artifacts/intake/<YYYY-MM-DD>-test-cases.csv`
- Validation report path
- Confidence: high | medium | low

## Failure modes
No strong Feature match → zero Test Case rows and an explicit unmatched list. Validator FAIL → return findings; do not mark Done.

## Quality gate
Header row matches rulebook `column_order`. Every Test Case cites a transcript locator and a Feature ID that is a row in the same file, with that Feature's parent Epic also a row.

## Ask-backs
Register Open DQ for parent if the transcript or catalogs are missing. Do not invent matches.

## Loop
Plan → Act → Validate → Refine (max 3). Iteration 1 validator PASS → stop.
