# Audit: MSD365 Business Entity scope rulebook and catalog

## What

Bootstrapped **MSDynamics 365 Business Entity** allow-list from `Area Paths.xlsx` (sheet **Details** only; **Area Path** sheet ignored). Columns 2–4 → Domain, Application, Business Entity (column 1 ignored). Empty Column 4 preserved on 11 rows (ISV apps, Data Migration, E2E Business Model, Infrastructure).

## Why

Transcript user stories must stay within team-approved MSD365 module scope. No Dynamics 365 business entities outside the Excel-derived catalog may be authored.

## How

| Artifact | Path |
|----------|------|
| Rulebook | `docs/intake/msd365-business-entity-scope-rulebook.yaml` |
| Runtime catalog | `artifacts/intake/msd365-business-entity-catalog.json` (121 entries, 70 named business entities) |
| Human-readable extract | `artifacts/intake/.pipeline/msd365-business-entity-catalog.csv` |
| Build (bootstrap only) | `python scripts/build-msd365-business-entity-catalog.py` |
| Validate (transcript pipeline) | `python scripts/validate-user-story-business-entity-scope.py --json <user-story-rows.json>` |
| Regression | `python scripts/test_msd365_business_entity_scope.py` |

User Story rows JSON carries `msd365_domain`, `msd365_application`, `msd365_business_entity` (not ADO CSV columns). Wired into `.cursor/skills/user-story-from-transcript/SKILL.md`, `/generate-user-stories-from-transcript`, and `.cursor/config.yaml` → `msd365_business_entity_scope`.

## Validation

- `build-msd365-business-entity-catalog.py` exit 0; 121 entries match Excel Details row count.
- `test_msd365_business_entity_scope.py` — 6 tests OK.

## Open Items

- Existing `2026-10-13-user-story-rows.json` predates scope fields; re-run `/generate-user-stories-from-transcript` or backfill `msd365_*` on User Story rows before scope validator PASS.

## Next command

Re-run `/generate-user-stories-from-transcript` with scope metadata on each User Story, or `/generate-test-cases-from-user-stories` after stories are in scope.
