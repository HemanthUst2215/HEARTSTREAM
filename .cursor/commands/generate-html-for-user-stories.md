# /generate-html-for-user-stories

## Objective
Validate **manual** and **AI-generated** user-story CSVs independently against the original workshop source inputs (transcript, MoM, pre-read materials, SOW feature list). Publish **two separate HTML reports**. Do **not** compare manual with AI.

## Orchestration
| Phase | Role | Agent / Subagent |
|-------|------|------------------|
| 0 Safety | Gate | intake-safety on every source path and both CSVs |
| 1 Allocate | Script | `scripts/generate_user_story_source_analysis.py allocate-run` |
| 2 Index sources | Script | `prepare-kb` → mechanical `kb_index` |
| 3 Unify KB | Subagent | source-knowledge-base-unifier → `unified_kb` |
| 4 Packet manual | Script | `prepare-stories --side manual` |
| 5 Analyze manual | Subagent | user-story-source-traceability-analyzer (`side: manual`) |
| 6 Render manual | Script | `validate` + `render` → manual HTML/JSON |
| 7 Packet AI | Script | `prepare-stories --side generated` |
| 8 Analyze AI | Subagent | user-story-source-traceability-analyzer (`side: generated`) |
| 9 Render AI | Script | `validate` + `render` → AI HTML/JSON |

Phases 5 and 8 are **independent**. Phase 8 must not read the manual analysis JSON except for shared `unified_kb`. Never spawn story-matching-evaluator or coverage metrics that pair manual with generated.

## Use Agents
| Order | Agent | Spec | When |
|-------|-------|------|------|
| Route | orchestrator-agent | `.cursor/agents/orchestrator-agent.md` | Always |
| 1 | **user-story-evaluation-agent** | `.cursor/agents/user-story-evaluation-agent.md` | Mode `source-traceability-html` after intake-safety exit 0 |

## Runtime Inputs

### Required
- `manual_csv` — manually created user stories (rulebook columns)
- `generated_csv` — AI-generated user stories (rulebook columns)
- `transcript_paths` — one or more transcript files (`.txt` / extracted text)
- `mom_paths` — meeting minutes (normalized `.txt` / `.md`; extract `.docx` via `scripts/extract-docx-text.py` first)
- `preread_paths` — pre-read / workshop materials (`.txt` / `.md` / extracted text)
- `sow_json` — feature list (`artifacts/work-items/SOW.json` by default)

### Optional
- `output_slug` (filename suffix)
- Existing `unified_knowledge_base` path (skip Phase 3 only when operator confirms KB is current for this corpus)

## Enforce Rules
`.cursor/rules/00-global-governance.mdc`, `01-project-context.mdc`, `02-security-and-compliance.mdc`, `09-agent-orchestration.mdc`, `10-audit-trail.mdc`, `22-behavior-provenance-and-anti-invention.mdc`, `31-untrusted-intake.mdc`, `32-catalog-only-work-item-mapping.mdc` (feature names from SOW rows only — do not invent features)

## Intake safety gate
Scan **all** transcript, MoM, pre-read, and both CSV paths. Load `.cursor/skills/intake-safety/SKILL.md`. Run `python scripts/intake-safety-scan.py` on the full path list **before** spawning user-story-evaluation-agent. Exit 2 → STOP. Exit 1 → STOP until redaction or waiver. Exit 0 → continue.

## Use Templates
`user-story-source-analysis-contract.yaml`, `user-story-source-analysis-report-template.md`, `subagent-io-template.md`, `audit-trail-template.md`

Rulebook (column contract): `docs/intake/user-story-csv-rulebook.yaml`

## Use Skills
`.cursor/skills/intake-safety/SKILL.md`, `.cursor/skills/user-story-source-traceability/SKILL.md`

## Execution Policy
Plan → Act → Observe → Reflect (max 3). Iteration 1 Observe pass (`validate` exit 0 and both HTML files written) → stop.

## Command-Specific Hardening
- **New run only (mandatory):** allocate a fresh path set every invocation:
  ```bash
  python scripts/generate_user_story_source_analysis.py allocate-run --date <YYYY-MM-DD> [--slug <output_slug>] --json
  ```
  Use every path in the JSON. Do **not** overwrite prior `*-manual-user-story-analysis*.html` or `*-ai-user-story-analysis*.html`.
