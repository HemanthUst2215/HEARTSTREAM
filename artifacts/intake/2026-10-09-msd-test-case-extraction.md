# User Story Excel → MSD E2E test case extraction

> From `/generate-test-cases-from-user-stories`. Scan the User Story Excel before use (rule 31). Load `docs/intake/msd-test-case-rulebook.yaml` only — never the bootstrap execution-plan workbook.

## Metadata

| Field | Value |
|-------|-------|
| User Story Excel | `artifacts/intake/2026-10-08-user-stories-from-transcript-v2.xlsx` |
| MSD rulebook | `docs/intake/msd-test-case-rulebook.yaml` |
| Source story rulebook | `docs/intake/user-story-csv-rulebook.yaml` |
| Iteration | 1 |
| Date | 2026-10-09 |

## Intake safety

| Path | Exit | Result |
|------|------|--------|
| `artifacts/intake/.pipeline/2026-10-09-msd-user-story-excel-scan.csv` | 0 | CLEAN |

Output-path gate: CLEAR.

## Source stories (from user-story-excel-analyzer)

29 User Story rows. Grouping uses `mapped_feature_id` (User Story `ID` = Feature row ID in the same workbook). Nearest-preceding Feature alone would have collapsed all stories onto `4. Install Base Management`.

## Scenario groups

| Scenario ID | Business Process | Story locators | Positive Case | Exception Case | Notes |
|-------------|------------------|----------------|---------------|----------------|-------|
| 1 | Contract Management | #row-47;row-48 | TC01-P01 | TC01-N01 | ASSUMPTION-MSDTC-001: no app named; used platform label Microsoft Dynamics |
| 2 | Channel Partner Strategy | #row-26 | TC02-P01 | TC02-N01 | DQ in AC: detailed CRM data points TBD |
| 3 | Partner Contracting & Commercial Setup | #row-45;row-46 | TC03-P01 | TC03-N01 | ASSUMPTION-MSDTC-001 on internal contract record app |
| 4 | Partner Onboarding & Enablement with Partner data synchronization | #row-21 | TC04-P01 | TC04-N01 | |
| 5 | Partner Data Available in CRM & synchronization with FnO | #row-22;row-23;row-24 | TC05-P01 | TC05-N01 | Feature title cites FnO; stories cite CRM legal entity |
| 6 | Partner Training & Enablement | #row-25 | TC06-P01 | TC06-N01 | |
| 7 | Partner Lead Generation & Performance | #row-27 | TC07-P01 | TC07-N01 | |
| 8 | Lead Registration & Qualification | #row-28;row-29 | TC08-P01 | TC08-N01 | Alternate path (partner-originated lead). DQ-001 volume not blocking |
| 9 | Opportunity Management | #row-30;row-31;row-32;row-33 | TC09-P01 | TC09-N01 | |
| 10 | Quotation & Pricing | #row-34;row-35;row-36;row-37 | TC10-P01 | TC10-N01 | DQ-007 shell-opportunity mechanics not invented |
| 11 | Order Capture / Management & Order processing by order sync between F&O and CRM | #row-38;row-39 | TC11-P01 | TC11-N01 | |
| 12 | Fulfillment & Shipment | #row-40;row-41 | TC12-P01 | TC12-N01 | ERP token cited as ERP/supply chain system |
| 13 | Service Contract Management | #row-43 | TC13-P01 | TC13-N01 | ASSUMPTION-MSDTC-001 |
| 14 | Install Base Management | #row-42;row-44 | TC14-P01 | TC14-N01 | DQ-003 trigger per product type not invented; owning CRM team DQ not invented |
| 15 | Escalation & Resolution | #row-49 | TC15-P01 | TC15-N01 | Detailed triage workflow deferred in story |

## Provenance table

| behavior_id | statement | source_path | source_locator | confidence |
|-------------|-----------|-------------|----------------|------------|
| TC-01-P01 | Contract duration and mid-term price update | artifacts/intake/2026-10-08-user-stories-from-transcript-v2.xlsx | #row-47;row-48 | derived |
| TC-04-P01 | Approved partner sync Zinfi → CRM | artifacts/intake/2026-10-08-user-stories-from-transcript-v2.xlsx | #row-21 | derived |
| TC-09-N01 | Block duplicate deal registration | artifacts/intake/2026-10-08-user-stories-from-transcript-v2.xlsx | #row-32 | derived |
| RB-MSDTC-001 | Workbook layout from MSD rulebook | docs/intake/msd-test-case-rulebook.yaml | rulebook | explicit |

## Unmatched / Open DQ

| ID | Group or story | Gap | Blocking | Owner |
|----|----------------|-----|----------|-------|
| ASSUMPTION-MSDTC-001 | Scenarios 1, 3, 13 | Stories do not name an application; Application / ISV set to rulebook platform label `Microsoft Dynamics` | No | domain |
| DQ (story AC) | Channel Partner Strategy | Detailed CRM account-planning data points TBD | No | domain |
| DQ-001 | Lead Registration | Partner-originated lead volume uncertain | No | domain |
| DQ-003 | Install Base | Exact create trigger per product type pending | No | domain |
| DQ-007 | Quotation | Shell-opportunity workflow mechanics pending | No | domain |
| unmatched_exception | (none) | Every group had constraint, negative, boundary, or alternate AC | | |

## Validation

- [x] `scripts/validate-msd-test-case-xlsx.py` PASS on output workbook
- [x] No bootstrap execution-plan content copied into cells
- [x] No pending Blocking assumptions (ASSUMPTION-MSDTC-001 is non-blocking)
