# Agent Audit — factory setup — MSD test-case rulebook bootstrap

> Aligns with `docs/harness/progress.md`. No secrets, credentials, or PHI/PII.

| Field | Value |
|-------|-------|
| **Date** | 2026-10-09 |
| **Command / Agent** | test-agent (mode `rulebook-bootstrap`) — framework authoring, not a generation run |
| **Iteration** | 1 of 3 |
| **Validation** | Layout regression PASS (`scripts/test_msd_test_case_xlsx_layout.py`); no test cases generated |

## What
- Authored `docs/intake/msd-test-case-rulebook.yaml` from **layout/rules/patterns only** in `E2E test execution plan.xlsx` (one-time bootstrap).
- Added `/generate-test-cases-from-user-stories` plus test-agent mode `from-user-story-excel`, five subagents, skill, templates, and config-driven writer/validator scripts.
- Did **not** generate MSD test cases from any User Story Excel.

## Why
Operator requested a Test Case Generation Rulebook and framework parallel to user-story generation, using the E2E execution-plan workbook only to derive structure. Explicit instruction: do not create test cases yet.

## How
- Rules: 00, 01, 07, 09, 10, 22, 31
- Templates: `msd-test-case-rulebook-template.yaml`, `msd-test-case-rows-json-template.md`, `msd-test-case-extraction-template.md`
- Skill: `.cursor/skills/msd-test-cases-from-user-stories/SKILL.md`
- Scripts: `msd_test_case_xlsx_layout.py`, `msd_test_case_xlsx.py`, `validate-msd-test-case-xlsx.py`, `test_msd_test_case_xlsx_layout.py` (synthetic fixtures only)

## Validation
| Check | Result | Evidence |
|-------|--------|----------|
| Inputs complete | PASS | Bootstrap xlsx used once for structure |
| DoD checklist | PASS (framework) | Rulebook Active; command/agents/scripts present |
| Tests / evals | PASS | `python scripts/test_msd_test_case_xlsx_layout.py` all five tests PASS |
| Scope allowlist | PASS | test-agent write includes `docs/intake/msd-test-case-rulebook.yaml` and `artifacts/intake/**` |
| No generation run | PASS | Public MSD xlsx not written from user stories |

## Behavior provenance
| behavior_id | statement | source | confidence |
|-------------|-----------|--------|------------|
| RB-MSDTC-001 | Three-sheet workbook: coverage index, step-level register, hidden ISV lookup; one row per step; 1 positive + 1 evidenced exception per group | `E2E test execution plan.xlsx` sheets/headers/Design Basis (layout only) | explicit |

## Open items
- Runtime generation waits for `/generate-test-cases-from-user-stories` with a User Story Excel. Do not treat this audit as a completed generation command.

## Next command
`/generate-test-cases-from-user-stories` with `user_story_excel` pointing at `artifacts/intake/<date>-user-stories-from-transcript.xlsx` (when the operator is ready to generate cases).

**Output path:** `artifacts/audit/2026-10-09-msd-test-case-rulebook-bootstrap.md`
