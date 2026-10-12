# HEARTSTREAM-1 — focused factory slice

Slash commands plus full **docs**, **scripts**, **tools**, **rules**, and **templates** trees.

| Command | Purpose |
|---------|---------|
| `/generate-user-stories-from-transcript` | Transcript → one Excel (stories + Epic/Feature/Workshop IDs) and a **separate** INVEST scorecard CSV |
| `/expand-test-coverage` | FR/BR test case design + coverage gate (stops at Pending Approval) |
| `/process-work-items-csv` | Work item CSV export → `artifacts/work-items/*.json` |
| `/evaluate-user-stories` | Manual CSV vs AI-generated CSV, transcript as ground truth → HTML evaluation report |

Operator setup: copy `.cursor/` + `.cursorrules`; merge `.cursor/config.yaml` from example if needed.

Prune helper: `scripts/prune_factory_keep_two_commands.py` — never deletes `docs/`, `scripts/`, `tools/`, `.cursor/rules/`, or `.cursor/templates/`.
