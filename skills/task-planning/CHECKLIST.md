# Supervisor Verification Checklist

The supervisor must check item by item before approving the executor's results:

## Goal Consistency
- [ ] Did the output solve the core problem in the original User Prompt?
- [ ] Is there any irrelevant over-engineering?

## Code Quality
- [ ] Are variable names clear and consistent?
- [ ] Are potential exception conditions (Exception Handling) handled?
- [ ] Are necessary comments and explanations included?

## Logic and Performance
- [ ] Is the time/space complexity of the algorithm within an acceptable range?
- [ ] Are there hard-coded voodoo constants?

## Failure Analysis (If an error occurs)
- [ ] Was the error due to environmental issues, syntax errors, or logic paradoxes?
- [ ] Will the next repair plan avoid repeating the same mistake?