# Templates

Contracts for the public commands. Use these files — do not invent a parallel doc shape.

## By command

| Template | Used by |
|----------|---------|
| `user-story-csv-rulebook-template.yaml` | `/generate-user-stories-from-transcript` one-time rulebook bootstrap |
| `transcript-story-extraction-template.md` | `/generate-user-stories-from-transcript` |
| `ado-user-story-rows-json-template.md` | row JSON before `ado_user_story_csv.py write` |
| `msd-test-case-rulebook-template.yaml` | `/generate-test-cases-from-user-stories` one-time MSD rulebook bootstrap |
| `msd-test-case-extraction-template.md` | `/generate-test-cases-from-user-stories` extraction notes |
| `msd-test-case-rows-json-template.md` | case JSON before `msd_test_case_xlsx.py write` |
| `gherkin-story-template.md` | `gherkin-acceptance-criteria-writer` |
| `work-items-output.schema.json` | `/process-work-items-csv` |
| `work-items-summary-template.md` | `/process-work-items-csv` enricher |
| `test-cases-template.md` | legacy case-body shape; `/expand-test-coverage` output is the rulebook CSV |
| `test-matrix-template.md` | `/expand-test-coverage` |
| `test-cases-br-coverage-template.md` | br-coverage-validator |
| `test-package-review-template.md` | expand Phase 2b human gate |
| `br-tc-taxonomy.md` / `generic-step-denylist.md` | expand companion quality |
| `test-case-quality-metrics-template.md` | step-quality validator |
| `intake-manifest.schema.md` | test-intake-normalizer |
| `bdd-test-case-template.md` | expand when Gherkin expansion is in scope |
| `plan-act-validate-refine-loop.md` | expand execution loop |
| `plan-as-input-protocol.md` | orchestrator when a governed plan or story artifact is supplied |
| `ooda-self-heal-loop.md` | quality-agent (self-heal inner loop only) |
| `subagent-io-template.md` | subagent return contract |
| `audit-trail-template.md` | every public command |
| `user-story-evaluation-metrics.yaml` | `/evaluate-user-stories` metric contract |
| `user-story-evaluation-report-template.md` | `/evaluate-user-stories` evaluation JSON shape |
