## Purpose
Turn grouped user stories (plus supplements) into **business-process-oriented** E2E scenarios: trigger → handoffs → outcome, with depth from workshop discussion — not single-function checks.

## Parent
test-agent (mode `from-user-story-excel`); runs **before** or **with** msd-test-case-extractor per skill ordering.

## Must / Must NOT
- Must: load MSD rulebook `generation.business_process_e2e` and `generation.case_model` (up to `max_cases` positive paths per group).
- Must: decompose acceptance criteria into multiple steps per `decompose_ac`; meet `min_steps_positive` for each positive case.
- Must: use supplemental `clarifications`, `workshop_prerequisite_kb`, and `transcript_path` when present in source-stories JSON — prefer clarified requirements over stale workshop-only text.
- Must: title cases as business outcomes (e.g. "Partner completes onboarding through CRM and PRM") not widget labels.
- Must: document in extraction notes when consultant-only stories were merged and which locators drove extra scenarios.
- Must NOT: invent ISVs, modules, or process names; copy bootstrap execution-plan content.

## Inputs
- Enriched `*-msd-source-stories.json`
- MSD rulebook

## Outputs
- Scenario plan per group (actors, systems, positive path count, exception evidence)
- Input to msd-test-case-extractor (or merged case draft)
- Confidence: high | medium | low

## Failure modes
Stories too thin for E2E → positive case with Open DQ `DQ-MSDTC-E2E-DEPTH`; do not pad with generic steps.

## Quality gate
Each positive case has ≥ `min_steps_positive` steps with at least two distinct Step Owner values when stories cite multiple roles.

## Ask-backs
Register Open DQ when clarification files contradict transcript stories — escalate `BLOCKED_CONFLICT`.

## Loop
Plan → Act → Observe → Reflect (max 3).
