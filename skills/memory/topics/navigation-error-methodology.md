<!-- SCOPE: Methodology for EKF and External INS tracking error analysis. -->
# Navigation Tracking Error Methodology

### [2026-05-20] Coordinate Projection (LLH vs XKF1)
- **Issue**: EKF internal `XKF1` frame diverges from flat-earth `llh2enu` over distance (~39m error at 20km).
- **Solution**: Extract Geodetic `POS` (Lat/Lng/Alt) from log; project both EKF and External INS using identical `llh2enu`.

### [2026-05-20] Analysis Scope & Telemetry
- **Active Flight Only**: Crop data where ground speed > 5 m/s.
- **Exclusions**: Focus on position, attitude, and TAS/ARSPD scaling; exclude `DiffPress` and `CAS`.
- **Recency**: Prioritize logs from the last 2 months.

### [2026-05-20] Vertical Baseline Calibration
- **Issue**: Static initialization differences cause vertical offsets.
- **Solution**: Zero-base altitudes by subtracting the first point's value to isolate active drift.

### [2026-05-28] Replay Origin Offset
- **Issue**: Replay (Core 100) and Flight (Core 0) initialize origins at different times/locations (e.g., 26m horizontal offset).
- **Solution**: Align PN/PE/PD trajectories by shifting replay coordinates to match flight's initial position.