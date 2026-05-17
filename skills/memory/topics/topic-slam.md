<!-- SCOPE: Knowledge about slam. Read when related tasks arise. -->
# Slam

### [2026-05-17 14:30] Tags: slam, cartographer, EKF
We successfully integrated Google Cartographer SLAM with EKF fusion on 2D LiDAR. Key discovery: EKF initial position 'pos0' must be aligned to the LiDAR origin LLA (e.g., [25.0, 121.0, 10.0]) instead of [0, 0, 0], otherwise coordinate conversion results in massive (~13,717 km) residual error causing EKF updates to blow up. With aligned origin and LiDAR-only updates, EKF 2D closure error is successfully restricted to 0.85m.
