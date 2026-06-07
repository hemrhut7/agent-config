<!-- SCOPE: Today's task log and working memory. Read at conversation start to resume context. -->
# Brain — Working Memory

## Last Updated: 2026-06-07 14:43

### Active Tasks
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

### Pending Decisions
- (none)

