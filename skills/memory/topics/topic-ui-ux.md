<!-- SCOPE: UI/UX design, PySide6, and frontend usability. -->
# UI/UX & PySide6

### [2026-06-04 14:57] Tags: pyside6, ui-ux
- **MAVLink Tool**: Refactored using `QStackedWidget` to prevent layout jumps. Added telemetry dash grid cards and monospace console with log clearing.
- **FlightMetricsPopup**: Migrated text-to-speech broadcast logic into the popup. Removed redundant Broadcast tab from `MAVLinkWidget`.
- **Thread Safety**: Handled lifecycle cleanup in `closeEvent` and `reject` overrides to prevent crashes on exit.
