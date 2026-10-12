# /generate-user-stories-from-transcript

## Objective
Convert a meeting **transcript** into **one** Excel workbook of user stories (rulebook columns; matched catalog Epic/Feature rows use the existing `ID` column) and a **separate INVEST scorecard**. Do not emit extra story CSVs or extra Excel twins.

This is the **only** public user-story command. It does **not** emit a techno-functional story pack, Gherkin pack, or tech spec.

Bootstrap CSV is used **only once** during factory setup to author the rulebook. At runtime agents load the rulebook only — never read or require the original bootstrap CSV.

## Orchestration
| Phase | Role | Agent / Subagent |
|-------|------|------------------|
| 0 Rulebook (setup only) | Primary | business-analyst-agent (mode `rulebook-bootstrap`) + user-story-csv-rulebook-author |
| 1 Extract | Primary | business-analyst-agent (mode `transcript-ado-csv`) + transcript-analyzer, transcript-story-extractor |
| 2 Author rows | Subagent | ado-user-story-csv-writer → `ado_user_story_csv.py write` (canonical writer; no hand-built CSV) |
| 3 Validate | Subagent | user-story-csv-compliance-validator |
| 4 INVEST | Subagent | invest-validator + **invest-scorecard-evaluator** → `artifacts/intake/<date>-invest-scorecard.csv` |
| 5 Map hierarchy IDs | Primary | **work-item-mapping-agent** + work-item-hierarchy-matcher → `map-user-stories-to-work-items.py` |

## Use Agents
| Order | Agent | Spec | When |
|-------|-------|------|------|
| Route | orchestrator-agent | `.cursor/agents/orchestrator-agent.md` | Always |
| 1 | business-analyst-agent (`transcript-ado-csv`) | `.cursor/agents/business-analyst-agent.md` | After intake-safety exit 0 |
| 2 | **work-item-mapping-agent** | `.cursor/agents/work-item-mapping-agent.md` | After `validate-user-story-csv.py` PASS **only**. Orchestrator must spawn this primary **by explicit name**. BA must not fill IDs itself. |

Spawn mapping: Task tool name `work-item-mapping-agent`, mode `map-transcript-csv`, skill `.cursor/skills/work-item-mapping/SKILL.md`, subagent `work-item-hierarchy-matcher`. **Every** validator-PASS run must attempt mapping. Skip spawn only when configured `catalog_epic_json` or `catalog_feature_json` under `artifacts/work-items/` is missing or has no `workItems[]` — register Open DQ; still complete the Excel (IDs blank) + separate INVEST scorecard. Never use domain-specific hint tables in agents or the mapper (see rule `32-catalog-only-work-item-mapping.mdc`).

## Runtime Inputs

### Required
- `transcript_path` (or inline transcript text persisted to `artifacts/intake/<date>-transcript.txt` before analyze)

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
Raw transcript only (not rulebook, not generated CSV). Load `.cursor/skills/intake-safety/SKILL.md`. Run `python3 scripts/intake-safety-scan.py` on transcript path **before** spawning business-analyst-agent. Exit 2 → STOP. Exit 1 → STOP until redaction or waiver. Exit 0 → continue.

## Use Templates
`user-story-csv-rulebook-template.yaml`, `transcript-story-extraction-template.md`, `audit-trail-template.md`

## Use Skills
`.cursor/skills/intake-safety/SKILL.md`, `.cursor/skills/user-story-from-transcript/SKILL.md`, `.cursor/skills/work-item-mapping/SKILL.md`

## Execution Policy
Plan → Act → Observe → Reflect (max 3). Iteration 1 Observe pass with validator PASS → INVEST scorecard → mapping → stop.

## Command-Specific Hardening
- **Output-path check gate (mandatory, before any write):** run
  `python scripts/output-path-gate.py --check artifacts/intake/<date>-transcript-story-extraction.md artifacts/intake/<date>-user-story-rows.json artifacts/intake/.pipeline/<date>-user-stories-working.csv artifacts/intake/<date>-user-story-csv-validation.json artifacts/intake/<date>-invest-scorecard.csv artifacts/intake/<date>-user-stories-from-transcript.xlsx --json`.
  - Exit `0` (CLEAR) → proceed to write.
  - Exit `2` (CONFLICT) → **STOP**. Ask **"new"** vs **"overwrite"**. Never pick a side for the human.
- Load `docs/intake/user-story-csv-rulebook.yaml` every run; column order and headers are fixed **for the ADO CSV**.
- Extract requirements from transcript with locators; no invented FR/BR IDs in CSV cells.
- **Mandatory write path:** persist rows to `artifacts/intake/<date>-user-story-rows.json`, then  
  `python scripts/ado_user_story_csv.py write --json <rows.json> --out artifacts/intake/.pipeline/<date>-user-stories-working.csv`  
  (working CSV is **internal** for the validator only — not a public Excel).
