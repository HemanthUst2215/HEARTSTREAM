# Cursor drop-in (core)

Governance: root [`.cursorrules`](../.cursorrules). Cursor also loads [`rules/cursor-factory-governance.mdc`](rules/cursor-factory-governance.mdc) (`alwaysApply`). Operator map: [`CURSOR-FLOW.md`](../CURSOR-FLOW.md).

| Path | Role |
|------|------|
| `../.cursorrules` | Always-on factory governance |
| PIPELINE.md | Drop-in spine pointer (canonical map is `CURSOR-FLOW.md`) |
| AGENTS.md | Catalog pointer |
| EXECUTION-OPTIONS.md | Manual vs batch |
| config.yaml.example | Module + eval + gate paths |
| scope.yaml | Agent write allowlists |
| mcp.json.example | Figma + Playwright |
| agents/ commands/ subagents/ rules/ skills/ templates/ hooks/ | Factory runtime (agents and subagents are flat `*.md`, no domain subfolders) |
