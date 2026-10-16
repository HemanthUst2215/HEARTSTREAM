# Transcript → user story extraction

## Metadata

| Field | Value |
|-------|-------|
| Transcript | `01. Sales - CE Record to Report UST Led Workshop-20260928-en-US.docx` |
| Text extract | `artifacts/intake/2026-10-13-transcript.txt` |
| Rulebook | `docs/intake/user-story-csv-rulebook.yaml` (`ado-user-story-xlsx-v2`) |
| Iteration | 1 |
| Date | 2026-10-13 |

## Cited facts (from transcript-analyzer)

| Locator | Fact | Confidence |
|---------|------|------------|
| transcript §partner/ZINFI | Partner onboarding in ZINFI must complete (diligence, contract, training) before CE sync | explicit |
| transcript §deal registration | Deal registrations are distinct from standard opportunities; channel conflict checks apply | explicit |
| transcript §quoting | Reseller contract price groups apply; discount tiers route to PAM / finance approval | explicit |
| transcript §fulfillment | ERP fulfillment status syncs to CRM and partner portal (ZINFI) | explicit |
| transcript §install base | Serialized install base location changes require controlled, auditable updates | explicit |
| transcript §parking lot | Partner master edit ownership in CE after sync remains unresolved | explicit |

## Candidate backlog

| # | Work Item Type | Title (Title 1 / 3) | Description (summary) | AC bullets | Parent Feature/Epic (catalog intent) | Area Path | Notes |
|---|----------------|---------------------|----------------------|------------|--------------------------------------|-----------|-------|
| 1 | Workshop | Title 1: Sales CE R2R workshop | Session scope: CE record-to-report, ZINFI, quoting, fulfillment | — | — | Day 2\CRM | State In Review |
| 2–19 | User Story | Title 3: partner sync, deal reg, quoting, fulfillment, install base, etc. | As-a / I-need / so-that per row JSON | `- ` bullets | B2B reseller / CRM Features in `feature.json` | optional | 18 stories |
| 20–21 | Issue | Title 3: parking-lot items | Risk / Impact / Mitigation in Description | empty | — | Day 2\CRM | |

Full row bodies: `artifacts/intake/2026-10-13-user-story-rows.json`.

## Provenance table

| behavior_id | statement | source_path | source_locator | confidence |
|-------------|-----------|-------------|----------------|------------|
| US-CE-001 | Workshop container for Sales CE R2R session | `artifacts/intake/2026-10-13-transcript.txt` | opening / workshop title | explicit |
| US-CE-002 | Partner sync only after ZINFI onboarding complete | same | ZINFI / onboarding discussion | explicit |
| US-CE-003 | Deal registration vs opportunity | same | deal registration segment | explicit |
| US-CE-ISSUE-001 | Partner master edit ownership unresolved | same | parking lot | explicit |

## Open DQ / assumptions

| ID | Question | Blocking | Owner |
|----|----------|----------|-------|
| DQ-CE-WS-001 | Workshop row has no catalog Workshop ID (mapper score below threshold) | No | intake |
| DQ-INVEST-001 | 17/18 User Stories INVEST Needs Refinement (Testable dimension) | No | BA / domain |

## Validation

- [x] `scripts/validate-user-story-csv.py` PASS on `artifacts/intake/.pipeline/2026-10-13-user-stories-working.csv` (21 rows)
- [x] No blocking assumptions for Done
