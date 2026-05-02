---
name: code-execution
description: Execute batch file operations or complex multi-step workflows using Python scripts. Use when tasks involve batch processing of 10+ files, data transformation, or automated processes.
---

# Batch Code Execution

Use Python scripts to handle batch operations involving large numbers of files or multiple steps, avoiding manual processing one by one.

## When to Use

- Batch operations (10+ files)
- Complex multi-step workflows
- Iterative processing across multiple files

## Execution Strategy

### 1. Write Batch Processing Script
Write the batch logic into a temporary Python script inside `.agent_scratchpad/`:

```python
# .agent_scratchpad/batch_process.py
from pathlib import Path
import re

results = {"modified": 0, "skipped": 0, "errors": []}

for py_file in Path("src").rglob("*.py"):
    content = py_file.read_text(encoding="utf-8")
    new_content = re.sub(r"old_pattern", "new_pattern", content)
    if new_content != content:
        py_file.write_text(new_content, encoding="utf-8")
        results["modified"] += 1
    else:
        results["skipped"] += 1

print(f"Modified: {results['modified']}, Skipped: {results['skipped']}")
```

### 2. Execute using venv
Follow the execution specifications of the `run-python` skill:
```bash
.\.venv\Scripts\python.exe -u .agent_scratchpad/batch_process.py
```

### 3. Report Summary
Return a statistical summary (how many files were modified, how many skipped), rather than the complete file contents.

### 4. Cleanup Temporary Files
Delete the temporary script in `.agent_scratchpad/` after execution is complete.

## Best Practices

✅ Return statistical summaries, do not return complete file contents  
✅ Batch process rather than operate one by one  
✅ Use `pathlib` for cross-platform path handling  
✅ Include error counting and handling  

❌ Do not return all code content back to the context  
❌ Do not use editing tools file-by-file (when > 10 files)  
