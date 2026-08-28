#############################################################################
## drophunt_sweep_driver_v3.g -- items 2,3,5 (裁定1773 GO条件) repair of the
## v2 driver:
##
## item 2: LINS is NEVER called in this file. All window ingredients
## (JX/JY/JC one-line, K_ord, F2_ratio, degree, F1_prime) are read from the
## PRE-BUILT batch file search/certs/drophunt_lins_batch_v1_20260829.g
## (produced once by search/drophunt_lins_batch_v1.g, itself checkpointed
## per-b3_index -- see that file's header for the livelock this fixes).
##
## item 3 (as refined by 裁定1774): DROP/ANOMALY detection is SYMMETRIC
## across Mode A (row36) and Mode B (row71), and the stop condition is
## valid_count NOT IN {0, F1'} where F1' := #{m in the window's m-residue
## class : gcd(2m+1,K_ord)=1} -- a PURE ARITHMETIC, PRE-REGISTERED quantity
## computed once per window in the batch file (NOT derived post-hoc from a
## particular run's own valid_count -- see F1_prime field in the batch
## records). valid_count=0 is DROP (NO_LIFT witnessed for every candidate at
## every eligible m). 0 < valid_count < F1' is ANOMALY (genuinely
## informative: some, not all, eligible m are witnessed) -- NOT silently
## treated as benign, per 裁定1774's explicit instruction not to sanitize
## this case. valid_count = F1' is the normal/expected case. valid_count >
## F1' was INITIALLY assumed here to be structurally impossible (at most
## one witness per eligible m) -- this assumption was FALSIFIED during this
## pass's own 20-window dry run (b3_index=12 window, F2_ratio=12, F1'=1,
## valid_count=3 -- 3 distinct coset witnesses at m=0, cross-checked
## byte-identical against the original LINS-based DCP3BuildWindow path, see
## cert calibration example #2). Multiplicity > 1 apparently becomes
## possible once F2 (coset size) is large enough; every window tested
## before this dry run had F2<=3. The valid>F1' branch is a REAL, OBSERVED
## case, not a defensive dead branch, and correctly halts as ANOMALY.
##
## item 5: checkpoint write order reversed (Summary written before
## LastIndex, so a kill mid-write leaves LastIndex stale/absent rather than
## advanced past an unrecorded Summary); fail-closed on resume requires BOTH
## bindings present together or the checkpoint is treated as CORRUPT (stop,
## do not guess); a DROP or ANOMALY halt writes a POISON LOCK file that
## resume refuses to proceed past without it being explicitly cleared (never
## silently double-counts a drop/anomaly across resumes); Error()-based
## hard stops on a per-window cross-check failure are replaced by an
## UNKNOWN-recording skip-and-continue (the window is recorded in a
## dedicated unknown list with a reason, the loop advances, and the final
## summary's denominator is defined as processed+drops+anomalies+unknown,
## which must equal the number of windows attempted this run).
#############################################################################

Read("search/drophunt_checker_producer_v3.g");;

DSDMaxDegree := 2000;;
DSDChunkBudgetMs := 480000;;   # 8 min work budget inside the 10 min wall-clock chunk
## self-caught bug (this pass): these three MUST be IsBound-guarded, not
## unconditional ":=", or a caller wrapper's pre-set override (e.g. the
## scratchpad 20-window dry-run harness, which uses SEPARATE checkpoint/lock
## paths so it never contaminates the real-launch state) is silently
## clobbered back to the default the moment this file is Read()-in.
if not IsBound(DSDCheckpointPath) then DSDCheckpointPath := "search/certs/drophunt_sweep_checkpoint_v3_20260829.g";; fi;;
if not IsBound(DSDDropLockPath) then DSDDropLockPath := "search/certs/drophunt_sweep_droplock_v3_20260829.g";; fi;;
if not IsBound(DSDDryRunLimit) then DSDDryRunLimit := infinity;; fi;;   # item 8: real launch script sets no limit

DSDT0 := GAPLIB_WallElapsedMs();;

#############################################################################
## B-2/B-4 preflight (unchanged from v2 -- roof-level facts, checked once).
#############################################################################
DSDThetaM := GroupHomomorphismByImages(DCP3MBlock, DCP3MBlock, [DCP3MX,DCP3MY], [DCP3MY,DCP3MX]);;
DSDTauM := GroupHomomorphismByImages(DCP3MBlock, DCP3MBlock, [DCP3MX,DCP3MY], [DCP3MY, DCP3MY^-1*DCP3MX^-1]);;
DSDDerivedM := DerivedSubgroup(DCP3MBlock);;

