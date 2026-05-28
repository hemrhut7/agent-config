<!-- SCOPE: Knowledge about InertialLabs INS-U driver. -->
# InertialLabs

### [2026-05-26] INS-U Driver Fixes
- **Status Mapping**: Corrected unsafe mapping of `solution status 2` (no GNSS) to `FIX_2D`.
- **Scaling**: Applied `* 100.0f` scaling to `track_over_ground_raw` (float yaw degrees).
- **Lock Detection**: Added `GNSS_POS_VALID` fallback for custom packets lacking `FULL_SAT_INFO`.
