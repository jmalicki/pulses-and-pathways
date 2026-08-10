"""SQLite marks store: users with priority override, full mark history."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

VERDICTS = frozenset({"leave-as-is", "needs-fix", "fixed", "wont-fix"})
SUPPRESS_VERDICTS = frozenset({"leave-as-is", "fixed", "wont-fix"})
MIN_REASON_LEN = 12

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  priority INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS marks (
  id INTEGER PRIMARY KEY,
  file TEXT NOT NULL,
  speaker TEXT NOT NULL,
  quote_norm TEXT NOT NULL,
  quote_hash TEXT NOT NULL,
  heuristic_id TEXT NOT NULL,
  user_id INTEGER NOT NULL REFERENCES users(id),
  verdict TEXT NOT NULL,
  reason TEXT NOT NULL,
  marked_at TEXT NOT NULL,
  UNIQUE (file, speaker, quote_hash, heuristic_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_marks_key
  ON marks (file, speaker, quote_hash, heuristic_id);
"""

DEFAULT_USERS = (
    ("joseph", 100),
    ("ai-voice-audit", 10),
)


@dataclass(frozen=True)
class User:
    id: int
    name: str
    priority: int


@dataclass(frozen=True)
class Mark:
    id: int
    file: str
    speaker: str
    quote_norm: str
    quote_hash: str
    heuristic_id: str
    user_id: int
    user_name: str
    user_priority: int
    verdict: str
    reason: str
    marked_at: str


@dataclass(frozen=True)
class EffectiveMark:
    file: str
    speaker: str
    quote_hash: str
    heuristic_id: str
    verdict: str
    user_name: str
    user_priority: int
    reason: str
    marked_at: str


def default_db_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "marks.sqlite"


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or default_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _migrate(conn: sqlite3.Connection) -> None:
    """Rename legacy marks.note → reason if needed."""
    tables = {
        r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    }
    if "marks" not in tables:
        return
    cols = {r[1] for r in conn.execute("PRAGMA table_info(marks)").fetchall()}
    if "note" in cols and "reason" not in cols:
        conn.execute("ALTER TABLE marks RENAME COLUMN note TO reason")
        conn.commit()


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    _migrate(conn)
    for name, priority in DEFAULT_USERS:
        conn.execute(
            """
            INSERT INTO users (name, priority) VALUES (?, ?)
            ON CONFLICT(name) DO UPDATE SET priority = excluded.priority
            """,
            (name, priority),
        )
    conn.commit()


def get_user(conn: sqlite3.Connection, name: str) -> User:
    row = conn.execute("SELECT id, name, priority FROM users WHERE name = ?", (name,)).fetchone()
    if row is None:
        raise KeyError(f"Unknown user: {name!r}. Add with: voice-audit users add …")
    return User(id=row["id"], name=row["name"], priority=row["priority"])


def list_users(conn: sqlite3.Connection) -> list[User]:
    rows = conn.execute(
        "SELECT id, name, priority FROM users ORDER BY priority DESC, name"
    ).fetchall()
    return [User(id=r["id"], name=r["name"], priority=r["priority"]) for r in rows]


def add_user(conn: sqlite3.Connection, name: str, priority: int) -> User:
    conn.execute(
        "INSERT INTO users (name, priority) VALUES (?, ?)",
        (name, priority),
    )
    conn.commit()
    return get_user(conn, name)


def set_user_priority(conn: sqlite3.Connection, name: str, priority: int) -> User:
    conn.execute("UPDATE users SET priority = ? WHERE name = ?", (priority, name))
    conn.commit()
    return get_user(conn, name)


def normalize_reason(reason: str) -> str:
    return " ".join(reason.split()).strip()


def require_reason(reason: str) -> str:
    text = normalize_reason(reason)
    if len(text) < MIN_REASON_LEN:
        raise ValueError(
            f"Mark requires textual reasoning (≥{MIN_REASON_LEN} chars after trim); "
            f"got {len(text)} chars."
        )
    return text


def upsert_mark(
    conn: sqlite3.Connection,
    *,
    file: str,
    speaker: str,
    quote_norm: str,
    quote_hash: str,
    heuristic_id: str,
    user_name: str,
    verdict: str,
    reason: str,
) -> Mark:
    if verdict not in VERDICTS:
        raise ValueError(f"Invalid verdict {verdict!r}; expected one of {sorted(VERDICTS)}")
    reason = require_reason(reason)
    user = get_user(conn, user_name)
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    conn.execute(
        """
        INSERT INTO marks (
          file, speaker, quote_norm, quote_hash, heuristic_id,
          user_id, verdict, reason, marked_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(file, speaker, quote_hash, heuristic_id, user_id) DO UPDATE SET
          quote_norm = excluded.quote_norm,
          verdict = excluded.verdict,
          reason = excluded.reason,
          marked_at = excluded.marked_at
        """,
        (
            file,
            speaker,
            quote_norm,
            quote_hash,
            heuristic_id,
            user.id,
            verdict,
            reason,
            now,
        ),
    )
    conn.commit()
    row = conn.execute(
        """
        SELECT m.*, u.name AS user_name, u.priority AS user_priority
        FROM marks m JOIN users u ON u.id = m.user_id
        WHERE m.file = ? AND m.speaker = ? AND m.quote_hash = ?
          AND m.heuristic_id = ? AND m.user_id = ?
        """,
        (file, speaker, quote_hash, heuristic_id, user.id),
    ).fetchone()
    return _row_to_mark(row)


