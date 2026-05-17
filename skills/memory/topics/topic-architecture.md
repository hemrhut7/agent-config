<!-- SCOPE: Knowledge about architecture. Read when related tasks arise. -->
# Architecture

### [2026-05-17 21:41] Tags: architecture, refactor, ekf
Refactored core INS/GNSS library: Introduced NavState/StateIndex for dynamic dimensions (15, 26, 32), converted configs to dataclasses with YAML support, standardized package structure with __init__.py, and centralized parameters in EKF_params.py. Verified behavior consistency with baseline flight data index 0.

### [2026-05-17 21:47] Tags: architecture, restruct
Completed Step 1: Project Structure & Modularization. Renamed MyLib to nav_ekf, reorganized into core, filters, sensors, framework, utils. Moved tester to examples and ParamFinder to apps. Updated all imports across the project.

### [2026-05-17 21:50] Tags: architecture, config
Completed Step 2: Configuration Management. Refactored ekf_params into TuningConfig dataclass, implemented YAML/JSON loading in EKFConfig, and established dependency injection pattern in EKFRunner. Resolved circular imports by introducing constants.py.

### [2026-05-17 21:53] Tags: architecture, sensor, modules
Completed Step 3: Sensor Abstraction. Introduced BaseSensorModule and implemented specific modules for GNSS, Baro, Airspeed, Mag, ZUPT, NHC, Lidar, and Body Velocity. Refactored INS_GNSS.run to use a registry-based execution loop, greatly improving extensibility and code clarity.

### [2026-05-17 21:56] Tags: architecture, maintenance, test
Completed Step 4: Code Quality & Maintenance. Decomposed monolithic run methods in INS_GNSS and EKFRunner into focused private methods. Enhanced type hinting in coordinate_transformation.py and added initial unit tests verifying core mathematical models.

### [2026-05-17 21:57] Tags: architecture, performance, numba
Completed Step 5: Performance. Optimized core mechanization and EKF functions by enforcing contiguous memory layouts, which improves Numba execution efficiency. Verified that all critical computational paths use cached JIT compilation.

### [2026-05-17 21:57] Tags: architecture, logging, debugging
Completed Step 6: Logging & Debugging. Enhanced DataLogger with Context Manager support and optimized chunked writing. Standardized visualization interfaces in EKFAnalyzer to provide automated performance reporting.
