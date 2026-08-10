"""Quote normalization and finding-key hashing for marks."""

from __future__ import annotations

import hashlib
import re

_APOS = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201b": "'",
    "\u2032": "'",
}
_QUOT = {
    "\u201c": '"',
    "\u201d": '"',
    "\u00ab": '"',
    "\u00bb": '"',
}
_DASH = {
    "\u2014": "-",
    "\u2013": "-",
    "\u2212": "-",
}


def normalize_quote(text: str) -> str:
    """Collapse whitespace; fold curly punctuation for stable keys."""
    t = text.strip()
    for src, dst in {**_APOS, **_QUOT, **_DASH}.items():
        t = t.replace(src, dst)
    t = re.sub(r"\s+", " ", t)
    return t


def quote_hash(text: str) -> str:
    norm = normalize_quote(text)
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:32]
