# Audit — MSD test-case pipeline — business-process refinement

| Field | Value |
|-------|-------|
| **Date** | 2026-10-14 |
| **Trigger** | Stakeholder review of `artifacts/intake/2026-10-13-msd-e2e-test-cases.xlsx` |
| **Iteration** | 1 of 3 |

## What

Tuned `/generate-test-cases-from-user-stories` factory contracts for:

- Business-process E2E depth (min steps, AC decomposition, multi-positive paths when evidenced)
- Precondition ↔ Step 1 coherence (validator + aligner subagent)
- Supplemental inputs: consultant story Excel, post-workshop clarifications, workshop prerequisite KB, transcript reference (`enrich-msd-source-stories.py`)

## Why

Review cited high-level functional coverage, precondition/step mismatches (Contract Management TC01-P01, Partner Onboarding TC04-P01), and need to ingest later stakeholder clarifications and consultant user stories.

## How

| Layer | Change |
|-------|--------|
| Rulebook | `docs/intake/msd-test-case-rulebook.yaml` — `business_process_e2e`, `precondition_step_coherence`, `input.supplemental_sources`, `validation.precondition_coherence` |
| Scripts | `msd_test_case_coherence.py`, `enrich-msd-source-stories.py`, `validate-msd-test-case-xlsx.py` integration |
| Agents | `test-agent.md` — enrich + business-process author + precondition aligner |
| Subagents | `msd-test-case-business-process-author`, `msd-test-case-precondition-aligner`; updated extractor + compliance validator |
| Skill / command | `msd-test-cases-from-user-stories/SKILL.md`, `generate-test-cases-from-user-stories.md` |
| Config | `.cursor/config.yaml` `msd_test_case_pipeline` optional inputs |

## Validation

| Check | Result | Evidence |
|-------|--------|----------|
| `test_msd_test_case_coherence.py` | PASS | local run |
| `test_msd_test_case_xlsx_layout.py` | PASS | local run (after fixture row count fix) |
| Existing 2026-10-13 xlsx | Expected FAIL on regenerate | coherence gate will flag legacy precondition gaps until cases are re-authored |

## Open items

- **DQ-MSDTC-REVIEW-001:** Collect post-28/09 clarification notes and consultant story Excel paths; re-run user-story pipeline where clarifications change AC.
- **DQ-MSDTC-REVIEW-002:** Re-run `/generate-test-cases-from-user-stories` with supplements on latest User Story Excel.

## Next command

Re-run `/generate-test-cases-from-user-stories` with `user_story_excel` plus optional `consultant_story_excel` and `clarification_paths` after updated stories are available.
