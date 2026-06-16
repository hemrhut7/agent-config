<!-- SCOPE: UI/UX design, PySide6, Plotly, and frontend usability. -->
# UI/UX & PySide6

### [2026-05-15 14:27] Tags: uavlogviewer, plotly, performance, async
- **Plotly Annotations in uavlogviewer**: Restored Plotly annotations. Implemented async rendering via `requestAnimationFrame` to prevent main-thread blocking. Added y-axis reset logic to ensure clean plots when switching chart configurations.

### [2026-06-04 14:57] Tags: pyside6, ui-ux
- **MAVLink Tool**: Refactored using `QStackedWidget` to prevent layout jumps. Added telemetry dash grid cards and monospace console with log clearing.
- **FlightMetricsPopup**: Migrated text-to-speech broadcast logic into the popup. Removed redundant Broadcast tab from `MAVLinkWidget`.
- **Thread Safety**: Handled lifecycle cleanup in `closeEvent` and `reject` overrides to prevent crashes on exit.
