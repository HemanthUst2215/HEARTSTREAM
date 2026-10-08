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

## Expand / quality

- `test-intake-normalizer` — untrusted intake scan + manifest
- `automation-companion-author` — case bodies (`docs/test-cases.md`); not scripts
- `tc-traceability-mapper` — `docs/test-matrix.md`
- `tc-completeness-validator`, `tc-step-quality-validator` — companion quality
- `br-coverage-validator` — only writer of `docs/test-cases-br-coverage.md`

UAT catalog authoring is **not** on the default expand path.

## Run-tests

- `spring-test-generator`, `playwright-codegen` — scripts after package Approved
- `api-test-runner`, `ui-test-runner`, `coverage-analyzer`
- `e2e-defect-analyzer` (single pass), `playwright-self-healer` (OODA inner loop; suggestions only)

## Run-eval

- `eval-agent` (`/run-eval`; inner `/close-eval-gaps`)
