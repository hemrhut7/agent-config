<!-- SCOPE: UI/UX design, PySide6, Plotly, and frontend usability. -->
# UI/UX & PySide6

### [2026-05-15] Tags: uavlogviewer, plotly, performance, async
- **Plotly Annotations**: Restored annotations (modes, events, params) in `uavlogviewer`. Implemented async rendering via `requestAnimationFrame` to prevent main-thread UI hangs. Added y-axis reset logic to fix stale title bugs.
- **Legend Stats Calculation**: Fixed legend statistics calculation (Min, Max, Mean, Std) in `Plotly.vue` and `PlotlyPopup.vue`. Avoided stack overflow (`RangeError: Maximum call stack size exceeded`) from `Math.min(...yInside)` on massive logs. Switched to `Plotly.restyle` to ensure correct legend updates. Handled undefined range fallback via `_fullLayout`. Recalculated stats dynamically during synchronized zooming.

### [2026-06-04] Tags: pyside6, ui-ux
- **MAVLink Tool**: Refactored using `QStackedWidget` to prevent layout jumps. Added telemetry dash grid cards and monospace console with log clearing.
- **FlightMetricsPopup**: Migrated text-to-speech broadcast logic into the popup. Removed redundant Broadcast tab from `MAVLinkWidget`.
- **Thread Safety**: Handled lifecycle cleanup in `closeEvent` and `reject` overrides to prevent crashes on exit.
