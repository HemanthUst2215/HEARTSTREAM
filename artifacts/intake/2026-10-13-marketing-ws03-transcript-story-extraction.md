# Transcript → user story extraction (Marketing WS-03)

| Field | Value |
|-------|-------|
| Transcript | `artifacts/intake/2026-10-13-marketing-ws03-transcript.txt` |
| Prerequisite KB | `artifacts/intake/2026-10-13-marketing-ws03-workshop-prerequisite-knowledge-base.json` |
| Iteration | 1 |
| Date | 2026-10-13 |

## Session notes

- Workshop title referenced **Lead to Opportunity**; facilitators clarified **Customer Insights = marketing** (transcript 5:18–9:05). Lead-management attendees were released; session focused on **external analytics ingestion & unification** (agenda WS-CE-01) with segmentation and profile demos.
- Heavy discussion: vertical market segmentation (hospital, EMS, education, dentist), distributor multi-vertical behavior, ship-to vs sold-to, late tracings, global product marketing visibility, consumable purchase analytics.

## Traceability (summary)

| Story (Title 3) | prerequisite_refs | transcript_locator | MSD365 triple |
|-----------------|-------------------|--------------------|---------------|
| Connect CRM account and contact master data to Customer Insights | OBJ-001, MOD-001 | 39:05–45:28 | CRM / Customer Insights / Lead to Opportunity |
| Ingest sales order and engagement data for unified profiles | OBJ-001, MOD-001 | 39:05–45:28 | CRM / Customer Insights / Lead to Opportunity |
| Define match rules for unified customer profiles | OBJ-001, MOD-002 | 39:05–57:55 | CRM / Customer Insights / Lead to Opportunity |
| Create dynamic segments by vertical end-market | MOD-001, OBJ-006 | 32:53–37:15 | CRM / Customer Insights / Lead to Opportunity |
| Identify distributors serving multiple vertical markets | MOD-001 | 50:33 | CRM / Customer Insights / Lead to Opportunity |
| Use ship-to attributes in Customer Insights segment rules | MOD-001, OBJ-001 | 48:02–48:07 | CRM / Customer Insights / Lead to Opportunity |
| Capture end-market segment at e-commerce order entry | MOD-001, OBJ-006 | 45:28–46:53 | CRM / Customer Insights / Lead to Opportunity |
| Provide account-level marketing profiles with contact drill-down | MOD-002, OBJ-002 | 58:17–59:55 | CRM / Customer Insights / Lead to Opportunity |
| Enable worldwide marketing analytics visibility for product marketing | OBJ-002, MOD-002 | 1:04:55–1:05:40 | CRM / Customer Insights / Lead to Opportunity |
| Update install base segment after partner tracing import | MOD-001, OBJ-001 | 37:15–38:39 | CRM / Customer Insights / Lead to Opportunity |
| Detect vertical sales trends for targeted campaigns | OBJ-006, OBJ-004 | 1:22:55–1:23:49 | CRM / Customer Insights / Lead to Opportunity |
| Ingest distributor sold-to location from partner channel into CI | OBJ-001, MOD-001 | 1:26:25–1:27:09 | CRM / Customer Insights / Lead to Opportunity |
| Analyze account consumable purchase patterns for marketing outreach | OBJ-002, MOD-002 | 1:31:52–1:33:26 | CRM / Customer Insights / Lead to Opportunity |

## Out of scope / excluded (prerequisite)

| Transcript locator | Topic | Reason |
|--------------------|-------|--------|
| 10:17–10:23 | Lead assignment through opportunity closure | OOS-001 — sales lead process not in scope for this marketing session |

## Out of scope / excluded (MSD365 entity)

None — all stories map to `CRM / Customer Insights / Lead to Opportunity`.

## Validation

- [x] `validate-user-story-workshop-scope.py` PASS
- [x] `validate-user-story-business-entity-scope.py` PASS
- [x] `validate-user-story-csv.py` PASS
- [x] Work-item mapping: 13/13 matched (`2026-10-13-marketing-ws03-work-item-mapping-log.json`)
