"""CLI: extract, scan, mark, users, disagreements."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from voice_audit import db
from voice_audit.extract import default_act_paths, extract_paths, to_markdown
from voice_audit.normalize import normalize_quote, quote_hash
from voice_audit.scan import annotate, hits_only, summary


def _repo_root(args: argparse.Namespace) -> Path:
    return args.repo_root.resolve() if args.repo_root else Path.cwd()


def _db(args: argparse.Namespace):
    path = Path(args.db) if getattr(args, "db", None) else db.default_db_path()
    conn = db.connect(path)
    db.init_db(conn)
    return conn, path


def cmd_init_db(args: argparse.Namespace) -> int:
    conn, path = _db(args)
    print(f"Initialized {path}")
    for u in db.list_users(conn):
        print(f"  user {u.name!r} priority={u.priority}")
    conn.close()
    return 0


def cmd_extract(args: argparse.Namespace) -> int:
    root = _repo_root(args)
    paths = list(args.paths) if args.paths else default_act_paths(root)
    if not paths:
        print("No act files found.", file=sys.stderr)
        return 1
    docs = extract_paths(paths, repo_root=root, by_speaker=args.by_speaker)
    if args.markdown:
        sys.stdout.write(to_markdown(docs))
    else:
        json.dump(docs, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    return 0


def cmd_scan(args: argparse.Namespace) -> int:
    root = _repo_root(args)
    conn, _ = _db(args)
    effective = None if args.ignore_marks else db.effective_marks(conn)

    if args.input:
        if args.input == "-":
            data = json.load(sys.stdin)
        else:
            data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        docs = [data] if isinstance(data, dict) else data
    else:
        paths = list(args.paths) if args.paths else default_act_paths(root)
        if not paths:
            print("No act files found.", file=sys.stderr)
            return 1
        docs = extract_paths(paths, repo_root=root, by_speaker=args.by_speaker)

    annotate(docs, effective=effective, include_suppressed=args.include_suppressed)
    out = hits_only(docs) if args.hits_only else docs

    if args.summary:
        json.dump(summary(out if args.hits_only else docs), sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    conn.close()
    return 0


def cmd_mark(args: argparse.Namespace) -> int:
    if args.verdict not in db.VERDICTS:
        print(f"Invalid verdict; choose from {sorted(db.VERDICTS)}", file=sys.stderr)
        return 1
    conn, _ = _db(args)
    qn = normalize_quote(args.quote)
    qh = quote_hash(args.quote)
    try:
        mark = db.upsert_mark(
            conn,
            file=args.file,
            speaker=args.speaker.upper(),
            quote_norm=qn,
            quote_hash=qh,
            heuristic_id=args.heuristic,
            user_name=args.user,
            verdict=args.verdict,
            reason=args.reason,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        conn.close()
        return 1
    print(
        json.dumps(
            {
                "file": mark.file,
                "speaker": mark.speaker,
                "heuristic_id": mark.heuristic_id,
                "quote_hash": mark.quote_hash,
                "user": mark.user_name,
                "priority": mark.user_priority,
                "verdict": mark.verdict,
                "reason": mark.reason,
                "marked_at": mark.marked_at,
            },
            indent=2,
        )
    )
    conn.close()
    return 0


def cmd_users(args: argparse.Namespace) -> int:
    conn, _ = _db(args)
    if args.users_cmd == "list":
        for u in db.list_users(conn):
            print(f"{u.name}\tpriority={u.priority}")
    elif args.users_cmd == "add":
        u = db.add_user(conn, args.name, args.priority)
        print(f"added {u.name!r} priority={u.priority}")
    elif args.users_cmd == "set-priority":
        u = db.set_user_priority(conn, args.name, args.priority)
        print(f"updated {u.name!r} priority={u.priority}")
    conn.close()
    return 0


def cmd_disagreements(args: argparse.Namespace) -> int:
    conn, _ = _db(args)
    rows = db.list_disagreements(conn)
    json.dump(rows, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    conn.close()
    return 0


def cmd_history(args: argparse.Namespace) -> int:
    conn, _ = _db(args)
    qh = args.quote_hash or quote_hash(args.quote)
    marks = db.history_for_key(
        conn,
        file=args.file,
        speaker=args.speaker.upper(),
        quote_hash=qh,
        heuristic_id=args.heuristic,
    )
    payload = [
        {
            "user": m.user_name,
            "priority": m.user_priority,
            "verdict": m.verdict,
            "reason": m.reason,
            "marked_at": m.marked_at,
            "quote_norm": m.quote_norm,
        }
        for m in marks
    ]
    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    conn.close()
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="voice-audit",
        description=(
            "Extract dialogue, run noisy voice-smell scan, and store marks "
            "(users + priority override). Scanner finds candidates including FPs; "
            "judgment is holistic elsewhere."
        ),
    )
    p.add_argument(
        "--db",
        default=None,
        help=f"SQLite path (default: {db.default_db_path()})",
    )
    p.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repo root for act globs (default: cwd)",
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    init = sub.add_parser("init-db", help="Create/migrate DB and seed users")
    init.set_defaults(func=cmd_init_db)

    ex = sub.add_parser("extract", help="Extract dialogue JSON/markdown")
    ex.add_argument("paths", nargs="*", type=Path)
    ex.add_argument("--by-speaker", metavar="KEY")
    ex.add_argument("--markdown", action="store_true")
    ex.set_defaults(func=cmd_extract)

    sc = sub.add_parser(
        "scan",
        help="Extract (or read JSON) + noisy heuristics; suppress via effective marks",
    )
    sc.add_argument("paths", nargs="*", type=Path, help="Act files (default: act_*.md)")
    sc.add_argument(
        "--input",
        help="Extract JSON path, or - for stdin (skips act extract)",
    )
    sc.add_argument("--by-speaker", metavar="KEY")
    sc.add_argument("--hits-only", action="store_true")
    sc.add_argument("--summary", action="store_true", help="Counts only")
    sc.add_argument(
        "--ignore-marks",
        action="store_true",
        help="Do not filter by SQLite effective marks",
    )
    sc.add_argument(
        "--include-suppressed",
        action="store_true",
        help="Keep hits even when effective mark suppresses them",
    )
    sc.set_defaults(func=cmd_scan)

    mk = sub.add_parser("mark", help="Upsert a mark for a finding key")
    mk.add_argument("--file", required=True)
    mk.add_argument("--speaker", required=True)
    mk.add_argument("--quote", required=True, help="Dialogue text (hashed for key)")
    mk.add_argument("--heuristic", required=True, help="Heuristic id, or * for whole turn")
    mk.add_argument(
        "--user",
        default="joseph",
        help="users.name (default: joseph)",
    )
    mk.add_argument(
        "--verdict",
        required=True,
        choices=sorted(db.VERDICTS),
    )
    mk.add_argument(
        "--reason",
        required=True,
        help=f"Required textual reasoning (≥{db.MIN_REASON_LEN} chars)",
    )
    mk.set_defaults(func=cmd_mark)

    us = sub.add_parser("users", help="Manage marker users / priorities")
    us_sub = us.add_subparsers(dest="users_cmd", required=True)
    us_list = us_sub.add_parser("list")
    us_list.set_defaults(func=cmd_users)
    us_add = us_sub.add_parser("add")
    us_add.add_argument("name")
    us_add.add_argument("priority", type=int)
    us_add.set_defaults(func=cmd_users)
    us_set = us_sub.add_parser("set-priority")
    us_set.add_argument("name")
    us_set.add_argument("priority", type=int)
    us_set.set_defaults(func=cmd_users)

    dis = sub.add_parser("disagreements", help="Finding keys with differing verdicts")
    dis.set_defaults(func=cmd_disagreements)

    hist = sub.add_parser("history", help="All marks for one finding key")
    hist.add_argument("--file", required=True)
    hist.add_argument("--speaker", required=True)
    hist.add_argument("--heuristic", required=True)
    g = hist.add_mutually_exclusive_group(required=True)
    g.add_argument("--quote")
    g.add_argument("--quote-hash")
    hist.set_defaults(func=cmd_history)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
