---
name: attitude-analysis
description: "Process, analyze, and visualize angular navigation data (roll, pitch, yaw) from multi-stream logs, handling wrapping to [-180, 180] and filtering outlier spikes."
---

# Attitude Analysis Skill

This skill provides specialized utilities for processing, analyzing, and visualizing navigation data from multi-stream logs (e.g., External INS vs ArduPilot EKF). It focuses on handling the circular nature of angular data and mitigating artifacts from timing/interpolation issues.

## Core Capabilities

1.  **Angle Normalization**: Automatically wraps angular errors to the `[-180, 180]` degree range to handle 360-degree boundary crossings correctly.
2.  **Robust Outlier Filtering**: Detects and removes "impossible" jumps in error values. These spikes are typically artifacts of:
    *   Sub-optimal interpolation between data streams with different sampling rates.
    *   Minor timing misalignments or jitter in log timestamps.
    *   Logic-based filtering using a configurable rate-of-change threshold (e.g., 100 deg/s).
3.  **Multi-Stream Alignment**: Utilities for interpolating diverse data sources onto a common timeline for accurate point-by-point comparison.

## Implementation Details

The logic is encapsulated in `scripts/nav_utils.py`.

### Angle Normalization
```python
def wrap_180(angle):
    return (angle + 180) % 360 - 180
```

### Outlier Removal
```python
def filter_angular_outliers(time, error, threshold_deg_per_sec=100.0):
    # Logic to identify and mask high-rate spikes
    ...
```

## Usage Guidelines

- **Always Normalize**: Any operation involving the subtraction of two angles (Roll, Pitch, Yaw) MUST be followed by a wrap to ±180.
- **Filter Before Statistics**: Calculate Mean and Std Dev only after filtering outliers to avoid skewed results.
- **Visualize the Delta**: Plotting the difference on a secondary axis is often more informative than overlapping raw signals for identifying subtle drifts or systematic offsets.
