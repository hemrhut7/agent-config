---
trigger: always_on
---

# High-Performance Development Guidelines

The core of this project comprises high-frequency (100–400 Hz) Inertial Navigation System & Extended Kalman Filter (INS/EKF) pipelines and a factor-graph global batch optimization engine. To guarantee maximum runtime throughput and prevent performance regression during ongoing development, all code modifications, refactorings, and new features MUST strictly adhere to the following principles:

---

## 1. Zero-Allocation in Tight Loops
- **Prohibit Dynamic Allocations in Hot Paths**: Inside the 100–400 Hz IMU mechanization loop, EKF predict/update stages, and sensor callback handlers, **NEVER** instantiate new NumPy arrays (`np.zeros()`, `np.ones()`, `np.empty()`, `np.array()`) or create dynamic Python objects per epoch.
- **Pre-allocation & Memory Reuse**:
  - All measurement matrices ($H$), innovation observation vectors ($Z$), and covariance matrices ($R$) MUST be pre-allocated as contiguous memory buffers during class initialization (`__init__` or `setInit`).
  - When processing incoming sensor measurements in `input()`, always clear workspace arrays using `.fill(0.0)` and write values via slice assignments (`self.H[0, :3] = ...`).
- **Cache Static Geometry & Invariants**:
  - Lever-arm presence checks (e.g. `has_lever_arm = np.any(lever_arm != 0)`) and mounting orientations MUST be evaluated and cached as boolean invariants during `setInit()`, avoiding redundant `np.any()` evaluations inside the main loop.
  - Body-frame direction constants (e.g. `_N_B`, `_M_B`) should be defined as class/module-level constants.

---

## 2. Innovation Context Reuse & Math Deduplication
- **Eliminate Duplicate Matrix Multiplications**:
  - The intermediate matrices computed during NIS gate evaluation / data association (`dataAssociation()`):
    $$pht = P H^T, \quad S = H P H^T + R, \quad e = Z - H dx$$
    MUST be calculated once via `compute_innovation_context` and cached.
  - The subsequent state update stage (`update_core_with_context`) MUST directly reuse this innovation context rather than recomputing $P H^T$ and $S$.
- **Prioritize Analytical Closed-Form Solutions for Low Dimensions**:
  - For 1D measurement updates (Baro altitude, Airspeed, Mag heading, Sideslip angle), compute the Kalman gain via scalar reciprocal multiplication: $K = pht \cdot S^{-1}$.
  - For 2D measurement updates, use 2nd-order analytical determinant inversion; NEVER call general-purpose `np.linalg.inv()`.
  - Always enforce numerical covariance symmetrization: $P_{new} = 0.5 (P_{new} + P_{new}^T)$.

---

## 3. Numba JIT Compilation & Vectorized Execution
- **JIT Compilation for Compute-Intensive Cores**:
  - Core numerical kernels (e.g., `update_core_with_context`, IMU pre-integration factors, Block-Cholesky solvers `_solve_L` and `_solve_LT`) MUST be decorated with `@njit(cache=True, fastmath=True)`.
  - Avoid Python lists or dictionaries inside Numba kernels; ensure all arrays are passed with contiguous memory layouts (`np.ascontiguousarray`).
- **Vectorization Over Python Loops**:
  - For asynchronous sensor timestamp alignment or nearest-neighbor queries, use vectorized binary searches (e.g., `_nearest_val_vectorized` and `np.searchsorted`). Python `for` loops across time series are strictly prohibited.
  - Angle unit conversions (e.g., `np.rad2deg`, `np.deg2rad`) MUST be executed in bulk on NumPy arrays during the logging serialization stage, never point-by-point inside the EKF loop.

---

## 4. Pre-Allocated Batched Logging & Serialization
- **Direct NumPy Buffer Writes for State Logging**:
  - In high-rate execution loops, telemetry loggers must write directly to pre-bound `_Buffer.data` array slices using index counters (`self._arr_pos[idx] = ...`), eliminating per-epoch Python method dispatch overhead (`_Buffer.append()`) across millions of iterations.
- **Vectorized Binary Serialization**:
  - When exporting ArduPilot DataFlash `.bin` logs, use structured dtypes (NumPy Structured DType) paired with `DataFlashWriter.write_batch` for single-pass contiguous binary writes (`tobytes()`), strictly avoiding per-row Python `struct.pack` loops.

---

## 5. Performance Regression & Accuracy Gates
- **Dual Verification Standards**:
  1. **Accuracy Gate**: No optimization or refactoring may alter navigation or outage estimation metrics. All unit tests (`pytest tests/`) must pass, and outage metrics must remain within strict tolerance.
  2. **Performance Gate**: Before and after major architectural changes, run benchmark verification (e.g., 5 repeated runs of `examples/ILB_outage_by_default.py` taking the median), ensuring execution time does not regress (target total runtime $\le 70\text{ s}$, EKF core runtime $\le 52\text{ s}$).