def _row_reason(row: sqlite3.Row) -> str:
    keys = row.keys()
    if "reason" in keys:
        return row["reason"]
    return row["note"]


def _row_to_mark(row: sqlite3.Row) -> Mark:
    return Mark(
        id=row["id"],
        file=row["file"],
        speaker=row["speaker"],
        quote_norm=row["quote_norm"],
        quote_hash=row["quote_hash"],
        heuristic_id=row["heuristic_id"],
        user_id=row["user_id"],
        user_name=row["user_name"],
        user_priority=row["user_priority"],
        verdict=row["verdict"],
        reason=_row_reason(row),
        marked_at=row["marked_at"],
    )


def effective_marks(conn: sqlite3.Connection) -> dict[tuple[str, str, str, str], EffectiveMark]:
    """Map finding key → effective mark (highest user priority; tie → newest)."""
    rows = conn.execute(
        """
        SELECT m.*, u.name AS user_name, u.priority AS user_priority
        FROM marks m
        JOIN users u ON u.id = m.user_id
        ORDER BY u.priority DESC, m.marked_at DESC, m.id DESC
        """
    ).fetchall()
    out: dict[tuple[str, str, str, str], EffectiveMark] = {}
    for row in rows:
        key = (row["file"], row["speaker"], row["quote_hash"], row["heuristic_id"])
        if key in out:
            continue
        out[key] = EffectiveMark(
            file=row["file"],
            speaker=row["speaker"],
            quote_hash=row["quote_hash"],
            heuristic_id=row["heuristic_id"],
            verdict=row["verdict"],
            user_name=row["user_name"],
            user_priority=row["user_priority"],
            reason=_row_reason(row),
            marked_at=row["marked_at"],
        )
    return out


def should_suppress(effective: EffectiveMark | None) -> bool:
    return effective is not None and effective.verdict in SUPPRESS_VERDICTS


def list_disagreements(conn: sqlite3.Connection) -> list[dict]:
    """Finding keys where ≥2 users have different verdicts."""
    rows = conn.execute(
        """
        SELECT file, speaker, quote_hash, heuristic_id,
               GROUP_CONCAT(DISTINCT verdict) AS verdicts,
               COUNT(DISTINCT user_id) AS n_users,
               COUNT(DISTINCT verdict) AS n_verdicts
        FROM marks
        GROUP BY file, speaker, quote_hash, heuristic_id
        HAVING n_verdicts > 1
        ORDER BY file, speaker, heuristic_id
        """
    ).fetchall()
    results: list[dict] = []
    for row in rows:
        marks = conn.execute(
            """
            SELECT m.*, u.name AS user_name, u.priority
            FROM marks m JOIN users u ON u.id = m.user_id
            WHERE m.file = ? AND m.speaker = ? AND m.quote_hash = ? AND m.heuristic_id = ?
            ORDER BY u.priority DESC, m.marked_at DESC
            """,
            (row["file"], row["speaker"], row["quote_hash"], row["heuristic_id"]),
        ).fetchall()
        quote = conn.execute(
            """
            SELECT quote_norm FROM marks
            WHERE file = ? AND speaker = ? AND quote_hash = ? AND heuristic_id = ?
            LIMIT 1
            """,
            (row["file"], row["speaker"], row["quote_hash"], row["heuristic_id"]),
        ).fetchone()
        results.append(
            {
                "file": row["file"],
                "speaker": row["speaker"],
                "quote_hash": row["quote_hash"],
                "heuristic_id": row["heuristic_id"],
                "quote_norm": quote["quote_norm"] if quote else "",
                "marks": [
                    {
                        "user": m["user_name"],
                        "priority": m["priority"],
                        "verdict": m["verdict"],
                        "reason": _row_reason(m),
                        "marked_at": m["marked_at"],
                    }
                    for m in marks
                ],
            }
        )
    return results


def history_for_key(
    conn: sqlite3.Connection,
    *,
    file: str,
    speaker: str,
    quote_hash: str,
    heuristic_id: str,
) -> list[Mark]:
    rows = conn.execute(
        """
        SELECT m.*, u.name AS user_name, u.priority AS user_priority
        FROM marks m JOIN users u ON u.id = m.user_id
        WHERE m.file = ? AND m.speaker = ? AND m.quote_hash = ? AND m.heuristic_id = ?
        ORDER BY u.priority DESC, m.marked_at DESC
        """,
        (file, speaker, quote_hash, heuristic_id),
    ).fetchall()
    return [_row_to_mark(r) for r in rows]
