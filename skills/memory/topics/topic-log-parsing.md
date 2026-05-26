<!-- SCOPE: Knowledge about log-parsing. Read when related tasks arise. -->
# Log-Parsing

### [2026-05-26 16:47] Tags: log-parsing, byte-level, python-mmap
## Fast Byte-level In-place Log Modification
For processing large ArduPilot DataFlash binary logs (.bin), traditional parser libraries (like pymavlink DFReader) can be very slow due to Python object instantiation overhead.

### Optimization Pattern:
1. **Memory Load**: Read the entire file into a mutable `bytearray`.
2. **Dynamic Format Parsing**: Scan FMT messages at the beginning of the file (sync bytes: `0xA3, 0x95`, message type: `128`). Map `msg_type_id` to its length, column list, and formats.
3. **Byte-level Navigation**: Move pointer `idx` directly by `msg_len` to avoid parsing skipped messages.
4. **In-place Rewrite**: Access payload using `struct.unpack_from` and write changes back instantly via `struct.pack_into`.
5. **Int Overflow Wrapping**: Custom `safe_pack_value` mask bits (e.g., `& 0xFFFF`) to mimic hardware behavior and prevent `struct.error` exceptions when values exceed int limits.

### [2026-05-26 16:49] Tags: log-parsing, parallel-processing, multiprocessing
## Parallel Binary Unpacking (ProcessPoolExecutor + mmap)
For read-only data analysis of large logs, multi-process parallel binary unpacking maximizes CPU core utilization.

### Pattern:
- **Chunking**: Get all message offsets using `mlog.offsets[tid]`. Split offsets list into chunks based on CPU cores.
- **Workers**: Each process maps the file using `mmap` (read-only), uses `struct.unpack_from` on the chunk of offsets, and returns raw data lists.
- **Aggregation**: Collect results in the main process and build Pandas DataFrames for plotting or computation.

## Comparison & Guidelines

| Method | State Dependency | Operation Type | Performance Bottleneck | Best For |
| :--- | :--- | :--- | :--- | :--- |
| **Byte-level In-place** | Stateful (requires sequential time states) | Read/Write (In-place) | Single-threaded CPU | Log injection, sensor outage simulation |
| **ProcessPoolExecutor** | Stateless (independent chunks) | Read-only | Multi-process IPC overhead | Trajectory comparison, statistics, plotting |
