---
name: code-refactor
description: Perform bulk code refactoring operations like renaming variables/functions across files, replacing patterns, and updating API calls. Use when users request renaming identifiers, replacing deprecated code patterns, updating method calls, or making consistent changes across multiple locations.
---

# Code Refactor

Systematic code refactoring across files.

## Mode Selection

- **1-9 files**: Use native tools (`grep_search` + `replace_file_content`)
- **10+ files**: Use `code-execution` skill（寫批量 Python 腳本處理）

**Batch example (10+ files):**
```python
# .agent_scratchpad/batch_rename.py
from pathlib import Path
import re

count = 0
for f in Path("src").rglob("*.py"):
    text = f.read_text(encoding="utf-8")
    new_text = re.sub(r'\boldName\b', 'newName', text)
    if new_text != text:
        f.write_text(new_text, encoding="utf-8")
        count += 1
print(f"Modified {count} files")
```

## When to Use

- "rename [identifier] to [new_name]"
- "replace all [pattern] with [replacement]"
- "refactor to use [new_pattern]"
- "update all calls to [function/API]"
- "convert [old_pattern] to [new_pattern]"

## Core Workflow (Native Mode)

### 1. Find All Occurrences
```
grep_search: Query="getUserData", SearchPath="src/"                    # Find files
grep_search: Query="getUserData", SearchPath="src/", MatchPerLine=true # Verify with context
```

### 2. Replace All Instances
```
replace_file_content:
  TargetFile="src/api.py"
  TargetContent="getUserData"
  ReplacementContent="fetchUserData"
  AllowMultiple=true
```

### 3. Verify Changes
```
grep_search: Query="getUserData", SearchPath="src/"  # Should return no matches
```

## Workflow Examples

### Rename Function
1. Find: `Grep(pattern="getUserData", output_mode="files_with_matches")`
2. Count: "Found 15 occurrences in 5 files"
3. Replace in each file with `replace_all=true`
4. Verify: Re-run Grep
5. Suggest: Run tests

### Replace Deprecated Pattern
1. Find: `Grep(pattern="\\bvar\\s+\\w+", output_mode="content", -n=true)`
2. Analyze: Check if reassigned (let) or constant (const)
3. Replace: `Edit(old_string="var count = 0", new_string="let count = 0")`
4. Verify: `npm run lint`

### Update API Calls
1. Find: `Grep(pattern="/api/auth/login", output_mode="content", -n=true)`
2. Replace: `Edit(old_string="'/api/auth/login'", new_string="'/api/v2/authentication/login'", replace_all=true)`
3. Test: Recommend integration tests

## Best Practices

**Planning:**
- Find all instances first
- Review context of each match
- Inform user of scope
- Consider edge cases (strings, comments)

**Safe Process:**
1. Search → Find all
2. Analyze → Verify appropriate
3. Inform → Tell user scope
4. Execute → Make changes
5. Verify → Confirm applied
6. Test → Suggest running tests

**Edge Cases:**
- Strings/comments: Ask if should update
- Exported APIs: Warn of breaking changes
- Case sensitivity: Be explicit

## Tool Reference

**Edit with replace_all:**
- `replace_all=true`: Replace all occurrences
- `replace_all=false`: Replace only first (or fail if multiple)
- Must match EXACTLY (whitespace, quotes)

**Grep patterns:**
- `-n=true`: Show line numbers
- `-B=N, -A=N`: Context lines
- `-i=true`: Case-insensitive
- `type="py"`: Filter by file type

## Integration

- **test-fixing**: Fix broken tests after refactoring
- **code-transfer**: Move refactored code
- **feature-planning**: Plan large refactorings
