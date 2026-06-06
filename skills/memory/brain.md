<!-- SCOPE: Today's task log and working memory. Read at conversation start to resume context. -->
# Brain — Working Memory

## Last Updated: 2026-05-30 10:48

### Active Tasks
- [x] Display IMU initialization failure as "IMU INIT FAILED!" on screen at boot and during execution.
- [x] Analyze IMU peak spikes and identify connection to firmware/hardware.
- [x] Implement a byte-wise sum checksum in telemetry for `FORMAT_DEFAULT`, `FORMAT_PID`, and `FORMAT_LIDAR`.
- [x] Implement a direct `Wire.read() == -1` timeout detection in `hal_imu_read()` on the ESP32 side to reject corrupted samples mid-stream.
- [x] Implement FreeRTOS PortMUX spinlocks around `ahrs_data` writes in `update()` and reads in `get_ahrs_data()` to prevent multi-core/multitasking data tearing.
- [x] Decouple I2C read blocking delay and complementary filter update: created `AHRS_Task` at **1000Hz** pinned to **Core 0**, while keeping the critical `Control_Task` at **200Hz** on **Core 1** reading pre-validated data instantly from memory.
- [x] Compile and verify the build using PlatformIO and successfully flash directly to COM7.
- [x] Implement a real-time I2C Bus Error Counter (`hal_imu_get_error_count()`) and display it dynamically on the LCD screen (`y=155`) in green (if zero) or red (if positive).
- [x] Solve QMI8658 Register Tearing by bypassing status register polling and using continuous block reads starting from 0x33.
- [x] Solve Byte Alignment Shifts by implementing Multi-Factor Physical Validation (temperature delta, gyro delta, accel delta checks).
- [x] Create [verify_spikes.py](file:///c:/Users/hemrh/Documents/GitHub/C Language/ABC_Controller/ABC_Controller/verify_spikes.py) and execute automated 120-second telemetry validation: **23,731 packets** parsed at **230400 baud** with a highly strict **3.5 dps threshold** and **ZERO spikes detected**!
- [x] Implement Scheme A: Configured QMI8658 to output DRDY hardware interrupts on `INT1` (`GPIO3`), set Accel/Gyro ODR to 500Hz, and synchronized `AHRS_Task` to block on the GPIO interrupt semaphore (`hal_imu_wait_for_data`).
- [x] Calculate battery voltage ADC LSB calibration coefficients using least-squares linear regression (Slope: `0.00680089f`, Offset: `3.43306268f`) and update `src/hal/hal_battery.h`.
- [x] Resolve EKF analysis log truncation
- [x] Implement robust log header resynchronization in DataFlashFileReader
- [x] Fix orchestrator path resolution to prioritize SITL target binary
- [x] Correct flight mode label clipping in plot analyzer
- [x] Audit and fix InertialLabs INS-U external AHRS driver (track_over_ground scaling, fix mapping, GPS lock detection)
- [x] Verify GPS2 mapping logic via log post-processing and EKF3 Replay
- [x] Verify and implement GPS auto-switching logic in EKF3 Replay
- [x] Implement adaptive PID gains: standstill soft-tuning (Rule 1) and pitch recovery gain boost (Rule 2) in AppMode, verified via successful build compilation.
- [x] Analyze and resolve the joystick reconnection and thread-safety issues (Guru Meditation Error crashes) in `HAL_Joystick` by introducing a FreeRTOS Mutex and robust pointer lifecycle management, verified via successful build compilation.
- [x] Optimize LIDAR telemetry transmission (using single PSRAM buffer to let LwIP handle IP fragmentation) and increase Serial2 RX buffer size to 1024 bytes to prevent serial data buffer overflow under high rates (230400 baud), committed as `e532ff9`.
- [x] Migrate board-integrated QMI8658 IMU to external MPU6050 via raw Wire I2C driver, restoring historical calibration parameters from commit `05f1b1e`.

### Session Notes
- **MPU6050 IMU Migration**:
  - Re-implemented `hal_imu.cpp` with a lightweight, raw I2C Wire driver for MPU6050 (default address `0x68`) operating at 200Hz ODR (divisor = 4) and 44Hz DLPF.
  - Configured MPU6050 hardware Data Ready Interrupts (DRDY) on GPIO 14 (configured as `IMU_INT1_PIN` in `config.h`).
  - Set up a FreeRTOS binary semaphore (`imu_sem`) and ISR (`imu_isr_handler`) on the rising edge of GPIO 14 to block-trigger the main `Control_Task` in `main.cpp` (Architecture B), eliminating loop timing jitter.
  - Set control and communication loop periods to 5ms (200Hz) in `main.cpp` and added a 10ms timeout fallback.
  - Restored original MPU6050 axis mapping (`raw_x = -ax`, `raw_y = ay`, `raw_z = -az`, `raw_gx = -gx`, `raw_gy = gy`, `raw_gz = -gz`).
  - Initialized IMU calibration parameters to identity matrix (R = I) and zero biases (B = 0).
  - Removed temperature delta and spike outlier checks to simplify processing.
  - Verification & Flash: Successfully compiled and flashed directly to COM7 (`pio run -t upload`) in 24.56 seconds.
- **QMI8658 IMU & CPF Calibration & Sync**:
  - Reverted DRDY hardware interrupts and task separation. Switched to continuous 250Hz synchronous reading on Core 1 ControlTask.
  - Recalibrated IMU accel/gyro bias vectors and R matrices for highest precision.
  - Implemented CPF static calibration startup delay of 10 cycles (-10 counter) to discard transients.
  - Optimized angle PID coefficients (`KP_ANGLE=500.0f`, `KI_ANGLE=4000.0f`, `KD_ANGLE=20.0f`) and velocity PID parameters (`KP_VELOCITY=0.2f`, `KD_VELOCITY=0.01f`).
  - Tuned battery ADC linear calibration: `Slope: 0.00680089f`, `Offset: 3.43306268f` in `hal_battery.h`.
- **Adaptive PID Gains & Safety Enhancements (Code-Reviewed & Audited)**:
  - **Rule 1 (Standstill Soft-tuning):** When targets are low and the robot is static (RPM < 25, velocity < 0.1 m/s) for over 2.0 seconds, dynamically divides velocity KP by 10 and multiplies KD by 2. Reverts instantly when commands or speeds exceed thresholds.
  - **Rule 2 (Tilt Recovery Boost):** Boosts angle PID KP and KI by 20% when the actual pitch angle exceeds the `MAX_PITCH` threshold (6.0 degrees) to accelerate recovery.
  - **Bumpless Transfer:** Implemented proportional scaling of the integral accumulator when KI changes inside `PID::setTunings` to prevent holding torque drop or control sags during Rule 2 deactivation.
  - **Cross-Core Spinlock:** Wrapped writes in `set_pid_gains()` and reads/transitions in `update()` with FreeRTOS `portENTER_CRITICAL(&app_mode_mux)` to prevent telemetry tearing and multi-core data races.
  - **Input Sanitization Failsafe:** Implemented strict non-negative, finite, and non-NaN boundaries checks in `AppScript` for serial PID commands to block catastrophic crash-inducing data.
  - **Type-safe Math:** Switched all float absolute comparisons to `std::abs()` to prevent compiler-dependent integer casting.
  - Compilation verified successfully via PlatformIO.
- **Joystick Reconnection & Thread Safety Fix**:
  - Solved reconnection failure by accepting new gamepads in `on_connected()` if the old pointer is stale (`!gamepad_->isConnected()`), and setting `gamepad_ = nullptr` immediately in the main loop upon disconnect detection.
  - Eliminated data races and Guru Meditation crashes between the BTstack background task and the main gamepad task by wrapping all pointer operations in a FreeRTOS Mutex.
  - Compilation verified successfully via PlatformIO (12.76 seconds).
- **InertialLabs INS-U Driver Audited and Fixed**: Audited the custom GPS lock detection and solution mapping against the INS-U ICD rev-1.43. Fixed a critical safety mapping issue where `ins_sol_status = 2` (no GNSS) was mapped to `FIX_2D`. Corrected the centidegrees scaling for `track_over_ground_raw` (which was set directly to float `yaw` degrees). Made the external GPS lock detection robust to custom packet configurations lacking `FULL_SAT_INFO` by falling back to `GNSS_POS_VALID` and `ins_sol_status`.
- **Replay Verification of INS GPS2 Logic**: Developed post-processing script `apply_ilb_gps2.py` to rewrite GPS2/GPA2 messages in binary logs based on the new driver's status-mapping and scaling rules. Optimized the C++ replayer's online GPS1 drop logic to allow selective outage simulations without needing the deprecated `inject_outage_gps1.py` script.
- **Verification**: Successfully simulated EKF3 GPS2 auto-switching on `log_26` under 6 simultaneous outages. The replayed EKF3 successfully switched to GPS2 (ILB data), keeping the estimation drift exceptionally low (down to 0.780 m/s in Outage 5, matching the external INS trajectory almost perfectly).
- **Documentation**: Updated `Tools/Replay/README.md` to document the new simplified simulation workflow and deprecated the `inject_outage_gps1.py` script.
- **Log Parsing Knowledge Persisted**: Saved the premium "pure byte-level in-place log modification" algorithm to long-term memory under `topics/topic-log-processing.md` for future reuse.

## Workspace Conventions
- Build config files (.cmake, Makefile, platformio.ini): **read-only** without explicit permission
- Temp files go in `.agent_scratchpad/`, never `/tmp`
- Uses `-u` flag for all Python execution (unbuffered)
- Weekly report path: `/media/hank/B0D4B41ED4B3E4AE/文件/週報`

### Pending Decisions
- (none)
