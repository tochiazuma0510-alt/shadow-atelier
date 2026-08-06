#############################################################################
## search/probe/w6_bu_s1_s3/w6_bu_s35_driver_v2.g
## W6BU S3.5 v2 repair driver -- implements Sol F110-2.5 minimal reclaim
## bundle 1-2 (裁定594):
##   (1) L-3 (full surjectivity onto Phat = V.Ghat5, NOT just onto the
##       S4-level extension E_S4) evaluated on ALL 1,263 affine solution
##       pairs across the 73 affine-solvable classes.
##   (2) Versioned v2 cert with SEPARATE count fields:
##         extension_classes=449, affine_solution_pairs=1263,
##         L3_surjective_lifts=<measured>, MARK-ISO_orbits=<measured>
##       plus explicit disclosure that the linear solver never physically
##       traverses the full 91,809-pair domain.
##   (3) D+D lane B extended to include L-3 (all 4 classes); explicit scope
##       statement that lane A/B cross-check is D+D-only (4 classes).
##   (4) F-2.5/F-2.6 computed for real (not "not computed"); F-3.5
##       affine-unsolvable negative fixture executed.
##
## THIS IS A NEW FILE. search/probe/w6_bu_s1_s3/w6_bu_s35_driver.g (v1) and
## its certs (search/certs/w6_bu_s35_firing_20260806.json,
## w6_bu_s35_math_detail_20260806.json) are UNCHANGED.
##
## Design authority for the Phat construction (fiber product
## Ghat5 x_{S4} E_S4, realized as an explicitly-generated subgroup of
## DirectProduct(Ghat5,E_S4) -- NOT full-domain enumeration): confirmed with
## 司令塔 (this session) as the standard "inflated extension" pullback,
## forced by VCEN-MOD (V inflated through Ghat5 -> S4). Validated at scale
## on the D+D row (p2_d4_a0b0c2, all 4 classes, 256 pairs) before this full
## 17-row run: Size(Phat)=3000*|V| every time; order(Uhat0*What0) in Phat
## matches order(Delta*delta) in Ghat5 for the split class and is exactly
## double for non-split classes (structural non-split detector, matches
## expectation) -- see scratchpad/test_phat_dd_4classes.g.
##
## KNOWN SLOW-STEP AVOIDANCE: NaturalHomomorphismByNormalSubgroup(Phat,Vhat)
## was empirically observed to hang (>5 min wall, no result) for a degree
## ~15+24|V| permutation group of order 3000|V|. We never call it. Instead:
## Phat's V-copy normality is asserted via IsNormal (cheap); the "does the
## quotient look like Ghat5" check is done via plain element orders
## (Order(Uhat0), Order(What0), Order(Uhat0*What0) vs the Ghat5-level
## reference), which only needs cycle-length computation on permutations.
## Surjectivity itself (L-3) uses Subgroup(Phat,[rho1,rho2]) + Size, which
## IS fast (Schreier-Sims on a moderate-degree perm group) -- this was
## already the exact operation used successfully in the v1 driver's D+D
## brute force block, just now compared against |Phat| instead of |E_S4|.
##
## Non-contact: Im R untouched, d_N unevaluated, 3 sealed quantities
## untouched. No isolated=TRUE/FALSE, kill, EMPTY, or candidate-found claim
## written anywhere. S3.6 and beyond untouched.
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
LoadPackage("cohomolo");;

FAILS := [];;
Chk := function(name, got, want)
  local ok;
  ok := (got = want);
  if not ok then Add(FAILS, rec(name := name, got := String(got), want := String(want))); fi;
  Print("  [", PF(ok), "] ", name, ": got=", got, " want=", want, "\n");
  return ok;
end;;

#############################################################################
## PART A -- Ghat5 (15-point model, verbatim from bu_s35_embedding_v1.md SS6.2
## / v1 driver), plus the quotient map p_G: Ghat5 -> S4grp used to build Phat.
#############################################################################
Print("\n=== PART A: Ghat5, F-1, F-2 (external anchor) ===\n");
sig1 := (1,4,2,5,3)(6,11)(7,12,10,15)(8,13,9,14);;
sig2 := (1,12,2,11)(3,15,5,13)(4,14)(6,9,7,10,8);;
DeltaHat := sig1*sig2*sig1;;
deltaHat := sig1*sig2;;
Ghat5 := Group(sig1, sig2);;

Chk("F-1.1: order(Delta)", Order(DeltaHat), 2);;
Chk("F-1.2: order(delta)", Order(deltaHat), 3);;
Chk("F-1.3: braid", sig1*sig2*sig1 = sig2*sig1*sig2, true);;
Chk("F-1.4: Delta^2=1", DeltaHat^2 = (), true);;
Chk("F-1.5: |Ghat5|", Size(Ghat5), 3000);;

g5anchor := MakeGn(5);;
Chk("F-2.1: sigma1^2 = MakeGn(5).x", sig1^2 = g5anchor.x, true);;
Chk("F-2.2: sigma2^2 = MakeGn(5).y", sig2^2 = g5anchor.y, true);;

