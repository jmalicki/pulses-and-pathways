# Voice audit tooling (UV)

Python package for extract → noisy heuristic scan → SQLite marks (priority override).

```bash
cd skills/voice-audit
uv sync
uv run voice-audit --help
uv run ruff check src tests
uv run ruff format src tests
```

From repo root:

```bash
uv run --project skills/voice-audit voice-audit scan act_*.md
```

SQLite DB defaults to `data/marks.sqlite` (tracked in git). See `SKILL.md` for the agent workflow.
