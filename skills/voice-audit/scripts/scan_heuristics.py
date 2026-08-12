#!/usr/bin/env python3
"""Deprecated shim — use: uv run --project skills/voice-audit voice-audit scan --input …"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))

from voice_audit.cli import main  # noqa: E402

if __name__ == "__main__":
    # Old API: scan_heuristics.py [file|-] [--hits-only]
    argv = ["scan", "--input"]
    args = sys.argv[1:]
    if not args:
        argv.append("-")
    else:
        argv.append(args[0])
        argv.extend(args[1:])
    raise SystemExit(main(argv))
