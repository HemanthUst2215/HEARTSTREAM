# User Story Excel → MSD E2E test case extraction

> From `/generate-test-cases-from-user-stories`. Scan the User Story Excel before use (rule 31). Load `docs/intake/msd-test-case-rulebook.yaml` only — never the bootstrap execution-plan workbook.

## Metadata

| Field | Value |
|-------|-------|
| User Story Excel | `Finance User Stories- Workshop -WS-02.xlsx` |
| Working CSV (header projection) | `artifacts/intake/.pipeline/2026-10-13-finance-ws02-rulebook.csv` |
| MSD rulebook | `docs/intake/msd-test-case-rulebook.yaml` |
| Source story rulebook | `docs/intake/user-story-csv-rulebook.yaml` |
| Iteration | 1 |
| Date | 2026-10-13 |

## Source stories (from user-story-excel-analyzer)

| Locator | Work Item Type | Title | Feature / Area Path | AC bullets | Confidence |
|---------|----------------|-------|---------------------|------------|------------|
| 103808#row-4 | User Story | Manage accruals | PR-001 – Accrual & Deferral Management / Day 2\Finance\Record to Report\General Ledger | 6 | explicit |
| 103810#row-5 | User Story | Manage deferrals | PR-001 – Accrual & Deferral Management / Day 2\Finance\Record to Report\General Ledger | 5 | explicit |
| 103811#row-7 | User Story | Process allocations | PR-002 – Ledger Allocation / Day 2\Finance | 5 | explicit |
| 103819#row-10 | User Story | Define posting policies | PR-005 – Journal Automation / Day 2\Finance | 5 | explicit |
| 103820#row-11 | User Story | Configure and administer workflows | PR-005 – Journal Automation / Day 2\Finance | 5 | explicit |
| 103821#row-12 | User Story | Configure and run background jobs | PR-005 – Journal Automation / Day 2\Finance | 5 | explicit |
| 103822#row-14 | User Story | Analyze costs | PR-006 – Cost & Revenue Allocation / Day 2\Finance | 5 | explicit |
| 103823#row-15 | User Story | Monitor financial performance | PR-006 – Cost & Revenue Allocation / Day 2\Finance | 5 | explicit |
| 111626#row-17 | User Story | Import payroll journals from Deel | Payroll Integration-Deel-Finance / Day 2\Finance\Record to Report | 6 | explicit |
| 111627#row-18 | User Story | Map payroll to GL accounts and dimensions | Payroll Integration-Deel-Finance / Day 2\Finance\Record to Report | 5 | explicit |
| 111628#row-19 | User Story | Reconcile payroll clearing accounts | Payroll Integration-Deel-Finance / Day 2\Finance\Record to Report | 5 | explicit |

`extract-stories` on the raw Excel failed: headers are `Title 1` / `Title 2` / `Title 3` (plus `State`, `Assigned To`, `User Story Type`) and do not match `csv.column_order`. Working CSV projects Title = Title 3 else Title 2 else Title 1; other rulebook columns left empty when the source had no equivalent. No new domain columns were invented.

Grouping used nearest preceding Feature title (User Story IDs do not equal Feature IDs in this workbook). Business process names strip the `PR-NNN –` numbering prefix from the Feature title.

## Scenario groups

| Scenario ID | Business Process | Story locators | Positive Case | Exception Case | Notes |
|-------------|------------------|----------------|---------------|----------------|-------|
| 1 | Accrual & Deferral Management | 103808, 103810 | TC01-P01 | TC01-N01 | Exception from mandatory dimensions (AC3) and approval-before-post (AC5) |
| 2 | Ledger Allocation | 103811 | TC02-P01 | TC02-N01 | Exception from allocation journal approval workflow (AC3) |
| 3 | Journal Automation | 103819, 103820, 103821 | TC03-P01 | TC03-N01 | Exception from SoD, rejection, posting restrictions, invalid combinations, batch-schedule auth |
| 4 | Cost & Revenue Allocation | 103822, 103823 | TC04-P01 | TC04-N01 | Exception from role-based access (103823 AC3). Budget comparison only when Budgeting is in scope — not tested |
| 5 | Payroll Integration-Deel-Finance | 111626, 111627, 111628 | TC05-P01 | TC05-N01 | Exception from unmapped codes, idempotent import, reprocessable errors. Provider Deel vs Workday unconfirmed |

