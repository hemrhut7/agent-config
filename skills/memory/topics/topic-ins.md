<!-- SCOPE: Knowledge about INS. Read when related tasks arise. -->
# Ins

### [2026-05-15 16:53] Tags: INS, BatchOptimizer, Jacobian, Preintegration
Stabilized GlobalBatchOptimizer by fixing rotation Jacobians (R * [dp]_skew) and implementing recursive bias propagation. Resolved unit mismatch in analyzer output by converting ENU to LLH (rad) in results dict. Final convergence cost 22.9, horizontal error 0.06m.
