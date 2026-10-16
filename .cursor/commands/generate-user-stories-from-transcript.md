# /generate-user-stories-from-transcript

## Objective
Convert a meeting **transcript** into **one** Excel workbook of user stories (rulebook columns; matched catalog Epic/Feature rows use the existing `ID` column) and a **separate INVEST scorecard**. Do not emit extra story CSVs or extra Excel twins.

This is the **only** public user-story command. It does **not** emit a techno-functional story pack, Gherkin pack, or tech spec.

Bootstrap CSV is used **only once** during factory setup to author the rulebook. At runtime agents load the rulebook only — never read or require the original bootstrap CSV.

## Orchestration
| Phase | Role | Agent / Subagent |
|-------|------|------------------|
| 0 Rulebook (setup only) | Primary | business-analyst-agent (mode `rulebook-bootstrap`) + user-story-csv-rulebook-author |
| **P Prerequisite** | Subagent | **workshop-prerequisite-analyzer** → knowledge-base MD + JSON (scope authority) |
| 1 Extract | Primary | business-analyst-agent (mode `transcript-ado-csv`) + transcript-analyzer, **mom-analyzer**, transcript-story-extractor (transcript + **MoM** + prerequisite scope + MSD365 catalog) |
| 2 Author rows | Subagent | ado-user-story-csv-writer → `ado_user_story_csv.py write` (canonical writer; no hand-built CSV) |
| 3 Validate scope | Subagent | **workshop-scope-compliance-validator** (prerequisite + MSD365 entity) |
| 3b Validate CSV | Subagent | user-story-csv-compliance-validator |
| 4 INVEST | Subagent | invest-validator + **invest-scorecard-evaluator** → `artifacts/intake/<date>-invest-scorecard.csv` |
| 5 Map SOW features | Primary | **work-item-mapping-agent** + work-item-hierarchy-matcher → `map-user-stories-to-sow-features.py` |

## Use Agents
| Order | Agent | Spec | When |
|-------|-------|------|------|
| Route | orchestrator-agent | `.cursor/agents/orchestrator-agent.md` | Always |
| 1 | business-analyst-agent (`transcript-ado-csv`) | `.cursor/agents/business-analyst-agent.md` | After intake-safety exit 0 |
| 2 | **work-item-mapping-agent** | `.cursor/agents/work-item-mapping-agent.md` | After `validate-user-story-csv.py` PASS **only**. Orchestrator must spawn this primary **by explicit name**. BA must not fill IDs itself. |

Spawn mapping: Task tool name `work-item-mapping-agent`, mode `map-transcript-csv`, skill `.cursor/skills/work-item-mapping/SKILL.md`, subagent `work-item-hierarchy-matcher`. **Every** validator-PASS run must attempt mapping using **`artifacts/work-items/SOW.json`** (not `epic.json` / `feature.json`). Skip Feature hierarchy only when `SOW.json` is missing or empty — register Open DQ; still complete Excel + INVEST scorecard. Never use domain-specific hint tables in agents or the mapper (see rule `32-catalog-only-work-item-mapping.mdc`).

## Runtime Inputs

### Required
- `transcript_path` (or inline transcript text persisted to `artifacts/intake/<date>-transcript.txt` before analyze)
- `mom_paths` — one or more **Minutes of Meeting** files (`.docx`, `.md`, `.txt`) for the same workshop session (official minuted decisions, agenda topics, action items)
- `prerequisite_paths` — one or more workshop prerequisite files (`.docx`, `.md`, `.txt`) defining scope, modules, and objectives for the session

### Optional
- `module_or_area_path` (defaults from transcript; must match rulebook Area Path patterns when stated)
- `parent_feature_title` / `parent_epic_title` (when transcript names parent Feature/Epic)
- `output_slug` (filename suffix)
- `sprint_number` / `story_scope_filter` (narrow extraction; do not invent stories outside the filter)
- `work_items_dir` (default `artifacts/work-items`)

