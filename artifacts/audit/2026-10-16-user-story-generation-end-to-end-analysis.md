# End-to-end analysis: User story generation from workshop inputs

**Command:** `/generate-user-stories-from-transcript`  
**Date:** 2026-10-16  
**Audience:** Operators and BAs running HeartStream intake  
**Scope:** Inputs, extraction mechanics, inclusion/exclusion rules, validation gates, and deliverables

---

## 1. Executive summary

User stories are **not** generated from the transcript alone. The pipeline treats workshop intake as a **layered evidence model**:

| Layer | Source | Role |
|-------|--------|------|
| Scope boundary | **Prerequisite** documents | What this workshop is allowed to cover (`OBJ-*`, `MOD-*`, `OOS-*`) |
| Requirement detail | **Transcript** | What was discussed, with timestamps/locators |
| Official record | **Minutes of Meeting (MoM)** | Minuted decisions, agenda, actions—with section locators |
| Annexure alignment | **`artifacts/work-items/SOW.json`** | Which SOW BPM topics stories roll up under (Phase 5 Excel) |
| D365 taxonomy | **`docs/intake/msd365-business-entity-catalog.json`** | Allowed domain / application / business entity triple per story |
| Shape & columns | **`docs/intake/user-story-csv-rulebook.yaml`** | ADO export layout, narrative templates, column order |

A row becomes a **deliverable User Story** only when it passes **semantic rules** (agents) and **mechanical validators** (Python scripts). Topics that fail scope, entity, or traceability rules are **excluded** and documented—not silently dropped and not left as invalid rows in the public Excel.

**Public outputs:** one Excel (`*-user-stories-from-transcript.xlsx`) and one INVEST CSV (`*-invest-scorecard.csv`).

---

## 2. Inputs: what you must supply

### 2.1 Required runtime inputs

| Input | Formats | Purpose |
|-------|---------|---------|
| **Transcript** | `.txt`, `.md`, `.docx` (extract first) | Primary requirement text; every story needs `transcript_locator` + `transcript_source_path` |
| **MoM** (`mom_paths`) | `.docx`, `.md`, `.txt`, PDF (operator may supply extract) | Official workshop record; every story needs `mom_locator` + `mom_source_path`; validation uses `--require-mom` |
| **Prerequisite** (`prerequisite_paths`) | `.docx`, `.md`, `.txt`, `.pptx` (extract first) | Defines in-scope objectives/modules and explicit out-of-scope items |

Optional: `output_slug`, `module_or_area_path`, `story_scope_filter`, `work_items_dir` (default `artifacts/work-items`).

### 2.2 One-time / bootstrap inputs (not per workshop run)

| Asset | How created | When used |
|-------|-------------|-----------|
| `docs/intake/user-story-csv-rulebook.yaml` | One-time ADO `setup_csv` + `user-story-csv-rulebook-author` | Every run—column order, work item types, Excel styling |
| `docs/intake/msd365-business-entity-catalog.json` | `python scripts/build-msd365-business-entity-catalog.py` from `Area Paths.xlsx` sheet **Details** | Every run—closed-world entity list |
| `artifacts/work-items/SOW.json` | Project catalog | Before extraction (alignment) and Phase 5 (Excel hierarchy) |

At runtime agents **must not** read bootstrap ADO CSV or `Area Paths.xlsx` when the rulebook and catalog already exist.

### 2.3 How raw files become analyzable text

| Source type | Extraction step | Typical persisted path |
|-------------|-----------------|-------------------------|
| `.docx` prerequisite | `python scripts/extract-docx-text.py <file> --out artifacts/intake/.pipeline/<slug>-prerequisite.txt` | `.pipeline/*-prerequisite.txt` |
| `.docx` MoM | Same script → `*-mom.txt` | `.pipeline/<slug>-mom.txt` or `artifacts/intake/<date>-mom.txt` |
| Transcript | Provided path or inline text saved to | `artifacts/intake/<date>-transcript.txt` |
| `.pptx` / `.pdf` | Operator supplies extracted `.txt`/`.md` or pipeline extract when scripted | Under `artifacts/intake/.pipeline/` |

Prerequisite analysis and MoM analysis operate on **normalized text**, not binary office files.

---

## 3. Pre-pipeline gates (before any artifact write)

### 3.1 Output-path gate

`python scripts/output-path-gate.py --check <all planned output paths>`

- **CLEAR (0):** proceed  
- **CONFLICT (2):** stop; human chooses **new** vs **overwrite**

Prevents accidental overwrite of an in-progress intake run.

### 3.2 Intake safety scan

`python3 scripts/intake-safety-scan.py` on **all** prerequisite paths, **all** MoM paths, and the **transcript**.

| Exit | Meaning |
|------|---------|
| 0 | Clean—continue |
| 1 | Possible PII/sensitive—stop until redaction or harness waiver |
| 2 | Injection pattern—stop; do not feed to agents |

