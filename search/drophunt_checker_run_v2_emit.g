#############################################################################
## drophunt_checker_run_v2_emit.g -- emit v2-schema receipts (with required
## fields) for the 5 small test windows, with node_id pre-registration
## checked against expected values (spec SS4 C-2: mismatch = stop).
#############################################################################

Read("search/drophunt_checker_producer_v2.g");;

if LoadPackage("lins") <> true then Error("DCE: LINS package load failed"); fi;

DCET0 := GAPLIB_WallElapsedMs();;
DCESearch := LowIndexNormalSubgroupsSearch(DCP2B3, 100);;
DCENodes := ComputedNormalSubgroups(DCESearch);;
Print("DCE_LINS100_DONE nodes=", Length(DCENodes),
  " elapsed_ms=", GAPLIB_WallElapsedMs()-DCET0, "\n");;

DCENodeId := function(L)
  local genWords;
  genWords := Set(List(GeneratorsOfGroup(L), String));;
  return HexSHA256(Concatenation("index=", String(Index(L, L)), "\n",
    JoinC(genWords, "\n"), "\n"));;
end;;
## NOTE: Index(L,L) above is wrong on purpose-check: replaced below with the
## actual b3_index passed in, matching lins_marked_strictness_export_v1.g's
## own node-key formula (index=[B3:L], not [L:L]).
DCENodeIdFixed := function(L, idx)
  local genWords;
  genWords := Set(List(GeneratorsOfGroup(L), String));;
  return HexSHA256(Concatenation("index=", String(idx), "\n",
    JoinC(genWords, "\n"), "\n"));;
end;;

DCETargets := [
  rec(bIndex:=96, expKord:=18, expF2:=2, label:="cheap1_fib2",
    expectedNodeIds:=["6d48054f9605854a3da43f39ed7f5427f40e01324981461e279932cedaaef2de"]),
  rec(bIndex:=12, expKord:=18, expF2:=3, label:="cheap2_fib3",
    expectedNodeIds:=["00fcf7ead7b82c4abf92fe8cd3510874f263296f92782206eda84b1db4c28a11"]),
  rec(bIndex:=18, expKord:=18, expF2:=3, label:="cheap3_fib3",
    expectedNodeIds:=["89c96e412539a5c6996ab22a868e5c8e37e63de0ac7902577ca2a68e61000780"]),
  rec(bIndex:=3,  expKord:=18, expF2:=3, label:="L3_fib3_K2ingredient",
    expectedNodeIds:=["16437e56512d99ab2c7ca8328293863fe6b7792504ebd592fa21da9d7952bc37"]),
  rec(bIndex:=48, expKord:=36, expF2:=2, label:="fib4_kordvalidated",
    expectedNodeIds:=["43fefcb39d96f5bbd7ea2885869562fdd8c75af8f86137b41d152dedfc8fa9af",
                       "a30e1d8cdf310efc79af078b17fb56b8311da2b240e70c54c7fc262df2f316cb"])
];;

DCEEmitted := [];;
for DCETgt in DCETargets do
  DCEMatches := Filtered(DCENodes, n -> Index(n) = DCETgt.bIndex);;
  for DCENode in DCEMatches do
    DCEL := Grp(DCENode);;
    DCEQrec := DCP2BuildWindow(DCEL);;
    if DCEQrec.K_ord = DCETgt.expKord and DCEQrec.F2 = DCETgt.expF2 then
      DCEId := DCENodeIdFixed(DCEL, DCETgt.bIndex);;
      if not (DCEId in DCETgt.expectedNodeIds) then
        Print("DCE_NODE_ID_PREREGISTRATION_MISMATCH label=", DCETgt.label,
          " got=", DCEId, " expected_one_of=", DCETgt.expectedNodeIds, "\n");;
        Error("DCE: node_id pre-registration mismatch -- fail-closed stop");;
      fi;;
      Print("DCE_NODE_ID_CONFIRMED label=", DCETgt.label, " node_id=", DCEId, "\n");;
      for DCESeed in DCP2Seeds do
        DCERunT0 := GAPLIB_WallElapsedMs();;
        DCEResult := DCP2EvalWindow(DCEQrec, DCESeed);;
        DCERunElapsed := GAPLIB_WallElapsedMs() - DCERunT0;;
        DCEOutPath := Concatenation("search/certs/drophunt_checker_v2_receipt_",
          DCETgt.label, "_", DCESeed.name, "_20260828.json");;
        DCEEmittedRec := DCP2EmitReceiptV2(DCEOutPath, DCEId, DCETgt.bIndex,
          DCEQrec, DCESeed.name, DCESeed.codes, DCEResult, DCERunElapsed);;
        Print("DCE_EMIT label=", DCETgt.label, " seed=", DCESeed.name,
          " c_in_K=", DCEQrec.c_in_K, " path=", DCEEmittedRec.path,
          " sha256=", DCEEmittedRec.sha256, "\n");;
        Add(DCEEmitted, rec(label:=DCETgt.label, seed:=DCESeed.name,
          path:=DCEEmittedRec.path, sha256:=DCEEmittedRec.sha256,
          c_in_K:=DCEQrec.c_in_K));;
      od;;
      break;;
    fi;;
  od;;
od;;

Print("DCE_TOTAL_ELAPSED_MS=", GAPLIB_WallElapsedMs()-DCET0, "\n");;
Print("ALL_DONE\n");;
