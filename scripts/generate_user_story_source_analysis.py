#!/usr/bin/env python3
"""Prepare and render /generate-html-for-user-stories reports.

prepare-kb     — mechanical source index (no semantic judgments).
prepare-stories — index User Stories from one CSV side (no manual vs AI pairing).
validate       — check analysis JSON against the structural contract.
render           — turn analysis JSON into HTML + public JSON copy.

Agents own semantic traceability and gap analysis. This script does
not compare manual CSV with generated CSV.

Usage:
  python scripts/generate_user_story_source_analysis.py allocate-run --date 2026-10-16 [--slug ws03] --json

  python scripts/generate_user_story_source_analysis.py prepare-kb \\
    --transcript t.txt --mom m1.txt --preread p.txt \\
    --sow-json artifacts/work-items/SOW.json \\
    --out artifacts/evaluation/.pipeline/2026-10-16-source-kb-index.json

  python scripts/generate_user_story_source_analysis.py prepare-stories \\
    --csv manual.csv --side manual --kb-index <index.json> --out <packet.json>

  python scripts/generate_user_story_source_analysis.py validate --analysis <analysis.json>
  python scripts/generate_user_story_source_analysis.py render \\
    --analysis <analysis.json> --html <manual-user-story-analysis.html> --json <public.json>
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from evaluate_user_stories import (  # noqa: E402 — sibling script
    DEFAULT_RULEBOOK,
    _load_yaml,
    _slug_safe,
    index_stories,
    read_csv_rows,
    strip_tokens,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = (
    ROOT / ".cursor" / "templates" / "user-story-source-analysis-contract.yaml"
)
TOKEN_RE = re.compile(r"[a-z0-9]+")
CHUNK_LINES = 40
NO_EVIDENCE_EXCERPT = "No Supporting Evidence Found"
EXACT_MATCH_LEXICAL_FLOOR = 0.35


def has_supporting_refs(refs: list | None) -> bool:
    """USHTML-MATCH-001: at least one excerpt that is not the no-evidence sentinel."""
    for ref in refs or []:
        excerpt = (ref.get("excerpt") or "").strip()
        if excerpt and excerpt != NO_EVIDENCE_EXCERPT:
            return True
    return False


def match_type_from_evidence(has_support: bool, lexical_best: float = 0.0) -> str:
    """USHTML-MATCH-001: No Match only without supporting references."""
    if not has_support:
        return "No Match"
    if lexical_best >= EXACT_MATCH_LEXICAL_FLOOR:
        return "Exact Match"
    return "Partial Match"


def _esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _line_chunks(text: str, source_type: str, path: str) -> list[dict]:
    lines = text.splitlines()
    chunks: list[dict] = []
    if not lines:
        chunks.append(
            {
                "locator": "empty",
                "text": "",
                "source_type": source_type,
                "source_path": path,
            }
        )
        return chunks
    for start in range(0, len(lines), CHUNK_LINES):
        end = min(start + CHUNK_LINES, len(lines))
        excerpt = "\n".join(lines[start:end])
        chunks.append(
            {
                "locator": f"lines {start + 1}-{end}",
                "text": excerpt,
                "source_type": source_type,
                "source_path": path,
            }
        )
    return chunks


def _sow_feature_rows(sow_path: Path) -> list[dict]:
    data = json.loads(sow_path.read_text(encoding="utf-8"))
    rows = data.get("rows") or []
    features: list[dict] = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            continue
        bpm = str(row.get("BPM") or row.get("topic") or "").strip()
        workshop = str(row.get("Workshop") or "").strip()
        minutes = row.get("Annexure ID") or row.get("Annexure ID1") or ""
        title = f"{minutes} - {bpm}".strip(" -") if minutes else bpm
        features.append(
            {
                "feature_key": f"SOW-{index}",
                "feature_name": title or workshop or f"Feature {index}",
                "workshop_code": workshop,
                "bpm_topic": bpm,
                "annexure_minutes": minutes,
                "source_path": str(sow_path),
                "source_locator": f"SOW.rows[{index - 1}]",
                "source_type": "Feature List",
            }
        )
    return features


def allocate_run_paths(date: str, slug: str | None = None) -> dict:
    """Versioned paths; bump until both public HTML stems are free."""
    safe = _slug_safe(slug) if slug else ""
    manual_stem = f"{date}-manual-user-story-analysis"
    ai_stem = f"{date}-ai-user-story-analysis"
    if safe:
        manual_stem = f"{manual_stem}-{safe}"
        ai_stem = f"{ai_stem}-{safe}"
    version = ""
    bump = 2
    ev_dir = ROOT / "artifacts" / "evaluation"
    pipe = ev_dir / ".pipeline"
    while True:
        manual_html = ev_dir / f"{manual_stem}{version}.html"
        ai_html = ev_dir / f"{ai_stem}{version}.html"
        if not manual_html.exists() and not ai_html.exists():
            break
        version = f"-v{bump}"
        bump += 1
    ver_suffix = version
    run_tag = f"{date}-user-story-source-analysis{ver_suffix}"
    if safe:
        run_tag = f"{run_tag}-{safe}"
    audit = ROOT / "artifacts" / "audit" / f"{date}-generate-html-for-user-stories{ver_suffix}.md"
    if safe and not ver_suffix:
        audit = ROOT / "artifacts" / "audit" / f"{date}-generate-html-for-user-stories-{safe}.md"
    elif safe and ver_suffix:
        audit = (
            ROOT / "artifacts" / "audit" / f"{date}-generate-html-for-user-stories-{safe}{ver_suffix}.md"
        )
    prefix = f"{date}-source"
    if safe:
        prefix = f"{date}-{safe}-source"
    return {
        "run_id": run_tag,
        "date": date,
        "output_slug": safe or None,
        "version_suffix": ver_suffix or None,
        "policy": "new_run_only",
        "public_manual_html": str(ev_dir / f"{manual_stem}{ver_suffix}.html"),
        "public_manual_json": str(ev_dir / f"{manual_stem}{ver_suffix}.json"),
        "public_ai_html": str(ev_dir / f"{ai_stem}{ver_suffix}.html"),
        "public_ai_json": str(ev_dir / f"{ai_stem}{ver_suffix}.json"),
        "kb_index": str(pipe / f"{prefix}-kb-index{ver_suffix}.json"),
        "unified_kb": str(pipe / f"{prefix}-knowledge-base{ver_suffix}.json"),
        "manual_packet": str(pipe / f"{prefix}-manual-packet{ver_suffix}.json"),
        "ai_packet": str(pipe / f"{prefix}-ai-packet{ver_suffix}.json"),
        "manual_analysis": str(pipe / f"{prefix}-manual-analysis{ver_suffix}.json"),
        "ai_analysis": str(pipe / f"{prefix}-ai-analysis{ver_suffix}.json"),
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


def prepare_kb(args: argparse.Namespace) -> int:
    transcripts = [Path(p) for p in args.transcript]
    moms = [Path(p) for p in args.mom]
    prereads = [Path(p) for p in args.preread]
    sow = Path(args.sow_json)
    corpus: list[dict] = []
    for path in transcripts:
        corpus.extend(_line_chunks(_read_text(path), "Transcript", str(path)))
    for path in moms:
        corpus.extend(_line_chunks(_read_text(path), "MoM", str(path)))
    for path in prereads:
        corpus.extend(_line_chunks(_read_text(path), "Pre-read Materials", str(path)))
    features = _sow_feature_rows(sow) if sow.is_file() else []
    packet = {
        "schema_version": "1.0",
        "kind": "source-kb-index",
        "status": "index",
        "inputs": {
            "transcript_paths": [str(p) for p in transcripts],
            "mom_paths": [str(p) for p in moms],
            "preread_paths": [str(p) for p in prereads],
            "sow_json": str(sow),
        },
        "source_corpus_chunks": corpus,
        "feature_list_rows": features,
        "note": (
            "Mechanical index only. source-knowledge-base-unifier merges this into "
            "unified_knowledge_base JSON with cited requirements."
        ),
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    print(f"WROTE {out}")
    return 0


def prepare_stories(args: argparse.Namespace) -> int:
    side = args.side
    if side not in ("manual", "generated"):
        print("FAIL: --side must be manual or generated", file=sys.stderr)
        return 1
    rulebook = _load_yaml(Path(args.rulebook))
    expected = list(rulebook.get("csv", {}).get("column_order", []))
    headers, rows = read_csv_rows(Path(args.csv))
    header_findings = []
    if expected and headers != expected:
        header_findings.append("CSV header does not match rulebook column_order")
    stories = strip_tokens(index_stories(rows, side))
    kb_index = json.loads(Path(args.kb_index).read_text(encoding="utf-8"))
    packet = {
        "schema_version": "1.0",
        "kind": "source-analysis-packet",
        "side": side,
        "status": "packet",
        "inputs": {
            "user_story_csv": str(args.csv),
            "kb_index": str(args.kb_index),
            "unified_knowledge_base": args.unified_kb or "",
        },
        "header_findings": header_findings,
        "user_stories": stories,
        "feature_list_rows": kb_index.get("feature_list_rows") or [],
        "kb_index_note": kb_index.get("note"),
        "analysis_contract": str(DEFAULT_CONTRACT),
        "forbidden": [
            "Do not read or compare the other CSV side.",
            "Do not perform manual vs AI matching or benchmarking.",
        ],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    print(f"WROTE {out}")
    return 0


def _validate_story(story: dict, contract: dict, prefix: str) -> list[str]:
    findings: list[str] = []
    for field in contract.get("story_required_fields") or []:
        if field not in story:
            findings.append(f"{prefix} missing field {field}")
    match_type = story.get("match_type")
    if match_type and match_type not in (contract.get("allowed_match_types") or []):
        findings.append(f"{prefix} invalid match_type {match_type!r}")
    for src in story.get("derived_sources") or []:
        if src not in (contract.get("allowed_derived_sources") or []):
            findings.append(f"{prefix} invalid derived_source {src!r}")
    cov = story.get("coverage_assessment")
    if cov and cov not in (contract.get("allowed_coverage_assessment") or []):
        findings.append(f"{prefix} invalid coverage_assessment {cov!r}")
    refs = story.get("source_references")
    if refs is not None and not isinstance(refs, list):
        findings.append(f"{prefix} source_references must be a list")
    has_support = has_supporting_refs(refs if isinstance(refs, list) else None)
    if match_type == "No Match" and has_support:
        findings.append(
            f"{prefix} USHTML-MATCH-001: No Match with supporting source_references"
        )
    if match_type in ("Partial Match", "Exact Match") and not has_support:
        findings.append(
            f"{prefix} USHTML-MATCH-001: {match_type} requires supporting source_references"
        )
    why_mapped = (story.get("why_mapped_to_feature") or "").lower()
    for banned in contract.get("feature_mapping_rules", {}).get(
        "forbidden_why_mapped_substrings"
    ) or []:
        if banned.lower() in why_mapped:
            findings.append(
                f"{prefix} USHTML-FEAT-001: why_mapped_to_feature must not cite CSV row order"
            )
            break
    return findings


def validate_analysis(document: dict, contract: dict) -> list[str]:
    findings: list[str] = []
    for key in ("schema_version", "kind", "side", "inputs", "executive_summary", "stories"):
        if key not in document:
            findings.append(f"missing top-level field: {key}")
    if document.get("kind") != "user-story-source-analysis":
        findings.append("kind must be user-story-source-analysis")
    if document.get("side") not in ("manual", "generated"):
        findings.append("side must be manual or generated")
    summary = document.get("executive_summary") or {}
    for field in contract.get("executive_summary_required_fields") or []:
        if field not in summary:
            findings.append(f"executive_summary missing {field}")
    stories = document.get("stories") or []
    if not isinstance(stories, list):
        findings.append("stories must be a list")
    else:
        for index, story in enumerate(stories, start=1):
            findings.extend(_validate_story(story, contract, f"stories[{index}]"))
    gap_fields = contract.get("matrix_row_requirements_not_in_stories_fields") or []
    for index, row in enumerate(document.get("feature_traceability_matrix") or [], start=1):
        for gap in row.get("requirements_not_in_stories") or []:
            for field in gap_fields:
                if not gap.get(field):
                    findings.append(
                        f"feature_traceability_matrix[{index}] requirements_not_in_stories missing {field}"
                    )
    for section in (
        "feature_traceability_matrix",
        "source_coverage_summary",
        "coverage_gap_analysis",
    ):
        if section not in document:
            findings.append(f"missing top-level field: {section}")
    return findings


def _refs_html(refs: list[dict]) -> str:
    if not refs:
        return "<p class='muted'>No Supporting Evidence Found</p>"
    items = []
    for ref in refs:
        excerpt = ref.get("excerpt") or "No Supporting Evidence Found"
        items.append(
            "<li>"
            f"<strong>{_esc(ref.get('source_type', ''))}</strong> "
            f"<span class='loc'>{_esc(ref.get('locator', ''))}</span>: "
            f"{_esc(excerpt)}"
            "</li>"
        )
    return f"<ul class='refs'>{''.join(items)}</ul>"


def _why_generated_html(story: dict) -> str:
    """Render multi-paragraph why_generated (AI / generated side HTML only)."""
    body = (story.get("why_generated") or "").strip()
    if not body:
        return ""
    paragraphs = [p.strip() for p in body.replace("\r\n", "\n").split("\n\n") if p.strip()]
    if len(paragraphs) <= 1 and "\n" in body:
        paragraphs = [p.strip() for p in body.split("\n") if p.strip()]
    if not paragraphs:
        paragraphs = [body]
    inner = "".join(f"<p>{_esc(p)}</p>" for p in paragraphs)
    return "<h4>Why generated</h4><div class='why-detail'>" + inner + "</div>"


def _story_cards(stories: list[dict], side: str) -> str:
    if not stories:
        return "<p class='muted'>No user stories indexed.</p>"
    show_generation_fields = side != "manual"
    blocks = []
    for story in stories:
        title = story.get("user_story_title") or story.get("title") or ""
        extra = ""
        if show_generation_fields:
            extra = (
                _why_generated_html(story)
                + "<h4>Why mapped to feature</h4>"
                f"<p>{_esc(story.get('why_mapped_to_feature', ''))}</p>"
            )
        blocks.append(
            "<article class='story-card'>"
            f"<h3>{_esc(story.get('user_story_id') or story.get('id', ''))} · {_esc(title)}</h3>"
            f"<p><strong>Feature:</strong> {_esc(story.get('feature_name', ''))} · "
            f"<strong>Match:</strong> {_esc(story.get('match_type', ''))}</p>"
            f"<p><strong>Derived sources:</strong> {_esc(', '.join(story.get('derived_sources') or []))}</p>"
            "<h4>Source references</h4>"
            + _refs_html(story.get("source_references") or [])
            + extra
            + f"<p><strong>Business context:</strong> {_esc(story.get('supporting_business_context', ''))}</p>"
            f"<p><strong>Coverage:</strong> {_esc(story.get('coverage_assessment', ''))}</p>"
            f"<p><strong>Confidence:</strong> {_esc(story.get('confidence_score', ''))} · "
            f"<strong>Action:</strong> {_esc(story.get('recommended_action', ''))}</p>"
            "</article>"
        )
    return "".join(blocks)


def _matrix_sections(rows: list[dict]) -> str:
    if not rows:
        return "<p class='muted'>None.</p>"
    blocks: list[str] = []
    for row in rows:
        mapped = row.get("mapped_user_stories") or []
        mapped_html = (
            "<ul>" + "".join(f"<li>{_esc(t)}</li>" for t in mapped) + "</ul>"
            if mapped
            else "<p class='muted'>None mapped in this CSV.</p>"
        )
        gaps = row.get("requirements_not_in_stories") or []
        if gaps:
            gap_items = []
            for gap in gaps:
                gap_items.append(
                    "<li>"
                    f"<strong>{_esc(gap.get('requirement', ''))}</strong>"
                    f"<p>{_esc(gap.get('why_not_converted', ''))}</p>"
                    f"<p class='src'>{_esc(gap.get('source_type', ''))} · "
                    f"{_esc(gap.get('source_locator', ''))}</p>"
                    "</li>"
                )
            gaps_html = f"<ul class='feature-gaps'>{''.join(gap_items)}</ul>"
        else:
            gaps_html = "<p class='muted'>All sourced requirements for this topic are represented in user stories (or none were indexed).</p>"
        code = row.get("workshop_code") or ""
        code_html = f" <span class='src'>({_esc(code)})</span>" if code else ""
        blocks.append(
            "<section class='feature-trace'>"
            f"<h3>{_esc(row.get('feature_name', ''))}{code_html}</h3>"
            f"<p><strong>Coverage:</strong> {_esc(row.get('coverage_percent', ''))}%</p>"
            "<h4>Mapped user stories</h4>"
            f"{mapped_html}"
            "<h4>Requirements not converted into user stories</h4>"
            f"{gaps_html}"
            "</section>"
        )
    return "".join(blocks)


def _gap_list(items: list[dict]) -> str:
    if not items:
        return "<p class='muted'>None identified.</p>"
    lis = []
    for item in items:
        lis.append(
            "<li>"
            f"{_esc(item.get('statement', ''))} "
            f"<span class='src'>({_esc(item.get('source_type', ''))} · "
            f"{_esc(item.get('source_path', ''))} · {_esc(item.get('source_locator', ''))})</span>"
            "</li>"
        )
    return f"<ul>{''.join(lis)}</ul>"


def render_html(document: dict) -> str:
    side = document.get("side") or ""
    side_label = "Manual" if side == "manual" else "AI-generated"
    command_label = "/generate-html-for-user-stories"
    summary = document.get("executive_summary") or {}
    inputs = document.get("inputs") or {}
    status = document.get("status") or "Draft — Pending Method Review"
    cov = document.get("source_coverage_summary") or {}
    gaps = document.get("coverage_gap_analysis") or {}
    open_items = document.get("open_items") or []
    open_html = (
        "<ul>" + "".join(f"<li>{_esc(item)}</li>" for item in open_items) + "</ul>"
        if open_items
        else "<p class='muted'>None recorded.</p>"
    )

    kpi_cards = [
        ("Total user stories", summary.get("total_user_stories")),
        ("Exact matches", summary.get("exact_matches")),
        ("Partial matches", summary.get("partial_matches")),
        ("No matches", summary.get("no_matches")),
        ("Fully supported", summary.get("fully_supported_stories")),
        ("Traceability score", summary.get("overall_traceability_score")),
    ]
    cards_html = "".join(
        "<article class='kpi'>"
        f"<p class='kicker'>{_esc(label)}</p>"
        f"<p class='score'>{_esc(value)}</p>"
        "</article>"
        for label, value in kpi_cards
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_esc(side_label)} user story source analysis</title>
<style>
  :root {{
    --bg: #f3f0e8;
    --paper: #fffcf7;
    --ink: #1c1915;
    --muted: #5e584e;
    --line: #e3dcd0;
    --accent: #1f6b4a;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.5 "Segoe UI", sans-serif; }}
  header {{ background: #1c1915; color: #f6f1e7; padding: 2.5rem 1.5rem 2rem; }}
  header .wrap, main {{ max-width: 1100px; margin: 0 auto; }}
  main {{ padding: 1.5rem 1.5rem 3rem; }}
  h1 {{ font-family: Georgia, serif; font-weight: 500; font-size: 2.1rem; margin: 0 0 0.35rem; }}
  h2 {{ font-family: Georgia, serif; font-weight: 500; font-size: 1.45rem; margin: 2rem 0 0.75rem; }}
  h3 {{ font-size: 1.05rem; margin: 0 0 0.4rem; }}
  h4 {{ font-size: 0.9rem; margin: 0.75rem 0 0.35rem; color: var(--muted); }}
  .eyebrow {{ letter-spacing: 0.08em; text-transform: uppercase; font-size: 0.75rem; color: #d7c7a5; }}
  .status {{ display: inline-block; margin-top: 0.8rem; border: 1px solid #8d7344; color: #f3e6cf;
    padding: 0.2rem 0.6rem; border-radius: 999px; font-size: 0.85rem; }}
  .meta {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 0.75rem; margin-top: 1.2rem; }}
  .meta div {{ background: #2a261f; border-radius: 8px; padding: 0.75rem 0.9rem; }}
  .meta span {{ display: block; color: #b7ab96; font-size: 0.75rem; text-transform: uppercase; }}
  .meta strong {{ font-weight: 500; word-break: break-word; font-size: 0.9rem; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 0.8rem; }}
  .kpi {{ background: var(--paper); border: 1px solid var(--line); border-top: 4px solid var(--accent);
    border-radius: 10px; padding: 0.9rem 1rem; }}
  .kicker {{ margin: 0; color: var(--muted); font-size: 0.72rem; }}
  .score {{ margin: 0; font-family: Georgia, serif; font-size: 1.5rem; }}
  .story-card {{ background: var(--paper); border: 1px solid var(--line); border-radius: 10px;
    padding: 1rem 1.1rem; margin: 0.75rem 0; }}
  .table-wrap {{ overflow-x: auto; border: 1px solid var(--line); border-radius: 10px; }}
  table {{ width: 100%; border-collapse: collapse; background: var(--paper); font-size: 0.92rem; }}
  th, td {{ border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; padding: 0.55rem 0.6rem; }}
  th {{ font-size: 0.75rem; text-transform: uppercase; color: var(--muted); }}
  .muted {{ color: var(--muted); }}
  .src, .loc {{ color: var(--muted); font-size: 0.85rem; }}
  .refs {{ margin: 0.3rem 0 0.6rem; padding-left: 1.2rem; }}
  .feature-trace {{ background: var(--paper); border: 1px solid var(--line); border-radius: 10px;
    padding: 1rem 1.1rem; margin: 0.85rem 0; }}
  .feature-gaps li {{ margin: 0.65rem 0; }}
  .why-detail {{ background: #f8f5ef; border-left: 3px solid var(--accent); padding: 0.5rem 0.85rem; margin: 0.35rem 0 0.75rem; }}
  .why-detail p {{ margin: 0.35rem 0; }}
  footer {{ color: var(--muted); font-size: 0.85rem; margin-top: 2rem; }}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <p class="eyebrow">{_esc(command_label)}</p>
    <h1>{_esc(side_label)} user story analysis</h1>
    <p>Independent validation of {_esc(side_label.lower())} user stories against workshop source inputs only.</p>
    <div class="status">{_esc(status)}</div>
    <div class="meta">
      <div><span>User story CSV</span><strong>{_esc(inputs.get('user_story_csv'))}</strong></div>
      <div><span>Unified knowledge base</span><strong>{_esc(inputs.get('unified_knowledge_base'))}</strong></div>
      <div><span>Side</span><strong>{_esc(side_label)}</strong></div>
    </div>
  </div>
</header>
<main>
  <h2>Executive summary</h2>
  <div class="grid">{cards_html}</div>
  <h2>Per user story</h2>
  {_story_cards(document.get('stories') or [], side)}
  <h2>Feature traceability matrix</h2>
  {_matrix_sections(document.get('feature_traceability_matrix') or [])}
  <h2>Source coverage summary</h2>
  <div class="grid">
    <article class="kpi"><p class="kicker">Transcript</p><p class="score">{_esc(cov.get('transcript_percent'))}%</p></article>
    <article class="kpi"><p class="kicker">MoM</p><p class="score">{_esc(cov.get('mom_percent'))}%</p></article>
    <article class="kpi"><p class="kicker">Pre-read</p><p class="score">{_esc(cov.get('preread_percent'))}%</p></article>
    <article class="kpi"><p class="kicker">Feature list</p><p class="score">{_esc(cov.get('feature_list_percent'))}%</p></article>
  </div>
  <h2>Coverage and gap analysis</h2>
  <h3>Feature requirements not converted into user stories</h3>
  {_gap_list(gaps.get('feature_requirements_not_in_stories') or [])}
  <h3>Source requirements discussed but not captured</h3>
  {_gap_list(gaps.get('source_requirements_not_captured') or [])}
  <h3>Unmapped user stories</h3>
  {_gap_list(gaps.get('unmapped_user_stories') or [])}
  <h3>Missing business scenarios</h3>
  {_gap_list(gaps.get('missing_business_scenarios') or [])}
  <h2>Open items</h2>
  {open_html}
  <footer>
    Method {_esc(document.get('assumption_id', 'ASSUMPTION-USHTML-001'))}.
    This report does not compare manual and AI user stories.
    HTML written only by scripts/generate_user_story_source_analysis.py render.
  </footer>
</main>
</body>
</html>
"""


