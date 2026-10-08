# Agents

Flat catalog: one `*-agent.md` per primary (plus this README). Orchestrator plus 19 primaries. See repository `AGENTS.md`. Do not merge quality specialists into quality-agent. Wiring is a required check gate inside `/implement-ui` (frontend-agent), not a public command and not a peer agent.

**Command-scoped primary (not a new public command):** `work-item-mapping-agent` is spawned only from `/generate-user-stories-from-transcript` Phase 5 after CSV validation PASS.
