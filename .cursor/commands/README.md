# Commands (focused kit)

| Command | Primary agent(s) |
|---------|------------------|
| `/generate-user-stories-from-transcript` | business-analyst-agent → **work-item-mapping-agent** (after CSV PASS); INVEST scorecard in Phase 4 |
| `/expand-test-coverage` | quality-agent → test-agent (`from-transcript`): transcript → Epic/Feature match → rulebook test-case CSV |
| `/process-work-items-csv` | work-item-csv-agent (CSV → JSON) |
| `/evaluate-user-stories` | user-story-evaluation-agent (manual CSV vs generated CSV vs transcript → HTML) |
| `/generate-html-for-user-stories` | user-story-evaluation-agent `source-traceability-html` (manual + AI each vs sources → two HTML reports) |
| `/generate-test-cases-from-user-stories` | test-agent (`from-user-story-excel`): User Story Excel → MSD E2E workbook via MSD rulebook |

**Preserved (not pruned):** `docs/`, `scripts/`, `tools/`. Rules, templates, and skills are limited to what these commands and their agents load.

Re-run prune: `python scripts/prune_factory_keep_two_commands.py` (close locked files under `artifacts/` first).
