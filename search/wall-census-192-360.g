#############################################################################
## wall-census-192-360.g -- I9-5: 帯 1 空白「指数 192-360 帯(未採掘)」の採掘
##
## Universe (pre-registered, do not widen/narrow after the fact): normal
## subgroups N of B3 = <a,b | aba=bab> with N <= PB3 = ker(B3 -> S3) and
## 192 < [B3:N] <= 360. Sieve: EXACTLY the W-A band predicate, reused
## verbatim from search/wall-miner-v5.g (kerchi-judge.g v1.2's JudgeWindow:
## c_in_N, (3.53) closure_353_holds, ker(chi~) commutativity/verdict,
## chi_image_order, T-A assert), with the same LID-1 discipline (single
## GAP process, single LowIndexNormalSubgroupsSearch call, so "same
## enumeration => exhaustive over the band" is structurally guaranteed
## within this run; canonical window id = literal generator words of N,
## not LINS node visitation order).
##
## Difference from wall-miner-v5.g: index bound raised from 192 to 360,
## and only nodes with b3_index STRICTLY GREATER than 192 are judged here
## (the <=192 band was already fully judged by wall-miner-v5.g -- this
## script does not re-judge it, it only records how many such nodes exist
## in this same enumeration, for the census "sieve stage" bookkeeping).
##
## Output: search/certs/wall_census_192_360_20260730.json
##
## Policy unchanged: rough is fine, no polish required, asserts stay,
## no interpretation, no commit of this cert file by this script, no u
## (sealed symbol).
#############################################################################

JUDGE_LIBRARY_ONLY := true;;
JUDGE_SKIP_LEGACY_CROSSCHECK := true;;
Read("search/kerchi-judge.g");   # MakeWindow/CorrectedShadows/GroupOfShadows/
                                  # FindKerWitness/AbstractProd/TT/TH/RtOf/
                                  # JudgeWindow/JStr/JB/JArr/WriteFile etc.

CENSUS_INDEX_LO := 192;;   # exclusive lower bound (already covered by W-A / wall-miner-v5.g)
CENSUS_INDEX_HI := 360;;   # inclusive upper bound (this task's assignment)

#############################################################################
## ---------------------- Hol sieve (from wall-miner-v2.g/v5.g, verbatim) ----
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

Print("=== wall-census-192-360: single-process, single-LINS-call census over band (",
      CENSUS_INDEX_LO, ", ", CENSUS_INDEX_HI, "] ===\n");
t0 := GAPLIB_WallElapsedMs();
if LoadPackage("lins") <> true then
  Error("Failed to load GAP package LINS.");
fi;
gr := LowIndexNormalSubgroupsSearch(B3, CENSUS_INDEX_HI);;   # ONE call, LID-1 discipline
nodes := ComputedNormalSubgroups(gr);;
tLins := GAPLIB_WallElapsedMs();
Print("LINS nodes total (this single call, bound=", CENSUS_INDEX_HI, "): ", Length(nodes),
      " (lins_elapsed_ms=", tLins - t0, ")\n");

#############################################################################
## ---------------------- sieve stage 0: raw node census ---------------------
#############################################################################
countRawTotal := Length(nodes);;
countIdx1 := Length(Filtered(nodes, nd -> Index(nd) = 1));;
countAlreadyCovered := 0;;   # in PB3, index <= CENSUS_INDEX_LO (out of scope, already W-A)
countAboveHi := 0;;          # should be 0 by construction of the LINS bound, sanity only
countNotInPB3_inBand := 0;;  # index in band but N not <= PB3 -- out of scope (PB3-only universe)

#############################################################################
## ---------------------- process band windows on this one enumeration ------
#############################################################################
RESULTS := [];;
SKIPLOG := [];;
RecordSkip := function(id, reason)
  Add(SKIPLOG, rec(window_id := id, reason := reason));
  Print("[SKIP] ", id, " :: ", reason, "\n");
end;;

serialByIdx := rec();;
countProcessed := 0;;

for nd in nodes do
  N := Grp(nd);
  b3idx := Index(nd);
  if b3idx = 1 then continue; fi;
  if b3idx > CENSUS_INDEX_HI then
    countAboveHi := countAboveHi + 1;
    continue;
  fi;
  if not IsSubset(PB3, N) then
    # out of scope regardless of index -- PB3-only universe, same as W-A
    continue;
  fi;
  if b3idx <= CENSUS_INDEX_LO then
    countAlreadyCovered := countAlreadyCovered + 1;
    continue;
  fi;
  # -- in band: PB3-normal, CENSUS_INDEX_LO < b3idx <= CENSUS_INDEX_HI --

  # run-local serial id (not a cross-run identifier -- LID-1)
  if IsBound(serialByIdx.(String(b3idx))) then
    serialByIdx.(String(b3idx)) := serialByIdx.(String(b3idx)) + 1;
  else
    serialByIdx.(String(b3idx)) := 1;
  fi;
  runLocalId := Concatenation("W-B192-360-B3idx", String(b3idx), "-s",
                               String(serialByIdx.(String(b3idx))));

  # canonical id (LID-1): literal generating words of N, as words in a,b
  genWords := List(GeneratorsOfGroup(N), String);;

  if not IsNormal(PB3, N) then
    RecordSkip(runLocalId, "N not normal in PB3 (unexpected)");
    continue;
  fi;

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

  if GAPLIB_CheckCap(500.0, "wall-census-192-360 loop") then
    Print("[CAP WARNING] stopping early at window ", runLocalId, "\n");
    break;
  fi;
