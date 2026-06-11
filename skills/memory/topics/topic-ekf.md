<!-- SCOPE: Knowledge about EKF. Read when related tasks arise. -->
# Ekf

### [2026-06-11 17:14] Tags: EKF, Optimization, GlobalBatchOptimizer, Python, Numba, searchsorted
GlobalBatchOptimizer Performance Optimization Results (2026-06-11):
1. `_preintegrate_all` (was 66.1% of time): Replaced full-array boolean mask `(imu_t > t_start) & (imu_t <= t_end)` with O(1) vectorized `np.searchsorted`. Time per iteration dropped by ~84% (from ~1.01s down to ~0.16s for 1877 nodes).
2. `_build_jacobian` (was 28.1% of time): Replaced O(N) GNSS search `np.argmin(np.abs(...))` with `np.searchsorted`.
Overall Impact: Total Batch EKF iteration time reduced by ~60% (e.g. from ~3.1-4.9s to ~1.3-1.9s for 4000 nodes).
Future optimization target: `_build_jacobian` is now the main bottleneck due to Python list appends inside `add_factor`. Next steps should consider pre-allocating Numpy arrays for Jacobian construction or migrating `add_factor` to Numba.
