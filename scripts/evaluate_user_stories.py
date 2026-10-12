#!/usr/bin/env python3
"""Prepare and render a /evaluate-user-stories report.

prepare  — parse both CSVs and emit a mechanical packet (no semantic scores).
render   — turn the KPI agent's evaluation JSON into HTML + a public JSON copy.
validate — check an evaluation JSON against the metric contract.

Agents own semantic scores. This script does not invent matches, hallucinations,
or business judgments. Structural signals (format, role, bullet counts, epic
context) are computed from the rulebook and row order so subagents can cite them.

Usage:
  python scripts/evaluate_user_stories.py prepare \\
    --manual manual.csv --generated generated.csv --transcript transcript.txt \\
    --out artifacts/evaluation/.pipeline/<date>-evaluation-packet.json

  python scripts/evaluate_user_stories.py render \\
    --evaluation artifacts/evaluation/.pipeline/<date>-evaluation.json \\
    --html artifacts/evaluation/<date>-user-story-evaluation.html \\
    --json artifacts/evaluation/<date>-user-story-evaluation.json

  python scripts/evaluate_user_stories.py allocate-run --date 2026-10-09 [--slug manual-vs-v2]
    Emits JSON paths for a **new** run. Never returns paths that already exist.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_METRICS = ROOT / ".cursor" / "templates" / "user-story-evaluation-metrics.yaml"
DEFAULT_RULEBOOK = ROOT / "docs" / "intake" / "user-story-csv-rulebook.yaml"

DESC_RE = re.compile(
    r"^As a (?P<role>[^,]+), I need to (?P<need>.+), so that (?P<benefit>.+)\.$",
    re.IGNORECASE | re.DOTALL,
)
GENERIC_ROLES = {"user", "users"}
TOKEN_RE = re.compile(r"[a-z0-9]+")
NEGATIVE_TOKENS = (
    "not",
    "cannot",
    "can't",
    "must not",
    "only",
    "at most",
    "at least",
    "empty",
    "blank",
    "maximum",
    "minimum",
    "boundary",
    "exception",
    "otherwise",
    "invalid",
    "unauthorized",
    "without",
)


def _load_yaml(path: Path) -> dict:
    if yaml is None:
        print("FAIL: PyYAML required (pip install pyyaml)", file=sys.stderr)
        sys.exit(1)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print(f"FAIL: YAML root must be a mapping: {path}", file=sys.stderr)
        sys.exit(1)
    return data


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            return [], []
        headers = list(reader.fieldnames)
        rows = []
        for row in reader:
            rows.append({k: (v or "").strip() for k, v in row.items() if k is not None})
    return headers, rows


def _bullets(cell: str) -> list[str]:
    return [line.strip() for line in (cell or "").splitlines() if line.strip()]


def _tokens(text: str) -> set[str]:
    return set(TOKEN_RE.findall((text or "").lower()))


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 0.0
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def _context_snapshot(row: dict[str, str], row_number: int) -> dict:
    return {
        "row_number": row_number,
        "id": row.get("ID", ""),
        "title": row.get("Title", ""),
        "work_item_type": row.get("Work Item Type", ""),
    }


def index_stories(rows: list[dict[str, str]], side: str) -> list[dict]:
    """Walk ADO row order. Epic/Feature context is the nearest preceding row."""
    epic: dict | None = None
    feature: dict | None = None
    stories: list[dict] = []
    for offset, row in enumerate(rows, start=2):
        wit = row.get("Work Item Type", "")
        if wit == "Epic":
            epic = _context_snapshot(row, offset)
            feature = None
            continue
        if wit == "Feature":
            feature = _context_snapshot(row, offset)
            continue
        if wit != "User Story":
            continue
        title = row.get("Title", "")
        description = row.get("Description", "")
        ac_lines = _bullets(row.get("Acceptance Criteria", ""))
        hyphen_ok = all(line.startswith("- ") for line in ac_lines) if ac_lines else False
        desc_match = DESC_RE.match(description.strip())
        role = desc_match.group("role").strip() if desc_match else ""
        title_ok = bool(title) and not title.lower().startswith("as a ")
        description_ok = desc_match is not None
        role_specific = bool(role) and role.lower() not in GENERIC_ROLES
        blob = f"{title}\n{description}"
        negative_hits = [
            line
            for line in ac_lines
            if any(token in line.lower() for token in NEGATIVE_TOKENS)
        ]
        stories.append(
            {
                "story_key": f"{side}-US-{offset}",
                "side": side,
                "row_number": offset,
                "id": row.get("ID", ""),
                "title": title,
                "description": description,
                "acceptance_criteria": ac_lines,
                "area_path": row.get("Area Path", ""),
                "epic": epic,
                "feature": feature,
                "structural": {
                    "title_ok": title_ok,
                    "description_ok": description_ok,
                    "format_ok": title_ok and description_ok,
                    "role": role,
                    "role_specific": role_specific,
                    "ac_count": len(ac_lines),
                    "ac_hyphen_format_ok": hyphen_ok,
                    "negative_boundary_signal_lines": negative_hits,
                    "need_count": len(re.findall(r"\bI need to\b", description, flags=re.IGNORECASE)),
                },
                "tokens": sorted(_tokens(blob)),
            }
        )
    return stories


def _mean(values: list[int]) -> float | None:
    if not values:
        return None
    return round(sum(values) / len(values), 2)


def structural_summary(stories: list[dict]) -> dict:
    count = len(stories)
    format_ok = sum(1 for s in stories if s["structural"]["format_ok"])
    role_ok = sum(1 for s in stories if s["structural"]["role_specific"])
    ac_counts = [s["structural"]["ac_count"] for s in stories]
    return {
        "user_story_count": count,
        "format_ok_count": format_ok,
        "format_compliance_ratio": (format_ok / count) if count else None,
        "role_specific_count": role_ok,
        "role_specificity_ratio": (role_ok / count) if count else None,
        "ac_bullet_total": sum(ac_counts),
        "ac_bullet_mean": _mean(ac_counts),
        "note": (
            "Signals only. Semantic metrics stay null until the owning subagent "
            "writes the evaluation JSON. ASSUMPTION-USEVAL-002 applies to role_specific."
        ),
    }


def candidate_pairs(manual: list[dict], generated: list[dict], floor: float) -> list[dict]:
    """Lexical proposals. Not matches and not recall/precision."""
    proposals: list[dict] = []
    for m in manual:
        m_tokens = set(m["tokens"])
        for g in generated:
            score = round(_jaccard(m_tokens, set(g["tokens"])), 4)
            if score < floor:
                continue
            proposals.append(
                {
                    "manual_key": m["story_key"],
                    "generated_key": g["story_key"],
                    "jaccard": score,
                    "status": "proposal",
                }
            )
    proposals.sort(key=lambda item: item["jaccard"], reverse=True)
    return proposals


def strip_tokens(stories: list[dict]) -> list[dict]:
    cleaned = []
    for story in stories:
        item = dict(story)
        item.pop("tokens", None)
        cleaned.append(item)
    return cleaned


def _slug_safe(slug: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", slug.strip())
    return cleaned.strip("-")


def allocate_run_paths(date: str, slug: str | None = None) -> dict:
    """Pick versioned artifact paths. Bump -v2, -v3, … until the public HTML path is free."""
    safe = _slug_safe(slug) if slug else ""
    stem = f"{date}-user-story-evaluation"
    if safe:
        stem = f"{stem}-{safe}"
    version = ""
    bump = 2
    ev_dir = ROOT / "artifacts" / "evaluation"
    pipe = ev_dir / ".pipeline"
    while True:
        run_tag = f"{stem}{version}"
        public_html = ev_dir / f"{run_tag}.html"
        if not public_html.exists():
            break
        version = f"-v{bump}"
        bump += 1
    ver_suffix = version
    if safe:
        eval_prefix = f"{date}-{safe}-evaluation"
        sub_prefix = f"{date}-{safe}"
    else:
        eval_prefix = f"{date}-evaluation"
        sub_prefix = date
    audit = ROOT / "artifacts" / "audit" / f"{date}-evaluate-user-stories{ver_suffix}.md"
    if safe and not ver_suffix:
        audit = ROOT / "artifacts" / "audit" / f"{date}-evaluate-user-stories-{safe}.md"
    elif safe and ver_suffix:
        audit = ROOT / "artifacts" / "audit" / f"{date}-evaluate-user-stories-{safe}{ver_suffix}.md"
    return {
        "run_id": run_tag,
        "date": date,
        "output_slug": safe or None,
        "version_suffix": ver_suffix or None,
        "policy": "new_run_only",
        "public_html": str(ev_dir / f"{run_tag}.html"),
        "public_json": str(ev_dir / f"{run_tag}.json"),
        "packet": str(pipe / f"{eval_prefix}-packet{ver_suffix}.json"),
        "story_matches": str(pipe / f"{sub_prefix}-story-matches{ver_suffix}.json"),
        "hallucination": str(pipe / f"{sub_prefix}-hallucination{ver_suffix}.json"),
        "coverage": str(pipe / f"{sub_prefix}-coverage{ver_suffix}.json"),
        "business_correctness": str(pipe / f"{sub_prefix}-business-correctness{ver_suffix}.json"),
        "acceptance_criteria": str(pipe / f"{sub_prefix}-acceptance-criteria{ver_suffix}.json"),
        "epic_feature": str(pipe / f"{sub_prefix}-epic-feature{ver_suffix}.json"),
        "evaluation": str(pipe / f"{eval_prefix}{ver_suffix}.json"),
        "audit": str(audit),
    }


def allocate_run(args: argparse.Namespace) -> int:
    paths = allocate_run_paths(args.date, args.slug)
    if args.json:
        print(json.dumps(paths, indent=2))
    else:
        for key, value in paths.items():
            print(f"{key}: {value}")
    return 0


def prepare(args: argparse.Namespace) -> int:
    metrics = _load_yaml(Path(args.metrics))
    rulebook = _load_yaml(Path(args.rulebook))
    expected = list(rulebook.get("csv", {}).get("column_order", []))
    manual_headers, manual_rows = read_csv_rows(Path(args.manual))
    generated_headers, generated_rows = read_csv_rows(Path(args.generated))
    header_findings = []
    if expected and manual_headers != expected:
        header_findings.append("manual CSV header does not match rulebook column_order")
    if expected and generated_headers != expected:
        header_findings.append("generated CSV header does not match rulebook column_order")

    transcript_path = Path(args.transcript)
    transcript_text = transcript_path.read_text(encoding="utf-8")
    manual_stories = index_stories(manual_rows, "manual")
    generated_stories = index_stories(generated_rows, "generated")
    floor = float(args.candidate_jaccard_floor)
    packet = {
        "schema_version": "1.0",
        "kind": "evaluation-packet",
        "assumption_id": metrics.get("assumption_id", "ASSUMPTION-USEVAL-001"),
        "status": "packet",
        "inputs": {
            "manual_csv": str(args.manual),
            "generated_csv": str(args.generated),
            "transcript_path": str(args.transcript),
            "transcript_char_count": len(transcript_text),
            "transcript_line_count": transcript_text.count("\n") + (1 if transcript_text else 0),
        },
        "header_findings": header_findings,
        "metric_contract": [
            {
                "metric_id": m["metric_id"],
                "name": m["name"],
                "owner": m["owner"],
                "kind": m["kind"],
                "formula": " ".join(str(m.get("formula", "")).split()),
            }
            for m in metrics.get("metrics", [])
        ],
        "manual_stories": strip_tokens(manual_stories),
        "generated_stories": strip_tokens(generated_stories),
        "structural_summary": {
            "manual": structural_summary(manual_stories),
            "generated": structural_summary(generated_stories),
        },
        "candidate_pairs": candidate_pairs(manual_stories, generated_stories, floor),
        "candidate_jaccard_floor": floor,
        "candidate_note": (
            "ASSUMPTION-USEVAL-003: Jaccard proposals are retrieval aids for "
            "story-matching-evaluator. They are not matches and must not be copied into Recall or Precision."
        ),
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    print(f"WROTE {out}")
    return 0


def _metric_index(contract: list[dict]) -> dict[str, dict]:
    return {item["metric_id"]: item for item in contract}


def validate_evaluation(document: dict, contract: list[dict]) -> list[str]:
    findings: list[str] = []
    for key in ("schema_version", "inputs", "matches", "manual_only", "generated_only", "metrics"):
        if key not in document:
            findings.append(f"missing top-level field: {key}")
    inputs = document.get("inputs") or {}
    for key in ("manual_csv", "generated_csv", "transcript_path"):
        if not inputs.get(key):
            findings.append(f"missing inputs.{key}")
    if not isinstance(document.get("matches", []), list):
        findings.append("matches must be a list")
    if not isinstance(document.get("manual_only", []), list):
        findings.append("manual_only must be a list")
    if not isinstance(document.get("generated_only", []), list):
        findings.append("generated_only must be a list")
    by_id = {item.get("metric_id"): item for item in document.get("metrics") or []}
    expected = _metric_index(contract)
    for metric_id, spec in expected.items():
        row = by_id.get(metric_id)
        if row is None:
            findings.append(f"missing metric: {metric_id}")
            continue
        if row.get("owner") != spec["owner"]:
            findings.append(
                f"{metric_id}: owner {row.get('owner')!r} != contract owner {spec['owner']!r}"
            )
        if row.get("kind") != spec["kind"]:
            findings.append(
                f"{metric_id}: kind {row.get('kind')!r} != contract kind {spec['kind']!r}"
            )
        if row.get("na") is True:
            if not row.get("na_reason"):
                findings.append(f"{metric_id}: na requires na_reason")
            continue
        if "display" not in row or row.get("display") in ("", None):
            findings.append(f"{metric_id}: display is required")
        evidence = row.get("evidence") or []
        if not evidence:
            findings.append(f"{metric_id}: evidence is required")
        else:
            for index, item in enumerate(evidence, start=1):
                for field in ("statement", "source_path", "source_locator", "confidence"):
                    if not item.get(field):
                        findings.append(f"{metric_id}: evidence[{index}] missing {field}")
    extra = set(by_id) - set(expected)
    for metric_id in sorted(extra):
        findings.append(f"metric not in contract: {metric_id}")
    for index, match in enumerate(document.get("matches") or [], start=1):
        for field in ("match_id", "manual_key", "generated_keys", "match_type", "confidence"):
            if match.get(field) in (None, "", []):
                findings.append(f"matches[{index}] missing {field}")
    for index, row in enumerate(document.get("generated_only") or [], start=1):
        if row.get("classification") not in ("valid_extra", "noise"):
            findings.append(f"generated_only[{index}] classification must be valid_extra or noise")
    return findings


def _esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _is_lower_better(metric_id: str | None) -> bool:
    return metric_id == "hallucination_rate"


def _band_from_unit(number: float, lower_better: bool = False) -> str:
    if lower_better:
        if number <= 0.1:
            return "good"
        if number <= 0.25:
            return "warn"
        return "bad"
    if number >= 0.8:
        return "good"
    if number >= 0.6:
        return "warn"
    return "bad"


def _metric_band(row: dict) -> str:
    if row.get("na") is True:
        return "neutral"
    metric_id = row.get("metric_id")
    kind = row.get("kind")
    if kind in ("count", "comparison", "split"):
        return "neutral"
    try:
        number = float(row.get("score"))
    except (TypeError, ValueError):
        return "neutral"
    if kind == "score":
        number = number / 100.0
    return _band_from_unit(number, lower_better=_is_lower_better(metric_id))


def _evidence_html(items: list[dict]) -> str:
    if not items:
        return "<p class='muted'>No evidence recorded.</p>"
    blocks = []
    for item in items:
        refs = item.get("transcript_refs") or []
        ref_html = ""
        if refs:
            chips = "".join(
                f"<li><span class='loc'>{_esc(ref.get('locator'))}</span> {_esc(ref.get('excerpt'))}</li>"
                for ref in refs
            )
            ref_html = f"<ul class='refs'>{chips}</ul>"
        blocks.append(
            "<blockquote>"
            f"<p>{_esc(item.get('statement'))}</p>"
            f"<p class='src'>{_esc(item.get('source_path'))} · {_esc(item.get('source_locator'))}"
            f" · {_esc(item.get('confidence'))}</p>"
            f"{ref_html}"
            "</blockquote>"
        )
    return "".join(blocks)


def _story_table(rows: list[dict], columns: list[tuple[str, str]]) -> str:
    if not rows:
        return "<p class='muted'>None.</p>"
    head = "".join(f"<th>{_esc(label)}</th>" for _, label in columns)
    body = []
    for row in rows:
        cells = "".join(f"<td>{_esc(row.get(key, ''))}</td>" for key, _ in columns)
        body.append(f"<tr>{cells}</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def _comparison_html(document: dict) -> str:
    rows = document.get("comparison") or []
    if not rows:
        return ""
    body = []
    for row in rows:
        better = row.get("better") or ""
        manual_cls = " class='win'" if better == "manual" else ""
        ai_cls = " class='win'" if better == "ai" else ""
        label = {"manual": "Manual", "ai": "AI", "tie": "Tie"}.get(better, "")
        body.append(
            "<tr>"
            f"<td>{_esc(row.get('name'))}</td>"
            f"<td{manual_cls}>{_esc(row.get('manual'))}</td>"
            f"<td{ai_cls}>{_esc(row.get('ai'))}</td>"
            f"<td>{_esc(label)}</td>"
            f"<td>{_esc(row.get('note'))}</td>"
            "</tr>"
        )
    return (
        "<h2>Manual and AI side by side</h2>"
        "<p class='muted'>A highlighted cell is the stronger side on that row. "
        "Hallucination rate is stronger when it is lower. Recall, precision, and agreement "
        "describe the pair, so neither side is highlighted.</p>"
        "<div class='table-wrap'>"
        "<table class='compare'><thead><tr>"
        "<th>Metric</th><th>Manual</th><th>AI</th><th>Stronger</th><th>Evidence note</th>"
        "</tr></thead><tbody>"
        + "".join(body)
        + "</tbody></table></div>"
    )


def _conclusion_html(document: dict) -> str:
    conclusion = document.get("conclusion") or {}
    if not conclusion:
        return ""
    strengths = conclusion.get("reasons") or []
    items = "".join(f"<li>{_esc(item)}</li>" for item in strengths)
    return (
        "<section class='conclusion'>"
        f"<p class='eyebrow dark'>{_esc(conclusion.get('label', 'Conclusion'))}</p>"
        f"<h2>{_esc(conclusion.get('headline'))}</h2>"
        f"<p class='verdict'>{_esc(conclusion.get('winner_line'))}</p>"
        f"<ul>{items}</ul>"
        f"<p>{_esc(conclusion.get('limit'))}</p>"
        "</section>"
    )


def render_html(document: dict) -> str:
    metrics = document.get("metrics") or []
    cards = []
    details = []
    for row in metrics:
        band = _metric_band(row)
        display = "n/a" if row.get("na") else row.get("display", "")
        cards.append(
            "<article class='kpi {band}'>"
            f"<p class='kicker'>{_esc(row.get('owner'))}</p>"
            f"<h3>{_esc(row.get('name'))}</h3>"
            f"<p class='score'>{_esc(display)}</p>"
            f"<p class='formula'>{_esc(row.get('formula', ''))}</p>"
            "</article>".replace("{band}", band)
        )
        details.append(
            "<details open>"
            f"<summary><span class='band {band}'></span>{_esc(row.get('name'))}"
            f"<em>{_esc(display)}</em></summary>"
            f"<p class='owner'>Owner: {_esc(row.get('owner'))} · kind {_esc(row.get('kind'))}</p>"
            + (
                f"<p class='na'>Not applicable: {_esc(row.get('na_reason'))}</p>"
                if row.get("na")
                else ""
            )
            + _evidence_html(row.get("evidence") or [])
            + "</details>"
        )

    matches = []
    for match in document.get("matches") or []:
        keys = match.get("generated_keys") or []
        generated = ", ".join(str(key) for key in keys)
        refs = match.get("transcript_refs") or []
        ref_text = "; ".join(
            f"{ref.get('locator', '')} {ref.get('excerpt', '')}".strip() for ref in refs
        )
        matches.append(
            {
                "match_id": match.get("match_id", ""),
                "manual_key": match.get("manual_key", ""),
                "manual_title": match.get("manual_title", ""),
                "generated": generated,
                "generated_titles": match.get("generated_titles", ""),
                "match_type": match.get("match_type", ""),
                "confidence": match.get("confidence", ""),
                "transcript": ref_text,
            }
        )

    manual_only = []
    for row in document.get("manual_only") or []:
        refs = row.get("transcript_refs") or []
        manual_only.append(
            {
                "story_key": row.get("story_key", ""),
                "title": row.get("title", ""),
                "rationale": row.get("rationale", ""),
                "transcript": "; ".join(
                    f"{ref.get('locator', '')} {ref.get('excerpt', '')}".strip() for ref in refs
                ),
            }
        )

    generated_only = []
    for row in document.get("generated_only") or []:
        refs = row.get("transcript_refs") or []
        generated_only.append(
            {
                "story_key": row.get("story_key", ""),
                "title": row.get("title", ""),
                "classification": row.get("classification", ""),
                "rationale": row.get("rationale", ""),
                "transcript": "; ".join(
                    f"{ref.get('locator', '')} {ref.get('excerpt', '')}".strip() for ref in refs
                ),
            }
        )

    inputs = document.get("inputs") or {}
    status = document.get("status") or "Draft — Pending Method Review"
    open_items = document.get("open_items") or []
    open_html = (
        "<ul>" + "".join(f"<li>{_esc(item)}</li>" for item in open_items) + "</ul>"
        if open_items
        else "<p class='muted'>None recorded.</p>"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>User story evaluation</title>
<style>
  :root {{
    --bg: #f3f0e8;
    --paper: #fffcf7;
    --ink: #1c1915;
    --muted: #5e584e;
    --line: #e3dcd0;
    --accent: #1f6b4a;
    --good: #1f6b4a;
    --warn: #8a5a12;
    --bad: #8f2d2d;
    --neutral: #3d4a55;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font: 16px/1.5 "Segoe UI", "Helvetica Neue", sans-serif;
  }}
  header {{
    background: #1c1915;
    color: #f6f1e7;
    padding: 2.5rem 1.5rem 2rem;
  }}
  header .wrap, main {{ max-width: 1100px; margin: 0 auto; }}
  main {{ padding: 1.5rem 1.5rem 3rem; }}
  h1 {{ font-family: Georgia, "Times New Roman", serif; font-weight: 500; font-size: 2.1rem; margin: 0 0 0.35rem; }}
  h2 {{ font-family: Georgia, "Times New Roman", serif; font-weight: 500; font-size: 1.45rem; margin: 2rem 0 0.75rem; }}
  .eyebrow {{ letter-spacing: 0.08em; text-transform: uppercase; font-size: 0.75rem; color: #d7c7a5; margin: 0 0 0.6rem; }}
  .status {{
    display: inline-block;
    margin-top: 0.8rem;
    border: 1px solid #8d7344;
    color: #f3e6cf;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-size: 0.85rem;
  }}
  .meta {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 0.75rem; margin-top: 1.2rem; }}
  .meta div {{ background: #2a261f; border-radius: 8px; padding: 0.75rem 0.9rem; }}
  .meta span {{ display: block; color: #b7ab96; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em; }}
  .meta strong {{ font-weight: 500; word-break: break-word; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 0.8rem; }}
  .kpi {{ background: var(--paper); border: 1px solid var(--line); border-top: 4px solid var(--neutral); border-radius: 10px; padding: 0.9rem 1rem 1rem; }}
  .kpi.good {{ border-top-color: var(--good); }}
  .kpi.warn {{ border-top-color: var(--warn); }}
  .kpi.bad {{ border-top-color: var(--bad); }}
  .kpi h3 {{ margin: 0.15rem 0 0.35rem; font-size: 1rem; }}
  .kicker {{ margin: 0; color: var(--muted); font-size: 0.72rem; }}
  .score {{ margin: 0; font-family: Georgia, serif; font-size: 1.7rem; }}
  .formula {{ margin: 0.45rem 0 0; color: var(--muted); font-size: 0.82rem; }}
  details {{ background: var(--paper); border: 1px solid var(--line); border-radius: 10px; padding: 0.7rem 1rem; margin: 0.6rem 0; }}
  summary {{ cursor: pointer; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; }}
  summary em {{ margin-left: auto; font-style: normal; font-weight: 500; color: var(--muted); }}
  .band {{ width: 0.65rem; height: 0.65rem; border-radius: 50%; background: var(--neutral); display: inline-block; }}
  .band.good {{ background: var(--good); }}
  .band.warn {{ background: var(--warn); }}
  .band.bad {{ background: var(--bad); }}
  .owner, .na, .src {{ color: var(--muted); font-size: 0.85rem; }}
  blockquote {{ margin: 0.6rem 0; padding: 0.4rem 0 0.4rem 0.8rem; border-left: 3px solid var(--line); }}
  blockquote p {{ margin: 0.2rem 0; }}
  table {{ width: 100%; border-collapse: collapse; background: var(--paper); font-size: 0.92rem; }}
  th, td {{ border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; padding: 0.55rem 0.6rem; }}
  th {{ font-size: 0.75rem; letter-spacing: 0.03em; text-transform: uppercase; color: var(--muted); }}
  .table-wrap {{ overflow-x: auto; border: 1px solid var(--line); border-radius: 10px; }}
  td.win {{ background: #e7f4ec; font-weight: 650; }}
  .compare td:nth-child(2), .compare td:nth-child(3) {{ width: 18%; }}
  .conclusion {{
    margin-top: 2rem;
    background: #1c1915;
    color: #f6f1e7;
    border-radius: 12px;
    padding: 1.4rem 1.5rem 1.2rem;
  }}
  .conclusion h2 {{ color: #f6f1e7; margin-top: 0.2rem; }}
  .conclusion .verdict {{ font-family: Georgia, serif; font-size: 1.35rem; margin: 0.2rem 0 0.8rem; }}
  .eyebrow.dark {{ color: #d7c7a5; margin: 0; }}
  .muted {{ color: var(--muted); }}
  footer {{ color: var(--muted); font-size: 0.85rem; margin-top: 2rem; }}
  @media print {{
    header {{ background: white; color: black; }}
    .meta div {{ background: white; border: 1px solid #ccc; }}
    body {{ background: white; }}
  }}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <p class="eyebrow">/evaluate-user-stories</p>
    <h1>User story evaluation</h1>
    <p>Manual stories compared with AI-generated stories. The transcript is the ground truth.</p>
    <div class="status">{_esc(status)}</div>
    <div class="meta">
      <div><span>Manual CSV</span><strong>{_esc(inputs.get("manual_csv"))}</strong></div>
      <div><span>Generated CSV</span><strong>{_esc(inputs.get("generated_csv"))}</strong></div>
      <div><span>Transcript</span><strong>{_esc(inputs.get("transcript_path"))}</strong></div>
    </div>
  </div>
</header>
<main>
  {_comparison_html(document)}
  <h2>Metric detail</h2>
  <div class="grid">
    {''.join(cards)}
  </div>
  <h2>Evidence</h2>
  {''.join(details)}
  <h2>Matched stories</h2>
  <div class="table-wrap">
    {_story_table(matches, [
        ("match_id", "Match"),
        ("manual_key", "Manual key"),
        ("manual_title", "Manual title"),
        ("generated", "Generated keys"),
        ("generated_titles", "Generated titles"),
        ("match_type", "Type"),
        ("confidence", "Confidence"),
        ("transcript", "Transcript"),
    ])}
  </div>
  <h2>Manual-only stories</h2>
  <div class="table-wrap">
    {_story_table(manual_only, [
        ("story_key", "Key"),
        ("title", "Title"),
        ("rationale", "Rationale"),
        ("transcript", "Transcript"),
    ])}
  </div>
  <h2>Generated-only stories</h2>
  <div class="table-wrap">
    {_story_table(generated_only, [
        ("story_key", "Key"),
        ("title", "Title"),
        ("classification", "Class"),
        ("rationale", "Rationale"),
        ("transcript", "Transcript"),
    ])}
  </div>
  <h2>Open items</h2>
  {open_html}
  {_conclusion_html(document)}
  <footer>
    Method {_esc(document.get("assumption_id", "ASSUMPTION-USEVAL-001"))}.
    Scores are Draft until that method is accepted.
    Public HTML is written only by scripts/evaluate_user_stories.py render.
  </footer>
</main>
</body>
</html>
"""


