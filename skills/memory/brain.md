<!-- SCOPE: Today's task log and working memory. Read at conversation start to resume context. -->
# Brain — Working Memory

## Last Updated: 2026-05-26 09:58

### Active Tasks
- [x] Resolve EKF analysis log truncation
- [x] Implement robust log header resynchronization in DataFlashFileReader
- [x] Fix orchestrator path resolution to prioritize SITL target binary
- [x] Correct flight mode label clipping in plot analyzer
- [x] Audit and fix InertialLabs INS-U external AHRS driver (track_over_ground scaling, fix mapping, GPS lock detection)
- [x] Verify GPS2 mapping logic via log post-processing and EKF3 Replay
- [x] Verify and implement GPS auto-switching logic in EKF3 Replay

### Session Notes
- **InertialLabs INS-U Driver Audited and Fixed**: Audited the custom GPS lock detection and solution mapping against the INS-U ICD rev-1.43. Fixed a critical safety mapping issue where `ins_sol_status = 2` (no GNSS) was mapped to `FIX_2D`. Corrected the centidegrees scaling for `track_over_ground_raw` (which was set directly to float `yaw` degrees). Made the external GPS lock detection robust to custom packet configurations lacking `FULL_SAT_INFO` by falling back to `GNSS_POS_VALID` and `ins_sol_status`.
- **Replay Verification of INS GPS2 Logic**: Developed post-processing script `apply_ilb_gps2.py` to rewrite GPS2/GPA2 messages in binary logs based on the new driver's status-mapping and scaling rules. Ran successful offline EKF3 replay and comparative analysis on `log_17`, confirming stable EKF3 dead-reckoning (3.25 m/s drift) during a 212-second simulated outage.
- **Orchestrator Argument Extension**: Fixed an argument parsing limitation in `AP_Replay_Orchestrator.py` by adding support for `--parm` command line argument, allowing users to override vehicle parameters (e.g. `--parm GPS_AUTO_SWITCH=4`) dynamically during re-simulation.
- **Log Header Corruption Resolved**: Implemented a resilient byte-by-byte resynchronization loop in `AP_LoggerFileReader::update` within `Tools/Replay/DataFlashFileReader.cpp`. The replayer now skips corrupted frames/headers and resumes reading, successfully parsing the entire log timeline (4821s vs. previously being cut off at ~3000s).
- **Orchestrator Target Priority**: Prioritized `build/sitl/tool/Replay` over `build/linux/tool/Replay` in `AP_Replay_Orchestrator.py` because the Linux target version checks serial/GPIO arguments first and exits on custom arguments like `--outage`.
- **Plot Labels Fixed**: Shifted flight mode labels to `y=0.95` inside the plot boundaries in `AP_ILB_Replay_Analyzer.py` to prevent text truncation.
- **Verification**: Successfully replayed and analyzed 6 simulated outages simultaneously covering the full 4821.74s timeline.
- **Log Parsing Knowledge Persisted**: Saved the premium "pure byte-level in-place log modification" algorithm to long-term memory under `topics/topic-log-parsing.md` for future reuse.
## Workspace Conventions
- Build config files (.cmake, Makefile, platformio.ini): **read-only** without explicit permission
- Temp files go in `.agent_scratchpad/`, never `/tmp`
- Uses `-u` flag for all Python execution (unbuffered)
- Weekly report path: `/media/hank/B0D4B41ED4B3E4AE/文件/週報`

### Pending Decisions
- (none)
