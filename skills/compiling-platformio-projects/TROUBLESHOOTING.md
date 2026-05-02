# PlatformIO Troubleshooting Reference

When `pio run` fails, please analyze according to the following error messages:

## Common Issues List

### 1. Platform not found
**Cause**: The corresponding development framework (e.g., `espressif32`) is not installed.
**Countermeasure**: Run `pio pkg install` or check the `platform` field in `platformio.ini`.

### 2. Missing header files
**Cause**: Necessary libraries are not included or path is incorrect.
**Countermeasure**:
- Check if `lib_deps` contains the library.
- Confirm if the `#include` name is correct.

### 3. Invalid platformio.ini
**Cause**: Syntax error or unsupported board name.
**Countermeasure**: Check against the official boards list to ensure the `board` ID is correct.

## Verification Steps
1. Read the last 10 lines of the error message.
2. Modify the code or configuration file according to the error type.
3. Re-run `pio run`.