def render(args: argparse.Namespace) -> int:
    contract = _load_yaml(Path(args.contract))
    document = json.loads(Path(args.analysis).read_text(encoding="utf-8"))
    findings = validate_analysis(document, contract)
    if findings:
        print("FAIL", file=sys.stderr)
        for item in findings:
            print(f"- {item}", file=sys.stderr)
        return 1
    html_path = Path(args.html)
    json_path = Path(args.json)
    html_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    document.setdefault("status", contract.get("status"))
    document.setdefault("assumption_id", contract.get("assumption_id"))
    html_path.write_text(render_html(document), encoding="utf-8")
    json_path.write_text(json.dumps(document, indent=2), encoding="utf-8")
    print(f"WROTE {html_path}")
    print(f"WROTE {json_path}")
    return 0


def validate_cmd(args: argparse.Namespace) -> int:
    contract = _load_yaml(Path(args.contract))
    document = json.loads(Path(args.analysis).read_text(encoding="utf-8"))
    findings = validate_analysis(document, contract)
    if findings:
        print("FAIL")
        for item in findings:
            print(f"- {item}")
        return 1
    print("PASS")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    alloc = sub.add_parser("allocate-run", help="Return paths for a new source-analysis run")
    alloc.add_argument("--date", required=True)
    alloc.add_argument("--slug", default=None)
    alloc.add_argument("--json", action="store_true")
    alloc.set_defaults(func=allocate_run)

    kb = sub.add_parser("prepare-kb", help="Write mechanical source index")
    kb.add_argument("--transcript", action="append", default=[], required=True)
    kb.add_argument("--mom", action="append", default=[])
    kb.add_argument("--preread", action="append", default=[])
    kb.add_argument("--sow-json", required=True)
    kb.add_argument("--out", required=True)
    kb.set_defaults(func=prepare_kb)

    stories = sub.add_parser("prepare-stories", help="Index one CSV side for analysis")
    stories.add_argument("--csv", required=True)
    stories.add_argument("--side", required=True, choices=["manual", "generated"])
    stories.add_argument("--kb-index", required=True)
    stories.add_argument("--unified-kb", default="")
    stories.add_argument("--rulebook", default=str(DEFAULT_RULEBOOK))
    stories.add_argument("--out", required=True)
    stories.set_defaults(func=prepare_stories)

    check = sub.add_parser("validate", help="Validate analysis JSON")
    check.add_argument("--analysis", required=True)
    check.add_argument("--contract", default=str(DEFAULT_CONTRACT))
    check.set_defaults(func=validate_cmd)

    shown = sub.add_parser("render", help="Render analysis JSON to HTML")
    shown.add_argument("--analysis", required=True)
    shown.add_argument("--html", required=True)
    shown.add_argument("--json", required=True)
    shown.add_argument("--contract", default=str(DEFAULT_CONTRACT))
    shown.set_defaults(func=render)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
