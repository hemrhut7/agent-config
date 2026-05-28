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
- **Replay Verification of INS GPS2 Logic**: Developed post-processing script `apply_ilb_gps2.py` to rewrite GPS2/GPA2 messages in binary logs based on the new driver's status-mapping and scaling rules. Optimized the C++ replayer's online GPS1 drop logic to allow selective outage simulations without needing the deprecated `inject_outage_gps1.py` script (which has been removed).
- **Verification**: Successfully simulated EKF3 GPS2 auto-switching on `log_26` under 6 simultaneous outages. The replayed EKF3 successfully switched to GPS2 (ILB data), keeping the estimation drift exceptionally low (down to 0.780 m/s in Outage 5, matching the external INS trajectory almost perfectly).
- **Documentation**: Updated `Tools/Replay/README.md` to document the new simplified simulation workflow and deprecated the `inject_outage_gps1.py` script.
- **Log Parsing Knowledge Persisted**: Saved the premium "pure byte-level in-place log modification" algorithm to long-term memory under `topics/topic-log-processing.md` for future reuse.
## Workspace Conventions
- Build config files (.cmake, Makefile, platformio.ini): **read-only** without explicit permission
- Temp files go in `.agent_scratchpad/`, never `/tmp`
- Uses `-u` flag for all Python execution (unbuffered)
- Weekly report path: `/media/hank/B0D4B41ED4B3E4AE/文件/週報`

### Pending Decisions
- (none)
