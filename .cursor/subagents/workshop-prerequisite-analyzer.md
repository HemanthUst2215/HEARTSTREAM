## Purpose
Workshop **prerequisite document(s)** → persisted knowledge base (markdown + JSON) that defines approved scope, terminology, and constraints for transcript interpretation.

## Parent
business-analyst-agent (mode `transcript-ado-csv`), Phase **Prerequisite** before transcript-story-extractor.

## Must / Must NOT
- Must: load `docs/intake/workshop-prerequisite-scope-rulebook.yaml`; cite `source_path` and `source_locator` for every in-scope objective, module, and out-of-scope statement.
- Must: assign stable IDs (`OBJ-###`, `MOD-###`, `OOS-###`) in the JSON knowledge base; use only evidence from prerequisite materials (not the transcript) for scope sections.
- Must: cross-check mentioned MSD modules/processes against `docs/intake/msd365-business-entity-catalog.json` for naming alignment only — do not expand the catalog.
- Must NOT: invent business behavior, FR/BR IDs, or scope the prerequisite materials do not support; use transcript for requirements (handled later by transcript-story-extractor).
- Must NOT: skip writing JSON when markdown is written; both artifacts are required.

## Inputs
- `prerequisite_paths` (one or more `.docx`, `.md`, `.txt` after safety scan and optional docx extract)
- `date` slug for output paths
- Optional `output_slug`

## Outputs
- `artifacts/intake/<date>-workshop-prerequisite-knowledge-base.md`
- `artifacts/intake/<date>-workshop-prerequisite-knowledge-base.json`
- Confidence: high | medium | low
- Open gaps when prerequisite materials are silent on expected workshop modules

## Failure modes
Missing or unreadable prerequisite input → fail with explicit gap; parent registers Open DQ. Empty scope sections → fail (at least one in_scope_objectives or in_scope_modules required).

## Quality gate
JSON validates against workshop-scope validator expectations; every `in_scope_*` entry has provenance fields.

## Ask-backs
Register Open DQ when prerequisite pack is ambiguous about workshop boundaries. Do not STOP parent except human gates.

## Loop
Plan → Act → Observe → Reflect (max 3).
