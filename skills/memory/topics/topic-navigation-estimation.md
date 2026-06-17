<!-- SCOPE: EKF, navigation, estimation algorithms, LiDAR SLAM fusion, and error analysis. -->
# Navigation, Estimation & SLAM

### [2026-05-15 16:39] Tags: navigation, least-squares, LSM, GNSS-delay, UAV
#### Global Batch Optimization (LSM) Framework
Implemented a trajectory smoother using Non-linear Least Squares (LSM).
- **Initialization**: Zero-EKF initialization via accLeveling and GNSS diff.
- **GNSS Delay (tau)**: Estimated via Taylor expansion Jacobian.
- **Manifold Optimization**: SO(3) updates for attitude.
- **Solver**: Sparse Levenberg-Marquardt using `scipy.sparse.linalg.spsolve`.
- **Stabilization**: Fixed rotation Jacobians and implemented recursive bias propagation. Horizontal error: 0.06m.

### [2026-05-17 19:12] Tags: navigation, ekf, calibration, lidar, slam
#### EKF LiDAR Yaw Calibration & Optimization
- **Key Discovery**: Identified +8.2° heading offset in Cartographer relative to absolute ENU.
- **Result**: Setting `lidar_yaw_offset_deg = 8.2` reduced 2D RMSE to 0.0713m (7.13cm).
- **Origin Alignment**: EKF `pos0` must match LiDAR origin LLA (e.g. [25.0, 121.0, 10.0]) to prevent residual explosion.
- **Odometry**: Enabled wheel odometry constraints, reducing RMSE from 0.31m to 0.08m.

### [2026-05-18 12:53] Tags: ekf, architecture-sync, bugfix
Synchronized `modify-project-structure` branch. Reverted state indexing for Wind/Gravity/SF. Reverted to Standard Form covariance update for consistency with master.

### [2026-05-20] Tags: navigation, coordinate-projection, llh
#### Tracking Error Methodology
- **Coordinate Projection**: EKF internal `XKF1` frame diverges from `llh2enu` over 20km (~39m error). Extract Geodetic `POS` for consistent projection.
- **Vertical Baseline**: Zero-base altitudes by subtracting the first point to isolate active drift.
- **Transitions**: Truncate query end times by -0.1s to avoid spikes from GNSS restoration/sync mismatch.

### [2026-05-17 14:30] Tags: slam, cartographer, metrics
Use aligned path RMSE/MAE as primary metrics for SLAM evaluation, not just closure error. Aligned path RMSE improved from 0.47m to 0.32m with `enable_lidar_yaw=True`.

### [2026-05-17 17:05] Tags: slam, abc, sweep
Three-stage sweep for ABC dataset found optimal yaw offset (+19°), timing (+0.1s), and lever arm (-0.13, -0.07) m, reducing RMSE_2D to 0.27m. Remaining error suggests URDF/TF inconsistencies.

### [2026-06-07 17:21] Tags: navigation-slam
#### GlobalBatchOptimizer Bias & Scale Factor Calibration
- **Issue**: Hardcoded priors on attitude and noise bounds allowed the optimizer to fit trajectories by slightly wiggling states rather than updating biases, causing bias values to remain near zero and scale factors to remain flat.
- **Fix**: Calculate and apply continuous-time noise parameters (ARW, VRW) scaled by `np.sqrt(dt)` for the state integration model, add GNSS velocity factor constraints, and set realistic prior bounds on Node 0. This successfully recovers realistic, slowly-varying bias estimation (gyro bias 5~45 DPH, accel bias -0.5~0 mg) and scale factor drift.
- **Unit Scale**: Gyro bias extraction from raw EKF logs must convert rad/s to DPH using `*(180.0 / np.pi * 3600.0)`.

### [2026-06-11] Tags: EKF, Optimization, GlobalBatchOptimizer, Python, Numba, searchsorted
#### GlobalBatchOptimizer Performance Optimization Results
1. `_preintegrate_all` (was 66.1% of time): Replaced full-array boolean mask `(imu_t > t_start) & (imu_t <= t_end)` with O(1) vectorized `np.searchsorted`. Time per iteration dropped by ~84% (from ~1.01s down to ~0.16s for 1877 nodes).
2. `_build_jacobian` (was 28.1% of time): Replaced O(N) GNSS search `np.argmin(np.abs(...))` with `np.searchsorted`.
Overall Impact: Total Batch EKF iteration time reduced by ~60% (e.g. from ~3.1-4.9s to ~1.3-1.9s for 4000 nodes).

### [2026-06-11] Tags: navigation, gpu, optimization, cupy
#### GPU Acceleration Investigation for Global Batch Optimizer
- **Feasibility**: High. GPU acceleration for the Hessian $H = J^T J$ and sparse linear solve is feasible for large-scale problems.
- **CuPy Strategy**: Transfer Jacobian $J$ (COO) and residual $r$ to GPU. Compute $H = J^T J$ and solve for $dx$ using `cupyx.scipy.sparse.linalg.spsolve`.
- **Bottlenecks**: Host-to-Device overhead for < 10,000 nodes; serial dependencies in Cholesky solvers.
- **Recommended Tools**: Theseus (Meta) or NVIDIA cuDSS for systems exceeding 20,000 nodes.

### [2026-06-11] Tags: navigation, ekf, performance, optimization, numba, python-overhead
#### EKF Performance Optimization Analysis for Large Logs
Current EKF core is highly efficient due to `numba.njit(cache=True)`, but high-frequency loops (200-400Hz) in Python wrappers introduce significant overhead.
- **Identified Bottlenecks**: (1) Redundant loop search logic, (2) Memory churn via excessive `.copy()` calls, (3) Redundant sensor flag checks, (4) Linear sync latency (use `np.searchsorted`).
- **Key Strategy**: Move toward a "Vectorized Input, Jitted Core" architecture.

### [2026-06-16] Tags: navigation, least-squares, LSM, optimization, numba
#### GlobalBatchOptimizer add_factor & Jacobian Build Optimization
- **Solution A (Implemented)**: Replaced element-by-element `list.append` (originally ~720K per-iteration) with batch `extend` and pre-cached identity/negative-identity matrices. This minimizes Python function call overhead and allocations.
- **Solution C (Recorded)**: Numba-ify `_build_jacobian` and `add_factor`. Compile the entire Jacobian triple-loop using `@njit(cache=True)`.