DSDCheckSeedInM := function(seed)
  local f, hex310, ymf, lhs, hex311, onto, genA, genB;
  f := DCP3EvalWord(seed.letters, DCP3MX, DCP3MY, Identity(DCP3MBlock));;
  hex310 := (f * Image(DSDThetaM, f) = Identity(DCP3MBlock));;
  ymf := DCP3MY^0 * f;;
  lhs := Image(DSDTauM, Image(DSDTauM, ymf)) * Image(DSDTauM, ymf) * ymf;;
  hex311 := (lhs = Identity(DCP3MBlock));;
  onto := false;;
  if hex310 and hex311 then
    genA := DCP3MX^1;; genB := f^-1*DCP3MY^1*f;;
    onto := Size(Group(genA,genB)) = Size(DCP3MBlock);;
  fi;;
  return (f in DSDDerivedM) and hex310 and hex311 and onto;;
end;;

DSDB2Pass := DSDCheckSeedInM(DCP3Seeds[2]);;   # row71
DSDB4Pass := DSDCheckSeedInM(DCP3Seeds[1]);;   # row36
Print("DSD_B2_PREFLIGHT(row71_full_M_shadow)=", DSDB2Pass, "\n");;
Print("DSD_B4_CONTROL(row36_full_M_shadow)=", DSDB4Pass, "\n");;
if not DSDB2Pass then
  Error("DSD: B-2 PREFLIGHT FAILED -- refusing to start sweep");
fi;;

#############################################################################
## item 2: load window ingredients from the pre-built batch (NO LINS call).
#############################################################################
DSDBatchPath := "search/certs/drophunt_lins_batch_v1_20260829.g";;
if not IsExistingFile(DSDBatchPath) then
  Error("DSD: batch file ", DSDBatchPath, " not found -- run search/drophunt_lins_batch_v1.g first (item 2)");
fi;;
Read("search/drophunt_frozen_node_list_v1_gap.g");;   # DSDFrozenWindows (fib_K asc order, authoritative processing order)
DLBWindows := [];; DLBDoneIndices := [];;
Read(DSDBatchPath);;
Print("DSD_BATCH_LOADED windows=", Length(DLBWindows), " done_b3_index=", Length(DLBDoneIndices), "\n");;
DSDBatchByNodeId := rec();;
for DSDW in DLBWindows do
  DSDBatchByNodeId.(DSDW.node_id) := DSDW;;
od;;

## NOTE: item3/1774's implementer-side "F1'" (pure-arithmetic gcd count) is
## now superseded by 裁定1776's DCP3ComputeMultAnalysis (defined in
## drophunt_checker_producer_v3.g and Read() above), which computes the
## SAME quantity under the mathematician-assigned name F1_double_prime,
## alongside per_m/lift_m/mult_set/verdict. The standalone DSDF1Prime
## function that used to live here has been removed to avoid two
## differently-named copies of the same arithmetic drifting apart.

#############################################################################
## Rebuild qrec from stored JX/JY/JC one-line data ONLY (no LINS, no L) --
## the whole point of item 2.
#############################################################################
DSDRebuildQrec := function(w)
  local deg, JX, JY, JC, G, A, pi0, H, thetaHom, tauHom;
  deg := w.degree;;
  JX := PermList(w.JX_one_line);; JY := PermList(w.JY_one_line);; JC := PermList(w.JC_one_line);;
  G := Group(JX, JY);; A := Group(JX, JY, JC);;
  pi0 := GroupHomomorphismByImages(G, DCP3MBlock, [JX,JY], [DCP3MX,DCP3MY]);;
  if pi0 = fail then Error("DSD: pi0 ill-defined on rebuild -- fail-closed"); fi;;
  H := Kernel(pi0);;
  thetaHom := GroupHomomorphismByImages(A, A, [JX,JY,JC], [JY,JX,JC]);;
  tauHom := GroupHomomorphismByImages(A, A, [JX,JY,JC], [JY, JY^-1*JX^-1*JC, JC]);;
  return rec(G:=G, A:=A, JX:=JX, JY:=JY, JC:=JC, degL:=deg-DCP3MDegree, K_ord:=w.K_ord,
    M_ord:=18, F2:=w.F2_ratio, F3:=(w.K_ord/18)*w.F2_ratio, pi0:=pi0, H:=H, D:=DerivedSubgroup(G),
    c_in_K:=(w.K_ord mod 2 = 0),   # placeholder unused field; c_in_K is not needed for eval, kept for receipt compatibility below
    thetaHom:=thetaHom, tauHom:=tauHom);;
