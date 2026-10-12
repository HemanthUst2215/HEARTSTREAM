---
name: msd-test-cases-from-user-stories
description: >-
  User Story Excel → MSD E2E test-case workbook using the stored MSD rulebook.
  Use for /generate-test-cases-from-user-stories. Never read the bootstrap
  execution-plan Excel at runtime.
---

# MSD test cases from User Story Excel

## Preconditions

1. **MSD rulebook exists:** `docs/intake/msd-test-case-rulebook.yaml` (status Active).
2. **Source story rulebook exists:** `docs/intake/user-story-csv-rulebook.yaml`.
3. If the MSD rulebook is missing, run **one-time bootstrap** only: test-agent mode `rulebook-bootstrap` + `msd-test-case-rulebook-author` with `setup_xlsx`. Persist the rulebook; do not retain the setup workbook as a runtime dependency.
4. **Intake safety** on the User Story Excel: convert `.xlsx` → CSV under `artifacts/intake/.pipeline/`, then `python scripts/intake-safety-scan.py <csv>` — STOP on 2; redact/waive on 1.

## Runtime workflow

1. **Load MSD rulebook** — sheets, column roles, ID pattern, case model, enums. No other layout source. Never open `E2E test execution plan.xlsx`.
2. **user-story-excel-analyzer** — `python scripts/msd_test_case_xlsx.py extract-stories --in <user_story_excel> --out artifacts/intake/<date>-msd-source-stories.json`. Attaches nearest Feature / Area Path. Does not author cases.
3. **msd-test-case-extractor** — group stories (`grouping_key`); one Scenario per group; one positive case from happy-path AC; one exception/control case only when constraint/negative/boundary evidence exists. Steps from cited AC/need only. Write extraction notes.
4. **msd-test-case-xlsx-writer** — persist `artifacts/intake/<date>-msd-test-case-rows.json` (role keys), then `python scripts/msd_test_case_xlsx.py write --json <rows.json> --out artifacts/intake/<date>-msd-e2e-test-cases.xlsx`. Coverage and ISV sheets are derived by the writer.
5. **msd-test-case-compliance-validator** — `python scripts/validate-msd-test-case-xlsx.py`. Parent rejects FAIL.

## Output paths

| Artifact | Path |
|----------|------|
| Extraction notes | `artifacts/intake/<YYYY-MM-DD>-msd-test-case-extraction.md` |
| Source stories JSON | `artifacts/intake/<YYYY-MM-DD>-msd-source-stories.json` |
| Case rows JSON | `artifacts/intake/<YYYY-MM-DD>-msd-test-case-rows.json` |
| Working register CSV (internal) | `artifacts/intake/.pipeline/<YYYY-MM-DD>-msd-test-cases-working.csv` |
| Validation JSON | `artifacts/intake/<YYYY-MM-DD>-msd-test-case-validation.json` |
| Public Excel | `artifacts/intake/<YYYY-MM-DD>-msd-e2e-test-cases.xlsx` |

## Row rules (summary)

- **Grain:** one register row per step; case-level fields repeated and identical within a Test Case ID.
- **IDs:** `TC{scenario:02d}-{P|N}{seq:02d}` from the rulebook. Scenario ID is the grouping sequence, not copied from ADO.
- **Test Type / Priority / Status:** allowed values from the rulebook. Generation Status = `Not Run`. Actual Result, Defect ID, Comments empty.
- **Application / ISV:** Microsoft Dynamics (or integration) tokens **cited in the stories**. Composite separator from the rulebook. Do not copy bootstrap product names.
- **Steps:** imperative action + observable expected result; test data only when cited; owner from story role or named actor.

## Provenance

Each case in extraction notes: `behavior_id`, statement, `source_path` (user-story excel), `source_locator` (row / story ID), `confidence`.

Silent requirements → `ASSUMPTION-xxx` in notes; do not mark Done with pending blocking assumptions.

## Do not

- Read the bootstrap execution-plan workbook when the rulebook is present.
- Hand-author xlsx or add/remove columns.
- Invent process names, Dynamics modules, ISVs, SKUs, or failure paths.
- Emit `/expand-test-coverage` markdown catalogs or executable scripts from this skill.
