# Subagent Prompt Templates & Dispatch Examples

This document provides battle-tested subagent prompt templates and invocation patterns for common parallel engineering workloads.

---

## Template 1: Parallel Code Survey (Read-Only)

Used when investigating, comparing, or auditing multiple decoupled subsystems concurrently.

```markdown
[OBJECTIVE]:
Perform an in-depth investigation of the implementation and public interfaces of [MODULE NAME, e.g., src/network/parser.cpp].

[TASKS]:
1. Analyze the core data structures and internal data flow of this module.
2. Catalog all public APIs, exported symbols, and external dependencies.
3. Identify potential memory leaks, unprotected critical sections, or edge-case handling deficits.

[SCOPE & INPUTS]:
- Target Paths: [Explicit file paths, e.g., src/network/parser.cpp, include/network/parser.h]
- Read-Only Mode: Strictly do NOT modify any project files.

[GUARDRAILS & PROHIBITIONS]:
- Comply with all workspace rules. If temporary inspection scripts are needed, write them solely inside .agent_scratchpad/.
- Strictly avoid unapproved external network requests.

[EXPECTED DELIVERABLE]:
- Provide a structured Markdown summary:
  1. Core operational flow (with clickable file:// links to key classes/functions)
  2. External dependencies and downstream caller catalog
  3. Identified risk points and concrete refactoring suggestions
```

---

## Template 2: Parallel Feature Implementation / Refactoring

Used when implementing features or refactoring modules that touch disjoint sets of files.

```markdown
[OBJECTIVE]:
Implement telemetry payload serialization in [MODULE NAME, e.g., src/telemetry/encoder.py] and provide comprehensive unit tests.

[TASKS]:
1. Implement [FEATURE NAME] in [TARGET FILE], strictly following zero-allocation and vectorized computation principles.
2. Write unit tests in [TEST FILE, e.g., tests/test_telemetry_encoder.py], covering nominal paths and boundary conditions.
3. Run the unit test suite and verify 100% pass rate.

[SCOPE & BOUNDARIES]:
- Allowed Write Targets: [Explicit paths, e.g., src/telemetry/encoder.py, tests/test_telemetry_encoder.py]
- Strictly Forbidden: Do NOT modify repository build files (Makefile, CMakeLists.txt) or files outside your target scope.
- Global Rules Compliance:
  - Do NOT write temporary files to /tmp; use only .agent_scratchpad/.
  - Hot mechanization loops must have ZERO dynamic heap allocations (no dynamic array reallocations or append loops).
  - Do NOT automatically execute git commit or git add.

[EXPECTED DELIVERABLE]:
- Detailed list of modified files with key implementation notes.
- Terminal output logs demonstrating that unit tests pass.
- Immediate escalation if unresolvable external interface blockers arise.
```

---

## Template 3: Parallel Test Failure Triage & Bug Isolation

Used when multiple test suites or benchmarks are failing and need concurrent root-cause analysis.

```markdown
[OBJECTIVE]:
Diagnose and resolve the failure in unit test [TEST NAME, e.g., tests/unit/test_parser.py].

[TASKS]:
1. Reproduce the test failure and capture the full traceback.
2. Apply systematic debugging principles: isolate root cause rather than patching superficial test assertions.
3. Fix the underlying bug or align outdated test fixtures.
4. Re-run the test file to verify clean resolution.

[SCOPE & CONSTRAINTS]:
- Target Files: [Specific test file and its corresponding core implementation files]
- Do NOT touch unrelated test suites or peripheral modules.
- Scratch diagnostic scripts must be placed in .agent_scratchpad/.

[EXPECTED DELIVERABLE]:
- Root-cause diagnostic summary.
- Summary of modifications and code diff.
- Final terminal verification log showing test passing.
```

---

## Single-Turn Dispatch Pattern

The parent agent dispatches multiple subagents concurrently within a single conversational turn, then ends the turn to await reactive notifications:

```python
# Example: Parent agent calls invoke_subagent multiple times in a single turn

# Task 1: Survey Module A (Read-only, fast model)
invoke_subagent(
    TypeName="research",
    Role="Module A Researcher",
    Prompt="...[Apply Template 1 for Module A]...",
    Workspace="inherit",
    Model="flash"
)

# Task 2: Survey Module B (Read-only, fast model)
invoke_subagent(
    TypeName="research",
    Role="Module B Researcher",
    Prompt="...[Apply Template 1 for Module B]...",
    Workspace="inherit",
    Model="flash"
)

# Task 3: Implement decoupled feature in Module C (Isolated branch workspace)
invoke_subagent(
    TypeName="self",
    Role="Module C Implementer",
    Prompt="...[Apply Template 2 for Module C]...",
    Workspace="branch",
    Model="inherit"
)

# --> After dispatching all subagents, the parent agent terminates the turn immediately.
# System automatically triggers a Reactive Wakeup when subagents complete or send messages.
```