### Setup-only (not runtime)
- `setup_csv` — **only** when `docs/intake/user-story-csv-rulebook.yaml` is missing. One-time bootstrap from ADO export. After rulebook exists, refuse `setup_csv` at runtime.

## Enforce Rules
`.cursor/rules/00-global-governance.mdc`, `01-project-context.mdc`, `13-business-analysis-invest.mdc`, `22-behavior-provenance-and-anti-invention.mdc`, `10-audit-trail.mdc`, `09-agent-orchestration.mdc`, `31-untrusted-intake.mdc`

## Intake safety gate
Prerequisite document(s), **MoM**, and transcript (not rulebook, not generated CSV). Load `.cursor/skills/intake-safety/SKILL.md`. Run `python3 scripts/intake-safety-scan.py` on all `prerequisite_paths`, all `mom_paths`, and the transcript **before** spawning business-analyst-agent. Exit 2 → STOP. Exit 1 → STOP until redaction or waiver. Exit 0 → continue.

## Use Templates
`user-story-csv-rulebook-template.yaml`, `workshop-prerequisite-knowledge-base-template.md`, `transcript-story-extraction-template.md`, `audit-trail-template.md`

## Use Skills
`.cursor/skills/intake-safety/SKILL.md`, `.cursor/skills/workshop-prerequisite-analysis/SKILL.md`, `.cursor/skills/user-story-from-transcript/SKILL.md`, `.cursor/skills/work-item-mapping/SKILL.md`

## Workshop prerequisite scope (mandatory)
- **Rulebook:** `docs/intake/workshop-prerequisite-scope-rulebook.yaml`
- **Phase P:** **workshop-prerequisite-analyzer** writes:
  - `artifacts/intake/<date>-workshop-prerequisite-knowledge-base.md`
  - `artifacts/intake/<date>-workshop-prerequisite-knowledge-base.json`
- For `.docx` prerequisites: `python scripts/extract-docx-text.py <file.docx> --out artifacts/intake/.pipeline/<slug>-prerequisite.txt` before analysis.
- For `.docx` MoM: `python scripts/extract-docx-text.py <file.docx> --out artifacts/intake/.pipeline/<slug>-mom.txt` (or `artifacts/intake/<date>-mom.txt` when a single consolidated extract is preferred) before **mom-analyzer**.
- **Scope rule:** prerequisite materials define what is in scope; **transcript** supplies detailed requirements; **MoM** supplies official minuted decisions and agenda alignment. Do **not** emit User Stories for topics that fail prerequisite alignment (record under **Out of scope / excluded (prerequisite)** in extraction notes). MoM ↔ transcript conflicts → Open DQ in extraction notes; do not silently resolve.
- Each User Story row JSON must include `prerequisite_refs` (IDs from knowledge base), `transcript_locator`, `transcript_source_path`, `mom_locator`, `mom_source_path`.

## MSD365 Business Entity scope (mandatory)
- **Rulebook:** `docs/intake/msd365-business-entity-scope-rulebook.yaml`
- **Catalog (runtime):** `docs/intake/msd365-business-entity-catalog.json` — built once from `Area Paths.xlsx` sheet **Details** (columns 2–4; column 1 ignored; column 4 may be empty) via `python scripts/build-msd365-business-entity-catalog.py`
- Each User Story in `<date>-user-story-rows.json` must include `msd365_domain`, `msd365_application`, and `msd365_business_entity` (empty string when the matched Excel row has no business entity). **Closed world:** do not author stories for Dynamics 365 business entities outside `catalog.business_entities`.
- Run **workshop-scope-compliance-validator** (or both scripts) after rows JSON is written:
  - `python scripts/validate-user-story-workshop-scope.py --json artifacts/intake/<date>-user-story-rows.json --knowledge-base artifacts/intake/<date>-workshop-prerequisite-knowledge-base.json --require-mom`
  - `python scripts/validate-user-story-business-entity-scope.py --json artifacts/intake/<date>-user-story-rows.json`
  FAIL → Reflect (exclude or remap; document in extraction notes).

