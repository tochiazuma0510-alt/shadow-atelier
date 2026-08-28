## drophunt_sweep_launch_v1.g -- item 8 (裁定1773): the REAL launch script
## body (no DryRunLimit -- processes the full frozen 358-window list, one
## chunk invocation at a time via checkpoint/resume). This file is a THIN
## wrapper: it does NOT set DSDDryRunLimit, so drophunt_sweep_driver_v3.g's
## own default (infinity) applies and DSDEndIndex is bounded only by the
## checkpoint resume point + the chunk time budget.
##
## 裁定1781 item3: Unbind DSDDryRunLimit/DSDCheckpointPath/DSDDropLockPath
## BEFORE Read()-ing the driver. Rationale: if this file is ever Read() in
## the SAME gap session as an earlier dry-run wrapper (e.g. scratchpad/
## drophunt_sweep_20window_dryrun_v1.g, which sets DSDDryRunLimit:=20 and
## its own scoped checkpoint/lock paths), GAP's global bindings would
## PERSIST across the two Read()s -- silently turning the "real" 358-window
## launch into a 20-window run using the wrong (scratchpad) checkpoint file,
## with NO error or warning. Unbind() is safe whether or not the variable
## was previously bound. After this, the driver's own IsBound guards fall
## through to its real defaults (DSDDryRunLimit=infinity, the real
## search/certs/ checkpoint/lock paths).
Unbind(DSDDryRunLimit);;
Unbind(DSDCheckpointPath);;
Unbind(DSDDropLockPath);;
Read("search/drophunt_sweep_driver_v3.g");;
