# Decisions Log

| Field | Value |
|-------|-------|
| **Updated** | 2026-10-09 |
| **Legend** | **User** = user-locked · **Agent** = agent recommendation accepted |

## Decisions

| Date | Decision | Who | Source |
|------|----------|-----|--------|
| 2026-08-17 | Shrink core primaries to 19. Commands stay. Absorbed specialists become modes or check gates. Do not merge backend+frontend, quality+test, review+cleanup, or BRD+stories. | User | chat lock |
| 2026-08-17 | Agent/asset refinement is hand-edit after reading each contract. Do not use Python emitters (`apply_agent_shrink.py`, `emit_factory.py`, `finish_factory.py`) to rewrite agents. | User | chat lock |
| 2026-08-17 | Drop public `/define-slo`, `/generate-runbook`, `/validate-dr-readiness`. Keep sre-agent with internal modes. | User | chat lock |
| 2026-08-17 | Port `/fix-issue` from costco-supplier-management. Classification in command. backend-fix-agent / frontend-fix-agent become backend-agent / frontend-agent mode `fix`. Rule 30. | User | chat lock |
| 2026-08-17 | Promote `/validate-kpi-metrics` to core (quality-agent mode `kpi`). Packs remain for domain overlays only. | User | chat lock |
| 2026-08-17 | Add Claude Code drop-in `.claude/` + `CLAUDE-FLOW.md`, mirroring the locked 19-primary Cursor catalog. Do not import Costco's 82-agent roster or `/phase-*` / `/generate-backend` public commands. | User | chat lock |
| 2026-08-17 | Remove `packs/`. Promote bounded-context, data-migration, figma-design-system, validation-chain into core. Delete remaining overlays. | User | chat lock |
| 2026-08-17 | Remove public `/write-tech-spec` and `/gap-analysis`. Tech spec is an internal step of `/generate-user-story`. Gap analysis is an internal step of the plan commands. | User | chat lock |
| 2026-08-17 | Supersede the KPI row that said packs remain: there is no `packs/` overlay. KPI stays core (quality-agent mode `kpi`). | User | chat lock |
| 2026-08-17 | Repair harness/evals/audit alignment: phase-changing command list in rule 10; audit paths on thin DoDs; factory evals grade 19-primary catalog and Claude twin. | User | chat lock |
| 2026-08-17 | Flatten `.cursor/agents/`, `.cursor/subagents/`, and `.claude/subagents/` — no domain subfolders (`api/`, `backend/`, `business/`, …). Identity is filename / YAML `name:`. | User | chat lock |
| 2026-08-17 | Add GitHub Copilot drop-in `.github/` + `COPILOT-FLOW.md`, mirroring the locked 19-primary catalog. Do not import Costco docker/perf Copilot agents. | User | chat lock |
| 2026-08-17 | Supersede the hand-edit lock: never use Python to **build or refine** the factory. Hand-edit `.cursor/`, `.claude/`, and `.github/` after reading each contract. Banned: `emit_factory.py`, `finish_factory.py`, `apply_agent_shrink.py`, `sync_claude_from_cursor.py`, `sync_copilot_from_cursor.py`, and any new catalog generator. Allowed Python: product tools only (`lint_contracts.py` read-only, `figma/validate.py`, `export/convert.py`). | User | chat lock |
| 2026-09-11 | Retrofit Opticals test split into all three twins. Locked execute spine is implement-api → implement-ui → expand-test-coverage → **[human: test-package Approved]** → run-tests → run-eval → review-changes → application-summary. `/expand-test-coverage` is design-only. `/run-eval` is the sole eval entry. `/review-changes` does not run eval-agent. Catalog remains 19 primaries. Portable artifacts: `docs/test-cases.md`, `docs/test-matrix.md`, `docs/test-cases-br-coverage.md`, `docs/quality/test-package-review.md`. ASSUMPTION-PCC-002: implement-* slice tests are not blocked by expand PASS. | User | Opticals `.cursor` retrofit |
| 2026-09-13 | `playwright-self-healer` uses Observe → Orient → Decide → Act (`ooda-self-heal-loop.md`) as an inner loop on `/run-tests` Phase 5 only. Not a factory-wide loop; PAVR/PAOR unchanged. Not a 20th primary. Suggestions only — mutating Act requires human proceed. `e2e-defect-analyzer` stays a single pass. | User | chat: OODA for self-heal |
| 2026-10-09 | `/generate-test-cases-from-user-stories` groups User Stories by mapped Feature ID when the story `ID` matches a Feature row in the same workbook (ADO mapping). Nearest-preceding Feature is fallback only. ASSUMPTION-MSDTC-001: platform label `Microsoft Dynamics` when a story names no application. | Agent | `/generate-test-cases-from-user-stories` |

Only `harness-updater` appends rows. No secrets or PHI. Never overwrite a prior decision row.