## Execution Policy
Plan → Act → Observe → Reflect (max 3). Iteration 1 Observe pass with validator PASS → INVEST scorecard → mapping → stop.

## Command-Specific Hardening
- **Output-path check gate (mandatory, before any write):** run
  `python scripts/output-path-gate.py --check artifacts/intake/<date>-workshop-prerequisite-knowledge-base.md artifacts/intake/<date>-workshop-prerequisite-knowledge-base.json artifacts/intake/<date>-transcript-story-extraction.md artifacts/intake/<date>-user-story-rows.json artifacts/intake/.pipeline/<date>-user-stories-working.csv artifacts/intake/<date>-user-story-csv-validation.json artifacts/intake/<date>-invest-scorecard.csv artifacts/intake/<date>-user-stories-from-transcript.xlsx --json`.
  - Exit `0` (CLEAR) → proceed to write.
  - Exit `2` (CONFLICT) → **STOP**. Ask **"new"** vs **"overwrite"**. Never pick a side for the human.
- Load `docs/intake/user-story-csv-rulebook.yaml` every run; column order and headers are fixed (`columns.stories.order` / `csv.column_order`: State, ID, Work Item Type, Title 1, Title 2, Title 3, …).
- Extract requirements from transcript with locators; no invented FR/BR IDs in CSV cells.
- **Mandatory write path:** persist rows to `artifacts/intake/<date>-user-story-rows.json`, then  
  `python scripts/ado_user_story_csv.py write --json <rows.json> --out artifacts/intake/.pipeline/<date>-user-stories-working.csv`  
  (working CSV is **internal** for the validator only — not a public Excel).
- **ADO layout (transcript CSV):** Workshop → User Stories → Issue/Risk. Workshop title in **Title 1**; User Story title in **Title 3**. Do not invent Epic/Feature titles from the transcript.
- **ADO layout (public Excel after mapping):** Workshop → **SOW Feature** (Title 2 = `<minutes> - <topic>`, Description = topic, **blank ID**, Annexure ID1 = minutes) → **User Stories** under that Feature (Title 3, blank ID) → next SOW Feature block. **No Epic rows.** Unmatched stories and Issue/Risk after Feature blocks. AC **one `- ` bullet per line**. Styling from the rulebook.
- User Story rows: Title 3 (short), Description (`As a … I need to … so that …`), Acceptance Criteria (`- ` bullets per line).
- Do not add Priority or Story Point columns to the ADO CSV.
- Run `python scripts/validate-user-story-csv.py --csv artifacts/intake/.pipeline/<date>-user-stories-working.csv --report <validation.json>`; FAIL → stay in Reflect. Do **not** map until this PASS.
- **INVEST scorecard (separate file only):** after validator PASS, run **invest-scorecard-evaluator**. Write `artifacts/intake/<date>-invest-scorecard.csv`. Do **not** put INVEST on the Excel workbook or on the working CSV. Gate: no critical dimension below 5; overall ≥ 7 for Pass. Needs Refinement → Reflect (max 3), do not invent copy to force a pass.
- **SOW first (mandatory):** Load `artifacts/work-items/SOW.json` before extracting or authoring User Stories. Align each story to a SOW annexure topic; do **not** use `epic.json` or `feature.json` for transcript mapping.
- **Identify SOW feature, then story.** Map each requirement to the best-matching SOW row (up to `work_item_mapping.max_related_features` when several qualify). Use `prerequisite_refs` on row JSON when present (`OBJ-00n` → `WS-CE-0n`).
- **Work item mapping (after CSV PASS):** load `.cursor/skills/work-item-mapping/SKILL.md`. Spawn **work-item-mapping-agent**. Run `map-user-stories-to-sow-features.py`. Public Excel: Workshop → SOW Feature → User Stories; Feature **ID** blank; **Annexure ID1** = SOW minutes.
  ```
  python scripts/map-user-stories-to-sow-features.py --csv artifacts/intake/.pipeline/<date>-user-stories-working.csv --rows-json artifacts/intake/<date>-user-story-rows.json --work-items-dir artifacts/work-items --out-xlsx artifacts/intake/<date>-user-stories-from-transcript.xlsx --log-json artifacts/intake/.pipeline/<date>-work-item-mapping-log.json
  ```
