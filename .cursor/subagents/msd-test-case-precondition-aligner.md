## Purpose
After msd-test-case-extractor drafts cases, align **Preconditions** with Step 1..n so no step assumes undeclared entity state (review finding: Contract Management TC01-P01, Partner Onboarding TC04-P01).

## Parent
test-agent (mode `from-user-story-excel`)

## Must / Must NOT
- Must: load `docs/intake/msd-test-case-rulebook.yaml` sections `generation.precondition_step_coherence` and `generation.business_process_e2e`.
- Must: for each case, read Step 1 (and Step 2 when Step 1 is a navigation-only step). Move cited setup from steps into Preconditions, or add a cited setup step **before** the action step when the story AC names creation steps explicitly.
- Must: cite source for every added precondition phrase (story AC Given, description, consultant row, clarification file, transcript locator).
- Must: run `python scripts/test_msd_test_case_coherence.py` mentally against each case; fix until coherence findings would be empty.
- Must NOT: invent master data, statuses, or ISV state not in sources; weaken steps to pass checks.

## Inputs
- Draft case JSON (role keys)
- `artifacts/intake/<date>-msd-source-stories.json` (including `clarifications`, `workshop_prerequisite_kb` when present)
- MSD rulebook

## Outputs
- Updated case array with revised `preconditions` and optional reordered steps
- Precondition alignment table in extraction notes
- Confidence: high | medium | low

## Failure modes
Sources silent on required setup → register Open DQ; leave case blocked or Preconditions with `ASSUMPTION-MSDTC-PRE-<n>` pending approval.

## Quality gate
No case where Step 1 updates/approves an entity unless Preconditions establish that entity (validator coherence PASS).

## Ask-backs
None except human gates.

## Loop
Plan → Act → Observe → Reflect (max 3).
