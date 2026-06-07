<!-- SCOPE: Hardware interfaces, telemetry protocols (UDP, MAVLink), and real-time control safety. -->
# Hardware & Telemetry

### [2026-05-30 09:15] Tags: telemetry, udp, lidar, buffer
- **UDP Fragmentation**: Bypassed manual chunking by expanding the static buffer to 4.7KB; LwIP handles IP fragmentation. Guarantees atomic delivery of 512-point Lidar scans.
- **RX Buffer**: Expanded Serial2 RX buffer to 1024 bytes. Protects against overflow when Core 0 is blocked by Wi-Fi/UDP tasks.

### [2026-06-06 15:10] Tags: hardware, safety, control
- **Bumpless Transfer**: Implemented proportional scaling of integral accumulator when KI changes in `PID::setTunings`. Prevents control sags during deactivation.
- **Cross-Core Safety**: Wrapped sensitive writes/reads in FreeRTOS critical sections (`portENTER_CRITICAL`) to prevent telemetry tearing and multi-core races.
- **Input Sanitization**: Strict non-negative, finite, and non-NaN checks in `AppScript` for serial PID commands.
- **Joystick Safety**: Solved reconnection failures by checking `isConnected()` status. Wrapped BTstack operations in a Mutex to eliminate Guru Meditation crashes.

### [2026-06-06 15:10] Tags: note, daily-summary
- **Type-safe Math**: Use `std::abs()` for float comparisons to prevent incorrect integer casting.
