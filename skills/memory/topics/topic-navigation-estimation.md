<!-- SCOPE: Navigation algorithms, EKF/SLAM estimation, log processing, and performance scaling. -->
# Navigation, Estimation & Log Analysis

## INS_python (Core Estimation & SLAM)

### [2026-05-15] Global Batch Optimization (LSM) Framework
- **Init & Delay**: Zero-EKF init via accLeveling/GPS diff. Est GNSS delay (tau) via Taylor expansion Jacobian.
- **Attitude**: SO(3) updates; sparse Levenberg-Marquardt solver via `spsolve`.
- **Stabilization**: Fixed rotation Jacobians & recursive bias propagation. (Horizontal error: 0.06m).
- **Project Structure**: Reverted state indexing for Wind/Gravity/SF. Reverted to Standard Form covariance.

### [2026-05-17] Cartographer SLAM & Calibration
- **Calibration**: Heading offset (+8.2°) alignment reduced 2D RMSE to 0.0713m. EKF `pos0` must match LLA.
- **Odometry**: Wheel constraints reduced RMSE from 0.31m to 0.08m. Aligned path RMSE/MAE is primary.
- **ABC Sweep**: Optimal yaw offset (+19°), timing (+0.1s), lever arm (-0.13, -0.07)m (RMSE_2D: 0.27m).
- **Tuning (N10 Lidar)**: No odometer setup; short range (15m). Set `num_range_data = 45` to prevent translation drift. High `rotation_weight = 150.0` leverages IMU Yaw constraint. Set `min_z = -0.1m` to filter ground reflections.
- **Submap Reprojection**: Bridge `/submap_list` from ROS to Windows UDP `9092`. Cache submap local poses `(idx, x, y, yaw)` to dynamically re-project historical points on redraw. Bound virtual submaps to prevent memory leaks.
- **Tracking Error**: XKF1 diverges from llh2enu over 20km (39m error). Extract Geodetic POS to isolate drift. Zero-base altitude by subtracting first point. Truncate query end times by -0.1s to avoid sync spikes.

### [2026-06-07] GlobalBatchOptimizer Bias & Scale Factor Calibration
- **Calibration Fix**: Apply continuous noise (ARW/VRW) scaled by `np.sqrt(dt)`, GNSS velocity factor constraints, Node 0 bounds. Recovers slowly-varying biases (gyro 5~45 DPH, accel -0.5~0 mg).
- **Unit Scale**: Gyro bias extraction from raw EKF logs must convert rad/s to DPH using `*(180.0 / np.pi * 3600.0)`.

### [2026-06-11] Performance & GPU Acceleration
- **Vectorization**: `np.searchsorted` for preintegration/Jacobian time-sync (dropped time/iteration by ~84%).
- **Jacobian**: Replaced `list.append` (720K per-iter) with `extend` & pre-cached identity matrices (30.7% speedup).
- **GPU Feasibility**: CuPy with `cupyx.scipy.sparse.linalg.spsolve` is viable for Hessian solving ($H = J^T J$) on N > 20k. Host-to-device overhead makes CPU faster for < 10k nodes.

## ArduPilot & Log Analysis (Data Processing)

### [2026-05-26] High-Performance Log Parsing
- **Optimization**: Read into mutable `bytearray`/`mmap`. ProcessPoolExecutor for parallel trajectory analysis.
- **Pitfalls**: Skip offsets where `body_start + body_len` exceeds file size. Preserve `IMS` alignment.
- **FFT Gaps**: Estimate `fs` from median positive `dt` in the longest continuous segment to avoid bias.
- **Scaling & CLI**: Standardized on `--input`/`--out`. Fixed ILB gyro double-conversion (57.3x) scaling.
- **NPZ Output**: Automatically save EKF results as compressed `.npz` file for rapid cross-model EKF analysis.

### [2026-06-11] Memory Safety & EKF Hot-Loop Tuning
- **EKF Hot-Loop Tuning**: Achieved 58% runtime reduction (22.83s to 9.53s). Pre-cached log categories, pre-computed sensor flags, re-used cache dict, and avoided redundant `.copy()` calls.
- **Resource Scaling**: Decimate data by 20 for plots. Run massive logs (>800MB) in isolated subprocesses.
- **Cores**: Use 2-3 cores (parallel workers count: `max(1, cpu_count - 4)`) to balance CPU and RAM usage.
