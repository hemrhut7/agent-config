<!-- SCOPE: Stable developer memory and rules for executing code in a Windows environment. Read when developing or running tasks on Windows/PowerShell. -->
# Windows Environment Memory & Rules

### [2026-05-24 09:22] Tags: windows, powershell, encoding, compatibility
**Rule 1: Never use standard shell redirection (`>`) to write text or JSON files**
- **Pitfall**: On Windows PowerShell, the redirection operator (`>`) or `Out-File` writes text files using `UTF-16LE` encoding (with byte-order marks) by default. This causes subsequent file reading operations, `view_file` calls, and JSON loaders (which expect `UTF-8`) to crash with decoding or unsupported MIME type errors.
- **Prevention**: Always perform file writing operations directly within Python using `Path(file).write_text(content, encoding='utf-8')` instead of shell-level stdout redirection.

**Rule 2: Avoid multi-line command string one-liners**
- **Pitfall**: Attempting to execute complex, multi-line Python snippets via command-line strings (e.g. `python -c "..."`) is highly error-prone on Windows because of PowerShell's quoting and escape rules. It frequently causes parser syntax errors (like `SyntaxError: unterminated string literal`).
- **Prevention**: Proactively write complex multi-step operations into a temporary Python script in the `.agent_scratchpad/` directory, execute the script, and delete it upon completion.
