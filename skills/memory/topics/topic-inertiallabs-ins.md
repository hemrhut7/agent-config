<!-- SCOPE: Knowledge about H35 External INS (InertialLabs INS-U) integration status, drivers, and scaling. Read when analyzing INS data or configurations. -->
# InertialLabs INS-U Integration Status

### [2026-05-20 08:52] Tags: external-ins, attitude-alignment, gnss-denied, airspeed-calibration
#### H35 External INS Integration Status
Current status of external InertialLabs INS-U (ILB3/ILB9) integration with ArduPilot EKF3:
1. **Attitude Alignment Issues**:
   - **Roll**: High consistency between INS-U and ArduPilot EKF, with differences stabilizing within **1.0°** after takeoff.
   - **Pitch**: Displays a persistent **2.2° offset** between INS-U body frame and ArduPilot. This offset fluctuates dynamically during VTOL transition phases (rotary-wing to fixed-wing).
   - **Yaw (Heading)**: Experiences a significant jump of **10° to 20°** during fixed-wing transitions, which gradually converges back during steady-state cruise.
2. **Airspeed Calibration & Scale Factor**:
   - Airspeed estimates are highly consistent between ArduPilot and INS-U.
   - The INS-U airspeed scale factor (`ARSPD_SF`) consistently converges to approximately **1.06** during cruise.
3. **GNSS-Denied Outage Performance**:
   - During GNSS outages, positioning drift consistently diverges towards the **North-East** direction.
   - This drift matches the wind estimation errors (North wind estimation is 3-4 m/s, East wind is < 1 m/s), indicating that wind-estimation errors are a primary driver of translation drift during GNSS-denied phases.
   - **Projected Position Tracking Error**: By parsing the EKF's true geodetic data (`POS`) and projecting both EKF and External INS trajectories using standard `llh2enu`, the apparent ~39m error is resolved as a coordinate-projection artifact. The true physical tracking error is shown to be just **~6.18 m**.
4. **Parameters & Workarounds**:
   - **Workaround**: Manually pinning `ARSPD_SF` to **1.06** prevents the wind estimation loop from using poor scale factor convergence, reducing initial drift.
   - **MinAirSpeed**: Adjusted from **15 m/s to 20 m/s** to improve wind estimation robustness.
   - **INS-U Parameter Tuning**:
     - `SF_ERROR` (Scale Factor Error): Tuned from **0.00 to 0.06**.
     - `Speed Threshold` (Ground speed threshold for active flight): Tuned from **5.0 to 10.0 m/s**.
5. **External MAVLink FCM Migration**:
   - The communication protocol for the FCM extender board is being transitioned from a custom binary protocol to standard **MAVLink protocol**. Branch changes are prepared and pending validation.

### [2026-05-26] Tags: external-ins, inertiallabs, driver, bugfix
#### INS-U Driver Fixes
- **Status Mapping**: Corrected unsafe mapping of `solution status 2` (no GNSS) to `FIX_2D`.
- **Scaling**: Applied `* 100.0f` scaling to `track_over_ground_raw` (float yaw degrees).
- **Lock Detection**: Added `GNSS_POS_VALID` fallback for custom packets lacking `FULL_SAT_INFO`.