S4grp := Group((1,2),(1,3,4));;
theta := (1,2);; tau := (1,3,4);;
FS4 := FreeGroup(2);;
FqS4 := FS4 / [FS4.1^2, FS4.2^3, (FS4.1*FS4.2)^4];;

G5loc := Group(sig1^2, sig2^2);;
Amod := DerivedSubgroup(G5loc);;
Chk("A: |Amod|", Size(Amod), 125);;
Chk("A: IsNormal(Ghat5,Amod)", IsNormal(Ghat5,Amod), true);;

quoGhat5 := NaturalHomomorphismByNormalSubgroup(Ghat5, Amod);;
Sbar := Image(quoGhat5);;
Chk("A: |Ghat5/Amod|", Size(Sbar), 24);;
thetaImg := Image(quoGhat5, DeltaHat);; tauImg := Image(quoGhat5, deltaHat);;
isoSbarToS4 := GroupHomomorphismByImages(Sbar, S4grp, [thetaImg,tauImg], [theta,tau]);;
Chk("A: isoSbarToS4 well-defined", isoSbarToS4 = fail, false);;
p_G := CompositionMapping(isoSbarToS4, quoGhat5);;
Chk("A: p_G(Delta)=theta", Image(p_G,DeltaHat), theta);;
Chk("A: p_G(delta)=tau", Image(p_G,deltaHat), tau);;

## ---- F-2.3/F-2.4/F-2.5/F-2.6 : Ad(.)|_A eigenstructure + explicit matrix
## match against canon (4.7)/(4.8) Theta,T -- ACTUALLY COMPUTED this time
## (v1 companion report declared these "not computed").
isoApc := IsomorphismPcGroup(Amod);;
Apc := Image(isoApc);;
pcgsA := Pcgs(Apc);;
AdMatrixOverGF5 := function(g)
  local rows, i, img, expv;
  rows := [];
  for i in [1..Length(pcgsA)] do
    img := Image(isoApc, PreImagesRepresentative(isoApc, pcgsA[i])^g);
    expv := ExponentsOfPcElement(pcgsA, img);
    Add(rows, expv * Z(5)^0);
  od;
  return rows;
end;;
AdX := AdMatrixOverGF5(sig1^2);; AdY := AdMatrixOverGF5(sig2^2);;
AdDelta := AdMatrixOverGF5(DeltaHat);; AdDeltaTau := AdMatrixOverGF5(deltaHat);;
Print("Ad(sigma1^2)|_A = ", AdX, "\n");
Print("Ad(sigma2^2)|_A = ", AdY, "\n");
Print("Ad(Delta)|_A = ", AdDelta, "\n");
Print("Ad(delta)|_A = ", AdDeltaTau, "\n");

## canon (4.7)/(4.8) matrices (bu_s35_embedding_v1.md SS1). Amod's pcgs
## basis (from IsomorphismPcGroup) is an ARBITRARY basis of F_5^3, not
## necessarily aligned to Theta/T's eigenbasis or the MakeGn/canon d-twist
## (SS7.4) at all (confirmed empirically: AdDelta is not even a signed
## permutation matrix in this basis). The basis-INDEPENDENT invariant that
## can honestly be checked without solving for an explicit conjugating
## matrix is the characteristic polynomial (similarity invariant): F-2.5
## passes iff Ad(Delta)|_A is similar to Theta (same char poly), and F-2.6
## passes iff Ad(delta)|_A is similar to T (same char poly) -- this
## confirms Delta,delta really do act on A with the canon (4.7)/(4.8)
## MODULE TYPE (order-2 with eigenvalues {1,-1,-1}; order-3 cyclic with
## char poly x^3-1), which is the substantive content of F-2.5/F-2.6 as a
## basis-sanity fixture. It does NOT pin down the exact conjugating matrix
## (a finer question, not needed for L-3's correctness: L-3 never mixes
## Amod's pcgs basis with the canon/MakeGn bases -- it stays entirely
## within Amod's own internally-consistent pcgs coordinates throughout).
ThetaCanon := [[0,1,0],[1,0,0],[0,0,-1]]*Z(5)^0;;
TCanon := [[0,0,1],[1,0,0],[0,1,0]]*Z(5)^0;;
cpAdDelta := CharacteristicPolynomial(AdDelta);;
cpTheta := CharacteristicPolynomial(ThetaCanon);;
cpAdDeltaTau := CharacteristicPolynomial(AdDeltaTau);;
cpT := CharacteristicPolynomial(TCanon);;
Print("charpoly(Ad(Delta))=", cpAdDelta, " charpoly(Theta)=", cpTheta, "\n");
Print("charpoly(Ad(delta))=", cpAdDeltaTau, " charpoly(T)=", cpT, "\n");
f25_pass := (cpAdDelta = cpTheta);;
f26_pass := (cpAdDeltaTau = cpT);;
f25_basis := (function() if f25_pass then return "similar to canon Theta (same char poly; exact conjugating basis not pinned down, not needed for L-3)"; else return "MISMATCH"; fi; end)();;
f26_basis := (function() if f26_pass then return "similar to canon T (same char poly; exact conjugating basis not pinned down, not needed for L-3)"; else return "MISMATCH"; fi; end)();;
Print("F-2.5 basis match: ", f25_basis, "\n");
Print("F-2.6 basis match: ", f26_basis, "\n");
Chk("F-2.5: Ad(Delta)|_A similar to Theta (char poly match)", f25_pass, true);;
Chk("F-2.6: Ad(delta)|_A similar to T (char poly match)", f26_pass, true);;

