<!-- SCOPE: Knowledge about pitfall. Read when related tasks arise. -->
# Pitfall

### [2026-05-15 16:39] Tags: pitfall, importerror
**Pitfall: ImportError**
- **Trigger**: cannot import name ENU2llh; TypeError: len() of unsized object in KF_Plot; AttributeError: MockKF missing my_EKF, device_name, reset_time"}
- **Fix**: (to be determined after root cause analysis)
- **Prevention**: (to be determined)

**Pitfall: Math Header Circular Dependency**
- **Trigger**: `Location.h` needs `Vector2F`, but `Vector2.h` needs `AP_Common.h`, which needs `Location.h`.
- **Fix**: Move `HAL_WITH_EKF_DOUBLE` to `HAL_Config.h`, centralize types in `AP_Math_Types.h`, and remove `AP_Common.h` from math headers (use `ftype.h` for macros).
- **Prevention**: Keep math headers leaf-like and avoid including global config headers if possible.

### [2026-05-17 21:41] Tags: pitfall, refactor
Refactoring global constants into module-level variables (e.g., EKF_params.py) can cause NameErrors in @njit decorated functions or other classes if not imported correctly. Always verify initialization paths and ensure core parameters like PARM_INIT_YAW are explicitly defined or imported in all relevant modules.
