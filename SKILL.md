---
name: claude-desktop-session-recovery
description: Find and restore missing Claude Code sessions in the Claude desktop app (Code tab) on macOS. Use when the user says their previous desktop chat history / sessions disappeared, the sidebar is empty after switching accounts or organizations, or asks whether old Claude Code desktop conversations can be recovered.
---

# Claude Desktop Session Recovery

Claude Code sessions in the desktop app are stored in two places:

| What | Where |
|------|-------|
| Session metadata (title, cwd, archived flag, link to transcript) | `~/Library/Application Support/Claude/claude-code-sessions/<account-id>/<org-id>/local_<id>.json` |
| Conversation transcript | `~/.claude/projects/<encoded-cwd>/<cliSessionId>.jsonl` |

The sidebar shows only the metadata under the **currently signed-in account/org**. Sessions usually "disappear" for one of two reasons:

1. **Signed in with a different account or org.** The metadata and transcripts are still on disk, just stored under another `<account-id>/<org-id>` folder.
2. **Transcripts were cleaned up.** Claude Code deletes old `.jsonl` transcripts after `cleanupPeriodDays` (30 days by default). The metadata may remain, but the conversation itself is gone unless there is a backup (for example Time Machine).

## Workflow

1. **Scan.** Run the scanner to list every account/org folder and each session's title, date, and whether its transcript still exists:
   ```bash
   python3 -I scripts/recover_sessions.py scan
   ```
   Find the folder of the currently signed-in account: it is the one holding the current session, usually the most recently modified. The `mcp__ccd_session_mgmt__list_sessions` tool, if you have it, shows which sessions the app currently sees.

2. **Report to the user.** Group the sessions into:
   - `OK`: the transcript exists, so the session can be restored.
   - `MISSING`: only metadata is left, so the session cannot be restored locally. Check `tmutil listbackups` or other backups.
   - CLI-only transcripts with no desktop metadata can still be resumed with `claude --resume` in their project directory.

3. **Restore.** Offer two options and let the user choose:
   - **Recommended:** sign back in to the original account. Nothing on disk changes.
   - **Copy:** copy the metadata into the current account's folder. This is unofficial and may not work in every app version:
     ```bash
     python3 -I scripts/recover_sessions.py copy --from <src-account>/<src-org> --to <dst-account>/<dst-org>
     ```
     The script backs up the destination folder first, never overwrites existing files, and leaves the source untouched.

4. **Tell the user to fully quit (⌘Q) and reopen the Claude app.** The session list is loaded at startup. If the sessions still don't appear, the app validates ownership; fall back to signing in with the original account. The backup can be copied back to undo the change.

## Notes

- Never delete or modify the source folder or any `.jsonl` transcript.
- Suggest raising `cleanupPeriodDays` in `~/.claude/settings.json` to prevent future loss.
- macOS only. Paths on other platforms differ.