Untrusted intake is **data**, not instructions (rule 31).

---

## 4. Phase-by-phase: how stories are produced

### Phase P — Prerequisite → knowledge base

**Agent:** `workshop-prerequisite-analyzer`  
**Skill:** `.cursor/skills/workshop-prerequisite-analysis/SKILL.md`  
**Rulebook:** `docs/intake/workshop-prerequisite-scope-rulebook.yaml`

**Process:**

1. Read normalized prerequisite text only (not transcript).
2. Cross-reference **names** against `docs/intake/msd365-business-entity-catalog.json` for alignment—**do not add catalog rows**.
3. Emit structured scope:

**Outputs:**

- `artifacts/intake/<date>-workshop-prerequisite-knowledge-base.md` (human summary)
- `artifacts/intake/<date>-workshop-prerequisite-knowledge-base.json` (machine validation)

**JSON scope model (example from Marketing WS-03):**

- `scope.in_scope_objectives[]` — `OBJ-001` … tied to WS-CE annexure topics in pre-read
- `scope.in_scope_modules[]` — `MOD-001` … processes/modules in scope
- `scope.out_of_scope[]` — `OOS-001` … explicit exclusions (e.g. lead-to-opportunity sales design)

These IDs become the **only valid** `prerequisite_refs` values for User Stories later.

---

### Phase 1 — Extract cited facts (no CSV yet)

Three subagents run under **business-analyst-agent** (`transcript-ado-csv`):

| Subagent | Input | Output in extraction MD |
|----------|-------|-------------------------|
| **transcript-analyzer** | Transcript + prerequisite KB as interpretive lens | Cited facts with transcript locators |
| **mom-analyzer** | MoM text + optional KB + transcript notes for conflicts | Cited facts with MoM locators; **conflict list** (not resolved) |
| **transcript-story-extractor** | All of the above + SOW.json (notes only) + MSD catalog | Candidate backlog; traceability; **exclusion tables** |

**Also loaded before/during extract:**

- `artifacts/work-items/SOW.json` — align requirements to annexure topics; **no** Epic/Feature rows authored here
- `docs/intake/msd365-business-entity-scope-rulebook.yaml` + catalog JSON

**Working document:** `artifacts/intake/<date>-transcript-story-extraction.md` (template: `.cursor/templates/transcript-story-extraction-template.md`)

Sections include: cited facts (transcript), cited facts (MoM), MoM ↔ transcript conflicts, candidate backlog, traceability table, **Out of scope / excluded**, provenance, Open DQ, validation checklist.

---

### Phase 2 — Author rows and internal CSV

**Subagent:** `ado-user-story-csv-writer`

1. Persist **`artifacts/intake/<date>-user-story-rows.json`** — full row objects including metadata keys **not** exported as ADO columns:
   - `prerequisite_refs`, `transcript_*`, `mom_*`, `msd365_domain`, `msd365_application`, `msd365_business_entity`
2. Run canonical writer (never hand-built CSV):

```bash
python scripts/ado_user_story_csv.py write \
  --json artifacts/intake/<date>-user-story-rows.json \
  --out artifacts/intake/.pipeline/<date>-user-stories-working.csv
```

**Row order in working CSV:** Workshop → User Stories → Issue/Risk (no Epic/Feature in this phase).

**User Story narrative rules:**

- **Title 3:** short capability name  
- **Description:** `As a <role>, I need to <need>, so that <benefit>.`  
- **Acceptance Criteria:** one `- ` bullet per line in the cell  
- **ID:** blank on User Stories  
- No Priority / Story Points columns  

---

### Phase 3 — Scope validation (what gets rejected mechanically)

**Subagent:** `workshop-scope-compliance-validator`

#### 3a Workshop / prerequisite scope

```bash
python scripts/validate-user-story-workshop-scope.py \
  --json <user-story-rows.json> \
  --knowledge-base <workshop-prerequisite-knowledge-base.json> \
  --require-mom
```

**Checks (per User Story row):**

- Knowledge base has at least one `in_scope_objectives` or `in_scope_modules` entry  
- `prerequisite_refs` is a non-empty array  
- Every ref ID exists in allowed set (`OBJ-*`, `MOD-*` from KB—not `OOS-*`)  
- `transcript_locator` and `transcript_source_path` present  
- With `--require-mom`: `mom_locator` and `mom_source_path` present  

**Note:** Validator enforces **ID validity and field presence**, not deep semantic “does OBJ-002 really match this title?”—that remains agent quality + later `/evaluate-user-stories`.

#### 3b MSD365 business entity scope

```bash
python scripts/validate-user-story-business-entity-scope.py \
  --json <user-story-rows.json>
```

**Checks:**

