#!/usr/bin/env python3
"""One-shot prune: keep two commands + deps. Never touches docs/, scripts/, tools/, rules/, templates/."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PROTECTED_PREFIXES = (
    "docs",
    "scripts",
    "tools",
    ".cursor/rules",
    ".cursor/templates",
)

KEEP_COMMANDS = {
    "generate-user-stories-from-transcript.md",
    "expand-test-coverage.md",
    "evaluate-user-stories.md",
    "README.md",
}

KEEP_AGENTS = {
    "orchestrator-agent.md",
    "business-analyst-agent.md",
    "quality-agent.md",
    "test-agent.md",
    "user-story-evaluation-agent.md",
    "README.md",
}

KEEP_SUBAGENTS = {
    "transcript-story-extractor.md",
    "user-story-csv-compliance-validator.md",
    "ado-user-story-csv-writer.md",
    "user-story-csv-rulebook-author.md",
    "transcript-analyzer.md",
    "invest-validator.md",
    "harness-updater.md",
    "audit-trail-writer.md",
    "test-intake-normalizer.md",
    "test-case-generator.md",
    "automation-companion-author.md",
    "tc-traceability-mapper.md",
    "tc-completeness-validator.md",
    "tc-step-quality-validator.md",
    "bdd-scenario-expander.md",
    "br-coverage-validator.md",
    "story-matching-evaluator.md",
    "coverage-analysis-evaluator.md",
    "business-correctness-evaluator.md",
    "acceptance-criteria-evaluator.md",
    "hallucination-detection-evaluator.md",
    "epic-feature-mapping-evaluator.md",
    "kpi-aggregation-evaluator.md",
    "README.md",
}

KEEP_SKILL_DIRS = {
    "user-story-from-transcript",
    "intake-safety",
    "br-coverage",
    "quality",
    "user-story-evaluation",
    "story-matching",
    "coverage-analysis",
    "business-correctness",
    "acceptance-criteria-evaluation",
    "hallucination-detection",
    "epic-feature-mapping-validation",
    "kpi-aggregation",
}

REMOVE_TOP_LEVEL_DIRS = (
    "evals",
    "artifacts",
    "workshop",
    "java_master_templates",
    "java_test_templates",
    ".claude",
    ".github",
    "worktrees",
)

REMOVE_TOP_LEVEL_FILES = (
    "CURSOR-FLOW.md",
    "CLAUDE-FLOW.md",
    "COPILOT-FLOW.md",
    "AGENTS.md",
)


def is_protected(rel: str) -> bool:
    rel = rel.replace("\\", "/")
    for p in PROTECTED_PREFIXES:
        if rel == p or rel.startswith(p + "/"):
            return True
    return False


def rm_path(path: Path) -> bool:
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    if is_protected(rel):
        raise RuntimeError(f"refused protected path: {rel}")
    try:
        if path.is_dir():
            shutil.rmtree(path, onerror=lambda _f, _p, _e: None)
            return not path.exists()
        if path.exists():
            path.unlink()
        return True
    except OSError as e:
        print(f"SKIP (locked or denied): {rel} ({e})")
        return False


def main() -> None:
    removed: list[str] = []
    skipped: list[str] = []

    def track(rel: str, ok: bool) -> None:
        (removed if ok else skipped).append(rel)

    for name in REMOVE_TOP_LEVEL_DIRS:
        p = ROOT / name
        if p.exists():
            track(name + "/", rm_path(p))

    for name in REMOVE_TOP_LEVEL_FILES:
        p = ROOT / name
        if p.exists():
            track(name, rm_path(p))

    for p in ROOT.glob("*.docx"):
        track(p.name, rm_path(p))
    for p in ROOT.glob("*.csv"):
        track(p.name, rm_path(p))

    plans = ROOT / ".cursor" / "plans"
    if plans.is_dir():
        track(".cursor/plans/", rm_path(plans))

    cmd_dir = ROOT / ".cursor" / "commands"
    for f in cmd_dir.glob("*.md"):
        if f.name not in KEEP_COMMANDS:
            track(f".cursor/commands/{f.name}", rm_path(f))

    ag_dir = ROOT / ".cursor" / "agents"
    for f in ag_dir.glob("*.md"):
        if f.name not in KEEP_AGENTS:
            track(f".cursor/agents/{f.name}", rm_path(f))

    sub_dir = ROOT / ".cursor" / "subagents"
    for f in sub_dir.glob("*.md"):
        if f.name not in KEEP_SUBAGENTS:
            track(f".cursor/subagents/{f.name}", rm_path(f))

    skills = ROOT / ".cursor" / "skills"
    if skills.is_dir():
        for d in skills.iterdir():
            if d.is_dir() and d.name not in KEEP_SKILL_DIRS:
                track(f".cursor/skills/{d.name}/", rm_path(d))

    print(f"Removed {len(removed)} paths; skipped {len(skipped)}")
    if skipped:
        print("Skipped:")
        for s in skipped[:20]:
            print(" !", s)
    for r in sorted(removed)[:40]:
        print(" -", r)
    if len(removed) > 40:
        print(f" ... and {len(removed) - 40} more")


if __name__ == "__main__":
    main()
