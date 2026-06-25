<!-- SCOPE: Today's task log and working memory. Read at conversation start to resume context. -->
# Brain — Working Memory

## Last Updated: 2026-06-24 15:15

### Achievements (I2C Integrity, Telemetry Sync, Log Preprocessing & EKF Tester Performance)
- **Verified I2C Wiring Integrity**: Reset and monitored serial console output; confirmed `ICM20948` IMU, `AK09916` Magnetometer, and `BMP280` Barometer all initialize and communicate successfully, verifying that SDA and SCL are wired correctly.
- **Removed Altitude Telemetry**: Removed `baro_data.altitude` from `FORMAT_DEFAULT` and `FORMAT_LIDAR` frames in `src/hal/hal_telemetry.cpp`, shrinking telemetry payload arrays from 25 to 24 floats and correctly shifting the checksum to index 23.
- **Upgraded IMU ODR to 562.5Hz**: Modified register configuration in `src/hal/hal_imu.cpp` by setting `GYRO_SMPLRT_DIV` and `ACCEL_SMPLRT_DIV` to `0x01` (divider = 1), raising gyroscope and accelerometer physical ODRs to 562.5Hz (from 225Hz) while keeping DLPF cutoff frequencies at 50.4Hz to prevent duplicate frames in the 400Hz control loop.
- **Synchronized Python Telemetry Receiver**: Resolved packet unpacking errors in [ABC.py](file:///C:/Users/hemrh/Documents/GitHub/Python/INS_Reader/src/connector/ABC.py) by updating `ABCReader` and `ABCReader_UDP` to parse 24-float packets (23 data floats + 1 checksum float) instead of the outdated 19-float format.
- **Refactored Python Telemetry Receiver to be Fully Dynamic**: Updated [ABC.py](file:///C:/Users/hemrh/Documents/GitHub/Python/INS_Reader/src/connector/ABC.py) so that `num_base_floats`, `payload_len`, `packet_len`, unpacking offsets, and `unpack_fmt` are dynamically computed based on `len(ABC_HEADER_NORMAL)` and `len(ABC_HEADER_PID)`. This ensures that any future modifications to the headers will automatically adjust the decoding parameters without requiring code edits in the parsing logic.
- **Successfully Built and Flashed Firmware**: PlatformIO build succeeded and was uploaded to COM7.
- **Preprocessed Log 146**: Extracted raw sensor logs from [log_146_20260622.bin](file:///home/hank/文件/Python/INS_python/data/ILB-logger/log_146_20260622.bin) (696MB) using [AP_INS_log_extractor.py](file:///home/hank/文件/Python/INS_python/tools/AP_INS_log_extractor.py).
- **Generated CSV Datasets**: Produced 15 structured CSV files (including IMU, Magnetometer, Barometer, Mode, etc.) in the [seg_0](file:///home/hank/文件/Python/INS_python/data/ILB-logger/log_146_20260622/seg_0) folder.
- **Optimized EKF Testers Data Loading**: Replaced inefficient `pd.read_csv` with `load_csv_or_npz` and `np.load` on the `.npz` binary cache to retrieve log bounds and durations. Reduced manual and default outage testing overhead from minutes to seconds.

## Last Updated: 2026-06-18 18:15

### Achievements (InertialLabs ExternalAHRS HDOP/VDOP Scale Factor Fix)
- **Fixed ExternalAHRS InertialLabs HDOP/VDOP Conversion Bug**: Corrected the conversion factor for HDOP and VDOP from `*0.1f` to `*0.001f` in [AP_ExternalAHRS_InertialLabs.cpp](file:///home/hank/CIRC_Ardupilot/libraries/AP_ExternalAHRS/AP_ExternalAHRS_InertialLabs.cpp#L602-L603) inside `check_uart()`. Since InertialLabs raw values are scaled by `1000` (e.g. `1200` represents an HDOP of `1.2`), and the generic AP_GPS handler `AP_GPS_ExternalAHRS` scales it by `100` (`state.hdop = pkt.hdop * 100`), the original `*0.1f` factor caused the resulting HDOP/VDOP inside ArduPilot to be scaled up by 100x (e.g., `12000` instead of `120`). Verified correct compilation of `arduplane` (`./waf plane`) with zero errors.

## Last Updated: 2026-06-17 15:22

### Achievements (MAVLinkWidget QMessageBox Dialog Blank Text Fix)
- **Fixed QMessageBox Blank Text in MAVLinkWidget**: Added explicit QSS styling rules for `QMessageBox` and its child components inside the `MAVLinkWidget` stylesheet in [MainWidgets.py](file:///home/hank/文件/Python/INS_Reader/src/widgets/MainWidgets.py). This overrides the inherited global `QLabel { color: #F8FAFC; }` rule, setting a matching dark theme background (`#1E293B`) and readable white text (`#F8FAFC`) for dialog labels and styling the buttons, ensuring confirmation prompts are fully visible and consistent with the interface style.

### Active Tasks
- (none)

### Session Notes
- Preprocessed large binary log (696MB) containing 12,265,321 messages. Fast parallel parsing mode succeeded.
- Resolved pack/unpack size mismatch by dynamically styling and parsing packet sizes dynamically.

### Pending Decisions
- (none)
