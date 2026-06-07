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
*   **Output**: `baseline_report.md`.

### Phase 1: Research Proposal & Review (Task Planning Integration)
*   **[Researcher A & B]** Independently propose their research plans.
*   **Standard**: Plans MUST follow the **Mode B: Structured Solution** from the `task-planning` skill, using the `plan.md` format. This includes requirement analysis, task checklists, and risk assessments.
*   **[Supervisor]** Reviews the plans to:
    *   Ensure significant divergence between Plan A and Plan B to avoid overlap.
    *   Assess feasibility and resource allocation.
    *   Request adjustments if paths are too similar.
*   **Output**: Approved `research_plan_A.md` and `research_plan_B.md`.

### Phase 2: Independent Research & Proactive Monitoring
*   **[Researcher A & B]** Set up their respective workspaces (Worktrees or independent folders).
*   **[Researcher A & B]** Submit "Progress Reports" to the Supervisor periodically (e.g., every 3-5 tool calls).
*   **[Supervisor] Proactive Oversight**: If a researcher fails to submit a report automatically, the Supervisor MUST periodically inspect the researcher's workspace, command history, and logs to verify status and ensure no "logical tunnel vision" or environment issues occur.
*   **[Supervisor]** Discusses progress with researchers, provides guidance, and corrects deviations to ensure alignment with the core goal.
*   **Output**: Multiple `progress_report_A_N.md` and `progress_report_B_N.md`.

### Phase 3: Evaluation & Comparison
*   **[Researcher A & B]** Validate their implementations using the Baseline test cases from Phase 0.
*   **[Researcher A & B]** Submit their final research result reports.
*   **[Supervisor]** Compares the results of A and B, analyzing the pros and cons of each approach.
*   **Output**: `evaluation_summary.md`.

### Phase 4: Synthesis & Final Report
*   **[Supervisor]** Decides whether to adopt one solution or fuse the strengths of both based on the results.
*   **[Supervisor]** Authors the final conclusion report, including implementation recommendations and future maintenance plans.
*   **Output**: `final_research_report.md`.

---

## 4. Execution Checklist

- [ ] **[Supervisor]** Baseline established and metrics recorded.
- [ ] **[Researcher A]** Submitted Plan A following `task-planning` standards.
- [ ] **[Researcher B]** Submitted Plan B following `task-planning` standards.
- [ ] **[Supervisor]** Research plans reviewed and approved for execution.
- [ ] **[Researcher A & B]** Developed in isolated environments without code conflicts.
- [ ] **[Supervisor]** Proactively inspected workspaces if periodic reports were missing.
- [ ] **[Supervisor]** Comparative evaluation of results completed.
- [ ] **[Supervisor]** Final synthesis report generated.