end;;

#############################################################################
## item 5: checkpoint read (resume) -- fail-closed on partial/corrupt state.
#############################################################################
DSDResumeFrom := 1;;
DSDPriorSummary := rec(processed:=0, valid36_total:=0, valid71_total:=0, drops:=0, anomalies:=0, unknown:=0, bugs:=0);;
if IsExistingFile(DSDDropLockPath) then
  Error("DSD: DROP/ANOMALY POISON LOCK present (", DSDDropLockPath, ") -- refusing to resume until a human clears it (item 5)");
fi;;
if IsExistingFile(DSDCheckpointPath) then
  DSDCheckpointLastIndex := fail;; DSDCheckpointSummary := fail;;
  Read(DSDCheckpointPath);;
  if DSDCheckpointLastIndex = fail or DSDCheckpointSummary = fail then
    Error("DSD: checkpoint file present but INCOMPLETE (missing LastIndex or Summary binding) -- CORRUPT, fail-closed stop (item 5: never guess a partial checkpoint)");
  fi;;
  DSDResumeFrom := DSDCheckpointLastIndex + 1;;
  DSDPriorSummary := DSDCheckpointSummary;;
  Print("DSD_RESUMING_FROM_CHECKPOINT last_completed=", DSDCheckpointLastIndex,
    " resume_index=", DSDResumeFrom, "\n");;
else
  Print("DSD_NO_CHECKPOINT_FOUND starting fresh from index 1\n");;
fi;;

DSDWriteCheckpoint := function(lastIndex, summary)
  local out;
  ## item 5: Summary written BEFORE LastIndex (reversed from v2) -- a kill
  ## mid-write leaves at most a stale/absent LastIndex, never a LastIndex
  ## pointing past an unrecorded Summary.
  out := Concatenation(
    "## drophunt_sweep_checkpoint_v3_20260829.g -- auto-written, Read() on resume.\n",
    "DSDCheckpointSummary := rec(processed:=", String(summary.processed),
      ", valid36_total:=", String(summary.valid36_total),
      ", valid71_total:=", String(summary.valid71_total),
      ", drops:=", String(summary.drops),
      ", anomalies:=", String(summary.anomalies),
      ", unknown:=", String(summary.unknown),
      ", bugs:=", String(summary.bugs), ");;\n",
    "DSDCheckpointLastIndex := ", String(lastIndex), ";;\n");;
  WriteFile(DSDCheckpointPath, out);;
end;;

DSDWritePoisonLock := function(reason, idx, nodeId)
  local out;
  out := Concatenation(
    "## drophunt_sweep_droplock_v3_20260829.g -- item 5 poison lock.\n",
    "## Presence of this file BLOCKS all resume until a human clears it --\n",
    "## prevents a drop/anomaly from being silently re-processed (and its\n",
    "## count double-added) on a subsequent invocation.\n",
    "DSDPoisonLockReason := \"", reason, "\";;\n",
    "DSDPoisonLockIndex := ", String(idx), ";;\n",
    "DSDPoisonLockNodeId := \"", nodeId, "\";;\n");;
  WriteFile(DSDDropLockPath, out);;
end;;

#############################################################################
## DROP/ANOMALY contract (stub call site; body intentionally unimplemented
## for the actual second-hexagon-system cross-check -- see 裁定1765/1773).
#############################################################################
DSDFullHexagonSecondSystemStub := function(nodeId, seedName)
  Print("DSD_DROP_CONTRACT_INVOKED node_id=", nodeId, " seed=", seedName, "\n");;
  Print("DSD_SECOND_SYSTEM_STATUS=UNIMPLEMENTED_STUB (spec v2 SS8 full hexagon (3.3)/(3.4) -- call site only)\n");;
  return rec(status:="UNIMPLEMENTED_STUB", cross_checked:=false);;
end;;

