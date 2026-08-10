"""Noisy heuristic candidate generator — high recall, expects false positives.

Not truth. AI/human judge holistically against Voice DNA; marks store suppresses
already-checked smells via priority override.
"""

from __future__ import annotations

import re
from typing import Any

from voice_audit.db import EffectiveMark, should_suppress
from voice_audit.normalize import normalize_quote, quote_hash

# Soft AI-language / drift smells — candidates to check, not auto-verdicts.
PHRASE_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    (
        "let-me-explain",
        re.compile(r"\blet me explain\b", re.I),
        "AI-language candidate: 'Let me explain…' — check if in-character",
    ),
    (
        "great-question",
        re.compile(r"\bgreat question\b", re.I),
        "AI-language candidate: 'Great question!'",
    ),
    (
        "thats-a-great",
        re.compile(r"\bthat'?s a great\b", re.I),
        "AI-language candidate: 'That's a great…'",
    ),
    (
        "youve-got-this",
        re.compile(r"\byou'?ve got this\b", re.I),
        "Pep / therapy diction candidate",
    ),
    (
        "fascinating",
        re.compile(r"\bfascinating\b", re.I),
        "AI-language candidate: 'Fascinating' — often TED; check speaker",
    ),
    (
        "exactly-bang",
        re.compile(r"\bexactly!\b", re.I),
        "AI-language candidate: emphatic 'Exactly!' — may be lecturer polish",
    ),
    (
        "ten-points",
        re.compile(r"\bten points\b", re.I),
        "Sitcom-mentor candidate: 'Ten points…'",
    ),
    (
        "beautiful-waveform",
        re.compile(r"\b(waveform|flow|trace)\s+is\s+beautiful\b|\bbeautiful\b", re.I),
        "Wonder/fanboy diction candidate — check if Stuart Anti-AI tell",
    ),
    (
        "visual-guy",
        re.compile(r"\b(i'?m a visual guy|visual learner)\b", re.I),
        "Lecturer-polish candidate",
    ),
    (
        "fanboy-wow",
        re.compile(
            r"\b(wow[,!]?\s+(that'?s\s+)?(amazing|incredible|fascinating)|that'?s amazing)\b",
            re.I,
        ),
        "Fanboy wonder candidate",
    ),
    (
        "absolutely",
        re.compile(r"\babsolutely[.!]?\s*$", re.I),
        "Generic polish assent candidate",
    ),
    (
        "in-other-words",
        re.compile(r"\bin other words\b", re.I),
        "Audience over-clarify candidate",
    ),
    (
        "evolution-rnd",
        re.compile(r"\b(billion years|biological r&d|patient engineer)\b", re.I),
        "TED-closer candidate",
    ),
    (
        "mapping-inside",
        re.compile(r"\bmap(ping)? the inside\b", re.I),
        "Staccato profundity / poetry-closer candidate",
    ),
]

OIL_PHYSICS_RE = re.compile(
    r"\b("
    r"annulus|ECD|Darcy|cavitation|shut-?in|wellbore|hydrostatic|"
    r"Poiseuille|Bernoulli|Reynolds|Windkessel|permeability|"
    r"choke|mud weight|pore pressure|fracture pressure|"
    r"history matching|vapor pressure|Boyle|gravel pack"
    r")\b",
    re.I,
)

PEP_THERAPY_RE = re.compile(
    r"\b("
    r"you'?ve got this|I hear you|that must be|safe space|"
    r"honored to|journey|lean into"
    r")\b",
    re.I,
)

# Noisy on purpose — real lists often hit; whitelist after check.
PARALLEL_THREE_RE = re.compile(
    r"\b\w+(?:\s+\w+){0,3},\s+\w+(?:\s+\w+){0,3},\s+(?:and\s+)?\w+(?:\s+\w+){0,3}\b",
    re.I,
)

MARK_QUIZ_RE = re.compile(
    r"\bStuart\s*[:—-].{0,40}\b("
    r"Reynolds|Poiseuille|Bernoulli|Darcy|Boyle|Laplace|Windkessel"
    r")\b",
    re.I,
)

MARK_FORMULA_TEACH_RE = re.compile(
    r"\b(density|pressure|velocity)\s+times\b.{0,40}\bover\b",
    re.I,
)

