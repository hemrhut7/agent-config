<!-- SCOPE: Knowledge about replay. Read when related tasks arise. -->
# Replay

### [2026-06-23 09:51] Tags: replay, plotting
Modified AP_Replay_Orchestrator.py to only plot the largest GNSS outage segment and add GNSS Outage to the legend in all plots.

### [2026-06-23 09:59] Tags: replay, plotting
Updated AP_Replay_Orchestrator.py to slice log data to the largest continuous recording segment (detecting gaps > 5.0 seconds) and plot only that segment, while keeping all overlapping outages plotted and labeled properly in legends.

### [2026-06-23 10:09] Tags: replay, output_dir
Updated AP_Replay_Orchestrator.py to resolve the default args.out directory dynamically using the generated replayed binary's filename (e.g. 2026-05-27 16-29-21_replay_outage3) so that analysis results are correctly saved in the outage-specific replay_output directory instead of the generic one.

### [2026-06-23 14:06] Tags: replay, analyzer, segment
Updated AP_ILB_Replay_Analyzer.py to filter plotted data to the largest continuous log segment (splitting by gaps > 5.0 seconds), clip the flight mode backgrounds and text labels correctly, set x-axis limits of Plot 2 and Plot 3 to exactly [t_min, t_max], and moved Plot 3 legends after the outage shading loop to correctly include the GNSS outage hatch in the legends.
