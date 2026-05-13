---
name: build-ardupilot-plane
description: "Build Ardupilot Plane firmware using waf, featuring state monitoring and automated error analysis. Prioritizes incremental compilation and optimizes output handling to prevent Terminal hanging. Trigger whenever the user asks to compile Ardupilot, build plane firmware, or run waf commands."
---

# Build Ardupilot Plane Skill (Monitored Version)

This skill is designed specifically for large-scale Ardupilot compilations, solving the issue of Agent response interruptions caused by verbose outputs.

## Execution Logic

### 1. Start Compilation (Asynchronous Optimization)
- **Command Execution**: Execute `./waf configure --board sitl && ./waf plane`, as well as `./waf configure --board CubeOrangePlus-CIRC && ./waf plane`, to ensure it can compile successfully in both physical flight controller and SITL environments.
- **Log Output**: It is recommended to redirect output to a temporary log file, or use the `--summary` flag (if supported) to reduce real-time text flow.
- **Prevent Hanging**: The Agent should avoid reading thousands of lines of compilation output line-by-line; instead, adopt a "tracking mode".

### 2. State Monitoring (5-second cycle)
During the compilation execution, the Agent must maintain the following monitoring cycle:
- **Heartbeat Check**: Confirm whether the background process is still running every 5 seconds.
- **State Determination**:
  - **Compiling**: Process activity is normal and CPU has load.
  - **Compilation Complete**: Process ended and return code is 0.
  - **Compilation Error**: Process ended and return code is not 0.

### 3. Exception Handling and Fallback
- **First Failure**: If `./waf plane` reports an error, automatically execute `./waf clean` and try `./waf plane` again.
- **Second Failure**: If it still fails after retrying, enter "Error Analysis Mode".

### 4. Error Analysis Mode
When compilation is interrupted, the Agent **should NOT read the entire log**, but instead:
- **Keyword Extraction**: Only capture the last 50-100 lines of the log.
- **Feature Search**: Look for `error:`, `fatal error:`, or `recipe for target ... failed`.
- **Cause Analysis**: Provide advice (in Traditional Chinese) regarding missing dependencies, syntax errors, or path issues.

## Command Suggestions (Prevent Buffer Overflow)
```bash
# It is recommended to minimize output or run in background
./waf plane > build_log.txt 2>&1 &
```