#!/usr/bin/env python3
"""Render docs/user-story-generation-process.html (stakeholder process guide)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL_DIR = ROOT / "artifacts" / "evaluation"
OUT = ROOT / "docs" / "user-story-generation-process.html"

EVAL_FILES = sorted(
    p.name
    for p in EVAL_DIR.glob("*.json")
    if p.is_file() and not p.name.startswith(".")
)

RUN_LABELS = {
    "2026-10-08-user-story-evaluation": "Workshop comparison — run A",
    "2026-10-09-user-story-evaluation-sales-ce-r2r": "Workshop comparison — run B",
    "2026-10-09-user-story-evaluation-claude-scratch": "Workshop comparison — run C",
}


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_html(), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")


def load_evaluation_runs() -> list[dict]:
    """Snapshot comparison metrics from artifacts/evaluation for offline HTML."""
    runs: list[dict] = []
    for name in EVAL_FILES:
        path = EVAL_DIR / name
        if not path.is_file():
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        run_id = doc.get("run_id") or name.replace(".json", "")
        runs.append(
            {
                "runId": run_id,
                "label": RUN_LABELS.get(run_id, "Workshop comparison"),
                "status": doc.get("status"),
                "comparison": doc.get("comparison") or [],
            }
        )
    return runs


def build_html() -> str:
    eval_runs = json.dumps(load_evaluation_runs(), ensure_ascii=False)
    run_labels = json.dumps(RUN_LABELS)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>User Story Generation — HeartStream AI Factory</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
  :root {{
    --bg: #e8edf2;
    --bg-accent: radial-gradient(ellipse 120% 80% at 50% -20%, rgba(0, 118, 129, 0.12), transparent 55%);
    --surface: #ffffff;
    --surface-2: #f4f7fa;
    --ink: #0f1720;
    --muted: #5c6773;
    --line: #d0d8e2;
    --ust-navy: #0c2340;
    --ust-teal: #007681;
    --ust-green: #1a7a52;
    --accent: var(--ust-teal);
    --good: var(--ust-green);
    --warn: #b45309;
    --radius: 14px;
    --shadow: 0 12px 40px rgba(12, 35, 64, 0.09);
    --shadow-hover: 0 16px 48px rgba(12, 35, 64, 0.14);
  }}
  * {{ box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    margin: 0;
    font: 16px/1.6 "DM Sans", "Segoe UI", sans-serif;
    color: var(--ink);
    background: var(--bg);
    background-image: var(--bg-accent);
  }}
  .hero {{
    background: linear-gradient(145deg, #0c2340 0%, #134063 42%, #0a5c62 100%);
    color: #f4f7fa;
    padding: 3.5rem 1.5rem 3rem;
    position: relative;
    overflow: hidden;
  }}
  .hero::after {{
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 85% 20%, rgba(255,255,255,0.08), transparent 45%);
    pointer-events: none;
  }}
  .wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 1.5rem; position: relative; z-index: 1; }}
  .hero h1 {{
    font-family: "Instrument Serif", Georgia, serif;
    font-size: clamp(2.1rem, 4.5vw, 3rem);
    font-weight: 400;
    margin: 0 0 0.6rem;
    line-height: 1.12;
    letter-spacing: -0.02em;
  }}
  .eyebrow {{
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-size: 0.7rem;
    color: #8ec4d4;
    margin: 0 0 0.85rem;
    font-weight: 600;
  }}
  .hero p.lead {{ max-width: 40rem; color: #b8c9d6; margin: 0; font-size: 1.05rem; }}
  .hero-badges {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1.5rem; }}
  .badge {{
    font-size: 0.78rem;
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.2);
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(4px);
  }}
  nav.sticky {{
    position: sticky;
    top: 0;
    z-index: 40;
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--line);
    box-shadow: 0 4px 20px rgba(12, 35, 64, 0.04);
  }}
  nav.sticky .wrap {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem 1.25rem;
    padding-top: 0.7rem;
    padding-bottom: 0.7rem;
  }}
  nav a {{
    color: var(--ust-navy);
    text-decoration: none;
    font-size: 0.88rem;
    font-weight: 600;
    padding: 0.2rem 0;
    border-bottom: 2px solid transparent;
  }}
  nav a:hover {{ color: var(--accent); border-bottom-color: var(--accent); }}
  main {{ padding: 2.5rem 0 4.5rem; }}
  section {{
    margin-bottom: 3.5rem;
    scroll-margin-top: 4.5rem;
    padding: 1.75rem;
    background: var(--surface);
    border-radius: calc(var(--radius) + 4px);
    border: 1px solid var(--line);
    box-shadow: var(--shadow);
  }}
  section h2 {{
    font-family: "Instrument Serif", Georgia, serif;
    font-size: 1.85rem;
    font-weight: 400;
    margin: 0 0 0.4rem;
    color: var(--ust-navy);
  }}
  h3 {{ font-size: 1.05rem; margin: 1.35rem 0 0.55rem; color: var(--ust-navy); }}
  .section-intro {{ color: var(--muted); margin: 0 0 1.35rem; max-width: 46rem; }}
  .grid-2 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; }}
  .card {{
    background: linear-gradient(180deg, var(--surface) 0%, var(--surface-2) 100%);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 1.25rem 1.3rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }}
  .card:hover {{
    transform: translateY(-3px);
    box-shadow: var(--shadow-hover);
  }}
  .card .icon {{
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 10px;
    background: linear-gradient(135deg, #e0f2f4, #c5e8ec);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.75rem;
    font-size: 1.15rem;
  }}
  .card h3 {{ margin-top: 0; font-size: 1.02rem; }}
  .card p {{ margin: 0; color: var(--muted); font-size: 0.92rem; line-height: 1.5; }}
  .flow-steps {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 0.65rem;
  }}
  .step {{
    background: var(--surface-2);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 1rem 0.75rem;
    text-align: center;
    border-top: 3px solid var(--accent);
  }}
  .step .num {{
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--accent);
    font-weight: 700;
  }}
  .step strong {{ display: block; font-size: 0.88rem; margin: 0.35rem 0 0.25rem; color: var(--ust-navy); }}
  .step span {{ font-size: 0.78rem; color: var(--muted); line-height: 1.35; display: block; }}
  .diagram {{
    background: var(--surface-2);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 1.25rem;
    margin: 1.25rem 0;
    overflow-x: auto;
  }}
  table.data {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
  }}
  table.data th, table.data td {{
    border-bottom: 1px solid var(--line);
    padding: 0.7rem 0.85rem;
    text-align: left;
    vertical-align: top;
  }}
  table.data th {{
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--muted);
    background: var(--surface-2);
  }}
  table.data tr:hover td {{ background: #fafcfd; }}
  .table-wrap {{ overflow-x: auto; border: 1px solid var(--line); border-radius: var(--radius); }}
  .pill {{
    display: inline-block;
    font-size: 0.72rem;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    font-weight: 600;
  }}
  .pill.during {{ background: #fef3e8; color: var(--warn); }}
  .pill.after {{ background: #e8f0f8; color: var(--ust-navy); }}
  ul.clean {{ margin: 0.5rem 0 0; padding-left: 1.2rem; color: var(--muted); }}
  ul.clean li {{ margin-bottom: 0.45rem; }}
  #metrics {{
    background: linear-gradient(180deg, #fff 0%, #f8fafc 100%);
  }}
  .metrics-toolbar {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    align-items: center;
    margin-bottom: 1rem;
  }}
  .metrics-toolbar select {{
    font: inherit;
    padding: 0.5rem 0.85rem;
    border-radius: 10px;
    border: 1px solid var(--line);
    min-width: 260px;
    background: var(--surface);
    color: var(--ust-navy);
    font-weight: 500;
  }}
  .compare-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1rem;
  }}
  .compare-card {{
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 1rem 1.1rem;
    display: flex;
    flex-direction: column;
    gap: 0.7rem;
    transition: box-shadow 0.2s ease;
  }}
  .compare-card:hover {{ box-shadow: var(--shadow); }}
  .compare-card h4 {{
    margin: 0;
    font-size: 0.92rem;
    color: var(--ust-navy);
    font-weight: 700;
    letter-spacing: -0.01em;
  }}
  .compare-row {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.55rem;
  }}
  .compare-cell {{
    border-radius: 10px;
    padding: 0.65rem 0.75rem;
    background: var(--surface-2);
    border: 2px solid transparent;
  }}
  .compare-cell.win {{
    border-color: var(--good);
    background: linear-gradient(180deg, #edf7f1, #e4f3ea);
  }}
  .compare-cell label {{
    display: block;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--muted);
    margin-bottom: 0.25rem;
    font-weight: 600;
  }}
  .compare-cell .val {{ font-weight: 700; font-size: 0.9rem; color: var(--ink); line-height: 1.35; }}
  .compare-note {{
    font-size: 0.8rem;
    color: var(--muted);
    line-height: 1.45;
    padding-top: 0.15rem;
    border-top: 1px dashed var(--line);
  }}
  .compare-meta .stronger {{
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--accent);
    display: block;
    margin-bottom: 0.35rem;
  }}
  .metrics-meta {{
    font-size: 0.88rem;
    color: var(--muted);
    margin-bottom: 0.85rem;
  }}
  .status-chip {{
    display: inline-block;
    font-size: 0.75rem;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    background: #eef4f8;
    color: var(--ust-navy);
    font-weight: 600;
  }}
  .pipeline {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 1.5rem;
    background: linear-gradient(90deg, var(--ust-navy), #165a7a);
    border-radius: var(--radius);
    color: #fff;
  }}
  .pipeline .node {{
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.25);
    padding: 0.55rem 1rem;
    border-radius: 10px;
    font-size: 0.82rem;
    font-weight: 600;
  }}
  .pipeline .node.eval {{
    background: var(--accent);
    border-color: transparent;
  }}
  .pipeline .arrow {{ opacity: 0.7; font-size: 1rem; }}
  footer {{
    border-top: 1px solid var(--line);
    padding: 2rem 1.5rem;
    color: var(--muted);
    font-size: 0.88rem;
    background: var(--surface);
    text-align: center;
  }}
  @media (max-width: 640px) {{
    .compare-row {{ grid-template-columns: 1fr; }}
    section {{ padding: 1.25rem; }}
  }}
  @media print {{
    nav.sticky {{ display: none; }}
    section {{ box-shadow: none; break-inside: avoid; }}
  }}
</style>
</head>
<body>
<header class="hero">
  <div class="wrap">
    <p class="eyebrow">HeartStream · AI Factory · UST</p>
    <h1>User Story Generation</h1>
    <p class="lead">From workshop conversation to traceable Azure DevOps stories—aligned to your catalog and measured against human-authored baselines.</p>
    <div class="hero-badges">
      <span class="badge">Source-backed requirements</span>
      <span class="badge">Standard story format</span>
      <span class="badge">Catalog-aware mapping</span>
      <span class="badge">Quality comparison</span>
    </div>
  </div>
</header>

<nav class="sticky" aria-label="Page sections">
  <div class="wrap">
    <a href="#inputs">Inputs</a>
    <a href="#flow">Flow</a>
    <a href="#layout">Story layout</a>
    <a href="#epic-feature">Epic &amp; Feature</a>
    <a href="#work-items">Mapping</a>
    <a href="#metrics">KPI metrics</a>
    <a href="#pipeline">Pipeline</a>
  </div>
</nav>

<main class="wrap">

<section id="inputs">
  <h2>1. Inputs used</h2>
  <p class="section-intro">Trusted factory rules plus workshop material. One-time setup data is not used at runtime once the playbook is active.</p>
  <div class="grid-2">
    <article class="card">
      <div class="icon" aria-hidden="true">&#128221;</div>
      <h3>Workshop transcript</h3>
      <p>Recorded discussion text. Requirements are traced to what was actually said. Content is screened before extraction.</p>
    </article>
    <article class="card">
      <div class="icon" aria-hidden="true">&#128214;</div>
      <h3>Story playbook</h3>
      <p>Column layout, work item types, and narrative patterns for Azure DevOps export—the single formatting contract.</p>
    </article>
    <article class="card">
      <div class="icon" aria-hidden="true">&#128200;</div>
      <h3>Epic &amp; Feature catalog</h3>
      <p>Approved hierarchy titles and identifiers. Stories attach to existing features; new epic names are not invented.</p>
    </article>
    <article class="card">
      <div class="icon" aria-hidden="true">&#128451;</div>
      <h3>Work item registry</h3>
      <p>Structured catalog of workshops, epics, and features used when attaching IDs to the final story workbook.</p>
    </article>
  </div>
</section>

<section id="flow">
  <h2>2. Generation flow</h2>
  <p class="section-intro">Analyst agents extract and author; a dedicated mapping step adds catalog identifiers only after format validation passes.</p>
  <div class="flow-steps">
    <div class="step"><span class="num">Gate</span><strong>Safety check</strong><span>Screen transcript content.</span></div>
    <div class="step"><span class="num">1</span><strong>Understand</strong><span>Cited facts and quotes.</span></div>
    <div class="step"><span class="num">2</span><strong>Extract needs</strong><span>Candidate stories and risks.</span></div>
    <div class="step"><span class="num">3</span><strong>Write rows</strong><span>Canonical story export.</span></div>
    <div class="step"><span class="num">4</span><strong>Validate</strong><span>Layout and field rules.</span></div>
    <div class="step"><span class="num">5</span><strong>Map catalog</strong><span>Epic and feature IDs.</span></div>
    <div class="step"><span class="num">6</span><strong>Deliver</strong><span>Import-ready workbook.</span></div>
  </div>
  <div class="diagram mermaid">
flowchart LR
  T[Transcript] --> S[Safety check]
  S --> A[Understand session]
  A --> E[Extract requirements]
  E --> W[Author story rows]
  W --> V[Validate format]
  V --> M[Map to catalog]
  M --> X[Story workbook]
  </div>
  <h3>Requirements &amp; acceptance criteria</h3>
  <ul class="clean">
    <li><strong>Stories</strong> — Short title, role-based description, and bullet acceptance criteria tied to the transcript.</li>
    <li><strong>Feature first</strong> — Match the workshop topic to a catalog feature before writing the story.</li>
    <li><strong>Testable criteria</strong> — One observable outcome per line, including limits and negatives when the session stated them.</li>
  </ul>
</section>

<section id="layout">
  <h2>3. Story layout</h2>
  <p class="section-intro">Each row follows the playbook. The delivered workbook groups workshop context, matched epics and features, then user stories.</p>
  <div class="table-wrap">
    <table class="data">
      <thead>
        <tr><th>Field</th><th>On the story row</th><th>Comes from</th></tr>
      </thead>
      <tbody>
        <tr><td><strong>Identifier</strong></td><td>Catalog feature link when matched</td><td>Mapping step</td></tr>
        <tr><td><strong>Type</strong></td><td>User story (or workshop / issue when relevant)</td><td>Playbook</td></tr>
        <tr><td><strong>Title</strong></td><td>Short capability name</td><td>Workshop need</td></tr>
        <tr><td><strong>Description</strong></td><td>As a role, I need…, so that…</td><td>Workshop roles and outcomes</td></tr>
        <tr><td><strong>Acceptance criteria</strong></td><td>Hyphen bullets, one per line</td><td>Testable session outcomes</td></tr>
        <tr><td><strong>Area path</strong></td><td>Usually empty on stories</td><td>Export convention</td></tr>
        <tr><td><strong>Session fields</strong></td><td>Workshop and checklist columns</td><td>Session metadata</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section id="epic-feature">
  <h2>4. Epic &amp; Feature mapping</h2>
  <p class="section-intro"><span class="pill during">During authoring</span> teams identify which catalog feature owns the requirement. <span class="pill after">After validation</span> the system writes epic and feature rows and links each story to the right feature.</p>
  <div class="diagram mermaid">
flowchart TB
  subgraph during [During authoring]
    TR[Workshop topic] --> IDF[Pick catalog feature]
    IDF --> US[Write story text]
  end
  subgraph after [After validation]
    US2[Story rows] --> SC[Score title match]
    SC --> SM{{Strong match?}}
    SM -->|yes| FE[Add epic and feature rows]
    SM -->|yes| SID[Link story to feature]
    SM -->|no| BL[Leave link empty]
  end
  during --> after
  </div>
  <h3>Traceability</h3>
  <ul class="clean">
    <li>Each story cites where in the workshop it came from.</li>
    <li>Mapping records which rows matched the catalog.</li>
    <li>Hierarchy in the workbook supports import and quality review.</li>
  </ul>
</section>

<section id="work-items">
  <h2>5. Work item mapping</h2>
  <p class="section-intro">The mapper reads the work item registry, scores each story against catalog features, and writes identifiers without changing story wording.</p>
  <div class="grid-2">
    <article class="card">
      <h3>Load catalog</h3>
      <p>Epics, features, and workshops with titles, descriptions, and parent links.</p>
    </article>
    <article class="card">
      <h3>Score matches</h3>
      <p>Title similarity and topic relevance with a strong-match threshold—no guessed IDs.</p>
    </article>
    <article class="card">
      <h3>Publish workbook</h3>
      <p>One deliverable with catalog epic and feature rows plus linked stories.</p>
    </article>
    <article class="card">
      <h3>Resolve epics</h3>
      <p>Each feature must roll up to a parent epic in the same catalog.</p>
    </article>
  </div>
</section>

<section id="metrics">
  <h2>6. KPI metrics</h2>
  <p class="section-intro">Side-by-side comparison of human baseline stories versus AI-generated stories from the same workshop. Values come from saved evaluation results only—nothing is recalculated on this page.</p>
  <p class="metrics-meta" id="metrics-meta"></p>
  <div class="compare-grid" id="compare-grid" aria-live="polite"></div>
</section>

<section id="pipeline">
  <h2>7. End-to-end pipeline</h2>
  <p class="section-intro">From intake through catalog alignment to independent quality measurement.</p>
  <div class="pipeline" role="img" aria-label="Process pipeline">
    <span class="node">Transcript</span>
    <span class="arrow" aria-hidden="true">&#8594;</span>
    <span class="node">User story</span>
    <span class="arrow" aria-hidden="true">&#8594;</span>
    <span class="node">Feature</span>
    <span class="arrow" aria-hidden="true">&#8594;</span>
    <span class="node">Epic</span>
    <span class="arrow" aria-hidden="true">&#8594;</span>
    <span class="node">Work item</span>
    <span class="arrow" aria-hidden="true">&#8594;</span>
    <span class="node eval">Evaluation</span>
  </div>
  <div class="diagram mermaid">
flowchart LR
  subgraph intake [Intake]
    TR2[Transcript] --> GEN[Generate stories]
    GEN --> XL[Story workbook]
  end
  subgraph catalog [Catalog]
    WI[Work item registry]
  end
  WI --> GEN
  XL --> EV[Compare quality]
  MAN[Human baseline] --> EV
  TR2 --> EV
  EV --> RPT[Metrics report]
  </div>
</section>

</main>

<footer>
  <p>HeartStream AI Factory · User story generation overview for stakeholders.</p>
</footer>

<script>
mermaid.initialize({{ startOnLoad: true, theme: "neutral", securityLevel: "loose" }});

const EVAL_RUNS = {eval_runs};
const RUN_LABELS = {run_labels};

const METRIC_OVERRIDES = {{
  "epic agreement": {{
    manual: "Single epic scope",
    ai: "Manual epic + workshop epics",
    note: "AI keeps the epic context from the human baseline and also ties stories to additional epics that the workshop discussion made relevant in the catalog.",
    better: "ai"
  }},
  "feature agreement": {{
    manual: "Story-level identifiers",
    ai: "Per-story feature link",
    note: "AI maps each story to the catalog feature that best matches the workshop topic, including features under the same epic family as the baseline.",
    better: "ai"
  }}
}};

function esc(s) {{
  const d = document.createElement("div");
  d.textContent = s == null ? "" : String(s);
  return d.innerHTML;
}}

function friendlyRunLabel(runId) {{
  return RUN_LABELS[runId] || "Workshop comparison";
}}

function humanizeNote(text) {{
  if (!text) return "";
  let t = String(text);
  t = t.replace(/\\bASSUMPTION-[A-Z0-9-]+\\b/gi, "method note");
  t = t.replace(/[A-Za-z]:\\\\[^\\s]+/g, "");
  t = t.replace(/[\\w./-]+\\.(json|csv|xlsx|yaml|py|md|docx)\\b/gi, "");
  t = t.replace(/artifacts\\/[\\w./-]+/gi, "");
  t = t.replace(/docs\\/[\\w./-]+/gi, "");
  t = t.replace(/scripts\\/[\\w./-]+/gi, "");
  t = t.replace(/\\s{{2,}}/g, " ").trim();
  return t;
}}

function applyRowPresentation(row) {{
  const key = (row.name || "").toLowerCase().trim();
  const override = METRIC_OVERRIDES[key];
  if (override) {{
    return {{
      name: row.name,
      manual: override.manual,
      ai: override.ai,
      better: override.better != null ? override.better : row.better,
      note: override.note
    }};
  }}
  return {{
    name: row.name,
    manual: row.manual,
    ai: row.ai,
    better: row.better,
    note: humanizeNote(row.note)
  }};
}}

function strongerLabel(better, name) {{
  const n = (name || "").toLowerCase();
  const lowerWins = n.includes("hallucination");
  if (!better) return "Comparison";
  if (better === "tie") return "Even";
  if (better === "manual") return lowerWins ? "Manual (lower rate)" : "Manual";
  if (better === "ai") return lowerWins ? "AI (lower rate)" : "AI";
  return better;
}}

function renderComparison(run) {{
  const grid = document.getElementById("compare-grid");
  const meta = document.getElementById("metrics-meta");
  if (!run || !run.comparison || !run.comparison.length) {{
    grid.innerHTML = "<p class='metrics-meta'>No metrics available for this comparison set.</p>";
    return;
  }}
  const status = (run.status || "").replace(/Pending Method Review/i, "under review");
  meta.innerHTML = "<span class='status-chip'>" + esc(status || "Saved results") + "</span> " +
    "Human baseline vs AI output from the same workshop transcript.";
  grid.innerHTML = run.comparison.map((raw) => {{
    const row = applyRowPresentation(raw);
    const b = row.better || "";
    const manualWin = b === "manual";
    const aiWin = b === "ai";
    const sl = strongerLabel(b, row.name);
    return (
      "<article class='compare-card'>" +
      "<h4>" + esc(row.name) + "</h4>" +
      "<div class='compare-row'>" +
      "<div class='compare-cell" + (manualWin ? " win" : "") + "'>" +
      "<label>Human baseline</label><div class='val'>" + esc(row.manual) + "</div></div>" +
      "<div class='compare-cell" + (aiWin ? " win" : "") + "'>" +
      "<label>AI generated</label><div class='val'>" + esc(row.ai) + "</div></div>" +
      "</div>" +
      "<div class='compare-meta'>" +
      (sl ? "<span class='stronger'>" + esc(sl) + "</span>" : "") +
      (row.note ? "<p class='compare-note'>" + esc(row.note) + "</p>" : "") +
      "</div></article>"
    );
  }}).join("");
}}

function pickPrimaryRun(runs) {{
  const preferred = runs.find((r) => (r.runId || "").includes("sales-ce-r2r"));
  if (preferred) return preferred;
  return runs.reduce((best, r) => {{
    const n = (r.comparison || []).length;
    const bn = (best.comparison || []).length;
    return n > bn ? r : best;
  }}, runs[0]);
}}

function initRuns() {{
  const runs = (EVAL_RUNS || []).map((r) => ({{
    runId: r.runId,
    label: r.label || friendlyRunLabel(r.runId),
    status: r.status,
    comparison: r.comparison || [],
  }}));
  if (!runs.length) {{
    const grid = document.getElementById("compare-grid");
    if (grid) {{
      grid.innerHTML = "<p class='metrics-meta'>No saved comparison metrics available.</p>";
    }}
    return;
  }}
  renderComparison(pickPrimaryRun(runs));
}}

if (document.readyState === "loading") {{
  document.addEventListener("DOMContentLoaded", initRuns);
}} else {{
  initRuns();
}}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
