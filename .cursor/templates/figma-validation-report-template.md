# Figma Validation Report — {{PROJECT}}

> Output from `tools/figma/validate.py` during `/figma-to-nextjs`. Score ≥ 7.0 and zero critical required to pass.

| Field | Value |
|-------|-------|
| **Project root** | {{path}} |
| **Run date** | {{YYYY-MM-DD}} |
| **Command** | `/figma-to-nextjs` |
| **Iteration** | {{n}} of 3 |
| **Overall score** | {{x.x}} / 10 |
| **Verdict** | Pass / Fail / Escalated |

## Score breakdown

| Category | Score | Weight | Notes |
|----------|-------|--------|-------|
| Theme tokens | | | |
| Component coverage | | | |
| TypeScript | | | |
| Structure | | | |

## Critical findings (must be zero to pass)

| ID | Finding | File | Remediation |
|----|---------|------|-------------|
| | | | |

## Non-critical findings

| ID | Severity | Finding | File |
|----|----------|---------|------|
| | warning | | |

## Commands run

```bash
tools/figma/validate.py --root {{path}}
# tsc / npm test if applicable
```

## Next steps

- [ ] refinement-agent loop if failed
- [ ] Escalate to human after iteration 3

**Output path:** `docs/figma/{{project}}-validation-{{date}}.md`
