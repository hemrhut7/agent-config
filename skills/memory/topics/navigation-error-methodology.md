<!-- SCOPE: Methodology for EKF and External INS tracking error analysis. Read when updating error projection or analyzing drift. -->
# Navigation Tracking Error Methodology & Preferences

### [2026-05-20 09:28] Tags: navigation-error, coordinate-projection, llh2enu, analysis-preferences

To evaluate navigation system tracking accuracy (especially during GNSS-denied/jamming scenarios) over long flight ranges, the following logic and conventions must be used:

1. **Avoid XKF1 Direct Comparison**
   * **Issue**: The EKF's internal `XKF1` (PN/PE/PD) Cartesian outputs are computed in the EKF's internal frame, which diverges from a standard flat-earth tangent plane (`llh2enu`) over long distances. Direct comparison between `XKF1` (PN/PE) and standard flat-earth projected External INS (ILB3) coordinates produces a ~39m tracking error at 20.4 km range.
   * **Solution**: Extract true geodetic data from the EKF's `POS` (Lat/Lng/Alt) message and project both EKF and External INS trajectories using the exact same standard `llh2enu` projection. This cancels out common-mode map projection distortions, showing the true physical tracking error (~6.18 m).

2. **Analysis Scope & Telemetry Exclusions**
   * **Active Flight segment**: Crop analysis based on ground speed (> 5 m/s) to isolate active flight, avoiding takeoff ground run and post-landing taxi.
   * **Excluded Telemetry**: Exclude differential pressure (`DiffPress`) and calibrated airspeed (`CAS`) from the final report structure to focus purely on positional tracking, attitude RMSE, and true/indicated airspeed scaling (`TAS` / `ARSPD_SF`).
   * **Weekly Report Focus**: Prioritize log analysis of recent data files (within the last 2 months).

3. **Relative Height baseline Calibration**
   * **Issue**: Vertical offset jumps can occur due to static initialization differences between EKF and External INS.
   * **Solution**: Subtract the first point's altitude to align the vertical baselines. This isolates active vertical drift from initial static offsets.
