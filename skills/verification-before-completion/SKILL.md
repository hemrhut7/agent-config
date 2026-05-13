---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing - requires running verification commands and confirming output before making any success claims.
---

# Verification Before Completion

Claiming work is complete without fresh evidence is a failure of discipline.

## The Iron Law
**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.**

If you haven't run the verification command in the current turn, you cannot claim it passes.

## The Gate Function

BEFORE claiming status or expressing satisfaction:
1. **Identify**: What command proves this claim?
2. **Run**: Execute the FULL command (fresh).
3. **Read**: Full output, check exit code, count failures.
4. **Verify**: Does output confirm the claim?
5. **Only Then**: Make the claim with evidence.

## Red Flags
- Using "should", "probably", "seems to".
- Expressing satisfaction before verification ("Great!", "Done!").
- Trusting your own prior memory of a run.
- Skipping linter or compiler checks for "simple" changes.

## Common Failures

| Claim | Required Evidence |
| :--- | :--- |
| "Tests pass" | Test output showing 0 failures. |
| "Linter clean" | Linter output showing 0 errors. |
| "Build succeeds" | Build command exit code 0. |
| "Bug fixed" | Test that previously failed now passes. |
