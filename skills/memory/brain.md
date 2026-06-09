<!-- SCOPE: Today's task log and working memory. Read at conversation start to resume context. -->
# Brain — Working Memory

## Last Updated: 2026-05-28 16:22

### Active Tasks
- (none yet)

### Session Notes
- Restored missing Plotly annotations (modes, events, params) in `uavlogviewer`.
- Implemented async rendering for annotations to prevent UI hangs.
- Added y-axis reset logic to fix stale title bugs.
- Fixed legend statistics calculation (Min, Max, Mean, Std) in `Plotly.vue` and `PlotlyPopup.vue`:
  - Resolved stack overflow error (`RangeError: Maximum call stack size exceeded`) caused by `Math.min(...yInside)` on large logs.
  - Switched from `Plotly.relayout` to `Plotly.restyle` for updating trace name strings to ensure the legend updates correctly.
  - Handled undefined initial range cases by accessing `_fullLayout` fallback.
  - Ensured initial calculation triggers during initial plot generation using `requestAnimationFrame`.
  - Recalculated statistics when synchronized zooming occurs across multiple charts.
- Committed all changes to master.

### Pending Decisions
- (none)
