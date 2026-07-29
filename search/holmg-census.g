#############################################################################
## search/holmg-census.g -- HOL-MG census driver (implementer, レーン B-3 /
## I11-C).
##
## Machine census of the candidate proposition HOL-MG:
##   GTSh/(GTSh)'' =? Hol(Z/N_ord) x (elementary abelian 2-group)
## over every window in the repo for which GTSh is (re)computable.
##
## For each window: rebuild s1,s2 (B3-generator images) from the SAME raw
## data (a1/b1 generating pairs, or S/T matrices for the PSL family) already
## recorded in the existing strike-*.g / week3-psl-*.g drivers, then
## reconstruct GTSh from scratch via kerchi-judge.g's MakeWindow /
## CorrectedShadows / GroupOfShadows (the SAME judging machinery those
## drivers use -- NOT a copy of any cert's recorded isotropy_order/idgroup
## field). G'' = second derived subgroup, Q := G/G''. IdGroup(Q) is compared
## against IdGroup(Hol(Z/N_ord) x C2^k) for the (unique, order-forced) k.
##
## No interpretation performed here (that is the coordinator's exclusive
## authority per the task instructions). ideas/ not read. Not committed.
##
## Output: search/certs/holmg_census_20260730.json
#############################################################################

Read("search/gaplib_common.g");
JUDGE_LIBRARY_ONLY := true;;
JUDGE_SKIP_LEGACY_CROSSCHECK := true;;
Read("search/kerchi-judge.g");        # MakeWindow, CorrectedShadows(Xi/Legacy), GroupOfShadows,
                                       # AbstractProd, BuildQTGeneral (via week3-battery-common.g)
Read("search/week3-psl-common.g");    # MakeMat, MatToPerm, MakeMatGF8, MatToPermGF8, PF

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

#############################################################################
## ---------------------- window builders ------------------------------------
#############################################################################

# AxS3 embedding (search/strike-a16.g / a18.g / a20.g pattern): a1,b1 in
# AlternatingGroup(n) (both known even here), E = A_n x S3.
BuildS1S2_AxS3 := function(a1, b1, n)
  local An, S3, Dgrp, embA, embS, agen, bgen;
  An := AlternatingGroup(n);;  S3 := SymmetricGroup(3);;
  Dgrp := DirectProduct(An, S3);;
  embA := Embedding(Dgrp, 1);;  embS := Embedding(Dgrp, 2);;
  agen := Image(embA, a1) * Image(embS, (1,3));;
  bgen := Image(embA, b1) * Image(embS, (1,3,2));;
  return rec(s1 := bgen^-1 * agen, s2 := agen^-1 * bgen^2);
end;;

# SymmetricGroup(n) x S3 embedding (search/strike-a13-ladder.g /
# search/strike-i10-1.g pattern): a1 may be odd, so S_n (not A_n) is used.
BuildS1S2_SxS3 := function(a1, b1, n)
  local Sn, S3, Dgrp, embA, embS, agen, bgen;
  Sn := SymmetricGroup(n);;  S3 := SymmetricGroup(3);;
  Dgrp := DirectProduct(Sn, S3);;
  embA := Embedding(Dgrp, 1);;  embS := Embedding(Dgrp, 2);;
  agen := Image(embA, a1) * Image(embS, (1,3));;
  bgen := Image(embA, b1) * Image(embS, (1,3,2));;
  return rec(s1 := bgen^-1 * agen, s2 := agen^-1 * bgen^2);
end;;

# PSL/PGL family (search/week3-psl-S1.g / S3.g / S4.g / S5.g pattern):
# S,T matrices -> w=S*T^-1, X=w^2, Y=S^-1*X*S, Gg=<X,Y>, then s1,s2 via the
# SAME BuildQTGeneral (QxT model) those scripts already use for the PU-F6
# exact-order check -- reused here as genuine B3-generator images.
BuildS1S2_PSL := function(Sperm, Tperm)
  local wPerm, Xperm, Yperm, Gg, qt;
  wPerm := Sperm * Tperm^-1;;
  Xperm := wPerm^2;;
  Yperm := Sperm^-1 * Xperm * Sperm;;
  Gg := Group(Xperm, Yperm);;
  qt := BuildQTGeneral(Gg, Xperm, Yperm, ());;
  return rec(s1 := qt.s1, s2 := qt.s2);
end;;

#############################################################################
## ---------------------- window table (raw generator data transcribed from
##   the existing drivers -- see per-window comment for the source file) ----
#############################################################################
WINDOWS := [];;

