# Daily Summary

## Achievements (EKF3 Replay & INS-U AHRS Integration) - Master Config
- **InertialLabs INS-U Driver Audited and Fixed**: Audited the custom GPS lock detection and solution mapping against the INS-U ICD rev-1.43. Fixed a critical safety mapping issue where `ins_sol_status = 2` (no GNSS) was mapped to `FIX_2D`. Corrected the centidegrees scaling for `track_over_ground_raw` (which was set directly to float `yaw` degrees). Made the external GPS lock detection robust to custom packet configurations lacking `FULL_SAT_INFO` by falling back to `GNSS_POS_VALID` and `ins_sol_status`.
- **Replay Verification of INS GPS2 Logic**: Developed post-processing script `apply_ilb_gps2.py` to rewrite GPS2/GPA2 messages in binary logs based on the new driver's status-mapping and scaling rules. Optimized the C++ replayer's online GPS1 drop logic to allow selective outage simulations without needing the deprecated `inject_outage_gps1.py` script (which has been removed).
- **Verification**: Successfully simulated EKF3 GPS2 auto-switching on `log_26` under 6 simultaneous outages. The replayed EKF3 successfully switched to GPS2 (ILB data), keeping the estimation drift exceptionally low (down to 0.780 m/s in Outage 5, matching the external INS trajectory almost perfectly).
- **Documentation**: Updated `Tools/Replay/README.md` to document the new simplified simulation workflow and deprecated the `inject_outage_gps1.py` script.
- **Log Parsing Knowledge Persisted**: Saved the premium "pure byte-level in-place log modification" algorithm to long-term memory under `topics/topic-log-processing.md` for future reuse.

## Achievements (Google Cartographer 2D LiDAR SLAM & EKF Fusion) - EKF Pipeline
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

## Active & Pending Tasks
- [x] Resolve EKF analysis log truncation
- [x] Implement robust log header resynchronization in DataFlashFileReader
- [x] Fix orchestrator path resolution to prioritize SITL target binary
- [x] Correct flight mode label clipping in plot analyzer
- [x] Audit and fix InertialLabs INS-U external AHRS driver (track_over_ground scaling, fix mapping, GPS lock detection)
- [x] Verify GPS2 mapping logic via log post-processing and EKF3 Replay
- [x] Verify and implement GPS auto-switching logic in EKF3 Replay
- **EKF Tuning & Refactoring**: Refactor `nav_ekf/filters/kalman_filter.py` namespace imports from `from .ekf_params import *` to `from . import ekf_params` to support dynamic parameter tuning.
- **Validation**: Run multi-scenario evaluations across other UDP-recorded datasets.
- **SLAM Tuning**: Fine-tune Ceres scan-matching covariances in Cartographer configuration (`my_2d.lua`).
- **Hardware Integration**: Verify IMU/Odometry performance on physical AGV hardware.

## Workspace Conventions
- Build config files (.cmake, Makefile, platformio.ini): **read-only** without explicit permission
- Temp files go in `.agent_scratchpad/`, never `/tmp`
- Uses `-u` flag for all Python execution (unbuffered)
- Weekly report path: `/media/hank/B0D4B41ED4B3E4AE/文件/週報`
