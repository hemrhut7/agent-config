# Deep Analysis Framework

## Thinking Dimensions

### 1. Dependency Analysis
- Which tasks must be completed first?
- Are there blocking points from external APIs or resources?

### 2. Edge Cases
- How to handle empty input data?
- Error paths for network delays or insufficient permissions?

### 3. Resource Budget
- Tokens consumption estimate: If the task is too large, do we need to split it into sub-plans?
- Time complexity: Is the algorithm optimized?
### 4. Skill Mapping
- Can any of the tasks be better handled by a specialized skill (e.g., TDD, ESKF, Git Committer)?
- Does the plan explicitly mention which skills will be used for which phases?

## Verification Checklist
- [ ] Does the plan have a "rollback mechanism"?
- [ ] Does each step have a clear Definition of Done?
- [ ] Has each task been checked for potential skill alignment?