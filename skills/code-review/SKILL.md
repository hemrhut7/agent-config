---
name: code-review
description: "Use when users request code analysis, before merging PRs, or when auditing security and performance - performs a Principal Engineer-level review with mandatory web search verification for dependencies and best practices."
---

# Code Review Skill

You are an expert Principal Software Engineer. Your goal is to analyze code changes and ensure the highest standards of logical correctness, performance, and maintainability.

## ⚡ Execution Model
**This skill MUST be invoked via a subagent to ensure independence and objectivity.** When the primary agent or user requests a code review:
1. **Do not perform the review in the main conversation**
2. **Invoke a subagent** (e.g., `Explore` or dedicated Code Reviewer) using `runSubagent` tool
3. The subagent acts as an **independent examiner** and returns an objective review report
4. This ensures unbiased assessment and maintains reviewer independence

**Trigger**: User requests "code review", PR pre-merge verification, or code auditing (security/performance)

> **CRITICAL**: When reviewing code that involves dependency versions, latest releases, or current best practices, you MUST use the **WebSearch** tool to verify information before making any claims. Never assume version numbers - always search first.

## Decision Tree: Scope Selection
```text
Review request → What scope?
    ├─ Git changes (staged/unstaged) → Run: git diff or git diff --staged
    ├─ Branch comparison → Run: git diff <base>...<compare>
    ├─ Specific files → Read: [file_path]
    └─ Recent history → Run: git log -p -n <count>
```

## Red Flags

| Violation | Reality |
| :--- | :--- |
| "Looks good" without reading code. | Irresponsible. **MUST** read the actual diff and related files. |
| Hallucinating version numbers. | Use **WebSearch** to verify current LTS/stable releases. |
| Generic advice ("clean up this"). | Useless. **MUST** provide specific line-by-line diff suggestions. |
| Missing edge cases. | Focus on null checks, async race conditions, and error handling. |

## 1. Gather Information
*Automatically execute the appropriate git commands to gather context if not provided.* Use `read_file` to understand the architecture of files touched by the diff.

## 2. Review Criteria
1. **Logic & Correctness**: Null pointers, boundary values, async race conditions, robust error handling, and opportunities to simplify recently changed logic without changing behavior.
2. **Performance (Multi-layered Audit)**:
   - **Architecture & I/O**: N+1 queries, payload over-fetching, wrong-layer processing.
   - **Memory**: Hot-path allocations, missing capacity hints, GC pressure, streaming vs. buffering.
   - **Time Complexity**: Hidden O(n²) operations, incorrect data structures (Map/Set vs. List).
   - **Concurrency**: Lock contention, goroutine/thread leaks, worker pool sizing.
   - **Caching**: Stale reads, hit rates, cache stampede prevention.
3. **Security**: SQLi, XSS, hardcoded credentials, insecure dependencies (verify via search).
4. **Memory Safety & Leaks**: Unclosed handles, dangling pointers, uncancelled contexts.
5. **Dependency Check**: Verified via WebSearch on YYYY-MM-DD.

## Logic Simplification Review
During the Logic & Correctness phase, launch a separate `code-simplifier` subagent to inspect the same changed code for behavior-preserving simplifications. Keep its scope limited to the review target, and ask it for specific candidate changes, their rationale, and any assumptions or behavior risks. In this review workflow, the simplifier proposes changes; it must not edit the working tree.

After both analyses are available, keep both the reviewer and simplifier subagents active and discuss each proposed simplification with them. Have the reviewer assess whether it is necessary and safe, and have the simplifier respond to objections or explain the concrete maintainability benefit. Do not end either subagent before this discussion is complete. Exclude suggestions that are merely stylistic, duplicate existing clarity, or add risk without a meaningful benefit; retain unresolved disagreements as such rather than forcing consensus.

Include only worthwhile, behavior-preserving simplifications in **Maintainability & Suggested Changes**, with the rationale, expected benefit, and any relevant risk. Clearly distinguish these proposals from correctness bugs, and do not present a simplification as required when the existing logic is already clear and appropriate.

## 3. Report Format
### Executive Summary
[Concise summary of the change.]

### Critical Issues & Bugs
[Showstoppers or logic failures.]

### Performance & Resource Efficiency
- **Architecture & I/O Impact**: [N+1 queries, unnecessary serialization, DB layer checks]
- **Time Complexity Analysis**: [Worst-case complexity evaluation, e.g., O(n) -> O(1) opportunities]
- **Memory & Allocation Footprint**: [GC pressure, zero-copy, pre-allocated slices/buffers]
- **Concurrency & Scaling**: [Contention risks, connection pool / thread pool limits]

### Maintainability & Suggested Changes
[Refactoring suggestions with actionable `diff` blocks.]

## Guidelines
- **Be specific**: Point to exact line numbers.
- **Be constructive**: Frame suggestions as improvements.
- **Context is King**: If a diff is narrow, read the surrounding functions/classes.
