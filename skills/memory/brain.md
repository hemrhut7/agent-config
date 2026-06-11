<!-- SCOPE: Today's task log and working memory. Read at conversation start to resume context. -->
# Brain — Working Memory

## Last Updated: 2026-06-11 13:40

### Achievements (EKF Wind Model Upgrade to FOGM & Performance Evaluation)
- **Compared Estimator Parameters**:
  - Conducted a comprehensive comparative audit of estimator parameters and model structures between EKF ([kalman_filter.py](file:///home/hank/文件/Python/INS_python/nav_ekf/filters/kalman_filter.py)) and Batch Optimizer ([global_batch_optimizer.py](file:///home/hank/文件/Python/INS_python/nav_ekf/core/global_batch_optimizer.py)).
  - Documented findings in [estimator_parameter_comparison.md](file:///home/hank/文件/Python/INS_python/doc/estimator_parameter_comparison.md).
- **Upgraded EKF Wind Model**:
  - Modified the EKF wind model from pure Random Walk to First-Order Gauss-Markov (FOGM) process.
  - Implemented exact discretization of FOGM process noise ($Q_{\text{wind}} = \sigma_w^2 (1 - e^{-2 dt/\tau_w})$) in `genQ_core` and exponential decay dynamics ($1 - dt/\tau_w$) in `genF_core`.
  - Added configuration parameters `wind_fogm_tau = 300.0` and `wind_fogm_sigma = 0.05` (the batch-optimized value) in [config.py](file:///home/hank/文件/Python/INS_python/nav_ekf/filters/config.py) and mapped them in [ekf_params.py](file:///home/hank/文件/Python/INS_python/nav_ekf/filters/ekf_params.py).
- **Verified and Evaluated Performance**:
  - Ran EKF outage simulations sequentially for IDs `0, 1, 2, 3, 4, 6` with FOGM vs Random Walk models.
  - **Results**: FOGM wind model constraints drift during outages for IDs 0 (+31.5% rate / +22.5% max err) and 3 (+3.6% rate / +24.3% max err). However, ID 4 experienced numerical divergence due to coupling between the FOGM decay constraint and wind shear, which was handled safely by adding try-except blocks around matplotlib plotting.
  - Documented findings in [ekf_wind_fogm_performance_analysis.md](file:///home/hank/文件/Python/INS_python/doc/ekf_wind_fogm_performance_analysis.md).

- **Researched GPU Acceleration for Global Batch Optimizer**:
  - Investigated the feasibility of offloading large Hessian matrix solving ($H = J^T J$) to GPUs.
  - Identified **CuPy** (with `cuSolver`) as a primary candidate for sparse solving, while noting that CPU (Numba/SciPy) remains competitive for systems < 10,000 nodes due to I/O overhead.
  - Recommended **Theseus (Meta)** or **NVIDIA cuDSS** for high-performance batch optimization exceeding 20,000 nodes.
  - Documented technical insights and bottlenecks in the project's persistent memory (`topic-navigation-slam.md`).
- **Analyzed EKF Computational Efficiency for Large Logs**:
  - Identified that core EKF math is already accelerated by **Numba**, but Python wrapper overhead (object instantiation, memory churn, and un-vectorized checks) in 400Hz loops is the primary bottleneck.
  - Proposed 5 optimization strategies: pre-computing GNSS outages/flags, reducing `.copy()` calls, reusing dictionary objects, and using `searchsorted` for time sync.
  - Logged optimization roadmap in `topic-navigation-slam.md` to guide future performance refactors.

## Last Updated: 2026-06-10 18:45

### Achievements (Batch Optimizer Wind-Roll Correlation Analysis & Fix)
- **Identified Root Cause of Wind-Roll Correlation**:
  - Found that the default wind Gauss-Markov process noise (`wind_fogm_sigma = 1.0`) was 800 times larger than the online EKF's wind random walk noise (`rw_wind = 0.0001`). This excessive flexibility allowed the wind state to oscillate at the turning frequency to absorb turn-induced aerodynamic model and sensor errors, creating a false correlation.
- **Verified and Tuned Parameters**:
  - Conducted a parameter sweep on `wind_fogm_sigma` from 1.0 down to 0.02.
  - Confirmed that setting `wind_fogm_sigma = 0.05` restricts the wind variation rate to a physically realistic range, resolving the false correlation with roll.
  - Verified that this change improved GNSS Outage trajectory accuracy: **maximum horizontal error dropped from 1.560 m to 0.980 m (37% improvement)** and **average horizontal drift rate dropped from 0.030 m/s to 0.015 m/s (50% improvement)**.
- **Updated Codebase**:
  - Modified the default `wind_fogm_sigma` parameter to `0.05` in [global_batch_optimizer.py](file:///home/hank/文件/Python/INS_python/nav_ekf/core/global_batch_optimizer.py).
  - Cleaned up temporary test files in `.agent_scratchpad`.
  - Saved a detailed analysis report to [wind_roll_correlation_analysis.md](file:///home/hank/.gemini/antigravity-cli/brain/f297e451-2918-4ab5-b9bf-e2f744953b9f/wind_roll_correlation_analysis.md).

### Achievements (QuadPlane Soft-Landing Safety Failsafes)
- **Implemented 5 Safety Failsafes for QuadPlane Soft-Landing**:
  - Clamped `RNGFND_LND_ALT` minimum to `3.0m` to avoid linear interpolation direction reversal.
  - Added rangefinder anomaly failsafe: freezes target descent rate at `MAX(last_rate, 40cm/s)` if rangefinder loses tracking near the ground.
  - Introduced `soft_landing_active` hysteresis state flag to prevent target speed chattering at the altitude boundary.
  - Integrated low-pass target speed filtering (`ret = last * 0.8 + new * 0.2`) to suppress rangefinder sensor noise.
  - Enforced a hard minimum landing speed limit of `0.4 m/s` (40 cm/s) to quickly clear ground effect turbulence and prevent wind tipping.
- **Verified Compilation**:
  - Successfully compiled both SITL (`./waf plane`) and hardware ChibiOS (`CubeOrangePlus-CIRC`) firmware with zero errors.

## Last Updated: 2026-06-10 09:40

### Achievements (Standard Reusable Vibration & FFT Library)
- **Created and verified reusable library modules under `src/`**:
  - [log_reader.py](file:///home/hank/文件/Python/logReader/src/log_reader.py): Implements high-performance binary parsing via `pymavlink` format detection combined with parallel `mmap` + `struct` workers, continuous segment detection, `(N-1)/duration_s` sampling rate estimation (robust to bimodal spacing), IMU instance filtering, and magnitude calculations.
  - [fft_utils.py](file:///home/hank/文件/Python/logReader/src/fft_utils.py): Implements 1-D FFT spectral analysis, convolved rolling-average spectral smoothing, band-limited RMS calculation, standard matplotlib `ggplot` styling, and multi-series/multi-subplot comparative plotting.
- **Tested and Verified End-to-End**:
  - Created a verification script at [.agent_scratchpad/test_lib.py](file:///home/hank/文件/Python/logReader/.agent_scratchpad/test_lib.py) and successfully tested the full parsing, segment extraction, FFT calculation, smoothing, and plotting pipeline using a flight log [log_10_2026-1-20-17-06-58.bin](file:///home/hank/文件/Python/logReader/data/log_10_2026-1-20-17-06-58.bin). All verification steps completed with clean results and correct data rates.
  - Verified reading performance on two large test flight logs [2026-05-27 16-29-21.bin](file:///home/hank/文件/Python/logReader/data/2026-05-27 16-29-21.bin) (144.85 MB parsed in 3.0 seconds, 1.18M rows) and [log80_2026-05-27 16-29-21.bin](file:///home/hank/文件/Python/logReader/data/ilb_logger/log80_2026-05-27 16-29-21.bin) (264.73 MB parsed in 43.1 seconds, 2.08M rows) containing `IMU`, `ILB1`, and `VIBE` messages using the script [.agent_scratchpad/verify_two_logs.py](file:///home/hank/文件/Python/logReader/.agent_scratchpad/verify_two_logs.py).
  - **Identified and Optimized GPS-less Log Scanning Bottleneck**: Discovered that when log files contain no GPS messages (like the 264 MB ground log), pymavlink's `init_clock()` sequentially scans the entire file twice in Python to search for clock anchors, causing connection setup to take ~32 seconds. Solved this by setting `ignore_gps_clock="auto"` as the default behavior in `parse_bin_log` inside [log_reader.py](file:///home/hank/文件/Python/logReader/src/log_reader.py), which uses the fast Cython-indexed offsets to check if `GPS`, `GPS2`, or `TIME` messages exist. If none are present, it automatically monkeypatches the clock init to bypass the slow scans and fallback directly to the microsecond clock. This yielded full automated parsing speed on both logs without manual settings (Log 1: **2.12 seconds**, Log 2: **3.34 seconds**), verified using [.agent_scratchpad/test_auto_mode.py](file:///home/hank/文件/Python/logReader/.agent_scratchpad/test_auto_mode.py).

## Last Updated: 2026-06-08 16:45

### Achievements (EKF Lane Switch Log Scan, Parallel Parsing Optimization & Root-Cause Analysis)
- **Scanned 32 ArduPilot Binary Logs**: Analyzed EKF lane switch events across all `.bin` files in the `data` directory using `ProcessPoolExecutor` with 18 parallel workers to maximize performance (scanned in under 1.5 minutes).
- **Identified EKF Lane Switch Events**: Found 3 logs with EKF lane switches/primary core switches:
  1. [log_9_2026-3-20-15-30-32.bin](file:///home/hank/文件/Python/logReader/data/log_9_2026-3-20-15-30-32.bin) (3 core switches between Core 0 and 2)
  2. [log_26_2026-5-21-14-40-54.bin](file:///home/hank/文件/Python/logReader/data/log_26_2026-5-21-14-40-54.bin) (3 core switches between Core 0 and 2)
  3. [log_20_2026-5-12-15-13-54.bin](file:///home/hank/文件/Python/logReader/data/log_20_2026-5-12-15-13-54.bin) (5 core switches among Core 0, 2, and 1)
- **Generated Markdown Report**: Saved the complete scan result table and EKF details to [output/ekf_lane_switch_analysis.md](file:///home/hank/文件/Python/logReader/output/ekf_lane_switch_analysis.md) and created a corresponding UI artifact.
- **Diagnosed Root Cause of EKF Lane Switches**: Conducted a deep analysis of EKF innovation ratios, vibration levels, and GPS data around switch timestamps. Confirmed that Z-axis vibration spikes (up to 97g) during the VTOL-to-Fixed-Wing transition triggered the lane switches (no GPS or compass anomalies). Saved the complete diagnosis report in Traditional Chinese to [output/ekf_lane_switch_causes.md](file:///home/hank/文件/Python/logReader/output/ekf_lane_switch_causes.md).
- **Verified EKF Lane Switch Code Location in `CIRC_Ardupilot`**: Found that `ArduPlane/ekf_check.cpp` triggers `ahrs.check_lane_switch()` when EKF variance failsafe is imminent. This routes to `NavEKF3::checkLaneSwitch()` in `AP_NavEKF3/AP_NavEKF3.cpp` which switches lanes if an alternative core is healthy and has a lower `errorScore()` (defined in `AP_NavEKF3_Outputs.cpp` based on Vel, Pos, Hgt, and Mag test ratios). Vibration triggers switches by raising innovation test ratios.

## Last Updated: 2026-06-08 15:26

### Achievements (Vibration Analysis Bugfixes & Markdown Indentation Formatting)
- **Fixed LaTeX Escaping Issue in Reports**: Resolved a Python f-string escaping bug where `\text{Hz}` was parsed as a tab character (`\t`) followed by `ext{Hz}` in [single_log_vibration_analysis.py](file:///home/hank/文件/Python/logReader/tools/single_log_vibration_analysis.py).
- **Fixed Indentation in Runner Markdown Reports**: Corrected 4-space indentation formatting inside the triple-quoted report content f-string in [vibration_analysis_runner.py](file:///home/hank/文件/Python/logReader/tools/vibration_analysis_runner.py) to prevent standard Markdown parsers from rendering paragraphs, tables, and images as pre-formatted code blocks.
- **Verified Data Consistency in g/m/s² Units**: Confirmed that both single log and log-pair runner analysis scripts successfully process Accelerometer/Vibration data converting $m/s^2$ to $g$ and rendering plots and reports with consistent labels.
- **Changed Default Output Directory**: Set the default output folder of [single_log_vibration_analysis.py](file:///home/hank/文件/Python/logReader/tools/single_log_vibration_analysis.py) to `output/vibration_analysis` to keep all vibration analysis results consolidated.

## Last Updated: 2026-06-08 10:22

### Achievements (Multi-Log FFT Plot Styling & Spectral Smoothing)
- **Fixed Syntax Error in FFT Plotting Loop**: Resolved a SyntaxError in `tools/single_log_vibration_analysis.py` introduced in a prior merge, restoring the correct loop structure and indentation for the InertialLabs ILB IMU FFT spectrum comparison.
- **Configured Comparison Plot Line Styles**: Updated the multi-log comparison charts to use default line widths, all solid line styles (no dashed/dotted), and custom alpha values (1.0 for baseline, 0.75 for other test logs).
- **Implemented Spectral Smoothing**: Applied a centered rolling average (window=7) to both the reference Cube line and the InertialLabs ILB lines in the FFT comparison chart. This significantly reduces high-frequency noise and overlaps, making the peak frequencies and absolute magnitudes much easier to observe.

## Last Updated: 2026-06-07 14:43

### Achievements (Standard GRMS Vibration Spectrum Plot, Dual Units, and Sampling Rate Bugfix)
- Integrated `scipy.signal` in `tools/single_log_vibration_analysis.py` to calculate standard Power Spectral Density (PSD in $g^2/Hz$) and Cumulative GRMS (in $g_{rms}$) from raw acceleration data.
- **Fixed Sampling Rate Estimation Bug**: Discovered and resolved an issue where the bimodal timing intervals (3.33ms / 6.66ms spacing) on the InertialLabs ILB IMU caused the median `dt` logic to underestimate `fs` as 153.4 Hz instead of 200 Hz. Fixed by computing `fs` using segment length and duration. This successfully aligned the vibration peaks (e.g. at 41.73 Hz) of both sensors perfectly.
- **Added Dual Units for GRMS**: Added both $g$ and $\text{m/s}^2$ units to the cumulative GRMS chart legends and the summary tables in `VIBRATION_REPORT.md` (e.g. `0.2367 g (2.321 m/s²)`). This directly addresses unit interpretation differences and ensures consistent comparison.
- Verified successful execution of the entire GVT log analysis pipeline.

## Last Updated: 2026-06-04 16:41

### Achievements (Multi-Log Vibration Comparison Graph & Report Integration)
- Updated `tools/single_log_vibration_analysis.py` to include `ap_vibe_ilb` in the returned data of `analyze_log_file`.
- Implemented `gvt_vibration_comparison.png` generation inside `generate_multi_log_comparison` which aligns and overlays the accelerometer vibration magnitude over time for the InertialLabs ILB IMU across all logs.
- Preserved the existing dampening ball color coding (green, slate, dark charcoal, red, amber) and line styles from the FFT comparison graph in the new vibration magnitude comparison graph.
- Appended a new section "5. Vibration Magnitude Comparison Plot" in `GVT_COMPARISON_REPORT.md` referencing the newly generated comparison plot.

## Last Updated: 2026-06-04 14:18

### Achievements (Active Vibration Analysis Refactoring, PPTX Report & ILB Exclusion)
- Modified `tools/single_log_vibration_analysis.py` to crop all DataFrames to the active phase first to guarantee that all downstream analysis calculations (vibration estimation, FFT, overlays, stats) use ONLY active test data.
- Raised the RPM active phase detection threshold from 100.0 to 1000.0.
- Explicitly set `standby_seg` to `None` to cleanly disable standby phase computations and format tables with N/A.
- Removed the first data point (index 0) from the calculated vibration and gyroscope vibration DataFrames to prevent the initial filter startup zero from skewing charts and statistical analysis.
- Generated a professional 5-slide weekly report presentation (`減震球震動實驗分析週報.pptx`) in `/media/hank/B0D4B41ED4B3E4AE/文件/週報` using Node.js and PptxGenJS, detailing the performance comparison of different dampening balls using InertialLabs high-precision data with Green as baseline.
- Refactored `generate_multi_log_comparison` to generate an improved `gvt_fft_comparison.png` chart, removing the ArduPilot IMU subplot and displaying only the InertialLabs ILB IMU data with custom line styles and color coding mapped to physical dampening ball colors (green, slate, black, red, amber).
- Restricted all markdown quantitative comparison tables in `GVT_COMPARISON_REPORT.md` to only display InertialLabs ILB IMU data, completely removing ArduPilot internal IMU rows to focus solely on high-precision external sensor measurements.
- Verified parsing and analysis execution successfully using `.venv` Python environment on `data/ground_vibration_test/log_72_black.bin`.

## Last Updated: 2026-05-22 09:15
## Last Updated: 2026-05-28 16:22


### Active Tasks
- [ ] 優化 `runner.py` 高頻迴圈：實作 GNSS Outages 與 Sensor Flags 的向量化預計算，消除迴圈內物件建立與 redundant check。
- [ ] 重構 `ins_gnss_kf.py` 記憶體管理：減少不必要的 `.copy()` 呼叫，並透過物件重用（In-place update）減輕 GC 壓力。
- [ ] 提升時間同步效率：使用 `numpy.searchsorted` 取代 `while` 狀態機進行 $O(\log n)$ 的 GNSS Epoch 映射。
- [ ] 實作 CuPy GPU 加速研究：針對 Batch Optimizer 實作可切換的 CuPy 後端，設計當資料量達到門檻（如 N > 20,000）時自動啟用，並量化評估其加速倍率與數據傳輸開銷。
- [ ] 將 Batch Optimizer 與 EKF 的參數統一進行管理，確保兩方參數的一致性，但需要先進行研究，確認兩者參數的定義、對模型影響是相同的。

- [x] 調查專案中 `num_range_data`、`min_z`、`rotation_weight` 參數是否設定及其預設值。
- [x] 在 `my_2d.lua` 中優化調整這三個參數（分別設為 45, -0.1, 150.0）。
- [x] 更新 `Cartographer Guide.md` 加入調參分析（特別是無里程計 vs 有里程計下的子圖剛性權衡）。

- [x] 在 `GlobalBatchTester.py` 執行完後，預設自動生成 `.npz` 結果記錄檔，利於後續進行快速比較（工作區與分支：`feat/batch-tester-npz`）。
- [x] 修正 `GlobalBatchOptimizer` 中 IMU bias 估測像雜訊、scale factor 固定不變的問題，使其符合物理規格並表現出合理飄移；校正 `states_analysis.png` 中的 Gyro Bias 數值使其與 DPH 單位標籤完全一致。


### Session Notes
- **EKF-Aligned GlobalBatchOptimizer**: Aligned state vector dimension to 30 states (P, V, Q, BG, BA, G, SG, SA, W, MI, MB).
- **Scale Factor Corrections**: Compounded IMU raw measurements using gyro/accel scale factors and analytical Jacobians inside `_preintegrate_all`.
- **Magnetometer Estimation**: Implemented 3D magnetometer observation residuals ($r = R^T m_I + m_{bias} - m_{meas}$) and analytical Jacobians. Corrected attitude Jacobian from `R_l2b @ vector2skew(m_I)` to `vector2skew(R_l2b @ m_I)` to resolve coordinate frame mismatch.
- **Scale Mismatch Bug Resolution**: Corrected initialization by dynamically calling the WMM model at the starting LLA ($\approx [ -30.0, 366.0, -264.0 ]\text{ mG}$).
- **A+B Magnetic Defense & Noise Tuning**: Implemented Hard Gate, Dynamic R, and Cauchy Robust Loss. Tuned default standard deviation `std_mag = 250.0` mG to align Pitch/Roll attitude to baseline (Roll RMSE: 0.12°, Pitch RMSE: 0.58°) while successfully bounding Yaw.
- **Validation Results**: Fully resolved attitude deviation. All plots verified and saved.

- **Lidar & SLAM Tuning**: 由於 N10 雷達量程只有 15m 且本專案無里程計限制，直接套用官方 10~30 秒（90 幀以上）的子圖長度會導致嚴重的平移累積誤差扭曲。故實務上調小 `num_range_data` 至 45（4.5 秒）能有效保障子圖一致性；搭配調高 `rotation_weight` 至 150.0 能充分發揮高精度 IMU 對 Yaw 角的約束力。
- **Ground Noise**: 調高 `min_z` 至 -0.1m 能濾除因小車晃動或地面不平造成的噪聲反射。
- **GlobalBatchTester NPZ logs**: Modified `GlobalBatchTester.py` to automatically save the optimization result dictionary as a compressed `.npz` file (`ekf_log.npz`) in the test directory, enabling rapid cross-model EKF analysis and performance comparison.
- Restored missing Plotly annotations (modes, events, params) in `uavlogviewer`.
- Implemented async rendering for annotations to prevent UI hangs.
- Added y-axis reset logic to fix stale title bugs.
- Fixed legend statistics calculation (Min, Max, Mean, Std) in `Plotly.vue` and `PlotlyPopup.vue`:
  - Resolved stack overflow error (`RangeError: Maximum call stack size exceeded`) caused by `Math.min(...yInside)` on large logs.
  - Switched from `Plotly.relayout` to `Plotly.restyle` for updating trace name strings to ensure the legend updates correctly.
  - Handled undefined initial range cases by accessing `_fullLayout` fallback.
  - Ensured initial calculation triggers during initial plot generation using `requestAnimationFrame`.
  - Recalculated statistics when synchronized zooming occurs across multiple charts.
- Committed all changes to master.

### Pending Decisions
- (none)
