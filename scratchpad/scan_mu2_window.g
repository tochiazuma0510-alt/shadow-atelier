Read("search/drophunt_checker_producer_v3.g");;
if LoadPackage("lins") <> true then Error("scan: LINS load failed"); fi;;
SCT0 := GAPLIB_WallElapsedMs();;
SCSearch := LowIndexNormalSubgroupsSearch(DCP3B3, 100);;
SCNodes := ComputedNormalSubgroups(SCSearch);;
Print("SCAN_LINS100 nodes=", Length(SCNodes), " elapsed_ms=", GAPLIB_WallElapsedMs()-SCT0, "\n");;
SCFound := fail;;
for SCNode in SCNodes do
  if Index(SCNode) = 1 then continue; fi;;
  SCq := DCP3BuildWindow(Grp(SCNode));;
  if (SCq.K_ord/18) > 1 and (18 mod Order(SCq.JC)) <> 0 then
    Print("SCAN_HIT b3_index=", Index(SCNode), " K_ord=", SCq.K_ord,
      " F1=", SCq.K_ord/18, " F2=", SCq.F2, " ord_cbar=", Order(SCq.JC), "\n");;
    SCFound := Index(SCNode);;
    break;;
  fi;;
od;;
if SCFound = fail then Print("SCAN_NO_HIT_FOUND\n");; fi;;
Print("SCAN_TOTAL_MS=", GAPLIB_WallElapsedMs()-SCT0, "\n");;
Print("ALL_DONE\n");;