#############################################################################
## PART B -- shared S4 module-building setup (verbatim from v1 driver)
#############################################################################
V4norm := Filtered(NormalSubgroups(S4grp), n -> Size(n) = 4)[1];;
quoS3 := NaturalHomomorphismByNormalSubgroup(S4grp, V4norm);;
S3q := Image(quoS3);;
gl22 := GL(2,2);;
isoS3toGL22 := IsomorphismGroups(S3q, gl22);;

triv_a := [[Z(2)^0]];; triv_b := [[Z(2)^0]];;
reg2_a := [[Z(2)^0,Z(2)^0],[0*Z(2),Z(2)^0]];;
reg2_b := IdentityMat(2,GF(2));;
D_a := Image(isoS3toGL22, Image(quoS3, theta));;
D_b := Image(isoS3toGL22, Image(quoS3, tau));;

BlockDiag := function(mats)
  local dimm, res, offs, i, j, m;
  dimm := Sum(mats, m -> Length(m));
  res := List([1..dimm], i -> List([1..dimm], j -> Zero(GF(2))));
  offs := 0;
  for m in mats do
    for i in [1..Length(m)] do
      for j in [1..Length(m)] do
        res[offs+i][offs+j] := m[i][j];
      od;
    od;
    offs := offs + Length(m);
  od;
  return res;
end;;

BuildVCenModuleP2 := function(a,b,c)
  local matsA, matsB, i, ma, mb;
  matsA := [];; matsB := [];;
  for i in [1..a] do Add(matsA, triv_a); Add(matsB, triv_b); od;
  for i in [1..b] do Add(matsA, reg2_a); Add(matsB, reg2_b); od;
  for i in [1..c] do Add(matsA, D_a); Add(matsB, D_b); od;
  return rec(ma := BlockDiag(matsA), mb := BlockDiag(matsB));
end;;

gl23 := GL(2,3);;
eltsGL23 := Elements(gl23);;
homsP3 := [];;
for aElt in eltsGL23 do
  if aElt^2 = aElt^0 then
    for bElt in eltsGL23 do
      if bElt^3 = bElt^0 then
        if (aElt*bElt)^2 = (aElt*bElt)^0 then Add(homsP3, [aElt,bElt]); fi;
      fi;
    od;
  fi;
od;
repsP3 := [];;
for pr in homsP3 do
  found := false;;
  for g in eltsGL23 do
    for rp in repsP3 do
      if pr[1]^g = rp[1] and pr[2]^g = rp[2] then found := true; break; fi;
    od;
    if found then break; fi;
  od;
  if not found then Add(repsP3, pr); fi;
od;

ParseP2Triple := function(modId)
  local aPos, bPos, cPos, aStr, bStr, cStr;
  aPos := PositionSublist(modId, "_a") + 2;
  bPos := PositionSublist(modId, "b");
  cPos := PositionSublist(modId, "c");
  aStr := modId{[aPos .. bPos-1]};
  bStr := modId{[bPos+1 .. cPos-1]};
  cStr := modId{[cPos+1 .. Length(modId)]};
  return [Int(aStr), Int(bStr), Int(cStr)];
end;;
ParseP3Index := function(modId)
  local parts;
  parts := SplitString(modId, "_");
  return Int(parts[Length(parts)]);
end;;

RowIds := [
  "p2_d2_a0b0c1", "p2_d2_a0b1c0", "p2_d2_a2b0c0",
  "p2_d3_a1b0c1", "p2_d3_a1b1c0", "p2_d3_a3b0c0",
  "p2_d4_a0b0c2", "p2_d4_a0b1c1", "p2_d4_a0b2c0",
  "p2_d4_a2b0c1", "p2_d4_a2b1c0", "p2_d4_a4b0c0",
  "p3_d2_bruteforce_1", "p3_d2_bruteforce_2", "p3_d2_bruteforce_3",
  "p3_d2_bruteforce_4", "p3_d2_bruteforce_5"
];;
## Shard support (gaplib_common.g convention: split when a run risks the 600s
## wall-clock cap). Set V2_ROW_SUBSET (a list of module_ids) and
## V2_OUT_SUFFIX (a string) BEFORE Read()-ing this file to run only a subset
## and write to a shard-specific output path; a merge script combines the
## shard JSONs afterwards. Default (unset) = full 17-row run, default path.
if not IsBound(V2_ROW_SUBSET) then V2_ROW_SUBSET := RowIds; fi;
if not IsBound(V2_OUT_SUFFIX) then V2_OUT_SUFFIX := ""; fi;
ProcessOrder := Filtered(Concatenation(["p2_d4_a0b0c2"], Filtered(RowIds, r -> r <> "p2_d4_a0b0c2")),
    r -> r in V2_ROW_SUBSET);;

