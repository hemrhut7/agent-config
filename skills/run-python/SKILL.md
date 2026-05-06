---
name: run-python
description: "Executes Python commands with intelligent environment selection (Venv > Global > Install). Includes output monitoring to prevent terminal hanging."
---

# Python Executor (Intelligent Environment)

## Operational Logic

### 1. Environment Selection Priority
Follow this sequence to determine the Python executable:

1.  **Workspace Venv**: If `.venv` exists in the workspace root, use it by default.
    - Linux: `./.venv/bin/python`
    - Windows: `.\.venv\Scripts\python.exe`
2.  **Missing Module Fallback**: If a required module is missing in the workspace `.venv`:
    - Check global environment: `python3 -c "import <module>"` (Linux) or `python -c "import <module>"` (Windows).
    - **Found Globally**: Use global Python.
    - **NOT Found Globally**: Install in `.venv` using `./.venv/bin/pip install <module>`.
3.  **No Venv Decision**: If no `.venv` exists:
    - **Ask the User**: "No virtual environment found. Should I use the global Python or create a new virtual environment?"

### 2. Execution Strategy (Anti-Hang)
- **Unbuffered Mode**: Always use the `-u` flag (e.g., `python -u script.py`) to ensure real-time log flushing.
- **Output Limitation**: For scripts with high-frequency data, append `| tail -n 100` to the command.
- **Polling Mechanism**: For tasks exceeding 10 seconds, use asynchronous execution and poll the process status every 5 seconds.

## Instructions
- **Command Transformation**: Use the determined executable + `-u`.
- **Dependency Management**: Only install packages if they are not available globally (when a venv is used) or when creating a new venv.
- **Error Analysis**: If execution fails, retrieve only the last 50 lines of `stderr` for troubleshooting.

## Examples
### Ubuntu (Existing Venv)
`./.venv/bin/python -u src/main.py | tail -n 50`

### Windows (Global Fallback)
`python -u tests/ekf_validation.py`
