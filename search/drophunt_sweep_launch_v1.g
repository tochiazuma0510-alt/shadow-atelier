## drophunt_sweep_launch_v1.g -- item 8 (裁定1773): the REAL launch script
## body (no DryRunLimit -- processes the full frozen 358-window list, one
## chunk invocation at a time via checkpoint/resume). This file is a THIN
## wrapper: it does NOT set DSDDryRunLimit, so drophunt_sweep_driver_v3.g's
## own default (infinity) applies and DSDEndIndex is bounded only by the
## checkpoint resume point + the chunk time budget.
##
## NOTE (explicit, per coordinator instruction): this script is NOT to be
## invoked for the real 358-window campaign in this pass -- only used, via
## a companion 20-window-capped wrapper (drophunt_sweep_20window_dryrun_v1.g),
## for the item-8 dry run. The actual full launch happens only after
## falsifier 第5前哨 (or an explicit exemption) per 裁定1773's own closing
## instruction ("発射はその後(前哨免除の判断は私がする)").
Read("search/drophunt_sweep_driver_v3.g");;