- Optional regression: `python scripts/test_ado_user_story_csv_layout.py` after rulebook/layout changes.
- Never read any bootstrap `setup_csv` / `setup_xlsx` or a prior workshop export when the Active rulebook exists.

## Clarification Protocol
Register Open DQ for: transcript path, **mom_paths**, area path, parent Feature/Epic when hierarchy is ambiguous, empty work-items catalog. Do not invent columns or work item types. Do not STOP except human gates. Refuse when rulebook missing and no one-time `setup_csv` supplied. Refuse when `mom_paths` is absent.

## Artifact Persistence
**Public (operator):**
- `artifacts/intake/<date>-user-stories-from-transcript.xlsx` — **the only Excel**; Epic/Feature catalog IDs; User Stories grouped under each Feature with blank `ID`
- `artifacts/intake/<date>-invest-scorecard.csv` — INVEST only (separate)

**Internal (not extra Excels):**
- `artifacts/intake/<date>-workshop-prerequisite-knowledge-base.md`
- `artifacts/intake/<date>-workshop-prerequisite-knowledge-base.json`
- `artifacts/intake/<date>-transcript-story-extraction.md` (transcript + MoM cited facts)
- `artifacts/intake/.pipeline/<slug>-mom.txt` or `artifacts/intake/<date>-mom.txt` (normalized MoM text when sourced from `.docx`)
- `artifacts/intake/<date>-user-story-rows.json`
- `artifacts/intake/.pipeline/<date>-user-stories-working.csv` (validator input)
- `artifacts/intake/<date>-user-story-csv-validation.json`
- `artifacts/intake/.pipeline/<date>-work-item-mapping-log.json`
- `artifacts/audit/<date>-generate-user-stories-from-transcript-<task>.md`

## Definition of Done
- [ ] Output-path gate run before any write; CLEAR, or CONFLICT resolved by explicit human "new"/"overwrite" choice
- [ ] Intake-safety scan exit 0, or exit 1 with recorded human redaction/waiver
- [ ] Rulebook loaded (or one-time bootstrap completed and persisted)
- [ ] Prerequisite knowledge base MD + JSON written from `prerequisite_paths`
- [ ] `validate-user-story-workshop-scope.py` exit 0 on rows JSON
- [ ] MoM normalized and analyzed; extraction notes cite transcript **and** MoM locators; MoM ↔ transcript conflicts → Open DQ in notes, not silent resolution
- [ ] `validate-user-story-workshop-scope.py` run with `--require-mom`
- [ ] Working CSV headers match rulebook `columns.stories.order` / `csv.column_order` exactly
- [ ] `validate-user-story-business-entity-scope.py` exit 0 on rows JSON
- [ ] `validate-user-story-csv.py` exit 0
- [ ] One public Excel written; no `*-mapped.csv` / second story workbook
- [ ] INVEST scorecard written as a **separate** CSV (not a sheet in the Excel)
- [ ] Mapping run after PASS (or skipped with Open DQ if SOW.json absent); public Excel uses Workshop → SOW Feature → User Stories; Feature `ID` blank, Annexure ID1 set; User Story `ID` blank; no Epic rows
- [ ] Internal mapping log lists every User Story as matched or unmatched
- [ ] `artifacts/audit/<date>-generate-user-stories-from-transcript-<task>.md` written
- [ ] Harness updated (phase-changing)

## Next command

> ✅ `/generate-user-stories-from-transcript` complete.
> **Next command:** Use `artifacts/intake/<date>-user-stories-from-transcript.xlsx` (and the separate INVEST CSV) with `/generate-test-cases-from-user-stories`, `/plan-governed-stories`, or `/plan-sprint`.
