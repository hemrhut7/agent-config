<!-- SCOPE: Knowledge about ExternalAHRS. Read when related tasks arise. -->
# Externalahrs

### [2026-06-29 09:07] Tags: ExternalAHRS, fallback, InertialLabs, Copter, VTOL
Implemented automatic EKF3 fallback for ExternalAHRS (AHRS_EKF_TYPE=11) under Copter and VTOL Q-mode. Added virtual gps_is_healthy() method to AP_ExternalAHRS_backend base class. Implemented gps_is_healthy() in AP_ExternalAHRS_InertialLabs using GNSS_FAIL, GNSS_FUSION_OFF, gnss_sol_status, and last_gps_ms freshness. Updated AP_AHRS::_active_EKF_type() to fallback from EXTERNAL to THREE (EKF3) if the vehicle is Copter or VTOL Q-mode and gps_is_healthy() returns false. Verified by compiling SITL successfully.
