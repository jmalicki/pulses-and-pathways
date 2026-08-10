#!/usr/bin/env python3
"""Deprecated shim — use: uv run --project skills/voice-audit voice-audit extract …"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))

from voice_audit.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(["extract", *sys.argv[1:]]))