def render(args: argparse.Namespace) -> int:
    metrics_doc = _load_yaml(Path(args.metrics))
    contract = metrics_doc.get("metrics") or []
    document = json.loads(Path(args.evaluation).read_text(encoding="utf-8"))
    findings = validate_evaluation(document, contract)
    if findings:
        print("FAIL", file=sys.stderr)
        for item in findings:
            print(f"- {item}", file=sys.stderr)
        return 1
    html_path = Path(args.html)
    json_path = Path(args.json)
    html_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    document.setdefault("status", "Draft — Pending Method Review")
    document.setdefault("assumption_id", metrics_doc.get("assumption_id"))
    for row in document.get("metrics") or []:
        spec = next(item for item in contract if item["metric_id"] == row["metric_id"])
        row["formula"] = " ".join(str(spec.get("formula", "")).split())
        row["name"] = spec["name"]
    html_path.write_text(render_html(document), encoding="utf-8")
    json_path.write_text(json.dumps(document, indent=2), encoding="utf-8")
    print(f"WROTE {html_path}")
    print(f"WROTE {json_path}")
    return 0


def validate_cmd(args: argparse.Namespace) -> int:
    metrics_doc = _load_yaml(Path(args.metrics))
    document = json.loads(Path(args.evaluation).read_text(encoding="utf-8"))
    findings = validate_evaluation(document, metrics_doc.get("metrics") or [])
    if findings:
        print("FAIL")
        for item in findings:
            print(f"- {item}")
        return 1
    print("PASS")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics", default=str(DEFAULT_METRICS))
    sub = parser.add_subparsers(dest="command", required=True)

    prep = sub.add_parser("prepare", help="Write the mechanical evaluation packet")
    prep.add_argument("--manual", required=True)
    prep.add_argument("--generated", required=True)
    prep.add_argument("--transcript", required=True)
    prep.add_argument("--rulebook", default=str(DEFAULT_RULEBOOK))
    prep.add_argument("--out", required=True)
    prep.add_argument("--candidate-jaccard-floor", type=float, default=0.28)
    prep.set_defaults(func=prepare)

    shown = sub.add_parser("render", help="Render evaluation JSON to HTML")
    shown.add_argument("--evaluation", required=True)
    shown.add_argument("--html", required=True)
    shown.add_argument("--json", required=True)
    shown.set_defaults(func=render)

    check = sub.add_parser("validate", help="Validate evaluation JSON against the metric contract")
    check.add_argument("--evaluation", required=True)
    check.set_defaults(func=validate_cmd)

    alloc = sub.add_parser(
        "allocate-run",
        help="Return paths for a new evaluation run (never an existing public HTML)",
    )
    alloc.add_argument("--date", required=True, help="YYYY-MM-DD run date")
    alloc.add_argument("--slug", default=None, help="Optional output_slug for the filename stem")
    alloc.add_argument("--json", action="store_true", help="Emit machine-readable JSON only")
    alloc.set_defaults(func=allocate_run)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
