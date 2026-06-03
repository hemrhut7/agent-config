# Daily Summary
## Last Updated: 2026-05-22 09:15

### Active Tasks
- [x] Standardize command-line arguments for all log analysis tools (`INS_log_extractor.py`, `AP_ILB_Replay_Analyzer.py`, `plot_AP-EKF_ILB-INS.py`, `GNSS_Denied_Analysis.py`, `Attitude_Airspeed_Analysis.py`).
- [x] Re-organize default output directories to route to `output/<log_name>/` subfolders.
- [x] Implement robust candidate directory search paths for CSV logs when referencing relative paths.
- [x] Complete end-to-end verification of all five tools.
- [x] Update `tools/README.md` to reflect unified usage and options.
- [x] Port parallel high-performance binary parsing to `LogPlotter.py` and fix the `mlog.offsets` list AttributeError bug.
- [x] Analyze and fix the ILB gyroscope unit mismatch (57.3x scaling bug) in `AP_ILB_Replay_Analyzer.py`.
- [x] Modify `vibration_analysis_runner.py` to use the longest continuous segments for all analyses, crop ILB data to the IMU0 segment window, and remove the vibration trend and rate aliasing comparison plots.
- [x] Implement ArduPilot-style dynamic filtered vibration calculation and plotting in `tools/vibration_analysis_runner.py`.

### Session Notes
- Standardized all tools on `--input` and `--out` CLI parameters.
- Re-organized analysis outputs to dynamically target `output/<log_name>/<analysis_type>_Analysis/`.
- Fixed a bug in `plot_AP-EKF_ILB-INS.py` where processing logs without InertialLabs EKF/INS replay data caused `NameError: name 't0' is not defined`.
- Verified all tools successfully via CLI on local logs.
- Documented new usage paradigms and formats in `tools/README.md`.
- Implemented high-performance binary file parsing (mmap, struct) in `LogPlotter.py`.
- Fixed the `AttributeError: 'list' object has no attribute 'get'` in `LogPlotter.py` by using index boundary check + list indexing. Verified speedup and correct behavior on real BIN logs.
- Fixed a gyroscope unit mismatch bug in `AP_ILB_Replay_Analyzer.py` where the ILB1 native gyroscope values (already in rad/s in the log) were incorrectly scaled by `np.radians` again. Removing the redundant conversion matches the AP IMU scale (e.g. standard deviation of ~9.5 deg/s vs ~6.2 deg/s) and fixes EKF vs ILB comparisons.
- Modified `tools/vibration_analysis_runner.py` to:
  - Extract the longest continuous segment for the master reference sensor (`IMU0`) first.
  - Crop all other sensors' DataFrames (`IMU1`, `IMU2`, high-rate ILB, standard-rate ILB) to this master segment window to enforce temporal alignment.
  - Extract the longest continuous segments from the cropped DataFrames for all subsequent analyses, stats calculations, FFT computations, and overlay plots.
  - Suppressed generation of the vibration trend plot (`vibration_trends.png`) and rate aliasing comparison plot (`rate_aliasing_comparison.png`).
  - Updated the markdown report generator (`VIBRATION_REPORT.md`) to reflect these changes, removing references/sections for the deleted plots.
- Implemented ArduPilot-style dynamic low-pass filtered vibration calculation (`compute_ap_vibration`) using a 5.0 Hz floor LPF and 2.0 Hz vibration LPF to mirror `AP_InertialSensor.cpp` logic.
- Added generation of `vibration_levels_comparison.png` (a 2x2 subplot comparing X, Y, Z, and Mag vibration levels over time for all IMUs and the high-rate ILB log).
- Updated the report template in `tools/vibration_analysis_runner.py` to compile detailed per-axis and magnitude statistics under a new section "3. ArduPilot-Style Vibration Analysis (5Hz Floor / 2Hz Vibe LPF)" and embed the comparison plot, omitting the standard-rate ILB sensor from all vibration metrics, plots, and report tables.

### Pending Decisions
- none

## Achievements (EKF3 Replay & INS-U AHRS Integration) - Master Config
- **InertialLabs INS-U Driver Audited and Fixed**: Audited the custom GPS lock detection and solution mapping against the INS-U ICD rev-1.43. Fixed a critical safety mapping issue where `ins_sol_status = 2` (no GNSS) was mapped to `FIX_2D`. Corrected the centidegrees scaling for `track_over_ground_raw` (which was set directly to float `yaw` degrees). Made the external GPS lock detection robust to custom packet configurations lacking `FULL_SAT_INFO` by falling back to `GNSS_POS_VALID` and `ins_sol_status`.
- **GPS Per-Instance Disable Bugs Audited and Fixed (Centralized Design)**:
  - Fixed a parameter-swapping bug in `AP_ExternalAHRS_InertialLabs` where `force_disable(0, true)` enabled GPS2 instead of disabling GPS1.
  - Centralized the disable override logic inside `AP_GPS::update_instance()` (right after raw logging), rewriting `state[instance].status` to `NO_FIX` if that instance is disabled.
  - This centralized override automatically propagates to EKF, blending, notify, and all external status readers via `status()`, completely eliminating the confusion of mixing raw `state[i].status` and `status(i)` calls throughout the codebase.
  - Added boundary checks (`instance < GPS_MAX_RECEIVERS`) on the `disabled_gps` array to guarantee safety.
- **Log Parsing Knowledge Persisted**: Saved the premium "pure byte-level in-place log modification" algorithm to long-term memory under `topics/topic-log-parsing.md` for future reuse.


## Last Updated: 2026-05-31 09:15

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
- [x] Fix flight mode switching command destination synchronization mismatch in MAVLink connector
- [x] Sort the MAVLink message rate list tree alphabetically by message name


## Workspace Conventions
- Build config files (.cmake, Makefile, platformio.ini): **read-only** without explicit permission
- Temp files go in `.agent_scratchpad/`, never `/tmp`
- Uses `-u` flag for all Python execution (unbuffered)
- Weekly report path: `/media/hank/B0D4B41ED4B3E4AE/文件/週報`