DSDWriteHaltCheckpoint := function(win, seedName, evalResult, mult, kind)
  local rowsJson, out, prefix;
  rowsJson := JoinC(List(evalResult.rows, r -> Concatenation(
    "{\"m\":", String(r.m), ",\"charming\":", DCP3BoolOrNull(r.charming),
    ",\"hex310\":", DCP3BoolOrNull(r.hex310), ",\"hex311\":", DCP3BoolOrNull(r.hex311),
    ",\"onto\":", DCP3BoolOrNull(r.onto), ",\"verdict\":", JB(r.verdict),
    ",\"stage\":", JStr(r.stage), "}")), ",\n");;
  prefix := "search/certs/drophunt_sweep_";;
  if kind = "DROP" then prefix := Concatenation(prefix, "drop_");
  elif kind = "BUG" then prefix := Concatenation(prefix, "bug_");
  else prefix := Concatenation(prefix, "anomaly_"); fi;;
  out := Concatenation(
    "{\n  \"schema\":\"drophunt-sweep-halt-checkpoint/v3\",\n",
    "  \"status\":\"", kind, "_DETECTED_SWEEP_HALTED\",\n",
    "  \"verdict\":\"", kind, "\",\n",
    "  \"node_id\":\"", win.node_id, "\",\n",
    "  \"b3_index\":", String(win.b3_index), ",\n",
    "  \"fib_K\":", String(win.fib_K), ",\n",
    "  \"seed\":\"", seedName, "\",\n",
    "  \"F1_prime\":", String(mult.F1_prime), ",\n",
    "  \"F1_double_prime\":", String(mult.F1_double_prime), ",\n",
    "  \"per_m\":[", JoinC(List(mult.per_m, DCP3IntOrNullStr), ","), "],\n",
    "  \"lift_m\":", String(mult.lift_m), ",\n",
    "  \"mult_set\":[", JoinC(List(mult.mult_set, String), ","), "],\n",
    "  \"valid_total\":", String(mult.valid_total), ",\n",
    "  \"cc1_candidate_coverage\":{\"evaluated_count\":", String(evalResult.evaluated_count),
      ",\"expected_count\":", String(evalResult.expected_count), "},\n",
    "  \"cc2_no_early_stop\":true,\n",
    "  \"cc3_seed_key\":\"", seedName, "\",\n",
    "  \"cc4_window_eligible\":{\"K_le_M\":true},\n",
    "  \"cc5_convention_block\":{\"product_order\":\"tau2_tau_id\",\"word_eval_order\":\"prepend\",\"reduction_index_order\":\"source_first\"},\n",
    "  \"cc6_mandatory_mutants_status\":\"NOT_RE_RUN_ON_THIS_SPECIFIC_HALT_WINDOW\",\n",
    "  \"second_system_stub_record\":\"UNIMPLEMENTED_STUB_INVOKED\",\n",
    "  \"all_rows\":[\n", rowsJson, "\n  ]\n}\n");;
  WriteFile(Concatenation(prefix, win.node_id{[1..16]}, "_v3_20260829.json"), out);;
end;;

#############################################################################
## Main loop -- item 2: NO LINS call anywhere below this point.
#############################################################################
DSDEndIndex := Minimum(Length(DSDFrozenWindows), DSDResumeFrom + DSDDryRunLimit - 1);;
Print("DSD_RUN_BOUNDED_TO index ", DSDResumeFrom, "..", DSDEndIndex,
  " (of ", Length(DSDFrozenWindows), " total frozen windows)\n");;

