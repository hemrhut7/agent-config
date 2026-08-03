# AI Agents Submodule

The purpose of this submodule is to **quickly apply consistent, standardized AI Agent skills, rules, and workflows** across various software projects.

By adding this repository as a Git submodule inside a project's root under `/.agents`, AI agent surfaces (such as the Antigravity CLI) can automatically discover and load these custom configurations, providing developers with a unified AI-assisted experience.

---

## 📂 Directory Structure

This submodule consists of three main components:

```
.agents/
├── README.md           ← Submodule sitemap and documentation
├── rules/              ← Persistent prompt instructions (e.g., principle.md - always_on)
├── skills/             ← Custom capabilities, scripts, and domain knowledge packages
│   ├── code-execution/ ← Dynamic environment selector and output monitoring
│   └── ...             
└── workflows/          ← Interactive step-by-step guides triggered via slash commands
    ├── codex-planning-and-reviewing.md
    ├── competitive-research-workflow.md
    └── ...
```

1. **`rules/` (AI Rules & Constraints)**:
   - Contains files defining style guidelines or behavioral constraints. Files configured with `trigger: always_on` in their YAML frontmatter are automatically evaluated on every prompt.
2. **`skills/` (Custom Skills)**:
   - Folders of instructions (`SKILL.md`), executable scripts, and unit tests that extend agent features (e.g., automated error evaluation, presentation generation, or knowledge graphs).
3. **`workflows/` (Task Trajectory Workflows)**:
   - Markdown guides outlining multi-stage execution checklists. Developers can trigger a workflow by running a slash command corresponding to the filename (e.g., `/codex-planning-and-reviewing`).

---

## ⚙️ How to Integrate

To apply this standardized agent environment in a new project, execute the following commands in the root of your target repository:

```bash
# 1. Add this repository as a submodule under the /.agents folder
git submodule add <your-agents-repository-url> .agents

# 2. Initialize and update the submodule
git submodule update --init --recursive
```

Once added, any Antigravity CLI or compatible IDE session initialized in the workspace will automatically recognize the custom rules, skills, and workflows.

---

## 🚨 Portability & Compatibility Guidelines

Since this submodule is shared across multiple projects with different tech stacks and structures, all modifications to this submodule MUST strictly comply with these guidelines:

1. **No Project-Specific Absolute Paths**:
   - Never use absolute paths (e.g. `C:/Users/...` or `/home/user/...`) or reference specific parent project folders (e.g., `INS_Reader`).
2. **Use Relative Paths**:
   - Refer to files or directories in the parent project using relative paths starting with `../../` (which points to the parent project's root from the `workflows/` directory).
   - Reference internal skills using `../skills/` relative references.
3. **Keep the Submodule Git Clean**:
   - Temporary files or session plan logs (like `plan.md`) must be written to the parent project's workspace scratchpad (e.g., `../../.agent_scratchpad/`). Never commit project-specific scratch files directly inside this submodule.
