<!-- SCOPE: Knowledge about telemetry. Read when related tasks arise. -->
# Telemetry

### [2026-05-30 09:15] Tags: telemetry, udp, lidar
1. UDP Lidar Fragmentation Optimization: Bypassed manual application-level chunking in src/hal/hal_telemetry.cpp by expanding the static buffer to 4.7KB and letting LwIP handle IP fragmentation. This guarantees atomic delivery of full Lidar scans (512 points) and eliminates alignment shifts (byte shifts).
2. Lidar UART RX Buffer Expansion: Configured Serial2.setRxBufferSize(1024) in src/main.cpp before calling egin(). This provides a 44ms buffer window (at 230400 bps), protecting from buffer overflows when Core 0 is temporarily blocked by UDP/Wi-Fi operations.
