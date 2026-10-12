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
- `transcript-story-extractor` — transcript → story candidates
- `ado-user-story-csv-writer` — candidates → CSV
- `user-story-csv-compliance-validator` — `scripts/validate-user-story-csv.py`
- `invest-scorecard-evaluator` — Phase 4 INVEST scorecard (`artifacts/intake/<date>-invest-scorecard.csv`)
- `work-item-hierarchy-matcher` — parent **work-item-mapping-agent** (Phase 5); catalog Epic/Feature `ID` only

## User story evaluation (`/evaluate-user-stories`)

Parent: `user-story-evaluation-agent`. One metric owner each. Public HTML comes from `scripts/evaluate_user_stories.py render`.

- `story-matching-evaluator` — matches; Granularity
- `hallucination-detection-evaluator` — Hallucination Rate; valid-extra vs noise evidence
- `coverage-analysis-evaluator` — Recall, Precision, Manual-only, Generated-only
- `business-correctness-evaluator` — Title and Description Format Compliance, Role Specificity
- `acceptance-criteria-evaluator` — Acceptance Criteria Count, Quality, Negative and Boundary Coverage
- `epic-feature-mapping-evaluator` — Epic Agreement, Feature Agreement
- `kpi-aggregation-evaluator` — evaluation JSON; parent renders HTML

## MSD E2E from User Story Excel (`/generate-test-cases-from-user-stories`)

Parent: `test-agent` mode `from-user-story-excel`. Layout comes only from `docs/intake/msd-test-case-rulebook.yaml`.

- `msd-test-case-rulebook-author` — one-time rulebook from setup xlsx
- `user-story-excel-analyzer` — User Story Excel → source stories JSON
- `msd-test-case-extractor` — stories → case/step objects (rulebook case model)
- `msd-test-case-xlsx-writer` — `scripts/msd_test_case_xlsx.py write`
- `msd-test-case-compliance-validator` — `scripts/validate-msd-test-case-xlsx.py`

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
