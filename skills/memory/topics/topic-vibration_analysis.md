<!-- SCOPE: Knowledge about vibration analysis log parsing and FFT segment handling. Read when working on tools/vibration_analysis_runner.py or AP_ILB_Replay_Analyzer.py. -->
# Vibration Analysis

### [2026-06-01 11:45] Tags: vibration_analysis, parse_log, fft_segment
- `AP_ILB_Replay_Analyzer.parse_log` pitfall: ILB1 raw messages include `IMS`, but if the ILB1 mapping omits it, `vibration_analysis_runner.get_time_offset_from_dfs()` cannot align high-rate and standard logs by IMS and falls back to a hardcoded/default offset. Preserve `IMS` as `ims` in both high-performance and sequential ILB1 parsing.
- Binary parser pitfall: `mlog.offsets` can include a final/incomplete message near EOF. Before `struct.unpack`, compute expected body length with `struct.Struct(msg_struct).size` and skip offsets whose `body_start + body_len` exceeds file size; otherwise `unpack requires a buffer of N bytes` forces a slow sequential fallback.
- FFT analysis pitfall: vibration FFT frequency axes are wrong if sample rate is estimated as `len(full_log) / full_log_duration` when the log has mid-file data gaps. For frequency-domain analysis, split by large `time_us` gaps, use only each sensor's longest continuous segment, and estimate `fs` from the segment's median positive `dt`.
- Validation note from 2026-06-01: log80 produced 2 IMU/ILB segments and changed ILB peak from ~55.69 Hz to ~44.52 Hz after segment-local FFT; log79 IMU had 2 segments while ILB had 1, and segment-local FFT aligned IMU/ILB peaks near 5.88/5.78 Hz.
