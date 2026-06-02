<!-- SCOPE: Knowledge about EKF, navigation, estimation algorithms, GPS/INS integration, and error analysis methodology. -->
# Navigation and Estimation Methodology

## INS_python (Python EKF & LSM Optimization Framework)

### [2026-05-15 16:39] Tags: navigation, least-squares, LSM, GNSS-delay, UAV
#### Global Batch Optimization (LSM) Framework
- **Overview**: Implemented a trajectory smoother using Non-linear Least Squares (LSM) to serve as a high-precision baseline for EKF evaluation. The system uses a Factor Graph approach with IMU pre-integration.
- **Key Features**:
  - **Zero-EKF Initialization**: Uses accLeveling for attitude and GNSS interpolation/finite-difference for pos/vel. Completely independent of EKF state.
  - **GNSS Delay Estimation (tau)**: Global parameter estimated via Taylor expansion Jacobian: partial r_p / partial tau = v_k.
  - **Pre-integration**: High-frequency IMU data compressed between nodes (e.g., 5Hz or 10Hz).
  - **Manifold Optimization**: Proper SO(3) updates for attitude (q <- q * exp(delta theta)).
  - **UAV Models**: Includes wind (2D), TAS scale/bias, and magnetic field constraints.
- **Architecture**:
  - **State Node (23 DOF)**: [p, v, delta theta, b_a, b_g, w, m_I, m_b].
  - **Global States**: [tau, s_tas, b_tas].
  - **Solver**: Sparse Levenberg-Marquardt using `scipy.sparse.linalg.spsolve`.
- **Compatibility**: Uses MockKF to bridge the gap between LSM results and EKFAnalyzer. Required attributes: `logger.data`, `dim`, `my_EKF.dim`, `device_name`, `reset_time`.

### [2026-05-15 16:53] Tags: INS, BatchOptimizer, Jacobian, Preintegration
- **Batch Optimization Stabilization**: Stabilized GlobalBatchOptimizer by fixing rotation Jacobians ($R \cdot [\delta\theta]_\times$) and implementing recursive bias propagation. Resolved unit mismatch in analyzer output by converting ENU to LLH (rad) in results dict. Final convergence cost 22.9, horizontal error 0.06m.

### [2026-05-17 19:12] Tags: navigation, ekf, calibration, lidar
#### EKF LiDAR Yaw Calibration & Optimization (ABC Dataset)
- **Context**: In the EKF navigation sensor fusion pipeline, the Cartographer 2D LiDAR SLAM coordinates showed a systematically offset heading relative to absolute vehicle ENU coordinates (driven by IMU orientation / wheel odometry).
- **Key Calibrations**:
  - **IMU Biases**: Initialized gyro biases to `[4600, -6500, -10500]` dph and accelerometer biases to `[-15, -20, 20]` mg directly in EKF.
  - **Odometry constraints**: Wheel velocity fusion (`enable_agv=True`) configured with standard deviation `(0.01, 0.1, 0.05)`.
  - **Chi-Square Gate**: Expanded Chi-Square gate threshold `self.K_threshold = 5` in `KalmanFilter.py` to prevent update rejection under high angular rates.
- **Discoveries**:
  - **Latency Excised**: Redundant `lidar_time_offset` latency parameters were excised since zero temporal latency offset (0.0 s) was proven optimal after bias calibration.
  - **Optimal Yaw Offset Sweep**: Swept `lidar_yaw_offset_deg` from -30.0 to +30.0 degrees. Identified the mathematically optimal heading offset to be **+8.2 degrees**.
  - **Result**: Setting `lidar_yaw_offset_deg = 8.2` reduces EKF 2D RMSE from 0.0832 m to a stunning **0.0713 m (7.13 cm)**, and 2D Closure Error to **0.0481 m (4.81 cm)**.

### [2026-05-18 12:53] Tags: ekf, architecture-sync, bugfix
#### EKF Architecture Sync & Bugfix
- **Status**: Successfully synchronized `modify-project-structure` branch with master logic.
- **Key Changes**:
  - Reverted state indexing in `nav_ekf/filters/nav_state.py` to match master: Wind (22-23), Gravity (15), SF (16-21).
  - Disabled Schmidt-Kalman Filter (`active_mask`) in `INS_GNSS` for consistency.
  - Reverted covariance update from Joseph Form to Standard Form.
  - Commented out new features (Dynamic R, GPS Yaw Fallback, Wind Jacobian in SideSlip) to isolate architecture changes.
- **Validation**:
  - `EKFTester_20251120.py` results are identical to master.
  - `ArduPilotTester.py` results differ by less than 1% due to data extractor numerical handling.
- **Pitfall**: Fixed `NameError: base_dir` in `ArduPilot_ILB_GNSS-denied_Tester.py`.

### [2026-05-20] Tags: navigation, coordinate-projection, llh, baseline
#### Navigation Tracking Error Methodology
- **Coordinate Projection (LLH vs XKF1)**:
  - **Issue**: EKF internal `XKF1` frame diverges from flat-earth `llh2enu` over distance (~39m error at 20km).
  - **Solution**: Extract Geodetic `POS` (Lat/Lng/Alt) from log; project both EKF and External INS using identical `llh2enu`.
- **Analysis Scope & Telemetry**:
  - **Active Flight Only**: Crop data where ground speed > 5 m/s.
  - **Exclusions**: Focus on position, attitude, and TAS/ARSPD scaling; exclude `DiffPress` and `CAS`.
  - **Recency**: Prioritize logs from the last 2 months.
- **Vertical Baseline Calibration**:
  - **Issue**: Static initialization differences cause vertical offsets.
  - **Solution**: Zero-base altitudes by subtracting the first point's value to isolate active drift.

### [2026-05-22 13:18] Tags: navigation-error, time-sync
#### Relative Tracking Error spikes at transitions
- **Issue**: Transient spikes in sub-segment relative tracking error are caused by time synchronization mismatch at boundary transitions (e.g., when GNSS is restored at the end of outage).
- **Solution**:
  1. Truncate sub-segment query end times by -0.1 seconds (e.g., `seg_end_t - 0.1`).
  2. Use effective duration `eff_duration = seg_duration - 0.1` for drift rate and percent error.
  3. Apply the same offset to plot masks to keep visuals aligned with the tabulated metrics.

## ArduPilot (C++ Autopilot Firmware & Replay System)

### [2026-05-22] Tags: gps, ekf3, switchover
#### GPS Switchover Logic
1. **AP_GPS Selection**: `update_primary()` selects instance based on `GPS_AUTO_SWITCH`. Failure (timeout > 2s) triggers switch.
2. **EKF3 Alignment**: `update_gps_selection()` detects index change. `ResetPositionNE()` (and `ResetPositionD`) align states with new GPS position to prevent control spikes.

### [2026-05-28] Tags: replay, navigation, alignment
#### Replay Origin Offset
- **Issue**: Replay (Core 100) and Flight (Core 0) initialize origins at different times/locations (e.g., 26m horizontal offset).
- **Solution**: Align PN/PE/PD trajectories by shifting replay coordinates to match flight's initial position.
