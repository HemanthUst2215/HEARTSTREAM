# Lineage keep/drop ledger

Sources: `costco_cursor_project_setup` ≈ `costco_nsi_ai_phase1` (Enterprise), `costco-opticals`, `nsi-wh72`.

Disposition: **K** keep in core (generalized), **G** pattern kept / product names dropped, **D** drop. Historical **P** (pack overlay) is retired — those rows are now **K** or **D**.

## Enterprise / NSI phase1 `.cursor/`

| Source area | Disposition | Master location |
|-------------|-------------|-----------------|
| agents/* (32 specialists) | K | `.cursor/agents/` rewritten to contracts |
| agents/figma/* | G | frontend-agent mode `design-system` + figma subagents |
| agents/quality/kpi-validation-agent | G | quality-agent mode `kpi` (no extra peer) |
| agents/planning/governed-story-planner | K | core |
| commands/generate-user-story | K | core |
| commands/generate-database-scripts, generate-api-contract, generate-backend, generate-frontend, generate-ui, wire-fe-be-api-sequence, generate-tests, generate-junit-api-tests | G | internals of `/implement-api` and `/implement-ui` — **not** public commands |
| commands/figma-to-nextjs | K | core `/figma-to-nextjs` |
| commands/validate-kpi-metrics | K | core `/validate-kpi-metrics` (promoted from pack 2026-08-17) |
| commands/phase-implementation, phase-business-analysis, phase-ux-data-alignment, phase-forward-engineering, phase-quality-release, phase-team-lead-pack | D | Duplicate the locked spine / intake commands; removed from core |
| commands/phase-reverse-engineering | D | pack deleted; not a core command |
| commands/plan-governed-stories | K | rewritten to implement-* rows |
| commands/write-bdd-tests, generate-documentation, sdlc-* | D | stale names |
| subagents/engineering/spring-* | K | core (flat `.cursor/subagents/spring-*.md`) |
| subagents/figma/* | K | `.cursor/subagents/` figma specialists (frontend-agent mode `design-system`) |
| subagents/quality/kpi-* | K | core (quality-agent mode kpi) |
| subagents/data/* | K | core data-agent + `.cursor/skills/migration/` |
| rules 00–11, 13, 15, 17–23, 27–28 (renumbered uniquely) | K | `.cursor/rules/` |
| rules 21-figma, 21-kpi (collided) | K | 25 figma, 26 kpi (core) |
| templates (contracts, stories, plans, API/UI) | K | `.cursor/templates/` |
| templates/kpi-* | K | `.cursor/templates/` |
| skills (planning, api, infra, ops, figma, kpi, migration, validation-chain) | K | native SKILL.md in `.cursor/skills/` |
| hooks + artifact-policy | K | rebuilt; `failClosed: true` on commit verify |
| java_master_templates, java_test_templates | K | generalized paths (`/api/v1/...`, Table* helpers) |
| portable/validate-kpi-metrics-kit | D | installer overlay not used; KPI is core |
| .github/agents (docker, gcp-workflow, perf) | D | Copilot docker/perf agents not in this factory |
| GitHub Copilot SDLC twin | K | `.github/agents/*.agent.md` + `.github/prompts/` + `COPILOT-FLOW.md` (same 19 primaries; not the docker pack) |
| flask_asset_generator | D | sidecar |
| tools/kpi-validation/*.py heuristics | D | not a gate |
| documented but missing check-artifacts / githooks / figma validate.py | K | rebuilt in master |

## Opticals `.cursor/`

| Source area | Disposition | Master location |
|-------------|-------------|-----------------|
| orchestrator-agent, harness, audits, PAVR | K | core |
| MENU-AGENT-CONTRACT | G | `parallel-agent-file-ownership.md` |
| ui-corrections-locked.md | K | `docs/harness/ui-corrections-locked.md` |
| /apply-requirements | K | core |
| deep-code-review-agent | G | merged into code-review-agent (read-only five-pass) |
| whiteboard-to-enterprise-mega-flow | K | core skill |
| reverse-engineering-agent, context-wiki | G | reverse-engineering-agent in core; no `/phase-reverse-engineering`; context-wiki dropped |
| orxe-dossier-restorer, dspf-field-mapper | D | IBM i / DSPF overlay deleted |
| hipaa-compliance-agent, hipaa-pii-scanner, 15-hipaa | D | HIPAA overlay deleted |
| optical-br-no-skip, IPDS, ATI names, deliver-ati, plan-ati | D/G | ATI planner generalized as `/plan-bounded-context` (planner-agent mode) |
| knowledge-graph MCP | D | sidecar |
| 23-kpi-anti-regression | K | rule 24 in core |
| decision.md filename | G | standardized to `decisions.md` |

## nsi-wh72 `.cursor/` + `evals/`

| Source area | Disposition | Master location |
|-------------|-------------|-----------------|
| /generate-brd + requirements-agent + intake subagents | K | core |
| /plan-sprint, /implement-*, /deliver-sprint, /expand-test-coverage, /review-changes, /application-summary, /close-eval-gaps | K | core spine |
| eval-agent + eval-suite skill + fix-queue | K | core; paths under `evals/product/` |
| evals/wave-1 L1/L4/LX SPECs | G | templates only, no WH72 cases |
| Scan-to-Destroy eval cases, config module names | D | product-specific |
| mockup-to-component | K | core |
| validation-chain-generator | K | `.cursor/subagents/validation-chain-generator.md` (does not replace test-agent) |
| skills/jacoco, playwright, application-summary-pdf | K | generalized |
| empty docs/stories, subagents/reverse placeholders | G | keep those agent types in master (from other sources) |
| java_master leftover sales-audit | D | stale |
| config.yaml without evals: | G | master `config.yaml.example` includes `evals:` |

## Packs in this library

**None.** Former overlays promoted or dropped 2026-08-17: figma-design-system, data-migration, validation-chain, bounded-context → core. kpi-validation → core earlier. reverse-engineering, as400-legacy, phi-hipaa, handoffs-ops, github-copilot-agents → deleted.

## Rule number map (master)

00 governance, 01 context, 02 security, 03 Spring, 04 Next, 05 API, 06 infra, 07 testing, 08 docs, 09 orchestration, 10 audit, 11 intake gates, 12 unused (former reverse pack), 13 INVEST, 14 data migration, 15 release, 16 SRE, 17 test logs, 18 compliance, 19 change mgmt, 20 DR, 21 API validation, 22 provenance, 23 test generation, 24 KPI anti-regression, 25 Figma MUI, 26 KPI catalog, 27 Python, 28 tech spec, 29 unused (former PHI pack), 30 production fix.

## Catalog after 2026-08-17 shrink (19 primaries)

User-locked: shrink specialists into modes/gates; do **not** merge SoD (backend≠frontend, quality≠test, review remains read-only, BRD≠stories). Commands stay. Hand-edited after reading every absorbed contract — no Python emitter.

| Absorbed | Surviving | Form |
|----------|-----------|------|
| fe-be-api-sequence-wiring-agent | frontend-agent | `/implement-ui` wiring **gate** |
| api-contract-agent | api-agent | gate 2 (sync/verify) |
| python-developer-agent | backend-agent | mode python |
| github-workflow-agent | infra-agent | mode workflow |
| database-script-generation-agent + data-migration-agent | data-agent | modes ddl / cutover |
| scaffold-agent + incremental-change-agent + code-cleanup-agent | change-agent | modes scaffold / cited / cleanup |
| bdd-test-case-writer-agent + api-endpoint-validation-agent + test-results-logger-agent | test-agent | modes generate / live / log |
| tech-spec-writer-agent | documentation-agent | mode tech-spec |
| performance-agent | sre-agent | mode perf; public `/performance-test` |
| release-manager-agent + release-train-agent | release-agent | modes readiness / canary |
| daily-handoff-agent + sprint-handoff-agent | handoff-agent | modes daily / sprint |
| governed-story-planner-agent + sprint-planning-agent + forward-engineering-agent | planner-agent | modes governed / sprint / bounded-context; gap-identifier is an internal plan step |
| ux-agent | business-analyst-agent (story UX tables) + frontend-agent (`/ingest-figma-sketch`) | split, not a peer |
| compliance-agent | security-agent | mode compliance (HIPAA not in this factory) |
| SAST / DAST / threat (new 2026-08-17) | security-agent | modes sast / dast / threat; public `/sast-scan`, `/dast-scan`, `/threat-profile`; subagents sast-scanner, dast-scanner, threat-profiler, threat-hunter |

## Public commands added 2026-08-17 (perf + security satellites)

`/performance-test` (sre-agent mode `perf`), `/sast-scan`, `/dast-scan`, `/threat-profile` (security-agent modes). Not on the locked implement-* spine. Not a 20th primary. Not Costco docker/perf peers. DAST/hunter: this product only; no exploits.

## Public commands dropped 2026-08-17 (SRE)

`/define-slo`, `/generate-runbook`, `/validate-dr-readiness` removed from core. `sre-agent` remains; SLO/runbook/DR are internal modes, not slash commands.

## Public commands folded 2026-08-17 (tech spec + gaps)

`/write-tech-spec` → internal step of `/generate-user-story` (documentation-agent mode `tech-spec`; BA does not write the spec).  
`/gap-analysis` → internal step of `/plan-governed-stories`, `/plan-sprint`, and `/plan-bounded-context` (gap-identifier). Not public slash commands.

## `/fix-issue` (ported 2026-08-17)

Source: `costco-supplier-management/.cursor` (`commands/fix-issue.md`, `rules/12-production-fix-governance.mdc`, `agents/fix/*`, `templates/issue-log-template.md`). Generalized: no product module names. Rule number **30** (12 is reverse pack). `backend-fix-agent` / `frontend-fix-agent` absorbed as **backend-agent** / **frontend-agent** mode `fix` — no new peer agents. Classification stays in the command.

## Claude Code twin (2026-08-17)

`.claude/` is the Claude Code drop-in of this same catalog (not the Costco 82-agent roster). Flow: `CLAUDE-FLOW.md`. Format source: `costco-claude-code` (frontmatter, hooks, `CLAUDE.md` `@import` only).

## KPI promoted to core 2026-08-17

`/validate-kpi-metrics` + rules 24/26 + templates + collectors are core. `kpi-validation-agent` is quality-agent mode `kpi`. Heuristic Python scorers remain **D** (not a gate).

