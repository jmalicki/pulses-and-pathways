---
name: voice-audit
description: >-
  Audits Pulses & Pathways dialogue for character voice and anti–house-AI drift
  against characters.md. Uses UV-packaged extract/scan plus SQLite marks
  (priority override). Scanner is a noisy candidate queue (FPs expected);
  judgment is holistic Voice DNA. Use when the user asks for a voice audit,
  character voice check, AI voice / anti-house-AI pass, or dialogue register review.
---

# Voice Audit (Pulses & Pathways)

Audit **spoken dialogue only** against writer notes. Do not rewrite act files unless the user explicitly asks.

**Scanner ≠ truth.** Heuristics are a high-recall candidate queue (false positives expected). Judge holistically against Voice DNA. SQLite marks record checks; higher `users.priority` overrides on disagreement; full mark history is kept.

## Authority

1. Read [`characters.md`](../../characters.md) — Anti–house-AI + Voice DNA / Do-Don't.
2. Prefer the catalog over live-script drift.
3. Skim [`case.md`](../../case.md) Team intensity / lanes when needed.
4. Compact axes: [checklist.md](checklist.md).

## Package (UV)

Canonical root: `skills/voice-audit/` (also `.cursor/skills/voice-audit/` via symlink).

```bash
cd skills/voice-audit && uv sync
# or from repo root:
uv run --project skills/voice-audit voice-audit --help
```

Dev: `uv run --project skills/voice-audit ruff check src tests` · `uv run --project skills/voice-audit pytest`

## CLI

```bash
# Seed DB (joseph priority=100, ai-voice-audit priority=10)
uv run --project skills/voice-audit voice-audit init-db

# Noisy candidates; suppresses leave-as-is/fixed/wont-fix via effective marks
uv run --project skills/voice-audit voice-audit scan act_*.md --hits-only
uv run --project skills/voice-audit voice-audit scan act_*.md --summary

# Record a mark (human or AI). Same key + different users → history; priority wins.
uv run --project skills/voice-audit voice-audit mark \
  --file act_2_pressure_and_flow.md --speaker HAYES \
  --quote "Good. Let's roll." --heuristic orphan-profundity \
  --user joseph --verdict leave-as-is --note "ops crumb"

uv run --project skills/voice-audit voice-audit disagreements
uv run --project skills/voice-audit voice-audit users list
```

DB default: `skills/voice-audit/data/marks.sqlite` (gitignored).

**Verdicts:** `leave-as-is` | `needs-fix` | `fixed` | `wont-fix`  
**Suppress from open queue when effective mark is:** leave-as-is, fixed, wont-fix.

Do **not** auto-whitelist AI `leave-as-is` unless the user asks to mark this pass.

## Workflow

1. Confirm target acts.
2. Read Voice DNA for speakers present.
3. `voice-audit scan … --hits-only` (candidates; FPs OK).
4. Holistic judgment on candidates + sample clean turns per speaker.
5. Report findings; optional rewrites. **Do not** patch acts unless asked.
6. If user wants, `mark` leave-as-is / fixed for checked items (user `joseph` or `ai-voice-audit`).

## Report schema

- File + line · Speaker · Quote · Track (`house-ai` | `character` | both)
- Guideline cite · Severity · Suggested rewrite (in-voice)
- Optional leave-as-is / whitelist note

End with per-character summary.

## Out of scope

- Stage directions / illustration prompts / science notes as “voice”
- Mechanical regex “fixes”
- Silent in-place rewrites
- Auto-filling the marks DB without user ask