# ---- strike-a16.g / strike-a18.g / strike-a20.g (AxS3) ----
Add(WINDOWS, rec(id := "W-D-A16-11a", family := "AxS3", n := 16,
  a1 := ( 1, 2)( 3,14)( 4,10)( 5,12)( 6, 8)( 7,16)( 9,13)(11,15),
  b1 := ( 2,11,14)( 3,15,10)( 4, 9,12)( 5,13, 8)( 6, 7,16),
  source := "search/strike-a16.g"));
Add(WINDOWS, rec(id := "W-D-A18-13a", family := "AxS3", n := 18,
  a1 := ( 1,17)( 2, 6)( 3,14)( 5,15)( 7,16)( 8,13)(10,12)(11,18),
  b1 := ( 1,16, 6)( 2, 5,14)( 3,15, 4)( 7,17,13)( 8,12, 9)(10,11,18),
  source := "search/strike-a18.g"));
Add(WINDOWS, rec(id := "W-D-A20-15a", family := "AxS3", n := 20,
  a1 := ( 1, 7)( 2,16)( 3, 5)( 4,20)( 6,17)( 8, 9)(10,15)(11,19)(12,13)(14,18),
  b1 := ( 1, 6,16)( 2,17, 5)( 3, 4,20)( 7,15, 9)(10,14,19)(11,18,13),
  source := "search/strike-a20.g"));

# ---- strike-a13-ladder.g (SxS3), 13 windows (4 canonical + 9 siblings) ----
A13_CANON := [
  rec(id := "W-E-A10-9t1", n := 10, t := 1,
      a1 := ( 1, 2)( 3, 5)( 4,10)( 6, 9), b1 := ( 2, 9, 5)( 3, 4,10)( 6, 8, 7)),
  rec(id := "W-E-A11-9t2", n := 11, t := 2,
      a1 := ( 2,11)( 3, 8)( 4, 5)( 6, 7)( 9,10), b1 := ( 1, 9,11)( 2,10, 8)( 3, 7, 5)),
  rec(id := "W-E-A12-9t3", n := 12, t := 3,
      a1 := ( 3, 9)( 4,11)( 5, 7)( 6,12)( 8,10), b1 := ( 1, 9, 2)( 3, 8,11)( 4,10, 7)( 5, 6,12)),
  rec(id := "W-E-A13-9t4", n := 13, t := 4,
      a1 := ( 2,10)( 3, 8)( 4,12)( 5, 6)( 7,13)( 9,11), b1 := ( 1, 9,10)( 2,11, 8)( 3, 7,12)( 4,13, 6)),
];;
A13_W0_BY_T := rec();;
for cw in A13_CANON do
  A13_W0_BY_T.(Concatenation("t", String(cw.t))) := cw.b1^-1 * cw.a1;
od;;
A13_SIBS := [
  rec(id := "W-E-A10-9t1-o2", n := 10, t := 1, a1 := ( 3, 9)( 4, 6)( 5,10)( 7, 8)),
  rec(id := "W-E-A10-9t1-o3", n := 10, t := 1, a1 := ( 2, 3)( 4, 9)( 6, 8)( 7,10)),
  rec(id := "W-E-A10-9t1-o4", n := 10, t := 1, a1 := ( 2, 3)( 4, 9)( 5, 7)( 6,10)),
  rec(id := "W-E-A10-9t1-o5", n := 10, t := 1, a1 := ( 2, 4)( 3,10)( 5, 9)( 6, 7)),
  rec(id := "W-E-A10-9t1-o6", n := 10, t := 1, a1 := ( 2, 6)( 3, 4)( 7, 9)( 8,10)),
  rec(id := "W-E-A11-9t2-o2", n := 11, t := 2, a1 := ( 2, 3)( 4, 9)( 5,10)( 6, 7)( 8,11)),
  rec(id := "W-E-A11-9t2-o3", n := 11, t := 2, a1 := ( 2, 7)( 3,10)( 4, 5)( 6,11)( 8, 9)),
  rec(id := "W-E-A12-9t3-o2", n := 12, t := 3, a1 := ( 2, 4)( 3,12)( 5, 9)( 6,10)( 8,11)),
  rec(id := "W-E-A12-9t3-o3", n := 12, t := 3, a1 := ( 2, 6)( 3,10)( 5,11)( 7, 9)( 8,12)),
];;
for sw in A13_SIBS do
  sw.b1 := sw.a1 * A13_W0_BY_T.(Concatenation("t", String(sw.t)))^-1;
