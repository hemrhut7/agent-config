<!-- SCOPE: Knowledge about log-parsing and replay performance optimizations. -->
# Log-Processing

### [2026-05-26] Byte-level Log Modification (R/W)
For processing large DataFlash logs without the overhead of parser libraries (e.g., pymavlink).
- **Memory Mapping**: Load file into a mutable `bytearray`.
- **Dynamic FMT Mapping**: Scan `FMT` messages (`0xA3 0x95 0x80`) to map type IDs to length/format.
- **Fast Navigation**: Pointer jumping via `msg_len` to skip irrelevant messages.
- **In-place Updates**: Use `struct.unpack_from` and `struct.pack_into` for zero-allocation edits.
- **Hardware Emulation**: Mask overflows (e.g., `& 0xFFFF`) in `struct.pack` to mimic firmware behavior.

### [2026-05-26] Parallel Binary Unpacking (Read-only)
Maximizes CPU utilization for telemetry analysis.
- **Strategy**: Chunk offsets from `mlog.offsets[tid]` across processes.
- **Execution**: `ProcessPoolExecutor` + `mmap` (read-only) + `struct.unpack_from`.
- **Aggregation**: Combine chunk results into a single Pandas DataFrame.

### [2026-05-18] High-Performance Replay Decoding
Integrated method for mapping and decoding 1.9GB+ logs in ~1.2s.
- **Cython Offset Mapping**: Uses `mlog.offsets[tid]` for immediate message localization.
- **Parallel Decoding**: `mmap` + `ProcessPoolExecutor` + `struct.unpack` to bypass GIL.
- **Vectorized Scaling**: Applies pymavlink scales directly in Pandas.
- **Dynamic Scaling**: Worker count set to `max(1, cpu_count - 4)` (e.g., 18 workers on 22-core system).
- **Resilient Fallback**: Reverts to sequential `recv_match` on error.

### Comparison Matrix
| Method | Ops | Bottleneck | Best For |
| :--- | :--- | :--- | :--- |
| **Byte-level** | R/W | Single-thread | Log injection, sensor outages |
| **Parallel** | Read | IPC/Overhead | Trajectory analysis, plotting |
