---
name: memory
description: "Persistent cross-conversation memory system with file-based recall and automated learning. Use BEFORE starting any new task to check for prior context, after completing tasks to persist knowledge, and when errors occur to record pitfalls. Triggers on: recalling past work, saving discoveries, daily summarization, error reflection, or skill promotion. This is a Level-0 skill — it runs before all others."
---

<!-- SCOPE: Master index for the memory skill. Read this first to navigate sub-files. -->
# Memory — Agent Persistent Knowledge System

## When to Read Sub-Files

| File | Read When... |
|:---|:---|
| `brain.md` | Starting a conversation — resume today's context |
| `user/preferences.md` | Composing output or choosing workflows |
| `topics/<name>.md` | `Recall_Background` finds a match |
| `temp_skills/<name>.md` | A generated skill is invoked |
| `archive/*` | Deep search finds no file-level match |

## Core Skills (Callable Actions)

### `Recall_Background(topic)`
**Mandatory before new tasks.** Scans file headers → reads matching file → falls back to archive search.
Script: `scripts/recall.py`

### `Save_To_LongTerm(tags, content, storage_type)`
Persists knowledge after task completion, user corrections, or new discoveries.
- `storage_type`: `"file"` (topics/user) | `"vector"` (archive, future) | `"auto"`
Script: `scripts/save.py`

### `Reflect_On_Error(error_message)`
Auto-triggered on script errors. Extracts pitfall patterns and persists them.
Script: `scripts/reflect.py`

### `Generate_New_Skill(requirement, constraints)`
Creates a temp skill via `skill-creator`, stores in `temp_skills/`.
After 5 successful invocations → auto-promoted to `.agents/skills/`.
Script: `scripts/promote.py`

## Automated Processes

### Daily Summarize (Time-Gated)
If >8 hours since last `brain.md` update, auto-suggest summarization.
Script: `scripts/daily_summarize.py`

### Line-Limit Enforcement
`SKILL.md` ≤60 | `user/preferences.md` ≤40 | `topics/*.md` ≤100 per file.
Script: `scripts/compress.py`

## Directory Map
```
memory/
├── SKILL.md            ← You are here
├── brain.md            ← Today's working memory
├── user/preferences.md ← Communication & work habits
├── topics/             ← Stable domain knowledge
├── temp_skills/        ← Skills pending promotion
├── archive/            ← Expired snapshots & anti-patterns
└── scripts/            ← Automation helpers
```
