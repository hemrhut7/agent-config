---
name: requesting-code-review
description: Use when completing a task or milestone - dispatches a virtual supervisor to verify work against requirements and quality standards.
---

# Requesting Code Review

Dispatch a virtual supervisor to catch issues before they cascade. This keeps implementation focused and preserves your own context.

## When to Request
- After each task in a multi-step plan.
- After completing a major feature or bugfix.
- Before merging into the primary branch.

## How to Request

### 1. Identify Changes
```bash
# If using git
git diff HEAD~1..HEAD
```

### 2. Dispatch Supervisor
Use `invoke_agent` with name `generalist` (or `@supervisor` if available) with the following prompt:

> "You are a Senior Code Reviewer. Review the following changes against these requirements: [PASTE REQUIREMENTS].
> 
> **What to check**:
> - Plan alignment: Does it match the intent?
> - Quality: DRY, Error handling, Type safety.
> - Testing: Are tests real or just mocks?
> 
> **Output Format**:
> - Strengths: [Bullets]
> - Issues: [Critical/Important/Minor]
> - Assessment: [Ready to Merge | Fix Required]"

### 3. Act on Feedback
- Fix Critical issues immediately.
- Address Important issues before moving to the next task.

## Red Flags
- Skipping review because "it's simple."
- Ignoring Critical issues flagged by the reviewer.
- Marking a task as DONE in `plan.md` without a review pass.
