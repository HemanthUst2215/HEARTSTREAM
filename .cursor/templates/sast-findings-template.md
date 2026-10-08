# SAST Findings — {{SCOPE}}

> From `/sast-scan` (security-agent). Static analysis only — no exploit payloads. Operator-owned localhost/staging.

| Field | Value |
|-------|-------|
| **Scan ID** | SAST-{{YYYYMMDD}}-{{slug}} |
| **Date (UTC)** | {{timestamp}} |
| **Command** | `/sast-scan` |
| **Roots scanned** | `${modules.api}`, `${modules.ui}`, `${modules.infra}` |
| **Tool(s)** | semgrep / SpotBugs / PMD / CodeQL / ESLint-security / STATIC_REVIEW / NEEDS_TOOL |
| **Commit** | {{sha}} |
| **Agent** | security-agent |

## Summary

| Severity | Count | Fixed | Open | Waived |
|----------|-------|-------|------|--------|
| Critical | | | | |
| High | | | | |
| Medium | | | | |
| Low | | | | |

## Findings

| ID | Severity | OWASP / CWE | Path:line | Rule / check | Finding summary | Owner | Status | Fix ref |
|----|----------|-------------|-----------|--------------|-----------------|-------|--------|---------|
| SAST-1 | critical/high/medium/low | | | | | | open/fixed/waived | PR/issue |

## Unowned Critical / High

> Must be empty or have documented owner before release GO.

| ID | Finding | Assigned owner | Due |
|----|---------|----------------|-----|
| | | | |

## Waivers

| ID | Control | Waiver reason | Approver | Expiry |
|----|---------|---------------|----------|--------|
| | | | | |

## Tool execution log

| Tool | Command | Exit code | Report path |
|------|---------|-----------|-------------|
| | | | `artifacts/security/` |

## Redaction attestation

- Secrets/PII masked in this report: **yes / no**
- No credentials in scan config committed: **yes / no**

**Output path:** `artifacts/security/{{date}}-sast-findings.md`

**Next command:** `/review-changes` or remediate → re-scan
