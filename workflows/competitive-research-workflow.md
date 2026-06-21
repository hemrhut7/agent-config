---
description: Manages complex problem-solving by deploying two concurrent independent subagents (Researchers A and B) to propose and implement competing solutions, with the Main Agent acting as the Supervisor to compare, evaluate, and synthesize the final outcome.
---

# Competitive Research Workflow

## 1. Overview
This workflow is designed to address complex problems by employing two independent **Researchers** (Sub-agents) to propose and implement different solutions. A **Supervisor** (Main Agent) oversees the process, evaluates progress, and synthesizes the final results. This competitive approach helps avoid logical blind spots and identifies the most effective implementation through comparative analysis.

## 2. Roles and Responsibilities

| Role | Agent Type | Primary Responsibility |
| :--- | :--- | :--- |
| **[Supervisor]** | Main Agent | Define problems, establish Baselines, review research plans, monitor progress (proactively if necessary), evaluate results, and author the final report. |
| **[Researcher A]** | Sub-agent | Propose Research Plan A (following `task-planning` standards), implement Solution A in an isolated environment, perform testing, and provide periodic/final reports. |
| **[Researcher B]** | Sub-agent | Propose Research Plan B (following `task-planning` standards), implement Solution B in an isolated environment, perform testing, and provide periodic/final reports. |

---

## 3. Workflow Stages

### Phase 0: Baseline Establishment & Problem Definition
*   **[Supervisor]** Clearly defines the phenomenon or bug to be improved.
*   **[Supervisor]** Establishes Baseline test cases and records current performance metrics (KPIs), such as RMSE, execution time, resource consumption, or bug frequency.
*   **Output**: Recorded in `[.agent_scratchpad/baseline_report.md](../../.agent_scratchpad/baseline_report.md)`.

### Phase 1: Research Proposal & Review (Task Planning Integration)
*   **[Supervisor]** Invokes two subagents using the `invoke_subagent` tool:
    - **Researcher A**: Name: `research_a`, Workspace mode: `"branch"` or `"share"` to ensure directory isolation.
    - **Researcher B**: Name: `research_b`, Workspace mode: `"branch"` or `"share"`.
*   **[Researcher A & B]** Independently propose their research plans.
*   **Standard**: Plans MUST follow the **Mode B: Structured Solution** from `[task-planning/SKILL.md](../skills/task-planning/SKILL.md)`, stored under:
    - `[.agent_scratchpad/research_plan_A.md](../../.agent_scratchpad/research_plan_A.md)`
    - `[.agent_scratchpad/research_plan_B.md](../../.agent_scratchpad/research_plan_B.md)`
*   **[Supervisor]** Reviews the plans to:
    - Ensure significant divergence between Plan A and Plan B to avoid overlap.
    - Assess feasibility and resource allocation.
    - Request adjustments if paths are too similar.

### Phase 2: Independent Research & Proactive Monitoring
*   **[Researcher A & B]** Set up their respective workspaces (branched directories).
*   **[Researcher A & B]** Submit "Progress Reports" to the Supervisor using the `send_message` tool periodically (every 5-10 steps).
*   **[Supervisor] Proactive Oversight**: If a researcher fails to report, the Supervisor MUST inspect the subagent's status/workspace using the `manage_subagents` and workspace toolsets.
*   **Output**: Saved as progress logs in `[.agent_scratchpad/progress_report_A_N.md](../../.agent_scratchpad/progress_report_A_N.md)` and `[.agent_scratchpad/progress_report_B_N.md](../../.agent_scratchpad/progress_report_B_N.md)`.

### Phase 3: Evaluation & Comparison
*   **[Researcher A & B]** Validate their implementations using the Baseline test cases from Phase 0.
*   **[Researcher A & B]** Submit their final research result reports.
*   **[Supervisor]** Compares the results of A and B, analyzing the pros and cons of each approach.
*   **Output**: Summary saved to `[.agent_scratchpad/evaluation_summary.md](../../.agent_scratchpad/evaluation_summary.md)`.

### Phase 4: Synthesis & Final Report
*   **[Supervisor]** Decides whether to adopt one solution or fuse the strengths of both based on the results.
*   **[Supervisor]** Authors the final conclusion report, including implementation recommendations and future maintenance plans.
*   **Output**: `[.agent_scratchpad/final_research_report.md](../../.agent_scratchpad/final_research_report.md)`.

---

## 4. Execution Checklist

```markdown
- [ ] **[Supervisor]** Baseline established and metrics recorded.
- [ ] **[Researcher A]** Subagent invoked and submitted Plan A under `.agent_scratchpad/`.
- [ ] **[Researcher B]** Subagent invoked and submitted Plan B under `.agent_scratchpad/`.
- [ ] **[Supervisor]** Research plans reviewed and approved for execution.
- [ ] **[Researcher A & B]** Developed in isolated workspaces without code conflicts.
- [ ] **[Supervisor]** Monitored progress and received status updates via `send_message`.
- [ ] **[Supervisor]** Comparative evaluation of results completed.
- [ ] **[Supervisor]** Final synthesis report generated under `.agent_scratchpad/`.
```
