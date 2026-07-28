#############################################################################
## wall-miner-v2.g -- wall campaign mining track v2 (Hol sieve pass)
##
## Policy unchanged: rough is fine, bugs tolerated, no polish required.
## This is the exact same "jouzai" caveat as v1 -- output is a lead list,
## NOT a ledger claim, no cross-check performed, no commit.
##
## Theory update (coordinator message, referencing
## docs/notes/wall_design_audit_v1.md Prop 7.1 / Cor 7.2):
##   - All 66 W-A windows (B3-index <= 192) are already THEORETICALLY solvable
##     (W2' floor: |[P_N,P_N]| <= 32 < 60).
##   - Windows with B3-index < 84 are already THEORETICALLY metabelian
##     (Prop 2.4(2) floor).
##   - So the only open question left in band W-A is metabelian-or-not for
##     the 46 windows with B3-index in [84,192].
##
## Hol sieve (Prop 7.1): for P_N := F2/N_F2 = <xbar,ybar> (computed here as
## Group(ximg,yimg) inside A := PB3/N),
##   dl(G_N) <= 1 + dl(C_{P_N}(ybar)) + dl(Stab_{Aut(P_N)}(xbar))
## In particular: both C and Stab solvable AND dl(C)+dl(Stab) <= 1
##   ==> dl(G_N) <= 2 ==> metabelian CONFIRMED (window excluded from "open").
## Cor 7.2 special case: ord(xbar) <= 2 ==> P_N dihedral-or-trivial ==>
##   [P_N,P_N] cyclic ==> metabelian CONFIRMED immediately (no sieve needed).
## Anything else (C or Stab non-solvable, or dl-sum > 1) stays OPEN
## (metabelian status still undetermined by this sieve) -- these are NOT
## claims of non-metabelian, just "this crude sieve did not close it".
##
## Output: search/certs/wall_miner_v2_20260729.json
#############################################################################

Read("search/gaplib_common.g");

if LoadPackage("lins") <> true then
  Error("Failed to load GAP package LINS.");
fi;

RESULTS := [];;
SKIPLOG := [];;

RecordSkip := function(id, reason)
  Add(SKIPLOG, rec(window_id := id, reason := reason));
  Print("[SKIP] ", id, " :: ", reason, "\n");
end;;

# derived length, tolerant of non-solvable input (returns -1 as a sentinel
# meaning "not solvable, dl undefined" instead of erroring)
SafeDl := function(G)
  if IsSolvable(G) then
    return DerivedLength(G);
  else
    return -1;
  fi;
end;;

# ================= Hol sieve for one window =================
# A: the quotient group PB3/N (a permutation group). ximg, yimg: images of
# x0=a^2, y0=b^2 in A.
HolSieve := function(windowId, A, ximg, yimg)
  local PN, ordx, r, Cent, Aut_PN, actFun, StabG, dlC, dlS, dlBound, excluded, reason;
  r := rec(window_id := windowId);
  PN := Group(ximg, yimg);
  r.abs_PN := Size(PN);
  ordx := Order(ximg);
  r.ord_xbar := ordx;

  if ordx <= 2 then
    r.excluded := true;
    r.reason := "ord_xbar<=2: P_N dihedral-or-trivial, metabelian confirmed by Cor 7.2 (no sieve needed)";
    r.dl_C := -2;      # -2 sentinel = "not computed (short-circuited)"
    r.dl_Stab := -2;
    r.dl_upper_bound := 2;
    return r;
  fi;

  Cent := Centralizer(PN, yimg);
  dlC := SafeDl(Cent);
  r.C_order := Size(Cent);
  r.dl_C := dlC;

  Aut_PN := AutomorphismGroup(PN);
  actFun := function(pt, g) return Image(g, pt); end;
  StabG := Stabilizer(Aut_PN, ximg, actFun);
  dlS := SafeDl(StabG);
  r.Stab_order := Size(StabG);
  r.dl_Stab := dlS;

  if dlC = -1 or dlS = -1 then
    r.excluded := false;
    r.reason := "C or Stab non-solvable -- Hol sieve bound undefined, window stays OPEN";
    r.dl_upper_bound := -1;   # -1 sentinel = undefined
    return r;
  fi;

  dlBound := 1 + dlC + dlS;
  r.dl_upper_bound := dlBound;
  if (dlC + dlS) <= 1 then
    r.excluded := true;
    r.reason := "Hol sieve: dl(C)+dl(Stab)<=1, dl(G_N)<=2, metabelian confirmed";
  else
    r.excluded := false;
    r.reason := "Hol sieve did not close: dl(C)+dl(Stab)>1, dl_upper_bound>2, window stays OPEN";
  fi;
  return r;
