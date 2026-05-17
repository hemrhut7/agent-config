<!-- SCOPE: Knowledge about navigation. Read when related tasks arise. -->
# Navigation

### [2026-05-15 16:39] Tags: navigation, least-squares, LSM, GNSS-delay, UAV
# Global Batch Optimization (LSM) Framework\n\n## Overview\nImplemented a trajectory smoother using Non-linear Least Squares (LSM) to serve as a high-precision baseline for EKF evaluation. The system uses a Factor Graph approach with IMU pre-integration.\n\n## Key Features\n- **Zero-EKF Initialization**: Uses accLeveling for attitude and GNSS interpolation/finite-difference for pos/vel. Completely independent of EKF state.\n- **GNSS Delay Estimation (tau)**: Global parameter estimated via Taylor expansion Jacobian: partial r_p / partial tau = v_k.\n- **Pre-integration**: High-frequency IMU data compressed between nodes (e.g., 5Hz or 10Hz).\n- **Manifold Optimization**: Proper SO(3) updates for attitude (q <- q * exp(delta theta)).\n- **UAV Models**: Includes wind (2D), TAS scale/bias, and magnetic field constraints.\n\n## Architecture\n- **State Node (23 DOF)**: [p, v, delta theta, b_a, b_g, w, m_I, m_b].\n- **Global States**: [tau, s_tas, b_tas].\n- **Solver**: Sparse Levenberg-Marquardt using scipy.sparse.linalg.spsolve.\n\n## Compatibility\nUses MockKF to bridge the gap between LSM results and EKFAnalyzer. Required attributes: logger.data, dim, my_EKF.dim, device_name, reset_time.

### [2026-05-17 19:12] Tags: navigation, ekf, calibration, lidar
### EKF LiDAR Yaw Calibration & Optimization (ABC Dataset)

#### Context
In the EKF navigation sensor fusion pipeline, the Cartographer 2D LiDAR SLAM coordinates showed a systematically offset heading relative to absolute vehicle ENU coordinates (driven by IMU orientation / wheel odometry).

#### Key Calibrations
- **IMU Biases**: Initialized gyro biases to [4600, -6500, -10500] dph and accelerometer biases to [-15, -20, 20] mg directly in EKF.
- **Odometry constraints**: Wheel velocity fusion (enable_agv=True) configured with standard deviation (0.01, 0.1, 0.05).
- **Chi-Square Gate**: Expanded Chi-Square gate threshold self.K_threshold = 5 in KalmanFilter.py to prevent update rejection under high angular rates.

#### Discoveries
- **Latency Excised**: Redundant lidar_time_offset latency parameters were excised since zero temporal latency offset (0.0 s) was proven optimal after bias calibration.
- **Optimal Yaw Offset Sweep**: Swept lidar_yaw_offset_deg from -30.0 to +30.0 degrees. Identified the mathematically optimal heading offset to be +8.2 degrees.
- **Result**: Setting lidar_yaw_offset_deg = 8.2 reduces EKF 2D RMSE from 0.0832 m to a stunning 0.0713 m (7.13 cm), and 2D Closure Error to 0.0481 m (4.81 cm).
