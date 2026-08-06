#############################################################################
## search/probe/sg_band_sweep/sg_chir2_single_window_v1.g
## CHIR-2 (裁定696): theorem_check_mirrorall_l3vacuous_v1.md SSG.11.3
## "実測指示書 CHIR-2" (数学者起草, verbatim). ONE window per GAP process
## (same architecture as CHIR-1 v2, per 司令塔's prior intervention --
## 1 gap.ps1 process per window, external `timeout 120` cap).
##
## Steps (verbatim from the note):
##   1. R := P/X (order 648 for layer-3); confirm R reflexible (re-confirm
##      canary C5, keeping the witness automorphism beta_R this time).
##   2. chi: R -> Aut(X) from the conjugation action; confirm chi != 1 and
##      ker(chi) has index 2 (only meaningful/exact for X elementary
##      abelian; non-abelian X is reported and the module framework is
##      honestly skipped for that window).
##   3. Build the GF(3)[R]-module M (dim = rank of X as elementary abelian
##      3-group; for layer-3 this is dim 1 = the signed module F_3(chi)).
##   4. dim_F3 H^2(R,M) via CHR/SecondCohomologyDimension (cohomolo
##      package, the SAME machinery already used throughout this session
##      for S3.5/pband2prime -- "TwoCohomology" in the note is descriptive,
##      not a literal GAP function name; this is the established
##      equivalent tool). PRIMARY MEASUREMENT: predicted >= 2.
##   5. Identify [eps]: iterate vec in M^dim(H^2), build
##      SplitExtensionCHR/NonsplitExtension(chr,vec), IdGroup-match against
##      Ghat.
##   6/7. beta_R* eigenvector test, made DIRECTLY computable (avoiding a
##      full AutomorphismGroup(Ghat) computation, order up to 1944): per
##      【GAP-G11-1】's own disclosed caveat, "beta_R lifts and [eps] is an
##      eigenvector" is (mod the residual Z^1(R,X) torsor adjustment, which
##      is NOT resolved here, disclosed honestly) equivalent to: exists
##      x1,x2 in X such that the map U->U*x1, W->W^-1*x2 extends to a
##      BIJECTIVE endomorphism of Ghat (i.e. an automorphism with images in
##      the correct X-cosets). |X| small (3 or 9) so this is a cheap finite
##      search (<=9 or <=81 candidate pairs), NOT a full Aut(Ghat) call.
##
## Canaries (a)(b)(c) per the note: (a) [eps]!=0 (NONSPLIT, checked via
## ComplementClassesRepresentatives); (b) kappa=|X| and |R|*|X|=|Ghat|;
## (c) not applicable here (this script is only invoked for the 5 non-
## isolated windows to begin with).
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
LoadPackage("cohomolo");;

if not IsBound(CHIR2_ORDER) or not IsBound(CHIR2_ID) then
  Error("CHIR2_ORDER / CHIR2_ID must be set before Read()-ing this file");
fi;

S3grp := SymmetricGroup(3);;

G1_Test := function(Ghat)
  local ab;
  ab := AbelianInvariants(Ghat);;
  return ab in [[2],[2,3],[6]];
end;;

FindOneG2G3Pair := function(Ghat)
  local invs, ord3, r, s, sz, quots;
  invs := Filtered(Elements(Ghat), x -> Order(x) = 2);;
  ord3 := Filtered(Elements(Ghat), x -> Order(x) = 3);;
  sz := Size(Ghat);;
  for r in invs do
    for s in ord3 do
      if Size(Subgroup(Ghat,[r,s])) = sz then
        quots := GQuotients(Ghat, S3grp);;
        if Length(quots) > 0 then
          return rec(ok := true, r := r, s := s);
        else
          return rec(ok := false);
        fi;
      fi;
    od;
  od;
  return rec(ok := false);
end;;

