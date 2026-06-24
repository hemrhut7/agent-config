<!-- SCOPE: Today's task log and working memory. Read at conversation start to resume context. -->
# Brain — Working Memory

## Last Updated: 2026-06-21 23:25

### Achievements (IMU ICM20948 Migration & 400Hz Loop Optimization)
- **Migrated IMU Driver to ICM20948**: Replaced MPU6050 with ICM20948 driver supporting secondary I2C access for the AK09916 magnetometer.
- **Added BMP280 Barometer and AK09916 Magnetometer Drivers**: Implemented robust reading interfaces for pressure, temperature, altitude, and magnetic field.
- **Upgraded Control Task Scheduler to 400Hz**: Utilized microsecond-precision hardware-backed `esp_timer` and binary semaphores to unblock the Control Task at exactly 400Hz, bypassing FreeRTOS 1ms tick limitations.
- **Configured Magnetometer to 20Hz & Barometer to 10Hz**: Scheduled sensor updates inside `CommTask` at modulo offsets.
- **Achieved Stable 400.00Hz Control Loop**: Transitioned the timer synchronization to a counting semaphore to allow the control task to catch up immediately after brief I2C bus locks, achieving a perfect, jitter-resistant 400.00Hz rate.
- **Implemented Shared I2C Mutex & Timing Optimization**: Added a shared mutex to protect the I2C bus from concurrent access collisions between the control and communication tasks, and optimized secondary I2C master transaction wait times to 1.0ms (reads) and 500us (writes).
- **Verified System Stability**: Checked loop rate telemetry showing stable 400Hz frequency and verified magnetometer and barometer data rates are exactly 20Hz and 10Hz respectively, with no watchdog triggers. Committed changes under git hash `e242a6a`.

### Active Tasks
- (See project-specific tasks in [task/INS_Reader.md](task/INS_Reader.md))
### Session Notes
- (fresh session)

### Pending Decisions
- (none)
