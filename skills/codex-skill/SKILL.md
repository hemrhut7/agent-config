---
name: codex
description: Use this skill to interact with the Codex CLI, an expert AI agent that can perform complex software engineering tasks, code reviews, and provide technical advice. Trigger this skill whenever the user asks to use 'codex', asks for an expert opinion on code, needs a code review, or wants to execute complex tasks that benefit from a specialized agent with deep codebase understanding.
---

# Codex Skill

This skill allows you to leverage the `codex` CLI tool to perform advanced software engineering tasks. `codex` is a powerful agent capable of understanding large codebases, providing architectural insights, and executing complex modifications.


## Continuous Task Delegation (Session Resumption)

To allow `codex` to act as a persistent, continuous worker that remembers context across multiple codebase changes, you MUST use its session resumption features rather than background terminal processes (which block standard input).

### How to Delegate Tasks Continuously:
1. **Initial Task:** Start the work by running a standard `exec` command. This creates a new session and applies the initial changes.
   ```bash
   codex exec "[INITIAL_TASK_DESCRIPTION]"
   ```
2. **Follow-up Tasks:** When you need Codex to continue working on the same context, fix an error it made, or refine its previous changes, use the `resume --last` command to pick up exactly where it left off.
   ```bash
   codex exec resume --last "[NEXT_TASK_OR_CORRECTION]"
   ```

## Core Capabilities
- **Task Execution:** Execute complex multi-file codebase instructions using `codex exec`.
- **Contextual Memory:** Remembers previous file changes and conversation history when using `codex exec resume --last`.
- **Code Review:** Perform non-interactive code reviews using `codex review`.
- **Technical Inquiries:** Ask complex technical questions (e.g., "如何計算經緯度之間的距離").

## Usage Guidelines

### 1. General Technical Inquiries
Use `codex exec` with the `--skip-git-repo-check` flag if the inquiry is general and not specific to the current repository's code, or if you are outside a git repo.

```bash
codex exec --skip-git-repo-check "[PROMPT]"
```

### 2. Repository-Specific Tasks
When working inside a repository, you can omit `--skip-git-repo-check`. Use `codex exec` to ask about the codebase or request changes.

```bash
codex exec "[PROMPT]"
```

### 3. Code Reviews
To get a professional review of the current changes or a specific area:

```bash
codex review
```

### 4. Advanced Options
- **Model Selection:** Use `-m <MODEL>` to specify a model (e.g., `gpt-4o`, `o3-mini`).
- **Sandbox Policy:** Use `-s <SANDBOX_MODE>` (read-only, workspace-write, danger-full-access) to control permissions.

## Examples

**Example 1: Complex Implementation & Follow-up**
Input: Ask codex to implement JWT authentication, then ask it to fix a missing import it forgot.
Action 1: `codex exec "Implement JWT-based authentication in the current project following existing patterns."`
Action 2: `codex exec resume --last "You forgot to import the jwt library in auth.py, please fix it."`

**Example 2: General Inquiry**
Input: Ask codex how to calculate distance between coordinates.
Action: `codex exec --skip-git-repo-check "如何計算經緯度之間的距離"`

**Example 3: Code Review**
Input: Use codex to review my recent changes.
Action: `codex review`

## Safety and Security
`codex` runs in a sandbox by default. Always review the commands it proposes if not using `--full-auto`. Never share secrets or credentials with the agent.
