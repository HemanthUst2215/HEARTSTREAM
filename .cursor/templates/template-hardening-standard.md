# Template hardening standard

Every factory template must be **fill-in-ready**: metadata header, required sections, tables with column definitions, provenance fields, and an explicit output path. Agents must not ship empty headings or one-line placeholders.

## Required elements

| Element | Rule |
|---------|------|
| **Title** | `# <Artifact type> — {{PLACEHOLDER}}` |
| **Metadata table** | Date, ID, status, owner, command/agent, iteration |
| **Sections** | H2 for major blocks; H3 for sub-blocks |
| **Tables** | Column headers with allowed values where enums apply |
| **Provenance** | `source_path`, `source_locator`, `confidence` for behavior/requirements |
| **Governance** | Human gate status, Open DQ refs, Do not invent reminders where applicable |
| **Output path** | Bold line at bottom: `**Output path:**` with canonical location |

## Quality bar

- **Thin (forbidden):** single line or bullet list without structure (e.g. "Paths, methods, envelope").
- **Hardened (required):** same depth as `issue-log-template.md` or `audit-trail-template.md` for operational artifacts; KPI templates keep evidence matrices.
- **Twins:** `.cursor/templates/`, `.claude/templates/`, `.github/templates/` must match byte-for-byte after changes.

## Status values (use consistently)

| Artifact | Status values |
|----------|---------------|
| BRD | Draft — Pending Domain Review / Accepted / Waived |
| Plan | Proposed — Pending Approval / Approved / Rejected |
| Coverage | PASS / FAIL / BLOCKED |
| KPI | GO / NO_GO / CONDITIONAL |
| Issue | Triage / Plan pending / Approved / In progress / Fixed / Verified / Cancelled |
| ADR | Proposed / Accepted / Deprecated / Superseded |

## Agent instructions

1. Copy template structure exactly; replace `{{placeholders}}` only.
2. Do not delete sections — mark `N/A` with rationale if truly inapplicable.
3. Register `ASSUMPTION-<id>` or `DQ-xxx` when sources are silent; do not invent content to fill gaps.
4. Redact secrets, credentials, and raw PII/PHI from all filled templates.
