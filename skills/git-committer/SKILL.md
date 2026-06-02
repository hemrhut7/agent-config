---
name: git-committer
description: "Analyze Git changes, generate standardized commit messages, and execute commits. Force trigger this workflow when the user mentions 'commit', 'save', 'stash the changes', or when version control needs to be advanced after completing a long task."
---

# Git Commit Management Workflow


## Core Rules
- **Automation First & Mandatory Analysis**: You MUST execute `.agents/skills/git-committer/scripts/git_helper.py --action analyze_all` before drafting any commit message. Never draft a message based solely on memory or recent conversation history.
- **Comprehensive Scope**: The commit message must describe all modifications detected by the analysis tool, rather than just the partial fragments discussed during the conversation.
- **Format Compliance**: Select language based on context (default is English).
   - English messages: Comply with [EN_FORMAT.md](EN_FORMAT.md).
   - Chinese messages: Comply with [CH_FORMAT.md](CH_FORMAT.md).
- **Plan Before Action**: After analysis, always present a comprehensive plan (including any necessary submodule repairs or intermediate commits) and the proposed message. Wait for user approval before modifying any files or executing any state-changing git commands.
- **Commit Confirmation**: Ensure you confirm the message content and the sequence of actions with the user before executing `commit`.

<EXTREMELY-IMPORTANT>
You MUST STOP and ask the user to confirm the final commit message before running any commit command. DO NOT assume the proposed message is final.
</EXTREMELY-IMPORTANT>

## Execution Workflow

1. **One-Click Extraction Analysis**:
   Run `python .agents/skills/git-committer/scripts/git_helper.py --action analyze_all`.
   - **Note**: If the change content is too large, the script will automatically save the report to `.agent_scratchpad/auto_analysis.md` and display a summary in the terminal. Finally, please delete the automatically generated report so it does not occupy space ('auto_analysis.md').
   - Write the Commit Message based on the report content (read the temporary file if one exists).

2. **Drafting**:
   Generate the commit message by referencing the `Detailed Staged Diff` and `Recent Commits Context` in the report.

3. **Plan and Verification**:
   - Present the proposed commit message and a list of all intended actions (e.g., submodule updates, file additions).
   - Check if technical jargon (e.g., `EKF`, `DMA`) is retained.
   - Ensure the message reflects all core modifications found in the report.
   - **STOP**: Wait for explicit user approval before proceeding to any execution.

4. **Execute Commit**:
   Run `python .agents/skills/git-committer/scripts/git_helper.py --action commit --message "[Message Content]"`.
   - **Protection Mechanism**: If there are unresolved conflicts, the script will automatically abort the commit.

5. **Confirm Commit**:
   Use `git log -n 1` to confirm.

## Error Handling
- **No staged changes**: Run `git add` first.
- **Conflict Warning**: If the script warns of conflicts, please resolve the conflicts first, then re-run `analyze_all`.
- **Submodule Dirty**: If there are changes in the submodule, include the plan to process them (e.g., `cd` into submodule, commit/reset) in your proposal to the user. DO NOT process them without approval.
