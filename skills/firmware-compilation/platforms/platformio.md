# PlatformIO Compilation Guide (pio)

Guidelines for building PlatformIO micro-controller firmware.

## 1. Verification Step
- Before compilation, confirm that the `platformio.ini` file exists in the workspace root directory.

## 2. Common Compilation Commands
- **Standard Compilation**:
  ```bash
  pio run
  ```
- **Clean and Recompile**:
  ```bash
  pio run -t clean
  pio run
  ```
- **Target Specific Environment**:
  ```bash
  # Example: Compile for esp32dev
  pio run -e esp32dev
  ```

## 3. General Rules
- Always use forward slashes `/` for path definitions.
- Inspect binary outputs inside the `.pio/build/` directory upon success.
- If compilation fails, check the troubleshooting index: [troubleshooting/platformio.md](../troubleshooting/platformio.md).
