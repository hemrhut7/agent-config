<!-- SCOPE: Drivers (InertialLabs), Firmware (ArduPilot), and EKF integration. -->
# Drivers, Firmware & Integration

### [2026-05-15 22:05] Tags: ekf, ardupilot, compilation, dll
#### ArduPilot EKF Standalone Build
Custom `build_ekf.py` using `g++` (MinGW) to compile `AP_NavEKF3`.
- **Interface**: `NavEKF3_Interface.cpp` exports `extern "C"` for Python `ctypes`.
- **Refactoring**: Moved `HAL_WITH_EKF_DOUBLE` to `HAL_Config.h`. Centralized math typedefs in `AP_Math_Types.h`.
- **Pitfall**: `APM_BUILD_TYPE` must be defined to `(0)` for standalone.

### [2026-06-06 15:10] Tags: inertiallabs, driver, bugfix
#### InertialLabs INS-U Integration
- **Safety Fix**: Corrected mapping where `ins_sol_status = 2` (no GNSS) was incorrectly mapped to `FIX_2D`.
- **Scaling**: Applied `* 100.0f` to `track_over_ground_raw`. Centidegrees scaling fixed.
- **Unit Mismatch**: Fixed bug where raw lat/lon/alt accuracies (mm) were passed to AP_GPS without converting to meters.
- **Robustness**: Added `GNSS_POS_VALID` fallback for packets lacking `FULL_SAT_INFO`.

### [2026-06-06 15:10] Tags: ekf3, gps, failsafe
#### EKF3 GPS Switching & Recovery
- **Notification**: Added `GCS_SEND_TEXT` for primary GPS changes.
- **Drift Reset**: Reset `gpsDriftNE = 0.0f` and `gpsloc_prev` on GPS switch to eliminate 12s failsafe transient.
- **Recovery Time**: Reduced EKF stability recovery threshold to **2 seconds** (from 10s) if the new GPS is healthy. Total switch recovery time reduced from 32s to 4s.

### [2026-05-22] Tags: gps, switchover
`AP_GPS::update_primary()` selects instance based on `GPS_AUTO_SWITCH`. Timeout > 2s triggers switch. EKF3 `ResetPositionNE()` aligns states with new GPS to prevent control spikes.
