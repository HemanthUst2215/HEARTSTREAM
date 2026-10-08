"""Semantic + fuzzy matching of user stories to indexed work items.

Scoring (0-100) blends four signals, all computed against the stemmed, stopword-free
token space with IDF weights built from the work-item corpus:

  title coverage   (0.50) IDF-weighted share of the work item's title tokens found in the story
                          (exact stem match, or fuzzy token match >= FUZZY_TOKEN_MIN)
  description cov. (0.20) same, for the highest-IDF tokens of the work item's description
  TF-IDF cosine    (0.20) semantic overlap of the full story text vs the work-item text
  title fuzzy      (0.10) token-set ratio of story title vs work-item title

Single-word work-item titles are down-weighted (they match too easily).
"""
from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from .work_items_index import (
    build_item_index,
    epic_and_feature_labels,
    load_work_items_from_directory,
    work_item_description_text,
)

TOKEN_RE = re.compile(r"[a-z0-9]+", re.I)
FUZZY_TOKEN_MIN = 0.86
DESC_TOKEN_CAP = 25
W_TITLE_COVER = 0.50
W_DESC_COVER = 0.20
W_COSINE = 0.20
W_TITLE_FUZZY = 0.10

STOPWORDS = frozenset(
    """a an and are as at be but by for from has have i if in into is it its of on or
    our so than that the their then there these they this to was we were will with
    within without who which what when where while would can could should may might
    must not no any all each per via etc also more most other such only own same
    given then user users want wants ws ce ad hoc""".split()
)


def _stem(t: str) -> str:
    if len(t) > 5 and t.endswith("ies"):
        return t[:-3] + "y"
    if len(t) > 6 and t.endswith("ing"):
        return t[:-3]
    if len(t) > 5 and t.endswith("ed"):
        return t[:-2]
    if len(t) > 5 and t.endswith("es"):
        return t[:-2]
    if len(t) > 3 and t.endswith("s") and not t.endswith("ss"):
        return t[:-1]
    return t


def tokenize(text: str) -> list[str]:
    out: list[str] = []
    for raw in TOKEN_RE.findall((text or "").lower()):
        if len(raw) < 2 or raw in STOPWORDS or raw.isdigit():
            continue
        out.append(_stem(raw))
    return out


def story_search_text(story: dict[str, Any]) -> str:
    parts = [
        story.get("title") or "",
        story.get("title") or "",  # title counted twice: strongest signal
        story.get("description") or "",
        story.get("acceptanceCriteria") or "",
        story.get("epic") or "",
        story.get("feature") or "",
        story.get("businessContext") or "",
    ]
    kw = story.get("keywords")
    if isinstance(kw, list):
        parts.extend(str(k) for k in kw)
    elif isinstance(kw, str):
        parts.append(kw)
    return " ".join(parts)


def fuzzy_ratio(a: str, b: str) -> float:
    ta = sorted(set(tokenize(a)))
    tb = sorted(set(tokenize(b)))
    if not ta or not tb:
        return 0.0
    try:
        from rapidfuzz import fuzz  # type: ignore

        return fuzz.token_set_ratio(" ".join(ta), " ".join(tb)) / 100.0
    except ImportError:
        pass
    inter = set(ta) & set(tb)
    if inter:
        base = " ".join(sorted(inter))
        s1 = SequenceMatcher(None, base, " ".join(sorted(inter) + [t for t in ta if t not in inter])).ratio()
        s2 = SequenceMatcher(None, base, " ".join(sorted(inter) + [t for t in tb if t not in inter])).ratio()
        s3 = SequenceMatcher(None, " ".join(ta), " ".join(tb)).ratio()
        return max(s1, s2, s3)
    return SequenceMatcher(None, " ".join(ta), " ".join(tb)).ratio()


class _Corpus:
    def __init__(self, items: list[dict[str, Any]]):
        self.items = items
        self.by_id = build_item_index(items)
        self.title_tokens: dict[int, list[str]] = {}
        self.desc_tokens: dict[int, list[str]] = {}
        self.full_tokens: dict[int, list[str]] = {}
        df: Counter[str] = Counter()
        for wi in items:
            wid = int(wi["workItemId"])
            tt = tokenize(wi.get("title") or "")
            dt = tokenize(work_item_description_text(wi))
            self.title_tokens[wid] = tt
            self.desc_tokens[wid] = dt
            full = tt + tt + dt
            self.full_tokens[wid] = full
            for tok in set(tt) | set(dt):
                df[tok] += 1
        n = len(items) or 1
        self.n = n
        self.df = df
        self.max_idf = math.log(n + 1) + 1.0
        for wid, dt in list(self.desc_tokens.items()):
            uniq = sorted(set(dt), key=lambda t: -self.idf(t))
            self.desc_tokens[wid] = uniq[:DESC_TOKEN_CAP]

    def idf(self, tok: str) -> float:
        d = self.df.get(tok)
        if d is None:
            return self.max_idf
        return math.log((self.n + 1) / (d + 1)) + 1.0


