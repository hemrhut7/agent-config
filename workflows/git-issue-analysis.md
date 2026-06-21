---
description: Read a specific GitHub Issue, analyze related Git commits and execution results, and automatically reply with an analysis report under the issue. Use when the user requests to track issue progress or confirm the impact of code changes on an issue.
---

# Git Issue Analysis & Response Workflow

Reads a specific GitHub Issue, analyzes related Git commits and execution results, and automatically replies with an analysis report under the issue. Use when the user requests to track issue progress or confirm the impact of code changes on an issue.

## Core Workflow

Please copy this checklist and track progress during execution:

Task Progress:

    [ ] Step 1: Read Issue details and context

    [ ] Step 2: Extract key terms and retrieve Git Log

    [ ] Step 3: Analyze commit content and code differences (Diff)

    [ ] Step 4: Draft analysis report and reply to the Issue

### Step 1: Read Issue Details
Use the `github:get_issue` tool (or CLI commands) to retrieve the title, description, and existing comments of the issue. Identify the core problem to be solved.

### Step 2: Analyze Git Commits
Retrieve recent code changes related to the issue:
1. Use `git log -n 20` to view recent commit messages.
2. Search for commits containing the issue number or related keywords.
3. For key commits, use `git show <commit_hash>` or `git diff` to view actual code changes.

### Step 3: Confirm Execution Results
Based on commit content and comments, determine:
- Whether the target bug was fixed or the new feature was completed.
- Whether there are records of passed tests (e.g., CI/CD status or test output in commits).
- Whether there are remaining edge cases left unhandled.

### Step 4: Reply to Issue
Use the `github:create_issue_comment` tool (or CLI equivalent) to submit a reply. The content should be professional, concise, and follow this structure:

**Reply Template:**
> ### 🔍 Automated Analysis Report
> 
> **Related Commits:** [List short hashes or commit titles]
> **Execution Result Analysis:**
> - [Briefly describe code change points]
> - [Confirm current execution status/test results] (If applicable, reference quantification results from `[algorithm-error-quantizer/SKILL.md](../skills/algorithm-error-quantizer/SKILL.md)`)
> 
> **Conclusion:** (e.g., Fixed / Further testing required / Deployed to development environment)

---

## Best Practice Guidelines
- **Maintain Objectivity**: Analyze solely based on Git Diff and issue description; do not speculate on developer intent.
- **Reference Paths**: If specific code lines are mentioned, provide the file path.
- **Avoid Redundancy**: If the issue already contains a comment with identical information, provide a new analytical perspective or summarize only the latest progress.
