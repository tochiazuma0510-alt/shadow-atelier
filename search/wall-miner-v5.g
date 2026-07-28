#############################################################################
## wall-miner-v5.g -- wall campaign mining track v5 (裁定171・LID-1 処方)
##
## "帯の締め": a SINGLE GAP PROCESS, ONE LINS call, processing all 66 W-A
## windows (N normal in B3, N <= PB3, index <= 192) on that SAME enumeration,
## so that "same enumeration => exhaustive over all 66" is structurally
## guaranteed within this run (no cross-process/cross-call reliance on LINS
## node order).
##
## *** LID-1 background (discovered while testing kerchi-judge v1.1/v1.2,
## reported to the coordinator 2026-07-29): LowIndexNormalSubgroupsSearch was
## found to return the SAME-index nodes in a NON-DETERMINISTIC order across
## repeated calls, even within a single GAP session (verified: 3 calls to
## LowIndexNormalSubgroupsSearch(B3,192) in the same process gave 3 different
## orderings of the six order-27 structures at B3-index 162). This means the
## "W-A-B3idx<n>-s<k>" ("k-th node found at this index") window-id scheme used
## throughout wall-miner-v1/v2/v3/v4.g and kerchi-judge.g is NOT guaranteed to
## refer to the same underlying subgroup across separate runs. LID-1 (this
## script) does not "fix" that scheme -- it REPLACES it: every window's
## canonical, run-independent identity here is the literal GENERATING WORD
## LIST of N (as words in a,b, i.e. GAP's own String() of each element of
## GeneratorsOfGroup(N)) -- reproducible by construction, since re-evaluating
## those exact words in B3 always yields the same subgroup regardless of what
## order any particular LINS call happened to visit it in. The old
## "W-A-B3idx<n>-s<k>" label is still recorded, explicitly marked
## run_local_serial_id, for cross-referencing this run's own printed log --
## it is NOT to be trusted as a cross-run identifier (see LID-1 above).
##
## Per window this computes:
##   - Hol sieve (search/wall-miner-v2.g's HolSieve, reused verbatim) as a
##     cross-reference / cheap dl-upper-bound alongside the exact computation
##     below (not used to skip or exclude anything here -- v5 computes the
##     exact answer for every one of the 66 windows regardless of what the
##     Hol sieve predicts).
##   - the exact (F2)+settled shadow enumeration (kerchi-judge.g v1.2's
##     JudgeWindow, reused via JUDGE_LIBRARY_ONLY, with
##     JUDGE_SKIP_LEGACY_CROSSCHECK := true -- the coordinator's explicit
##     instruction is NOT to rely on the old EnumerateReducedHexagon path at
##     all here, on either side of c_in_N, since KJ-1 raised doubt about
##     whether ITS hex310/hex311 conditions have the same missing-settled-
##     check gap that the (F2) predicate had before the KJ-1 fix).
##   - (3.53) closure, ker(chi~) commutativity (exact, with witness if
##     NONABELIAN), chi_image_order.
##
## Output: search/certs/wall_miner_v5_20260729.json (all 66 windows in one
## certificate).
##
## Policy unchanged: rough is fine, no polish required, asserts stay,
## no interpretation, no commit, no u (sealed symbol).
#############################################################################

JUDGE_LIBRARY_ONLY := true;;
JUDGE_SKIP_LEGACY_CROSSCHECK := true;;
Read("search/kerchi-judge.g");   # MakeWindow/CorrectedShadows/GroupOfShadows/
                                  # FindKerWitness/AbstractProd/TT/TH/RtOf/
                                  # JudgeWindow/JStr/JB/JArr/WriteFile etc.

#############################################################################
## ---------------------- Hol sieve (from wall-miner-v2.g, verbatim reuse) --
#############################################################################
SafeDl := function(G)
  if IsSolvable(G) then
    return DerivedLength(G);
  else
    return -1;
  fi;
end;;

HolSieve := function(A, ximg, yimg)
  local PN, ordx, r, Cent, Aut_PN, actFun, StabG, dlC, dlS, dlBound;
  r := rec();
  PN := Group(ximg, yimg);
  r.ord_xbar := Order(ximg);

  if r.ord_xbar <= 2 then
    r.dl_C := -2;  r.dl_Stab := -2;  r.dl_upper_bound := 2;
    r.hol_metabelian_confirmed := true;
    r.hol_reason := "ord_xbar<=2: dihedral-or-trivial P_N, metabelian by Cor 7.2";
    return r;
  fi;

  Cent := Centralizer(PN, yimg);
  dlC := SafeDl(Cent);
  r.C_order := Size(Cent);  r.dl_C := dlC;

  Aut_PN := AutomorphismGroup(PN);
  actFun := function(pt, g) return Image(g, pt); end;
  StabG := Stabilizer(Aut_PN, ximg, actFun);
  dlS := SafeDl(StabG);
  r.Stab_order := Size(StabG);  r.dl_Stab := dlS;

  if dlC = -1 or dlS = -1 then
    r.dl_upper_bound := -1;
    r.hol_metabelian_confirmed := false;
    r.hol_reason := "C or Stab non-solvable -- Hol sieve bound undefined";
    return r;
  fi;

  dlBound := 1 + dlC + dlS;
  r.dl_upper_bound := dlBound;
  r.hol_metabelian_confirmed := ((dlC + dlS) <= 1);
  if r.hol_metabelian_confirmed then
    r.hol_reason := "dl(C)+dl(Stab)<=1, dl(G_N)<=2, metabelian confirmed";
  else
    r.hol_reason := "dl(C)+dl(Stab)>1, sieve did not close (window would have been OPEN in v2)";
  fi;
  return r;
