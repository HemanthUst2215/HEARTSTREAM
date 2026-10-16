# User Story Excel → MSD E2E test case extraction

> From `/generate-test-cases-from-user-stories`. Scan the User Story Excel before use (rule 31). Load `docs/intake/msd-test-case-rulebook.yaml` only — never the bootstrap execution-plan workbook.

## Metadata

| Field | Value |
|-------|-------|
| User Story Excel | `<path>` |
| MSD rulebook | `docs/intake/msd-test-case-rulebook.yaml` |
| Source story rulebook | `docs/intake/user-story-csv-rulebook.yaml` |
| Iteration | 1 |
| Date | `<YYYY-MM-DD>` |

## Source stories (from user-story-excel-analyzer)

| Locator | Work Item Type | Title | Feature / Area Path | AC bullets | Confidence |
|---------|----------------|-------|---------------------|------------|------------|
| | | | | | |

## Supplemental inputs

| Source type | Path | Used for (locators) | Post-workshop clarification? |
|-------------|------|---------------------|------------------------------|
| Primary User Story Excel | | | |
| Consultant story excel | | | |
| Clarification file(s) | | | |
| Workshop prerequisite KB | | | |
| Transcript | | | |

## E2E scenario plan (business-process author)

| Scenario ID | Business Process | Trigger | Handoffs (roles / systems) | Outcome | Positive case count | Consultant traceability |
|-------------|------------------|---------|----------------------------|---------|---------------------|-------------------------|
| 1 | | | | | | |

## Scenario groups

| Scenario ID | Business Process | Story locators | Positive Case | Exception Case | Notes |
|-------------|------------------|----------------|---------------|----------------|-------|
| 1 | | | | | |

## Precondition alignment

| Test Case ID | Step 1 summary | Gap (if any) | Fix applied | Source locator |
|--------------|----------------|--------------|-------------|----------------|
| | | | | |

## Provenance table

| behavior_id | statement | source_path | source_locator | confidence |
|-------------|-----------|-------------|----------------|------------|
| | | | | |

## Unmatched / Open DQ

| ID | Group or story | Gap | Blocking | Owner |
|----|----------------|-----|----------|-------|
| | | No exception evidence (case_model) | | |

## Validation

- [ ] `scripts/validate-msd-test-case-xlsx.py` PASS on output workbook
- [ ] No bootstrap execution-plan content copied into cells
- [ ] No pending Blocking assumptions
