<!-- SCOPE: Rules for executing code in a Windows environment. -->
# Windows Environment Memory

### [2026-05-24] Redirection Encoding
- **Issue**: PowerShell `>` operator uses `UTF-16LE`, crashing UTF-8/JSON readers.
- **Rule**: Write files directly in Python (`Path.write_text(encoding='utf-8')`).

### [2026-05-24] Multi-line Commands
- **Issue**: PowerShell quoting makes complex `python -c "..."` one-liners error-prone.
- **Rule**: Write multi-step operations to `.agent_scratchpad/script.py` and execute.
