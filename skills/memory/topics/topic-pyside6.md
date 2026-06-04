<!-- SCOPE: Knowledge about pyside6. Read when related tasks arise. -->
# Pyside6

### [2026-06-04 14:57] Tags: pyside6, ui-ux
MAVLink tool UI refactored using QStackedWidget to prevent layout jumps and telemetry dash grid cards for improved user usability. Monospace console output with clear log button added.

### [2026-06-04 16:46] Tags: pyside6, ui-ux
Migrated text-to-speech broadcast controls and logic into FlightMetricsPopup inside MavLink.py. Cleaned up and removed the redundant Broadcast tab from MAVLinkWidget. Handled thread lifecycle cleanup in closeEvent and reject overrides.
