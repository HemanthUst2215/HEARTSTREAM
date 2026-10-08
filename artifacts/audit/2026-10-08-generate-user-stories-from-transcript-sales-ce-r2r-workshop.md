# Audit: /generate-user-stories-from-transcript — Sales CE Record-to-Report Workshop

**Date:** 2026-10-08
**Command:** `/generate-user-stories-from-transcript`
**Primary:** business-analyst-agent (mode `transcript-ado-csv`)

## What
Converted the meeting transcript `01. Sales - CE Record to Report UST Led Workshop-20260928-en-US.docx` (located at workspace root) into an ADO-importable User Story CSV conforming to `docs/intake/user-story-csv-rulebook.yaml`.

## Why
Human requested `/generate-user-stories-from-transcript` with the workshop docx. No sprint plan or BRD input was supplied for this run — transcript is the sole intake source.

## How
1. Located the docx at workspace root (not previously tracked in `docs/intake` or `artifacts/intake`); confirmed via file-system search.
2. Ran `scripts/intake-safety-scan.py` on the raw docx — **CLEAN** (0 injection hits, 0 PII hits), exit 0.
3. Extracted verbatim text (1551 paragraphs) via `python-docx`, persisted to `artifacts/intake/2026-10-08-transcript.txt` (raw, untouched).
4. Loaded `docs/intake/user-story-csv-rulebook.yaml` (column order, taxonomy, title/AC/description formats).
5. Read the full transcript and authored extraction notes with timestamp locators: `artifacts/intake/2026-10-08-transcript-story-extraction.md` — 8 Epics, 14 Features, 23 User Stories, 1 Task, 2 Issues, 7 Open DQs, 4 parking-lot items (not converted to stories per facilitator's explicit deferral).
6. Authored row objects (never hand-built CSV text): `artifacts/intake/2026-10-08-user-story-rows.json`, ordered monotonically per ADO layout (Workshop → Epic → Feature → User Story → Task → Issue → Risk) with descriptions conforming to `^As an? <role>, I need to <need>, so that <benefit>` and Acceptance Criteria using ASCII `- ` bullets.
7. Wrote CSV via canonical writer: `python scripts/ado_user_story_csv.py write --json artifacts/intake/2026-10-08-user-story-rows.json --out artifacts/intake/2026-10-08-user-stories-from-transcript.csv` — wrote 57 rows, 0 critical findings.
8. Validated: `python scripts/validate-user-story-csv.py --csv ... --report artifacts/intake/2026-10-08-user-story-csv-validation.json` — **PASS**, 0 critical, 57 rows.

## Validation
- Intake-safety scan: CLEAN (exit 0)
- Writer script structural + content validation: 0 critical findings
- `validate-user-story-csv.py`: `status: PASS`, `critical: 0`, `row_count: 57`
- Headers match rulebook `column_order` exactly (enforced by writer)
- No hand-authored CSV text; all rows round-tripped through `ado_user_story_csv.py`

## Open Items (registered, not invented — see extraction notes for full detail)
- DQ-001: Partner self-registration of leads in Zinfi — adoption uncertain
- DQ-002: Direct customer (hospital/EMS/GPO) contract model — deferred to follow-up session (also captured as an Issue row)
- DQ-003: Exact install-base creation trigger per product type
- DQ-004: Owning CRM team for install-base location-change requests
- DQ-005: North America contracted direct-sales rep system access (Zenfi vs Dynamics) (also captured as an Issue row)
- DQ-006: Quoting-tool look-and-feel parity across Zenfi/Dynamics/E-store (parking lot — not converted to a story)
- DQ-007: Low-value item quote/order workflow without full opportunity (parking lot context; captured as a User Story acknowledging the gap)

## Follow-up fix (same day)
Excel rendered Acceptance Criteria bullets as `#NAME?` because cells beginning with `-` are parsed as formulas by Excel on CSV open (RFC4180 quoting does not prevent this — Excel re-applies formula detection to quoted cell content). Fixed generically at the writer level, not just for this file:
- Added `excel_safe_cell()` / `EXCEL_FORMULA_TRIGGER_CHARS` to `scripts/ado_user_story_csv_layout.py::write_csv()` — any cell starting with `=`, `+`, `-`, or `@` gets a single leading space prefix before write.
- The content stays fully readable (`" - Partner record..."` reads identically to `"- Partner record..."`), and `ac_bullet_lines()` strips whitespace before checking the `- ` prefix, so rulebook/validator compliance is unaffected.
- Regenerated `2026-10-08-user-stories-from-transcript.csv` via the same writer command; re-ran `validate-user-story-csv.py` — still **PASS**, 0 critical, 57 rows.
- Ran `scripts/test_ado_user_story_csv_layout.py` regression — OK.
- This fix is generic and applies to all future `/generate-user-stories-from-transcript` runs (and any other script using this shared layout module), not a one-off patch.

## Artifacts
- `artifacts/intake/2026-10-08-transcript.txt` (verbatim source, persisted pre-analysis)
- `artifacts/intake/2026-10-08-transcript-story-extraction.md`
- `artifacts/intake/2026-10-08-user-story-rows.json`
- `artifacts/intake/2026-10-08-user-stories-from-transcript.csv`
- `artifacts/intake/2026-10-08-user-story-csv-validation.json`

## Next command

✅ `/generate-user-stories-from-transcript` complete.
**Next command:** Human import of the CSV to ADO, then `/plan-governed-stories` or `/plan-sprint`. A BRD track (`/generate-brd`) may run in parallel from the same transcript if required.