od;;
for w in Concatenation(A13_CANON, A13_SIBS) do
  Add(WINDOWS, rec(id := w.id, family := "SxS3", n := w.n, a1 := w.a1, b1 := w.b1,
      source := "search/strike-a13-ladder.g"));
od;;

# ---- strike-i10-1.g (SxS3), 2 windows ----
Add(WINDOWS, rec(id := "W-E-A10-5x2t0", family := "SxS3", n := 10,
  a1 := ( 1, 2)( 3, 6)( 7,10), b1 := ( 2,10, 6)( 3, 5, 4)( 7, 9, 8),
  source := "search/strike-i10-1.g"));
Add(WINDOWS, rec(id := "W-E-A15-5x3t0", family := "SxS3", n := 15,
  a1 := ( 1, 4)( 5, 9)( 6,15)( 7,13)( 8,11), b1 := ( 1, 3, 2)( 4,10, 9)( 5, 8,15)( 6,14,13)( 7,12,11),
  source := "search/strike-i10-1.g"));

# ---- week3-psl-S1.g / S3.g / S4.g / S5.g (PSL family) ----
Add(WINDOWS, rec(id := "S1", family := "PSL", q := 7, gf8 := false,
  Smat := MakeMat(7, 2,1,1,5), Tmat := MakeMat(7, 4,0,2,2),
  source := "search/week3-psl-S1.g"));
Add(WINDOWS, rec(id := "S3", family := "PSL", q := 8, gf8 := true,
  SmatGF8 := MakeMatGF8(1,0,1,1), TmatGF8 := MakeMatGF8(4,2,4,5),
  source := "search/week3-psl-S3.g"));
Add(WINDOWS, rec(id := "S4", family := "PSL", q := 8, gf8 := true,
  SmatGF8 := MakeMatGF8(1,0,1,1), TmatGF8 := MakeMatGF8(4,3,1,5),
  source := "search/week3-psl-S4.g"));
Add(WINDOWS, rec(id := "S5", family := "PSL", q := 11, gf8 := false,
  Smat := MakeMat(11, 1,1,1,10), Tmat := MakeMat(11, 9,1,8,1),
  source := "search/week3-psl-S5.g"));

Print("Inventory: ", Length(WINDOWS), " windows to census:\n");
for w in WINDOWS do
  Print("  ", w.id, "  (family=", w.family, ", source=", w.source, ")\n");
od;;

#############################################################################
## ---------------------- HOL-MG check per window -----------------------------
#############################################################################
# Hol(Z/N) built EXPLICITLY as a permutation group on N points {1..N} (point
# i <-> residue i-1 mod N): the affine maps x -> a*x+b mod N, gcd(a,N)=1,
# b in Z/N. No GAP library Holomorph()/SemidirectProduct() shortcut used for
# the CONSTRUCTION -- IdGroup is only read off the resulting permutation
# group afterwards. (GAP's core library has no top-level Holomorph() function
# in this install -- confirmed by "Variable: 'Holomorph' must have an
# assigned value" on first run; this explicit affine-map construction avoids
# depending on it.)
HolCyclic := function(N)
  local units, a, b, gens, images, x, ax;
  units := Filtered([1 .. N], a -> Gcd(a, N) = 1);;
  gens := [];;
  for a in units do
    for b in [0 .. N-1] do
      images := [];;
      for x in [0 .. N-1] do
        ax := (a*x + b) mod N;;
        images[x+1] := ax + 1;;
      od;;
      Add(gens, PermList(images));;
    od;;
  od;;
  return Group(gens);;
end;;

IdGroupOrDesc := function(G)
  if SmallGroupsAvailable(Size(G)) then
    return rec(has_idgroup := true, idgroup := IdGroup(G));
  else
    return rec(has_idgroup := false,
               structure_description := StructureDescription(G),
               order := Size(G));
  fi;
end;;

