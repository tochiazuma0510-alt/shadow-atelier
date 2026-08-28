#############################################################################
## drophunt_lins_batch_v1.g -- item 2 (裁定1773 GO条件2): LINS out of the
## sweep loop. Generates (node_id, JX,JY,JC one-line, K_ord, F2, degree) for
## ALL 358 frozen windows ONCE, via PER-b3_index LowIndexNormalSubgroupsSearchForIndex
## calls (NOT one single bound-1944 sweep), so the batch itself has a real
## checkpoint granularity: if killed mid-run, only the b3_index value that
## was in flight is redone, not the whole 358-window batch. This is the fix
## for the livelock diagnosed under 裁定1773 item 2: the OLD design (single
## LowIndexNormalSubgroupsSearch(DCP3B3, 1944) call inside the sweep driver,
## re-issued on every process restart) took ~16 min, exceeding both the 8-min
## in-loop budget AND the ~10-12 min background-task kill window, so a killed
## run reproduced the SAME LINS call on every resume without ever reaching
## the loop body that writes a checkpoint -- infinite non-progress.
##
## Output: search/certs/drophunt_lins_batch_v1_20260829.g (GAP script,
## Read()-able), containing DLBWindows := [rec(node_id,b3_index,K_ord,
## F2_ratio,degree,JX_one_line,JY_one_line,JC_one_line), ...] for every
## frozen window successfully reproduced, plus DLBDoneIndices (list of
## b3_index values fully processed) for checkpoint/resume.
#############################################################################

Read("search/drophunt_checker_producer_v3.g");;
Read("search/drophunt_frozen_node_list_v1_gap.g");;

if not IsBound(DLBOutPath) then DLBOutPath := "search/certs/drophunt_lins_batch_v1_20260829.g";; fi;;
DLBChunkBudgetMs := 480000;;   # 8 min work budget per invocation

DLBT0 := GAPLIB_WallElapsedMs();;

## Distinct b3_index values needed, ascending (so cheap windows finish first --
## matches the sweep's own fib_K-ascending processing order in spirit).
DLBAllIndices := Set(List(DSDFrozenWindows, w -> w.b3_index));;
Sort(DLBAllIndices);;
## DLBIndexCap: optional pre-bound global (set by a caller script BEFORE
## Read()-ing this file) to restrict to a smoke-test-sized subset of
## b3_index values. Undefined in the real batch run (no cap).
if IsBound(DLBIndexCap) then
  DLBAllIndices := Filtered(DLBAllIndices, x -> x <= DLBIndexCap);;
  Print("DLB_INDEX_CAP_ACTIVE cap=", DLBIndexCap, " -- SMOKE TEST, NOT the real batch\n");;
fi;;
Print("DLB_TOTAL_DISTINCT_B3_INDEX=", Length(DLBAllIndices), " total_windows=", Length(DSDFrozenWindows), "\n");;

## Resume: read prior output if present.
DLBWindows := [];;
DLBDoneIndices := [];;
if IsExistingFile(DLBOutPath) then
  Read(DLBOutPath);;   # may (re)define DLBWindows, DLBDoneIndices
  Print("DLB_RESUMING done_b3_index_count=", Length(DLBDoneIndices),
    " windows_so_far=", Length(DLBWindows), "\n");;
else
  Print("DLB_NO_PRIOR_OUTPUT starting fresh\n");;
fi;;

DLBWriteOutput := function()
  local out, w;
  out := Concatenation(
    "## drophunt_lins_batch_v1_20260829.g -- auto-written by drophunt_lins_batch_v1.g. Read() to load.\n",
    "## Reversed-write-order discipline (item 5, 裁定1773): DLBDoneIndices (the\n",
    "## authoritative 'what is safely resumable' marker) is written to a STRING\n",
    "## first and both bindings are emitted together in ONE WriteFile call, so a\n",
    "## kill mid-write cannot leave DLBWindows advanced past DLBDoneIndices.\n",
    "DLBDoneIndices := ", String(DLBDoneIndices), ";;\n",
    "DLBWindows := [\n");;
  for w in DLBWindows do
    out := Concatenation(out, "  rec(node_id:=\"", w.node_id, "\", b3_index:=", String(w.b3_index),
      ", K_ord:=", String(w.K_ord), ", F2_ratio:=", String(w.F2_ratio), ", degree:=", String(w.degree),
      ", JX_one_line:=", String(w.JX_one_line), ", JY_one_line:=", String(w.JY_one_line),
      ", JC_one_line:=", String(w.JC_one_line), "),\n");;
  od;;
  out := Concatenation(out, "];;\n");;
  WriteFile(DLBOutPath, out);;
