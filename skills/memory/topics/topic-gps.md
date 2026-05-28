<!-- SCOPE: Knowledge about GPS switchover and EKF integration. -->
# GPS

### [2026-05-22] Switchover Logic
1. **AP_GPS Selection**: `update_primary()` selects instance based on `GPS_AUTO_SWITCH`. Failure (timeout > 2s) triggers switch.
2. **EKF3 Alignment**: `update_gps_selection()` detects index change. `ResetPositionNE()` (and `ResetPositionD`) align states with new GPS position to prevent control spikes.