- `msd365_domain`, `msd365_application`, `msd365_business_entity` present (via `story_scope_fields`)  
- Triple matches exactly one row in `catalog.entries`  
- Non-empty `business_entity` must appear in `catalog.business_entities`  

**FAIL on either script → Reflect** (fix rows or extraction notes, max 3 iterations).

---

### Phase 3b — CSV rulebook compliance

```bash
python scripts/validate-user-story-csv.py \
  --csv artifacts/intake/.pipeline/<date>-user-stories-working.csv \
  --report artifacts/intake/<date>-user-story-csv-validation.json
```

Headers, column order, work item types, and narrative patterns must match `user-story-csv-rulebook.yaml`. **Mapping must not run until this PASS.**

---

### Phase 4 — INVEST scorecard (separate file)

**Subagent:** `invest-scorecard-evaluator`

- Output: `artifacts/intake/<date>-invest-scorecard.csv` only  
- Not embedded in Excel  
- Gate guidance: no critical dimension below 5; overall ≥ 7 for Pass  

---

### Phase 5 — SOW feature mapping → public Excel

**Primary:** `work-item-mapping-agent` (orchestrator spawns **by explicit name** after CSV PASS)

```bash
python scripts/map-user-stories-to-sow-features.py \
  --csv <working.csv> \
  --rows-json <user-story-rows.json> \
  --work-items-dir artifacts/work-items \
  --out-xlsx artifacts/intake/<date>-user-stories-from-transcript.xlsx \
  --log-json artifacts/intake/.pipeline/<date>-work-item-mapping-log.json
```

**Public Excel hierarchy:** Workshop → **SOW Feature** (Title 2 = `<minutes> - <topic>`, blank Feature ID, Annexure ID1 = minutes) → User Stories under feature → unmatched stories + Issue/Risk at end. **No Epic rows.**

Matching is **generic** token overlap on titles/descriptions (+ optional `prerequisite_refs` → `WS-CE-*` hints). Thresholds: `.cursor/config.yaml` (`strong_threshold`, `winner_margin`, `max_related_features`).

Stories below threshold appear as **unmatched** in the mapping log—not deleted, but not grouped under a SOW Feature row.

---

## 5. Inclusion logic: when a User Story is created

A **User Story** candidate is **included** in `user-story-rows.json` only when the extractor applies **all** of the following:

| # | Criterion | Evidence on row / in MD |
|---|-----------|-------------------------|
| 1 | Transcript explicitly supports the capability | `transcript_locator`, `transcript_source_path` |
| 2 | MoM supports the same line of requirement | `mom_locator`, `mom_source_path` |
| 3 | Aligns with ≥1 in-scope objective or module | `prerequisite_refs` → `OBJ-*` or `MOD-*` |
| 4 | Does not contradict `out_of_scope` in KB | Excluded earlier if OOS |
| 5 | Maps to exactly one MSD catalog `entries` row | `msd365_*` triple |
| 6 | Implementable as ADO User Story per rulebook | Title 3, Description pattern, ≥1 AC bullet |
| 7 | Passes all validators | Workshop scope, entity scope, CSV |

**SOW alignment** is used for annexure topic consistency during extraction and for Excel grouping in Phase 5; it does not replace prerequisite scope.

---

## 6. Exclusion logic: how topics are ignored or dropped

Exclusion happens at **three layers**: agent decision, documentation, and validator rejection.

### 6.1 Agent-level exclusion (intended path)

| Reason | Action | Where recorded |
|--------|--------|----------------|
| Topic in transcript but **not** in prerequisite in-scope objectives/modules | **Do not** emit User Story | `## Out of scope / excluded` → **Prerequisite misalignment** |
| Contradicts prerequisite `out_of_scope` (e.g. `OOS-001`) | **Do not** emit User Story | Same table with reason ID |
| No matching MSD catalog `entries` row | **Do not** emit User Story | **MSD365 entity / catalog** subsection |
| Transcript discusses out-of-catalog D365 entity | Often **Issue/Risk**, not User Story | Per MSD entity rulebook `transcript_exception` |
| MoM ↔ transcript conflict on requirement | **Do not** silently pick a winner; may withhold story | **MoM ↔ transcript conflicts** + Open DQ |
| Transcript-only (no MoM support) | **Do not** emit User Story (with `--require-mom`) | Validator fails if row exists without mom fields |

**Example (Marketing WS-03):** Transcript mentioned lead assignment through opportunity closure; prerequisite `OOS-001` excludes deep lead-to-opportunity sales design → listed at locator `10:17–10:23`, **no** User Story row.

### 6.2 Validator-level rejection (if a bad row was written)

| Failure | Effect |
|---------|--------|
| Empty or invalid `prerequisite_refs` | `validate-user-story-workshop-scope.py` **FAIL** |
| Missing transcript or MoM locators | **FAIL** |
| Invalid `msd365_*` triple | `validate-user-story-business-entity-scope.py` **FAIL** |
| CSV shape/narrative violation | `validate-user-story-csv.py` **FAIL** |

