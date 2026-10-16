---
name: user-story-source-traceability
description: >-
  Validate manual or AI-generated user stories against unified workshop sources
  (transcript, MoM, pre-read, SOW features). Use for /generate-html-for-user-stories.
  Two independent HTML reports; never compare manual with AI.
---

# User story source traceability

## When to use
- Command: `/generate-html-for-user-stories`
- Primary: **user-story-evaluation-agent** mode `source-traceability-html`
- After intake-safety exit 0 on all source paths and both CSVs

## Order
1. `python scripts/generate_user_story_source_analysis.py allocate-run --date <YYYY-MM-DD> [--slug <output_slug>] --json` — use returned paths. Never overwrite prior public HTML.
2. Output-path gate on allocated public HTML paths only.
3. `prepare-kb` with all `transcript_paths`, `mom_paths`, `preread_paths`, `sow_json` → `<kb_index>`.
4. **source-knowledge-base-unifier** reads `kb_index` and writes `<unified_kb>` with:
   - `requirements[]` — `{id, statement, source_type, source_path, source_locator, confidence}`
   - `features[]` — aligned to SOW rows (`feature_name`, `workshop_code`, locators)
   - `sources[]` — manifest of inputs
5. `prepare-stories --csv <manual_csv> --side manual --kb-index <kb_index> --unified-kb <unified_kb> --out <manual_packet>`
6. **user-story-source-traceability-analyzer** with `side: manual` → `<manual_analysis>` (full report JSON per template).
7. `validate --analysis <manual_analysis>` then `render` → `public_manual_html` + `public_manual_json`.
8. `prepare-stories --csv <generated_csv> --side generated ... --out <ai_packet>`
9. **user-story-source-traceability-analyzer** with `side: generated` → `<ai_analysis>`.
10. `validate` + `render` → `public_ai_html` + `public_ai_json`.

## Evaluation framework (same for both sides)
For each User Story row in the packet:
- **Source references first**: excerpt + locator per source; use `No Supporting Evidence Found` when absent
- **Match type (USHTML-MATCH-001):** `No Match` **only** if there is no supporting reference. If any real excerpt exists → `Partial Match` or `Exact Match` (Exact = full story substantiated by citations; otherwise Partial)
- **Derived sources**: subset of Transcript, MoM, Pre-read Materials, Feature List (non-empty when supporting references exist)
- **Feature mapping (USHTML-FEAT-001)**: `why_mapped_to_feature` cites SOW BPM topic, annexure/workshop code, and source excerpts/locators. CSV hierarchy may label `feature_name` only; row order is not a rationale
- **Coverage assessment**: Fully Supported | Partially Supported | Unsupported
- **Executive summary** and **overall_traceability_score** (0–100) derived from story-level coverage and match counts
- **Feature traceability matrix** (per annexure: mapped stories, coverage %, `requirements_not_in_stories[]` each with `why_not_converted`), **source coverage summary**, **coverage_gap_analysis** per template

## Subagents
| Subagent | Skill / role |
|----------|----------------|
| source-knowledge-base-unifier | Merge mechanical index into cited `unified_kb` |
| user-story-source-traceability-analyzer | One side only; writes analysis JSON |

## Rules the parent enforces
- Do not spawn story-matching-evaluator, coverage-analysis-evaluator, or kpi-aggregation-evaluator from `/evaluate-user-stories`.
- Do not load the other CSV while analyzing one side (except both CSVs appear in intake-safety and `prepare-kb` input manifest).
- Provenance: every non-trivial statement needs `source_path`, `source_locator`, `confidence`.
- Report status: **Draft — Pending Method Review** until `ASSUMPTION-USHTML-001` is accepted.

## Do not
- Hand-write HTML.
- Compare manual vs AI or emit a single combined report.
- Invent Feature titles or SOW rows not in `sow_json`.
- Treat either user-story CSV as ground truth.
