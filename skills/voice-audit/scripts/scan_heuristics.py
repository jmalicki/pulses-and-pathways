#!/usr/bin/env python3
"""Annotate extracted dialogue JSON with cheap voice / house-AI heuristics.

Reads extract_dialogue.py JSON from a file or stdin (-).
Writes the same structure with optional heuristics: [{id, note}] on each line.
Pattern list lives in HEURISTICS below — edit here, not in SKILL.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

# --- editable pattern list -------------------------------------------------

PHRASE_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    (
        "let-me-explain",
        re.compile(r"\blet me explain\b", re.I),
        "House-AI phrase: 'Let me explain…'",
    ),
    (
        "great-question",
        re.compile(r"\bgreat question\b", re.I),
        "House-AI phrase: 'Great question!'",
    ),
    (
        "thats-a-great",
        re.compile(r"\bthat'?s a great\b", re.I),
        "House-AI phrase: 'That's a great…'",
    ),
    (
        "youve-got-this",
        re.compile(r"\byou'?ve got this\b", re.I),
        "Pep / therapy diction",
    ),
    (
        "fanboy-wow",
        re.compile(r"\b(wow[,!]?\s+(that'?s\s+)?(amazing|incredible|fascinating)|that'?s amazing)\b", re.I),
        "Stuart Anti-AI tell: fanboy wonder",
    ),
    (
        "absolutely",
        re.compile(r"\babsolutely[.!]?\s*$", re.I),
        "Generic polish assent",
    ),
    (
        "in-other-words",
        re.compile(r"\bin other words\b", re.I),
        "Over-clarifying for the audience inside dialogue",
    ),
]

# Oil / physics terms that smell wrong in quiet-lane speakers
OIL_PHYSICS_RE = re.compile(
    r"\b("
    r"annulus|ECD|Darcy|cavitation|shut-?in|wellbore|hydrostatic|"
    r"Poiseuille|Bernoulli|Reynolds|Windkessel|permeability|"
    r"choke|mud weight|pore pressure|fracture pressure|"
    r"history matching|vapor pressure|Boyle"
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

# Rough parallel-three: three comma- or semicolon-separated short clauses / "-ing" stack
PARALLEL_THREE_RE = re.compile(
    r"\b\w+(?:\s+\w+){0,3},\s+\w+(?:\s+\w+){0,3},\s+(?:and\s+)?\w+(?:\s+\w+){0,3}\b",
    re.I,
)

ORPHAN_MAX_WORDS = 4
ORPHAN_SPEAKERS = {"MARK", "HAYES", "STUART"}
LANE_NO_SCIENCE = {"ELENA", "PRIYA", "OKONKWO"}
PEP_SPEAKERS = {"HAYES", "PRIYA"}


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", text))


def looks_orphan_profundity(text: str) -> bool:
    """Very short sole-content turn — staccato profundity smell."""
    t = text.strip().rstrip(".")
    if word_count(text) > ORPHAN_MAX_WORDS:
        return False
    # Allow pure functional assents / ops crumbs
    if re.fullmatch(
        r"(right|understood|okay|ok|good|yes|no|mm|huh|irrigate|suction|got it)",
        t,
        re.I,
    ):
        return False
    return True


def scan_line(speaker: str, text: str) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []

    for hid, pattern, note in PHRASE_PATTERNS:
        if pattern.search(text):
            hits.append({"id": hid, "note": note})

    if speaker in ORPHAN_SPEAKERS and looks_orphan_profundity(text):
        hits.append(
            {
                "id": "orphan-profundity",
                "note": "Very short standalone turn — check staccato profundity / Anti-AI tell",
            }
        )

    if PARALLEL_THREE_RE.search(text) and text.count(",") >= 2:
        # Avoid flagging clinical vitals-style lists with numbers
        if not re.search(r"\d", text):
            hits.append(
                {
                    "id": "parallel-three",
                    "note": "Possible perfect-parallel / list-of-three polish",
                }
            )

    if speaker in LANE_NO_SCIENCE and OIL_PHYSICS_RE.search(text):
        hits.append(
            {
                "id": "lane-science",
                "note": f"{speaker} speaking oil/physics — default lane is no",
            }
        )

    if speaker in PEP_SPEAKERS and PEP_THERAPY_RE.search(text):
        hits.append(
            {
                "id": "pep-therapy",
                "note": f"{speaker} pep/therapy diction — keep craft-short / factual",
            }
        )

    return hits


def annotate(docs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for doc in docs:
        for line in doc.get("lines", []):
            hits = scan_line(line.get("speaker", ""), line.get("text", ""))
            if hits:
                line["heuristics"] = hits
            else:
                line.pop("heuristics", None)
    return docs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input",
        nargs="?",
        default="-",
        help="Extract JSON path, or - for stdin",
    )
    parser.add_argument(
        "--hits-only",
        action="store_true",
        help="Emit only lines that have heuristic hits",
    )
    args = parser.parse_args()

    if args.input == "-":
        raw = sys.stdin.read()
    else:
        raw = open(args.input, encoding="utf-8").read()

    data = json.loads(raw)
    if isinstance(data, dict):
        docs = [data]
    else:
        docs = data

    annotate(docs)

    if args.hits_only:
        trimmed = []
        for doc in docs:
            lines = [ln for ln in doc.get("lines", []) if ln.get("heuristics")]
            if lines:
                trimmed.append({"file": doc.get("file"), "lines": lines})
        docs = trimmed

    json.dump(docs, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
