<!-- SCOPE: Knowledge about replay. Read when related tasks arise. -->
# Replay

### [2026-06-25 11:18] Tags: replay, log-processing, gps2
Created merge_logs_gps2_200hz.py to extract 200Hz ILB messages from high-frequency logs and merge them into low-frequency original logs, replacing GPS2 and synchronizing boot times based on the constant clock offset between boot time (TimeUS) and InertialLabs IMS time.