- **Output-path check gate:** after `allocate-run`, run `python scripts/output-path-gate.py --check` on allocated public HTML paths only.
- Ground truth is the **unified knowledge base** built from listed sources only — not either CSV.
- **Forbidden:** manual vs AI matching, Granularity, Recall, Precision, side-by-side winner tables, or reading one CSV to score the other.
- **Feature name** on each story may reflect the workbook hierarchy (for display). **why_mapped_to_feature** must follow **USHTML-FEAT-001**: cite SOW BPM topic / annexure and workshop source locators that justify the mapping — never "preceding Feature row in CSV" as the reason.
- **Match type vs source references (USHTML-MATCH-001):** `No Match` only when there is **no** supporting reference (`source_references` empty or every excerpt is `No Supporting Evidence Found`). If at least one supporting reference exists → **Partial Match** or **Exact Match** (Exact when cited spans fully substantiate the story; otherwise Partial). Do not assign `No Match` while listing real excerpts.
- **Feature traceability matrix:** under each SOW topic, list `requirements_not_in_stories[]` with `why_not_converted` for workshop requirements not represented in this CSV (source locators required).
- **Canonical render:** `python scripts/generate_user_story_source_analysis.py render` twice (manual + AI). Agents must not hand-write HTML.
- Report status stays **Draft — Pending Method Review** while `ASSUMPTION-USHTML-001` is pending.

## Per-story fields (both reports)
User Story ID, Title, Feature Name, Match Type (Exact / Partial / No Match — USHTML-MATCH-001), Derived Source(s), Source References (excerpts or `No Supporting Evidence Found`), why generated (detailed narrative in JSON; **shown in HTML for AI-generated report only**), why mapped to feature (JSON always; **HTML for AI-generated report only** — omitted from manual HTML), supporting business context, coverage assessment, confidence score, recommended action.

## Clarification Protocol
Register Open DQ for missing required paths or non-rulebook CSVs. Do not invent stories, features, or scores. Refuse when a Required input is absent.

## Artifact Persistence
Paths from `allocate-run` (versioned when a prior run exists the same day).

**Public (operator):**
- `artifacts/evaluation/<date>-manual-user-story-analysis[-<slug>][-vN].html`
- `artifacts/evaluation/<date>-manual-user-story-analysis[-<slug>][-vN].json`
- `artifacts/evaluation/<date>-ai-user-story-analysis[-<slug>][-vN].html`
- `artifacts/evaluation/<date>-ai-user-story-analysis[-<slug>][-vN].json`

**Internal:**
- `artifacts/evaluation/.pipeline/<date>-source-kb-index[-vN].json`
- `artifacts/evaluation/.pipeline/<date>-source-knowledge-base[-vN].json`
- `artifacts/evaluation/.pipeline/<date>-source-manual-packet[-vN].json`
- `artifacts/evaluation/.pipeline/<date>-source-ai-packet[-vN].json`
- `artifacts/evaluation/.pipeline/<date>-source-manual-analysis[-vN].json`
- `artifacts/evaluation/.pipeline/<date>-source-ai-analysis[-vN].json`
- `artifacts/audit/<date>-generate-html-for-user-stories[-<slug>][-vN].md`

## Definition of Done
- [ ] `allocate-run` used; prior HTML not overwritten
- [ ] Output-path gate CLEAR on allocated public HTML paths
- [ ] Intake-safety exit 0 on all sources and both CSVs (or exit 1 with waiver)
- [ ] `prepare-kb` written; `unified_kb` written by source-knowledge-base-unifier
- [ ] Manual and AI analysis JSON each pass `validate`
- [ ] Both HTML files written only by `render`
- [ ] No manual-vs-AI comparison artifacts
- [ ] Status Draft — Pending Method Review while `ASSUMPTION-USHTML-001` pending
- [ ] Audit written
- [ ] Not a harness phase change

## Next command

> ✅ `/generate-html-for-user-stories` complete.
> **Next command:** Review `artifacts/evaluation/<date>-manual-user-story-analysis.html` and `artifacts/evaluation/<date>-ai-user-story-analysis.html`. Accept or reject `ASSUMPTION-USHTML-001` before treating traceability scores as accepted.
