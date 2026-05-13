---
name: universal-structured-solving
description: Execute a universal six-stage problem solving and task management workflow. Systematically complete complex tasks and produce final reports through goal clarification, experimental design, empirical execution, result evaluation, and recursive verification. Applicable to development, analysis, experiments, and decision-making scenarios.
---

# Universal Structured Problem Solving Skill (Universal Solver)

This skill transforms any complex request into a rigorous, controlled execution workflow, ensuring the task goals and final outputs are highly consistent.

## Core Workflow Outline

The Agent must sequentially execute the following stages and clearly mark stage changes:

### Stage 1: Clarification of Goal or Problem Cause
- **Goal**: Define the specific appearance of "success" or identify the core pain points of the problem.
- **Output**: A clear task definition list.

### Stage 2: Sub-project and Experimental Design
- **Goal**: Break down the large task into executable sub-units.
- **Action**: Propose hypotheses, plan experimental parameters, define quantitative metrics.

### Stage 3: Execution and Finding Evidence
- **Goal**: Implement solutions and gather physical evidence.
- **Action**: Execute code, query data, conduct comparison tests to prove whether the hypothesis stands.

### Stage 4: Result Analysis and Evaluation
- **Goal**: Compare "actual results" with the "expected goals of Stage 1".
- **Focus**: Analyze reasons for deviations and evaluate the effectiveness of the current path.

### Stage 5: Recursive Verification Loop
- **Pattern**: Plan → Execute → Verify → Correct.
- **Logic**: If Stage 4 evaluation fails to meet the standard, revert to Stage 2 for redesign until results converge.

### Stage 6: Final Report
- **Output**: A complete report containing process records, correction history, final data, and conclusions.

## Progressive Disclosure
- For detailed checklists of each stage, please refer to [WORKFLOW.md](WORKFLOW.md).

## Core Principles
- **Evidence-Oriented**: All conclusions must be based on evidence collected in Stage 3.
- **Reject Voodoo Constants**: Any parameter adjustment or logic change must have a design basis.