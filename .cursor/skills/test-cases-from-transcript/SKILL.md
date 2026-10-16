---
name: test-cases-from-transcript
description: >-
  Transcript requirements matched to epic.json and feature.json, then a rulebook
  CSV of test cases. Use for /expand-test-coverage and test-agent mode from-transcript.
---

# Test cases from transcript

## When
`/expand-test-coverage` before any test case is written.

## Steps
1. Intake-safety scan the transcript (`scripts/intake-safety-scan.py`). Exit 2 stops. Exit 1 stops until redaction or waiver.
2. Read the transcript. Record each requirement with a locator. Do not write cases in this step.
3. Load `artifacts/work-items/feature.json` and `artifacts/work-items/epic.json`.
4. Match each requirement to Feature title and `description.plainText`. Keep a match only when it meets `.cursor/config.yaml` `work_item_mapping.strong_threshold`, wins by `winner_margin`, and `parent.workItemId` is an Epic in epic.json.
5. Generate test cases only for those Features. Traceability on every Test Case is Transcript locator → Epic id → Feature id → Test Case title.
6. Write row JSON, then:
   ```bash
   python scripts/ado_user_story_csv.py write --json artifacts/intake/<date>-test-case-rows.json --out artifacts/intake/<date>-test-cases.csv --rulebook docs/intake/user-story-csv-rulebook.yaml
   python scripts/validate-user-story-csv.py --csv artifacts/intake/<date>-test-cases.csv --report artifacts/intake/<date>-test-case-validation.json
   ```
7. Columns and Test Case Description shape come from `docs/intake/user-story-csv-rulebook.yaml` (`columns.stories.order` / `csv.column_order` and `test_case`). Epic → Title 1; Feature → Title 2; Test Case → Title 3. Do not add columns.

## Must NOT
- Cases for Features that did not strongly match
- Invented Epic or Feature records
- A second case format (markdown matrix is not this command's output)