end;;

# ================= JSON serialization =================
ResultJson := function(r)
  return Concatenation("  {\n",
    "    \"window_id\":", JStr(r.window_id), ",\n",
    "    \"abs_PN\":", String(r.abs_PN), ",\n",
    "    \"ord_xbar\":", String(r.ord_xbar), ",\n",
    "    \"dl_C\":", String(r.dl_C), ",\n",
    "    \"dl_Stab\":", String(r.dl_Stab), ",\n",
    "    \"dl_upper_bound\":", String(r.dl_upper_bound), ",\n",
    "    \"excluded_metabelian\":", JB(r.excluded), ",\n",
    "    \"reason\":", JStr(r.reason), "\n",
    "  }");
end;;

#############################################################################
## ---------------------- shared B3 / PB3 setup ------------------------------
#############################################################################
BF3 := FreeGroup("a", "b");;
aa := BF3.1;;  bb := BF3.2;;
brel := aa * bb * aa * (bb * aa * bb)^-1;;
B3 := BF3 / [brel];;
ga := B3.1;;  gb := B3.2;;

S3can := SymmetricGroup(3);;
phiCan := GroupHomomorphismByImages(B3, S3can, [ga, gb], [(1,2), (2,3)]);;
if phiCan = fail then Error("canonical B3 -> S3 map failed sanity check"); fi;
PB3 := Kernel(phiCan);;

x0 := ga^2;;  y0 := gb^2;;

#############################################################################
## ---------------------- LINS, restrict to B3-index in [84,192] ------------
#############################################################################
Print("=== wall-miner-v2: Hol sieve on the 46 open windows (B3-index 84..192) ===\n");
t0 := GAPLIB_WallElapsedMs();
gr := LowIndexNormalSubgroupsSearch(B3, 192);;
nodes := ComputedNormalSubgroups(gr);;
Print("LINS nodes total: ", Length(nodes), "\n");

serialByIdx := rec();;
countInRange := 0;;
countOutOfRange := 0;;
countNotInPB3 := 0;;

for nd in nodes do
  N := Grp(nd);
  idx := Index(nd);
  if idx = 1 then continue; fi;
  if not IsSubset(PB3, N) then
    countNotInPB3 := countNotInPB3 + 1;
    continue;
  fi;
  if idx < 84 or idx > 192 then
    countOutOfRange := countOutOfRange + 1;
    continue;
  fi;

  if IsBound(serialByIdx.(String(idx))) then
    serialByIdx.(String(idx)) := serialByIdx.(String(idx)) + 1;
  else
    serialByIdx.(String(idx)) := 1;
  fi;
  windowId := Concatenation("W-A-B3idx", String(idx), "-s", String(serialByIdx.(String(idx))));

  if not IsNormal(PB3, N) then
    RecordSkip(windowId, "N not normal in PB3 (unexpected)");
    continue;
  fi;

  nhomP := NaturalHomomorphismByNormalSubgroup(PB3, N);;
  AA := Image(nhomP);;
  ximgA := Image(nhomP, x0);;
  yimgA := Image(nhomP, y0);;

  isoA := IsomorphismPermGroup(AA);;
  AAp := Image(isoA);;
  ximgAp := Image(isoA, ximgA);;
  yimgAp := Image(isoA, yimgA);;

  res := HolSieve(windowId, AAp, ximgAp, yimgAp);
  Add(RESULTS, res);
  countInRange := countInRange + 1;
  Print("  [", windowId, "] |P_N|=", res.abs_PN, " ord(xbar)=", res.ord_xbar,
        " dl_C=", res.dl_C, " dl_Stab=", res.dl_Stab,
        " excluded=", res.excluded, "\n");

  if GAPLIB_CheckCap(500.0, "wall-miner-v2 loop") then
    Print("[CAP WARNING] stopping early at window ", windowId, "\n");
    break;
  fi;
