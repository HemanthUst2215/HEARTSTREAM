# Work Item CSV Agent

## Goal
Own end-to-end conversion of work item CSV export(s) into validated, human-friendly JSON under `artifacts/work-items/` — **one canonical JSON file per source CSV**.

## Must / Must NOT
- Must: run `scripts/intake-safety-scan.py` on every CSV before transformation; run `scripts/csv-to-work-items-json.py` **once per CSV** with a dedicated `-o` path; spawn subagents for manifest, schema profile, optional narrative enrichment, and validation per output; cite CSV row `ID` for every work item.
- Must NOT: drop rows silently; rename core fields without mapping in output; **merge multiple CSVs into one JSON** unless the user explicitly requests merge; overwrite JSON without recording source path in audit; write outside scope allowlist.

## Input checklist
- Path to source CSV (required) — **or multiple CSV paths**
- Optional `-o` output path per file (single CSV default: `artifacts/work-items/work-items.json`)
- Multiple CSVs without `-o`: derive `artifacts/work-items/<basename-stem>.json` (e.g. `EPIC.csv` → `epic.json`)
- Optional `--summary-md` per output (default `<stem>-summary.md` beside JSON when `full`)

## Output checklist
- `artifacts/work-items/<date>-manifest.json` with `outputs[]` listing each `source_csv` → `output_json`
- `artifacts/work-items/<date>-schema-profile-<stem>.json` per source (plus optional index `<date>-schema-profile.json`)
- One JSON per CSV (e.g. `work-items.json`, `epic.json`, `feature.json`)
- Optional per-file summary markdown
- `artifacts/audit/<date>-process-work-items-csv.md` (or `<date>-work-item-csv-agent-<task>.md`)

## Clarification protocol
Open DQ when columns differ from `config.yaml` `csv_pipeline.required_columns`. Continue with profiler output when extra columns exist; STOP only on safety scan exit 2.

## Execution loop
Plan → Act → Validate → Refine (max 3).

1. **Plan** — confirm paths; load `.cursor/skills/csv-intake-safety/SKILL.md`; assign one output JSON per CSV
2. **Act** — scan all CSVs; chain subagents; run transform script per file
3. **Validate** — **json-output-validator** must PASS for **each** output
4. **Refine** — fix mapping or script flags from validator feedback (max 3)

## Check gates
- csv-intake-normalizer: manifest + scan status + `outputs[]`
- csv-schema-profiler: column coverage per file
- json-output-validator: schema + row count parity per JSON

## Definition of Done
- [ ] Safety scan exit 0 or documented waiver in audit (exit 1)
- [ ] Manifest and schema profile(s) written
- [ ] One script-produced JSON per CSV (no merge)
- [ ] Validator PASS for each JSON
- [ ] Agent audit written

## Delegates
1. `csv-intake-normalizer`
2. `csv-schema-profiler`
3. `work-item-enricher` (optional summaries — after each JSON exists)
4. `json-output-validator`

## Modes
- `transform-only` — script + validator, no LLM enrichment
- `full` — default; includes enricher summary markdown per output
