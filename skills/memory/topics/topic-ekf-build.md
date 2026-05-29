<!-- SCOPE: Technical details of ArduPilot EKF standalone build. Read during compilation tasks. -->
# ArduPilot EKF Standalone Build

### [2026-05-15 22:05] Tags: ekf, compilation, dll, ardupilot, mingw
## Status: In Progress (Logic Refinement)

### Architecture
- **Build System**: Custom `build_ekf.py` using `g++` (UCRT64/MinGW).
- **Core Library**: `AP_NavEKF3` core logic.
- **Abstraction**: Uses `AP_DAL` (Data Abstraction Layer) to decouple from physical hardware.
- **Interface**: `NavEKF3_Interface.cpp` exports `extern "C"` functions for Python `ctypes` integration.

### Key Refactorings
- **Circular Dependency Fix**: 
    - Moved `HAL_WITH_EKF_DOUBLE` to `AP_HAL/HAL_Config.h`.
    - Centralized math typedefs in `AP_Math/AP_Math_Types.h`.
    - Removed `AP_Common.h` from math headers; replaced with `ftype.h` + `WARN_IF_UNUSED` fallback.
- **Stubbed Components**:
    - `GCS_MAVLink/GCS.h`: Macro stubs for text logging.
    - `AP_AHRS`: Minimal class for EAS2TAS and status.
    - `Logger`: No-op data logging for standalone mode.
    - `AP_NavEKF_Source`: Enum and bitmask configuration for sensor sources.

### Known Pitfalls
- **APM_BUILD_TYPE**: ArduPilot core uses this macro for conditional logic (e.g., `ArduSub`). Must be defined to `(0)` for standalone or specific values if sub-logic is needed.
- **Matrix Kfusion/KH/KHP**: These matrices are used across fusion files (`PosVelFusion`, `RngBcnFusion`) and must be defined as members of `NavEKF3_core` in `AP_NavEKF3_core.h`.
- **Location methods**: `get_distance_NE_ftype` and `offset` must be implemented in `Location.cpp` to avoid circular dependency in headers.

### Resume Checklist
1. **AP_NavEKF3_VehicleStatus.cpp**: Resolve `APM_BUILD_TYPE(APM_BUILD_ArduSub)` error (line 387). Fix by defining `APM_BUILD_TYPE(x)` to always return false or a specific constant in `AP_HAL_Macros.h`.
2. **AP_BoardConfig**: Ensure `namespace AP_BoardConfig` in `AP_BoardConfig.h` is used consistently and doesn't conflict with any class definitions.
3. **Linker Phase**: Check `NavEKF3_Interface.cpp` for any missing exports. Ensure `init_ekf`, `inject_imu`, `inject_gps` are correctly visible to Python.
4. **Python Bridge**: Verify `MyLib/Navigation/ArduPilotEKF.py` maps to the new DLL functions.

### Next Command
```bash
python build_ekf.py > build_log.txt 2>&1
# Then search for errors:
Select-String "error:" build_log.txt | select -first 10
```
