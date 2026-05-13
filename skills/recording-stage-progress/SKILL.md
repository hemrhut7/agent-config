---
name: recording-stage-progress
description: "Directly write and append stage results, intermediate data, or decisions to a Markdown file. Use this during long tasks, complex analysis, or when information needs to be retained across turns, preventing information loss due to long contexts."
---

# Stage Progress Recording

## Core Function

This skill is responsible for directly appending intermediate results in a standardized Markdown format to a record file (such as `progress.md` or `session_log.md`) during the execution of complex or multi-step tasks, establishing a traceable execution log.

## Record Format Standards

Every time you write or append content, you must strictly follow the structure below. Ensure that each record point is separated by a horizontal rule (`---`):

```markdown
### [YYYY-MM-DD HH:MM] Stage: [Stage Name]
- **Execution Status**: [Success / Partially Complete / Error Occurred]
- **Key Output**:
  [Place the complete data output results, summary, error messages, or analysis results here]
- **Remaining Issues / Next Steps**: [Record unresolved issues or the next action]

---
```

## Execution Flow

1. **Identify Record Points**: Proactively trigger this before completing a sub-task, obtaining important data, or preparing to switch to the next workflow.
2. **Prepare Content**: Organize the current context and results according to the "Record Format Standards" above, preserving as much information as possible to avoid taking things out of context.
3. **Append to File**: Use the system's file editing tools or Bash commands to directly append the content to the end of the target `.md` file.

   **Bash Append Operation Example** (if using bash tools):
   ```bash
   cat >> progress.md << 'EOF'
   
   ### [2026-04-07 16:30] Stage: Initial API Data Scraping
   - **Execution Status**: Success
   - **Key Output**:
     Successfully retrieved 50 pages of the product list. Data structure confirmed to include `id`, `price`, `stock`.
   - **Remaining Issues / Next Steps**: Begin data cleaning and normalization of the price field.
   
   ---
   EOF
   ```
4. **Quality Verification**: Ensure that the write operation did not overwrite previous historical records (it must be Append, not Overwrite).