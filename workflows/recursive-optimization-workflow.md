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

## Stage 4: Agent-Driven Automated Verification & Recursive Loop
*Goal: Leverage an autonomous subagent to continuously execute, evaluate, and optimize parameters/logic in a closed loop until strict quantitative KPIs are achieved.*

1. **Deploy Autonomous Optimization Agent (Subagent)**:
   - Define or invoke a `self` subagent (or specialized optimizer) specifically tasked with driving the parameter-sweeping and evaluation loop.
   - Provide the subagent with the active parameter configuration file (e.g., `config.py` or `EKF_params.py`), the test runner execution command (e.g., `python tester/ABC_Tester.py`), and target KPI thresholds (e.g., 2D RMSE < 0.08m).

2. **Subagent-Driven Autonomous Execution & Verification Loop**:
   - **Step A: Execute Test**: The subagent runs the automated test runner inside a temporary scratchpad/command runner.
   - **Step B: Parse & Evaluate KPIs**: The subagent reads the output metrics (RMSE, MAE, residuals, covariances, state bounds).
     - **Residual Stability**: Check if innovation residuals exhibit zero-mean white noise characteristics.
     - **Convergence Path**: Confirm EKF covariance bounds shrink and estimate states converge without oscillation.
     - **Improvement Rate**: Verify if the error reduction meets target benchmarks compared to the Baseline.
   - **Step C: Recursive Decision & Self-Adjustment**:
     - **If KPIs are NOT met (and max iterations not reached)**:
       - The subagent analyzes the EKF state history to determine if it is a tuning issue (e.g. Q/R covariance balance) or a logic bug.
       - If it is a tuning issue, the subagent dynamically adjusts the parameters in the config file (or runs an optimization search algorithm like Simulated Annealing or Grid Sweep) and **autonomously loops back to Step A**.
       - If a potential code logic error is diagnosed, the subagent halts and notifies the parent agent with diagnostic details.
     - **If KPIs are met**:
       - The subagent records the optimal parameters, locks the configuration, and terminates the loop, reporting the final optimal KPI improvements to the parent agent.

3. **Termination Criteria**:
   - The recursive loop terminates automatically when:
     - All KPI target metrics are fully met (Success).
     - The improvement delta drops below a convergence threshold (e.g., $\Delta < 1\%$).
     - The maximum iterations limit (e.g., 20 autonomous sweeps) is reached.

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
- [ ] **Stage 4**: Deployed Autonomous Optimization Agent with target KPI thresholds.
- [ ] **Stage 4**: Subagent completed autonomous recursive parameter-sweeping and evaluation loop.
- [ ] **Stage 4**: Verified residuals, convergence, and quantitative benchmark criteria are met.
- [ ] **Stage 5**: Completed final comparison report and documentation.
```
