<!-- SCOPE: Knowledge about user_preference. Read when related tasks arise. -->
# User_Preference

### [2026-05-15 16:39] Tags: user_preference, baseline, LSM
- **Estimation Philosophy**: Prefers Global Batch Least Squares (Scheme C/Factor Graph) with IMU pre-integration for baseline data generation.\n- **Initialization Rule**: Avoid using EKF results for initializing baseline smoothing to prevent feedback loops. Use sensor-based initialization (accLeveling + GPS diff).\n- **Parameter Observation**: Explicitly track GNSS delay, wind states, and airspeed parameters in global optimization.