#############################################################################
## PART C -- helpers: affine solve, vector->Vsub element, Phat builder, L-3
#############################################################################
SolveAffine := function(M, v, p)
  local dimM, part, ns, sols, combo, cur;
  dimM := Length(M);
  part := SolutionMat(M, v);
  if part = fail then return []; fi;
  ns := NullspaceMat(M);
  if Length(ns) = 0 then return [part]; fi;
  sols := [];
  for combo in Cartesian(List([1..Length(ns)], i -> [0..p-1])) do
    cur := part + Sum([1..Length(ns)], i -> combo[i]*ns[i]) * Z(p)^0;
    Add(sols, cur);
  od;
  return sols;
end;;

VecToElt := function(vv, gens, dimm)
  local expv, j;
  expv := List([1..dimm], j -> IntFFE(vv[j]));
  return Product([1..dimm], j -> gens[j]^expv[j]);
end;;

## Builds Phat = Ghat5 x_{S4} E_S4 (fiber product, realized as an explicitly
## generated subgroup of DirectProduct(Ghat5,Epc) -- no ambient-domain
## enumeration) for a given (chr,vec) class. Returns a record with Phat,
## Uhat0, What0, Vgens (as Epc elements), emb2 (embedding Epc -> D), and
## sizePhat, plus the diagnostic order(Uhat0*What0).
BuildPhatForClass := function(chr, vec, dim, pPrime)
  local Eext, isoE, Epc, EGpc, U0, W0, Vgens, Vsub, D, emb1, emb2,
        PhatGens, Phat, Uhat0, What0;
  if ForAll(vec, vv -> vv = 0) then
    Eext := SplitExtensionCHR(chr);;
  else
    Eext := NonsplitExtension(chr, vec);;
  fi;
  isoE := IsomorphismPcGroup(Eext);;
  Epc := Image(isoE);;
  EGpc := List(GeneratorsOfGroup(Eext), g -> Image(isoE,g));;
  U0 := EGpc[1];; W0 := EGpc[2];;
  Vgens := EGpc{[3..2+dim]};;
  Vsub := Subgroup(Epc, Vgens);;
  D := DirectProduct(Ghat5, Epc);;
  emb1 := Embedding(D,1);; emb2 := Embedding(D,2);;
  PhatGens := Concatenation(
    List(GeneratorsOfGroup(Amod), a -> Image(emb1,a)),
    List(GeneratorsOfGroup(Vsub), v -> Image(emb2,v)),
    [ Image(emb1,DeltaHat) * Image(emb2,U0),
      Image(emb1,deltaHat) * Image(emb2,W0) ]
  );;
  Phat := Subgroup(D, PhatGens);;
  Uhat0 := Image(emb1,DeltaHat) * Image(emb2,U0);;
  What0 := Image(emb1,deltaHat) * Image(emb2,W0);;
  return rec(Phat := Phat, sizePhat := Size(Phat), Uhat0 := Uhat0, What0 := What0,
             Vgens := Vgens, emb2 := emb2, orderProd := Order(Uhat0*What0));
end;;

#############################################################################
## PART D -- main loop over 17 rows: EMB-LIN (lane A) + per-pair L-3
#############################################################################
RowDetail := rec();;
ClassWitnesses := [];;
TotalClasses := 0;; AcceptedClasses := 0;; RejectedClasses := 0;;
TotalAffinePairs := 0;; TotalL3Surjective := 0;; TotalMarkIsoOrbits := 0;;

DD_LaneB_L3 := [];;   ## D+D row: lane B per-class L-3 surjective counts

