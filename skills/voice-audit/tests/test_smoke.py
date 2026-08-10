"""Smoke tests for normalize + extract + marks priority."""

from __future__ import annotations

from pathlib import Path

from voice_audit import db
from voice_audit.extract import extract_file
from voice_audit.normalize import quote_hash
from voice_audit.scan import annotate, scan_line


def test_quote_hash_stable():
    assert quote_hash("  hello   world ") == quote_hash("hello world")


def test_quote_hash_curly_apostrophe():
    assert quote_hash("Good. Let's roll.") == quote_hash("Good. Let’s roll.")


def test_scan_mark_quiz_candidate():
    hits = scan_line(
        "MARK",
        "That's turbulence. Stuart: Reynolds number. Density times velocity over viscosity.",
    )
    ids = {h["id"] for h in hits}
    assert "mark-quiz" in ids


def test_priority_override(tmp_path: Path):
    path = tmp_path / "marks.sqlite"
    conn = db.connect(path)
    db.init_db(conn)
    q = "Good. Let's roll."
    qh = quote_hash(q)
    db.upsert_mark(
        conn,
        file="act_0.md",
        speaker="HAYES",
        quote_norm=q,
        quote_hash=qh,
        heuristic_id="orphan-profundity",
        user_name="ai-voice-audit",
        verdict="needs-fix",
        note="AI thinks short",
    )
    db.upsert_mark(
        conn,
        file="act_0.md",
        speaker="HAYES",
        quote_norm=q,
        quote_hash=qh,
        heuristic_id="orphan-profundity",
        user_name="joseph",
        verdict="leave-as-is",
        note="ops crumb",
    )
    eff = db.effective_marks(conn)
    key = ("act_0.md", "HAYES", qh, "orphan-profundity")
    assert eff[key].verdict == "leave-as-is"
    assert eff[key].user_name == "joseph"
    disag = db.list_disagreements(conn)
    assert len(disag) == 1
    conn.close()


def test_annotate_suppresses(tmp_path: Path):
    path = tmp_path / "marks.sqlite"
    conn = db.connect(path)
    db.init_db(conn)
    text = "Fascinating. So the fluid moves."
    qh = quote_hash(text)
    db.upsert_mark(
        conn,
        file="a.md",
        speaker="HAYES",
        quote_norm=text,
        quote_hash=qh,
        heuristic_id="fascinating",
        user_name="joseph",
        verdict="leave-as-is",
    )
    docs = [{"file": "a.md", "lines": [{"n": 1, "speaker": "HAYES", "text": text}]}]
    annotate(docs, effective=db.effective_marks(conn))
    assert "heuristics" not in docs[0]["lines"][0]
    annotate(docs, effective=db.effective_marks(conn), include_suppressed=True)
    assert docs[0]["lines"][0]["heuristics"]
    conn.close()


def test_extract_act0():
    repo = Path(__file__).resolve().parents[3]
    act0 = repo / "act_0_ed_handoff.md"
    if not act0.exists():
        return
    doc = extract_file(act0)
    assert any(ln["speaker"] == "OKONKWO" for ln in doc["lines"])
