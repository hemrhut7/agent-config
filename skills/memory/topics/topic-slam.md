<!-- SCOPE: Knowledge about slam. Read when related tasks arise. -->
# Slam

### [2026-05-17 14:30] Tags: slam, cartographer, EKF
We successfully integrated Google Cartographer SLAM with EKF fusion on 2D LiDAR. Key discovery: EKF initial position 'pos0' must be aligned to the LiDAR origin LLA (e.g., [25.0, 121.0, 10.0]) instead of [0, 0, 0], otherwise coordinate conversion results in massive (~13,717 km) residual error causing EKF updates to blow up. With aligned origin and LiDAR-only updates, EKF 2D closure error is successfully restricted to 0.85m.

### [2026-05-17 15:38] Tags: slam, ekf
We isolated EKF-LiDAR SLAM fusion in EKFTester_ABC.py by disabling NHC and encoder odom updates. We discovered that when wheel encoder updates were always running (due to a bug ignoring enable_agv=False), they introduced systematic noise/slippage. Correctly disabling encoder speed updates and NHC drastically reduced the EKF 2D closure error from 0.85m to 0.32m! We also fixed a vertical velocity coordinate flip bug in KF_Plot.py L970.

### [2026-05-17 16:20] Tags: slam, cartographer, yaw, abc
For `data/ABC/ABC_Controller_UDP_20260516_192933`, Cartographer position fusion is usable, but direct Cartographer yaw fusion is not trustworthy yet. The project convention is local `ENU`, body `RFU` (`+X right, +Y forward, +Z up`), Euler order `[pitch, roll, yaw]`. Re-running `tester/EKFTester_ABC.py` with LiDAR yaw disabled restored stable behavior and produced about `0.3287 m` 2D closure. Treat Cartographer yaw as opt-in until its frame/sign convention is explicitly verified against EKF yaw.

### [2026-05-17 16:45] Tags: slam, cartographer, metrics, abc
Closure error was a misleading metric for ABC path evaluation. After adding time-aligned `EKF vs Cartographer` path metrics in `tester/ekf_framework/analyzer.py`, the same `20260516_192933` dataset showed that `enable_lidar_yaw=True` is actually better than `False`: RMSE_2D improved from about `0.474 m` to `0.322 m`, even though closure alone suggested the opposite. Use aligned path RMSE/MAE/MAX as the primary metric for ABC SLAM fusion, not closure.

### [2026-05-17 17:05] Tags: slam, abc, parameter-sweep, yaw, timing, lever-arm
For `data/ABC/ABC_Controller_UDP_20260516_192933`, a three-stage sweep using aligned `EKF vs Cartographer` path error found: baseline (`yaw offset=0 deg`, `time offset=0 s`, `lever arm=(0,0,0)`) gives RMSE_2D about `0.3223 m`. Best yaw offset alone was about `+19 deg` (RMSE_2D `0.3112 m`). Best timing after that was about `+0.10 s` LiDAR delay compensation (RMSE_2D `0.3052 m`). Best planar lever arm after that was about `(-0.13, -0.07, 0.0) m`, improving RMSE_2D to about `0.2755 m` and RMSE_3D to about `0.5039 m`. This is a meaningful improvement, but still far from the target `0.1 m`, so remaining error is likely not explained by only yaw/time/planar lever-arm mismatch.

### [2026-05-17 17:20] Tags: slam, abc, yaw-source, tf
Further analysis for `20260516_192933` showed: Cartographer quaternion yaw is actually close to controller yaw (mean difference about `-0.4 deg`, mean absolute difference about `4.7 deg`), so the SLAM yaw source itself is not obviously broken. Using path-tangent heading instead of quaternion yaw made the EKF path fit much worse, so the quaternion orientation still carries useful pose information. `docker/robot.urdf` currently declares both `imu_link` and `laser` at zero rotation/translation from `base_link`, but the best EKF-vs-Cartographer fit still requires about `+20 deg` yaw offset and about `(-0.13, -0.07) m` planar lever arm. This strongly suggests the effective sensor/base frame relationship in the recorded data is not consistent with the current URDF/TF assumptions.

### [2026-05-17 17:24] Tags: slam, abc, imu, yaw
ABC IMU `wz` matches controller yaw-rate extremely well (correlation about `0.997`, scale about `1.0`), so the raw Z-axis gyro sign/scale is likely correct. Remaining yaw inconsistency is therefore more likely due to frame-definition mismatch or weak yaw-state alignment inside the EKF fusion chain, not a simple raw-gyro axis sign error.
