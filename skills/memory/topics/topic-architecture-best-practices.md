<!-- SCOPE: System architecture, refactoring, code quality, and technical pitfalls. -->
# Architecture & Best Practices

### [2026-05-17 21:41] Tags: architecture, refactor, ekf
#### Core INS/GNSS Library Refactor
- **State Management**: Introduced `NavState`/`StateIndex` for dynamic dimensions (15, 26, 32).
- **Configuration**: Converted configs to dataclasses with YAML support.
- **Modularity**: Reorganized into `core`, `filters`, `sensors`, `framework`, `utils`. Centralized parameters in `EKF_params.py`.
- **Sensor Abstraction**: Introduced `BaseSensorModule` and specific registry-based execution loops.

### [2026-05-17 21:57] Tags: architecture, performance, numba
- **Memory Layout**: Optimized core mechanization by enforcing contiguous memory layouts for Numba JIT efficiency.
- **Logging**: Enhanced `DataLogger` with Context Manager support and chunked writing.

### [2026-05-15 16:39] Tags: pitfall, architecture
- **Circular Dependency**: `Location.h` vs `Vector2.h`. Fix: Moved `HAL_WITH_EKF_DOUBLE` to `HAL_Config.h`, centralized types in `AP_Math_Types.h`.
- **NJIT Refactor**: Refactoring global constants into module-level variables can cause `NameError` in `@njit` functions if not explicitly imported/passed.
- **Type-safe Math**: Avoid compiler-dependent integer casting; use `std::abs()` for all float comparisons.
