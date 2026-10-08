# DAST Findings — {{TARGET}}

> From `/dast-scan` (security-agent). **This product localhost/staging only** — never third-party production. No exploit payloads attached.

| Field | Value |
|-------|-------|
| **Scan ID** | DAST-{{YYYYMMDD}}-{{slug}} |
| **Date (UTC)** | {{timestamp}} |
| **Command** | `/dast-scan` |
| **Target URL** | {{url — no secrets in query strings logged}} |
| **Tool** | OWASP ZAP / header-auth-check / NEEDS_RUNTIME |
| **Operator confirmed ownership** | **yes / no** (required) |
| **Agent** | security-agent |

## Summary

| Severity | Count | Open | Remediated |
|----------|-------|------|------------|
| Critical | | | |
| High | | | |
| Medium | | | |
| Low | | | |

## Findings

| ID | Severity | OWASP category | Endpoint | Evidence (redacted) | Finding | Owner | Status |
|----|----------|----------------|----------|---------------------|---------|-------|--------|
| DAST-1 | | | | screenshot/header snippet | | | open/fixed |

## Auth coverage

| Route class | Probed unauthenticated | Probed invalid token | Expected deny | Actual |
|-------------|------------------------|----------------------|---------------|--------|
| Protected API | | | 401/403 | |
| Public health | | | 200 | |

## Unowned Critical / High

| ID | Finding | Owner | Due |
|----|---------|-------|-----|
| | | | |

## Hardening attestation

- [ ] No exploit payloads or PoCs attached to this report
- [ ] Target is operator-owned environment
- [ ] Secrets redacted from evidence column

**Output path:** `artifacts/security/{{date}}-dast-findings.md`

**Next command:** `/threat-profile` or `/review-changes`
