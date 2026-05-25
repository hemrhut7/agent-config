---
name: task-planning
description: "Use when users pose complex requirements, start new projects, or need structured execution steps - provides multi-mode analysis (Fast, Structured, Dual Role) and enforces workspace hygiene."
---

# Task Planning and Problem Solving

## Red Flags

- Starting execution without a committed `plan.md`.
- Combining multiple complex tasks into one turn.
- Using "TBD" or placeholders in the plan.
- **Using a low-tier/flash model for Mode B or Mode C planning.** (Ensure high-reasoning models are active for complex tasks).
- **Skipping TDD or Systematic Debugging** during implementation. See `test-driven-development`.

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
5. **Skill Mapping**: Check if each task in the checklist can be proceeded with specialized skills.
6. **Cleanup**: Delete `plan.md` and any temporary scratch files (e.g., from `.agent_scratchpad/` or `scratch/`) once the task is completed and verified.

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
- Map sub-tasks to available specialized skills.

### Stage 3: Execution and Finding Evidence
- Execute code, query data, conduct comparison tests to prove whether the hypothesis stands.

### Stage 4: Result Analysis and Evaluation
- Compare "actual results" with the "expected goals of Stage 1".
- Analyze reasons for deviations and evaluate the effectiveness of the current path.

### Stage 5: Recursive Verification Loop
- **Pattern**: Plan → Execute → Verify → Correct.
- If evaluation fails to meet the standard, revert to Stage 2 for redesign. **Max iterations: 3**.

### Stage 6: Final Report and Cleanup
- A complete report containing process records, correction history, final data, and conclusions.
- **Cleanup**: Delete all temporary planning files (e.g., `plan.md`) and intermediate scratch scripts. **Crucial**: Do not remove the outputs or results (data, plots, reports) generated during the stages to allow for user review.

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
1. **[Supervisor]** Define goal and plan (including skill check for each task)
2. **[Executor]** Implementation and execution
3. **[Supervisor]** Strict review (against standards)
4. **[Supervisor]** Decision: if qualified output conclusion, if not analyze cause and request corrections
5. **Max Iterations: 5**, if exceeded stop and report root cause analysis
6. **Cleanup**: Upon reaching qualification and documenting the final solution, delete all temporary files and the execution plan.

## Codebase Research with Graphify

When a task requires analyzing the codebase architecture, finding relationships between modules, or searching for specific concepts/APIs, you should prioritize using the `graphify` knowledge graph tool:

1. **Leveraging the Graph**:
   - Use `/graphify query "<question>"` to traverse the knowledge graph and locate relevant files, functions, and cross-community relationships.
   - Use `/graphify path "ConceptA" "ConceptB"` to find shortest dependency paths between components.
   - Use `/graphify explain "Concept"` to quickly grasp the context and connections of a core abstraction.

2. **Synchronization & Quick Updates (Incremental Mode)**:
   - **Crucial Warning**: Before query or search, always check the difference between the current codebase state and the generated graphify data version (`graphify-out/graph.json` modified timestamp vs recent git commits).
   - **Quick Update**: If the codebase has changed since the last graphify run, run `/graphify --update` to perform a very fast incremental update. This only scans new/modified files, avoiding redundant LLM semantic processing and completing code-only updates deterministically using fast AST extraction with zero token cost.

---

## Core Principles
- **Evidence-Oriented**: All conclusions must be based on collected evidence.
- **Model Optimization**: For Mode B (Structured) and Mode C (Dual Role), the user should be prompted or the system should be configured to use high-tier reasoning models (e.g., Gemini 1.5 Pro) to ensure deep architectural insight. Use Flash models only for Mode A or simple script execution.
- **Reject Voodoo Constants**: Any parameter adjustment or logic change must have a design basis.
- **Atomization**: Ensure every task in the list can be completed in a single conversation turn.
- **Experiment Records**: When test results are involved, use the `recording-stage-progress` skill to keep records.
- **Skill Assessment**: After finishing the task-planning, verify if each task can be handled by existing specialized skills to ensure execution quality.
- **Workspace Hygiene**: All temporary files created for planning or execution (e.g., `plan.md`, `scratch/` scripts, or `.agent_scratchpad/`) must be deleted once the task is completed and verified. Always preserve final results, output data, and reports for user inspection.
