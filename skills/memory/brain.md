# Daily Summary - 2026-05-17

## Context
Implementing and validating Google Cartographer 2D LiDAR SLAM with EKF fusion.

## Achievements
- **Dockerized SLAM Setup**: Compiled Google Cartographer ROS Noetic inside a lightweight Docker image and automated master/offline-node lifecycle execution in entrypoint.sh.
- **Automated Data Pipeline**: Implemented pure Python `npz_to_rosbag.py`, `run_slam.py`, and `slam_result_injector.py` to seamlessly convert point clouds, execute offline SLAM, and inject trajectories back to telemetry files.
- **EKF LiDAR Fusion**: Addressed LLA origin misalignment between EKF (`pos0` = [0, 0, 0] LLA) and LiDAR SLAM (`origin_lla` = [25.0, 121.0, 10.0] LLA). Aligned EKF origin to Taipei LLA, successfully reducing EKF 2D closure error with only-LiDAR updates to 0.85m.
- **LiDAR Map Stitching**: Implemented global coordinate transformation mapping in `plot_slam_only.py`, successful stitching of 231,011 points, producing high-resolution environmental vector maps.
- **Visualization & UI**: Updated `KF_Plot.py` with LiDAR heading update indicators and recorded all analysis plots to walkthrough resources.

## Pending
- Run multi-scenario evaluations across other UDP-recorded datasets.
- Fine-tune Ceres scan-matching covariances in Cartographer configuration (`my_2d.lua`).
