<!-- SCOPE: Today's task log and working memory. Read at conversation start to resume context. -->
# Brain — Working Memory

## Last Updated: 2026-05-22 09:15

### Active Tasks
- [x] Standardize command-line arguments for all log analysis tools (`INS_log_extractor.py`, `AP_ILB_Replay_Analyzer.py`, `plot_AP-EKF_ILB-INS.py`, `GNSS_Denied_Analysis.py`, `Attitude_Airspeed_Analysis.py`).
- [x] Re-organize default output directories to route to `output/<log_name>/` subfolders.
- [x] Implement robust candidate directory search paths for CSV logs when referencing relative paths.
- [x] Complete end-to-end verification of all five tools.
- [x] Update `tools/README.md` to reflect unified usage and options.
- [x] Port parallel high-performance binary parsing to `LogPlotter.py` and fix the `mlog.offsets` list AttributeError bug.
- [x] Analyze and fix the ILB gyroscope unit mismatch (57.3x scaling bug) in `AP_ILB_Replay_Analyzer.py`.
- [x] Modify `vibration_analysis_runner.py` to use the longest continuous segments for all analyses, crop ILB data to the IMU0 segment window, and remove the vibration trend and rate aliasing comparison plots.
- [x] Implement ArduPilot-style dynamic filtered vibration calculation and plotting in `tools/vibration_analysis_runner.py`.

### Session Notes
- Standardized all tools on `--input` and `--out` CLI parameters.
- Re-organized analysis outputs to dynamically target `output/<log_name>/<analysis_type>_Analysis/`.
- Fixed a bug in `plot_AP-EKF_ILB-INS.py` where processing logs without InertialLabs EKF/INS replay data caused `NameError: name 't0' is not defined`.
- Verified all tools successfully via CLI on local logs.
- Documented new usage paradigms and formats in `tools/README.md`.
- Implemented high-performance binary file parsing (mmap, struct) in `LogPlotter.py`.
- Fixed the `AttributeError: 'list' object has no attribute 'get'` in `LogPlotter.py` by using index boundary check + list indexing. Verified speedup and correct behavior on real BIN logs.
- Fixed a gyroscope unit mismatch bug in `AP_ILB_Replay_Analyzer.py` where the ILB1 native gyroscope values (already in rad/s in the log) were incorrectly scaled by `np.radians` again. Removing the redundant conversion matches the AP IMU scale (e.g. standard deviation of ~9.5 deg/s vs ~6.2 deg/s) and fixes EKF vs ILB comparisons.
- Modified `tools/vibration_analysis_runner.py` to:
  - Extract the longest continuous segment for the master reference sensor (`IMU0`) first.
  - Crop all other sensors' DataFrames (`IMU1`, `IMU2`, high-rate ILB, standard-rate ILB) to this master segment window to enforce temporal alignment.
  - Extract the longest continuous segments from the cropped DataFrames for all subsequent analyses, stats calculations, FFT computations, and overlay plots.
  - Suppressed generation of the vibration trend plot (`vibration_trends.png`) and rate aliasing comparison plot (`rate_aliasing_comparison.png`).
  - Updated the markdown report generator (`VIBRATION_REPORT.md`) to reflect these changes, removing references/sections for the deleted plots.
- Implemented ArduPilot-style dynamic low-pass filtered vibration calculation (`compute_ap_vibration`) using a 5.0 Hz floor LPF and 2.0 Hz vibration LPF to mirror `AP_InertialSensor.cpp` logic.
- Added generation of `vibration_levels_comparison.png` (a 2x2 subplot comparing X, Y, Z, and Mag vibration levels over time for all IMUs and the high-rate ILB log).
- Updated the report template in `tools/vibration_analysis_runner.py` to compile detailed per-axis and magnitude statistics under a new section "3. ArduPilot-Style Vibration Analysis (5Hz Floor / 2Hz Vibe LPF)" and embed the comparison plot, omitting the standard-rate ILB sensor from all vibration metrics, plots, and report tables.

### Pending Decisions
- none
