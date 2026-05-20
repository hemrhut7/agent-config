<!-- SCOPE: Knowledge about log-replay. Read when related tasks arise. -->
# Log-Replay

### [2026-05-18 18:13] Tags: log-replay
High-performance direct binary log parsing method was successfully integrated:
1. Cython Offset Mapping: Uses mlog.offsets[tid] to immediately locate target message bytes, taking ~1.2s to map 1.9GB log.
2. Parallel struct.unpack: Memory-maps log file (mmap) and concurrently decodes binary blocks via ProcessPoolExecutor, avoiding GIL.
3. Vectorized Multiplier: Decodes raw values and vectorially applies pymavlink scales in Pandas.
4. Dynamic Workers: Set via `max(1, int(max(cpu_count - 4, cpu_count / 2)))` for optimal core usage (18 workers on 22-core system).
5. Robust Fallback: Automatically falls back to standard sequential `recv_match` on any exception.
