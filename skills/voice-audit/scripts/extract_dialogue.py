#!/usr/bin/env python3
"""Extract spoken dialogue from Pulses & Pathways act markdown.

Supports:
  - Inline:  **SPEAKER**: [*beat*] line…
  - Block:   **SPEAKER**\\n[*beat*]\\nline…

Strips stage directions, images, callouts, HTML comments, and pure stage lines.
Writes JSON to stdout (array of {file, lines: [{n, speaker, text}]}).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

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

# Bold speaker label alone on a line, optional trailing colon / stage already handled separately
INLINE_RE = re.compile(
    r"^\*\*(?P<label>[^*]+)\*\*:\s*(?P<rest>.*)$"
)
BLOCK_SPEAKER_RE = re.compile(
    r"^\*\*(?P<label>[^*]+)\*\*\s*$"
)
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
    # Drop leftover markdown emphasis markers used as stage wrappers already stripped
    text = re.sub(r"\s+", " ", text).strip()
    # Trim leading / trailing dashes left by stage removal
    text = text.strip("—- ").strip()
    return text


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
    if s.startswith("<!--"):
        return True
    return False


def extract_file(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    # Strip HTML comments early so they don't split turns
    raw = HTML_COMMENT_RE.sub("", raw)
    lines = raw.splitlines()

    out: list[dict] = []
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
        line = lines[i]
        stripped = line.strip()

        # Callout blocks: skip until blank line after callout content
        if CALLOUT_START_RE.match(stripped) or (
            in_callout and stripped.startswith(">")
        ):
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
            current_start = i + 1  # 1-based
            buf = [rest] if rest else []
            # Continue collecting following non-speaker content lines for same turn? Inline usually one line.
            # Peek ahead for continuation lines that aren't a new speaker / stage-only / image.
            i += 1
            while i < len(lines):
                nxt = lines[i]
                ns = nxt.strip()
                if not ns:
                    break
                if INLINE_RE.match(ns) or BLOCK_SPEAKER_RE.match(ns):
                    break
                if is_skippable_content_line(ns) and not strip_inline_noise(ns):
                    i += 1
                    continue
                if is_skippable_content_line(ns):
                    # images / stage-only — skip without ending turn
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
                nxt = lines[i]
                ns = nxt.strip()
                if not ns:
                    # blank ends turn
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
    """Prefer act_*.md in cwd; fall back to pulses-and-pathways/ for nested checkouts."""
    here = sorted(repo_root.glob("act_*.md"))
    if here:
        return here
    nested = repo_root / "pulses-and-pathways"
    return sorted(nested.glob("act_*.md"))


def to_markdown(docs: list[dict]) -> str:
    parts: list[str] = []
    for doc in docs:
        parts.append(f"## {doc['file']}")
        for line in doc["lines"]:
            parts.append(f"- L{line['n']} **{line['speaker']}**: {line['text']}")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Act markdown files (default: act_*.md in cwd)",
    )
    parser.add_argument(
        "--by-speaker",
        metavar="KEY",
        help="Filter to one catalog speaker (MARK, HAYES, …)",
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Print compact markdown instead of JSON",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repo root for default act glob (default: cwd)",
    )
    args = parser.parse_args()

    repo_root = args.repo_root or Path.cwd()
    paths = args.paths or default_act_paths(repo_root)
    if not paths:
        print("No act files found.", file=sys.stderr)
        return 1

    speaker_filter = args.by_speaker.upper() if args.by_speaker else None
    docs: list[dict] = []
    for p in paths:
        path = p if p.is_absolute() else repo_root / p
        if not path.exists():
            # also try as given relative to cwd
            path = p
        if not path.exists():
            print(f"Missing: {p}", file=sys.stderr)
            return 1
        doc = extract_file(path.resolve())
        # Prefer path relative to repo / as given for readability
        try:
            doc["file"] = str(path.resolve().relative_to(repo_root.resolve()))
        except ValueError:
            doc["file"] = str(path)
        if speaker_filter:
            doc["lines"] = [ln for ln in doc["lines"] if ln["speaker"] == speaker_filter]
        docs.append(doc)

    if args.markdown:
        sys.stdout.write(to_markdown(docs))
    else:
        json.dump(docs, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