od;

t1 := GAPLIB_WallElapsedMs();
Print("Done: band_processed=", countProcessed, " already_covered_le192=", countAlreadyCovered,
      " above_hi_sanity=", countAboveHi, " elapsed_ms_total=", t1 - t0, "\n");

#############################################################################
## ---------------------- summary (sieve-stage survivor counts) --------------
#############################################################################
nonAbelianRows := Filtered(RESULTS, r -> r.judge.verdict = "NONABELIAN");;
abelianRows := Filtered(RESULTS, r -> r.judge.verdict = "ABELIAN");;
unscreenedRows := Filtered(RESULTS, r -> r.judge.verdict = "UNSCREENED");;
holMismatchRows := Filtered(RESULTS, r -> (r.judge.verdict = "ABELIAN") <> r.hol.hol_metabelian_confirmed
                                           and r.judge.verdict <> "UNSCREENED");;
taFailRows := Filtered(RESULTS, r -> not r.judge.ta_assert_holds);;
settledFailRows := Filtered(RESULTS, r -> r.judge.settled_fail_count > 0);;
cInNRows := Filtered(RESULTS, r -> r.judge.c_in_N);;

Print("\n=== SUMMARY (sieve stages) ===\n");
Print("Band (", CENSUS_INDEX_LO, ", ", CENSUS_INDEX_HI, "]: PB3-normal-in-band candidates found: ",
      Length(RESULTS) + Length(SKIPLOG), "\n");
Print("Band windows processed (judged): ", Length(RESULTS), "\n");
Print("  of which c_in_N = true: ", Length(cInNRows), "\n");
Print("  of which (3.53) closure holds (screened, not UNSCREENED): ",
      Length(RESULTS) - Length(unscreenedRows), "\n");
Print("  of which ker(chi~) ABELIAN: ", Length(abelianRows), "\n");
Print("  of which ker(chi~) NONABELIAN (real leads, with witness): ", Length(nonAbelianRows), "\n");
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
Add(outParts, "  \"generated_by\": \"search/wall-census-192-360.g\",\n");
Add(outParts, "  \"note\": \"I9-5 band-1 census: normal N<=PB3 with 192<[B3:N]<=360, single GAP process, single LINS call (LID-1 discipline, ruling 171), judged uniformly via kerchi-judge.g v1.2's (F2)+settled JudgeWindow with legacy EnumerateReducedHexagon crosscheck disabled -- IDENTICAL sieve predicate to wall-miner-v5.g's W-A band (index<=192), extended to the next band only. NOT a ledger claim, no interpretation, no cross-check against an independently-implemented checker (crosscheck/ is separate).\",\n");
Add(outParts, Concatenation("  \"band_index_lo_exclusive\": ", String(CENSUS_INDEX_LO), ",\n"));
Add(outParts, Concatenation("  \"band_index_hi_inclusive\": ", String(CENSUS_INDEX_HI), ",\n"));
Add(outParts, Concatenation("  \"lins_nodes_total_this_call\": ", String(countRawTotal), ",\n"));
Add(outParts, Concatenation("  \"lins_elapsed_ms\": ", String(tLins - t0), ",\n"));
Add(outParts, Concatenation("  \"total_elapsed_ms\": ", String(t1 - t0), ",\n"));
Add(outParts, Concatenation("  \"already_covered_le", String(CENSUS_INDEX_LO), "_pb3_count\": ",
                             String(countAlreadyCovered), ",\n"));
Add(outParts, Concatenation("  \"band_candidates_found\": ",
                             String(Length(RESULTS) + Length(SKIPLOG)), ",\n"));
Add(outParts, Concatenation("  \"band_windows_processed\": ", String(countProcessed), ",\n"));
Add(outParts, Concatenation("  \"c_in_N_count\": ", String(Length(cInNRows)), ",\n"));
Add(outParts, Concatenation("  \"closure_353_holds_count\": ",
                             String(Length(RESULTS) - Length(unscreenedRows)), ",\n"));
Add(outParts, Concatenation("  \"abelian_count\": ", String(Length(abelianRows)), ",\n"));
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

WriteFile("search/certs/wall_census_192_360_20260730.json", Concatenation(outParts));
Print("Wrote search/certs/wall_census_192_360_20260730.json\n");
Print("ALL_DONE\n");
