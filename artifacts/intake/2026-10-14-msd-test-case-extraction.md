# User Story Excel → MSD E2E test case extraction

> Finance WS-02 · Iteration 1 · 2026-10-14 · Pipeline: business-process E2E + precondition coherence

## Metadata

| Field | Value |
|-------|-------|
| User Story Excel | `Finance User Stories- Workshop -WS-02.xlsx` |
| MSD rulebook | `docs/intake/msd-test-case-rulebook.yaml` |
| Source story rulebook | `docs/intake/user-story-csv-rulebook.yaml` |
| Stories extracted | 11 stories, 5 scenario groups |
| Intake safety | CLEAN (`2026-10-14-finance-ws02-intake.csv`) |

## Supplemental inputs

| Source type | Path | Used for | Post-workshop clarification? |
|-------------|------|----------|----------------------------|
| Primary User Story Excel | Finance User Stories- Workshop -WS-02.xlsx | All cases | No |
| Consultant story excel | — | — | — |
| Clarification file(s) | — | — | — |

## E2E scenario plan (business-process author)

| Scenario ID | Business Process | Trigger | Handoffs | Outcome | Positive cases | Notes |
|-------------|------------------|---------|----------|---------|----------------|-------|
| 1 | Accrual & Deferral Management | Vendor invoice / prepaid setup | Finance → approval → GL close | TB reconciliation | 1 (P01) | Accruals + deferrals in one close cycle |
| 2 | Ledger Allocation | Month-end allocation run | Finance → approval → reporting | Net-zero allocations in PR-006 | 1 | |
| 3 | Journal Automation | Manual journal + batch close | Submitter → approver → batch admin | SOX-aligned posting | 1 | |
| 4 | Cost & Revenue Allocation | Period close refresh | Finance → Power BI consumers | P&L + TB reconcile | 1 | |
| 5 | Payroll Integration-Deel-Finance | Approved Deel pay run | Deel → D365 GL → bank recon | Clearing reconciled | 1 | DQ: Deel vs Workday provider |

## Scenario groups

| Scenario ID | Business Process | Story IDs | Positive | Exception | Notes |
|-------------|------------------|-----------|----------|-----------|-------|
| 1 | Accrual & Deferral Management | 103808, 103810 | TC01-P01 | TC01-N01 | |
| 2 | Ledger Allocation | 103811 | TC02-P01 | TC02-N01 | |
| 3 | Journal Automation | 103819–103821 | TC03-P01 | TC03-N01 | |
| 4 | Cost & Revenue Allocation | 103822, 103823 | TC04-P01 | TC04-N01 | |
| 5 | Payroll Integration-Deel-Finance | 111626–111628 | TC05-P01 | TC05-N01 | Open DQ provider |

## Precondition alignment

| Test Case ID | Step 1 focus | Alignment |
|--------------|--------------|-----------|
| TC01-P01 | Configure schemes (setup) | Preconditions cite COA, journal names, prepaid accounts before operational steps |
| TC02-N01 | Generate allocation journal | Preconditions: journal generated + approval required |
| TC05-P01 | Mapping table | Preconditions: mapping maintained; Deel pay run available |

## Provenance table

| behavior_id | statement | source_path | source_locator | confidence |
|-------------|-----------|-------------|----------------|------------|
| TC-01-P01 | Accrual/deferral E2E through month-end | Finance User Stories- Workshop -WS-02.xlsx | 103808, 103810 | derived |
| TC-05-P01 | Deel payroll import and clearing | Finance User Stories- Workshop -WS-02.xlsx | 111626–111628 | derived |

## Unmatched / Open DQ

| ID | Gap | Blocking | Owner |
|----|-----|----------|-------|
| DQ-MSDTC-WS02-001 | Payroll provider Deel vs Workday (story 111626 AC6) | No | Finance / Integration |
| DQ-MSDTC-WS02-002 | Post-workshop clarification files not supplied for enrich | No | Operator |

## Validation

- [x] `scripts/validate-msd-test-case-xlsx.py` PASS (post-write)
- [x] Precondition coherence (`msd_test_case_coherence.py`)
- [x] No bootstrap execution-plan content in cells
