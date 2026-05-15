---
name: codex
description: Use this skill to interact with the Codex CLI, an expert AI agent that can perform complex software engineering tasks, code reviews, and provide technical advice. Trigger this skill whenever the user asks to use 'codex', asks for an expert opinion on code, needs a code review, or wants to execute complex tasks that benefit from a specialized agent with deep codebase understanding.
---

# Codex Skill

This skill allows you to leverage the `codex` CLI tool to perform advanced software engineering tasks. `codex` is a powerful agent capable of understanding large codebases, providing architectural insights, and executing complex modifications.

## Core Capabilities
- **Technical Inquiries:** Ask complex technical questions or request explanations (e.g., "如何計算經緯度之間的距離").
- **Code Review:** Perform non-interactive code reviews using `codex review`.
- **Task Execution:** Execute specific instructions within the codebase using `codex exec`.

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
- **Full Auto:** Use `--full-auto` for a low-friction experience with workspace-write access.

## Examples

**Example 1: General Inquiry**
Input: Ask codex how to calculate distance between coordinates.
Action: `codex exec --skip-git-repo-check "如何計算經緯度之間的距離"`

**Example 2: Code Review**
Input: Use codex to review my recent changes.
Action: `codex review`

**Example 3: Complex Implementation**
Input: Ask codex to implement a new feature for user authentication in this project.
Action: `codex exec --full-auto "Implement JWT-based authentication in the current project following existing patterns."`

## Safety and Security
`codex` runs in a sandbox by default. Always review the commands it proposes if not using `--full-auto`. Never share secrets or credentials with the agent.
