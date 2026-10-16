# Transcript → user story extraction

> From `/generate-user-stories-from-transcript`. Untrusted intake — scan before use (rule 31).

## Metadata

| Field | Value |
|-------|-------|
| Transcript | `<path>` |
| MoM | `<mom_path>` |
| Prerequisite KB | `artifacts/intake/<date>-workshop-prerequisite-knowledge-base.json` |
| Rulebook | `docs/intake/user-story-csv-rulebook.yaml` |
| Prerequisite rulebook | `docs/intake/workshop-prerequisite-scope-rulebook.yaml` |
| MSD365 catalog | `docs/intake/msd365-business-entity-catalog.json` |
| Iteration | 1 |
| Date | `<YYYY-MM-DD>` |

## Cited facts (from transcript-analyzer)

| Locator | Fact | Confidence |
|---------|------|------------|
| | | explicit / derived / assumption |

## Cited facts (from mom-analyzer)

| MoM locator | Fact | Confidence |
|-------------|------|------------|
| | | explicit / derived / assumption |

## MoM ↔ transcript conflicts

| Transcript locator | MoM locator | Topic | Notes |
|--------------------|-------------|-------|-------|
| | | | Open DQ — not resolved |

## Candidate backlog

| # | Work Item Type | Title | Description (summary) | AC bullets | Prerequisite refs | Transcript locator | MoM locator | MSD365 domain / app / entity | Parent Feature/Epic | Area Path | Notes |
|---|----------------|-------|----------------------|------------|-------------------|--------------------|-------------|------------------------------|---------------------|-----------|-------|
| 1 | User Story | | | | OBJ-001 | | | CRM / Sales / Lead to Opportunity | | | |

## Traceability

| Story title | prerequisite_refs | transcript_locator | mom_locator | msd365_domain | msd365_application | msd365_business_entity |
|-------------|-------------------|--------------------|-------------|---------------|--------------------|------------------------|
| | | | | | | |

## Out of scope / excluded

### Prerequisite misalignment

| Transcript locator | Topic | Reason |
|--------------------|-------|--------|
| | | Not in prerequisite in_scope objectives/modules |

### MSD365 entity / catalog

| Transcript locator | Topic | Reason |
|--------------------|-------|--------|
| | | No catalog.entries match |

## Provenance table

| behavior_id | statement | source_path | source_locator | confidence |
|-------------|-----------|-------------|----------------|------------|
| | | | | |

## Open DQ / assumptions

| ID | Question | Blocking | Owner |
|----|----------|----------|-------|
| ASSUMPTION-001 | | | |

## Validation

- [ ] `scripts/validate-user-story-csv.py` PASS on output CSV
- [ ] No pending Blocking assumptions