Pipeline **Reflect:** remove or fix rows, update extraction MD, re-run writers and validators. Public Excel is not finalized until PASS.

### 6.3 Mapping-level partial exclusion

- Story remains in workbook but **unmatched** to any SOW Feature if score &lt; `strong_threshold` or margin rules fail  
- Logged in `*-work-item-mapping-log.json`  
- Not the same as prerequisite exclusion—story may still be a valid User Story under Workshop/unmatched section

### 6.4 What is **not** done

- Silently omitting discussed topics without a row in **Out of scope / excluded**  
- Inventing `prerequisite_refs` for out-of-scope topics (invalid IDs **FAIL** validation)  
- Expanding prerequisite KB during extraction to “fit” transcript topics  
- Using `epic.json` / `feature.json` for transcript mapping (SOW.json only per catalog rule 32)

---

## 7. Authority and conflict handling

```
Prerequisite KB  ──►  bounds WHAT may become a User Story
        │
        ▼
Transcript       ──►  supplies DETAIL (locators, AC ideas, roles)
        │
        ▼
MoM              ──►  confirms OFFICIAL alignment (agenda/decisions)
        │
        ▼
MSD catalog      ──►  tags D365 domain/app/entity (closed world)
        │
        ▼
SOW.json         ──►  groups stories under annexure Features in Excel
```

**MoM ↔ transcript conflicts:** listed in extraction MD as Open DQ; agents must **not** resolve conflicts into requirements without human review.

**Assumptions:** register `ASSUMPTION-*` in extraction notes; do not mark run Done with blocking assumptions unresolved.

---

## 8. Artifact map

| Artifact | Operator-facing? | Role |
|----------|------------------|------|
| `*-workshop-prerequisite-knowledge-base.{md,json}` | Internal | Scope authority |
| `*-transcript-story-extraction.md` | Internal | Extraction audit trail + exclusions |
| `*-user-story-rows.json` | Internal | Canonical rows + metadata |
| `.pipeline/*-user-stories-working.csv` | Internal | Validator input |
| `*-user-story-csv-validation.json` | Internal | CSV PASS/FAIL report |
| `*-invest-scorecard.csv` | **Yes** | INVEST only |
| `*-user-stories-from-transcript.xlsx` | **Yes** | Deliverable story pack |
| `.pipeline/*-work-item-mapping-log.json` | Internal | Matched vs unmatched |
| `artifacts/audit/*-generate-user-stories-from-transcript-*.md` | Internal | Command audit |

---

## 9. Orchestration and iteration policy

- **Entry:** `orchestrator-agent` routes `/generate-user-stories-from-transcript`  
- **Loop:** Plan → Act → Observe → Reflect (max **3** iterations)  
- **Iteration 1:** if validators PASS → INVEST → mapping → **stop** (no extra polish loops unless validation failed)  
- **BA agent** does not perform Phase 5 mapping; **work-item-mapping-agent** runs after CSV PASS only  

---

## 10. Downstream use

After successful completion:

- `/generate-test-cases-from-user-stories` — MSD E2E cases from the Excel  
- `/plan-governed-stories` or `/plan-sprint` — planning spine  

Related: `/generate-html-for-user-stories` — source traceability HTML (separate command; does not replace this pipeline).

---

## 11. Validation summary

| Gate | Script / agent | Blocks Excel? |
|------|----------------|---------------|
| Intake safety | `intake-safety-scan.py` | Yes (start) |
| Output paths | `output-path-gate.py` | Yes (writes) |
| Prerequisite + MoM refs | `validate-user-story-workshop-scope.py --require-mom` | Yes |
| MSD entity triple | `validate-user-story-business-entity-scope.py` | Yes |
| CSV rulebook | `validate-user-story-csv.py` | Yes (and blocks mapping) |
| INVEST | invest-scorecard-evaluator | Quality signal; Reflect if below gate |
| SOW map | `map-user-stories-to-sow-features.py` | Delivers grouped Excel; unmatched logged |

---

## 12. References

- Command: `.cursor/commands/generate-user-stories-from-transcript.md`  
- Skills: `user-story-from-transcript`, `workshop-prerequisite-analysis`, `work-item-mapping`, `intake-safety`  
- Rulebooks: `docs/intake/user-story-csv-rulebook.yaml`, `workshop-prerequisite-scope-rulebook.yaml`, `msd365-business-entity-scope-rulebook.yaml`  
- Config: `.cursor/config.yaml` (`workshop_prerequisite_scope`, `msd365_business_entity_scope`, `work_item_mapping`)  
- Example run: Marketing WS-03 artifacts under `artifacts/intake/2026-10-16-*` and `2026-10-13-marketing-ws03-*`
