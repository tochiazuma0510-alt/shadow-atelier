#############################################################################
## wall-miner-v3.g -- wall campaign mining track v3 (final stage, ruling 163)
##
## Policy unchanged: rough is fine, bugs tolerated, no polish required.
## Output is a lead list, NOT a ledger claim, no cross-check performed,
## no commit, no u (sealed symbol).
##
## Scope: the 26 windows left OPEN by wall-miner-v2.g's Hol sieve (window ids
## hardcoded below, copied from search/certs/wall_miner_v2_20260729.json).
##
## For each window, actually compute ker(chi-tilde) = the "c=1 layer"
## F_0 := {[0,f] in G_N} at SHADOW level (not a proxy this time):
##   (i)  c_in_N windows: EnumerateReducedHexagon (week3-battery-common.g)
##        with charmingSet = ALL charming m mod N_ord (gcd(2m+1,N_ord)=1),
##        NOT just m=0 (v1's sensitivity bug -- fixed here).
##   (ii) c_notin_N windows: EnumerateWordLevelHexagonPrepend (the LATEST
##        coordinator ruling recorded in week3-battery-common.g, 2026-07-26,
##        "prepend" convention -- reversing an earlier "natural" ruling).
## From the full shadow list, filter to m=0 (the ker-chi-tilde / F_0 layer).
## |ker| := that count. T-A count identity assert:
##   |ker| =?= |shadow_total| / Phi(2*N_ord)
## (this is the |G_N| = |Im(chi-tilde)| * |F_0| torsor identity, assuming
## chi-tilde surjects onto its full (Z/2N_ord)^x codomain of size Phi(2N_ord);
## a mismatch is not "wrong", it is itself a recorded fact -- possible
## C2F-type collapse or source-kernel contamination per the coordinator's
## framing).
##
## Commutativity of F_0 is tested via the EXACT (3.53) composition formula
## specialized to m1=m2=0 (u=1 both sides), not a proxy:
##   [0,f1] o [0,f2] = [0, f1 * E_{0,f1}(f2)],   E_{0,f1} := (xbar->xbar,
##   ybar -> f1^-1 ybar f1) as an actual GAP automorphism of A=PB3/N.
## Since [0,f] |-> f is injective (Prop 2.3 of docs/notes/wall_design_audit_v1.md),
## equality of the f-components f1*E_{0,f1}(f2) vs f2*E_{0,f2}(f1) is an EXACT
## test of [0,f1][0,f2] =?= [0,f2][0,f1], not a heuristic.
## If a noncommuting pair is found, its two [m=0,f] word-witnesses are saved
## (the actual lead payoff of this pass).
##
## Output: search/certs/wall_miner_v3_20260729.json
#############################################################################

Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");

if LoadPackage("lins") <> true then
  Error("Failed to load GAP package LINS.");
fi;

RESULTS := [];;
SKIPLOG := [];;

RecordSkip := function(id, reason)
  Add(SKIPLOG, rec(window_id := id, reason := reason));
  Print("[SKIP] ", id, " :: ", reason, "\n");
end;;

# the 26 v2-OPEN window ids (copied verbatim from wall_miner_v2_20260729.json's
# "results" entries with excluded_metabelian=false)
OPEN_WINDOW_IDS := [
  "W-A-B3idx96-s2", "W-A-B3idx96-s4", "W-A-B3idx96-s5",
  "W-A-B3idx108-s1",
  "W-A-B3idx120-s2",
  "W-A-B3idx126-s2", "W-A-B3idx126-s3",
  "W-A-B3idx144-s1", "W-A-B3idx144-s3", "W-A-B3idx144-s4", "W-A-B3idx144-s5",
  "W-A-B3idx144-s6", "W-A-B3idx144-s7",
  "W-A-B3idx150-s2",
  "W-A-B3idx162-s1", "W-A-B3idx162-s2", "W-A-B3idx162-s3", "W-A-B3idx162-s4",
  "W-A-B3idx162-s5",
  "W-A-B3idx168-s2",
  "W-A-B3idx192-s2", "W-A-B3idx192-s3", "W-A-B3idx192-s4", "W-A-B3idx192-s5",
  "W-A-B3idx192-s6", "W-A-B3idx192-s7"
];;

