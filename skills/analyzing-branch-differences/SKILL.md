---
name: analyzing-branch-differences
description: "Read the differences between two Git branches and perform in-depth analysis. Identify logic changes, architectural impacts, and potential risks. Trigger whenever the user asks to analyze branch differences, perform code reviews, prepare Pull Requests (PR), or track version differences."
---

# Deep Analysis of Branch Differences

## Core Rules
- **Structured Analysis**: The analysis process must cover "Logic Changes", "Breaking Changes", and "Risk Assessment".
- **Technical Precision**: Retain original technical terminology and provide in-depth discussions on modifications to algorithms or communication protocols.
- **Progressive Disclosure**: If the difference is too large, first list the files, then read specific file contents as needed.

## Deep Analysis Workflow
Please copy and execute the following checklist to ensure the completeness of the analysis:

```text
Analysis Progress:
- [ ] Step 1: Obtain branch difference list (`git diff <base>..<compare> --stat`)
- [ ] Step 2: Categorize change scope (Logic/Config/Docs)
- [ ] Step 3: Perform Deep Code Walkthrough
- [ ] Step 4: Assess architectural impacts and potential risks
- [ ] Step 5: Generate a structured analysis report (refer to [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md))
```
