<!-- SCOPE: Knowledge about ekf. Read when related tasks arise. -->
# Ekf

### [2026-05-18 12:53] Tags: ekf, architecture-sync, bugfix
### EKF Architecture Sync & Bugfix (2026-05-18)
- Status: Successfully synchronized modify-project-structure branch with master logic.
- Key Changes:
    - Reverted state indexing in nav_ekf/filters/nav_state.py to match master: Wind (22-23), Gravity (15), SF (16-21).
    - Disabled Schmidt-Kalman Filter (active_mask) in INS_GNSS for consistency.
    - Reverted covariance update from Joseph Form to Standard Form.
    - Commented out new features (Dynamic R, GPS Yaw Fallback, Wind Jacobian in SideSlip) to isolate architecture changes.
- Validation:
    - EKFTester_20251120.py results are identical to master.
    - ArduPilotTester.py results differ by less than 1% due to data extractor numerical handling.
- Pitfall: Fixed NameError: base_dir in ArduPilot_ILB_GNSS-denied_Tester.py.
