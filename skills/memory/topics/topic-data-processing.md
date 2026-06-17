<!-- SCOPE: Log parsing, binary unpacking, and data analysis optimization. -->
# Data Processing & Log Analysis

### [2026-05-26 16:47] Tags: log-parsing, python-mmap, optimization
#### High-Performance Binary Log Parsing
For large ArduPilot .bin logs, use byte-level in-place modification or parallel unpacking.
- **Optimization**: Read into mutable `bytearray` or `mmap`. Scan `FMT` messages (`0xA3, 0x95, 128`).
- **Parallelism**: Use `ProcessPoolExecutor` with `mmap` for read-only trajectory analysis.
- **Aggregation**: Collect results into Pandas DataFrames. Apply pymavlink scales directly in Pandas.
- **Workers**: Set to `max(1, int(max(cpu_count - 4, cpu_count / 2)))` for optimal core usage.

### [2026-06-01 11:45] Tags: log-parsing, pitfalls
- **EOF Pitfall**: Skip offsets where `body_start + body_len` exceeds file size to avoid `struct.unpack` errors.
- **FFT Gap Pitfall**: Estimate `fs` from median positive `dt` in the longest continuous segment to avoid bias from data gaps.
- **IMS Alignment**: Preserve `IMS` in all parsing modes to ensure alignment between high-rate and standard logs.

### [2026-06-06 15:10] Tags: log-analysis, standardization
- **CLI Standard**: Standardized on `--input` and `--out` parameters. Outputs routed to `output/<log_name>/<analysis_type>_Analysis/`.
- **Scaling Fix**: Resolved ILB gyroscope double-conversion (57.3x) scaling bug in `AP_ILB_Replay_Analyzer.py`.

### [2026-06-11 14:55] Tags: memory-management, multiprocessing, plotting
#### Memory Safety & Core Count Guidelines for Large Data Simulations
Running EKF or SLAM simulations on massive flight datasets (e.g., >800MB log files) easily exhausts RAM and causes OS crashes due to Python's memory retention (especially in Matplotlib plotting and logger array allocations).
- **Core Allocation Guideline**: Suggest using **2-3 cores** for processing (depending on hardware performance) to balance computation time and memory usage.
- **Memory Risk Estimation**: If estimated memory usage per task is high relative to available RAM, fall back to sequential execution or reduce worker count.
- **Memory Optimization Strategies**:
  - Run massive dataset tasks in isolated subprocesses (via `subprocess.run`) so the OS fully reclaims memory upon subprocess exit.
  - Downsample high-rate logger data (e.g., decimate by 20) *only during plotting* to prevent Matplotlib from holding millions of points in memory.
  - Wrap plotting in try-except blocks to catch numerical divergence exceptions (e.g., coordinate layout calculations on `inf`/`nan`).

