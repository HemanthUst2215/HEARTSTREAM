---
name: work-item-mapping
description: >-
  Map generated user stories to Epic/Feature/Workshop IDs from artifacts/work-items
  JSON using strong-match scoring only. Use during /generate-user-stories-from-transcript
  after CSV validation. Public output is one Excel; INVEST stays a separate CSV.
---

# Work item mapping

## When to use
- After `/generate-user-stories-from-transcript` working CSV validates PASS
- Primary: **work-item-mapping-agent**

## Catalog sources (required)
- **Epics:** `artifacts/work-items/epic.json` only
- **Features:** `artifacts/work-items/feature.json` only
- **Workshop IDs (optional):** `artifacts/work-items/work-items.json` for Workshop row `ID` only — never treat Workshop rows as Features

Paths and scoring are configurable via `.cursor/config.yaml` → `work_item_mapping` (no hardcoded domains — enforced by rule `32-catalog-only-work-item-mapping.mdc`, always on).

## Phases
1. Confirm working CSV exists and validator PASS.
2. Load `epic.json` and `feature.json` before mapping.
3. Output-path gate on the **single** xlsx only.
4. Run:
   ```bash
   python scripts/map-user-stories-to-work-items.py \
     --csv artifacts/intake/.pipeline/<date>-user-stories-working.csv \
     --work-items-dir artifacts/work-items \
     --out-xlsx artifacts/intake/<date>-user-stories-from-transcript.xlsx \
     --log-json artifacts/intake/.pipeline/<date>-work-item-mapping-log.json
   ```
5. Do **not** write mapped CSV or a second workbook.
6. Do **not** write INVEST into the Excel (`invest-scorecard.csv` is separate).

## Strong-match policy (generic)
- **Never** create, suggest, or inject new Epic/Feature rows or IDs.
- Score each User Story against **existing** Feature title + description in `feature.json`; parent Epic must exist in `epic.json`.
- Use generic token/title similarity only (no hardcoded domain phrases, epic IDs, or topic hint tables).
- Optional workshop alignment: when the CSV has a Workshop row, require minimum token overlap between workshop text and Feature+Epic text (`workshop_context_min_overlap` in config; `0` = off).
- Up to `max_related_features` (default 3) Features within `winner_margin` of the top score → one User Story row per Feature `ID` (same narrative).
- Excel layout (reference: `artifacts/intake/2026-10-08-user-stories-from-transcript-v2.xlsx`): Workshop → matched catalog **Epic** rows → matched catalog **Feature** rows → User Stories (`ID` = Feature workItemId). Traceability: Epic ID and Feature ID come from catalog JSON only (rulebook `ID` column; no extra EPIC ID / FEATURE ID columns).
- Leave User Story `ID` blank only when no catalog Feature clears the threshold.

## Must NOT
- Promote Workshop items into the Feature catalog
- Edit story narrative fields
- Emit extra Excel/CSV twins of the stories
- Invent IDs

## Definition of Done
- One Excel written; mapping log lists each source User Story as matched or unmatched
- No new hierarchy items outside `epic.json` / `feature.json`
