#############################################################################
## wall-miner-v4.g -- wall campaign mining track v4 (ruling 166: WCP5-D fix)
##
## Policy unchanged: rough is fine, bugs tolerated, no polish required.
## Asserts are kept (fail-closed is the point of this pass). Output is a
## lead list, NOT a ledger claim, no cross-check performed against an
## independent implementation, no commit, no u (sealed symbol).
##
## Background (docs/notes/wcp5d_resolution_v1.md, search/wcp5d-verify.g):
## the old c-notin-N enumeration predicate (word-level, either "natural" or
## "prepend" convention) is WRONG for windows where tau (x->y, y->z=(xy)^-1)
## does not descend to F2/N_F2 -- which happens whenever c is not in N and
## is the generic case, not an edge case. The true descended maps are
##   theta~ := Ad(Delta),  tau~ := Ad(delta)      (Delta=s1 s2 s1, delta=s1 s2)
## acting on PB3/N (well-defined since N is normal in B3, so conjugation by
## any B3/N element preserves the subgroup PB3/N). The correct (F2) quotient
## rule (no word-level BFS needed at all):
##   f * theta~(f) = 1   AND   tau~^2(y^m f) tau~(y^m f) (y^m f) = c^m   AND
##   <x^u, f^-1 y^u f> = P_N  (generation)
## This script re-enumerates the 17 c-not-in-N windows that wall-miner-v3.g
## left as UNKNOWN (its shadow_total/ker_size/ker_commutes for those 17 were
## computed with the now-superseded word-level predicate).
##
## Also fixed here (v3's secondary bug, noted in wcp5d_resolution_v1.md S5):
## N_ord must be Lcm(ord(x), ord(y), ord(c)), not just ord(x). v3 used
## ord(x) alone; it happened to coincide with ord(c) in v3's own worked
## example (idx192-s4, both 8) but that coincidence is not guaranteed.
##
## For each of the 17 windows this computes:
##   (1) shadow_total = |CorrectedShadows(W, charmingSet)|
##   (2) ker(chi-tilde) (m=0 layer) commutativity -- EXACT, via the actual
##       (3.53) group-of-shadows regular permutation representation
##       (GroupOfShadows below, adapted from wcp5d-verify.g), not a proxy.
##       A witness pair of noncommuting [0,f] shadows is saved if found.
##   (3) T-A count identity assert: |ker| =?= shadow_total / Phi(2*N_ord)
##   (4) (3.53) closure assert (GroupOfShadows.closed)
##
## Output: search/certs/wall_miner_v4_20260729.json
#############################################################################

Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");   # for AbstractProd, PF (not used for the
                                          # superseded word-level enumerators here)

if LoadPackage("lins") <> true then
  Error("Failed to load GAP package LINS.");
fi;

RESULTS := [];;
SKIPLOG := [];;

RecordSkip := function(id, reason)
  Add(SKIPLOG, rec(window_id := id, reason := reason));
  Print("[SKIP] ", id, " :: ", reason, "\n");
end;;

# the 17 c-notin-N windows from wall-miner-v3.g flagged UNKNOWN per
# docs/notes/wcp5d_resolution_v1.md S "再計算対象" list
TARGET_WINDOW_IDS := [
  "W-A-B3idx96-s2", "W-A-B3idx96-s4",
  "W-A-B3idx108-s1",
  "W-A-B3idx120-s2",
  "W-A-B3idx144-s1", "W-A-B3idx144-s3", "W-A-B3idx144-s4", "W-A-B3idx144-s6",
  "W-A-B3idx162-s2", "W-A-B3idx162-s3", "W-A-B3idx162-s4",
  "W-A-B3idx168-s2",
  "W-A-B3idx192-s2", "W-A-B3idx192-s3", "W-A-B3idx192-s4", "W-A-B3idx192-s5",
  "W-A-B3idx192-s6"
];;

#############################################################################
## ---------------------- (F2) machinery, adapted from search/wcp5d-verify.g -
#############################################################################
# MakeWindow: given images (s1,s2) of B3's own generators (sigma1,sigma2) in
# some finite permutation quotient, build every derived quantity needed.
# N_ord FIX (this script, per ruling 166): Lcm of all three orders, not just
# ord(x) (v3's bug).
MakeWindow := function(s1, s2)
  local xx, yy, DD, dd, cc, zz;
  xx := s1^2;  yy := s2^2;
  DD := AbstractProd([s1, s2, s1]);  dd := AbstractProd([s1, s2]);
  cc := DD^2;  zz := AbstractProd([xx, yy])^-1;
  return rec(s1 := s1, s2 := s2, x := xx, y := yy, Dlt := DD, dlt := dd, c := cc, z := zz,
             Bq := Group(s1, s2), PN := Group(xx, yy),
             Nord := Lcm(Order(xx), Order(yy), Order(cc)));
