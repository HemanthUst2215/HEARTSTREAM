# Commands (focused kit)

| Command | Primary agent(s) |
|---------|------------------|
| `/generate-user-stories-from-transcript` | business-analyst-agent → **work-item-mapping-agent** (after CSV PASS); INVEST scorecard in Phase 4 |
| `/expand-test-coverage` | quality-agent + test-agent (design only) |
| `/process-work-items-csv` | work-item-csv-agent (CSV → JSON) |

**Preserved (not pruned):** `docs/`, `scripts/`, `tools/`, `.cursor/rules/`, `.cursor/templates/`.

Re-run prune: `python scripts/prune_factory_keep_two_commands.py` (close locked files under `artifacts/` first).