CensusWindow := function(w)
  local built, s1, s2, W, charmingSet, corrRes, corr, gi, G, Gpp, natGQ, Q,
        Nord, holBase, holOrder, ratio, k, isPow2, candidate, candIdG, qIdG,
        matchK, mismatchReason, r;
  r := rec(id := w.id, source := w.source, family := w.family);;

  if w.family = "AxS3" then
    built := BuildS1S2_AxS3(w.a1, w.b1, w.n);;
  elif w.family = "SxS3" then
    built := BuildS1S2_SxS3(w.a1, w.b1, w.n);;
  elif w.family = "PSL" then
    if w.gf8 then
      built := BuildS1S2_PSL(MatToPermGF8(w.SmatGF8), MatToPermGF8(w.TmatGF8));;
    else
      built := BuildS1S2_PSL(MatToPerm(w.q, w.Smat), MatToPerm(w.q, w.Tmat));;
    fi;
  else
    Error("holmg-census.g: unknown family ", w.family);
  fi;
  s1 := built.s1;;  s2 := built.s2;;

  if AbstractProd([s1, s2, s1]) <> AbstractProd([s2, s1, s2]) then
    r.error := "braid relation FAILS for reconstructed s1,s2 -- refusing to judge";
    Print("[FAIL] ", w.id, ": ", r.error, "\n");
    return r;
  fi;

  W := MakeWindow(s1, s2);;
  Nord := W.Nord;;
  r.N_ord := Nord;;
  charmingSet := Filtered([0 .. Nord - 1], m -> Gcd(2*m+1, Nord) = 1);;

  JUDGE_FORCE_SCAN_MODE := "xi_restricted";;
  corrRes := CorrectedShadows(W, charmingSet);;
  corr := corrRes.shadows;;
  r.shadow_total := Length(corr);;
  r.settled_fail_count := corrRes.settled_fail_count;;

  gi := GroupOfShadows(W, corr);;
  if not gi.closed then
    r.error := "(3.53) closure FAILED -- refusing to report structure of a group not confirmed to exist";
    Print("[FAIL] ", w.id, ": ", r.error, "\n");
    return r;
  fi;
  G := gi.G;;
  r.abs_G := Size(G);;

  Gpp := DerivedSubgroup(DerivedSubgroup(G));;
  r.abs_Gpp := Size(Gpp);;
  natGQ := NaturalHomomorphismByNormalSubgroup(G, Gpp);;
  Q := Image(natGQ);;
  r.abs_Q := Size(Q);;
  qIdG := IdGroupOrDesc(Q);;
  r.Q_idgroup := qIdG;;

  # Hol(Z/N_ord) order = N_ord * phi(N_ord). Compute exactly (no library
  # IdGroup shortcut) via Holomorph(CyclicGroup(N_ord)).
  holBase := HolCyclic(Nord);;
  holOrder := Size(holBase);;
  r.hol_order := holOrder;;

  if r.abs_Q mod holOrder <> 0 then
    r.hol_c2k_match := "MISMATCH_ORDER";
    r.mismatch_detail := Concatenation("|Q|=", String(r.abs_Q),
      " not a multiple of |Hol(Z/", String(Nord), ")|=", String(holOrder));
    Print("[MISMATCH_ORDER] ", w.id, ": ", r.mismatch_detail, "\n");
    return r;
  fi;

  ratio := r.abs_Q / holOrder;;
  isPow2 := (ratio >= 1) and (2^(LogInt(ratio, 2)) = ratio);;
  if not isPow2 then
    r.hol_c2k_match := "MISMATCH_ORDER";
    r.mismatch_detail := Concatenation("|Q|/|Hol(Z/", String(Nord), ")| = ", String(ratio),
      " is not a power of 2 -- no C2^k candidate has the right order");
    Print("[MISMATCH_ORDER] ", w.id, ": ", r.mismatch_detail, "\n");
    return r;
  fi;

  if ratio = 1 then
    k := 0;;  candidate := holBase;;
  else
    k := LogInt(ratio, 2);;
    candidate := DirectProduct(holBase, ElementaryAbelianGroup(ratio));;
  fi;
  r.candidate_k := k;;
  candIdG := IdGroupOrDesc(candidate);;
  r.candidate_idgroup := candIdG;;

  if qIdG.has_idgroup and candIdG.has_idgroup then
    if qIdG.idgroup = candIdG.idgroup then
      r.hol_c2k_match := Concatenation("MATCH_k", String(k));
      Print("[MATCH k=", k, "] ", w.id, ": IdGroup(G/G'')=", qIdG.idgroup,
            " = IdGroup(Hol(Z/", Nord, ")xC2^", k, ")\n");
    else
      r.hol_c2k_match := "MISMATCH_IDGROUP";
      r.mismatch_detail := Concatenation("orders equal (", String(r.abs_Q),
        ") but IdGroup(G/G'')=", String(qIdG.idgroup), " <> IdGroup(candidate)=",
        String(candIdG.idgroup));
      Print("[MISMATCH_IDGROUP] ", w.id, ": ", r.mismatch_detail, "\n");
    fi;
  else
    # fall back to IsomorphismGroups when IdGroup is unavailable for either side
    if IsomorphismGroups(Q, candidate) <> fail then
      r.hol_c2k_match := Concatenation("MATCH_k", String(k), "_via_IsomorphismGroups");
      Print("[MATCH k=", k, " via IsomorphismGroups] ", w.id, "\n");
    else
      r.hol_c2k_match := "MISMATCH_ISOMORPHISM";
      Print("[MISMATCH_ISOMORPHISM] ", w.id, ": IdGroup unavailable for at least one side and IsomorphismGroups(Q,candidate)=fail\n");
    fi;
  fi;

  return r;
