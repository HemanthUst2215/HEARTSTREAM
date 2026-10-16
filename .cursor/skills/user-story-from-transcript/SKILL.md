---
name: user-story-from-transcript
description: Transcript + MoM → ADO user story CSV using the stored rulebook. Use for /generate-user-stories-from-transcript. Never read bootstrap setup CSV at runtime. Requires workshop prerequisite knowledge base, MoM paths, and MSD365 entity catalog.
---

# User stories from transcript (ADO CSV)

## Preconditions

1. **Rulebook exists:** `docs/intake/user-story-csv-rulebook.yaml` (status Active). Honor `runtime_contract` — no bootstrap exports or hardcoded workshop examples at runtime.
2. If missing, run **one-time bootstrap** only: business-analyst-agent mode `rulebook-bootstrap` + `user-story-csv-rulebook-author` with `setup_csv`. Persist rulebook; do not retain setup CSV as a runtime dependency.
3. **Prerequisite scope:** `prerequisite_paths` supplied; load `.cursor/skills/workshop-prerequisite-analysis/SKILL.md` and complete Phase P before extraction.
4. **MoM:** `mom_paths` supplied; normalize `.docx` via `scripts/extract-docx-text.py` before **mom-analyzer**.
5. **Intake safety** on prerequisites + MoM + transcript: `python3 scripts/intake-safety-scan.py <prereq...> <mom...> <transcript>` — STOP on 2; redact/waive on 1.

## Runtime workflow

1. **Load rulebook** — column order, work item types, narrative formats, required fields. No other schema source.
2. **Prerequisite knowledge base** — `docs/intake/workshop-prerequisite-scope-rulebook.yaml` + `artifacts/intake/<date>-workshop-prerequisite-knowledge-base.json` (primary scope authority).
3. **Load MSD365 business entity scope** — `docs/intake/msd365-business-entity-scope-rulebook.yaml` and `docs/intake/msd365-business-entity-catalog.json` only (never read `Area Paths.xlsx` at runtime). Author **only** User Stories whose capability maps to one catalog `entries` row. Leave `msd365_business_entity` empty when the matched row has empty Column 4. Do not use any Dynamics 365 business entity not listed in `catalog.business_entities`.
4. **Load SOW features** — `artifacts/work-items/SOW.json` before story authoring (align stories to annexure topics; do not load `epic.json` / `feature.json` for mapping).
5. **transcript-analyzer** — cited facts, quotes, conflicts; interpret using prerequisite terminology (do not resolve conflicts into requirements).
7. **mom-analyzer** — cited MoM facts, decisions, agenda topics; list MoM ↔ transcript conflicts without resolving them.
8. **transcript-story-extractor** — User Story candidates **only** when transcript + MoM + prerequisite scope align; set `prerequisite_refs`, `transcript_locator`, `transcript_source_path`, `mom_locator`, `mom_source_path`, and `msd365_*` on each User Story; exclude out-of-scope topics (document in extraction notes).
9. **ado-user-story-csv-writer** — persist row JSON → `python scripts/ado_user_story_csv.py write` to the **internal** working CSV.
10. **workshop-scope-compliance-validator** — `validate-user-story-workshop-scope.py --require-mom` + MSD365 entity validators; reject FAIL.
11. **user-story-csv-compliance-validator** — `scripts/validate-user-story-csv.py`; parent rejects FAIL.
12. **invest-scorecard-evaluator** — write **only** `artifacts/intake/<date>-invest-scorecard.csv`.
13. **work-item-mapping-agent** (after PASS) — match to `SOW.json`; public Excel Workshop → SOW Feature → User Stories (Feature Title 2 / Annexure ID1 per rulebook; no Epic).

## Output paths

| Artifact | Path |
|----------|------|
| Prerequisite KB | `artifacts/intake/<YYYY-MM-DD>-workshop-prerequisite-knowledge-base.md` + `.json` |
| Extraction notes | `artifacts/intake/<YYYY-MM-DD>-transcript-story-extraction.md` |
| Working CSV (internal) | `artifacts/intake/.pipeline/<YYYY-MM-DD>-user-stories-working.csv` |
| Validation JSON | `artifacts/intake/<YYYY-MM-DD>-user-story-csv-validation.json` |
| INVEST scorecard (separate) | `artifacts/intake/<YYYY-MM-DD>-invest-scorecard.csv` |
| Public Excel (only workbook) | `artifacts/intake/<YYYY-MM-DD>-user-stories-from-transcript.xlsx` |

## CSV / Excel row rules (summary)

- **Columns:** `State`, `ID`, `Work Item Type`, `Title 1`, `Title 2`, `Title 3`, `Assigned To` (hidden on the public Excel), `Area Path`, `Description`, `Acceptance Criteria`, `Annexure ID1`, `Fit Gap Status`, `User Story Type`. No legacy single `Title` header.
- **Title split:** Workshop / Epic → `Title 1`; Feature → `Title 2`; User Story / Test Case / Task / Issue / Risk → `Title 3`. Leave the other title cells empty.
- **Row order:** Workshop → User Stories → Issue/Risk. Epic/Feature IDs come from existing work-items JSON (mapping phase).
- **Work Item Type** for implementable needs: `User Story`.
- **Title 3:** short capability name (no `As a user` prefix).
- **Description:** `As a <role>, I need to <need>, so that <benefit>.` (User Story only).
- **Acceptance Criteria:** one ASCII `- ` (hyphen + space) criterion per line inside the cell; leave empty for Issue/Risk. Inbound Excel may use numbered lists; generated output still uses `- `.
- **Area Path:** populate on Workshop / Feature / Issue when known; optional on User Story when the transcript or mapped Feature assigns an area.
- **ID:** blank on User Story rows (working CSV and public Excel). Epic/Feature rows use catalog IDs; stories sit directly under their Feature.
- **State:** default `In Review` on Workshop, `New` on other types unless the source states a value. **Assigned To** and **User Story Type** stay blank unless the current source names them.
- **Priority / Story Points:** do not add columns (not in rulebook).

## Provenance

Each story in extraction notes: `behavior_id`, statement, `source_path` (transcript and/or MoM), `source_locator` (timestamp/line or MoM section), `confidence`, `prerequisite_refs`, MSD365 triple.

Silent requirements → register `ASSUMPTION-xxx` in extraction notes; do not mark Done with pending assumptions.

## Do not

- Read workshop bootstrap CSV when rulebook is present.
- Emit techno-functional packs or BRD sections from this skill.
- Self-approve ADO import or plan Approved.
- Author stories from transcript-only topics outside prerequisite scope.
