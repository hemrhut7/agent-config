# Daily Summary - 2026-05-15

## Context
Implementing Global Batch Optimization (Scheme C) as a baseline for EKF evaluation.

## Achievements
- Implemented `GlobalBatchOptimizer.py` for trajectory smoothing using non-linear least squares.
- Successfully modeled and estimated GNSS Delay as a global parameter.
- Developed `tester/GlobalBatchTester.py` for performance evaluation against existing EKF framework.
- Extended `CoordinateTransformation.py` with `ENU2llh` support.
- **Stabilized GlobalBatchOptimizer**: Fixed mathematical Jacobian errors and implemented dynamic pre-integration.
- **Resolved Output Anomalies**: Fixed unit scaling and coordinate conversion bugs in analysis output, achieving 0.06m horizontal error.

## Pending
- Integration of magnetic field calibration into the batch optimization loop.
- Comparison of Batch LSM results with EKF replay for long-duration datasets.