od;

t1 := GAPLIB_WallElapsedMs();
Print("Done: in_range=", countInRange, " out_of_range=", countOutOfRange,
      " not_in_PB3=", countNotInPB3, " elapsed_ms=", t1 - t0, "\n");

#############################################################################
## ---------------------- previous-lead survival check -----------------------
#############################################################################
# v1 leads that fall in this band's index range [84,192]:
#   W-A-B3idx144-s5, W-A-B3idx144-s7, W-A-B3idx192-s7
# (W-A-B3idx48-s4 is out of range: 48 < 84, already theoretically metabelian.)
prevLeadIds := ["W-A-B3idx144-s5", "W-A-B3idx144-s7", "W-A-B3idx192-s7"];;
Print("\n=== v1 lead survival check ===\n");
for pid in prevLeadIds do
  found := First(RESULTS, r -> r.window_id = pid);
  if found = fail then
    Print("  ", pid, ": NOT FOUND in this run's window set (check serial numbering / index range)\n");
  else
    if found.excluded then
      Print("  ", pid, ": EXCLUDED by Hol sieve (metabelian confirmed) -- v1 lead DOES NOT SURVIVE\n");
    else
      Print("  ", pid, ": OPEN (not excluded) -- v1 lead SURVIVES (still a candidate)\n");
    fi;
  fi;
od;

#############################################################################
## ---------------------- write output --------------------------------------
#############################################################################
openResults := Filtered(RESULTS, r -> not r.excluded);;
excludedResults := Filtered(RESULTS, r -> r.excluded);;
Print("\n=== SUMMARY ===\n");
Print("Total windows processed: ", Length(RESULTS), "\n");
Print("Excluded (metabelian confirmed): ", Length(excludedResults), "\n");
Print("Open (metabelian still undetermined): ", Length(openResults), "\n");

outParts := [];;
Add(outParts, "{\n");
Add(outParts, "  \"generated_by\": \"search/wall-miner-v2.g\",\n");
Add(outParts, "  \"note\": \"Hol sieve pass on the 46 open W-A windows (B3-index 84..192); rough lead screening, NOT a ledger claim, no cross-check performed\",\n");
Add(outParts, Concatenation("  \"in_range_processed\": ", String(countInRange), ",\n"));
Add(outParts, Concatenation("  \"out_of_range_skipped\": ", String(countOutOfRange), ",\n"));
Add(outParts, Concatenation("  \"not_in_pb3_skipped\": ", String(countNotInPB3), ",\n"));
Add(outParts, Concatenation("  \"total_excluded_metabelian\": ", String(Length(excludedResults)), ",\n"));
Add(outParts, Concatenation("  \"total_open\": ", String(Length(openResults)), ",\n"));
Add(outParts, "  \"results\": [\n");
for i in [1 .. Length(RESULTS)] do
  Add(outParts, ResultJson(RESULTS[i]));
  if i < Length(RESULTS) then Add(outParts, ",\n"); else Add(outParts, "\n"); fi;
od;
Add(outParts, "  ],\n");
Add(outParts, "  \"skip_log\": [\n");
for i in [1 .. Length(SKIPLOG)] do
  Add(outParts, Concatenation("    {\"window_id\":", JStr(SKIPLOG[i].window_id),
                               ",\"reason\":", JStr(SKIPLOG[i].reason), "}"));
  if i < Length(SKIPLOG) then Add(outParts, ",\n"); else Add(outParts, "\n"); fi;
od;
Add(outParts, "  ]\n");
Add(outParts, "}\n");

WriteFile("search/certs/wall_miner_v2_20260729.json", Concatenation(outParts));
Print("Wrote search/certs/wall_miner_v2_20260729.json\n");
Print("ALL_DONE\n");
