# claude-desktop-session-recovery

A Claude Code skill that finds and restores "lost" sessions in the Claude desktop app (Code tab) on macOS.

Sessions often vanish from the sidebar after you switch accounts or organizations. Their metadata is stored per account, but the transcripts are still on disk. This skill:

- scans every account/org folder and shows which sessions still have their transcript (restorable) and which were cleaned up;
- copies session metadata into the currently signed-in account, backing up the destination first and never overwriting anything.

## Install

```bash
git clone https://github.com/William-WANG02/claude-desktop-session-recovery ~/.claude/skills/claude-desktop-session-recovery
```

Then ask Claude: "Can you recover my previous Claude Code desktop sessions?"

## Use the script directly

```bash
python3 scripts/recover_sessions.py scan
python3 scripts/recover_sessions.py copy --from <account-id>/<org-id> --to <account-id>/<org-id>
```

Fully quit (Cmd+Q) and reopen the Claude app afterwards.

## Caveats

- Unofficial. It relies on the desktop app's on-disk layout, which may change.
- Transcripts deleted by `cleanupPeriodDays` (default 30 days) can't be recovered without a backup.
- macOS only.
