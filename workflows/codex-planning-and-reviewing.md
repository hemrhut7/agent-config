---
description: This workflow integrates the external `codex` CLI for structured planning and code review. Agent 1 (Assistant) performs implementation while Codex acts as the Supervisor for planning and auditing.
---

# Codex Planning and Reviewing Workflow

This workflow is designed for complex tasks where structural planning and rigorous code review are required. It leverages the external `codex` tool to provide a "Supervisor" layer over the "Executor" (Agent 1).

---

## Core Directive: The Second Agent
- **Terminal Isolation**: All `codex` commands MUST be executed in a dedicated persistent terminal session (e.g., `RequestedTerminalID: "codex_agent"`). This mimics a "Second Agent" acting as a supervisor.
- **Primary Consultant**: For ANY troubleshooting, errors, or ambiguity, **Codex is the primary point of discussion**. Do not attempt local fixes or ask the user until Codex has been consulted for an analysis and a proposed solution.

---

## Stage 1: Planning with Codex
*Goal: Leverage Codex to analyze requirements and formulate a robust plan.*

1. **Invoke Codex Planning**: Agent 1 runs `codex` in the dedicated **"codex_agent"** terminal to process the `task-planning` skill.
   - **Command Example**: `codex "Follow the task-planning skill to create a plan for: [USER_REQUEST]"`
2. **Review & Solidify Plan**: Agent 1 ensures the plan is committed to the scratchpad path: `[.agent_scratchpad/plan.md](../../.agent_scratchpad/plan.md)` as per the `task-planning` skill requirements.
3. **User Approval**: Present the `[.agent_scratchpad/plan.md](../../.agent_scratchpad/plan.md)` to the user and wait for approval if required.

---

## Stage 2: Implementation & Development
*Goal: Execute the plan with precision.*

1. **Follow Plan**: Agent 1 implements the code changes following the established `[.agent_scratchpad/plan.md](../../.agent_scratchpad/plan.md)`.
2. **Standard Practices**: Adhere to TDD, Systematic Debugging, and Verification Before Completion as defined in `.agents/rules/principle.md` Rule 2.
3. **Staging**: Once a logical unit of work is completed, ensure changes are staged or clearly visible in the workspace.

---

## Stage 3: Audit & Recursive Review Loop
*Goal: Ensure code quality through external validation.*

1. **Invoke Codex Review**: Agent 1 runs the non-interactive review command in the **"codex_agent"** terminal.
   - **Command**: `codex review --uncommitted`
2. **Troubleshoot with Codex**:
   - **If issues are found**: Do not fix them immediately. Prompt Codex in the **"codex_agent"** terminal for a root cause analysis and a step-by-step fix plan.
   - **Command Example**: `codex "The review found these issues: [COPIED_RESULTS]. How should I fix these? Provide a plan."`
   - **Address Issues**: Agent 1 follows the Codex-provided fix plan.
   - **If no issues are found**: Proceed to Stage 4.
3. **Recursive Correction**: After applying fixes, **Return to Step 1** of this stage to re-verify the code. This loop continues until Codex provides a clean review.

---

## Stage 4: Finalization & Cleanup
*Goal: Wrap up the task and maintain workspace hygiene.*

1. **Verification**: Run final tests to ensure the fixes haven't introduced regressions.
2. **Cleanup**: Delete `[.agent_scratchpad/plan.md](../../.agent_scratchpad/plan.md)` and any temporary scripts as mandated by the `task-planning` skill.
3. **Final Report**: Provide the user with a summary of the work and the results of the final Codex review.

---

## Task Progress Checklist

```markdown
- [ ] **Stage 1**: Codex planning complete in dedicated terminal.
- [ ] **Stage 2**: Implementation complete according to plan.
- [ ] **Stage 3**: `codex review --uncommitted` executed.
- [ ] **Stage 3**: Issues troubleshot with Codex and resolved.
- [ ] **Stage 3**: Re-review confirmed no remaining issues (Recursive Loop closed).
- [ ] **Stage 4**: Workspace hygiene completed (cleanup of plan.md).
```
