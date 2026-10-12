---
name: quality-coordination
description: Coordinate specialists; never lower gates.
---

# Quality coordination

quality-agent coordinates `/expand-test-coverage` (design + gate + Pending Approval), `/run-tests` (scripts + execute after Approved), and `/run-eval` (eval-agent + `/close-eval-gaps`). `/generate-test-cases-from-user-stories` is test-agent mode `from-user-story-excel` and is not routed through quality-agent. test-agent writes `docs/test-cases.md` + matrix (design on expand; scripts/run on `/run-tests`). br-coverage-validator is the only writer of `docs/test-cases-br-coverage.md`. Parent rejects a run that omits always-on safety families, treats silence as pass, scripts before coverage PASS, or runs `/run-tests` before package Approved. quality-agent mode `kpi` owns `/validate-kpi-metrics`. Do not merge review or security into quality-agent. Do not self-approve test packages.