No unmatched_exception groups: every group had constraint, negative, or control evidence in AC.

## Provenance table

| behavior_id | statement | source_path | source_locator | confidence |
|-------------|-----------|-------------|----------------|------------|
| RB-MSDTC-001 | Workbook layout and case model from MSD rulebook | docs/intake/msd-test-case-rulebook.yaml | rulebook status Active | explicit |
| TC-01-P01 | Accrual schemes, provision/CONQ journals, prepaid release, TB reconcile | Finance User Stories- Workshop -WS-02.xlsx | 103808#row-4; 103810#row-5 | derived |
| TC-01-N01 | Mandatory dimensions and approval workflow block posting | Finance User Stories- Workshop -WS-02.xlsx | 103808 AC3, AC5 | derived |
| TC-02-P01 | Ledger allocation rules, batch close calendar, net-to-zero | Finance User Stories- Workshop -WS-02.xlsx | 103811#row-7 | derived |
| TC-02-N01 | Allocation journal not posted without approval | Finance User Stories- Workshop -WS-02.xlsx | 103811 AC3 | derived |
| TC-03-P01 | Journal names, approval workflow, batch/DMF schedule | Finance User Stories- Workshop -WS-02.xlsx | 103819–103821 | derived |
| TC-03-N01 | SoD, rejection, posting restrictions, invalid combinations | Finance User Stories- Workshop -WS-02.xlsx | 103819 AC2–4; 103820 AC2, AC4; 103821 AC3, AC5 | derived |
| TC-04-P01 | Dimensional cost analysis and management P&L after allocations | Finance User Stories- Workshop -WS-02.xlsx | 103822#row-14; 103823#row-15 | derived |
| TC-04-N01 | Role-based access on Financial reporting and Power BI | Finance User Stories- Workshop -WS-02.xlsx | 103823 AC3 | derived |
| TC-05-P01 | Deel payroll import, mapping, clearing reconciliation | Finance User Stories- Workshop -WS-02.xlsx | 111626–111628 | derived |
| TC-05-N01 | Unmapped codes stop import; duplicate pay run not posted | Finance User Stories- Workshop -WS-02.xlsx | 111626 AC3–4; 111627 AC4 | derived |
| ASSUMPTION-MSDTC-001 | Application token Dynamics 365 Finance when stories cite D365; Workshop description names Dynamics 365 Finance | Finance User Stories- Workshop -WS-02.xlsx | Workshop 68403 description | assumption |
| ASSUMPTION-MSDTC-002 | Default step owner Finance from Area Path `Day 2\Finance` when the story is not `As a <role>` and the step does not name another actor | source Area Path | all groups | assumption |

Application / ISV tokens used only when cited: Dynamics 365 Finance (D365 / Workshop), Power BI (103822, 103823), DMF (103821), Deel (111626 title/feature). Workday is not emitted as an ISV (unconfirmed provider).

## Unmatched / Open DQ

| ID | Group or story | Gap | Blocking | Owner |
|----|----------------|-----|----------|-------|
| DQ-MSDTC-001 | Source workbook | Headers do not match user-story CSV `column_order` (`Title 1/2/3`). Working CSV is a field projection only. | No | intake / BA |
| DQ-MSDTC-002 | All user stories | Descriptions are not `As a <role>, I need to <need>, so that <benefit>.` Default owner from Area Path / named AC actors (ASSUMPTION-MSDTC-002). | No | BA |
| DQ-MSDTC-003 | 111626 / Feature 93700 | Payroll provider Deel vs Workday per Annexure 176 is not confirmed. Feature Fit Gap = Gap; stories Fit Gap = TBD. Cases use Deel as cited in title/feature. | No | Finance / integrations |
| DQ-MSDTC-004 | 103823 AC2 | Actual vs budget comparison only when Budgeting feature is in scope. Not included as a required step. | No | Finance |

## Validation

- [x] `scripts/validate-msd-test-case-xlsx.py` PASS on output workbook (critical 0)
- [x] No bootstrap execution-plan content copied into cells
- [x] No pending Blocking assumptions (ASSUMPTION-MSDTC-001/002 are non-blocking)