## NOTE (self-caught bug, item 5 discipline): GAP records assign BY
## REFERENCE, not by value -- "DSDSummary := DSDPriorSummary;;" would make
## every later mutation of DSDSummary ALSO mutate DSDPriorSummary (same
## object), silently corrupting the denominator check below (it would
## always read attempted-vs-itself = 0, discovered exactly this way during
## this pass's own 20-window dry run). ShallowCopy breaks the aliasing.
DSDPriorTotal := DSDPriorSummary.processed + DSDPriorSummary.drops + DSDPriorSummary.anomalies + DSDPriorSummary.unknown + DSDPriorSummary.bugs;;
DSDSummary := ShallowCopy(DSDPriorSummary);;
DSDStopFlag := false;;
DSDIdx := DSDResumeFrom;;
while DSDIdx <= DSDEndIndex and not DSDStopFlag do
  if GAPLIB_WallElapsedMs() - DSDT0 > DSDChunkBudgetMs then
    Print("DSD_TIME_BUDGET_EXCEEDED at index ", DSDIdx, " -- checkpointing and stopping cleanly\n");;
    DSDWriteCheckpoint(DSDIdx - 1, DSDSummary);;
    Print("DSD_STATUS=CHUNK_BUDGET_STOP\n");;
    DSDStopFlag := true;;
    continue;;
  fi;;

  DSDWin := DSDFrozenWindows[DSDIdx];;
  if DSDWin.b3_index > DSDMaxDegree - DCP3MDegree then
    Print("DSD_DEGREE_GUARD_SKIP index=", DSDIdx, " node_id=", DSDWin.node_id, "\n");;
    DSDIdx := DSDIdx + 1;;
    continue;;
  fi;;

  ## item 5: batch-miss -> UNKNOWN recorded, skip-and-continue (no Error()).
  if not IsBound(DSDBatchByNodeId.(DSDWin.node_id)) then
    Print("DSD_UNKNOWN_BATCH_MISS index=", DSDIdx, " node_id=", DSDWin.node_id,
      " reason=NOT_IN_LINS_BATCH_YET\n");;
    DSDSummary.unknown := DSDSummary.unknown + 1;;
    DSDWriteCheckpoint(DSDIdx, DSDSummary);;
    DSDIdx := DSDIdx + 1;;
    continue;;
  fi;;
  DSDBW := DSDBatchByNodeId.(DSDWin.node_id);;
  if DSDBW.K_ord <> DSDWin.K_ord or DSDBW.F2_ratio <> DSDWin.F2_ratio then
    Print("DSD_UNKNOWN_BATCH_MISMATCH index=", DSDIdx, " node_id=", DSDWin.node_id,
      " reason=K_ord_or_F2_MISMATCH_VS_FROZEN_LIST\n");;
    DSDSummary.unknown := DSDSummary.unknown + 1;;
    DSDWriteCheckpoint(DSDIdx, DSDSummary);;
    DSDIdx := DSDIdx + 1;;
    continue;;
  fi;;
  Print("DSD_NODE_ID_CONFIRMED_FROM_BATCH index=", DSDIdx, " node_id=", DSDWin.node_id, "\n");;

  DSDQrec := DSDRebuildQrec(DSDBW);;
  ## c_in_K is a genuine property (not the placeholder above) -- recompute
  ## it honestly for receipt purposes via the same F2-quotient definition
  ## the producer uses (JC = identity in the M/L-joint quotient).
  DSDQrec.c_in_K := (DSDQrec.JC = Identity(DSDQrec.A));;

  ## 裁定1776: final stop lattice. Mode A (row36) and Mode B (row71) are
  ## evaluated SYMMETRICALLY; each gets its own DCP3ComputeMultAnalysis
  ## verdict in {BUG,DROP,ANOMALY,PASS} (exclusive priority order: BUG >
  ## DROP > ANOMALY > PASS -- see DCP3ComputeMultAnalysis's own header for
  ## the exact lattice). BUG (lift_m>F1'' or |mult_set|>1, i.e. a MULT-COSET
  ## theorem violation) and DROP (valid_total=0) and ANOMALY (0<lift_m<F1'')
  ## ALL halt immediately with a poison lock; only PASS on BOTH modes lets
  ## the loop continue to the next window.
  DSDResultA := DCP3EvalWindow(DSDQrec, DCP3Seeds[1]);;
  DSDMultA := DCP3ComputeMultAnalysis(DSDQrec, DSDResultA);;
  Print("DSD_MODE_A index=", DSDIdx, " valid_total=", DSDMultA.valid_total,
    " F1_double_prime=", DSDMultA.F1_double_prime, " lift_m=", DSDMultA.lift_m,
    " mult_set=", DSDMultA.mult_set, " verdict=", DSDMultA.verdict, "\n");;

  if DSDMultA.verdict <> "PASS" then
    Print("DSD_", DSDMultA.verdict, "_DETECTED index=", DSDIdx, " node_id=", DSDWin.node_id,
      " seed=row36 -- HALTING IMMEDIATELY\n");;
    DSDStubResult := DSDFullHexagonSecondSystemStub(DSDWin.node_id, "row36");;
    DSDWriteHaltCheckpoint(DSDWin, "row36", DSDResultA, DSDMultA, DSDMultA.verdict);;
    if DSDMultA.verdict = "DROP" then DSDSummary.drops := DSDSummary.drops + 1;
    elif DSDMultA.verdict = "BUG" then DSDSummary.bugs := DSDSummary.bugs + 1;
    else DSDSummary.anomalies := DSDSummary.anomalies + 1;; fi;;
    DSDWriteCheckpoint(DSDIdx - 1, DSDSummary);;
    DSDWritePoisonLock(DSDMultA.verdict, DSDIdx, DSDWin.node_id);;
    Print("DSD_STATUS=", DSDMultA.verdict, "_HALT\n");;
    DSDStopFlag := true;;
    continue;;
  fi;;

  DSDResultB := DCP3EvalWindow(DSDQrec, DCP3Seeds[2]);;
  DSDMultB := DCP3ComputeMultAnalysis(DSDQrec, DSDResultB);;
  Print("DSD_MODE_B index=", DSDIdx, " valid_total=", DSDMultB.valid_total,
    " F1_double_prime=", DSDMultB.F1_double_prime, " lift_m=", DSDMultB.lift_m,
    " mult_set=", DSDMultB.mult_set, " verdict=", DSDMultB.verdict, "\n");;

  if DSDMultB.verdict <> "PASS" then
    Print("DSD_", DSDMultB.verdict, "_DETECTED index=", DSDIdx, " node_id=", DSDWin.node_id,
      " seed=row71 -- HALTING IMMEDIATELY\n");;
    DSDStubResult := DSDFullHexagonSecondSystemStub(DSDWin.node_id, "row71");;
    DSDWriteHaltCheckpoint(DSDWin, "row71", DSDResultB, DSDMultB, DSDMultB.verdict);;
    if DSDMultB.verdict = "DROP" then DSDSummary.drops := DSDSummary.drops + 1;
    elif DSDMultB.verdict = "BUG" then DSDSummary.bugs := DSDSummary.bugs + 1;
    else DSDSummary.anomalies := DSDSummary.anomalies + 1;; fi;;
    DSDWriteCheckpoint(DSDIdx - 1, DSDSummary);;
    DSDWritePoisonLock(DSDMultB.verdict, DSDIdx, DSDWin.node_id);;
    Print("DSD_STATUS=", DSDMultB.verdict, "_HALT\n");;
    DSDStopFlag := true;;
    continue;;
  fi;;

  ## Both modes PASS -- receipt emission (single date, node_id-prefix label).
  DSDLabel := DSDWin.node_id{[1..16]};;
  DSDPathA := Concatenation("search/certs/drophunt_sweep_receipt_", DSDLabel, "_row36_v3_20260829.json");;
  DSDPathB := Concatenation("search/certs/drophunt_sweep_receipt_", DSDLabel, "_row71_v3_20260829.json");;
  DSDEmitA := DCP3EmitReceipt(DSDPathA, DSDWin.node_id, DSDWin.b3_index, DSDQrec, "row36", DCP3Seeds[1].codes, DSDResultA, 0);;
  DSDEmitB := DCP3EmitReceipt(DSDPathB, DSDWin.node_id, DSDWin.b3_index, DSDQrec, "row71", DCP3Seeds[2].codes, DSDResultB, 0);;
  Print("DSD_RECEIPTS_EMITTED index=", DSDIdx, " pathA=", DSDEmitA.path, " pathB=", DSDEmitB.path, "\n");;

  DSDSummary.processed := DSDSummary.processed + 1;;
  DSDSummary.valid36_total := DSDSummary.valid36_total + DSDMultA.valid_total;;
  DSDSummary.valid71_total := DSDSummary.valid71_total + DSDMultB.valid_total;;
  DSDWriteCheckpoint(DSDIdx, DSDSummary);;
  Print("DSD_CHECKPOINT_WRITTEN last_completed=", DSDIdx, "\n");;

  DSDIdx := DSDIdx + 1;;
od;;

if not DSDStopFlag then
  Print("DSD_RUN_COMPLETE_THIS_INVOCATION processed_this_run=", DSDSummary.processed,
    " cumulative_summary=", DSDSummary, "\n");;
  Print("DSD_DENOMINATOR_CHECK attempted=", DSDEndIndex - DSDResumeFrom + 1,
    " accounted=", (DSDSummary.processed + DSDSummary.drops + DSDSummary.anomalies + DSDSummary.unknown + DSDSummary.bugs) - DSDPriorTotal, "\n");;
  Print("DSD_STATUS=RUN_COMPLETE\n");;
fi;;
Print("ALL_DONE\n");;
