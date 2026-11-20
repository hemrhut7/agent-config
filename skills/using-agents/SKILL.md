---
name: using-agents
description: Use when starting any conversation or switching to a new complex task - establishes the mandatory protocol for using the agents skill library and enforces structural discipline.
---

# Using Agents: The Master Protocol

You have a library of specialized skills in `.agents/skills/`. To ensure high-quality and consistent results, you MUST follow this protocol.

<EXTREMELY-IMPORTANT>
If there is even a 1% chance a skill might apply to your current task, you MUST invoke it.
YOU DO NOT HAVE A CHOICE. YOU CANNOT RATIONALIZE YOUR WAY OUT OF THIS.
</EXTREMELY-IMPORTANT>

## The Rule

**Check for relevant skills BEFORE ANY response or action.** Even a "simple" question might be part of a complex process that requires a skill (like `task-planning`).

### Skill Priority
1. **Process Skills** (`task-planning`, `using-agents`) - These determine HOW to approach the task.
2. **Engineering Discipline** (`.agents/rules/principle.md` Rule 2) - TDD, Systematic Debugging, and Verification Before Completion.
3. **Domain Skills** (`algorithm-error-quantizer`, `web-artifacts-builder`) - Specific task execution.

## Red Flags

If you find yourself thinking these, you are **rationalizing** away from the protocol. STOP and check for skills:

| Thought | Reality |
| :--- | :--- |
| "This is just a simple question." | Questions are tasks. Check for planning skills. |
| "I'll just do this one thing first." | Check BEFORE doing anything. |
| "I know how to do this manually." | Skills encode battle-tested patterns you might forget. |
| "The skill is overkill for this." | Complexity emerges from simplicity. Use the discipline. |
| "I'll write tests after I'm done." | **VIOLATION of TDD.** See `.agents/rules/principle.md` Rule 2. |

## Navigation & Control (High-Risk Strategies)

When working on algorithmic optimizations or high-risk logic changes, you MUST follow the recursive verification loop defined in `workflows/recursive-optimization-workflow.md`.

**Recursive Decisions**:
- **Baseline KPI** must be established before ANY logic change.
- **Residuals/Innovation** must be zero-mean white noise (if applicable).
- **Optimization Rate** must be >50% or justified.

## Mandatory First Response Protocol

Before responding to a new task:
1. **Research**: Scan `.agents/skills/` and `.agents/rules/`.
2. **Invoke**: Call `activate_skill` for the most relevant skill.
3. **Announce**: State "I am using the [Skill Name] to [Purpose]."
4. **Follow**: Create a `TodoWrite` (or similar tracker) if the skill has a checklist.
