---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes - enforces a 4-phase root cause analysis process.
---

# Systematic Debugging

Random fixes waste time and create technical debt. Always find the root cause before patching symptoms.

## The Iron Law
**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

## The 4-Phase Process

### Phase 1: Root Cause Investigation
- **Read Errors**: Don't skim. Stack traces contain the solution.
- **Reproduce**: Trigger the failure reliably.
- **Trace**: Where does the bad value originate? Trace backward through the call chain.
- **Instrumentation**: Add logs to component boundaries to see WHERE it breaks.

### Phase 2: Pattern Analysis
- **Compare**: What works that is similar to what is broken?
- **References**: Read the relevant documentation or reference implementation COMPLETELY.

### Phase 3: Hypothesis and Testing
- **Single Hypothesis**: "I think X is the root cause because Y."
- **Test Minimally**: Make the smallest possible change to test the theory.
- **Verify**: If it didn't work, DELETE the change and form a NEW hypothesis. No shotgun debugging.

### Phase 4: Implementation
- **Failing Test**: Write a test that reproduces the bug.
- **Root Fix**: Fix the source, not the symptom.
- **Regression**: Verify all other tests still pass.

## Red Flags

- "I'll just try changing X to see if it works."
- "It's probably Y, let me patch it."
- Skipping stack traces because "I see the problem."
- Leaving failing hypotheses in the codebase.
- **Fixing symptoms instead of sources.**
