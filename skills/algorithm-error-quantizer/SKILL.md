---
name: algorithm-error-quantizer
description: "Use when algorithm updates are detected or when the user asks to measure performance improvements - quantifies optimization effects (RMSE, MAE) and ensures workspace hygiene via environment restoration."
---

# Algorithm Error Quantization and Environment Management

## Core Principles
- **Accuracy First**: Prioritize error and accuracy metrics over system execution speed.
- **Zero Persistence**: Strictly prohibit submitting temporarily modified test scripts to the version control system.

## Red Flags

| Violation | Reality |
| :--- | :--- |
| Submitting temporary logs or scripts. | Pollutes repo. **MUST** restore state before reporting. |
| Using "feel" instead of metrics. | Subjective. **MUST** use quantitative improvement data. |
| Skipping baseline testing. | No comparison possible. **MUST** establish baseline first. |

## Execution Workflow

Please copy this checklist and verify step-by-step during execution:

Task Progress:

    [ ] 1. Identify algorithm changes and locate test scripts
    [ ] 2. Temporarily adjust scripts to extract error metrics (RMSE/MAE/Residuals, etc.)
    [ ] 3. Execute comparison tests (Baseline vs. Optimized)
    [ ] 4. Extract and quantify improvement data
    [ ] 5. Force environment restoration (Mandatory)

### 1. Error Quantization Process
When algorithm updates are detected, perform the following steps:
1. **Script Adjustment**: Modify the evaluation script to capture specific error metrics.
2. **Performance Comparison**: Run evaluations to obtain the "Baseline" and "Optimized" values.
3. **Data Extraction**: Calculate the improvement percentage (e.g., "Error reduced by 15%").

### 2. Environment Restoration (Mandatory Requirement)
Before completing the task and outputting the report, you **MUST** restore the environment:
- **State Restoration**: Undo all modifications made to test scripts or local files.
- **Execute Command**: Run `git restore .` or equivalent commands to ensure the workspace is completely consistent with the remote branch state.
- **Verification**: Confirm there are no uncommitted changes (Clean workspace).

## Report Format Specifications
Your reply must include the following structure:

### 📊 Algorithm Optimization Report
**Logic Change Summary**: [Briefly describe the changes]

**Quantization Results Table**:
| Metric | Baseline | Optimized | Improvement |
| :--- | :--- | :--- | :--- |
| [e.g., RMSE] | [Value] | [Value] | [▲/▼ %] |

**Environment Verification**:
- ✅ The workspace environment has been fully restored with no residual temporary modifications.
