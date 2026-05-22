<!-- SCOPE: Knowledge about navigation-error. Read when related tasks arise. -->
# Navigation-Error

### [2026-05-22 13:18] Tags: navigation-error
Transient spikes in sub-segment relative tracking error are caused by time synchronization mismatch at boundary transitions (e.g., when GNSS is restored at the end of outage). To eliminate these transient spikes and yield clean, steady-state metrics: 1) Truncate sub-segment query end times by -0.1 seconds (e.g. 'seg_end_t - 0.1'). 2) Use effective duration 'eff_duration = seg_duration - 0.1' for drift rate and percent error. 3) Apply the same offset to plot masks to keep visuals aligned with the tabulated metrics.
