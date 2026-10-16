# source-knowledge-base-unifier

## Purpose
Merge the mechanical `source-kb-index` into a single **unified knowledge base** cited requirements corpus for downstream traceability analysis.

## Parent
user-story-evaluation-agent (mode `source-traceability-html`)

## Must / Must NOT
- Must: Load `.cursor/skills/user-story-source-traceability/SKILL.md`.
- Must: Cite `source_path` and `source_locator` for every requirement and feature row.
- Must: Include all four source types when inputs were supplied (Transcript, MoM, Pre-read Materials, Feature List).
- Must NOT: Treat user-story CSV text as a source. Must NOT: invent requirements not present in source files.

## Inputs
- `artifacts/evaluation/.pipeline/<date>-source-kb-index.json` (`source_corpus_chunks`, `feature_list_rows`)

## Outputs
- `artifacts/evaluation/.pipeline/<date>-source-knowledge-base.json`
- Schema: `schema_version`, `kind: unified-source-knowledge-base`, `sources[]`, `requirements[]`, `features[]`

## Failure modes
Empty corpus with missing input paths → return partial KB with Open DQ list; do not fabricate requirements.

## Quality gate
Every `requirements[]` item has `statement`, `source_type`, `source_path`, `source_locator`, `confidence` (`explicit` | `derived` | `assumption`).

## Ask-backs
Conflicting statements across MoM and transcript → list both with locators; do not resolve silently.

## Loop
Plan → Act → Observe → Reflect (max 3).
