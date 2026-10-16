#!/usr/bin/env python3
"""Precondition ↔ step coherence checks for MSD E2E test cases.

Used by validate-msd-test-case-xlsx.py and agents before write. Heuristic only —
flags likely gaps (e.g. Step 1 updates an entity that preconditions never establish).
"""
from __future__ import annotations

import re
from typing import Any

# Step 1 verbs that usually require prior setup in Preconditions (not in Step 1).
_UPDATE_VERBS = re.compile(
    r"\b(update|change|modify|set|adjust|approve|reject|cancel|activate|deactivate|"
    r"onboard|offboard|submit|post|release|apply|transfer|reassign)\b",
    re.I,
)

# Entity / state tokens we expect to appear in preconditions when cited in early steps.
_ENTITY_HINTS = re.compile(
    r"\b("
    r"contract|agreement|partner|customer|account|order|quote|invoice|journal|"
    r"onboarding|onboarded|pricelist|list price|price list|campaign|lead|opportunity|"
    r"vendor|employee|user|role|workflow|approval|status|active|approved|"
    r"integration|zinfi|isv"
    r")\b",
    re.I,
)

_STATUS_TO_PATTERN = re.compile(
    r"\b(?:status|state)\s+(?:to|as|=)\s*[\"']?(\w+)[\"']?",
    re.I,
)
_SET_TO_PATTERN = re.compile(
    r"\bset\s+(?:the\s+)?(\w+(?:\s+\w+){0,3}?)\s+to\s+[\"']?(\w+)[\"']?",
    re.I,
)


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def _tokens_from_steps(steps: list[dict[str, Any]], max_steps: int = 2) -> set[str]:
    out: set[str] = set()
    for step in steps[:max_steps]:
        blob = " ".join(
            str(step.get(k) or "")
            for k in ("detailed_test_step", "test_data", "expected_result")
        )
        for m in _ENTITY_HINTS.finditer(blob):
            out.add(_norm(m.group(1)))
    return out


def _precondition_blob(preconditions: str) -> str:
    return _norm(preconditions)


def _step1_demands_setup(step_text: str) -> bool:
    if not step_text:
        return False
    if _UPDATE_VERBS.search(step_text):
        return True
    if re.search(r"\bto\s+approved\b", step_text, re.I):
        return True
    return False


def _missing_precondition_tokens(preconditions: str, step_tokens: set[str]) -> list[str]:
    pre = _precondition_blob(preconditions)
    missing: list[str] = []
    for tok in sorted(step_tokens):
        if not tok:
            continue
        # Allow partial match (e.g. "list price" in step vs "price" in preconditions).
        if tok in pre:
            continue
        if any(part in pre for part in tok.split() if len(part) > 3):
            continue
        missing.append(tok)
    return missing


def check_case_precondition_coherence(case: dict[str, Any], rulebook: dict[str, Any] | None = None) -> list[str]:
    """Return human-readable findings for one case dict (role keys + steps[])."""
    findings: list[str] = []
    pre = str(case.get("preconditions") or "")
    steps = case.get("steps") or []
    if not isinstance(steps, list) or not steps:
        return findings

    step1 = str((steps[0] or {}).get("detailed_test_step") or "")
    test_type = str(case.get("test_type") or "")
    cid = str(case.get("test_case_id") or "?")

    gen = (rulebook or {}).get("generation") or {}
    bp = gen.get("business_process_e2e") or {}
    min_pos = int(bp.get("min_steps_positive") or 0)
    if "positive" in test_type.lower() and min_pos and len(steps) < min_pos:
        findings.append(
            f"{cid}: positive E2E case has {len(steps)} step(s); "
            f"rulebook min_steps_positive is {min_pos} (business-process depth)."
        )

    if _step1_demands_setup(step1):
        early_tokens = _tokens_from_steps(steps, max_steps=1)
        # Drop generic tokens that rarely belong in preconditions alone.
        early_tokens -= {"status", "user", "role"}
        missing = _missing_precondition_tokens(pre, early_tokens)
        if missing:
            findings.append(
                f"{cid}: Step 1 implies existing state ({', '.join(missing)}) "
                f"but Preconditions do not establish it: {pre[:120]!r}..."
                if len(pre) > 120
                else f"{cid}: Step 1 implies existing state ({', '.join(missing)}) "
                f"but Preconditions do not establish it."
            )

    for m in _STATUS_TO_PATTERN.finditer(step1):
        status_val = _norm(m.group(1))
        if status_val and status_val not in _precondition_blob(pre):
            if not re.search(rf"\b{re.escape(status_val)}\b", pre):
                findings.append(
                    f"{cid}: Step 1 sets status to '{m.group(1)}' but Preconditions "
                    f"do not cite that status or prior lifecycle state."
                )

    for m in _SET_TO_PATTERN.finditer(step1):
        entity, value = m.group(1), m.group(2)
        ent_n = _norm(entity)
        val_n = _norm(value)
        if ent_n and ent_n not in _precondition_blob(pre) and val_n not in _precondition_blob(pre):
            findings.append(
                f"{cid}: Step 1 sets '{entity}' to '{value}' but Preconditions "
                f"do not describe '{entity}' existing before Step 1."
            )

    return findings


def check_cases_coherence(
    cases: list[dict[str, Any]],
    rulebook: dict[str, Any] | None = None,
) -> tuple[list[str], int]:
    """Return (findings, critical_count)."""
    cfg = ((rulebook or {}).get("validation") or {}).get("precondition_coherence") or {}
    severity = str(cfg.get("severity") or "critical")
    findings: list[str] = []
    critical = 0
    for case in cases:
        for msg in check_case_precondition_coherence(case, rulebook):
            findings.append(msg)
            if severity == "critical":
                critical += 1
    return findings, critical


def cases_from_register_rows(rulebook: dict[str, Any], rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    """Rebuild case objects from flat register rows (same shape as layout helper)."""
    roles = rulebook["columns"]["register"]["roles"]
    case_roles = rulebook["columns"]["register"]["case_level_roles"]
    step_roles = rulebook["columns"]["register"]["step_level_roles"]
    grouped: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for row in rows:
        cid = str(row.get(roles["test_case_id"]) or "").strip()
        if cid not in grouped:
            case = {k: str(row.get(roles[k]) or "").strip() for k in case_roles}
            case["steps"] = []
            grouped[cid] = case
            order.append(cid)
        step = {k: str(row.get(roles[k]) or "").strip() for k in step_roles}
        grouped[cid]["steps"].append(step)
    return [grouped[c] for c in order if c]
