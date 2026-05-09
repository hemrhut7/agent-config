---
description: This workflow is specialized for optimizing and developing mathematical models or complex algorithmic modules. It uses a "Plan-Execute-Verify-Iterate" closed-loop architecture to ensure that logic changes (e.g., sensor fusion, predictive models, data filters) meet strict quantitative benchmarks before final documentation.
---

# Unified Algorithmic Optimization & Recursive Development Workflow

This workflow is specialized for optimizing and developing mathematical models or complex algorithmic modules. It uses a "Plan-Execute-Verify-Iterate" closed-loop architecture to ensure that logic changes (e.g., sensor fusion, predictive models, data filters) meet strict quantitative benchmarks before final documentation.

---

## Stage 1: Alignment & Baseline Establishment
*Goal: Ensure consistency in the underlying logic and establish a control group.*

1. **Logic Verification**: Review `README.md` or technical specs to establish coordinate systems, sign conventions for error compensation (e.g., $\delta x$), and Jacobian/matrix definitions.
2. **Monitoring Configuration**: Insert logging points in the source code to record residuals (innovation), state covariance (confidence metrics), and estimated biases or parameters.
3. **Baseline Testing**: Run existing scripts to record pre-optimization KPIs (Key Performance Indicators) to serve as a benchmark for subsequent iterations.

---

## Stage 2: Implementation & Preliminary Integration
*Goal: Complete core logic coding and ensure system stability.*

1. **Core Development**: Implement the prediction and update equations based on mathematical derivations (e.g., state anchoring, filter updates).
2. **Unit Testing**: Perform isolated tests on mathematical modules (e.g., matrix operations, coordinate transformations) to eliminate basic computation errors.
3. **Architectural Integration**: Connect the new module to the main process, ensuring proper data alignment and timestamp synchronization (if applicable).

---

## Stage 3: Dynamic Tuning & Sensitivity Analysis
*Goal: Balance system response speed and noise suppression.*

1. **Initial Uncertainty (Initialization)**: Set initial values for the covariance matrix or error state to ensure rapid model convergence.
2. **Dynamic Noise/Random Walk**: Tune parameters for dynamic biases or state transitions to balance the flexibility of state tracking.
3. **Observation Noise**: Adjust noise parameters for each input source to optimize rejection of outliers or measurement errors.

---

## Stage 4: Automated Verification & Recursive Loop
*Goal: Determine if further optimization is needed via strict metric checks.*

1. **Execute Automated Tests**: Launch test scripts for full-scale data playback or simulation.
2. **KPI Evaluation**:
   - **Residual Stability**: Do residuals/innovation exhibit zero-mean white noise characteristics?
   - **Convergence Path**: Is the system state stable and converging rather than oscillating or diverging?
   - **Improvement Rate**: Is the error reduction or KPI improvement significant (>50% or as specified) compared to the Baseline?

3. **Recursive Decision Logic**:
   - **If KPIs are NOT met**:
     - Analyze logs to determine if it is a "Model Logic Error" or "Parameter Tuning Issue."
     - **Return to Stage 2** (Logic error) or **Stage 3** (Parameter issue) and restart the loop.
   - **If KPIs are met but optimization potential remains**:
     - Record the current best result and attempt to fine-tune parameters for peak performance, triggering verification again.
   - **If all termination conditions are met**: Proceed to Stage 5.

---

## Stage 5: Finalization & Asset Solidification
*Goal: Transform experience and mathematical derivations into team assets.*

1. **Technical Manual Update**: Document the final mathematical derivations, parameter settings, and symbol definitions used.
2. **Comparison Report**: Generate "Before vs. After" KPI charts and data to prove optimization effectiveness.

---

## Task Progress Checklist
*Use this list to track status during execution:*

```markdown
- [ ] **Stage 1**: Verified math/logic conventions and sign consistency.
- [ ] **Stage 1**: Recorded Baseline KPIs for comparison.
- [ ] **Stage 2**: Passed unit tests for core mathematical modules.
- [ ] **Stage 3**: Completed initial parameter sweep and sensitivity analysis.
- [ ] **Stage 4**: Residuals/Innovation satisfy zero-mean distribution.
- [ ] **Stage 4**: KPI improvement targets met.
- [ ] **Stage 5**: Completed final comparison report and documentation.
```