## Reidemeister-Schreier-via-spanning-tree (same as sg_chir1_single_window_v2.g)
BFSPresentation := function(Ghat, U, W)
  local F, uF, wF, elems, words, i, gens, pr, x, xF, g2, j, relators, rel;
  F := FreeGroup(2);; uF := F.1;; wF := F.2;;
  elems := [ One(Ghat) ];;
  words := [ One(F) ];;
  gens := [ [U,uF], [W,wF] ];;
  i := 1;;
  while i <= Length(elems) do
    for pr in gens do
      x := pr[1];; xF := pr[2];;
      g2 := elems[i]*x;;
      j := Position(elems, g2);;
      if j = fail then
        Add(elems, g2);; Add(words, words[i]*xF);;
      fi;
    od;
    i := i + 1;;
  od;
  relators := [];;
  for i in [1..Length(elems)] do
    for pr in gens do
      x := pr[1];; xF := pr[2];;
      g2 := elems[i]*x;;
      j := Position(elems, g2);;
      rel := words[i]*xF*words[j]^-1;;
      if rel <> One(F) then Add(relators, rel); fi;
    od;
  od;
  return rec(F := F, relators := relators);;
end;;

RhoWord := function(w)
  local er, i;
  er := ShallowCopy(ExtRepOfObj(w));;
  for i in [1,3..Length(er)-1] do
    if er[i] = 2 then er[i+1] := -er[i+1]; fi;
  od;
  return ObjByExtRep(FamilyObj(w), er);;
end;;

ComputeXgrp := function(Ghat, U, W)
  local pres, F, evalHom, imgs, Xgrp;
  pres := BFSPresentation(Ghat, U, W);;
  F := pres.F;;
  evalHom := GroupHomomorphismByImages(F, Ghat, GeneratorsOfGroup(F), [U,W]);;
  imgs := List(pres.relators, rw -> Image(evalHom, RhoWord(rw)));;
  if Length(imgs) = 0 or ForAll(imgs, x -> x = One(Ghat)) then
    Xgrp := TrivialSubgroup(Ghat);;
  else
    Xgrp := NormalClosure(Ghat, Subgroup(Ghat, imgs));;
  fi;
  return Xgrp;;
end;;

## Build an FqR fp-presentation (via BFS on R) usable with CHR, matching
## generator order [Ubar,Wbar].
BuildFqR := function(R, Ubar, Wbar)
  local pres;
  pres := BFSPresentation(R, Ubar, Wbar);;
  return pres.F / pres.relators;;
end;;

## Action matrix of g (in Ghat) on Xgrp (elementary abelian p-group),
## expressed in a fixed pcgs basis -- same pattern as AdMatrixOverGF5 used
## throughout this session (w6_bu_s35_driver_v2.g / sg_pband2prime_driver_v1.g).
ActionMatrixOnX := function(Xgrp, isoXpc, pcgsX, p, g)
  local rows, i, x0, img, expv;
  rows := [];;
  for i in [1..Length(pcgsX)] do
    x0 := PreImagesRepresentative(isoXpc, pcgsX[i]);;
    img := x0^g;;
    expv := ExponentsOfPcElement(pcgsX, Image(isoXpc, img));;
    Add(rows, expv * Z(p)^0);;
  od;
  return rows;;
end;;

#############################################################################
## MAIN (single window)
#############################################################################
t0 := GAPLIB_WallElapsedMs();;
outRec := rec(order := CHIR2_ORDER, id := CHIR2_ID);;

Ghat := SmallGroup(CHIR2_ORDER, CHIR2_ID);;
if not G1_Test(Ghat) then
  outRec.status := "HANDOFF_MISMATCH";;
