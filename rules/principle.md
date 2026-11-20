---
trigger: always_on
---

0. **Master Protocol**: You MUST follow the logic in `.agents/skills/using-agents/SKILL.md`. This includes checking for specialized skills (like ESKF Optimization) before every action.

1. If the project is based on Python, all Python commands or scripts MUST follow the "code-execution" skill logic.

2. **Engineering Discipline**:
   - **Test-Driven Development**: Write a failing test before production code, implement minimal code to pass, then refactor.
   - **Systematic Debugging**: On any bug or failure, reproduce and identify the root cause before proposing fixes; never guess or apply unverified patches.
   - **Verification Before Completion**: Run relevant build/test/verification commands after final edits and confirm actual passing output before claiming completion.

3. If the project contains a graphify-out folder, you MUST prioritize checking its contents (e.g., GRAPH_REPORT.md or graph.json) during the research or exploration phase to gather architectural insights and module relationships.

4. In C or C++, only manually add reserved bytes for alignment when a struct is required for packet transmission and needs explicit packing/alignment semantics; otherwise, do not add unnecessary alignment.

5. After code edits, do not automatically stage the changes into Git.