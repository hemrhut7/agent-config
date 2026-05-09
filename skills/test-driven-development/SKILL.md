---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code - enforces the RED-GREEN-REFACTOR cycle to ensure code reliability and test coverage.
---

# Test-Driven Development (TDD)

Write the test first. Watch it fail. Write minimal code to pass.

## The Iron Law
**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**

If you write code before the test: **Delete it.** Start over. No exceptions.

## Red-Green-Refactor Cycle

1. **RED**: Write a minimal failing test that demonstrates the desired behavior.
2. **Watch it Fail**: Run the test. Verify it fails for the expected reason (feature missing).
3. **GREEN**: Write the SMALLEST amount of code possible to make the test pass.
4. **Verify Green**: Run the test again. It must pass.
5. **REFACTOR**: Clean up the code while keeping tests green. Don't add features here.

## Red Flags

| Pattern | Reality |
| :--- | :--- |
| "I'll write tests after I finish." | Passing tests after-the-fact proves nothing about failure modes. |
| "This is too simple to test." | Simple code breaks too. Test takes 30 seconds. |
| "I already manually tested it." | Manual tests aren't reproducible. Automation is systematic. |
| "Deleting 1 hour of work is wasteful." | Sunk cost fallacy. Code you can't trust is technical debt. |

## Quick Checklist
- [ ] Every new function has a test.
- [ ] Watched the test fail before implementing.
- [ ] Wrote minimal code to pass.
- [ ] Output is clean (no warnings/errors).
