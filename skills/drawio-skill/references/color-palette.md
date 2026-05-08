# Color Palette & Brand Style

**This is the single source of truth for all colors and brand-specific styles.** To customize diagrams for your own brand, edit this file — everything else in the skill is universal.

---

## Shape Colors (Semantic)

Colors encode meaning, not decoration. Each semantic purpose has a fill/stroke pair, optimized for a clean, modern aesthetic with light fills and bold strokes.

| Semantic Purpose | Fill | Stroke |
|------------------|------|--------|
| Primary/Neutral | `#f0f9ff` | `#0284c7` |
| Secondary | `#f8fafc` | `#475569` |
| Tertiary | `#ffffff` | `#94a3b8` |
| Start/Trigger | `#ffedd5` | `#ea580c` |
| End/Success | `#f0fdf4` | `#16a34a` |
| Warning/Reset | `#fef2f2` | `#dc2626` |
| Decision | `#fefce8` | `#ca8a04` |
| AI/LLM | `#f5f3ff` | `#7c3aed` |
| Inactive/Disabled | `#f1f5f9` | `#64748b` (use dashed stroke) |
| Error | `#fef2f2` | `#dc2626` |

**Rule**: Always pair a darker stroke with a lighter fill for contrast. The fill should be very subtle (Tailwind 50 level), and the stroke should be distinct and legible (Tailwind 500/600 level).

---

## Text Colors (Hierarchy)

Use color on free-floating text to create visual hierarchy without containers.

| Level | Color | Use For |
|-------|-------|---------|
| Title | `#0f172a` | Section headings, major labels |
| Subtitle | `#334155` | Subheadings, secondary labels |
| Body/Detail | `#475569` | Descriptions, annotations, metadata |
| On light fills | `#0f172a` | Text inside standard light-colored shapes |
| On dark fills | `#ffffff` | Text inside dark-colored shapes (use sparingly) |

---

## Evidence Artifact Colors

Used for code snippets, data examples, and other concrete evidence inside technical diagrams.

| Artifact | Background | Text Color |
|----------|-----------|------------|
| Code snippet | `#0f172a` | Syntax-colored (language-appropriate) |
| JSON/data example | `#0f172a` | `#22c55e` (green) |

---

## Default Stroke & Line Colors

| Element | Color |
|---------|-------|
| Arrows | Use the stroke color of the source element's semantic purpose (e.g., `#0284c7`) |
| Structural lines (dividers, trees, timelines) | Slate (`#64748b`) or Primary stroke (`#0284c7`) |
| Marker dots (fill + stroke) | Primary stroke (`#0284c7`) |

---

## Background

| Property | Value |
|----------|-------|
| Canvas background | `#ffffff` or `#fcfdfe` |