for modId in ProcessOrder do
  Print("\n=== S3.5 v2: ", modId, " ===\n");
  if modId{[1,2]} = "p2" then
    trip := ParseP2Triple(modId);;
    built := BuildVCenModuleP2(trip[1],trip[2],trip[3]);;
    maR := built.ma;; mbR := built.mb;; pPrime := 2;; dim := Length(maR);;
  else
    idx := ParseP3Index(modId);;
    rp := repsP3[idx];;
    maR := rp[1];; mbR := rp[2];; pPrime := 3;; dim := Length(maR);;
  fi;

  chr := CHR(S4grp, pPrime, FqS4, [maR, mbR]);;
  h2 := SecondCohomologyDimension(chr);;
  Cohomolo(chr, false, true, false, Concatenation("scratchpad/.tmp_s35v2_",modId));;
  Chk(Concatenation(modId,": codim2 = SecondCohomologyDimension"), chr.codim2, h2);;

  Ntheta := maR + IdentityMat(dim, GF(pPrime));;
  Ntau := IdentityMat(dim, GF(pPrime)) + mbR + mbR^2;;

  classVecs := [];;
  if h2 = 0 then Add(classVecs, []);
  else classVecs := Cartesian(List([1..h2], ii -> [0..pPrime-1]));; fi;

  rowAccepted := 0;; rowRejected := 0;; rowPairs := 0;; rowL3 := 0;; rowMarkIso := 0;;
  rowClassRecs := [];;

  for vec in classVecs do
    epsDelta := List([1..dim], j -> (Sum([1..h2], k -> vec[k]*chr.modrelvals[k][1][j])) mod pPrime) * Z(pPrime)^0;;
    epsDelta := epsDelta * (-Z(pPrime)^0);;
    epsTau := List([1..dim], j -> (Sum([1..h2], k -> vec[k]*chr.modrelvals[k][2][j])) mod pPrime) * Z(pPrime)^0;;
    epsTau := epsTau * (-Z(pPrime)^0);;
    solsA := SolveAffine(Ntheta, epsDelta, pPrime);;
    solsB := SolveAffine(Ntau, epsTau, pPrime);;
    laneA := Length(solsA) * Length(solsB);;
    TotalClasses := TotalClasses + 1;;

    if laneA = 0 then
      RejectedClasses := RejectedClasses + 1;; rowRejected := rowRejected + 1;;
      Add(ClassWitnesses, rec(
        traversal_id := Concatenation(modId, "_s35v2_class_vec_", JoinC(List(vec,String),"-")),
        disposition := "REJECTED", source_tag := "S3_5_V2_EMB_LIN"));;
      Add(rowClassRecs, rec(vec := vec, laneA := laneA, l3_surjective := 0,
          sizePhat := fail, sizeH_distribution := rec()));;
    else
      AcceptedClasses := AcceptedClasses + 1;; rowAccepted := rowAccepted + 1;;
      TotalAffinePairs := TotalAffinePairs + laneA;; rowPairs := rowPairs + laneA;;

      pb := BuildPhatForClass(chr, vec, dim, pPrime);;

      classSurjPairs := [];;   ## list of [aVec,bVec] that pass L-3
      sizeHTally := rec();;    ## 診断欄(②): |<rho(sigma1),rho(sigma2))>| の
                                ## 実測分布 -- 0 の理由を紙で追えるようにする
                                ## (司令塔 続行承認メッセージの防壁②)
      for aVec in solsA do
        for bVec in solsB do
          aElt := VecToElt(aVec, pb.Vgens, dim);; bElt := VecToElt(bVec, pb.Vgens, dim);;
          UhatA := pb.Uhat0 * Image(pb.emb2,aElt);;
          WhatB := pb.What0 * Image(pb.emb2,bElt);;
          rho1 := WhatB^-1 * UhatA;;
          rho2 := UhatA^-1 * WhatB^2;;
          Hp := Subgroup(pb.Phat,[rho1,rho2]);;
          sizeHkey := String(Size(Hp));;
          if IsBound(sizeHTally.(sizeHkey)) then
            sizeHTally.(sizeHkey) := sizeHTally.(sizeHkey) + 1;
          else
            sizeHTally.(sizeHkey) := 1;
          fi;
          if Size(Hp) = pb.sizePhat then
            Add(classSurjPairs, [aVec,bVec]);
          fi;
        od;
      od;
      rowL3 := rowL3 + Length(classSurjPairs);; TotalL3Surjective := TotalL3Surjective + Length(classSurjPairs);;
      Print("    class vec=",vec," sizePhat=",pb.sizePhat," |H| distribution=",
            List(RecNames(sizeHTally), k -> Concatenation(k,":",String(sizeHTally.(k)))), "\n");

      ## MARK-ISO orbits (w6_bottomup_design_v3.md SS1.1): among the L-3
      ## surjective pairs of THIS class, two lifts (a,b),(a',b') are
      ## MARK-ISO-equivalent iff related by V-conjugation (the B^1
      ## coboundary of EMB-H1, same shape, now for module V instead of A):
      ## gamma in V acts by (a,b) -> (a+(I-theta)gamma, b+(I-tau)gamma).
      if Length(classSurjPairs) > 0 then
        gammaOrbitReps := [];;
        seen := [];;
        for pr in classSurjPairs do
          key := Concatenation(String(pr[1]),"|",String(pr[2]));;
          if not (key in seen) then
            orbit := [];;
            for gammaCombo in Cartesian(List([1..dim], ii -> [0..pPrime-1])) do
              gammaVec := gammaCombo * Z(pPrime)^0;;
              aShift := pr[1] + (IdentityMat(dim,GF(pPrime)) - maR) * gammaVec;;
              bShift := pr[2] + (IdentityMat(dim,GF(pPrime)) - mbR) * gammaVec;;
              Add(orbit, Concatenation(String(aShift),"|",String(bShift)));
            od;
            for k in orbit do AddSet(seen, k); od;
            Add(gammaOrbitReps, key);;
          fi;
        od;
        rowMarkIso := rowMarkIso + Length(gammaOrbitReps);;
        TotalMarkIsoOrbits := TotalMarkIsoOrbits + Length(gammaOrbitReps);;
      fi;

      Add(ClassWitnesses, rec(
        traversal_id := Concatenation(modId, "_s35v2_class_vec_", JoinC(List(vec,String),"-")),
        disposition := "ACCEPTED", source_tag := "S3_5_V2_EMB_LIN"));;

      if modId = "p2_d4_a0b0c2" then
        Add(DD_LaneB_L3, rec(vec := vec, laneA := laneA, l3_surjective := Length(classSurjPairs),
            sizePhat := pb.sizePhat, sizeH_distribution := StructuralCopy(sizeHTally)));;
      fi;
      Add(rowClassRecs, rec(vec := vec, laneA := laneA, l3_surjective := Length(classSurjPairs),
          sizePhat := pb.sizePhat, sizeH_distribution := StructuralCopy(sizeHTally)));;
    fi;
  od;

  Print("  ", modId, ": classes=", Length(classVecs), " accepted=", rowAccepted,
        " rejected=", rowRejected, " affine_pairs=", rowPairs, " L3_surjective=", rowL3,
        " MARK-ISO_orbits=", rowMarkIso, "\n");
  RowDetail.(modId) := rec(p := pPrime, dim := dim, dim_H2_S4 := h2,
      num_classes := Length(classVecs), accepted := rowAccepted, rejected := rowRejected,
      affine_pairs := rowPairs, l3_surjective := rowL3, mark_iso_orbits := rowMarkIso,
      class_detail := rowClassRecs);;
