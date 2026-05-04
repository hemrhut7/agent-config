---
name: ardupilot-built-in-log-tools
description: "Use built-in pymavlink tools to perform deep analysis on ArduPilot logs (.bin, .tlog). Supports parameter extraction, message filtering, CSV export, and trend plotting. Trigger whenever the user asks to analyze Ardupilot telemetry logs, parse bin files, or plot data from flight logs."
---

# ArduPilot Built-in Tool Management Skill

This skill allows the Agent to directly invoke scripts in `agents/skills/ardupilot-built-in-log-tools/scripts` for efficient log processing.

## Tool Directory Specifications
Built-in tools are located at: `agents/skills/ardupilot-built-in-log-tools/scripts`
You should switch to this directory or use absolute paths when executing.

## Core Workflows and Commands

### Feature 1: List Data Types and Statistics
Use `mavmsgstats.py` to get the frequency of all tags in the log.
```bash
python3 mavmsgstats.py data/flight.bin
```

### Feature 2: Extract Vehicle Parameter Table
Use `mavparms.py` to read the complete configuration.
```bash
python3 mavparms.py data/flight.bin
```

### Feature 3: Advanced Efficient Plotting (New)
This is a more efficient general-purpose plotting tool compared to `mavgraph.py`. It uses single-pass parsing and automatically handles data alignment and breakpoint detection.

- **Usage**: `python3 fast_plot.py <log_path> "MSG1.Field1" "MSG2.Field2" ...`
- **Example**: Plot comparison of Roll and Pitch
  ```bash
  python3 fast_plot.py data/flight.bin "ATT.Roll" "ATT.Pitch" --output output/fast_plot.png
  ```

### Feature 4: Unified Analysis Entry and Caching Architecture (Highest Performance - New)
To solve the time-consuming issue of repeatedly parsing massive logs, use `auto_analysis.py` to handle composite tasks:
1. **Log Caching**: The first execution caches the log as `.pkl` (stored in `.logcache/`), subsequent loading takes only milliseconds.
2. **Integrated Workflow**: A single command completes alignment, PVA error calculation, and chart report generation.
3. **Smart Downsampling**: Automatically optimizes plot points to prevent Matplotlib rendering freezes.

- **Usage**: `python3 auto_analysis.py <log_path> --task pva --out <output_prefix>`
- **Example**:
  ```bash
  python3 auto_analysis.py data/flight.bin --task pva --out output/pva_report
  ```

## Auxiliary Feature: Quick Summary
To quickly understand flight conditions (like total flight time), run:
```bash
python3 mavsummarize.py data/flight.bin
```

## Progressive Disclosure
If you are unsure about the meaning of a specific message (like NKF1), please read [MESSAGE_REFERENCE.md](MESSAGE_REFERENCE.md).

## Notes
- **Plotting Restrictions**: When plotting with `mavgraph.py`, field names must follow the "TYPE.Field" format (e.g., `ATT.Roll`).
- **Path Specifications**: Always use forward slashes `/`. If the path contains spaces, please enclose it in quotes.