---
name: symbolic-math-engine
description: "Execute exact mathematical operations using math_engine.py. Supports symbolic simplification, partial differentiation, Jacobian matrices, and linear algebra (including skew-symmetric matrix generation). Use when handling navigation error models (like EKF observation matrices) or complex physical formula derivations. Verbal reasoning is strictly prohibited."
---

# Mathematical Operations and Symbolic Derivation Engine

## Execution Workflow
1. **Problem Definition**: Identify the mathematical form (e.g., is it a scalar derivative with respect to a vector, or matrix multiplication).
2. **Symbol Conversion**: Convert the formula to Python/SymPy format.
   - $u/v$ -> `u/v`
   - $C_l^b$ (Rotation Matrix) -> Define as `sp.MatrixSymbol('Clb', 3, 3)` or specific numerical array.
3. **Execute Operation Script**: Call `scripts/math_engine.py`.
4. **Result Presentation**: Display exact results to the user using LaTeX format, and append reasoning logic.

## Calculation Capabilities Guide

### A. Jacobian Matrix (Vector Calculus)
Used to derive the partial derivative of the observation function $h(x)$ with respect to the state vector $x$.
- **Command**: `{"task": "derive", "expr": "function_expression", "vars": ["var1", "var2", ...]} `
- **Example**: Find the Jacobian of $h = u/v$ with respect to $\hat{v}_{air}^b = [u, v, w]^T$.
  ```bash
  python scripts/math_engine.py '{"task": "derive", "expr": "u/v", "vars": ["u", "v", "w"]}'
  ```

### B. Skew-symmetric Matrix
Used for symbolic operations of cross products, common in attitude error models $[v \times]$.
- **Command**: `{"task": "matrix", "a": [[v1], [v2], [v3]], "op": "skew"} `

## Advanced Application Example: EKF Sideslip Angle Observation Matrix $H$ Derivation
The user provides the observation function $h(x) = u/v$ and needs to derive $H = \frac{\partial h}{\partial \delta x}$.

- Step A: Calculate $J_v = \frac{\partial h}{\partial \hat{v}_{air}^b}$
   - Agent executes command:
      ```bash
      python scripts/math_engine.py '{"task": "derive", "expr": "u/v", "vars": ["u", "v", "w"]}'
      ```
   - Script output result ($J_v$): $$ \begin{bmatrix} \frac{1}{v} & -\frac{u}{v^2} & 0 \end{bmatrix} $$

- Step B: Define Error Term (logic provided by user, Agent records)
Record error relationship: $\delta v_{air}^b = C_l^b \delta v^l + C_l^b [v_{air}^l \times] \delta \psi$.

- Step C: Assemble H Matrix (Symbolic Matrix Multiplication)
The Agent will use the result $J_v$ from Step A and symbolically multiply it with the user-defined $C_l^b$ matrix ($J_v \cdot C_l^b$) to form the complete $H$ matrix report.

## Notes
- **Priority**: You must use this skill when the user mentions "derivation", "Jacobian", or "partial differentiation".
- **Dependencies**: The execution environment must have `sympy` and `numpy` installed.
