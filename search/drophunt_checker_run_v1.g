#############################################################################
## drophunt_checker_run_v1.g -- driver: find target LINS windows, evaluate
## Mode A (row36) and Mode B (row71) via drophunt_checker_producer_v1.g,
## emit one receipt JSON per (window,seed), plus a summary log.
#############################################################################

Read("search/drophunt_checker_producer_v1.g");;

if LoadPackage("lins") <> true then Error("DCR: LINS package load failed"); fi;

DCRT0 := GAPLIB_WallElapsedMs();;
DCRSearch := LowIndexNormalSubgroupsSearch(DCPB3, 100);;
DCRNodes := ComputedNormalSubgroups(DCRSearch);;
Print("DCR_LINS100_DONE nodes=", Length(DCRNodes),
  " elapsed_ms=", GAPLIB_WallElapsedMs()-DCRT0, "\n");;

## targets: (b3_index, expected K_ord, expected F2ratio, label)
DCRTargets := [
  rec(bIndex:=96, expKord:=18, expF2:=2, label:="cheap1_fib2"),
  rec(bIndex:=12, expKord:=18, expF2:=3, label:="cheap2_fib3"),
  rec(bIndex:=18, expKord:=18, expF2:=3, label:="cheap3_fib3"),
  rec(bIndex:=3,  expKord:=18, expF2:=3, label:="L3_fib3_K2ingredient"),
  rec(bIndex:=48, expKord:=36, expF2:=2, label:="fib4_kordvalidated")
];;

DCRSummary := [];;
for DCRTgt in DCRTargets do
  DCRMatches := Filtered(DCRNodes, n -> Index(n) = DCRTgt.bIndex);;
  DCRFound := false;;
  for DCRNode in DCRMatches do
    DCRL := Grp(DCRNode);;
    DCRQrec := DCPBuildWindow(DCRL);;
    if DCRQrec.K_ord = DCRTgt.expKord and DCRQrec.F2 = DCRTgt.expF2 then
      DCRFound := true;;
      Print("DCR_TARGET_MATCHED b3_index=", DCRTgt.bIndex, " label=", DCRTgt.label,
        " K_ord=", DCRQrec.K_ord, " F2=", DCRQrec.F2, " F3(fib)=", DCRQrec.F3, "\n");;
      for DCRSeed in DCPSeeds do
        DCRRunT0 := GAPLIB_WallElapsedMs();;
        DCRResult := DCPEvalWindow(DCRQrec, DCRSeed);;
        DCRRunElapsed := GAPLIB_WallElapsedMs() - DCRRunT0;;
        DCROutPath := Concatenation("search/certs/drophunt_checker_receipt_",
          DCRTgt.label, "_", DCRSeed.name, "_v1_20260830.json");;
        DCREmitted := DCPEmitReceipt(DCROutPath,
          rec(node_id:=HexSHA256(String(DCRL)), b3_index:=DCRTgt.bIndex),
          DCRQrec, DCRSeed.name, DCRResult, DCRRunElapsed);;
        Print("DCR_RESULT label=", DCRTgt.label, " seed=", DCRSeed.name,
          " evaluated=", DCRResult.evaluated_count,
          " expected=", DCRResult.expected_count,
          " valid=", DCRResult.valid_count,
          " elapsed_ms=", DCRRunElapsed,
          " path=", DCREmitted.path, " sha256=", DCREmitted.sha256, "\n");;
        Add(DCRSummary, rec(label:=DCRTgt.label, b3_index:=DCRTgt.bIndex,
          K_ord:=DCRQrec.K_ord, F2:=DCRQrec.F2, F3_fib:=DCRQrec.F3,
          seed:=DCRSeed.name, evaluated:=DCRResult.evaluated_count,
          expected:=DCRResult.expected_count, valid:=DCRResult.valid_count,
          elapsed_ms:=DCRRunElapsed, receipt_path:=DCREmitted.path,
          receipt_sha256:=DCREmitted.sha256));;
      od;;
      break;;
    fi;;
  od;;
  if not DCRFound then
    Print("DCR_TARGET_NOT_FOUND b3_index=", DCRTgt.bIndex, " label=", DCRTgt.label,
      " candidates_at_index=", Length(DCRMatches), "\n");;
  fi;;
od;;

DCRTotalElapsed := GAPLIB_WallElapsedMs() - DCRT0;;
Print("DCR_SUMMARY windows_processed=", Length(DCRSummary)/2,
  " total_elapsed_ms=", DCRTotalElapsed, "\n");;

DCRSummaryJson := JoinC(List(DCRSummary, r -> Concatenation(
  "{\"label\":", JStr(r.label), ",\"b3_index\":", String(r.b3_index),
  ",\"K_ord\":", String(r.K_ord), ",\"F2\":", String(r.F2),
  ",\"F3_fib\":", String(r.F3_fib), ",\"seed\":", JStr(r.seed),
  ",\"evaluated\":", String(r.evaluated), ",\"expected\":", String(r.expected),
  ",\"valid\":", String(r.valid), ",\"elapsed_ms\":", String(r.elapsed_ms),
  ",\"receipt_path\":", JStr(r.receipt_path),
  ",\"receipt_sha256\":", JStr(r.receipt_sha256), "}")), ",\n");;

DCRSummaryOut := Concatenation(
  "{\n  \"schema\":\"drophunt-checker-run-summary/v1\",\n",
  "  \"lins100_search_elapsed_ms\":", String(GAPLIB_WallElapsedMs()-DCRT0), ",\n",
  "  \"total_elapsed_ms\":", String(DCRTotalElapsed), ",\n",
  "  \"windows\":[\n", DCRSummaryJson, "\n  ]\n}\n");;
WriteFile("search/certs/drophunt_checker_run_summary_v1_20260830.json", DCRSummaryOut);;
Print("DCR_OUTPUT path=search/certs/drophunt_checker_run_summary_v1_20260830.json\n");;
Print("ALL_DONE\n");;
