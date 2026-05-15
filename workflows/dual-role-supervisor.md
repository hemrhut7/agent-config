# Dual-Role Supervisor Workflow (External Agent Integration)

## 1. Overview
This workflow implements the **Dual Role Mode** from `task-planning/SKILL.md` by integrating an external `gemini` CLI instance as an independent **[Supervisor]**. This ensures objective planning, strict auditing, and prevents logical "tunnel vision" during high-risk tasks.

## 2. Roles and Responsibilities

| Role | Agent | Primary Responsibility |
|:---|:---|:---|
| **[Supervisor]** | `gemini` CLI | Goal definition, Plan auditing, Code review, Verdict (GO/NO-GO) |
| **[Executor]** | Antigravity (Current Agent) | Implementation, Script execution, Debugging, Documentation |

---

## 3. Workflow Loop

### Step 1: Initialization
- **Action**: Executor initializes a persistent session for the Supervisor.
- **Command**: `gemini --session-id "supervisor_<task_name>"` (Check `--list-sessions` first).

### Step 2: [Supervisor] Define Goal and Plan
- **Action**: Executor sends the requirements to the Supervisor.
- **Command**: 
  ```bash
  gemini -p "Context: [Project Summary]. Task: [Task Description]. 
  Role: You are the [Supervisor] defined in task-planning/SKILL.md. 
  Action: Provide a structured Goal Analysis and a Task Checklist (plan.md format)."
  ```
- **Output**: Recorded into `plan.md`.

### Step 3: [Executor] Implementation and Execution
- **Action**: Executor implements the code based on `plan.md`.
- **Constraint**: Must use `test-driven-development` and `systematic-debugging` skills.
- **Progress**: Log intermediate results using `recording-stage-progress`.

### Step 4: [Supervisor] Strict Review (The Audit)
- **Action**: Once the Executor claims "Ready", submit the code/diff to the Supervisor.
- **Command**:
  ```bash
  gemini -p "Role: [Supervisor]. 
  Input: [Code Content / Diff]. 
  Task: Audit this implementation against the original plan. 
  Check for: Edge cases, Performance, Naming consistency, and Error handling. 
  Verdict: Provide a clear 'GO' or 'NO-GO' with specific reasons."
  ```

### Step 5: Iteration (Max 5)
- **If NO-GO**: Supervisor provides specific "Correction Requests". Return to Step 3.
- **If GO**: Proceed to final verification and cleanup.

---

## 4. Interaction Commands

### To Start Supervisor:
`gemini -p "Initial Instructions"`

### To Resume/Continue Context:
`gemini -r latest -p "Next Audit Step..."`

## 5. Cleanup
- Once the task is verified (GO verdict), delete `plan.md` and any temporary scratch files.
- Persist the final "Supervisor Approval Report" in the project log if necessary.
