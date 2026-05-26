<!-- SCOPE: Knowledge about inertiallabs. Read when related tasks arise. -->
# Inertiallabs

### [2026-05-26 09:57] Tags: inertiallabs, ins-u, driver
InertialLabs INS-U driver maps solution status 2 (no GNSS) to FIX_2D, which is unsafe. Also track_over_ground_raw needs scaling * 100.0f from float yaw degrees. SolnSVs > 3 check fails if FULL_SAT_INFO is missing from custom packet configurations, so fallback to GNSS_POS_VALID is needed.
