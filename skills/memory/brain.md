<!-- SCOPE: Today's task log and working memory. Read at conversation start to resume context. -->
# Brain — Working Memory

## Last Updated: 2026-06-06 21:03

### Active Tasks
- [x] 調查專案中 `num_range_data`、`min_z`、`rotation_weight` 參數是否設定及其預設值。
- [x] 在 `my_2d.lua` 中優化調整這三個參數（分別設為 45, -0.1, 150.0）。
- [x] 更新 `Cartographer Guide.md` 加入調參分析（特別是無里程計 vs 有里程計下的子圖剛性權衡）。

### Session Notes
- **Lidar & SLAM Tuning**: 由於 N10 雷達量程只有 15m 且本專案無里程計限制，直接套用官方 10~30 秒（90 幀以上）的子圖長度會導致嚴重的平移累積誤差扭曲。故實務上調小 `num_range_data` 至 45（4.5 秒）能有效保障子圖一致性；搭配調高 `rotation_weight` 至 150.0 能充分發揮高精度 IMU 對 Yaw 角的約束力。
- **Ground Noise**: 調高 `min_z` 至 -0.1m 能濾除因小車晃動或地面不平造成的噪聲反射。

### Pending Decisions
- (none)
