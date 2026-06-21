---
name: memory
description: "Persistent cross-conversation memory system with file-based recall and automated learning. Use BEFORE starting any new task to check for prior context, after completing tasks to persist knowledge, and when errors occur to record pitfalls. Triggers on: recalling past work, saving discoveries, daily summarization, error reflection, or skill promotion. This is a Level-0 skill — it runs before all others."
---

<!-- SCOPE: Master index for the memory skill. Read this first to navigate sub-files. -->
# Memory — Agent Persistent Knowledge System

## When to Read Sub-Files
- `brain.md`: Starting a conversation — resume today's context.
- `user/preferences.md`: Composing output or choosing workflows.
- `topics/<name>.md`: When `Recall_Background` finds a match.
- `temp_skills/<name>.md`: When a generated skill is invoked.
- `archive/*`: If deep search finds no file-level match.

## Core Skills (Callable Actions)

### `Recall_Background(topic)`
Mandatory pre-task. Scans headers, reads matching file, or falls back to archive. (Script: `scripts/recall.py`)

### `Save_To_LongTerm(tags, content, storage_type)`
Persists knowledge after task completion or user corrections. (Script: `scripts/save.py`)

### `Reflect_On_Error(error_message)`
Auto-triggered on script errors to extract pitfalls. (Script: `scripts/reflect.py`)

### `Generate_New_Skill(requirement, constraints)`
Creates temp skills pending promotion after 5 runs. (Script: `scripts/promote.py`)

### `Record_Stage_Progress()`
During complex workflows, record active tasks, milestones, and results directly in `brain.md` or a progress file to maintain context.

## Automated Processes

### Daily Summarize (Auto-Execution)
At session startup (Recall_Background), the agent MUST run `python -u scripts/daily_summarize.py --check-only`. If `"due": true`, the agent MUST run `python -u scripts/daily_summarize.py` to archive the prior session, extract notes, and restore incomplete Active Tasks to the new `brain.md`.

### Line-Limit Enforcement
`SKILL.md` ≤60 | `user/preferences.md` ≤40 | `topics/*.md` ≤100. (Script: `scripts/compress.py`)

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
