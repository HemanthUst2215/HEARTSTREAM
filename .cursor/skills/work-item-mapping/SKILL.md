---
name: work-item-mapping
description: >-
  Map generated user stories to SOW.json features (no epic.json / feature.json).
  Use during /generate-user-stories-from-transcript after CSV validation.
  Public output is one Excel; INVEST stays a separate CSV.
---

# Work item mapping (SOW features)

## When to use
- After `/generate-user-stories-from-transcript` working CSV validates PASS
- Primary: **work-item-mapping-agent**

## Catalog source (required)
- **Features:** `artifacts/work-items/SOW.json` only (`rows[]` with columns BPM, Workshop, Annexure ID per operator mapping)
- **Do not load** `epic.json` or `feature.json` for transcript user-story mapping when `work_item_mapping.feature_source` is `sow_json`.

## Workshop row
- **Annexure ID1** must stay **empty** (no annexure on Workshop).

## Feature row shape (public Excel)
| Column | Value |
|--------|--------|
| Work Item Type | Feature |
| Title 2 | `{Annexure ID} - {BPM}` e.g. `70 - External Analytics Data Ingestion & Unification` |
| Description | BPM session topic (same text without minutes prefix) |
| ID | blank |
| Annexure ID1 | Annexure ID minutes from SOW (e.g. `70`) |

## Phases
1. Confirm working CSV exists and validator PASS.
2. Load `SOW.json` before mapping.
3. Output-path gate on the **single** xlsx only.
4. Run:
   ```bash
   python scripts/map-user-stories-to-sow-features.py \
     --csv artifacts/intake/.pipeline/<date>-user-stories-working.csv \
     --rows-json artifacts/intake/<date>-user-story-rows.json \
     --work-items-dir artifacts/work-items \
     --out-xlsx artifacts/intake/<date>-user-stories-from-transcript.xlsx \
     --log-json artifacts/intake/.pipeline/<date>-work-item-mapping-log.json
   ```
5. Do **not** write mapped CSV or a second workbook.
6. Do **not** write INVEST into the Excel (`invest-scorecard.csv` is separate).

## Match policy
- Prefer `prerequisite_refs` on row JSON (`OBJ-001` → `WS-CE-01`) when `--rows-json` is supplied.
- Otherwise generic title/description similarity against SOW feature title and BPM topic.
- **Never** insert Epic rows.
- User Story `ID` stays blank; group under matched SOW Feature blocks in SOW.json order.

## Unmatched
Stories below threshold appear after all Feature blocks with blank ID. Log in mapping JSON.

## Reference
- Config: `.cursor/config.yaml` → `work_item_mapping`
- Rulebook: `docs/intake/user-story-csv-rulebook.yaml` → `generation.sow_feature_mapping`
