# Techno-Functional Story Pack — Sprint {{N}}

> Optional pack template. Public story command is `/generate-user-stories-from-transcript` (ADO CSV). Do not treat this pack as a required deliverable of that command.

| Field | Value |
|-------|-------|
| **Sprint** | {{N}} |
| **Pack ID** | {{slice-slug}} |
| **Sources** | {{business_rule_sources — paths}} |
| **Generated** | {{YYYY-MM-DD}} |
| **Agent** | business-analyst-agent |
| **Validation** | invest-validator: pass/fail |

## Sprint summary

- **Objective:**
- **Stories in pack:**

## Dependencies

| Dependency | Type | Status | Blocker for |
|------------|------|--------|-------------|
| | API / Figma / DDL | ready/TBD | SP- |

## Gaps (DDL / API / UI / Wiring)

> TBD values **only** here — not silent invention.

| Dimension | Gap | DQ ID | Owner |
|-----------|-----|-------|-------|
| DDL | | DQ- | data-agent path |
| API | | | api-agent |
| UI | | | frontend-agent |
| Wiring | | | frontend-agent |

---

## Story {{SP-ID}} — {{Title}}

### User story

As a **{{role}}**, I want **{{capability}}**, so that **{{benefit}}**.

### Gherkin

See `gherkin-story-template.md` — scenarios with @AC tags.

### INVEST scorecard

| Criterion | Pass | Notes |
|-----------|------|-------|
| Independent | | |
| Negotiable | | |
| Valuable | | |
| Estimable | | |
| Small | | |
| Testable | | |

### Rule provenance

| behavior_id | statement | source_path | source_locator | confidence |
|-------------|-----------|-------------|----------------|------------|
| BEH- | | | | explicit/derived/assumption |

### Acceptance criteria

| AC ID | Criterion | Testable |
|-------|-----------|----------|
| AC-01 | | yes |

### DDL hints (cited or gap)

| Entity | Columns / constraints | Source or DQ |
|--------|----------------------|--------------|
| | | |

### API surface

| operationId | Method | Path | Purpose | Auth |
|-------------|--------|------|---------|------|
| | | | | |

### UI data workflow

| Screen | Fields | Actions | API calls |
|--------|--------|---------|-----------|
| | | | |

### Data tables (UI ↔ API ↔ persistence)

| UI field | API field | DB column | Transform |
|----------|-----------|-----------|-----------|
| | | | |

### Wiring sequence preview

1. 
2. 

---

**Output path:** `docs/sprint{{N}}/userstory/{{slice}}-techno-functional-pack.md`

**Next command:** `/plan-governed-stories`
