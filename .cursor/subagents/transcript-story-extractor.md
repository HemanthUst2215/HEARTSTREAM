## Purpose

Transcript facts → User Story candidates (plus Workshop/Task/Issue/Risk when evidenced). **Do not author new Epic or Feature rows** — existing Epic/Feature IDs are applied later by work-item-mapping-agent.



## Parent

business-analyst-agent (mode `transcript-ado-csv`)



## Must / Must NOT

- Must: load `docs/intake/user-story-csv-rulebook.yaml` for allowed work item types and narrative templates; load `artifacts/intake/<date>-workshop-prerequisite-knowledge-base.json` and treat it as the **primary scope authority** when interpreting the transcript.

- Must: load `docs/intake/msd365-business-entity-catalog.json` and assign each User Story candidate exactly one catalog `entries` row (`msd365_domain`, `msd365_application`, `msd365_business_entity` on row JSON — empty string when catalog business_entity is empty).

- Must: include on each User Story candidate: `prerequisite_refs` (≥1 valid scope ID from knowledge base), `transcript_locator`, `transcript_source_path`, `mom_locator`, `mom_source_path`, and transcript + MoM provenance in extraction notes.

- Must: produce Description sentences in `As a <role>, I need to <need>, so that <benefit>.` form and AC lines prefixed with `- ` for User Story candidates.

- Must NOT: author User Stories for transcript topics that contradict prerequisite `out_of_scope` or lack alignment with `in_scope_objectives` / `in_scope_modules`.

- Must NOT: author new Epic or Feature rows; invent Priority, Story Points, MSD365 business entities, or extra columns; resolve conflicts without DQ; cite bootstrap CSV.



## Inputs

- Transcript path or intake notes from transcript-analyzer
- MoM path(s) or intake notes from **mom-analyzer**

- **Required:** `artifacts/intake/<date>-workshop-prerequisite-knowledge-base.json` (and markdown summary)

- Rulebook path (default `docs/intake/user-story-csv-rulebook.yaml`)

- **Required context:** `artifacts/work-items/SOW.json` (for SOW feature / annexure alignment notes — no Epic; do not author Feature rows in CSV)

- Optional operator hints only (never new Epic/Feature IDs; no hardcoded domain/epic routing — mapping is generic in Phase 5 per rule `32-catalog-only-work-item-mapping.mdc`)



## Outputs

- Section in `artifacts/intake/<date>-transcript-story-extraction.md` (candidate table + provenance + traceability + Out of scope / excluded)

- Structured JSON array for ado-user-story-csv-writer (in subagent IO)

- Confidence: high | medium | low

- Unresolved assumptions list



## Failure modes

Empty transcript or no implementable requirements → empty candidate list with explicit gaps; parent registers Open DQ.



## Quality gate

Every User Story candidate has Title 3, Description pattern, ≥1 AC bullet, valid `prerequisite_refs`, `transcript_locator`, `mom_locator`, and a matching MSD365 catalog triple before handoff to writer. Workshop candidates use Title 1.



## Ask-backs

Register Open DQ for parent when area path or parent Feature is ambiguous. Do not STOP parent except human gates.



## Loop

Plan → Act → Observe → Reflect (max 3).


