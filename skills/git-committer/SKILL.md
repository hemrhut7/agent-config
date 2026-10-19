---
name: git-committer
description: "Analyze Git changes, generate standardized commit messages, and execute commits. Force trigger this workflow when the user mentions 'commit', 'save', 'stash the changes', or when version control needs to be advanced after completing a long task."
---

# Git Commit Management Workflow


## Core Rules
- **Automation First & Mandatory Analysis**: You MUST execute `.agents/skills/git-committer/scripts/git_helper.py --action analyze_all` before drafting any commit message. Never draft a message based solely on memory or recent conversation history.
- **Comprehensive Scope**: The commit plan must account for all intended modifications detected by the analysis tool, rather than just the partial fragments discussed during the conversation. Each message must describe its own commit's changes, and the full sequence must cover the complete intended change set.
- **Format Compliance**: Select language based on context (default is English).
   - English messages: Comply with [EN_FORMAT.md](EN_FORMAT.md).
   - Chinese messages: Comply with [CH_FORMAT.md](CH_FORMAT.md).
- **Plan Before Action**: After analysis, always present a comprehensive plan (including any necessary submodule repairs or intermediate commits) and the proposed message or messages. Wait for user approval before modifying any files or executing any state-changing git commands.
- **Commit Confirmation**: Ensure the user approves every proposed message and the full sequence of actions before executing any `commit`.

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
   - Review the full change set, not only the staged diff: use status and inspect unstaged and untracked changes as needed so the plan accounts for all intended modifications.

3. **Choose Commit Granularity**:
   - Decide whether the changes form one cohesive, clearly describable unit or contain multiple independently meaningful updates.
   - When there is a substantial amount of code change, split it into multiple commits when the actual updates support meaningful, cohesive groups (for example, separate features or fixes, with their directly related tests). Do not split merely because there are many changed files or lines; keep tightly coupled implementation and tests together.
   - For each proposed commit, specify its order, the exact logical scope/files or hunks it will contain, and its own message in the applicable format. Make sure the sequence is coherent and that no intended changes are omitted or accidentally included in another commit.
   - If the changes are one cohesive unit, use a single commit.

4. **Plan and Verification**:
   - Present the complete commit plan, all proposed messages, and a list of all intended actions (e.g., submodule updates, file additions, and how changes will be staged).
   - Check if technical jargon (e.g., `EKF`, `DMA`) is retained.
   - Ensure each message describes its commit's changes, and the plan collectively covers all intended modifications found in the analysis.
   - **STOP**: Wait for explicit user approval before proceeding to any execution.

5. **Execute Commit**:
   - After approval, stage only the changes for the first planned commit (use interactive/hunk staging when a file contains changes for different commits), then run `analyze_all` again and verify the staged diff matches that commit's approved scope.
   - Run `python .agents/skills/git-committer/scripts/git_helper.py --action commit --message "[Approved Message]"`.
   - For a multi-commit plan, verify the commit, then stage and analyze the next approved group before committing it. Keep changes assigned to later commits out of the current commit.
   - **Protection Mechanism**: If there are unresolved conflicts, the script will automatically abort the commit.

6. **Confirm Commit(s)**:
   Use `git log` and `git status` to confirm the planned commits were created and check whether any intended changes remain.

## Error Handling
- **No staged changes**: After user approval, stage only the changes included in the approved first commit, then verify the staged diff before committing.
- **Conflict Warning**: If the script warns of conflicts, please resolve the conflicts first, then re-run `analyze_all`.
- **Submodule Dirty**: If there are changes in the submodule, include the plan to process them (e.g., `cd` into submodule, commit/reset) in your proposal to the user. DO NOT process them without approval.
