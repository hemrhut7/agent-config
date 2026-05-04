---
name: file-operations
description: "Analyze files and get detailed metadata including size, line counts, modification times, and content statistics. Use when users request file information, statistics, or analysis without modifying files."
---

# File Operations

Analyze files and retrieve metadata using native tools without modifying files.

## When to Use

- "analyze [file]"
- "get file info for [file]"
- "how many lines in [file]"
- "compare [file1] and [file2]"
- "file statistics"

## Core Operations

### File Size & Metadata

**Windows (PowerShell):**
```powershell
Get-Item [file_path] | Select-Object Length, LastWriteTime
Get-ChildItem [directory] | Format-Table Name, Length, LastWriteTime
```

**Linux:**
```bash
stat -c "%s bytes, modified %y" [file_path]
ls -lh [directory]
```

### Line Counts

**Cross-platform (PowerShell):**
```powershell
(Get-Content [file_path]).Count                         # Single file
Get-ChildItem [dir] -Filter *.py -Recurse | ForEach-Object { "$($_.Name): $((Get-Content $_.FullName).Count) lines" }
```

**Linux:**
```bash
wc -l [file_path]
find [dir] -name "*.py" | xargs wc -l
```

### Content Analysis
Use `view_file` to analyze structure, then use `grep_search` to count functions/classes/imports.

### Pattern Search
```
grep_search: pattern="^def ", SearchPath="src/"         # Find functions
grep_search: pattern="TODO|FIXME", SearchPath="."       # Find TODOs
grep_search: pattern="^import ", SearchPath="."         # Find imports
```

### Find Files
Use `list_dir` to explore directory structure.

## Workflow Examples

### Comprehensive File Analysis
1. View file: `view_file [file_path]`
2. Count functions: `grep_search pattern="def " SearchPath="[file]"`
3. Count classes: `grep_search pattern="class " SearchPath="[file]"`

### Code Quality Metrics
1. Find all Python files: `list_dir [src_dir]`
2. Search TODOs: `grep_search pattern="TODO|FIXME|HACK"`
3. Find test files: `grep_search pattern="test_" SearchPath="."`

## Best Practices

- **Non-destructive**: Only read and analyze, never modify
- **Efficient**: Use `grep_search` for large codebases, `view_file` for small files
- **Context-aware**: Compare to project averages, suggest optimizations
