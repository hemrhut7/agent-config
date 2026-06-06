<!-- SCOPE: Knowledge about note. Read when related tasks arise. -->

> [!NOTE]
> Compressed on 2026-06-06. Older content archived to `archive\compressed\topics_topic-note.md_2026-06-06.md`.

**Bumpless Transfer:** Implemented proportional scaling of the integral accumulator when KI changes inside `PID::setTunings` to prevent holding torque drop or control sags during Rule 2 deactivation.

### [2026-06-06 15:10] Tags: note, daily-summary
**Cross-Core Spinlock:** Wrapped writes in `set_pid_gains()` and reads/transitions in `update()` with FreeRTOS `portENTER_CRITICAL(&app_mode_mux)` to prevent telemetry tearing and multi-core data races.

### [2026-06-06 15:10] Tags: note, daily-summary
**Input Sanitization Failsafe:** Implemented strict non-negative, finite, and non-NaN boundaries checks in `AppScript` for serial PID commands to block catastrophic crash-inducing data.

### [2026-06-06 15:10] Tags: note, daily-summary
**Type-safe Math:** Switched all float absolute comparisons to `std::abs()` to prevent compiler-dependent integer casting.

### [2026-06-06 15:10] Tags: note, daily-summary
**Joystick Reconnection & Thread Safety Fix**:

### [2026-06-06 15:10] Tags: note, daily-summary
Solved reconnection failure by accepting new gamepads in `on_connected()` if the old pointer is stale (`!gamepad_->isConnected()`), and setting `gamepad_ = nullptr` immediately in the main loop upon disconnect detection.

### [2026-06-06 15:10] Tags: note, daily-summary
Eliminated data races and Guru Meditation crashes between the BTstack background task and the main gamepad task by wrapping all pointer operations in a FreeRTOS Mutex.

### [2026-06-06 15:10] Tags: note, daily-summary
Compilation verified successfully via PlatformIO (12.76 seconds).

### [2026-06-06 15:10] Tags: note, daily-summary
**InertialLabs INS-U Driver Audited and Fixed**:

### [2026-06-06 15:10] Tags: note, daily-summary
Audited the custom GPS lock detection and solution mapping against the INS-U ICD rev-1.43. Fixed a critical safety mapping issue where `ins_sol_status = 2` (no GNSS) was mapped to `FIX_2D`. Corrected the centidegrees scaling for `track_over_ground_raw` (which was set directly to float `yaw` degrees).

### [2026-06-06 15:10] Tags: note, daily-summary
Made the external GPS lock detection robust to custom packet configurations lacking `FULL_SAT_INFO` by falling back to `GNSS_POS_VALID` and `ins_sol_status`.

### [2026-06-06 15:10] Tags: note, daily-summary
Discovered and resolved a unit-mismatch bug in `AP_ExternalAHRS_InertialLabs.cpp` where raw lat/lon/alt accuracies reported by INS-U (in mm) were passed directly to AP_GPS without converting to meters. Fixed by multiplying accuracies by `1e-3f` and populated `horizontal_vel_accuracy`.

### [2026-06-06 15:10] Tags: note, daily-summary
**GPS Switching Failsafe & Switch Grace Period Optimization in EKF3**:

### [2026-06-06 15:10] Tags: note, daily-summary
**Primary GPS GCS Notification**: Added `GCS_SEND_TEXT` when the primary GPS changes in `AP_GPS::update()` to print a clear notification `"GPS primary changed to %u"`.

### [2026-06-06 15:10] Tags: note, daily-summary
**GPS Switch Grace Period Optimization in EKF3**:

### [2026-06-06 15:10] Tags: note, daily-summary
Reset EKF position drift accumulator `gpsDriftNE = 0.0f` and reference coordinate `gpsloc_prev` when the EKF detects a GPS switch (`preferred_gps != last_preferred_gps`). This eliminates the ground-based 12-second drift failsafe transient.

### [2026-06-06 15:10] Tags: note, daily-summary
Instantly reset accuracy variables to raw new GPS metrics on switch to prevent 20-second decay lag.

### [2026-06-06 15:10] Tags: note, daily-summary
Dynamically reduced EKF quality check recovery threshold (`align_recover_threshold`) and EKF stability recovery threshold (`stable_recover_threshold`) to **2 seconds** instead of 10 seconds if the target GPS is reported as healthy by its driver (`status >= GPS_OK_FIX_3D`). This reduces EKF Ground Switch recovery time from 32s to 4s.

### [2026-06-06 15:10] Tags: note, daily-summary
**Google Cartographer 2D LiDAR SLAM & EKF Fusion**:

### [2026-06-06 15:10] Tags: note, daily-summary
Dockerized SLAM setup using lightweight ROS Noetic container.

### [2026-06-06 15:10] Tags: note, daily-summary
Built pure Python pipelines (`npz_to_rosbag.py`, `run_slam.py`, `slam_result_injector.py`) for offline SLAM injection.

### [2026-06-06 15:10] Tags: note, daily-summary
Resolved LLA origin misalignment between EKF (`pos0` = [0, 0, 0] LLA) and LiDAR SLAM (`origin_lla` = [25.0, 121.0, 10.0] LLA), reducing EKF LiDAR-only closure error to 0.85m.

### [2026-06-06 15:10] Tags: note, daily-summary
Enabled wheel odometry constraints and tuned biases, reducing AGV 2D RMSE from `0.3133 m` to `0.0832 m`.

### [2026-06-06 15:10] Tags: note, daily-summary
Discovered absolute Cartographer heading coordinate offset of `+8.2°` relative to vehicle body frame. Applying this reduced EKF 2D RMSE to a spectacular `7.13 cm` (0.0713m).

### [2026-06-06 15:10] Tags: note, daily-summary
**Log Parsing & Extractor CLI Standardization**:

### [2026-06-06 15:10] Tags: note, daily-summary
Standardized all log analysis tools on `--input` and `--out` parameters, routing outputs to `output/<log_name>/<analysis_type>_Analysis/`.

### [2026-06-06 15:10] Tags: note, daily-summary
Implemented high-performance binary file parsing (mmap, struct) in `LogPlotter.py` and resolved `AttributeError` on `mlog.offsets`.

### [2026-06-06 15:10] Tags: note, daily-summary
Corrected ILB gyroscope double-conversion unit mismatch (57.3x scaling bug) in `AP_ILB_Replay_Analyzer.py`.

### [2026-06-06 15:10] Tags: note, daily-summary
Build config files (.cmake, Makefile, platformio.ini): **read-only** without explicit permission

### [2026-06-06 15:10] Tags: note, daily-summary
Temp files go in `.agent_scratchpad/`, never `/tmp`

### [2026-06-06 15:10] Tags: note, daily-summary
Uses `-u` flag for all Python execution (unbuffered)

### [2026-06-06 15:10] Tags: note, daily-summary
Weekly report path: `/media/hank/B0D4B41ED4B3E4AE/文件/週報`