end;;

#############################################################################
## ---------------------- JSON writer -----------------------------------------
#############################################################################
IdGroupOrDescJson := function(rr)
  if rr.has_idgroup then
    return Concatenation("{\"idgroup\":", JPair(rr.idgroup[1], rr.idgroup[2]), "}");
  else
    return Concatenation("{\"structure_description\":", JStr(rr.structure_description),
      ",\"order\":", String(rr.order), "}");
  fi;
end;;

WindowResultJson := function(r)
  local parts;
  parts := [];;
  Add(parts, Concatenation("  {\"id\":", JStr(r.id), ",\"source\":", JStr(r.source),
      ",\"family\":", JStr(r.family)));
  if IsBound(r.error) then
    Add(parts, Concatenation(",\"error\":", JStr(r.error), "}"));
    return Concatenation(parts);
  fi;
  Add(parts, Concatenation(",\"N_ord\":", String(r.N_ord)));
  Add(parts, Concatenation(",\"shadow_total\":", String(r.shadow_total)));
  Add(parts, Concatenation(",\"settled_fail_count\":", String(r.settled_fail_count)));
  Add(parts, Concatenation(",\"abs_G\":", String(r.abs_G)));
  Add(parts, Concatenation(",\"abs_Gpp\":", String(r.abs_Gpp)));
  Add(parts, Concatenation(",\"abs_Q\":", String(r.abs_Q)));
  Add(parts, Concatenation(",\"Q_idgroup\":", IdGroupOrDescJson(r.Q_idgroup)));
  Add(parts, Concatenation(",\"hol_order\":", String(r.hol_order)));
  if IsBound(r.candidate_k) then
    Add(parts, Concatenation(",\"candidate_k\":", String(r.candidate_k)));
    Add(parts, Concatenation(",\"candidate_idgroup\":", IdGroupOrDescJson(r.candidate_idgroup)));
  fi;
  Add(parts, Concatenation(",\"hol_c2k_match\":", JStr(r.hol_c2k_match)));
  if IsBound(r.mismatch_detail) then
    Add(parts, Concatenation(",\"mismatch_detail\":", JStr(r.mismatch_detail)));
  fi;
  Add(parts, "}");
  return Concatenation(parts);
end;;

#############################################################################
## ---------------------- main loop -------------------------------------------
#############################################################################
RESULTS := [];;
for w in WINDOWS do
  Print("\n################################################################\n");
  Print("# HOL-MG census window: ", w.id, " (family=", w.family, ")\n");
  Print("################################################################\n");
  Add(RESULTS, CensusWindow(w));;
od;;

outParts := [];;
Add(outParts, "{\n");
Add(outParts, "  \"generated_by\": \"search/holmg-census.g\",\n");
Add(outParts, "  \"note\": \"HOL-MG machine census -- IdGroup(GTSh/(GTSh)'') vs IdGroup(Hol(Z/N_ord) x C2^k), all windows independently RE-reconstructed from raw generator data (not copied from any existing cert field). No interpretation performed (coordinator's exclusive authority).\",\n");
Add(outParts, Concatenation("  \"windows_censused\": ", String(Length(RESULTS)), ",\n"));
Add(outParts, "  \"windows\": [\n");
for i in [1 .. Length(RESULTS)] do
  Add(outParts, WindowResultJson(RESULTS[i]));
  if i < Length(RESULTS) then Add(outParts, ",\n"); else Add(outParts, "\n"); fi;
od;;
Add(outParts, "  ]\n");
Add(outParts, "}\n");
WriteFile("search/certs/holmg_census_20260730.json", Concatenation(outParts));;
Print("\nWrote search/certs/holmg_census_20260730.json\n");
Print("HOLMG_CENSUS_DONE\n");
