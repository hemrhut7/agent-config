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

## Sub-Agent Delegation Strategy

Hermes is a primary candidate for **Sub-Agent Delegation** via the `invoke_subagent` tool. Use it to "compress" complex or repetitive work, keeping the main session history lean.

### Skill Integration (Accessing Local Skills)
To allow Hermes to use skills from `./.agents/skills/` (e.g., `pptx`, `xlsx`, `code-review`), use one of the following methods:

#### Scheme A: Path Mounting (Persistent)
Configure Hermes to automatically scan the workspace skill directory.
```bash
hermes config set skills.paths '["~/.hermes/skills", "./.agents/skills"]'
```

#### Scheme B: Dynamic Preloading (Task-Specific)
When delegating a specific task, use the `-s` or `--skills` flag to load the necessary capabilities.
```bash
# Example: Using Hermes to generate a PPTX report
hermes -s pptx -z "Create a presentation based on output/report.md"
```

### When to Delegate to Hermes:
- **Repetitive Batch Tasks:** Processing multiple files (e.g., "Summarize 20 log files").
- **High-Volume Output:** Commands that return massive data streams.
- **Speculative Research:** Trial-and-error investigations before a clear path is found.

### How to Invoke as Sub-Agent:
When using `invoke_subagent` with the `self` or `research` agent type, specify a clear `Prompt` and `Role`.

```json
{
  "Subagents": [
    {
      "TypeName": "self",
      "Role": "Generalist Assistant",
      "Prompt": "Use hermes to [TASK_DESCRIPTION]. Use model [MODEL_NAME] to respect quotas. Return a structured summary of the findings."
    }
  ]
}
```
*Note: Since 'hermes' is a CLI tool, it is typically invoked via the `self` or `research` sub-agent or directly using `run_command`.*

## Core Capabilities
- **Task Delegation:** Offload simple or routine tasks to Hermes.
- **Model Intelligence:** Automatically switches between Flash and Pro models to optimize usage.
- **Oneshot Mode:** Execute single prompts and get direct output for integration.

## Usage Guidelines

### 1. General Usage
Use `hermes -z` (oneshot mode) for simple tasks where you just need the result.

```bash
hermes -z "[PROMPT]"
```

### 2. Complexity-Based Model Selection
Refer to `Gemini Model Limit.csv` for the latest quotas. The following strategy is recommended:

| Task Type | Complexity | Recommended Model | Command Example |
| :--- | :--- | :--- | :--- |
| Simple query, summary | Low | `gemini-3.1-flash-lite` | `hermes -m google/gemini-3.1-flash-lite -z "..."` |
| **Quota Fallback** | **Low** | **`gemma-4-31b`** | **`hermes -m google/gemma-4-31b -z "..."`** |
| Code generation, analysis | Medium | `gemini-2.5-flash` | `hermes -m google/gemini-2.5-flash -z "..."` |
| Deep research, complex logic | High | `gemini-3.5-flash` or `gemini-3-flash` | `hermes -m google/gemini-3.5-flash -z "..."` |

### 3. Interactive Sessions
For tasks requiring multiple steps, use the `chat` command.

```bash
hermes chat -q "[PROMPT]"
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

**Example 1: Batch Data Summary**
Input: Use hermes to summarize these 10 log files using Flash Lite.
Action: `hermes -m google/gemini-3.1-flash-lite -z "Summarize the following logs: [LOG_CONTENTS]"`

**Example 2: Code Refactoring**
Input: Ask hermes to refactor this function for better performance using 2.5 Flash.
Action: `hermes -m google/gemini-2.5-flash -z "Refactor this Python function for performance: [CODE]"`

**Example 3: Complex Investigation**
Input: Use hermes 3.5 Flash to investigate the root cause of the memory leak reported in the logs.
Action: `hermes -m google/gemini-3.5-flash -z "Investigate memory leak in: [CONTEXT]"`

## Safety and Security
Always review the output of Hermes before applying changes to the codebase. Ensure sensitive information is not sent to the models unless necessary for the task.
