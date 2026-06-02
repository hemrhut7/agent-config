<!-- SCOPE: Knowledge about log-parsing, byte-level modification, parallel binary unpacking, and parser pitfalls. -->
# Log-Parsing and Processing

### [2026-05-26 16:47] Tags: log-parsing, byte-level, python-mmap
#### Fast Byte-level In-place Log Modification
For processing large ArduPilot DataFlash binary logs (.bin), traditional parser libraries (like pymavlink DFReader) can be very slow due to Python object instantiation overhead.

##### Optimization Pattern:
1. **Memory Load**: Read the entire file into a mutable `bytearray`.
2. **Dynamic Format Parsing**: Scan FMT messages at the beginning of the file (sync bytes: `0xA3, 0x95`, message type: `128`). Map `msg_type_id` to its length, column list, and formats.
3. **Byte-level Navigation**: Move pointer `idx` directly by `msg_len` to avoid parsing skipped messages.
4. **In-place Rewrite**: Access payload using `struct.unpack_from` and write changes back instantly via `struct.pack_into`.
5. **Int Overflow Wrapping**: Custom `safe_pack_value` mask bits (e.g., `& 0xFFFF`) to mimic hardware behavior and prevent `struct.error` exceptions when values exceed int limits.

### [2026-05-26 16:49] Tags: log-parsing, parallel-processing, multiprocessing
#### Parallel Binary Unpacking (ProcessPoolExecutor + mmap)
For read-only data analysis of large logs, multi-process parallel binary unpacking maximizes CPU core utilization.

##### Pattern:
- **Chunking**: Get all message offsets using `mlog.offsets[tid]`. Split offsets list into chunks based on CPU cores.
- **Workers**: Each process maps the file using `mmap` (read-only), uses `struct.unpack_from` on the chunk of offsets, and returns raw data lists.
- **Aggregation**: Collect results in the main process and build Pandas DataFrames for plotting or computation.

#### Comparison Matrix

| Method | State Dependency | Operation Type | Performance Bottleneck | Best For |
| :--- | :--- | :--- | :--- | :--- |
| **Byte-level In-place** | Stateful (requires sequential time states) | Read/Write (In-place) | Single-threaded CPU | Log injection, sensor outage simulation |
| **ProcessPoolExecutor** | Stateless (independent chunks) | Read-only | Multi-process IPC overhead | Trajectory comparison, statistics, plotting |

### [2026-05-18 18:13] Tags: log-replay, dynamic-scaling
#### High-Performance Replay Decoding
Integrated method for mapping and decoding 1.9GB+ logs in ~1.2s:
- **Cython Offset Mapping**: Uses `mlog.offsets[tid]` for immediate message localization.
- **Parallel Decoding**: `mmap` + `ProcessPoolExecutor` + `struct.unpack` to bypass GIL.
- **Vectorized Scaling**: Applies pymavlink scales directly in Pandas.
- **Dynamic Workers**: Set via `max(1, int(max(cpu_count - 4, cpu_count / 2)))` for optimal core usage (18 workers on 22-core system).
- **Robust Fallback**: Reverts to sequential `recv_match` on error.

### [2026-06-01 11:45] Tags: log-parsing, parse-log, pitfalls
#### Log Parser & Processing Pitfalls
- **AP_ILB_Replay_Analyzer.parse_log pitfall**: ILB1 raw messages include `IMS`, but if the ILB1 mapping omits it, `vibration_analysis_runner.get_time_offset_from_dfs()` cannot align high-rate and standard logs by IMS and falls back to a hardcoded/default offset.
  - *Fix*: Preserve `IMS` as `ims` in both high-performance and sequential ILB1 parsing.
- **Binary Parser EOF pitfall**: `mlog.offsets` can include a final/incomplete message near EOF. Before `struct.unpack`, compute expected body length with `struct.Struct(msg_struct).size` and skip offsets whose `body_start + body_len` exceeds file size; otherwise `unpack requires a buffer of N bytes` forces a slow sequential fallback.
- **FFT Segment analysis pitfall**: vibration FFT frequency axes are wrong if sample rate is estimated as `len(full_log) / full_log_duration` when the log has mid-file data gaps.
  - *Fix*: Split by large `time_us` gaps, use only each sensor's longest continuous segment, and estimate `fs` from the segment's median positive `dt`.
