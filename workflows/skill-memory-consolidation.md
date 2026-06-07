---
description: Workflow for consolidating agent memory topics, refactoring specific rules to preferences, and organizing skills with progressive disclosure. Use when cleaning up the agents folder or restructuring agent configuration files.
---

# Skill and Memory Consolidation Workflow

Consolidates overlapping agent memory topics, refactors environment-specific rules to user preferences, and structures complex skills using progressive disclosure and relative paths. Use when clean-ups are needed for `/.agents/` folder files.

## Core Workflow

Please copy this checklist and track progress during execution:

Task Progress:

    [ ] Step 1: File Inventory and Reference Search

    [ ] Step 2: Consolidate Domain Topics

    [ ] Step 3: Refactor Specific Rules to User Preferences

    [ ] Step 4: Restructure Skills with Progressive Disclosure

    [ ] Step 5: Verify Changes with Unit Tests

    [ ] Step 6: Commit and Record in Version Control

### Step 1: File Inventory and Reference Search
1. Scan `skills/memory/topics/` and detect redundant, short (under 5 lines), or overlapping files.
2. Use `grep_search` to find all active code and config references targeting files planned for deletion or renaming.

### Step 2: Consolidate Domain Topics
1. Group related domain knowledge (e.g. navigation, estimation, calibration, log parsing) into a single, high-density file (e.g. `topic-navigation-estimation.md`).
2. Categorize the consolidated file's subsections by project or system layer (e.g. `INS_python` vs `ArduPilot`) to make it easily navigable.
3. Keep file length strictly under the limit (`topics/*.md` <= 100 lines). Delete the redundant source files.

### Step 3: Refactor Specific Rules to User Preferences
1. Identify general-purpose developer environment constraints (e.g. Windows/PowerShell CLI rules) buried in topics.
2. Move them to `user/preferences.md` or a global rules file so they apply globally.
3. Update any pointing paths/references (such as in `graphify/SKILL.md`) to point to the new location.

### Step 4: Restructure Skills with Progressive Disclosure
1. If multiple skills have overlapping responsibilities (e.g. `build-ardupilot-plane` and `compiling-platformio-projects`), merge them into a single integrated skill folder (e.g. `firmware-compilation/`).
2. Create a top-level `SKILL.md` index that lists triggers, and delegate specific compilation environments to nested files (`platforms/`, `troubleshooting/`).
3. Ensure all links inside the restructured skill use **relative paths** so they are portable.
4. Delete the original obsolete skill folders.

### Step 5: Verify Changes with Unit Tests
1. Run the test suite (`test_memory.py`) to verify that core actions (`recall`, `save`, `reflect`, `daily_summarize`) operate normally.
2. Adjust test fixtures or assertions as needed if they target specific file configurations.
3. Re-run tests to confirm 100% pass rates.

### Step 6: Commit and Record in Version Control
1. Run 'git-committer' skill
---

## Best Practice Guidelines
- **No Data Loss**: Before deleting any topic file, ensure its context and dates are copied and merged.
- **Portability**: Never use absolute file links (e.g., `file:///home/hank/` or `C:/`) inside skill folders.
- **Conform to Limits**: Enforce length limits (`SKILL.md` <= 60 lines, `user/preferences.md` <= 40 lines) to keep LLM context clean.
