---
name: firmware-compilation
description: "Compile and build embedded firmware projects (ArduPilot Plane using waf, PlatformIO projects using pio run), featuring state monitoring, clean recovery, and automated error analysis."
---

# Firmware Compilation Skill

This skill governs the compilation and building of embedded firmware projects. To prevent terminal hanging and maintain structured workflow execution, it provides progressive access to specific platform compilation details.

## 1. Trigger & Platform Selection

When invoked to build or compile a project, identify the target platform and navigate to its dedicated sub-file:

| Target Platform | Trigger Conditions | Compilation Guide | Troubleshooting |
| :--- | :--- | :--- | :--- |
| **ArduPilot (waf)** | Contains `waf`, `AP_HAL`, or requests to compile Plane | [platforms/ardupilot.md](platforms/ardupilot.md) | [troubleshooting/ardupilot.md](troubleshooting/ardupilot.md) |
| **PlatformIO (pio)** | Contains `platformio.ini`, `pio run`, or `.ino`/`.cpp` hardware files | [platforms/platformio.md](platforms/platformio.md) | [troubleshooting/platformio.md](troubleshooting/platformio.md) |

## 2. Core Operational Principles (Anti-Hang)

Regardless of the platform, the following execution standards MUST be applied to prevent terminal locks and response timeouts:

- **Incremental Priority**: Always try incremental compilation first; only use clean builds (`waf clean` or `pio run -t clean`) as a recovery step.
- **Asynchronous Execution & Monitoring**: For builds expected to exceed 10 seconds, run the build command in the background, redirecting stdout to a temporary log file (e.g. `> build_log.txt 2>&1 &`). Check the background process status every 5 seconds.
- **Strict Output Limit**: Never read or stream the full compilation log to the active context. If compilation fails, extract and analyze only the final 50–100 lines.
