---
trigger: always_on
---

0. **Master Protocol**: You MUST follow the logic in `.agents/skills/using-agents/SKILL.md`. This includes checking for specialized skills (like TDD, Systematic Debugging, and ESKF Optimization) before every action.

1. If the project is based on Python, all Python commands or scripts MUST follow the "code-execution" skill logic.

2. After code updates, compile or run the project to confirm there is not any error during the processing of compiling or running. If something goes wrong, you MUST follow the `systematic-debugging` skill.

3. If the project contains a graphify-out folder, you MUST prioritize checking its contents (e.g., GRAPH_REPORT.md or graph.json) during the research or exploration phase to gather architectural insights and module relationships.

4. **Memory First**: At the start of every new conversation or major task, you MUST automatically invoke the `memory` skill (read `brain.md` and trigger `Recall_Background`) before taking any other action.