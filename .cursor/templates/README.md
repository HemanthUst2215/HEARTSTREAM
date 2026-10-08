# Templates

Contracts, BRD, stories, plans, audit, evals, quality, ops, issue logs. **Always use these templates** — do not create ad-hoc doc structures.

See **[template-hardening-standard.md](template-hardening-standard.md)** for required elements (metadata, tables, provenance, output paths).

## Quality bar

| Tier | Example | Line count guide |
|------|---------|------------------|
| Hardened operational | `issue-log-template.md`, `audit-trail-template.md` | 40+ lines with tables |
| Hardened KPI / command | `kpi-evidence-matrix-template.md`, `command-contract-template.md` | 40+ lines |
| **Forbidden** | Single-line placeholders ("Paths, methods, envelope") | — |

## Twin sync

After editing `.cursor/templates/`, mirror to `.claude/templates/` and `.github/templates/` (byte-identical).

## Common templates by command

| Template | Used by |
|----------|---------|
| `issue-log-template.md` | `/fix-issue` → `artifacts/issues/<date>-<slug>.md` |
| `audit-trail-template.md` | Every public command |
| `brd-template.md` | `/generate-brd` |
| `test-cases-template.md` | implement-*, expand-test-coverage, fix-issue |
| `test-package-review-template.md` | expand-test-coverage Phase 2b human gate |
| `br-tc-taxonomy.md` / `generic-step-denylist.md` | expand-test-coverage companion quality |
| `test-cases-br-coverage-template.md` | br-coverage-validator (PASS before `/run-tests`) |
| `playwright-spec-template.md` / `page-object-template.md` | `/run-tests` playwright-codegen |
| `defect-analysis-template.md` / `self-heal-suggestion-template.md` | `/run-tests` after execution |
| `ooda-self-heal-loop.md` | `playwright-self-healer` only (Phase 5 inner loop; not factory-wide) |
| `api-contract-template.md` | `/implement-api`, api-agent |
| `tech-spec-template.md` | plan / documentation-agent (not a public story command) |
| `user-story-csv-rulebook-template.yaml` | one-time rulebook bootstrap |
| `transcript-story-extraction-template.md` | `/generate-user-stories-from-transcript` |
| `ado-user-story-rows-json-template.md` | row JSON before `ado_user_story_csv.py write` |
| `kpi-*-template.md` | `/validate-kpi-metrics` → `docs/quality/kpi-validations/` |
| `pr-template.md` | `/pr-assist` |
| `code-generation-dos-donts.md` | All implement commands |
