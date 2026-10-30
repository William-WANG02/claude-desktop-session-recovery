#!/usr/bin/env python3
"""Scan and restore Claude Code desktop sessions across accounts (macOS)."""
import argparse
import datetime
import glob
import json
import os
import shutil
import sys
import time

SESSIONS = os.path.expanduser("~/Library/Application Support/Claude/claude-code-sessions")
PROJECTS = os.path.expanduser("~/.claude/projects")


def transcripts():
    return {os.path.basename(p)[:-6]: p for p in glob.glob(os.path.join(PROJECTS, "*", "*.jsonl"))}


def fmt(ts):
    if isinstance(ts, (int, float)) and ts:
        return datetime.datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d")
    return str(ts or "?")[:10]


def scan(_args):
    tx = transcripts()
    linked = set()
    for folder in sorted(glob.glob(os.path.join(SESSIONS, "*", "*"))):
        if not os.path.isdir(folder):
            continue
        rows = []
        for f in glob.glob(os.path.join(folder, "local_*.json")):
            try:
                d = json.load(open(f))
            except (OSError, ValueError):
                continue
            sid = d.get("cliSessionId") or ""
            linked.add(sid)
            rows.append((d.get("lastActivityAt") or d.get("createdAt") or 0, d, sid in tx))
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(folder)).strftime("%Y-%m-%d %H:%M")
        ok = sum(r[2] for r in rows)
        print(f"\n== {os.path.relpath(folder, SESSIONS)}  (modified {mtime}, {len(rows)} sessions, {ok} restorable)")
        for ts, d, has in sorted(rows, key=lambda r: r[0] if isinstance(r[0], (int, float)) else 0):
            flag = "OK     " if has else "MISSING"
            arch = "[archived] " if d.get("isArchived") else ""
            print(f"  {fmt(ts)}  {flag}  {arch}{d.get('title') or '(untitled)'}  |  {d.get('cwd', '')}")
    orphans = [p for sid, p in tx.items() if sid not in linked]
    print(f"\n{len(tx)} transcripts on disk; {len(orphans)} have no desktop metadata (CLI sessions, use `claude --resume`).")


def copy(args):
    src = os.path.join(SESSIONS, args.src)
    dst = os.path.join(SESSIONS, args.dst)
    for p in (src, dst):
        if not os.path.isdir(p):
            sys.exit(f"Not a folder: {p}")
    backup = os.path.join(args.backup_dir, f"claude-sessions-backup-{time.strftime('%Y%m%d-%H%M%S')}")
    shutil.copytree(dst, backup)
    print(f"Backed up destination to {backup}")
    copied = skipped = 0
    for f in glob.glob(os.path.join(src, "local_*.json")):
        target = os.path.join(dst, os.path.basename(f))
        if os.path.exists(target):
            skipped += 1
            continue
        shutil.copy2(f, target)
        copied += 1
    print(f"Copied {copied}, skipped {skipped} existing. Fully quit (Cmd+Q) and reopen Claude to see them.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("scan", help="list accounts and sessions").set_defaults(fn=scan)
    c = sub.add_parser("copy", help="copy session metadata between account/org folders")
    c.add_argument("--from", dest="src", required=True, help="<account-id>/<org-id> to copy from")
    c.add_argument("--to", dest="dst", required=True, help="<account-id>/<org-id> of the signed-in account")
    c.add_argument("--backup-dir", default=os.path.expanduser("~/Desktop"), help="where to back up the destination")
    c.set_defaults(fn=copy)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
