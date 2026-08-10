---
name: voice-audit
description: >-
  Audits Pulses & Pathways dialogue for character voice and anti–house-AI drift
  against characters.md. Extracts dialogue with scripts, runs cheap heuristics,
  then reports findings with in-voice rewrite suggestions. Use when the user
  asks for a voice audit, character voice check, AI voice / anti-house-AI pass,
  or dialogue register review on act scripts.
---

# Voice Audit (Pulses & Pathways)

Audit **spoken dialogue only** against writer notes. Do not rewrite act files unless the user explicitly asks.

## Authority

1. Read [`characters.md`](../../characters.md) — Anti–house-AI kill list + each speaker’s Voice DNA / Do-Don't / example register.
2. Prefer the catalog over live-script drift when judging lines.
3. When intensity or who-speaks-when matters, skim [`case.md`](../../case.md) Team intensity and the OR ensemble lanes table in `characters.md`.
4. For a compact axis reminder, see [checklist.md](checklist.md) (pointers only — not a substitute for `characters.md`).

## Scripts (run before judging)

Canonical skill root: `skills/voice-audit/` (also available as `.cursor/skills/voice-audit/` via symlink).

```bash
# Extract dialogue from one or more acts (default: all act_*.md in repo root)
python3 skills/voice-audit/scripts/extract_dialogue.py \
  [--by-speaker MARK] [--markdown] [paths...]

# Annotate extracted JSON with cheap heuristics
python3 skills/voice-audit/scripts/scan_heuristics.py [extract.json|-]
```

Typical pipeline (from repo root):

```bash
python3 skills/voice-audit/scripts/extract_dialogue.py act_*.md \
  | python3 skills/voice-audit/scripts/scan_heuristics.py -
```

Use script output as the primary feed. Re-open the act file only for local context around a finding (stage beat, intensity). Do not load full acts into context when the extract is enough.

## Workflow

1. Confirm target (one scene, one act, or all `act_*.md`).
2. Read Anti–house-AI + Voice DNA for speakers present.
3. Run extract → heuristics via Shell.
4. Audit dialogue:
   - Start with heuristic hits (verify false positives).
   - Sample non-flagged turns per speaker for register / music / ego / lane drift.
5. Score each real finding on two tracks:
   - **house-ai** — generic polish / sameness / TED-therapy / parallel threes / over-clarify in dialogue
   - **character** — wrong Voice DNA (register, music, humor, heat, ego, lane) for that speaker
6. Emit the report. **Do not** patch acts unless asked.

## Report schema

Per finding:

- **File + line**
- **Speaker** (catalog key: `MARK` | `HAYES` | `STUART` | `ELENA` | `PRIYA` | `OKONKWO`)
- **Quote** (short)
- **Track:** `house-ai` | `character` | both
- **Guideline cite** (e.g. Mark Anti-AI tell: staccato profundity)
- **Severity:** `high` | `med` | `low`
- **Suggested rewrite** (one in-voice alternative)
- Optional: **leave-as-is** if a heuristic was a false positive

End with a short **per-character summary** (what’s working / recurring drift).

## Out of scope

- Stage directions, illustration prompts, science callouts / notes as “voice”
- Expanding Voice DNA (note catalog gaps separately if the pass reveals them)
- Silent in-place rewrites