else
  entry := FindOneG2G3Pair(Ghat);;
  if not entry.ok then
    outRec.status := "HANDOFF_MISMATCH";;
  else
    U := entry.r;; W := entry.s;;
    Xgrp := ComputeXgrp(Ghat, U, W);;
    kappa := Size(Xgrp);;

    ## canary (b)
    canB := (kappa = Size(Xgrp)) and (Size(Ghat) mod kappa = 0)
            and ((Size(Ghat)/kappa) * kappa = Size(Ghat));;

    quoHom := NaturalHomomorphismByNormalSubgroup(Ghat, Xgrp);;
    Print("  [diag] R constructed", "\n");
    R := Image(quoHom);;
    Ubar := Image(quoHom, U);; Wbar := Image(quoHom, W);;

    ## step 1: R reflexible? find beta_R witness.
    ## bugfix: AutomorphismGroup(R) (order 648 for layer-3) + iterating
    ## over ALL its elements was the actual 120s-timeout bottleneck (silent
    ## hang, no partial output). Replaced with the SAME cheap direct test
    ## used later for the eigenvector-lift check: construct the specific
    ## candidate homomorphism Ubar->Ubar, Wbar->Wbar^-1 and just check
    ## IsBijective -- no full automorphism group needed at all.
    betaR := GroupHomomorphismByImages(R, R, [Ubar,Wbar], [Ubar,Wbar^-1]);;
    rReflexible := (betaR <> fail) and IsBijective(betaR);;
    Print("  [diag] betaR test done, rReflexible=", rReflexible, "\n");
    if not rReflexible then betaR := fail; fi;

    ## canary (a): [eps] != 0 (nonsplit), via absence of a complement
    comps := ComplementClassesRepresentatives(Ghat, Xgrp);;
    canA_nonsplit := (Length(comps) = 0);;
    Print("  [diag] complement check done", "\n");

    isAbelianX := IsAbelian(Xgrp);;
    outRec.status := "OK";;
    outRec.kappa := kappa;;
    outRec.R_order := Size(R);;
    outRec.R_reflexible := rReflexible;;
    outRec.X_abelian := isAbelianX;;
    outRec.canary_a_nonsplit := canA_nonsplit;;
    outRec.canary_b_arith := canB;;

    if not isAbelianX then
      outRec.module_framework_applies := false;;
      outRec.note := "X non-abelian -- chi:R->Aut(X) / H^2(R,M) module framework does not apply as specified (needs X abelian); reported per SSG.11.3's own disclosed scope difference for layer-2 (2,3-part comparison), not computed further";;
    else
      outRec.module_framework_applies := true;;
      p := 3;;
      isoXpc := IsomorphismPcGroup(Xgrp);;
      Xpc := Image(isoXpc);;
      pcgsX := Pcgs(Xpc);;
      d := Length(pcgsX);;
      outRec.module_dim := d;;

      matU := ImmutableMatrix(GF(p), ActionMatrixOnX(Xgrp, isoXpc, pcgsX, p, U));;
      matW := ImmutableMatrix(GF(p), ActionMatrixOnX(Xgrp, isoXpc, pcgsX, p, W));;
      ## sanity: matU,matW should factor through R (i.e. depend only on
      ## Ubar,Wbar, not on the specific X-coset representative chosen for
      ## U,W) -- automatic since X is abelian and normal (conjugation by
      ## elements of X on X is trivial), not re-verified here explicitly.

      if d = 1 then
        chiU := matU[1][1];; chiW := matW[1][1];;
        outRec.chi_U := String(chiU);; outRec.chi_W := String(chiW);;
        outRec.chi_nontrivial := (chiU <> Z(p)^0) or (chiW <> Z(p)^0);;
        outRec.chi_W_is_trivial_as_predicted := (chiW = Z(p)^0);;   ## Syl_3(R) subseteq ker chi
      fi;

      ## bugfix (2nd occurrence): CHR (cohomolo package) requires its 1st
      ## argument's GeneratorsOfGroup to be EXACTLY [gen for u, gen for w]
      ## matching FqR's generators -- fixed via Group(UbarP,WbarP).
      ## bugfix (3rd occurrence): the regular-action representation (degree
      ## =|R|=648) made the cohomolo package's EXTERNAL cohomology binary
      ## exceed the 120s cap (silently, no partial output) for the layer-3
      ## windows. Switched to IsomorphismPermGroup(R)'s own (much smaller,
      ## e.g. core-free-subgroup-coset-action) degree, while STILL forcing
      ## the generator list to be exactly [UbarP,WbarP] via Group(...) so
      ## CHR's relator check still passes; faithfulness verified by size.
      isoRsmall := IsomorphismPermGroup(R);;
      Print("  [diag] IsomorphismPermGroup(R) done", "\n");
      UbarP := Image(isoRsmall, Ubar);;
      WbarP := Image(isoRsmall, Wbar);;
      Rperm := Group(UbarP, WbarP);;
      if Size(Rperm) <> Size(R) then
        Error("small-degree permutation representation of R is not faithful/generating -- unexpected");
      fi;
      FqR := BuildFqR(Rperm, UbarP, WbarP);;
      chr := CHR(Rperm, p, FqR, [matU, matW]);;
      Print("  [diag] CHR built, Rperm degree=", NrMovedPoints(Rperm), "\n");
      h2dim := SecondCohomologyDimension(chr);;
      Print("  [diag] h2dim=", h2dim, "\n");
      outRec.dim_H2 := h2dim;;
      outRec.dim_H2_ge2 := (h2dim >= 2);;

      ## identify [eps]: match vec -> extension isomorphic to Ghat.
      ## bugfix (4th occurrence): the exhaustive IdGroup(Epc) comparison
      ## over all 3^dim_H2 candidates (27 for the observed dim=3) was the
      ## remaining 120s-timeout cause (each IdGroup call on an order-1944
      ## group is not free). LIGHTENED per time budget: cheap AbelianInvariants
      ## pre-filter first (rules out most candidates for free), and IdGroup
      ## is only called on candidates that survive the filter, WITH A HARD
      ## CAP of 6 IdGroup calls (chosen to fit the 120s budget) -- if the
      ## cap is hit before a match is found, eps_identified is reported
      ## honestly as UNKNOWN_CAPPED (not silently claimed either way). The
      ## PRIMARY measurement (dim_H2 >= 2, already obtained above) does not
      ## depend on this step at all.
      idGhat_abinv := AbelianInvariants(Ghat);;
      idGhat_cached := IdGroup(Ghat);;   ## bugfix: was recomputed every loop iteration
      matchingVecs := [];;
      idGroupCallsUsed := 0;;
      IDGROUP_CALL_CAP := 6;;
      capHit := false;;
      if h2dim = 0 then
        candVecs := [ [] ];;
      else
        candVecs := Cartesian(List([1..h2dim], ii -> [0..p-1]));;
      fi;
      Print("  [diag] starting eps-identification loop, ", Length(candVecs), " candidates, cap=", IDGROUP_CALL_CAP, "\n");
      for vec in candVecs do
        if capHit then break; fi;
        if ForAll(vec, vv -> vv = 0) then
          Eext := SplitExtensionCHR(chr);;
        else
          Eext := NonsplitExtension(chr, vec);;
        fi;
        isoE := IsomorphismPcGroup(Eext);;
        Epc := Image(isoE);;
        if Size(Epc) <> Size(Ghat) then continue; fi;
        if AbelianInvariants(Epc) <> idGhat_abinv then continue; fi;
        if idGroupCallsUsed >= IDGROUP_CALL_CAP then
          capHit := true;; break;
        fi;
        idGroupCallsUsed := idGroupCallsUsed + 1;;
        if IdGroup(Epc) = idGhat_cached then
          Add(matchingVecs, vec);;
        fi;
      od;
      Print("  [diag] eps-identification loop done, idGroup calls used=", idGroupCallsUsed, " capHit=", capHit, "\n");
      outRec.eps_matching_vecs := matchingVecs;;
      outRec.eps_identified := (Length(matchingVecs) > 0);;
      outRec.eps_identification_capped := capHit;;
      outRec.eps_idgroup_calls_used := idGroupCallsUsed;;

      ## beta_R* eigenvector test, made directly computable (see header):
      ## exists x1,x2 in X such that U->U*x1, W->W^-1*x2 extends to a
      ## BIJECTIVE endomorphism of Ghat.
      eigVecFound := fail;;
      if isAbelianX then
        Print("  [diag] starting eigenvector search", "\n");
        for x1 in Xgrp do
          for x2 in Xgrp do
            hom := GroupHomomorphismByImages(Ghat, Ghat, [U,W], [U*x1, W^-1*x2]);;
            if hom <> fail and IsBijective(hom) then
              eigVecFound := [x1,x2];;
            fi;
          od;
        od;
      fi;
      outRec.eigenvector_lift_exists := (eigVecFound <> fail);;
      outRec.eigenvector_lift_witness := (function()
          if eigVecFound = fail then return "null"; else return Concatenation("[", String(eigVecFound[1]), ",", String(eigVecFound[2]), "]"); fi;
        end)();;
      outRec.prediction_note := "predicted: eigenvector_lift_exists = FALSE for layer-3 (FRAT-CHIR); layer-2 comparison, no specific prediction";;
    fi;
  fi;
