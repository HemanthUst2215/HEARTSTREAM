# Transcript → user story extraction (GL workshop)

> From `/generate-user-stories-from-transcript`. Intake safety: **CLEAN** (exit 0) on source docx.

## Metadata

| Field | Value |
|-------|-------|
| Transcript | `D365 Finance - General Ledger UST Led Workshop-20260928_125637UTC-Meeting Recording-en-IN.docx` → `artifacts/intake/2026-10-12-transcript.txt` |
| Rulebook | `docs/intake/user-story-csv-rulebook.yaml` |
| Catalog | `artifacts/work-items/epic.json`, `artifacts/work-items/feature.json` (read before authoring; no new Epic/Feature rows) |
| Iteration | 1 |
| Date | 2026-10-12 |

## Cited facts (from transcript-analyzer)

| Locator | Fact | Confidence |
|---------|------|------------|
| Workshop open | F&O GL process modeling: COA/main accounts, dimensions (BU, profit center, cost center), fiscal calendar, currencies/revaluation, account structures; accrual/deferral and allocations deferred | explicit |
| COA | Single global chart shared across legal entities; Heartstream in-use accounts from extract vs full legacy catalog; entity-specific restrictions (KPNC, India GST) | explicit |
| Controls | Sub-ledger control accounts block manual GL; main account approval; suspend unused legacy accounts | explicit |
| Dimensions | Target ~4–5 active dimensions; account structures/advanced rules; SCM defaults for profit/cost center | explicit |
| Close | December fiscal year alignment (India transition); soft close; AR/AP module close before GL; period close workspace | explicit |
| Forex | Monthly shared rates; revaluation GL/AR/AP/bank | explicit |
| SoD / IC | Security roles for small team; intercompany voucher prefix | explicit |
| Localization | Customer invoice language per customer master | explicit |
| Follow-up | Accrual/deferral and ledger allocation session not completed | explicit |

## Candidate backlog

| # | Work Item Type | Title | Parent Feature (catalog note) | Notes |
|---|----------------|-------|------------------------------|-------|
| — | Workshop | 02. Finance - General Ledger UST Led Workshop | WS-02 scope in `work-items.json` (Workshop ID only) | Area Path: Day 2\Business E2E flow |
| 1–22 | User Story | See `2026-10-12-user-story-rows.json` | **No GL Features in `feature.json`** — alignment notes only; IDs applied in Phase 5 mapper | 22 implementable GL stories |
| 23–24 | Task | BU MRU / sample reports action items | — | Workshop actions |
| 25 | Issue | Accrual workshop incomplete | — | DQ-GL-005 |
| 26 | Risk | GL Features missing from ADO catalog | — | DQ-GL-CATALOG |

## Provenance table

| behavior_id | statement | source_path | source_locator | confidence |
|-------------|-----------|-------------|----------------|------------|
| GL-US-001 | Global shared COA across legal entities | `2026-10-12-transcript.txt` | COA / main account discussion | explicit |
| GL-US-002 | Entity-specific main account restrictions | `2026-10-12-transcript.txt` | KPNC / India tax accounts | explicit |
| GL-US-003 | Dimension and account structure enforcement | `2026-10-12-transcript.txt` | Financial dimensions segment | explicit |
| GL-US-004 | Period close and forex | `2026-10-12-transcript.txt` | Fiscal calendar / revaluation | explicit |

## Open DQ / assumptions

| ID | Question | Blocking | Owner |
|----|----------|----------|-------|
| DQ-GL-CATALOG | No GL/R2R Features in `feature.json`; mapper may match unrelated CRM Features or leave IDs blank | Mapping traceability | ADO / finance PO |
| DQ-GL-002 | Functional area: separate dimension vs cost-center-derived | Design | Finance |
| DQ-GL-003 | India GST account scope pending tax workshop | AC refinement | Tax workstream |
| DQ-GL-004 | Automated FX rate feed (Oanda) | Implementation | Treasury |
| DQ-GL-005 | Accrual/deferral and allocations deferred session | Story baseline | Workshop facilitators |
| DQ-GL-008 | SCM material → profit center mapping | Integration | SCM workstream |

## Validation

- [x] `scripts/validate-user-story-csv.py` PASS (27 rows)
- [x] Phase 5 `map-user-stories-to-work-items.py` run (see mapping log)
- [x] INVEST: `artifacts/intake/2026-10-12-invest-scorecard.csv` (separate from Excel)
