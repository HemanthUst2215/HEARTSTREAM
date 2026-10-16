# Subagents

Flat catalog: one `*.md` per specialist (plus this README). Bounded tasks. Return subagent-io-template.md with confidence. Parent rejects below-gate output.

FE↔BE wiring is **not** a subagent and **not** a peer agent — it is a required check gate of `frontend-agent` inside `/implement-ui`.

## Work item CSV → JSON (`/process-work-items-csv`)

- `csv-intake-normalizer` — untrusted CSV scan + normalize
- `csv-schema-profiler` — column/profile manifest
- `work-item-enricher` — enrich rows for JSON export
- `json-output-validator` — schema check vs `work-items-output.schema.json`
- `work-item-reference-matcher` — link stories to work-items index

## Transcript → ADO CSV (`/generate-user-stories-from-transcript`)

- `user-story-csv-rulebook-author` — one-time rulebook from setup CSV
- `workshop-prerequisite-analyzer` — prerequisite docs → knowledge-base MD/JSON (scope authority)
- `transcript-analyzer` — cited transcript facts (uses prerequisite KB when provided)
- `mom-analyzer` — cited MoM facts, decisions, agenda topics (conflicts vs transcript listed, not resolved)
- `transcript-story-extractor` — transcript + MoM + prerequisite scope + MSD365 catalog → story candidates
- `ado-user-story-csv-writer` — candidates → CSV
- `workshop-scope-compliance-validator` — `validate-user-story-workshop-scope.py` + `validate-user-story-business-entity-scope.py`
- `user-story-csv-compliance-validator` — `scripts/validate-user-story-csv.py`
- `invest-scorecard-evaluator` — Phase 4 INVEST scorecard (`artifacts/intake/<date>-invest-scorecard.csv`)
- `work-item-hierarchy-matcher` — parent **work-item-mapping-agent** (Phase 5); catalog Epic/Feature `ID` only

## User story evaluation (`/evaluate-user-stories`)

Parent: `user-story-evaluation-agent`. One metric owner each. Public HTML comes from `scripts/evaluate_user_stories.py render`.

- `story-matching-evaluator` — matches; Granularity
- `hallucination-detection-evaluator` — Hallucination Rate (Generated) and Hallucination Rate (Manual); valid-extra vs noise evidence
- `coverage-analysis-evaluator` — Recall, Precision, Manual-only, Generated-only
- `business-correctness-evaluator` — Title and Description Format Compliance, Role Specificity
- `acceptance-criteria-evaluator` — Acceptance Criteria Count, Quality, Negative and Boundary Coverage
- `epic-feature-mapping-evaluator` — Epic Agreement, Feature Agreement
- `kpi-aggregation-evaluator` — evaluation JSON; parent renders HTML

## User story source traceability (`/generate-html-for-user-stories`)

Parent: `user-story-evaluation-agent` mode `source-traceability-html`. Two independent HTML reports via `scripts/generate_user_story_source_analysis.py render`. **No** manual-vs-AI matching.

- `source-knowledge-base-unifier` — transcript + MoM + pre-read + SOW → unified KB JSON
- `user-story-source-traceability-analyzer` — one CSV side vs unified KB → analysis JSON (run twice: manual, generated)

## MSD E2E from User Story Excel (`/generate-test-cases-from-user-stories`)

Parent: `test-agent` mode `from-user-story-excel`. Layout comes only from `docs/intake/msd-test-case-rulebook.yaml`.

- `msd-test-case-rulebook-author` — one-time rulebook from setup xlsx
- `user-story-excel-analyzer` — User Story Excel → source stories JSON
- `msd-test-case-business-process-author` — E2E scenario plan per group (trigger → handoffs → outcome)
- `msd-test-case-extractor` — stories → case/step objects (rulebook case model + E2E depth)
- `msd-test-case-precondition-aligner` — Preconditions vs Step 1 coherence
- `msd-test-case-xlsx-writer` — `scripts/msd_test_case_xlsx.py write`
- `msd-test-case-compliance-validator` — `scripts/validate-msd-test-case-xlsx.py` (+ `msd_test_case_coherence.py`)

## Expand / quality

- `test-intake-normalizer` — transcript intake-safety scan
- `test-case-generator` — matched Features → rulebook test-case CSV (`test-agent` mode `from-transcript`)

UAT catalog authoring is **not** on the default expand path.

## Run-tests

- `spring-test-generator`, `playwright-codegen` — scripts after package Approved
- `api-test-runner`, `ui-test-runner`, `coverage-analyzer`
- `e2e-defect-analyzer` (single pass), `playwright-self-healer` (OODA inner loop; suggestions only)

## Run-eval

- `eval-agent` (`/run-eval`; inner `/close-eval-gaps`)
