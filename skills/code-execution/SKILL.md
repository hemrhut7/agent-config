---
name: code-execution
description: "Execute batch file operations, complex multi-step workflows, or general Python commands with intelligent environment selection (Venv > Global > Install). Includes output monitoring to prevent terminal hanging."
---

# Python Code Execution & Batch Processing

This skill handles both general Python execution and batch operations involving large numbers of files or multiple steps, ensuring an optimized environment and preventing terminal hangs.

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

## Batch Operations (10+ Files)

When handling batch operations:
1. Write the batch logic into a temporary Python script inside `.agent_scratchpad/`.
2. Execute the script using the environment selection logic above.
3. Return a statistical summary (modified/skipped/errors) rather than complete file contents.
4. Delete the temporary script after execution.

## Instructions
- **Command Transformation**: Use the determined executable + `-u`.
- **Dependency Management**: Only install packages if they are not available globally (when a venv is used) or when creating a new venv.
- **Error Analysis**: If execution fails, retrieve only the last 50 lines of `stderr` for troubleshooting.
- **Path Handling**: Use `pathlib` for cross-platform compatibility.

## Examples
### General Python Execution (Ubuntu)
`./.venv/bin/python -u src/main.py | tail -n 50`

### Batch Processing Script
```python
# .agent_scratchpad/batch_process.py
from pathlib import Path
import re

results = {"modified": 0, "skipped": 0, "errors": []}
for py_file in Path("src").rglob("*.py"):
    # ... logic ...
    results["modified"] += 1

print(f"Modified: {results['modified']}, Skipped: {results['skipped']}")
```

## Best Practices

✅ Use intelligent environment selection  
✅ Return statistical summaries for batch work  
✅ Use `-u` for unbuffered output  
✅ Include error counting and handling  

❌ Do not return all code content for batch operations  
❌ Do not use editing tools file-by-file for > 10 files
