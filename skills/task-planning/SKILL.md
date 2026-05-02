---
name: task-planning
description: Responsible for in-depth problem analysis, goal breakdown, and task planning. Use when users pose complex requirements, start new projects, or need structured execution steps. This skill integrates three working modes: Fast Planning, Complete Six-Stage Solution, and Dual Role (Executor/Supervisor) Mode.
---

# Task Planning and Problem Solving

This skill integrates three working modes, automatically selected based on task complexity or specified by the user.

## Mode Selection Guide

| Complexity | Mode | Applicable Scenarios |
|:---|:---|:---|
| Low | **Fast Planning** | Feature additions, single module modifications |
| Medium | **Structured Solution** | Cross-module refactoring, experimental design and verification |
| High | **Dual Role Mode** | High-risk modifications, multi-step debugging, problems prone to trial-and-error loops |

---

## Mode A: Fast Planning

### Execution Flow
1. **Problem Analysis**: Identify core requirements, potential constraints, and technical challenges.
2. **Formulate Plan**: Break down the goal into executable atomic tasks.
3. **Produce Document**: Write the results into `plan.md`. Do not start execution immediately.
4. **Verification Loop**: Check against [ANALYSIS_FRAMEWORK.md](ANALYSIS_FRAMEWORK.md) for any missed edge cases.

### Plan Template (plan.md)

```markdown
# Task Execution Plan: [Title]

## 1. Requirement Analysis
- **Core Goal**: [Brief description of the final deliverable]
- **Scope Explanation**: [What is included and what is not]

## 2. Task Checklist
- [ ] **Phase 1: Preparation**
    - [ ] Task 1.1...
- [ ] **Phase 2: Core Development/Execution**
    - [ ] Task 2.1...
- [ ] **Phase 3: Verification and Optimization**
    - [ ] Task 3.1...

## 3. Risks and Countermeasures
- [Risk Point] -> [Prevention or Remediation Measure]
```

---

## Mode B: Structured Solution (Six Stages)

Applicable for complex tasks requiring experimental design and hypothesis verification.

### Stage 1: Clarification of Goal or Problem Cause
- Define the specific appearance of "success" or identify the core pain points of the problem.
- **Output**: A clear task definition list.

### Stage 2: Sub-project and Experimental Design
- Break down the large task into executable sub-units.
- Propose hypotheses, plan experimental parameters, define quantitative metrics.

### Stage 3: Execution and Finding Evidence
- Execute code, query data, conduct comparison tests to prove whether the hypothesis stands.

### Stage 4: Result Analysis and Evaluation
- Compare "actual results" with the "expected goals of Stage 1".
- Analyze reasons for deviations and evaluate the effectiveness of the current path.

### Stage 5: Recursive Verification Loop
- **Pattern**: Plan → Execute → Verify → Correct.
- If evaluation fails to meet the standard, revert to Stage 2 for redesign. **Max iterations: 3**.

### Stage 6: Final Report
- A complete report containing process records, correction history, final data, and conclusions.

For detailed checkpoints, please refer to [WORKFLOW.md](WORKFLOW.md).

---

## Mode C: Dual Role Mode (High-Risk Tasks)

When facing high-risk problems prone to trial-and-error loops, alternately execute the roles of "Executor" and "Supervisor".

### Role Definitions

**[Executor Mode]**:
- Write code, modify existing logic, execute scripts, decipher error messages.
- When an error occurs, provide specific repair attempts instead of just describing the problem.

**[Supervisor Mode]**:
- Define success criteria, review code, analyze problem root causes.
- Strictly check edge cases and performance issues.
- Refer to [CHECKLIST.md](CHECKLIST.md) for deep inspection.

### Collaboration Loop
1. **[Supervisor]** Define goal and plan
2. **[Executor]** Implementation and execution
3. **[Supervisor]** Strict review (against standards)
4. **[Supervisor]** Decision: if qualified output conclusion, if not analyze cause and request corrections
5. **Max Iterations: 5**, if exceeded stop and report root cause analysis

---

## Core Principles
- **Evidence-Oriented**: All conclusions must be based on collected evidence.
- **Reject Voodoo Constants**: Any parameter adjustment or logic change must have a design basis.
- **Atomization**: Ensure every task in the list can be completed in a single conversation turn.
- **Experiment Records**: When test results are involved, use the `recording-stage-progress` skill to keep records.