# /process-work-items-csv

## Objective
Analyze a work item CSV export and produce structured, user-friendly JSON (Title, Work Item ID, Work Item Type, State, hierarchy, paths, readable description). Does **not** modify the source CSV or push to external systems.

## When to use
- Azure DevOps / similar CSV exports with columns like `ID`, `Title`, `Work Item Type`
- HeartStream workshop backlog (`Workshop items.csv` at kit root)
- Separate business exports (e.g. `EPIC.csv`, `Feature.csv`)

Distinct from: ad-hoc chat parsing — always prefer the transform script for canonical output.

## Runtime Inputs

### Required
- `source_csv` — path to one `.csv`, **or multiple CSV paths** in one invocation

### Optional
- `output_json` — for a **single** CSV, default `artifacts/work-items/work-items.json`
- **Multiple CSVs:** one JSON per file — default output stem from basename: `EPIC.csv` → `artifacts/work-items/epic.json`, `Feature.csv` → `artifacts/work-items/feature.json`. Override with explicit `-o` per file when user supplies mapping.
- `mode` — `transform-only` | `full` (default `full`)
- `summary_md` — per output: `<stem>-summary.md` next to each JSON when `full` (e.g. `epic-summary.md`)

### Multi-file policy
- Run intake safety scan on **all** CSV paths in one scan command when possible.
- Run `scripts/csv-to-work-items-json.py` **once per CSV** with its own `-o` path.
- **Do not merge** work items into one JSON unless the user explicitly requests merge (register as Open DQ / one-off).

## Use Agents
`orchestrator-agent` → `work-item-csv-agent`

## Delegate to Subagents
1. `csv-intake-normalizer` (safety + manifest)
2. `csv-schema-profiler`
3. Run `scripts/csv-to-work-items-json.py` (per CSV)
4. `json-output-validator` (per output JSON)
5. `work-item-enricher` (if `full`, per summary file)

## Enforce Rules
- `.cursor/rules/heartstream-csv-governance.mdc`

## Use Templates / Skills
- `.cursor/templates/work-items-output.schema.json`
- `.cursor/templates/work-items-summary-template.md`
- `.cursor/templates/audit-trail-template.md`
- `.cursor/skills/csv-intake-safety/SKILL.md`
- `.cursor/skills/work-item-json-authoring/SKILL.md`

## Execution Policy
Plan → Act → Validate → Refine. Max 3. Iteration 1 Validate PASS → stop.

## Intake safety gate
Load `.cursor/skills/csv-intake-safety/SKILL.md`. Run `python scripts/intake-safety-scan.py <source_csv>` **before** transform. Exit 2 → **STOP**. Exit 1 → STOP until human acknowledges in audit or redacts CSV.

## Clarification Protocol
Open DQ if `source_csv` missing. Do not invent work items.

## Definition of Done
- [ ] Intake safety scan recorded in manifest (exit 0 or documented exit 1)
- [ ] Schema profile written **per source CSV**
- [ ] One `work-items.json` or `<stem>.json` per CSV from script (no silent merge)
- [ ] Validator PASS for **each** output
- [ ] Summary markdown per output when `full`
- [ ] `artifacts/audit/<date>-process-work-items-csv.md` written

## Required Output
- One JSON per processed CSV under `artifacts/work-items/` (e.g. `work-items.json`, `epic.json`, `feature.json`)
- `artifacts/work-items/<date>-manifest.json` (lists all `outputs[]`)
- `artifacts/work-items/<date>-schema-profile.json` (index) and/or `<date>-schema-profile-<stem>.json` per file
- `artifacts/work-items/<date>-validation-report.json` (index) and/or per-file validation reports
- `artifacts/audit/<date>-process-work-items-csv.md`

## Next command
Re-run with a different CSV path, or filter/summarize from a specific JSON (e.g. `feature.json` by `parent.workItemId`).