end;;

# tau~ = Ad(delta), theta~ = Ad(Delta) -- always well-defined on Bq (and hence on the
# PB3/N-subgroup PN, since N is normal in B3) because conjugation is an inner automorphism
# of the whole ambient group Bq=B3/N.
TT := function(W, g) return AbstractProd([W.dlt, g, W.dlt^-1]); end;;
TH := function(W, g) return AbstractProd([W.Dlt, g, W.Dlt^-1]); end;;
RtOf := function(W, m, f)
  local Wd;
  Wd := AbstractProd([W.y^m, f]);
  return AbstractProd([TT(W, TT(W, Wd)), TT(W, Wd), Wd]);
end;;

# (F2) quotient rule -- no word-level BFS, no c_in_N/c_notin_N branch needed at all
# (degenerates correctly to the old quotient-shortcut when c=1).
CorrectedShadows := function(W, charmingSet)
  local out, f, m, u;
  out := [];
  for f in Elements(DerivedSubgroup(W.PN)) do
    if AbstractProd([f, TH(W, f)]) <> Identity(W.Bq) then continue; fi;
    for m in charmingSet do
      u := 2*m + 1;
      if RtOf(W, m, f) <> W.c^m then continue; fi;
      if Size(Group(W.x^u, AbstractProd([f^-1, W.y^u, f]))) <> Size(W.PN) then continue; fi;
      Add(out, [m, f]);
    od;
  od;
  return Set(out);
end;;

# (3.53) closure + regular permutation representation of G_N = GTSh(N,N), built directly
# from the shadow-composition law (not a proxy): elements are S (a list of [m,f] pairs),
# multiplication table computed via the composition formula, then read off as permutations
# of the shadow-index set. ker = the subgroup generated by the m=0 layer's permutations.
GroupOfShadows := function(W, S)
  local n, i, j, m1, f1, u1, Eh, nm, nf, p, closed, regs, GT, kerIdx;
  n := Length(S);  closed := true;  regs := [];
  for i in [1 .. n] do
    m1 := S[i][1];  f1 := S[i][2];  u1 := 2*m1 + 1;
    Eh := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y],
            [W.x^u1, AbstractProd([f1^-1, W.y^u1, f1])]);
    if Eh = fail then return rec(closed := false, note := "E hom fail"); fi;
    regs[i] := [];
    for j in [1 .. n] do
      nm := (2*m1*S[j][1] + m1 + S[j][1]) mod W.Nord;
      nf := AbstractProd([f1, Image(Eh, S[j][2])]);
      p := Position(S, [nm, nf]);
      if p = fail then closed := false; regs[i][j] := 1; else regs[i][j] := p; fi;
    od;
  od;
  if not closed then return rec(closed := false); fi;
  regs := List(regs, PermList);
  GT := Group(regs);
  kerIdx := Filtered([1 .. n], i -> S[i][1] = 0);
  return rec(closed := true, G := GT, order := Size(GT), regs := regs,
             ker := Group(List(kerIdx, i -> regs[i])), ker_idx := kerIdx);
end;;

# find a witness pair of noncommuting m=0 shadows (first found, exact -- via the actual
# regular-permutation composition, not a proxy) -- fail if the ker subgroup is abelian.
FindKerWitness := function(S, regs, kerIdx)
  local i, j;
  for i in [1 .. Length(kerIdx)] do
    for j in [i+1 .. Length(kerIdx)] do
      if regs[kerIdx[i]] * regs[kerIdx[j]] <> regs[kerIdx[j]] * regs[kerIdx[i]] then
        return rec(f1 := S[kerIdx[i]][2], f2 := S[kerIdx[j]][2]);
      fi;
    od;
  od;
  return fail;
end;;

# ================= JSON serialization =================
WitnessJson := function(w)
  if w = fail then return "null"; fi;
  # word representation not tracked here (F2 rule is word-free); record the group
  # elements themselves via their permutation image string as the witness coordinate.
  return Concatenation("{\"m1\":0,\"f1_perm\":", JStr(String(w.f1)),
                        ",\"m2\":0,\"f2_perm\":", JStr(String(w.f2)), "}");
