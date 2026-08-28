#############################################################################
## drophunt_checker_run_v2_escalation.g -- one additional, larger-degree/
## larger-F2 cost datapoint (b3_index=108, fib=9) to check whether the
## quotient-construction cost estimated from the 5 small (b3_index<=100)
## samples generalizes, before extrapolating to the full fib<=100 358-window
## set (which spans b3_index up to 1944, median 432).
#############################################################################

Read("search/drophunt_checker_producer_v1.g");;

if LoadPackage("lins") <> true then Error("DCR2: LINS package load failed"); fi;

DCR2T0 := GAPLIB_WallElapsedMs();;
DCR2Search := LowIndexNormalSubgroupsSearch(DCPB3, 108);;
DCR2Nodes := ComputedNormalSubgroups(DCR2Search);;
Print("DCR2_LINS108_DONE nodes=", Length(DCR2Nodes),
  " elapsed_ms=", GAPLIB_WallElapsedMs()-DCR2T0, "\n");;

DCR2Matches := Filtered(DCR2Nodes, n -> Index(n) = 108);;
Print("DCR2_MATCHES_AT_108=", Length(DCR2Matches), "\n");;
for DCR2Node in DCR2Matches do
  DCR2L := Grp(DCR2Node);;
  DCR2BuildT0 := GAPLIB_WallElapsedMs();;
  DCR2Qrec := DCPBuildWindow(DCR2L);;
  DCR2BuildElapsed := GAPLIB_WallElapsedMs() - DCR2BuildT0;;
  Print("DCR2_WINDOW K_ord=", DCR2Qrec.K_ord, " F2=", DCR2Qrec.F2,
    " F3=", DCR2Qrec.F3, " degree=", DCPMDegree+DCR2Qrec.degL,
    " build_ms=", DCR2BuildElapsed, "\n");;
  if DCR2Qrec.F3 = 9 then
    for DCR2Seed in DCPSeeds do
      DCR2EvalT0 := GAPLIB_WallElapsedMs();;
      DCR2Result := DCPEvalWindow(DCR2Qrec, DCR2Seed);;
      DCR2EvalElapsed := GAPLIB_WallElapsedMs() - DCR2EvalT0;;
      Print("DCR2_EVAL seed=", DCR2Seed.name, " evaluated=", DCR2Result.evaluated_count,
        " valid=", DCR2Result.valid_count, " eval_ms=", DCR2EvalElapsed, "\n");;
    od;;
    DCR2OutPath := "search/certs/drophunt_checker_receipt_escalation108_row36_v1_20260830.json";;
    DCR2Emitted := DCPEmitReceipt(DCR2OutPath,
      rec(node_id:=HexSHA256(String(DCR2L)), b3_index:=108),
      DCR2Qrec, "row36", DCPEvalWindow(DCR2Qrec, DCPSeeds[1]), DCR2BuildElapsed);;
    Print("DCR2_OUTPUT path=", DCR2Emitted.path, "\n");;
  fi;;
od;;
Print("DCR2_TOTAL_ELAPSED_MS=", GAPLIB_WallElapsedMs()-DCR2T0, "\n");;
Print("ALL_DONE\n");;
