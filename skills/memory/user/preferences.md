- **Estimation Philosophy**: Prefers Global Batch Least Squares (Scheme C/Factor Graph) with IMU pre-integration for baseline data generation.
- **Initialization Rule**: Avoid using EKF results for initializing baseline smoothing to prevent feedback loops. Use sensor-based initialization (accLeveling + GPS diff).
- **Parameter Observation**: Explicitly track GNSS delay, wind states, and airspeed parameters in global optimization.
- **Agent Workflow**: Values "Deep Memory" cycles (`@[/memory]`) to maintain context across sessions and ensure technical discipline in complex refactoring tasks.
- **Windows Environment Redirection**: Avoid PowerShell stdout redirection (`>`) for JSON/text files to prevent UTF-16LE conversion. Always use Python-based UTF-8 writing or specify explicit UTF-8 encoding options.
- **Windows CLI Command Execution**: Avoid executing complex multi-line command strings on Windows. Proactively write multi-step operations to a temporary Python script in `.agent_scratchpad/`, execute it, and clean up afterwards.
- **Codebase Research Philosophy**: Prioritize using `graphify` (`/graphify query`, `/graphify path`, `/graphify explain`) for codebase exploration and architectural searches. Always ensure the graph is in sync with the latest code updates by performing a fast incremental update (`/graphify --update`) if code changes are detected.
- **Configuration File Integrity**: Build configuration files (e.g., `.cmake`, `Makefile`, `platformio.ini`, `pyproject.toml`) are considered **read-only** and must not be modified without explicit user permission.
- **Workspace Hygiene**: All temporary files and scratch scripts MUST be placed in the `.agent_scratchpad/` directory. Avoid using system-wide temporary folders like `/tmp` or `C:\Temp`.
- **Python Execution Standard**: Always use the `-u` flag (unbuffered) for all Python executions to ensure logs are captured in real-time.
- **Reporting**: Maintain the weekly report at the specified path: `/media/hank/B0D4B41ED4B3E4AE/文件/週報`.


## Project Standards

### Python Documentation Requirements
All Python scripts in the `tools/` directories MUST include a standardized top-level docstring.

**Standard Docstring Format:**
```python
"""
module_name — Brief one-line overview of the script/module.

Detailed description of core functionality and features.
Explain the specific purpose, algorithms, or data handling logic.

Dependencies: list of key dependencies (e.g., numpy, pandas, src.log_reader).

Typical usage::

    python tools/example_script.py --arg value
"""
```

**Key Components:**
- **Header**: Short name and high-level summary.
- **Description**: Technical details and functional scope.
- **Dependencies**: Explicit list of internal and external requirements.
- **Usage**: Reproducible CLI or API examples.