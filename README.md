# claude-desktop-session-recovery

中文 | [English](README.en.md)

一个 Claude Code skill，用来找回 macOS 上 Claude 桌面端（Code 标签页）中"消失"的会话记录。

## 为什么会话会消失

桌面端的会话数据存在两个地方：

| 内容 | 位置 |
|------|------|
| 会话元信息（标题、工作目录、是否归档等） | `~/Library/Application Support/Claude/claude-code-sessions/<账号ID>/<组织ID>/local_*.json` |
| 对话内容 | `~/.claude/projects/<目录>/<会话ID>.jsonl` |

侧边栏只显示**当前登录账号/组织**目录下的会话。常见的两种情况：

1. **换了账号或组织登录**：会话和对话内容其实都还在硬盘上，只是在另一个账号的目录里，所以侧边栏是空的。**这种情况可以恢复。**
2. **对话内容被自动清理**：Claude Code 默认会删除 30 天前的对话文件（由 `cleanupPeriodDays` 控制）。这时元信息可能还在，但内容已经没了。没有 Time Machine 等备份的话，**无法恢复**。

## 功能

- **扫描**：列出所有账号/组织目录下的会话，标出哪些能恢复（`OK`）、哪些内容已丢失（`MISSING`）。
- **复制**：把旧账号的会话元信息复制到当前登录的账号下。复制前会先备份目标目录，不会覆盖任何已有文件，也不会改动原文件。

✅ 已在 macOS 版 Claude 桌面端实测（2026 年 10 月）：复制后重启应用，会话重新出现在侧边栏，对话记录完整。

## 安装

```bash
git clone https://github.com/William-WANG02/claude-desktop-session-recovery ~/.claude/skills/claude-desktop-session-recovery
```

装好后直接对 Claude 说：「帮我查一下这台电脑上之前的 Claude Code 桌面端聊天记录，能不能恢复」。

## 直接使用脚本

```bash
# 1. 扫描，找出原账号目录和当前账号目录
python3 scripts/recover_sessions.py scan

# 2. 把原账号的会话复制到当前账号
python3 scripts/recover_sessions.py copy --from <原账号ID>/<组织ID> --to <当前账号ID>/<组织ID>
```

复制完成后，用 **⌘Q 完全退出** Claude 桌面端再重新打开，会话就会出现。

如果不想改动任何文件，也可以直接退出当前账号、换回原来的账号登录。

## 防止以后丢失

在 `~/.claude/settings.json` 中调大保留天数，例如：

```json
{
  "cleanupPeriodDays": 365
}
```

## 注意事项

- 非官方工具，依赖桌面端在本地的文件结构，应用更新后可能失效。
- 已被自动清理的对话内容无法通过本工具找回。
- 仅支持 macOS。

## 许可证

MIT
