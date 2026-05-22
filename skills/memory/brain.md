<!-- SCOPE: Today's task log and working memory. Read at conversation start to resume context. -->
# Brain — Working Memory

## Last Updated: 2026-05-22 09:15

### Active Tasks
- [x] Standardize command-line arguments for all log analysis tools (`INS_log_extractor.py`, `AP_ILB_Replay_Analyzer.py`, `plot_AP-EKF_ILB-INS.py`, `GNSS_Denied_Analysis.py`, `Attitude_Airspeed_Analysis.py`).
- [x] Re-organize default output directories to route to `output/<log_name>/` subfolders.
- [x] Implement robust candidate directory search paths for CSV logs when referencing relative paths.
- [x] Complete end-to-end verification of all five tools.
- [x] Update `tools/README.md` to reflect unified usage and options.

### Session Notes
- Standardized all tools on `--input` and `--out` CLI parameters.
- Re-organized analysis outputs to dynamically target `output/<log_name>/<analysis_type>_Analysis/`.
- Fixed a bug in `plot_AP-EKF_ILB-INS.py` where processing logs without InertialLabs EKF/INS replay data caused `NameError: name 't0' is not defined`.
- Verified all tools successfully via CLI on local logs.
- Documented new usage paradigms and formats in `tools/README.md`.

### Pending Decisions
- none