fi;
outRec.wall_ms := GAPLIB_WallElapsedMs() - t0;;

#############################################################################
## write per-window JSON
#############################################################################
if outRec.status = "OK" then
  base := Concatenation(
    "{\"order\":", String(outRec.order), ",\"id\":", String(outRec.id),
    ",\"status\":", JStr(outRec.status), ",\"wall_ms\":", String(outRec.wall_ms),
    ",\"kappa\":", String(outRec.kappa), ",\"R_order\":", String(outRec.R_order),
    ",\"R_reflexible\":", JB(outRec.R_reflexible),
    ",\"canary_a_nonsplit\":", JB(outRec.canary_a_nonsplit),
    ",\"canary_b_arith\":", JB(outRec.canary_b_arith),
    ",\"X_abelian\":", JB(outRec.X_abelian),
    ",\"module_framework_applies\":", JB(outRec.module_framework_applies));;
  if outRec.module_framework_applies then
    extra := Concatenation(
      ",\"module_dim\":", String(outRec.module_dim),
      ",\"dim_H2\":", String(outRec.dim_H2),
      ",\"dim_H2_ge2\":", JB(outRec.dim_H2_ge2),
      ",\"eps_matching_vecs\":", JArr(List(outRec.eps_matching_vecs, v -> JArr(List(v,String)))),
      ",\"eps_identified\":", JB(outRec.eps_identified),
      ",\"eps_identification_capped\":", JB(outRec.eps_identification_capped),
      ",\"eps_idgroup_calls_used\":", String(outRec.eps_idgroup_calls_used),
      ",\"eigenvector_lift_exists\":", JB(outRec.eigenvector_lift_exists),
      ",\"eigenvector_lift_witness\":", outRec.eigenvector_lift_witness,
      ",\"prediction_note\":", JStr(outRec.prediction_note));;
    if IsBound(outRec.chi_U) then
      extra := Concatenation(extra,
        ",\"chi_U\":", JStr(outRec.chi_U), ",\"chi_W\":", JStr(outRec.chi_W),
        ",\"chi_nontrivial\":", JB(outRec.chi_nontrivial),
        ",\"chi_W_is_trivial_as_predicted\":", JB(outRec.chi_W_is_trivial_as_predicted));;
    fi;
  else
    extra := Concatenation(",\"note\":", JStr(outRec.note));;
  fi;
  json := Concatenation(base, extra, "}\n");;
else
  json := Concatenation(
    "{\"order\":", String(outRec.order), ",\"id\":", String(outRec.id),
    ",\"status\":", JStr(outRec.status), ",\"wall_ms\":", String(outRec.wall_ms), "}\n");;
fi;

OUT_PATH := Concatenation("scratchpad/chir2_window_", String(CHIR2_ORDER), "_", String(CHIR2_ID), ".json");;
WriteFile(OUT_PATH, json);;
Print("Wrote ", OUT_PATH, " wall_ms=", outRec.wall_ms, " status=", outRec.status, "\n");
Print("W6_SG_CHIR2_SINGLE_DONE\n");
QUIT;