end;;

ResultJson := function(r)
  return Concatenation("  {\n",
    "    \"window_id\":", JStr(r.window_id), ",\n",
    "    \"c_in_N\":", JB(r.c_in_N), ",\n",
    "    \"abs_Bq\":", String(r.abs_Bq), ",\n",
    "    \"abs_PN\":", String(r.abs_PN), ",\n",
    "    \"N_ord\":", String(r.N_ord), ",\n",
    "    \"charming_count\":", String(r.charming_count), ",\n",
    "    \"status\":", JStr(r.status), ",\n",
    "    \"shadow_total\":", String(r.shadow_total), ",\n",
    "    \"ker_size\":", String(r.ker_size), ",\n",
    "    \"phi_2Nord\":", String(r.phi_2Nord), ",\n",
    "    \"ta_predicted_ker\":", String(r.ta_predicted_ker), ",\n",
    "    \"ta_assert_holds\":", JB(r.ta_assert_holds), ",\n",
    "    \"closure_353_holds\":", JB(r.closure_353_holds), ",\n",
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

#############################################################################
## ---------------------- process each of the 17 target windows -------------
#############################################################################
Print("=== wall-miner-v4: (F2) quotient-rule re-enumeration of the 17 c-notin-N windows ===\n");
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

  if not (windowId in TARGET_WINDOW_IDS) then
    continue;
  fi;
  countMatched := countMatched + 1;

  r := rec(window_id := windowId);

  # NOTE: unlike v1/v2/v3, we build the natural hom from the FULL B3 (not just PB3),
  # so that s1,s2 (the sigma1,sigma2 markings) are preserved -- (F2) needs Delta,delta
  # which live in B3/N generally, not in PB3/N.
  hm := NaturalHomomorphismByNormalSubgroup(B3, N);;
  isoQ := IsomorphismPermGroup(Image(hm));;
  s1 := Image(isoQ, Image(hm, ga));;
  s2 := Image(isoQ, Image(hm, gb));;

  W := MakeWindow(s1, s2);;
  r.abs_Bq := Size(W.Bq);
  r.abs_PN := Size(W.PN);
  r.c_in_N := (W.c = Identity(W.Bq));
  r.N_ord := W.Nord;
  charmingSet := Filtered([0 .. W.Nord - 1], m -> Gcd(2*m+1, W.Nord) = 1);;
  r.charming_count := Length(charmingSet);
  r.phi_2Nord := Phi(2 * W.Nord);

  Print("--- ", windowId, "  |B3/N|=", r.abs_Bq, " |P_N|=", r.abs_PN, " c_in_N=", r.c_in_N,
        " N_ord=", r.N_ord, " |charming|=", r.charming_count, "\n");

  if r.c_in_N then
    RecordSkip(windowId, "unexpected: this window is listed as c_notin_N in wcp5d_resolution_v1.md but c_in_N came out true here -- check index/serial alignment");
  fi;

  if GAPLIB_CheckCap(400.0, windowId) then
    r.status := "UNSCREENED"; r.shadow_total := -1; r.ker_size := -1;
    r.ta_predicted_ker := -1; r.ta_assert_holds := false;
    r.closure_353_holds := false; r.ker_commutes := false; r.witness := fail;
    r.note := "cap exceeded before enumeration completed, left UNSCREENED";
    Add(RESULTS, r);
    RecordSkip(windowId, "cap exceeded, UNSCREENED");
    continue;
  fi;

  corr := CorrectedShadows(W, charmingSet);;
  r.shadow_total := Length(corr);
  kerList := Filtered(corr, k -> k[1] = 0);;
  r.ker_size := Length(kerList);

  # ---- T-A count identity assert ----
  if r.phi_2Nord = 0 then
    r.ta_predicted_ker := -1; r.ta_assert_holds := false;
  elif r.shadow_total mod r.phi_2Nord <> 0 then
    r.ta_predicted_ker := -1; r.ta_assert_holds := false;
  else
    r.ta_predicted_ker := r.shadow_total / r.phi_2Nord;
    r.ta_assert_holds := (r.ta_predicted_ker = r.ker_size);
  fi;

  # ---- (3.53) closure + exact ker commutativity ----
  gi := GroupOfShadows(W, corr);;
  r.closure_353_holds := gi.closed;
  if gi.closed then
    r.ker_commutes := IsAbelian(gi.ker);
    if r.ker_commutes then
      r.witness := fail;
    else
      r.witness := FindKerWitness(corr, gi.regs, gi.ker_idx);
    fi;
    r.note := Concatenation("|GTSh|=", String(gi.order));
  else
    r.ker_commutes := false;
    r.witness := fail;
    r.note := "(3.53) closure FAILED -- E hom fail or shadow set not closed under composition";
  fi;
  r.status := "computed";

  Print("    shadow_total=", r.shadow_total, " ker_size=", r.ker_size,
        " phi(2*N_ord)=", r.phi_2Nord, " ta_predicted=", r.ta_predicted_ker,
        " ta_holds=", r.ta_assert_holds, " closure=", r.closure_353_holds,
        " ker_commutes=", r.ker_commutes, "\n");

  Add(RESULTS, r);

  if GAPLIB_CheckCap(500.0, "wall-miner-v4 loop") then
    Print("[CAP WARNING] stopping early at window ", windowId, "\n");
    break;
  fi;
od;

t1 := GAPLIB_WallElapsedMs();
Print("Done: matched=", countMatched, " (of 17 expected) elapsed_ms=", t1 - t0, "\n");

if countMatched <> Length(TARGET_WINDOW_IDS) then
  RecordSkip("GLOBAL", Concatenation("countMatched=", String(countMatched),
             " != expected 17 -- some hardcoded window ids were not found by this run's",
             " LINS iteration; check serialByIdx numbering carefully"));
fi;

#############################################################################
## ---------------------- summary --------------------------------------------
#############################################################################
nonCommuteResults := Filtered(RESULTS, r -> IsBound(r.ker_commutes) and (not r.ker_commutes)
                                             and r.status = "computed");;
assertFailResults := Filtered(RESULTS, r -> IsBound(r.ta_assert_holds) and (not r.ta_assert_holds)
                                             and r.status = "computed");;
closureFailResults := Filtered(RESULTS, r -> IsBound(r.closure_353_holds) and (not r.closure_353_holds)
                                              and r.status = "computed");;
unscreenedResults := Filtered(RESULTS, r -> r.status = "UNSCREENED");;

Print("\n=== SUMMARY ===\n");
Print("Total windows processed: ", Length(RESULTS), "\n");
Print("ker(chi-tilde) NONCOMMUTATIVE (real leads, with witness): ", Length(nonCommuteResults), "\n");
for r in nonCommuteResults do
  Print("  LEAD: ", r.window_id, " witness f1=", r.witness.f1, " f2=", r.witness.f2, "\n");
od;
Print("T-A count-identity assert FAILED: ", Length(assertFailResults), "\n");
for r in assertFailResults do
  Print("  T-A MISMATCH: ", r.window_id, " shadow_total=", r.shadow_total,
        " ker_size=", r.ker_size, " phi_2Nord=", r.phi_2Nord, "\n");
od;
Print("(3.53) closure FAILED: ", Length(closureFailResults), "\n");
for r in closureFailResults do
  Print("  CLOSURE FAIL: ", r.window_id, "\n");
od;
Print("UNSCREENED: ", Length(unscreenedResults), "\n");

#############################################################################
## ---------------------- write output --------------------------------------
#############################################################################
outParts := [];;
Add(outParts, "{\n");
Add(outParts, "  \"generated_by\": \"search/wall-miner-v4.g\",\n");
Add(outParts, "  \"note\": \"(F2) quotient-rule re-enumeration of the 17 c-notin-N windows per docs/notes/wcp5d_resolution_v1.md (ruling 166); rough lead screening, NOT a ledger claim, no cross-check performed\",\n");
Add(outParts, Concatenation("  \"windows_matched\": ", String(countMatched), ",\n"));
Add(outParts, Concatenation("  \"total_noncommutative_leads\": ", String(Length(nonCommuteResults)), ",\n"));
Add(outParts, Concatenation("  \"total_ta_assert_failed\": ", String(Length(assertFailResults)), ",\n"));
Add(outParts, Concatenation("  \"total_closure_failed\": ", String(Length(closureFailResults)), ",\n"));
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

WriteFile("search/certs/wall_miner_v4_20260729.json", Concatenation(outParts));
Print("Wrote search/certs/wall_miner_v4_20260729.json\n");
Print("ALL_DONE\n");