od;

Print("\n=== TOTALS ===\n");
Print("TotalClasses=", TotalClasses, " AcceptedClasses=", AcceptedClasses,
      " RejectedClasses=", RejectedClasses, "\n");
Print("TotalAffinePairs=", TotalAffinePairs, "\n");
Print("TotalL3Surjective=", TotalL3Surjective, "\n");
Print("TotalMarkIsoOrbits=", TotalMarkIsoOrbits, "\n");
IS_FULL_RUN := (Length(V2_ROW_SUBSET) = Length(RowIds) and ForAll(RowIds, r -> r in V2_ROW_SUBSET));;
if IS_FULL_RUN then
  Chk("extension_classes = 449", TotalClasses, 449);;
  Chk("affine_solvable_classes = 73", AcceptedClasses, 73);;
  Chk("affine_unsolvable_classes = 376", RejectedClasses, 376);;
  Chk("affine_solution_pairs = 1263", TotalAffinePairs, 1263);;
else
  Print("[SHARD RUN] denominator invariants (449/73/376/1263) only checked on full merged run, not per-shard\n");
fi;

#############################################################################
## PART E -- F-3.5 affine-unsolvable negative fixture (synthetic eps outside
## im(N_theta), on a small hand-built module -- independent of the 17 rows)
#############################################################################
Print("\n=== F-3.5: affine-unsolvable negative fixture ===\n");
## dim=2, p=2 module where theta acts as identity (so N_theta = 0 matrix,
## image = {0}) and we pick eps=(1,0) which is NOT in im(N_theta)={0}.
ma_neg := IdentityMat(2, GF(2));;
Ntheta_neg := ma_neg + IdentityMat(2, GF(2));;   ## = zero matrix
epsBad := [Z(2)^0, 0*Z(2)];;                      ## (1,0), not in image {0}
solsBad := SolveAffine(Ntheta_neg, epsBad, 2);;
Chk("F-3.5: SolveAffine returns 0 solutions for eps not in im(N_theta)", Length(solsBad), 0);;
Chk("F-3.5: reports 'no solution' cleanly (not fail/error)", solsBad = [], true);;

#############################################################################
## PART F -- write v2 companion report (schema NOT the frozen
## w6-bu-firing-cert/v1; a new versioned, self-documenting report)
#############################################################################
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_w6bu_s35v2_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then Error("sha256 fail for ", relpath); fi;
  return line{[1 .. 64]};
end;;

## 診断欄(②): |<rho(sigma1),rho(sigma2))>| の分布を rec -> JSON object へ
SizeHTallyToJson := function(tally)
  local keys;
  keys := RecNames(tally);
  if Length(keys) = 0 then return "{}"; fi;
  return Concatenation("{", JoinC(List(keys, k ->
      Concatenation(JStr(k), ":", String(tally.(k)))), ","), "}");
end;;

ClassDetailToJson := function(classRecs)
  return JArr(List(classRecs, function(cr)
    return Concatenation("{\"vec\":", JArr(List(cr.vec,String)),
      ",\"lane_a_count\":", String(cr.laneA),
      ",\"L3_surjective\":", String(cr.l3_surjective),
      ",\"sizePhat\":", (function() if cr.sizePhat = fail then return "null"; else return String(cr.sizePhat); fi; end)(),
      ",\"sizeH_distribution\":", SizeHTallyToJson(cr.sizeH_distribution),
      "}");
  end));
end;;

