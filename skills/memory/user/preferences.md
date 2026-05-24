- **Estimation Philosophy**: Prefers Global Batch Least Squares (Scheme C/Factor Graph) with IMU pre-integration for baseline data generation.
- **Initialization Rule**: Avoid using EKF results for initializing baseline smoothing to prevent feedback loops. Use sensor-based initialization (accLeveling + GPS diff).
- **Parameter Observation**: Explicitly track GNSS delay, wind states, and airspeed parameters in global optimization.
- **Agent Workflow**: Values "Deep Memory" cycles (`@[/memory]`) to maintain context across sessions and ensure technical discipline in complex refactoring tasks.
- **Windows Environment Redirection**: Avoid PowerShell stdout redirection (`>`) for JSON/text files to prevent UTF-16LE conversion. Always use Python-based UTF-8 writing or specify explicit UTF-8 encoding options.
- **Codebase Research Philosophy**: Prioritize using `graphify` (`/graphify query`, `/graphify path`, `/graphify explain`) for codebase exploration and architectural searches. Always ensure the graph is in sync with the latest code updates by performing a fast incremental update (`/graphify --update`) if code changes are detected.

