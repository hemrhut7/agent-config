---
trigger: always_on
---

0. **Skill Check**: Before starting any task, check `.agents/skills/` and read any applicable `SKILL.md` (including domain skills like ESKF Optimization).

1. **Python Execution**: Prefer the workspace `.venv/bin/python -u` (fall back to global Python or ask before creating/installing if missing); for batch edits across 10+ files, run a temporary script in `.agent_scratchpad/` and delete it afterward.

2. **Engineering Discipline**:
   - **Test-Driven Development**: Write a failing test before production code, implement minimal code to pass, then refactor.
   - **Systematic Debugging**: On any bug or failure, reproduce and identify the root cause before proposing fixes; never guess or apply unverified patches.
   - **Verification Before Completion**: Run relevant build/test/verification commands after final edits and confirm actual passing output before claiming completion.

3. If the project contains a graphify-out folder, you MUST prioritize checking its contents (e.g., GRAPH_REPORT.md or graph.json) during the research or exploration phase to gather architectural insights and module relationships.

4. In C or C++, only manually add reserved bytes for alignment when a struct is required for packet transmission and needs explicit packing/alignment semantics; otherwise, do not add unnecessary alignment.

5. After code edits, do not automatically stage the changes into Git.