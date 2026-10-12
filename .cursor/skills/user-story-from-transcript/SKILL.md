---
name: user-story-from-transcript
description: Transcript → ADO user story CSV using the stored rulebook. Use for /generate-user-stories-from-transcript. Never read bootstrap setup CSV at runtime.
---

# User stories from transcript (ADO CSV)

## Preconditions

1. **Rulebook exists:** `docs/intake/user-story-csv-rulebook.yaml` (status Active).
2. If missing, run **one-time bootstrap** only: business-analyst-agent mode `rulebook-bootstrap` + `user-story-csv-rulebook-author` with `setup_csv`. Persist rulebook; do not retain setup CSV as a runtime dependency.
3. **Intake safety** on transcript: `python3 scripts/intake-safety-scan.py <transcript>` — STOP on 2; redact/waive on 1.

## Runtime workflow

1. **Load rulebook** — column order, work item types, narrative formats, required fields. No other schema source.
2. **transcript-analyzer** — cited facts, quotes, conflicts (do not resolve conflicts into requirements).
3. **transcript-story-extractor** — candidate User Stories (and Workshop/Task/Issue/Risk when evidenced). Do **not** create new Epic or Feature rows.
4. **ado-user-story-csv-writer** — row JSON → `python scripts/ado_user_story_csv.py write` to the **internal** working CSV (canonical; see rulebook `validation.mandatory_flow`).
5. **user-story-csv-compliance-validator** — run `scripts/validate-user-story-csv.py`; parent rejects FAIL (layout + field rules).
6. **invest-scorecard-evaluator** — write **only** `artifacts/intake/<date>-invest-scorecard.csv`. Do not add INVEST columns to the working CSV or the public Excel.
7. **Identify Feature, then story.** Match the transcript to an existing Feature before writing the User Story. **work-item-mapping-agent** (after PASS) writes one public Excel. A matched User Story `ID` is that Feature's workItemId.

## Output paths

| Artifact | Path |
|----------|------|
| Extraction notes | `artifacts/intake/<YYYY-MM-DD>-transcript-story-extraction.md` |
| Working CSV (internal) | `artifacts/intake/.pipeline/<YYYY-MM-DD>-user-stories-working.csv` |
| Validation JSON | `artifacts/intake/<YYYY-MM-DD>-user-story-csv-validation.json` |
| INVEST scorecard (separate) | `artifacts/intake/<YYYY-MM-DD>-invest-scorecard.csv` |
| Public Excel (only workbook) | `artifacts/intake/<YYYY-MM-DD>-user-stories-from-transcript.xlsx` |

## CSV row rules (summary)

- **Row order:** Workshop → User Stories → Issue/Risk. Epic/Feature IDs come from existing work-items JSON (mapping phase).
- **Work Item Type** for implementable needs: `User Story`.
- **Title:** short capability name (no `As a user` prefix).
- **Description:** `As a <role>, I need to <need>, so that <benefit>.` (User Story only).
- **Acceptance Criteria:** one ASCII `- ` (hyphen + space) criterion per line inside the cell; leave empty for Issue/Risk.
- **Area Path:** on Workshop/Feature/Issue; usually **blank** on User Story rows (ADO export convention).
- **ID:** blank on the working CSV. On the public Excel, every User Story `ID` is a catalog Feature workItemId. Leave it blank only when no catalog Feature title relates.
- **Priority / Story Points:** do not add columns (not in rulebook).

## Provenance

Each story in extraction notes: `behavior_id`, statement, `source_path` (transcript), `source_locator` (timestamp/line), `confidence`.

Silent requirements → register `ASSUMPTION-xxx` in extraction notes; do not mark Done with pending assumptions.

## Do not

- Read workshop bootstrap CSV when rulebook is present.
- Emit techno-functional packs or BRD sections from this skill.
- Self-approve ADO import or plan Approved.