# ================= ker(chi-tilde) commutativity via exact (3.53) composition =================
# kerShadows: list of rec(m:=0, f:=<elt of A>, word:=<x/y word>) already filtered to m=0.
# Returns rec(commute, witness) -- witness is fail, or rec with the two f-words that fail
# to commute (the first pair found, early-exit).
CheckKerCommute := function(A, ximg, yimg, kerShadows)
  local i, j, f1, f2, hom1, hom2, comp12, comp21, k;
  k := Length(kerShadows);
  for i in [1 .. k] do
    for j in [i+1 .. k] do
      f1 := kerShadows[i].f;
      f2 := kerShadows[j].f;
      hom1 := GroupHomomorphismByImages(A, A, [ximg, yimg], [ximg, f1^-1 * yimg * f1]);
      hom2 := GroupHomomorphismByImages(A, A, [ximg, yimg], [ximg, f2^-1 * yimg * f2]);
      if hom1 = fail or hom2 = fail then
        continue;  # defensive: should not happen if shadow already passed hexagon checks
      fi;
      comp12 := f1 * Image(hom1, f2);
      comp21 := f2 * Image(hom2, f1);
      if comp12 <> comp21 then
        return rec(commute := false,
                    witness := rec(f1_word := kerShadows[i].word, f2_word := kerShadows[j].word));
      fi;
    od;
  od;
  return rec(commute := true, witness := fail);
end;;

# ================= JSON serialization =================
WitnessJson := function(w)
  if w = fail then
    return "null";
  fi;
  return Concatenation("{\"m1\":0,\"f1_word\":", JArr(List(w.f1_word, p -> JPair(JStr(p[1]), p[2]))),
                        ",\"m2\":0,\"f2_word\":", JArr(List(w.f2_word, p -> JPair(JStr(p[1]), p[2]))), "}");
end;;

