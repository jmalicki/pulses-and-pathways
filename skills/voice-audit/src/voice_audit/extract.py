"""Extract spoken dialogue from Pulses & Pathways act markdown."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

SPEAKER_ALIASES = {
    "MARK": "MARK",
    "STUART": "STUART",
    "ELENA": "ELENA",
    "PRIYA": "PRIYA",
    "PRIYA NAZARI": "PRIYA",
    "HAYES": "HAYES",
    "DR. SARAH HAYES": "HAYES",
    "SARAH HAYES": "HAYES",
    "OKONKWO": "OKONKWO",
    "DR. AMARA OKONKWO": "OKONKWO",
    "AMARA OKONKWO": "OKONKWO",
    "DR. OKONKWO": "OKONKWO",
}

INLINE_RE = re.compile(r"^\*\*(?P<label>[^*]+)\*\*:\s*(?P<rest>.*)$")
BLOCK_SPEAKER_RE = re.compile(r"^\*\*(?P<label>[^*]+)\*\*\s*$")
STAGE_ONLY_RE = re.compile(r"^\[\*([^*]|\*(?!\]))*\*\]\s*$")
STAGE_INLINE_RE = re.compile(r"\[\*([^*]|\*(?!\]))*\*\]")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
CALLOUT_START_RE = re.compile(r"^>\s*\[!NOTE\]", re.IGNORECASE)
HEADING_RE = re.compile(r"^#{1,6}\s")
HR_RE = re.compile(r"^-{3,}\s*$")


def normalize_speaker(label: str) -> str | None:
    key = " ".join(label.strip().upper().split())
    return SPEAKER_ALIASES.get(key)


def strip_inline_noise(text: str) -> str:
    text = STAGE_INLINE_RE.sub("", text)
    text = IMAGE_RE.sub("", text)
    text = HTML_COMMENT_RE.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text.strip("—- ").strip()


def is_skippable_content_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if HEADING_RE.match(s) or HR_RE.match(s):
        return True
    if s.startswith("**Characters:**") or s.startswith("* **"):
        return True
    if IMAGE_RE.match(s) or s.startswith("!["):
        return True
    if STAGE_ONLY_RE.match(s):
        return True
    if CALLOUT_START_RE.match(s) or s.startswith("> "):
        return True
    if s.startswith("$$") or s.startswith("$"):
        return True
    return bool(s.startswith("<!--"))


def extract_file(path: Path) -> dict[str, Any]:
    raw = HTML_COMMENT_RE.sub("", path.read_text(encoding="utf-8"))
    lines = raw.splitlines()

    out: list[dict[str, Any]] = []
    i = 0
    in_callout = False
    current_speaker: str | None = None
    current_start: int | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal current_speaker, current_start, buf
        if current_speaker is None or current_start is None:
            buf = []
            return
        text = strip_inline_noise(" ".join(buf))
        buf = []
        if text:
            out.append({"n": current_start, "speaker": current_speaker, "text": text})
        current_speaker = None
        current_start = None

    while i < len(lines):
        stripped = lines[i].strip()

        if CALLOUT_START_RE.match(stripped) or (in_callout and stripped.startswith(">")):
            in_callout = True
            i += 1
            continue
        if in_callout:
            if not stripped:
                in_callout = False
            i += 1
            continue

        inline = INLINE_RE.match(stripped)
        if inline:
            flush()
            speaker = normalize_speaker(inline.group("label"))
            if speaker is None:
                i += 1
                continue
            rest = strip_inline_noise(inline.group("rest"))
            current_speaker = speaker
            current_start = i + 1
            buf = [rest] if rest else []
            i += 1
            while i < len(lines):
                ns = lines[i].strip()
                if not ns:
                    break
                if INLINE_RE.match(ns) or BLOCK_SPEAKER_RE.match(ns):
                    break
                if is_skippable_content_line(ns) and not strip_inline_noise(ns):
                    i += 1
                    continue
                if is_skippable_content_line(ns):
                    if IMAGE_RE.match(ns) or STAGE_ONLY_RE.match(ns) or ns.startswith("> "):
                        i += 1
                        continue
                    break
                cleaned = strip_inline_noise(ns)
                if cleaned:
                    buf.append(cleaned)
                i += 1
            flush()
            continue

        block = BLOCK_SPEAKER_RE.match(stripped)
        if block:
            flush()
            speaker = normalize_speaker(block.group("label"))
            if speaker is None:
                i += 1
                continue
            current_speaker = speaker
            current_start = i + 1
            buf = []
            i += 1
            while i < len(lines):
                ns = lines[i].strip()
                if not ns:
                    break
                if INLINE_RE.match(ns) or BLOCK_SPEAKER_RE.match(ns):
                    break
                if CALLOUT_START_RE.match(ns) or ns.startswith("> "):
                    break
                if HEADING_RE.match(ns) or HR_RE.match(ns):
                    break
                if IMAGE_RE.match(ns) or ns.startswith("!["):
                    i += 1
                    continue
                if STAGE_ONLY_RE.match(ns):
                    i += 1
                    continue
                if ns.startswith("<!--"):
                    i += 1
                    continue
                cleaned = strip_inline_noise(ns)
                if cleaned:
                    buf.append(cleaned)
                i += 1
            flush()
            continue

        i += 1

    flush()
    return {"file": str(path), "lines": out}


def default_act_paths(repo_root: Path) -> list[Path]:
    here = sorted(repo_root.glob("act_*.md"))
    if here:
        return here
    return sorted((repo_root / "pulses-and-pathways").glob("act_*.md"))


def extract_paths(
    paths: list[Path],
    *,
    repo_root: Path,
    by_speaker: str | None = None,
) -> list[dict[str, Any]]:
    speaker_filter = by_speaker.upper() if by_speaker else None
    docs: list[dict[str, Any]] = []
    for p in paths:
        path = p if p.is_absolute() else repo_root / p
        if not path.exists():
            path = p
        if not path.exists():
            raise FileNotFoundError(p)
        doc = extract_file(path.resolve())
        try:
            doc["file"] = str(path.resolve().relative_to(repo_root.resolve()))
        except ValueError:
            doc["file"] = str(path)
        if speaker_filter:
            doc["lines"] = [ln for ln in doc["lines"] if ln["speaker"] == speaker_filter]
        docs.append(doc)
    return docs


def to_markdown(docs: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for doc in docs:
        parts.append(f"## {doc['file']}")
        for line in doc["lines"]:
            parts.append(f"- L{line['n']} **{line['speaker']}**: {line['text']}")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"
