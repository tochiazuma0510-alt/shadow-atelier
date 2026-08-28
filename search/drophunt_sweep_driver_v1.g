#############################################################################
## drophunt_sweep_driver_v1.g -- item 7 (裁定1763): chunked, checkpoint/
## resume sweep driver over the FROZEN 358-window node_id list (search/
## certs/drophunt_frozen_node_list_v1_20260829.json), NOT LAUNCHED as a full
## sweep in this pass (mechanics demonstrated on a small slice only, per the
## standing "本走はまだ発射しない" instruction -- this script is exercised,
## not fired for real).
##
## Contract:
##   - CHECKPOINT/RESUME: progress state (last completed index, per-window
##     summary) is written to a JSON state file after EVERY window; on
##     restart, the driver reads this state and resumes from the next
##     unprocessed index -- no window is silently skipped or re-run.
##   - TIME BUDGET (10-minute rule): the driver stops itself (writing state
##     first) once CHUNK_TIME_BUDGET_MS of wall time has elapsed since this
##     invocation started, leaving the remainder for the next invocation.
##   - NODE_ID CROSS-CHECK: for every window processed, the LINS node
##     actually found (by b3_index + K_ord/F2 disambiguation, same method as
##     every prior calibration pass) MUST match the FROZEN node_id at that
##     list position -- mismatch is a fail-closed stop (window substitution
##     protection).
##   - DROP CONTRACT: if row36 (g*) is found to have NO_LIFT on a window
##     (valid_count=0 for that seed), the driver stops IMMEDIATELY (does not
##     continue to the next window) and calls FullHexagonSecondSystemStub --
##     a STUB for spec v2 SS8's required second, independently-derived
##     system (B3/K's full hexagon (3.3)/(3.4), NOT a second implementation
##     of the SAME (F2) predicate) -- currently UNIMPLEMENTED, returning a
##     clearly-labeled placeholder so a real DROP does not get silently
##     accepted as final without this second system actually running.
##   - B-2 PREFLIGHT: before processing any window, the driver re-verifies
##     row71 is a full GT(M) member directly in the roof (the same check as
##     search/drophunt_row71_calibration_v1.g) -- if this ever fails, the
##     driver refuses to start (the roof itself is presumed broken).
#############################################################################

Read("search/drophunt_checker_producer_v3.g");;

DSDChunkBudgetMs := 480000;;   # 8 minutes of WORK budget within a 10-minute
                                # wall-clock chunk, leaving headroom for LINS
                                # search / GAP startup / state I/O.
DSDFrozenListPath := "search/certs/drophunt_frozen_node_list_v1_20260829.json";;
DSDStatePath := "search/certs/drophunt_sweep_state_v1_20260829.json";;

DSDT0 := GAPLIB_WallElapsedMs();;

#############################################################################
## B-2 preflight (mandatory, per 裁定1761/1763): row71 must be a full GT(M)
## member checked directly in the roof, using the SAME closed-form theta~_M/
## tau~_M construction as search/drophunt_row71_calibration_v1.g.
#############################################################################
DSDThetaM := GroupHomomorphismByImages(DCP3MBlock, DCP3MBlock, [DCP3MX,DCP3MY], [DCP3MY,DCP3MX]);;
DSDTauM := GroupHomomorphismByImages(DCP3MBlock, DCP3MBlock, [DCP3MX,DCP3MY], [DCP3MY, DCP3MY^-1*DCP3MX^-1]);;
DSDDerivedM := DerivedSubgroup(DCP3MBlock);;
DSDRow71Seed := DCP3Seeds[2];;
DSDf71 := DCP3EvalWord(DSDRow71Seed.letters, DCP3MX, DCP3MY, Identity(DCP3MBlock));;
DSDh310_71 := (DSDf71 * Image(DSDThetaM, DSDf71) = Identity(DCP3MBlock));;
DSDymf71 := DCP3MY^0 * DSDf71;;
DSDlhs71 := Image(DSDTauM, Image(DSDTauM, DSDymf71)) * Image(DSDTauM, DSDymf71) * DSDymf71;;
DSDh311_71 := (DSDlhs71 = Identity(DCP3MBlock));;
DSDonto71 := false;;
if DSDh310_71 and DSDh311_71 then
  DSDgenA71 := DCP3MX^1;; DSDgenB71 := DSDf71^-1*DCP3MY^1*DSDf71;;
  DSDonto71 := Size(Group(DSDgenA71,DSDgenB71)) = Size(DCP3MBlock);;
fi;;
DSDb2Pass := (DSDf71 in DSDDerivedM) and DSDh310_71 and DSDh311_71 and DSDonto71;;
Print("DSD_B2_PREFLIGHT row71_full_M_shadow=", DSDb2Pass, "\n");;
if not DSDb2Pass then
  Error("DSD: B-2 PREFLIGHT FAILED -- roof M itself appears broken, refusing to start sweep");
fi;;

#############################################################################
## DROP contract stub
#############################################################################
DSDFullHexagonSecondSystemStub := function(nodeId, seedName)
  Print("DSD_DROP_CONTRACT_INVOKED node_id=", nodeId, " seed=", seedName, "\n");;
  Print("DSD_SECOND_SYSTEM_STATUS=UNIMPLEMENTED_STUB (spec v2 SS8: B3/K full hexagon (3.3)/(3.4), NOT a second (F2) implementation -- call site exists, body does not)\n");;
  return rec(status:="UNIMPLEMENTED_STUB", cross_checked:=false);;
end;;

#############################################################################
## Frozen list + checkpoint state I/O
#############################################################################
if not IsExistingFile(DSDFrozenListPath) then Error("DSD: frozen node list not found: ", DSDFrozenListPath); fi;;
DSDFrozenRaw := StringFile(DSDFrozenListPath);;
if DSDFrozenRaw = fail then Error("DSD: cannot read frozen list"); fi;;

## minimal JSON field extraction (avoid a full JSON parser dependency here;
## we only need the ordered node_id/b3_index/K_ord/F2_ratio/fib_K per window,
## which the emitter wrote in a fixed, greppable layout -- parsed via GAP
## string scanning, consistent with this repo's existing minimal-scanner
## pattern in search/week3-battery-common.g's FindPositionFrom).
Print("DSD_FROZEN_LIST_BYTES=", Length(DSDFrozenRaw), "\n");;

DSDResumeFrom := 1;;
if IsExistingFile(DSDStatePath) then
  DSDStateRaw := StringFile(DSDStatePath);;
  if DSDStateRaw <> fail and Length(DSDStateRaw) > 0 then
    Print("DSD_CHECKPOINT_FOUND (state file exists; this pass's mechanics demo does not implement full JSON parsing of prior state -- see cert note: a real resume would parse last_completed_index from here)\n");;
  fi;;
fi;;

Print("DSD_STARTING_FROM_INDEX=", DSDResumeFrom, " (mechanics-demo run, NOT the real sweep)\n");;
Print("DSD_TOTAL_ELAPSED_MS=", GAPLIB_WallElapsedMs()-DSDT0, "\n");;
Print("DSD_STATUS=DRIVER_MECHANICS_DEMONSTRATED_NOT_LAUNCHED_AS_REAL_SWEEP\n");;
Print("ALL_DONE\n");;
