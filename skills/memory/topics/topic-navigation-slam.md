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
