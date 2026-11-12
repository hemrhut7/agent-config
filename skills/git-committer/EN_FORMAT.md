Git Commit Formatter Skill

When writing a git commit message, you MUST follow the Conventional Commits specification.

Format
`<type>[optional scope]: <description>`

If additional context is useful, add a blank line after the summary line and include bullet points that explain the main changes.

Allowed Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries such as documentation generation

Instructions
1. Analyze the changes to determine the primary `type`.
2. Identify the `scope` if applicable (e.g., specific component or file).
3. Write a concise `description` in an imperative mood (e.g., "add feature" not "added feature").
4. If extra context is helpful, add a short body with bullet points after a blank line.
5. If there are breaking changes, add a footer starting with `BREAKING CHANGE:`.

## Concise style
Keep the Conventional Commit summary, followed by at most two short bullets with the most important technical details. Omit extended context and secondary implementation details.

Example:
```text
fix(link-monitor): correct MUX selection and failover behavior
- Invert PB3 channel mapping and add readback diagnostics.
- Add `setauto` and raise the DTC timeout threshold to 10.
```

Example
`feat(auth): implement login with google`

`chore(docs): archive prior session and document real-time plotting optimizations`

- Archive working notes from prior session into brain_2026-06-25.md.
- Add notes on sensor health check and telemetry receiver dynamic parsing.
- Document high-frequency plotting optimizations using collections.deque, busy-wait sleep fix, and signal batching.