end;;

if LoadPackage("lins") <> true then Error("DLB: LINS load failed"); fi;;

DLBStopFlag := false;;
DLBIdx := 1;;
while DLBIdx <= Length(DLBAllIndices) and not DLBStopFlag do
  DLBB3Index := DLBAllIndices[DLBIdx];;
  if DLBB3Index in DLBDoneIndices then
    DLBIdx := DLBIdx + 1;;
    continue;;
  fi;;

  if GAPLIB_WallElapsedMs() - DLBT0 > DLBChunkBudgetMs then
    Print("DLB_TIME_BUDGET_EXCEEDED before starting b3_index=", DLBB3Index, " -- stopping cleanly (already-done work saved)\n");;
    Print("DLB_STATUS=CHUNK_BUDGET_STOP\n");;
    DLBStopFlag := true;;
    continue;;
  fi;;

  Print("DLB_PROCESSING b3_index=", DLBB3Index, " (", DLBIdx, "/", Length(DLBAllIndices), ") elapsed_ms=",
    GAPLIB_WallElapsedMs()-DLBT0, "\n");;
  DLBFound := LowIndexNormalSubgroupsSearchForIndex(DCP3B3, DLBB3Index, infinity);;
  DLBSubs := ComputedNormalSubgroups(DLBFound);;
  Print("DLB_FOUND_SUBGROUPS b3_index=", DLBB3Index, " count=", Length(DLBSubs), "\n");;

  DLBWanted := Filtered(DSDFrozenWindows, w -> w.b3_index = DLBB3Index);;
  for DLBSub in DLBSubs do
    DLBL := Grp(DLBSub);;
    DLBQrec := DCP3BuildWindow(DLBL);;
    DLBGenWords := Set(List(GeneratorsOfGroup(DLBL), String));;
    DLBNodeIdComputed := HexSHA256(Concatenation("index=", String(DLBB3Index), "\n",
      JoinC(DLBGenWords, "\n"), "\n"));;
    DLBMatch := First(DLBWanted, w -> w.node_id = DLBNodeIdComputed);;
    if DLBMatch <> fail then
      Add(DLBWindows, rec(node_id:=DLBNodeIdComputed, b3_index:=DLBB3Index,
        K_ord:=DLBQrec.K_ord, F2_ratio:=DLBQrec.F2, degree:=DCP3MDegree+DLBQrec.degL,
        JX_one_line:=List([1..DCP3MDegree+DLBQrec.degL], j -> j^DLBQrec.JX),
        JY_one_line:=List([1..DCP3MDegree+DLBQrec.degL], j -> j^DLBQrec.JY),
        JC_one_line:=List([1..DCP3MDegree+DLBQrec.degL], j -> j^DLBQrec.JC)));;
    fi;;
  od;;

  DLBFoundNodeIds := Set(List(Filtered(DLBWindows, w -> w.b3_index = DLBB3Index), w -> w.node_id));;
  DLBWantedNodeIds := Set(List(DLBWanted, w -> w.node_id));;
  if DLBFoundNodeIds <> DLBWantedNodeIds then
    Print("DLB_WARNING_MISSING_NODE_IDS b3_index=", DLBB3Index, " wanted=", DLBWantedNodeIds,
      " found=", DLBFoundNodeIds, " -- NOT marking this b3_index done (will retry / reported honestly)\n");;
  else
    Add(DLBDoneIndices, DLBB3Index);;
  fi;;
  DLBWriteOutput();;
  Print("DLB_CHECKPOINT_WRITTEN b3_index=", DLBB3Index, " total_windows_so_far=", Length(DLBWindows), "\n");;

  DLBIdx := DLBIdx + 1;;
od;;

if not DLBStopFlag then
  Print("DLB_ALL_DONE total_windows=", Length(DLBWindows), " total_expected=", Length(DSDFrozenWindows),
    " missing=", Length(DSDFrozenWindows) - Length(DLBWindows), "\n");;
  Print("DLB_STATUS=BATCH_COMPLETE\n");;
fi;;
Print("ALL_DONE\n");;
