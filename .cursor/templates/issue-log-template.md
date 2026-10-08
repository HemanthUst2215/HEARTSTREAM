# Issue Log — {{TITLE}}

| Field | Value |
|-------|-------|
| **ID** | ISS-{{YYYYMMDD}}-{{slug}} |
| **Reported** | {{YYYY-MM-DD}} |
| **Severity** | Critical / High / Medium / Low |
| **Classification** | backend / frontend / full-stack / config-env |
| **Classification rationale** | {{1–3 sentences — signals from /fix-issue Phase 0}} |
| **Agent(s)** | backend-agent / frontend-agent (mode fix) |
| **Status** | Triage / Plan pending / Approved / In progress / Fixed / Verified / Cancelled |

## Issue description

- **Summary:**
- **Steps to reproduce:**
- **Expected:**
- **Actual:**
- **Environment:** (local / branch / browser / JDK / DB)

## Root cause analysis

- **Where:** (file paths, layer — controller / service / UI component / config)
- **Why:** (mechanism — not symptom only)
- **BRD / contract reference:** (FR-xxx, OpenAPI operation, or DQ-xxx if silent)

## Impact analysis

| Layer | Affected | Risk |
|-------|----------|------|
| API / OpenAPI | | |
| Database / migrations | | |
| UI / routes | | |
| Tests | | |
| Security / auth | | |

## Fix plan (pre-implementation)

1. 
2. 

**Approach:** Production-grade fix — reuse existing patterns; no workarounds.

**Human approval:** {{date}} — {{proceed | revise | cancelled}}  
**Approver note:**

## Implementation

- **Files changed:**
- **Design choices:** (what was reused vs extended)

## Test evidence

| Suite | Command | Result | Notes |
|-------|---------|--------|-------|
| Unit (new/changed) | | pass / fail | |
| API regression | | | |
| UI regression | | | |
| E2E | | | |
| Coverage | | | |

**Evidence files:** `artifacts/test-results-{{date}}.md`, `artifacts/e2e-test-results-*.md`

## Outcome

- **Fixed:** yes / no / partial
- **Regression risk:** low / medium / high
- **Open items / follow-ups:**
- **Recommended next command:** `/review-changes` | `/pr-assist` | `/plan-sprint`

**Output path:** `artifacts/issues/{{YYYY-MM-DD}}-{{slug}}.md`