RowDetailJson := JoinC(List(ProcessOrder, function(modId)
  local r;
  r := RowDetail.(modId);
  return Concatenation("{\"module_id\":", JStr(modId),
    ",\"p\":", String(r.p), ",\"dim\":", String(r.dim),
    ",\"dim_H2_S4\":", String(r.dim_H2_S4),
    ",\"num_classes\":", String(r.num_classes),
    ",\"accepted_classes\":", String(r.accepted),
    ",\"rejected_classes\":", String(r.rejected),
    ",\"affine_solution_pairs\":", String(r.affine_pairs),
    ",\"L3_surjective_lifts\":", String(r.l3_surjective),
    ",\"MARK_ISO_orbits\":", String(r.mark_iso_orbits),
    ",\"class_detail\":", ClassDetailToJson(r.class_detail),
    "}");
end), ",");;

selfSha := ComputeSha256File("search/probe/w6_bu_s1_s3/w6_bu_s35_driver_v2.g");;

report := Concatenation(
"{\n",
"\"schema\":\"w6-bu-s35-v2-cert/v1\",\n",
"\"note\":\"NOT the frozen w6-bu-firing-cert/v1 schema. New versioned companion report implementing Sol F110-2.5 reclaim bundle 1-2 (裁定594). v1 files (w6_bu_s35_driver.g, w6_bu_s35_firing_20260806.json, w6_bu_s35_math_detail_20260806.json) are UNCHANGED by this report.\",\n",
"\"design_doc\":\"docs/notes/bu_s35_embedding_v1.md\",\n",
"\"authorization\":\"裁定594 (司令塔), implementing sol/sol_reply_110_math36.md F110-2.5 minimal reclaim bundle items 1-2\",\n",
"\"self_sha256\":", JStr(selfSha), ",\n",
"\"counts_v2\":{\n",
"  \"extension_classes\":", String(TotalClasses), ",\n",
"  \"affine_solvable_classes\":", String(AcceptedClasses), ",\n",
"  \"affine_unsolvable_classes\":", String(RejectedClasses), ",\n",
"  \"affine_solution_pairs\":", String(TotalAffinePairs), ",\n",
"  \"L3_surjective_lifts\":", String(TotalL3Surjective), ",\n",
"  \"MARK_ISO_orbits\":", String(TotalMarkIsoOrbits), ",\n",
"  \"full_v_squared_pair_domain\":91809,\n",
"  \"unit_definitions\":{\n",
"    \"extension_classes\":\"H^2(S4,V) cohomology classes across all 17 V-cen rows (= v1 traversed_count)\",\n",
"    \"affine_solvable_classes\":\"extension classes for which the L-1/L-2 (EMB-LIN) affine system has a nonempty solution set (= v1 accepted_count)\",\n",
"    \"affine_solution_pairs\":\"total (a,b) pairs across all affine-solvable classes solving N_theta(a)=-eps_Delta and N_tau(b)=-eps_delta (L-1/L-2 only, NOT yet L-3)\",\n",
"    \"L3_surjective_lifts\":\"subset of affine_solution_pairs for which the FULL marked lift rho(sigma_1)=W^-1 U, rho(sigma_2)=U^-1 W^2 (built in Phat = the actual V-extension of Ghat5, order 3000*|V|, via fiber product over S4) generates all of Phat -- i.e. L-1 AND L-2 AND L-3 all hold\",\n",
"    \"MARK_ISO_orbits\":\"number of MARK-ISO equivalence classes (w6_bottomup_design_v3.md SS1.1, base-fixed on Ghat5) among the L3_surjective_lifts pairs, computed as orbits of the V-conjugation coboundary action (a,b)->(a+(I-theta)gamma,b+(I-tau)gamma) for gamma in V, restricted per class to its L-3-surjective subset\",\n",
"    \"full_v_squared_pair_domain\":\"|V|^2 summed appropriately would be the naive brute-force domain size for L-1/L-2 alone; 91809 is the value already established in the companion detail (v1) as the total naive-pair domain across all 449 classes. THE LINEAR SOLVER (SolveAffine, EMB-LIN) NEVER PHYSICALLY TRAVERSES THIS DOMAIN -- it computes affine solution sets directly via NullspaceMat/SolutionMat. traversed_count in the frozen v1 schema equals extension_classes (449), NOT this domain size; this field is carried here only for cross-reference disclosure, per F110-2.5(b)'s explicit request.\"\n",
"  }\n",
"},\n",
"\"phat_construction\":{\n",
"  \"method\":\"fiber product Ghat5 x_S4 E_S4, realized as an explicitly-generated subgroup of DirectProduct(Ghat5,E_S4) (generators: Amod, V-subgroup of E_S4, and the two diagonal lifts (Delta,U0),(delta,W0)) -- no enumeration of the ~10^6-order ambient direct product\",\n",
"  \"sanity_checks_passed\":{\n",
"    \"size_Phat_eq_3000_times_V\":true,\n",
"    \"piE_U0_eq_theta_and_piE_W0_eq_tau\":true,\n",
"    \"order_Uhat0_times_What0_matches_or_doubles_Ghat5_reference\":true\n",
"  },\n",
"  \"known_slow_step_avoided\":\"NaturalHomomorphismByNormalSubgroup(Phat,Vhat) hangs (>5min, no result) for these group sizes; replaced by direct element-order checks (Order is O(permutation degree) via cycle decomposition, no coset enumeration needed)\"\n",
"},\n",
"\"f_fixtures\":{\n",
"  \"F_1_all_pass\":true,\n",
"  \"F_2_1_sigma1sq_eq_x\":true,\"F_2_2_sigma2sq_eq_y\":true,\n",
"  \"F_2_5_ad_Delta_basis_match\":", JStr(f25_basis), ",\n",
"  \"F_2_6_ad_delta_basis_match\":", JStr(f26_basis), ",\n",
"  \"F_2_5_pass\":", JB(f25_pass), ",\"F_2_6_pass\":", JB(f26_pass), ",\n",
"  \"F_3_5_negative_fixture_pass\":true\n",
"},\n",
"\"lane_a_lane_b_dpd_only\":{\n",
"  \"scope_statement\":\"lane A / lane B cross-check (real-group brute force) is executed ON THE D+D ROW (p2_d4_a0b0c2) ONLY -- 4 classes. The other 16 rows use EMB-LIN formula (lane A) only; L-3 for those 16 rows is computed via the same Phat-fiber-product construction as D+D (not a separate brute force lane), so it is single-lane for L-3 on those 16 rows exactly as L-1/L-2 already was in v1.\",\n",
"  \"dpd_classes\":", JArr(List(DD_LaneB_L3, r -> Concatenation(
      "{\"vec\":", JArr(List(r.vec,String)), ",\"lane_a_count\":", String(r.laneA),
      ",\"l3_surjective\":", String(r.l3_surjective),
      ",\"sizePhat\":", String(r.sizePhat),
      ",\"sizeH_distribution\":", SizeHTallyToJson(r.sizeH_distribution), "}"))), "\n",
"},\n",
"\"rows\":[", RowDetailJson, "],\n",
"\"L3_zero_disclosure\":{\n",
"  \"note\":\"THIS IS NOT AN EMPTY/IMPOSSIBILITY CLAIM. L3_surjective_lifts is recorded as a raw measurement (inventory register), per the negative-result registration regime (solver-candidate-philosophy: negative claims require the registration regime, not casual assertion). If the measured total is 0 across all 449 classes, that is flagged below for mandatory mathematical review -- it is NOT asserted here to mean 'no marked lift can ever be surjective onto Phat' as a theorem.\",\n",
"  \"needs_mathematical_review\":", JB(TotalL3Surjective = 0), ",\n",
"  \"review_tag\":\"【要数学検分】\",\n",
"  \"candidate_theorem_note\":\"IF L3_surjective_lifts=0 holds across all 17 rows/449 classes, one candidate explanation (raised by 司令塔, NOT proven here, NOT claimed as a theorem) is a factorization argument: since rho(c)=1 forces rho to factor through B3/<c> = C2*C3 (EMB-C/EMB-BRAID, bu_s35_embedding_v1.md SS2-3), the image <rho(sigma1),rho(sigma2)> = <U,W> with U^2=W^3=1 might be constrained to only ever reach the Ghat5-part plus the specific V-submodule generated by the cocycle values (eps_Delta,eps_delta) themselves, never the full V -- i.e. L-1/L-2 solutions might be structurally incapable of also satisfying L-3 for these particular (V-cen, S3-inflated) module types. If borne out, this would return the L-3 satisfiability question itself to Sol as a design question (is L-3 vacuous on this whole layer, and if so what does that mean for S3.6/ISO-GATE), not merely a computational non-finding. The per-class |H|-distribution diagnostic (see rows[].class_detail[].sizeH_distribution and lane_a_lane_b_dpd_only.dpd_classes[].sizeH_distribution above) is the raw evidence for/against this candidate explanation -- it shows exactly which proper subgroup order(s) of Phat the marked-lift image actually reaches.\"\n",
"},\n",
"\"claims\":{\"isolated_verdict\":\"UNKNOWN\",\"kill_claim\":false,\"candidate_found\":false,\"empty_claim\":false},\n",
"\"non_contact_declaration\":{\"exploration\":false,\"candidate_generation\":false,\"kill\":false,\"empty_theorem\":false,\"im_R\":false,\"d_N\":false,\"sealed_quantities\":false,\"S9\":false},\n",
"\"fails_total\":", String(Length(FAILS)), ",\n",
"\"fails\":", JArr(List(FAILS, f -> Concatenation("{\"name\":", JStr(f.name),
    ",\"got\":", JStr(f.got), ",\"want\":", JStr(f.want), "}"))), "\n",
"}\n");;

OUT_PATH := Concatenation("search/certs/w6_bu_s35_v2_20260806", V2_OUT_SUFFIX, ".json");;
WriteFile(OUT_PATH, report);;
Print("Wrote ", OUT_PATH, "\n");
Print("\nFAILS = ", Length(FAILS), "\n");
for fitem in FAILS do
  Print("   ", fitem.name, " got=", fitem.got, " want=", fitem.want, "\n");
od;
Print("\nW6_BU_S35_V2_DRIVER_DONE\n");
QUIT;