- **ADO layout (transcript CSV):** Workshop → User Stories → Issue/Risk. Do not invent Epic/Feature titles from the transcript.
- **ADO layout (public Excel after mapping):** Workshop → **matched catalog Epics (with ID)** → **matched catalog Features (with ID)** → User Stories. User Story **Area Path blank**; AC **one `- ` bullet per line** (ASCII hyphen).
- User Story rows: Title (short), Description (`As a … I need to … so that …`), Acceptance Criteria (`- ` bullets per line).
- Do not add Priority or Story Point columns to the ADO CSV.
- Run `python scripts/validate-user-story-csv.py --csv artifacts/intake/.pipeline/<date>-user-stories-working.csv --report <validation.json>`; FAIL → stay in Reflect. Do **not** map until this PASS.
- **INVEST scorecard (separate file only):** after validator PASS, run **invest-scorecard-evaluator**. Write `artifacts/intake/<date>-invest-scorecard.csv`. Do **not** put INVEST on the Excel workbook or on the working CSV. Gate: no critical dimension below 5; overall ≥ 7 for Pass. Needs Refinement → Reflect (max 3), do not invent copy to force a pass.
- **Catalog first (mandatory):** Load `artifacts/work-items/epic.json` and `artifacts/work-items/feature.json` before extracting or authoring User Stories. Use **only** existing Epics/Features — never create new hierarchy items or IDs.
- **Identify Feature, then story.** Map each requirement to the best-matching existing Feature (up to `work_item_mapping.max_related_features` when several qualify). Parent Epic must exist in `epic.json`.
- **Work item mapping (after CSV PASS):** load `.cursor/skills/work-item-mapping/SKILL.md`. Spawn **work-item-mapping-agent**. Generic scoring via `map-user-stories-to-work-items.py` (threshold, margin, optional `workshop_context_min_overlap` in config — no hardcoded domains). Public Excel layout as `artifacts/intake/2026-10-08-user-stories-from-transcript-v2.xlsx`: Workshop → matched Epic → matched Feature → User Stories (`ID` = Feature workItemId). Do not invent IDs; blank `ID` when no catalog Feature qualifies.
  ```
  python scripts/map-user-stories-to-work-items.py --csv artifacts/intake/.pipeline/<date>-user-stories-working.csv --work-items-dir artifacts/work-items --out-xlsx artifacts/intake/<date>-user-stories-from-transcript.xlsx --log-json artifacts/intake/.pipeline/<date>-work-item-mapping-log.json
  ```
- Optional regression: `python scripts/test_ado_user_story_csv_layout.py` after rulebook/layout changes.
- Never read `WS-68405.csv` or any `setup_csv` path when rulebook exists.

## Clarification Protocol
Register Open DQ for: transcript path, area path, parent Feature/Epic when hierarchy is ambiguous, empty work-items catalog. Do not invent columns or work item types. Do not STOP except human gates. Refuse when rulebook missing and no one-time `setup_csv` supplied.

## Artifact Persistence
**Public (operator):**
- `artifacts/intake/<date>-user-stories-from-transcript.xlsx` — **the only Excel**; Epic/Feature rows keep catalog IDs; each matched User Story `ID` is the Feature workItemId identified from the transcript
- `artifacts/intake/<date>-invest-scorecard.csv` — INVEST only (separate)

**Internal (not extra Excels):**
- `artifacts/intake/<date>-transcript-story-extraction.md`
- `artifacts/intake/<date>-user-story-rows.json`
- `artifacts/intake/.pipeline/<date>-user-stories-working.csv` (validator input)
- `artifacts/intake/<date>-user-story-csv-validation.json`
- `artifacts/intake/.pipeline/<date>-work-item-mapping-log.json`
- `artifacts/audit/<date>-generate-user-stories-from-transcript-<task>.md`

## Definition of Done
- [ ] Output-path gate run before any write; CLEAR, or CONFLICT resolved by explicit human "new"/"overwrite" choice
- [ ] Intake-safety scan exit 0, or exit 1 with recorded human redaction/waiver
- [ ] Rulebook loaded (or one-time bootstrap completed and persisted)
- [ ] Extraction notes cite transcript locators; conflicts → Open DQ in notes, not silent resolution
- [ ] Working CSV headers match rulebook `column_order` exactly
- [ ] `validate-user-story-csv.py` exit 0
- [ ] One public Excel written; no `*-mapped.csv` / second story workbook
- [ ] INVEST scorecard written as a **separate** CSV (not a sheet in the Excel)
- [ ] Mapping run after PASS (or skipped with Open DQ if work-items catalog absent); every User Story `ID` is a catalog Feature workItemId; blank only when no catalog Feature relates
- [ ] Internal mapping log lists every User Story as matched or unmatched
- [ ] `artifacts/audit/<date>-generate-user-stories-from-transcript-<task>.md` written
- [ ] Harness updated (phase-changing)

## Next command

> ✅ `/generate-user-stories-from-transcript` complete.
> **Next command:** Use `artifacts/intake/<date>-user-stories-from-transcript.xlsx` (and the separate INVEST CSV) with `/generate-test-cases-from-user-stories`, `/plan-governed-stories`, or `/plan-sprint`.
