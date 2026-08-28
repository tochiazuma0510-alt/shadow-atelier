#############################################################################
## drophunt_checker_run_v2_stage0b.g -- stage 0-b: largest fib<=100 window
## (b3_index=1944 class) cost/RSS probe, run separately (per 10-minute local
## chunk discipline, since LowIndexNormalSubgroupsSearch(B3,1944) itself may
## take a while -- this run's OWN wall time is itself part of the venue
## evidence to report).
#############################################################################

Read("search/drophunt_checker_producer_v2.g");;

if LoadPackage("lins") <> true then Error("DCR2B: LINS package load failed"); fi;

DCR2BT0 := GAPLIB_WallElapsedMs();;
DCR2BSearch := LowIndexNormalSubgroupsSearch(DCP2B3, 1944);;
DCR2BNodes := ComputedNormalSubgroups(DCR2BSearch);;
DCR2BLinsElapsed := GAPLIB_WallElapsedMs() - DCR2BT0;;
Print("DCR2B_LINS1944_DONE nodes=", Length(DCR2BNodes),
  " elapsed_ms=", DCR2BLinsElapsed, "\n");;

DCR2BTarget := Filtered(DCR2BNodes, n -> Index(n) = 1944);;
Print("DCR2B_MATCHES_AT_1944=", Length(DCR2BTarget), "\n");;

DCR2BStatus := "NOT_RUN";;
if Length(DCR2BTarget) > 0 then
  DCR2BL := Grp(DCR2BTarget[1]);;
  DCR2BBuildT0 := GAPLIB_WallElapsedMs();;
  DCR2BQrec := DCP2BuildWindow(DCR2BL);;
  DCR2BBuildElapsed := GAPLIB_WallElapsedMs() - DCR2BBuildT0;;
  Print("DCR2B_BUILD K_ord=", DCR2BQrec.K_ord, " F2=", DCR2BQrec.F2,
    " F3=", DCR2BQrec.F3, " c_in_K=", DCR2BQrec.c_in_K,
    " size_G=", Size(DCR2BQrec.G), " degree=", 36+DCR2BQrec.degL,
    " build_ms=", DCR2BBuildElapsed, "\n");;

  DCR2BWarmT0 := GAPLIB_WallElapsedMs();;
  DCR2BResult := DCP2EvalWindow(DCR2BQrec, DCP2Seeds[1]);;
  DCR2BWarmElapsed := GAPLIB_WallElapsedMs() - DCR2BWarmT0;;
  Print("DCR2B_WARMUP evaluated=", DCR2BResult.evaluated_count,
    " valid=", DCR2BResult.valid_count, " blocked=", DCR2BResult.blocked_count,
    " warmup_ms=", DCR2BWarmElapsed, "\n");;

  DCR2BPerCandMs := 0;;
  if DCR2BResult.evaluated_count > 0 then
    DCR2BPerCandMs := DCR2BWarmElapsed / DCR2BResult.evaluated_count;;
  fi;;

  DCR2BMemStats := GasmanStatistics();;
  Print("DCR2B_MEM ", DCR2BMemStats, "\n");;
  Print("DCR2B_PER_CANDIDATE_MS_APPROX=", DCR2BPerCandMs, "\n");;
  DCR2BStatus := "DONE";;

  DCR2BOutput := Concatenation(
    "{\n  \"schema\":\"drophunt-checker-stage0b/v1\",\n",
    "  \"b3_index\":1944,\n",
    "  \"lins1944_search_elapsed_ms\":", String(DCR2BLinsElapsed), ",\n",
    "  \"K_ord\":", String(DCR2BQrec.K_ord), ",\n",
    "  \"F2\":", String(DCR2BQrec.F2), ",\n",
    "  \"F3_fib\":", String(DCR2BQrec.F3), ",\n",
    "  \"c_in_K\":", JB(DCR2BQrec.c_in_K), ",\n",
    "  \"size_G\":", String(Size(DCR2BQrec.G)), ",\n",
    "  \"degree\":", String(36+DCR2BQrec.degL), ",\n",
    "  \"build_ms\":", String(DCR2BBuildElapsed), ",\n",
    "  \"warmup_ms\":", String(DCR2BWarmElapsed), ",\n",
    "  \"evaluated_count\":", String(DCR2BResult.evaluated_count), ",\n",
    "  \"valid_count\":", String(DCR2BResult.valid_count), ",\n",
    "  \"blocked_count\":", String(DCR2BResult.blocked_count), ",\n",
    "  \"per_candidate_ms_approx\":", String(DCR2BPerCandMs), ",\n",
    "  \"gasman_stats_raw\":", JStr(String(DCR2BMemStats)), "\n}\n");;
  WriteFile("search/certs/drophunt_checker_stage0b_20260828.json", DCR2BOutput);;
  Print("DCR2B_OUTPUT path=search/certs/drophunt_checker_stage0b_20260828.json\n");;
else
  Print("DCR2B_STATUS=NO_1944_NODE_FOUND_AT_THIS_BOUND\n");;
  WriteFile("search/certs/drophunt_checker_stage0b_20260828.json",
    Concatenation("{\n  \"schema\":\"drophunt-checker-stage0b/v1\",\n",
      "  \"status\":\"NO_1944_NODE_FOUND\",\n",
      "  \"lins1944_search_elapsed_ms\":", String(DCR2BLinsElapsed), "\n}\n"));;
fi;;
Print("DCR2B_TOTAL_ELAPSED_MS=", GAPLIB_WallElapsedMs()-DCR2BT0, "\n");;
Print("ALL_DONE\n");;
