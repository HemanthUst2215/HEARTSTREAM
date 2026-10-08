# Compliance Evidence — {{FRAMEWORK_OR_CONTROL_SET}}

> Evidence pack from `/compliance-check` (security-agent mode compliance). Do not mark compliant without cited production evidence locators.

| Field | Value |
|-------|-------|
| **Assessment ID** | COMP-{{YYYYMMDD}}-{{slug}} |
| **Date** | {{YYYY-MM-DD}} |
| **Scope** | {{system, release, environment}} |
| **Framework** | {{SOC2 control family, ISO 27001 annex, org policy id}} |
| **Assessor** | security-agent |
| **Overall status** | Compliant / Partial / Non-compliant / Needs evidence |

## Control matrix

| Control ID | Control statement | Requirement source | Evidence type | Evidence locator | Status | Gap / owner |
|------------|-------------------|--------------------|--------------|--------------------|--------|-------------|
| | | | config / log / policy / scan | path or URL (no secrets) | Met / Partial / Not met | |

## Evidence inventory

| Artifact | Path | Collected | Redaction applied |
|----------|------|-----------|-------------------|
| SAST report | `artifacts/security/` | | yes |
| Dependency scan | | | |
| Auth config | | | |
| Audit logging sample | | | |

## Findings

| ID | Severity | Control | Finding | Remediation | Target date |
|----|----------|---------|---------|-------------|-------------|
| | critical/high/medium/low | | | | |

## Sign-off

| Role | Name | Date | Decision |
|------|------|------|----------|
| Security owner | | | Accept / Remediate |

**Output path:** `docs/compliance/{{date}}-{{slug}}-evidence.md`
