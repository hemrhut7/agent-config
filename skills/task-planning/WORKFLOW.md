# General Workflow Detailed SOP

## Stage 1: Clarify Guidance
- What problem are we trying to solve now?
- What are the specific indicators of success (e.g., code passes tests, error rate below 1%, word count meets requirements)?

## Stage 2: Design Guidance
- **Deconstruction**: If this task is a machine, what are its components?
- **Hypothesis**: If I change variable A, will result B occur?
- **Validator**: How will I "prove" this step was successful?
- **Skill Matching**: Identify which specialized skills (e.g., TDD, debugging) apply to each component.

## Stage 5: Recursive Verification Checklist
When entering this loop, the Agent should ask itself:
- [ ] Did this attempt improve the result?
- [ ] Is the cause of failure a "logic error" or an "environment configuration issue"?
- [ ] Do I need to adjust the "Goal (Stage 1)" or the "Method (Stage 2)"?

**Decision Path**:
1. **RMSE Drops**: Record success, try to optimize further.
2. **No Significant Change**: Revert current modification, look for new evidence paths.
3. **Result Worsens**: Revert immediately and re-analyze the hypothesis in Stage 2.