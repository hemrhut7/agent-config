# Hermes Usage History

### [2026-06-09 09:56] Hermes Call
- **Task**: Draft the Traditional Chinese analysis report of the EKF switchback mechanism at disarming.
- **Model**: Default (Gemini)
- **Status**: Success
- **Details**: Generated a concise markdown explanation of the C++ logic in AP_NavEKF3.cpp that forces primary core reset to Core 0 upon landing and disarming to avoid EKF lane lottery.
---
### [2026-06-09 13:31] Hermes Call
- **Task**: Integrate vibration/clipping code analysis into ekf_lane_switch_causes.md section 4
- **Model**: google/gemini-2.5-flash (then google/gemini-3.5-flash)
- **Status**: Error (both models returned HTTP 404)
- **Details**: Gemini API unavailable. Task completed manually by parent agent instead.
---
### [2026-06-09 13:36] Hermes Call
- **Task**: Test gemma-4-31b connectivity
- **Model**: google/gemma-4-31b
- **Status**: Error
- **Details**: HTTP 404: Gemini returned HTTP 404
---
### [2026-06-09 13:36] Hermes Call
- **Task**: Test gemini-3.1-flash-lite connectivity
- **Model**: google/gemini-3.1-flash-lite
- **Status**: Error
- **Details**: HTTP 404: Gemini returned HTTP 404
---
### [2026-06-09 13:37] Hermes Call
- **Task**: Test gemini-2.5-flash connectivity
- **Model**: google/gemini-2.5-flash
- **Status**: Error
- **Details**: HTTP 404: Gemini returned HTTP 404
---
### [2026-06-09 13:37] Hermes Call
- **Task**: Test gemini-3.5-flash connectivity
- **Model**: google/gemini-3.5-flash
- **Status**: Error
- **Details**: HTTP 404: Gemini returned HTTP 404
---
### [2026-06-09 13:38] Hermes Call
- **Task**: Test hermes with default model
- **Model**: Default
- **Status**: Success
- **Details**: Connectivity confirmed.
---
### [2026-06-09 13:39] Hermes Call
- **Task**: Test model connectivity without prefix
- **Model**: gemini-3.1-flash-lite, gemini-3.5-flash, gemini-2.5-flash
- **Status**: Success
- **Details**: Omiting 'google/' prefix resolved the 404 for Gemini models. gemma-4-31b still 404s.
---
