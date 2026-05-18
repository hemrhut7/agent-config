<!-- SCOPE: Today's task log and working memory. Read at conversation start to resume context. -->
# Brain — Working Memory

## Last Updated: 2026-05-18 13:19

### Active Tasks
- [x] Custom EKF3 Replay Engine Implementation & Validation
- [x] Dynamic Output File Naming & Git Commit Execution

### Session Notes
- Memory skill system successfully utilized.
- **Critical Discovery**: Real flight logs include all message definitions (including native DAL types like `RISI`, `RFRF`) in the header blocks. This caused `has_native_dal` to trigger `true` even on standard logs.
- **Implemented Fix**: We introduced parameter-based dynamic mode selection (reads `LOG_REPLAY=1` to switch to native mode, otherwise uses synthetic sensor feeds).
- **Orchestrator Developed**: Built `AP_Replay_Orchestrator.py` which compiles `Replay`, runs execution, and performs pymavlink-based RMSE drift evaluation and plotting.
- **Dynamic File Naming**: Modified Python orchestrator to dynamically rename replayed `.bin` logs to `[original_name]_outage[time].bin` (e.g. `_outage150-200.bin` or `_outage0.bin` if no outage simulated).
- **Git Commit**: Successfully committed all EKF3 offline replay engine core source files, python orchestrator, and README user guide under Conventional Commits `feat(replay)`.
- **Results**: Replayed trajectory matches original flight within <6.0m max drift. Simulating a 50s GPS outage shows robust dead-reckoning (<72m horizontal drift).

### Pending Decisions
- None. System is fully operational, verified, and successfully version-controlled!