ResultJson := function(r)
  return Concatenation("  {\n",
    "    \"window_id\":", JStr(r.window_id), ",\n",
    "    \"c_in_N\":", JB(r.c_in_N), ",\n",
    "    \"abs_A\":", String(r.abs_A), ",\n",
    "    \"abs_PN\":", String(r.abs_PN), ",\n",
    "    \"N_ord\":", String(r.N_ord), ",\n",
    "    \"charming_count\":", String(r.charming_count), ",\n",
    "    \"status\":", JStr(r.status), ",\n",
    "    \"shadow_total\":", String(r.shadow_total), ",\n",
    "    \"ker_size\":", String(r.ker_size), ",\n",
    "    \"phi_2Nord\":", String(r.phi_2Nord), ",\n",
    "    \"ta_predicted_ker\":", String(r.ta_predicted_ker), ",\n",
    "    \"ta_assert_holds\":", JB(r.ta_assert_holds), ",\n",
    "    \"ker_commutes\":", JB(r.ker_commutes), ",\n",
    "    \"witness\":", WitnessJson(r.witness), ",\n",
    "    \"note\":", JStr(r.note), "\n",
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

x0 := ga^2;;  y0 := gb^2;;  c0 := (ga * gb * ga)^2;;

#############################################################################
## ---------------------- process each of the 26 OPEN windows ----------------
#############################################################################
Print("=== wall-miner-v3: ker(chi-tilde) shadow-level computation on the 26 v2-OPEN windows ===\n");
t0 := GAPLIB_WallElapsedMs();
gr := LowIndexNormalSubgroupsSearch(B3, 192);;
nodes := ComputedNormalSubgroups(gr);;
Print("LINS nodes total: ", Length(nodes), "\n");

serialByIdx := rec();;
countMatched := 0;;

for nd in nodes do
  N := Grp(nd);
  idx := Index(nd);
  if idx = 1 then continue; fi;
  if not IsSubset(PB3, N) then continue; fi;
  if idx < 84 or idx > 192 then continue; fi;

  if IsBound(serialByIdx.(String(idx))) then
    serialByIdx.(String(idx)) := serialByIdx.(String(idx)) + 1;
  else
    serialByIdx.(String(idx)) := 1;
  fi;
  windowId := Concatenation("W-A-B3idx", String(idx), "-s", String(serialByIdx.(String(idx))));

  if not (windowId in OPEN_WINDOW_IDS) then
    continue;  # not one of the 26 -- v2 already excluded it, out of scope for v3
  fi;
  countMatched := countMatched + 1;

  r := rec(window_id := windowId);

  if not IsNormal(PB3, N) then
    RecordSkip(windowId, "N not normal in PB3 (unexpected)");
    continue;
  fi;

  nhomP := NaturalHomomorphismByNormalSubgroup(PB3, N);;
  AA := Image(nhomP);;
  ximgA := Image(nhomP, x0);;
  yimgA := Image(nhomP, y0);;
  cimgA := Image(nhomP, c0);;

  isoA := IsomorphismPermGroup(AA);;
  Ap := Image(isoA);;
  ximgAp := Image(isoA, ximgA);;
  yimgAp := Image(isoA, yimgA);;
  cimgAp := Image(isoA, cimgA);;

  # IMPORTANT (fixed after a first-run crash): the qrec.G expected by
  # EnumerateReducedHexagon / EnumerateWordLevelHexagonPrepend is P_N :=
  # Group(x,y) itself (see MakeGn in this same file: "G := Group(x,y)"),
  # NOT the ambient A=PB3/N. When xy_generate_A=false (several of our 26
  # windows), A properly contains P_N, and passing G:=A makes BFSWords
  # under-cover G and Error out. Using PN here matches the established
  # convention throughout week3-battery-common.g / week3-M5-explorer.g.
  PN := Group(ximgAp, yimgAp);;
  r.abs_A := Size(Ap);
  r.abs_PN := Size(PN);
  r.c_in_N := (cimgAp = Identity(Ap));
  NordVal := Order(ximgAp);
  r.N_ord := NordVal;
  charmingSet := Filtered([0 .. NordVal - 1], m -> Gcd(2*m+1, NordVal) = 1);;
  r.charming_count := Length(charmingSet);
  r.phi_2Nord := Phi(2 * NordVal);

  Print("--- ", windowId, "  |A|=", r.abs_A, " |P_N|=", r.abs_PN, " c_in_N=", r.c_in_N,
        " N_ord=", NordVal, " |charming|=", r.charming_count, "\n");

  # ---- enumerate full shadow set over ALL charming m (not just m=0) ----
  hexres := fail;
  if r.c_in_N then
    hexres := EnumerateReducedHexagon(rec(x := ximgAp, y := yimgAp, G := PN), charmingSet);
  else
    hexres := EnumerateWordLevelHexagonPrepend(rec(x := ximgAp, y := yimgAp, G := PN), charmingSet);
  fi;

  if GAPLIB_CheckCap(400.0, windowId) then
    r.status := "UNSCREENED";
    r.shadow_total := -1; r.ker_size := -1; r.ta_predicted_ker := -1;
    r.ta_assert_holds := false; r.ker_commutes := false; r.witness := fail;
    r.note := "cap exceeded before enumeration completed, left UNSCREENED";
    Add(RESULTS, r);
    RecordSkip(windowId, "cap exceeded, UNSCREENED");
    continue;
  fi;

  r.shadow_total := hexres.shadow_total;
  kerShadows := Filtered(hexres.shadows, s -> s.m = 0);;
  r.ker_size := Length(kerShadows);

  # ---- T-A count identity assert: |ker| =?= |shadow_total| / Phi(2*N_ord) ----
  if r.phi_2Nord = 0 then
    r.ta_predicted_ker := -1;
    r.ta_assert_holds := false;
    r.note := "phi_2Nord = 0 (degenerate), T-A assert skipped";
  elif r.shadow_total mod r.phi_2Nord <> 0 then
    r.ta_predicted_ker := -1;
    r.ta_assert_holds := false;
  else
    r.ta_predicted_ker := r.shadow_total / r.phi_2Nord;
    r.ta_assert_holds := (r.ta_predicted_ker = r.ker_size);
  fi;

  # ---- ker(chi-tilde) commutativity, exact (3.53) composition ----
  kc := CheckKerCommute(PN, ximgAp, yimgAp, kerShadows);;
  r.ker_commutes := kc.commute;
  r.witness := kc.witness;
  r.status := "computed";
  if not IsBound(r.note) then r.note := ""; fi;

  Print("    shadow_total=", r.shadow_total, " ker_size=", r.ker_size,
        " phi(2*N_ord)=", r.phi_2Nord, " ta_predicted=", r.ta_predicted_ker,
        " ta_holds=", r.ta_assert_holds, " ker_commutes=", r.ker_commutes, "\n");

  Add(RESULTS, r);

  if GAPLIB_CheckCap(500.0, "wall-miner-v3 loop") then
    Print("[CAP WARNING] stopping early at window ", windowId, "\n");
    break;
  fi;
od;

t1 := GAPLIB_WallElapsedMs();
Print("Done: matched=", countMatched, " (of 26 expected) elapsed_ms=", t1 - t0, "\n");

if countMatched <> Length(OPEN_WINDOW_IDS) then
  RecordSkip("GLOBAL", Concatenation("countMatched=", String(countMatched),
             " != expected 26 -- some hardcoded window ids from v2 were not found by this run's",
             " LINS iteration (index/serial mismatch); check serialByIdx numbering carefully"));
fi;

#############################################################################
## ---------------------- summary + witness highlight -------------------------
#############################################################################
nonCommuteResults := Filtered(RESULTS, r -> IsBound(r.ker_commutes) and (not r.ker_commutes));;
assertFailResults := Filtered(RESULTS, r -> IsBound(r.ta_assert_holds) and (not r.ta_assert_holds));;
unscreenedResults := Filtered(RESULTS, r -> r.status = "UNSCREENED");;

Print("\n=== SUMMARY ===\n");
Print("Total windows processed: ", Length(RESULTS), "\n");
Print("ker(chi-tilde) NONCOMMUTATIVE (real leads, with witness): ", Length(nonCommuteResults), "\n");
for r in nonCommuteResults do
  Print("  LEAD: ", r.window_id, " witness f1_word=", r.witness.f1_word,
        " f2_word=", r.witness.f2_word, "\n");
od;
Print("T-A count-identity assert FAILED (collapse/contamination signal): ", Length(assertFailResults), "\n");
for r in assertFailResults do
  Print("  T-A MISMATCH: ", r.window_id, " shadow_total=", r.shadow_total,
        " ker_size=", r.ker_size, " phi_2Nord=", r.phi_2Nord, "\n");
od;
Print("UNSCREENED (cap or other failure): ", Length(unscreenedResults), "\n");

#############################################################################
## ---------------------- write output --------------------------------------
#############################################################################
outParts := [];;
Add(outParts, "{\n");
Add(outParts, "  \"generated_by\": \"search/wall-miner-v3.g\",\n");
Add(outParts, "  \"note\": \"ker(chi-tilde) shadow-level computation on the 26 v2-OPEN windows; rough lead screening, NOT a ledger claim, no cross-check performed\",\n");
Add(outParts, Concatenation("  \"windows_matched\": ", String(countMatched), ",\n"));
Add(outParts, Concatenation("  \"total_noncommutative_leads\": ", String(Length(nonCommuteResults)), ",\n"));
Add(outParts, Concatenation("  \"total_ta_assert_failed\": ", String(Length(assertFailResults)), ",\n"));
Add(outParts, Concatenation("  \"total_unscreened\": ", String(Length(unscreenedResults)), ",\n"));
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

WriteFile("search/certs/wall_miner_v3_20260729.json", Concatenation(outParts));
Print("Wrote search/certs/wall_miner_v3_20260729.json\n");
Print("ALL_DONE\n");