ORPHAN_MAX_WORDS = 4
ORPHAN_SPEAKERS = {"MARK", "HAYES", "STUART"}
LANE_NO_SCIENCE = {"ELENA", "PRIYA", "OKONKWO"}
PEP_SPEAKERS = {"HAYES", "PRIYA"}
ORPHAN_ALLOW = re.compile(
    r"^(right|understood|okay|ok|good|yes|no|mm|huh|irrigate|suction|got it|"
    r"how so|keep going|same physics|lucky me|unclamp|duplex again)$",
    re.I,
)


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", text))


def looks_orphan_profundity(text: str) -> bool:
    t = text.strip().rstrip(".")
    if word_count(text) > ORPHAN_MAX_WORDS:
        return False
    return not bool(ORPHAN_ALLOW.fullmatch(t))


def scan_line(speaker: str, text: str) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []

    for hid, pattern, note in PHRASE_PATTERNS:
        if pattern.search(text):
            hits.append({"id": hid, "note": note})

    if speaker in ORPHAN_SPEAKERS and looks_orphan_profundity(text):
        hits.append(
            {
                "id": "orphan-profundity",
                "note": "Short turn candidate — check staccato profundity / Anti-AI tell",
            }
        )

    if PARALLEL_THREE_RE.search(text) and text.count(",") >= 2 and not re.search(r"\d", text):
        hits.append(
            {
                "id": "parallel-three",
                "note": "List-of-three candidate (often FP on real lists) — check polish",
            }
        )

    if speaker in LANE_NO_SCIENCE and OIL_PHYSICS_RE.search(text):
        hits.append(
            {
                "id": "lane-science",
                "note": f"{speaker} oil/physics candidate — default lane is no",
            }
        )

    if speaker in PEP_SPEAKERS and PEP_THERAPY_RE.search(text):
        hits.append(
            {
                "id": "pep-therapy",
                "note": f"{speaker} pep/therapy candidate",
            }
        )

    if speaker == "MARK" and (MARK_QUIZ_RE.search(text) or MARK_FORMULA_TEACH_RE.search(text)):
        hits.append(
            {
                "id": "mark-quiz",
                "note": "Mark quiz/formula-teach candidate — check Voice DNA (no Stuart quiz)",
            }
        )

    if speaker == "MARK" and re.search(r"\bkinetic energy\b", text, re.I):
        hits.append(
            {
                "id": "mark-kinetic",
                "note": "Mark 'kinetic energy' candidate — shop talk may prefer plain 'energy'",
            }
        )

    return hits


def annotate(
    docs: list[dict[str, Any]],
    *,
    effective: dict[tuple[str, str, str, str], EffectiveMark] | None = None,
    include_suppressed: bool = False,
) -> list[dict[str, Any]]:
    """Attach heuristic hits; optionally drop those with suppressing effective marks."""
    for doc in docs:
        file = doc.get("file", "")
        for line in doc.get("lines", []):
            speaker = line.get("speaker", "")
            text = line.get("text", "")
            qh = quote_hash(text)
            line["quote_hash"] = qh
            line["quote_norm"] = normalize_quote(text)

            hits = scan_line(speaker, text)
            kept: list[dict[str, Any]] = []
            for hit in hits:
                key = (file, speaker, qh, hit["id"])
                eff = effective.get(key) if effective else None
                if eff and should_suppress(eff) and not include_suppressed:
                    continue
                item: dict[str, Any] = dict(hit)
                if eff:
                    item["effective_mark"] = {
                        "verdict": eff.verdict,
                        "user": eff.user_name,
                        "priority": eff.user_priority,
                        "reason": eff.reason,
                    }
                kept.append(item)
            if kept:
                line["heuristics"] = kept
            else:
                line.pop("heuristics", None)
    return docs


def hits_only(docs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    trimmed: list[dict[str, Any]] = []
    for doc in docs:
        lines = [ln for ln in doc.get("lines", []) if ln.get("heuristics")]
        if lines:
            trimmed.append({"file": doc.get("file"), "lines": lines})
    return trimmed


def summary(docs: list[dict[str, Any]]) -> dict[str, Any]:
    by_heuristic: dict[str, int] = {}
    by_speaker: dict[str, int] = {}
    total = 0
    for doc in docs:
        for line in doc.get("lines", []):
            for hit in line.get("heuristics", []):
                total += 1
                by_heuristic[hit["id"]] = by_heuristic.get(hit["id"], 0) + 1
                sp = line.get("speaker", "?")
                by_speaker[sp] = by_speaker.get(sp, 0) + 1
    return {"total_hits": total, "by_heuristic": by_heuristic, "by_speaker": by_speaker}
