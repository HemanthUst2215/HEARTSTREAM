---
name: work-item-json-authoring
description: >-
  Author and explain HeartStream work-items.json structure. Use when transforming
  CSV exports, validating JSON, or summarizing work items for stakeholders.
---

# Work item JSON authoring

## When to use
- After `csv-to-work-items-json.py` runs
- When explaining output to users or extending the schema

## Phases
1. Load `.cursor/templates/work-items-output.schema.json`.
2. Prefer script output as source of truth; use LLM only for `work-items-summary.md`.
3. Map CSV columns:
   - `ID` → `workItemId`
   - `Title` → `title` (+ parsed `workItemCode` when pattern `WS-*` present)
   - `Work Item Type` → `workItemType`
   - `State` → `state`
   - `Description` → `description.plainText` and `description.summary` (first paragraph)
   - `Parent` → `parent.workItemId`
   - `Area Path` / `Iteration Path` → nested path objects
4. Validate with `json-output-validator` subagent.

## Inputs / outputs
- Input: CSV path (or multiple paths — one transform per file), optional filters
- Output: one JSON per CSV under `artifacts/work-items/` (default single file: `work-items.json`; e.g. `EPIC.csv` → `epic.json`, `Feature.csv` → `feature.json`)

## Provenance
Each `workItems[]` entry includes `source.rowNumber` and `source.id` from CSV.

## Must NOT
- Invent IDs, titles, or states not in CSV
- Drop rows without logging in validation report
