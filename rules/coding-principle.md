---
trigger: always_on
---

1. If the project is based on Python, all Python commands or scripts MUST follow the "run-python" (python-executor) skill logic. This involves prioritizing the workspace `.venv`, but allows intelligent fallback to the global environment if modules are missing, or asking the user if no environment exists. Only when executing 'graphify' commands can the global Python interpreter be used directly.

2. After code updates, compile or run the project to confirm there is not any error during the processing of compiling or running. If something goes wrong, try to find out the reason and fix it.

3. If the project contains a graphify-out folder, you MUST prioritize checking its contents (e.g., GRAPH_REPORT.md or graph.json) during the research or exploration phase to gather architectural insights and module relationships.