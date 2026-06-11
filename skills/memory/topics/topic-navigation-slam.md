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
- **Fix**: Calculate and apply continuous-time noise parameters (ARW, VRW) scaled by \
p.sqrt(dt)\ for the state integration model, add GNSS velocity factor constraints, and set realistic prior bounds on Node 0. This successfully recovers realistic, slowly-varying bias estimation (gyro bias 5~45 DPH, accel bias -0.5~0 mg) and scale factor drift.
- **Unit Scale**: Gyro bias extraction from raw EKF logs must convert rad/s to DPH using \*(180.0 / np.pi * 3600.0)\.

### [2026-06-11] Tags: navigation, gpu, optimization, cupy
#### GPU Acceleration Investigation for Global Batch Optimizer
- **Feasibility**: High. GPU acceleration for the Hessian $H = J^T J$ and sparse linear solve is feasible for large-scale problems.
- **CuPy Strategy**: Transfer Jacobian $J$ (COO) and residual $r$ to GPU. Compute $H = J^T J$ and solve for $dx$ using `cupyx.scipy.sparse.linalg.spsolve` (which uses cuSolver).
- **Bottlenecks**: 
    - **Host-to-Device Overhead**: For systems < 10,000 nodes, CPU (Numba + SciPy) might be faster due to transfer latency.
    - **Serial Dependencies**: The block-tridiagonal Cholesky solver has serial dependencies along the time axis. Direct parallelization requires specialized algorithms like Parallel Cyclic Reduction (PCR).
- **Recommended Tools**: 
    - **Theseus (Meta)**: Best for native GPU-accelerated batch optimization (BaSpaCho).
    - **NVIDIA cuDSS**: Latest high-performance sparse solver, significantly faster than `cuSolverSp`.
- **Performance Threshold**: GPU typically shows clear benefits when matrix dimensions exceed 20,000.

### [2026-06-11] Tags: navigation, ekf, performance, optimization, numba, python-overhead
#### EKF Performance Optimization Analysis for Large Logs
Current EKF core is highly efficient due to `numba.njit(cache=True)`, but high-frequency loops (200-400Hz) in Python wrappers introduce significant overhead.
- **Identified Bottlenecks**:
    1. **Redundant Logic**: `any(start <= t <= end for ...)` in hot loops creates expensive generator objects. Use vectorized pre-computation.
    2. **Memory churn**: Excessive `.copy()` calls on state vectors and constant dictionary instantiation (`sensor_data = {...}`) triggers heavy GC. Use in-place updates or reusable objects.
    3. **Sensor Flag Logic**: Computing sensor enablement per-step is redundant. Pre-calculate boolean arrays for `in_bar`, `in_mag`, etc.
    4. **Sync Latency**: Linear scanning in `_sync_gnss` can be replaced with `numpy.searchsorted` for $O(\log n)$ mapping before the loop.
- **Key Strategy**: Move toward a "Vectorized Input, Jitted Core" architecture. Python should only handle flow control and indexing, not per-step data processing or object creation.