class _StoryProfile:
    def __init__(self, story: dict[str, Any], corpus: _Corpus):
        self.story = story
        self.tokens = tokenize(story_search_text(story))
        self.token_set = set(self.tokens)
        self.by_first: dict[str, list[str]] = defaultdict(list)
        for t in self.token_set:
            self.by_first[t[0]].append(t)
        counts = Counter(self.tokens)
        total = sum(counts.values()) or 1
        self.vec = {t: (c / total) * corpus.idf(t) for t, c in counts.items()}
        self.norm = math.sqrt(sum(v * v for v in self.vec.values())) or 1.0
        self._memo: dict[str, float] = {}

    def token_match(self, tok: str) -> float:
        if tok in self.token_set:
            return 1.0
        cached = self._memo.get(tok)
        if cached is not None:
            return cached
        best = 0.0
        if len(tok) >= 4:
            for cand in self.by_first.get(tok[0], ()):
                if abs(len(cand) - len(tok)) > 2:
                    continue
                r = SequenceMatcher(None, tok, cand).ratio()
                if r > best:
                    best = r
            if best < FUZZY_TOKEN_MIN:
                best = 0.0
        self._memo[tok] = best
        return best


def _coverage(tokens: list[str], profile: _StoryProfile, corpus: _Corpus) -> float:
    uniq = sorted(set(tokens))
    if not uniq:
        return 0.0
    num = den = 0.0
    for t in uniq:
        w = corpus.idf(t)
        den += w
        num += w * profile.token_match(t)
    return num / den if den else 0.0


def _cosine(profile: _StoryProfile, tokens: list[str], corpus: _Corpus) -> float:
    if not tokens:
        return 0.0
    counts = Counter(tokens)
    total = sum(counts.values()) or 1
    vec = {t: (c / total) * corpus.idf(t) for t, c in counts.items()}
    norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
    dot = sum(profile.vec.get(t, 0.0) * v for t, v in vec.items())
    return dot / (profile.norm * norm)


def score_story_against_item(
    profile: _StoryProfile, wid: int, corpus: _Corpus, item_title: str
) -> float:
    tt = corpus.title_tokens[wid]
    cover_title = _coverage(tt, profile, corpus)
    single_word_guard = min(1.0, len(set(tt)) / 3.0) if tt else 0.0
    cover_desc = _coverage(corpus.desc_tokens[wid], profile, corpus)
    cos = min(1.0, _cosine(profile, corpus.full_tokens[wid], corpus) / 0.5)
    title_fuzzy = fuzzy_ratio(profile.story.get("title") or "", item_title)
    raw = (
        W_TITLE_COVER * cover_title * single_word_guard
        + W_DESC_COVER * cover_desc
        + W_COSINE * cos
        + W_TITLE_FUZZY * title_fuzzy
    )
    return round(min(100.0, max(0.0, raw * 100)), 1)


def _match_profile(
    profile: _StoryProfile, corpus: _Corpus, threshold: float
) -> list[tuple[int, float]]:
    matches: list[tuple[int, float]] = []
    for wi in corpus.items:
        wid = int(wi["workItemId"])
        s = score_story_against_item(profile, wid, corpus, wi.get("title") or "")
        if s >= threshold:
            matches.append((wid, s))
    matches.sort(key=lambda x: (-x[1], x[0]))
    return matches


def _fmt_score(s: float) -> str:
    return str(int(round(s)))


def enrich_story(
    story: dict[str, Any],
    corpus: _Corpus,
    threshold: float,
) -> dict[str, Any]:
    profile = _StoryProfile(story, corpus)
    matches = _match_profile(profile, corpus, threshold)
    out = dict(story)
    # Each reference is "<WorkItemType>:<id>", e.g. Feature:67562|Workshop:68406
    out["referenceWorkItemIds"] = "|".join(
        f"{corpus.by_id[m[0]].get('workItemType') or 'WorkItem'}:{m[0]}" for m in matches
    )
    out["matchScores"] = "|".join(_fmt_score(m[1]) for m in matches)
    if matches:
        # Epic/Feature come from the best-scoring match that resolves them (Feature type preferred)
        ordered = sorted(
            matches,
            key=lambda m: (
                0 if (corpus.by_id[m[0]].get("workItemType") or "").lower() == "feature" else 1,
                -m[1],
            ),
        )
        for wid, _ in ordered:
            epic, feat = epic_and_feature_labels(corpus.by_id[wid], corpus.by_id)
            if epic or feat:
                if not out.get("epic") and epic:
                    out["epic"] = epic
                if not out.get("feature") and feat:
                    out["feature"] = feat
                if out.get("epic") and out.get("feature"):
                    break
    return out


def match_all_stories(
    stories: list[dict[str, Any]],
    work_items_dir: Path,
    threshold: float = 70.0,
) -> list[dict[str, Any]]:
    items = load_work_items_from_directory(Path(work_items_dir))
    corpus = _Corpus(items)
    return [enrich_story(s, corpus, threshold) for s in stories]
