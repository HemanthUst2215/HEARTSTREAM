# Agents

Flat catalog: one `*-agent.md` per primary (plus this README). Orchestrator plus 19 primaries. See repository `AGENTS.md`. Do not merge quality specialists into quality-agent. Wiring is a required check gate inside `/implement-ui` (frontend-agent), not a public command and not a peer agent.

**Command-scoped primary (not a new public command):** `work-item-mapping-agent` is spawned only from `/generate-user-stories-from-transcript` Phase 5 after CSV validation PASS.

**Command primary:** `user-story-evaluation-agent` is the primary for `/evaluate-user-stories` and `/generate-html-for-user-stories` (mode `source-traceability-html`). Compare-csv metrics stay in `*-evaluator.md`; source traceability uses `source-knowledge-base-unifier` and `user-story-source-traceability-analyzer`.

**Command primary (existing agent, new mode):** `test-agent` mode `from-user-story-excel` is the primary for `/generate-test-cases-from-user-stories`. Not a 20th primary.
