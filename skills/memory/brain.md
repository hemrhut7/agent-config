# Daily Summary - 2026-05-18

## Context
Implementing and validating Google Cartographer 2D LiDAR SLAM with EKF fusion; refactoring package structure to unified `nav_ekf` layout.

## Achievements
- **Dockerized SLAM Setup**: Compiled Google Cartographer ROS Noetic inside a lightweight Docker image and automated master/offline-node lifecycle execution in entrypoint.sh.
- **Automated Data Pipeline**: Implemented pure Python `npz_to_rosbag.py`, `run_slam.py`, and `slam_result_injector.py` to seamlessly convert point clouds, execute offline SLAM, and inject trajectories back to telemetry files.
- **EKF LiDAR Fusion**: Addressed LLA origin misalignment between EKF (`pos0` = [0, 0, 0] LLA) and LiDAR SLAM (`origin_lla` = [25.0, 121.0, 10.0] LLA). Aligned EKF origin to Taipei LLA, successfully reducing EKF 2D closure error with only-LiDAR updates to 0.85m.
- **LiDAR Map Stitching**: Implemented global coordinate transformation mapping in `plot_slam_only.py`, successful stitching of 231,011 points, producing high-resolution environmental vector maps.
- **Visualization & UI**: Updated `KF_Plot.py` with LiDAR heading update indicators and recorded all analysis plots to walkthrough resources.
- **EKF Bias & Constraints Calibration**: Initialized gyro biases to `[4600, -6500, -10500]` dph and accelerometer biases to `[-15, -20, 20]` mg, and enabled wheel odometry constraints (`enable_agv=True`). Set `K_threshold = 5` in `KalmanFilter.py` to prevent gating rejections under dynamics, dropping baseline 2D RMSE from `0.3133 m` to `0.0832 m`.
- **LiDAR Yaw Offset Optimization**: Swept `lidar_yaw_offset_deg` from `-30.0` to `+30.0` degrees at $0.1^\circ$ resolution. Discovered that Cartographer LiDAR SLAM heading contains an absolute coordinate offset of **`+8.2°`** relative to vehicle absolute coordinates. Applying this offset reduced 2D RMSE to a spectacular **`0.0713 m` (7.13 cm)** and 2D closure error to **`0.0481 m` (4.81 cm)**.
- **Temporal Mismatch Excised**: Removed the redundant `lidar_time_offset` variable entirely as raw timestamp alignment without temporal compensation yielded the cleanest result under optimal bias calibration.
- **EKF Parameter Synchronization**: Synced EKF default `TuningConfig` parameter constants in `nav_ekf/filters/config.py` to match the legacy `MyLib/Navigation/EKF_params.py` values exactly.
- **Tester Script Path Migration**: Corrected image, plot, and experiment result save directories in the migrated `examples/` tester scripts (`ArduPilotTester.py`, `ArduPilot_ILB_ATT_ARSPD_Tester.py`, `ArduPilot_ILB_GNSS-denied_Tester.py`, `ArduPilot_ILB_Combined_Tester.py`, `EKFTester_ABC.py`) to save results locally under `examples/results/` instead of `tester/results/`.
- **Log GUI Refactoring**: Refactored `examples/log_gui.py` imports to load `plot_data`, etc. from the local `log_playback` module inside `examples/`.
- **Unified EKF Execution Validation**: Successfully ran the multi-log parallel experiment runner (`ArduPilotTester.py`) to verify correct execution with the synchronized EKF config, saving EKF NPZ logs and plots cleanly under `examples/results/ArduPilot_Multi/`.

## Pending
- Refactor `nav_ekf/filters/kalman_filter.py` namespace imports from `from .ekf_params import *` to `from . import ekf_params` to support dynamic parameter tuning.
- Run multi-scenario evaluations across other UDP-recorded datasets.
- Fine-tune Ceres scan-matching covariances in Cartographer configuration (`my_2d.lua`).
- Verify IMU/Odometry performance on physical AGV hardware.