end;;

#############################################################################
## ---------------------- shared B3 / PB3 setup, LINS called EXACTLY ONCE ---
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

Print("=== wall-miner-v5: single-process, single-LINS-call pass over all 66 W-A windows ===\n");
t0 := GAPLIB_WallElapsedMs();
if LoadPackage("lins") <> true then
  Error("Failed to load GAP package LINS.");
fi;
gr := LowIndexNormalSubgroupsSearch(B3, 192);;   # ONE call, per LID-1 / ruling 171 (1)
nodes := ComputedNormalSubgroups(gr);;
Print("LINS nodes total (this single call): ", Length(nodes), "\n");

#############################################################################
## ---------------------- process all 66 windows on this one enumeration ----
#############################################################################
RESULTS := [];;
SKIPLOG := [];;
RecordSkip := function(id, reason)
  Add(SKIPLOG, rec(window_id := id, reason := reason));
  Print("[SKIP] ", id, " :: ", reason, "\n");
end;;

serialByIdx := rec();;
countProcessed := 0;;
countNotInPB3 := 0;;

for nd in nodes do
  N := Grp(nd);
  b3idx := Index(nd);
  if b3idx = 1 then continue; fi;
  if not IsSubset(PB3, N) then
    countNotInPB3 := countNotInPB3 + 1;
    continue;
  fi;

  # run-local serial id (NOT a cross-run identifier -- see LID-1 header note)
  if IsBound(serialByIdx.(String(b3idx))) then
    serialByIdx.(String(b3idx)) := serialByIdx.(String(b3idx)) + 1;
  else
    serialByIdx.(String(b3idx)) := 1;
  fi;
  runLocalId := Concatenation("W-A-B3idx", String(b3idx), "-s", String(serialByIdx.(String(b3idx))));

  # canonical id (LID-1): the literal generating words of N, as words in a,b
  genWords := List(GeneratorsOfGroup(N), String);;

  if not IsNormal(PB3, N) then
    RecordSkip(runLocalId, "N not normal in PB3 (unexpected)");
    continue;
  fi;

  # full-B3-level hom, preserving sigma1,sigma2 marking (needed for theta~/tau~/settled)
  hm := NaturalHomomorphismByNormalSubgroup(B3, N);;
  isoQ := IsomorphismPermGroup(Image(hm));;
  s1 := Image(isoQ, Image(hm, ga));;
  s2 := Image(isoQ, Image(hm, gb));;

  W := MakeWindow(s1, s2);;
  holRes := HolSieve(W.Bq, W.x, W.y);;

  jres := JudgeWindow(s1, s2, runLocalId);;

  rowRec := rec(run_local_serial_id := runLocalId, canonical_id_words := genWords,
                b3_index := b3idx, judge := jres, hol := holRes);
  Add(RESULTS, rowRec);
  countProcessed := countProcessed + 1;

  Print("  [", runLocalId, "] b3_index=", b3idx, " canonical=", genWords, "\n");
  Print("      c_in_N=", jres.c_in_N, " |B3/N|=", jres.abs_Bq, " |P_N|=", jres.abs_PN,
        " N_ord=", jres.N_ord, " shadow_total=", jres.shadow_total,
        " settled_fail=", jres.settled_fail_count, "\n");
  Print("      verdict=", jres.verdict, " ker_size=", jres.ker_size,
        " chi_image_order=", jres.chi_image_order, " ta_holds=", jres.ta_assert_holds,
        " closure=", jres.closure_353_holds, "\n");
  Print("      Hol: ord_xbar=", holRes.ord_xbar, " dl_upper_bound=", holRes.dl_upper_bound,
        " hol_metabelian_confirmed=", holRes.hol_metabelian_confirmed, "\n");
  if jres.verdict = "NONABELIAN" then
    Print("      *** LEAD: ker(chi~) NONABELIAN *** witness=", jres.witness, "\n");
  fi;

  if GAPLIB_CheckCap(500.0, "wall-miner-v5 loop") then
    Print("[CAP WARNING] stopping early at window ", runLocalId, "\n");
    break;
  fi;
od;

t1 := GAPLIB_WallElapsedMs();
Print("Done: processed=", countProcessed, " (of 66 expected) not_in_PB3_skipped=", countNotInPB3,
      " elapsed_ms=", t1 - t0, "\n");

if countProcessed <> 66 then
  RecordSkip("GLOBAL", Concatenation("countProcessed=", String(countProcessed),
             " != expected 66 -- see skip_log / cap warnings above for why"));
