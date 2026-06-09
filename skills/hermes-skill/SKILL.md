---
name: hermes
description: Use this skill to delegate simple or batch tasks to the Hermes Agent. Trigger this skill when you want to use 'hermes' to handle tasks like data processing, code generation, or routine documentation while respecting Gemini model usage limits. It automatically selects the optimal model based on task complexity.
---

# Hermes Skill

This skill allows you to leverage the `hermes` CLI tool, an AI assistant with tool-calling capabilities, to perform various tasks. It is specifically designed to manage Gemini API usage limits by selecting appropriate models based on task complexity.

## Mandatory Usage Logging

To ensure traceability and monitor quota consumption, **every call to Hermes must be logged** to `.agents/skills/hermes-skill/history.md` immediately after execution.

### Log Format
```markdown
### [YYYY-MM-DD HH:MM] Hermes Call
- **Task**: [Brief description of the work]
- **Model**: [Model name used]
- **Status**: [Success / Error]
- **Details**: [Key output or error message]
---
```

### Logging Instruction
After running `hermes`, use a non-interactive append or a file edit tool to update `.agents/skills/hermes-skill/history.md`. For example:
```bash
cat << 'EOF' >> .agents/skills/hermes-skill/history.md
### [YYYY-MM-DD HH:MM] Hermes Call
- **Task**: [Brief description of the work]
- **Model**: [Model name used]
- **Status**: [Success / Error]
- **Details**: [Key output or error message]
---
EOF
```
Using `cat << 'EOF'` prevents terminal hangs that can happen with interactive `cat >>`.

## Continuous Task Delegation (Session Isolation)

To allow `hermes` to act as a persistent worker without blocking your terminal, you must use its session management.
**CRITICAL: Do NOT use the `-c` (continue) flag.** The `-c` flag resumes the *globally* most recent session, which will cause catastrophic cross-contamination if you or the user are working on multiple projects simultaneously.
**CRITICAL: Do NOT use the `-z` (oneshot) flag.** It prevents contextual continuity.

### How to Delegate Tasks Continuously & Safely:
1. **Initial Task:** Start the work by running a standard chat query. This creates a new session.
   ```bash
   hermes chat -q "[INITIAL_TASK_DESCRIPTION]"
   ```
2. **Capture Session ID:** In the output of the command above, look for the text `Session: <SESSION_ID>` (e.g., `Session: 20260609_102223_eecac7`).
3. **Follow-up Tasks:** When you need Hermes to continue working on the same context or correct a previous output, you **MUST explicitly use the `-r <SESSION_ID>` flag** to resume that exact session.
   ```bash
   hermes chat -r [SESSION_ID] -q "[NEXT_TASK_OR_CORRECTION]"
   ```

### Skill Integration (Accessing Local Skills)
To allow Hermes to use skills from `./.agents/skills/` (e.g., `pptx`, `xlsx`, `code-review`), use one of the following methods:

#### Scheme A: Path Mounting (Persistent)
Configure Hermes to automatically scan the workspace skill directory.
```bash
hermes config set skills.paths '["~/.hermes/skills", "./.agents/skills"]'
```

#### Scheme B: Dynamic Preloading (Task-Specific)
When starting a session, use the `-s` or `--skills` flag to load the necessary capabilities.
```bash
hermes chat -s pptx -q "Create a presentation based on output/report.md"
```

## Core Capabilities
- **Task Delegation:** Offload simple or routine tasks to Hermes.
- **Model Intelligence:** Automatically switches between Flash and Pro models to optimize usage.
- **Contextual Memory:** Remembers conversation history across invocations when using the `-r <SESSION_ID>` flag.

## Usage Guidelines

### 1. General Usage
Always use `hermes chat -q` for tasks to ensure the session is recorded and can be resumed if follow-up is needed. **Never use the `-z` flag** as it prevents contextual continuity.

```bash
hermes chat -q "[PROMPT]"
```

### 2. Complexity-Based Model Selection
Refer to `Gemini Model Limit.csv` for the latest quotas. The following strategy is recommended:

| Task Type | Complexity | Recommended Model | Command Example |
| :--- | :--- | :--- | :--- |
| Simple query, summary | Low | `gemini-3.1-flash-lite` | `hermes chat -m google/gemini-3.1-flash-lite -q "..."` |
| **Quota Fallback** | **Low** | **`gemma-4-31b`** | **`hermes chat -m google/gemma-4-31b -q "..."`** |
| Code generation, analysis | Medium | `gemini-2.5-flash` | `hermes chat -m google/gemini-2.5-flash -q "..."` |
| Deep research, complex logic | High | `gemini-3.5-flash` or `gemini-3-flash` | `hermes chat -m google/gemini-3.5-flash -q "..."` |

### 3. Interactive Continuity
If the first attempt isn't perfect, just tell Hermes to fix it in the exact same session using its ID:
```bash
hermes chat -r [SESSION_ID] -q "That looks good, but please change the output format to JSON."
```

## Usage Limits (Summary from Gemini Model Limit.csv)

| Model | RPM | TPM | RPD | Usage Strategy |
| :--- | :---: | :---: | :---: | :--- |
| **Gemma 4 31B** | 15 | **Unlimited** | **1.5K** | **Ultra-Fallback** for text/data when Gemini is exhausted. |
| **3.1 Flash Lite** | 15 | 250K | 500 | **Primary** for simple text/data tasks. |
| **2.5 Flash** | 5 | 250K | 20 | Use for code-heavy or medium logic. |
| **3.5 Flash** | 5 | 250K | 20 | Use for high-precision flash tasks. |
| **3 Flash** | 5 | 250K | 20 | Alternative for high-precision tasks. |

*RPM: Requests Per Minute | TPM: Tokens Per Minute | RPD: Requests Per Day*

## Examples

**Example 1: Batch Data Summary & Follow-up**
Input: Use hermes to summarize these 10 log files using Flash Lite, then ask it to extract just the errors.
Action 1: `hermes chat -m google/gemini-3.1-flash-lite -q "Summarize the following logs: [LOG_CONTENTS]"`
*(Agent observes `Session: 20260609_123456_abcdef` in the output)*
Action 2: `hermes chat -r 20260609_123456_abcdef -q "Now extract only the critical errors from those logs."`

**Example 2: Code Refactoring**
Input: Ask hermes to refactor this function for better performance using 2.5 Flash.
Action: `hermes chat -m google/gemini-2.5-flash -q "Refactor this Python function for performance: [CODE]"`

**Example 3: Complex Investigation**
Input: Use hermes 3.5 Flash to investigate the root cause of the memory leak reported in the logs.
Action: `hermes chat -m google/gemini-3.5-flash -q "Investigate memory leak in: [CONTEXT]"`

## Safety and Security
Always review the output of Hermes before applying changes to the codebase. Ensure sensitive information is not sent to the models unless necessary for the task.
