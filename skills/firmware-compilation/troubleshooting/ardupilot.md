# ArduPilot Troubleshooting Reference

When waf compilation fails, follow this procedure to resolve compilation bottlenecks:

## 1. Error Analysis Procedure
1. **Never read the full log**. Extract only the last 50–100 lines using:
   ```bash
   tail -n 100 build_log.txt
   ```
2. Scan for key error signatures:
   - `error:`
   - `fatal error:`
   - `recipe for target ... failed`
3. Analyze and provide resolution advice (in **Traditional Chinese** / **繁體中文**).

## 2. Common Issues & Remediations
- **Missing Toolchain / Board Mismatch**: Check if target compiler is matching SITL/GCC compiler setups.
- **Header Circular Dependencies**: Refer to EKF circular dependency fix protocols (e.g. modifying `HAL_Config.h` or `AP_Math_Types.h`).
- **Waf Cache Issues**: Run `./waf clean` followed by `./waf configure` to rebuild project index caches.