fi;

#############################################################################
## ---------------------- summary --------------------------------------------
#############################################################################
nonAbelianRows := Filtered(RESULTS, r -> r.judge.verdict = "NONABELIAN");;
unscreenedRows := Filtered(RESULTS, r -> r.judge.verdict = "UNSCREENED");;
holMismatchRows := Filtered(RESULTS, r -> (r.judge.verdict = "ABELIAN") <> r.hol.hol_metabelian_confirmed
                                           and r.judge.verdict <> "UNSCREENED");;
taFailRows := Filtered(RESULTS, r -> not r.judge.ta_assert_holds);;
settledFailRows := Filtered(RESULTS, r -> r.judge.settled_fail_count > 0);;

Print("\n=== SUMMARY ===\n");
Print("Total windows processed: ", Length(RESULTS), " (target: 66)\n");
Print("NONABELIAN (real leads, with witness): ", Length(nonAbelianRows), "\n");
for r in nonAbelianRows do
  Print("  LEAD: ", r.run_local_serial_id, " canonical=", r.canonical_id_words,
        " witness=", r.judge.witness, "\n");
od;
Print("UNSCREENED ((3.53) closure failed): ", Length(unscreenedRows), "\n");
for r in unscreenedRows do
  Print("  UNSCREENED: ", r.run_local_serial_id, " canonical=", r.canonical_id_words, "\n");
od;
Print("T-A universal assert FAILED: ", Length(taFailRows), "\n");
Print("Windows where settled clause rejected >=1 candidate: ", Length(settledFailRows), "\n");
for r in settledFailRows do
  Print("  settled_fail_count=", r.judge.settled_fail_count, " at ", r.run_local_serial_id,
        " canonical=", r.canonical_id_words, "\n");
od;
Print("Windows where exact verdict disagrees with Hol-sieve prediction (excluding UNSCREENED): ",
      Length(holMismatchRows), "\n");
for r in holMismatchRows do
  Print("  HOL MISMATCH: ", r.run_local_serial_id, " exact_verdict=", r.judge.verdict,
        " hol_metabelian_confirmed=", r.hol.hol_metabelian_confirmed, "\n");
od;

#############################################################################
## ---------------------- write output --------------------------------------
#############################################################################
CanonicalIdJson := function(words) return JArr(List(words, JStr)); end;;

HolJson := function(h)
  return Concatenation("{\"ord_xbar\":", String(h.ord_xbar),
    ",\"dl_C\":", String(h.dl_C), ",\"dl_Stab\":", String(h.dl_Stab),
    ",\"dl_upper_bound\":", String(h.dl_upper_bound),
    ",\"hol_metabelian_confirmed\":", JB(h.hol_metabelian_confirmed),
    ",\"hol_reason\":", JStr(h.hol_reason), "}");
end;;

RowJson := function(row)
  return Concatenation("  {\n",
    "    \"run_local_serial_id\":", JStr(row.run_local_serial_id), ",\n",
    "    \"canonical_id_words\":", CanonicalIdJson(row.canonical_id_words), ",\n",
    "    \"b3_index\":", String(row.b3_index), ",\n",
    "    \"judge\":", ResultJson(row.judge), ",\n",
    "    \"hol\":", HolJson(row.hol), "\n",
    "  }");
end;;

outParts := [];;
Add(outParts, "{\n");
Add(outParts, "  \"generated_by\": \"search/wall-miner-v5.g\",\n");
Add(outParts, "  \"note\": \"LID-1 consolidation pass (ruling 171): single GAP process, single LINS call, all 66 W-A windows judged uniformly via kerchi-judge.g v1.2's (F2)+settled JudgeWindow (legacy EnumerateReducedHexagon crosscheck disabled throughout, per coordinator instruction); NOT a ledger claim, no cross-check against an independently-implemented checker\",\n");
Add(outParts, Concatenation("  \"windows_processed\": ", String(countProcessed), ",\n"));
Add(outParts, Concatenation("  \"windows_not_in_pb3_skipped\": ", String(countNotInPB3), ",\n"));
Add(outParts, Concatenation("  \"nonabelian_count\": ", String(Length(nonAbelianRows)), ",\n"));
Add(outParts, Concatenation("  \"unscreened_count\": ", String(Length(unscreenedRows)), ",\n"));
Add(outParts, Concatenation("  \"ta_assert_failed_count\": ", String(Length(taFailRows)), ",\n"));
Add(outParts, Concatenation("  \"settled_rejected_any_count\": ", String(Length(settledFailRows)), ",\n"));
Add(outParts, Concatenation("  \"hol_mismatch_count\": ", String(Length(holMismatchRows)), ",\n"));
Add(outParts, "  \"windows\": [\n");
for i in [1 .. Length(RESULTS)] do
  Add(outParts, RowJson(RESULTS[i]));
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

WriteFile("search/certs/wall_miner_v5_20260729.json", Concatenation(outParts));
Print("Wrote search/certs/wall_miner_v5_20260729.json\n");
Print("ALL_DONE\n");
