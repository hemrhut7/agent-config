<!-- SCOPE: Knowledge about gps. Read when related tasks arise. -->
# Gps

### [2026-05-22 17:43] Tags: gps, ekf
ArduPilot GPS switchover logic summary: 1. AP_GPS: update_primary() selects primary_instance based on GPS_AUTO_SWITCH. A failure (timeout > 2s or quality drop) triggers a switch to GPS 2. 2. EKF3: update_gps_selection() updates selected_gps. In SelectVelPosFusion(), gpsDataDelayed.sensor_idx != last_gps_idx triggers ResetPositionNE() (and ResetPositionD() if GPS is height source) to align states with the new GPS position, compensating the jump in output observer to prevent control spikes.
