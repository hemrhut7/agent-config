# ArduPilot Compilation Guide (waf)

Guidelines for building ArduPilot Plane firmware.

## 1. Supported Build Environments
Ensure you compile and verify on both flight controller and SITL boards:
- **SITL (Simulation)**: `./waf configure --board sitl && ./waf plane`
- **Physical Board**: `./waf configure --board CubeOrangePlus-CIRC && ./waf plane`

## 2. Compilation Strategy
- **Minimize Logging**: Redirect output to prevent terminal buffer overflows:
  ```bash
  ./waf plane > build_log.txt 2>&1 &
  ```
- **State Monitoring**:
  - Poll the background compile process status every 5 seconds.
  - CPU usage will remain high while `Compiling` is active.
  - Check return code: `0` = Success, non-zero = Failure.

## 3. Fallback Plan
- **On First Failure**: Execute a clean configuration to resolve stale objects:
  ```bash
  ./waf clean
  ./waf configure --board <board_name>
  ./waf plane > build_log.txt 2>&1 &
  ```
- **On Second Failure**: Do not retry. Jump to [troubleshooting/ardupilot.md](../troubleshooting/ardupilot.md).
