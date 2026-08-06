#############################################################################
## search/probe/sg_band_sweep/sg_chir3_single_window_v1.g
## CHIR-3 (裁定699 part1): theorem_check_mirrorall_l3vacuous_v1.md SSG.12.2
## "実測指示書 CHIR-3" (数学者起草, verbatim). Reuses CHIR-2's exact
## (R, chi, module, chr) construction for the 2 layer-3 windows and adds
## the FirstCohomologyDimension(chr) measurement (dim H^1) -- the note's
## own "極小コスト" (秒) claim, since it is the SAME chr object CHIR-2
## already builds, just a different cohomolo call.
##
## Steps (verbatim):
##   1. dim_H1 := FirstCohomologyDimension(chr) (main measurement).
##   2. dim_Z1 := dim_B1 + dim_H1, with dim_B1 = dim(X) - dim(X^R) = 1 - 0
##      = 1 (since chi != 1 forces X^R = 0, already confirmed in CHIR-2).
##      image_dim := Minimum(dim_Z1, 2) (Z^1(R,X) embeds into F_3^2 via
##      d -> (d(Ubar),d(Wbar)), injectively, per the note).
##   3. Weak-lift construction + (x,y) membership test: SKIPPED here with
##      justification -- CHIR-2 already established (via an EXHAUSTIVE
##      search over all 9 candidate (x1,x2) in X x X, not just an abstract
##      membership test) that eigenvector_lift_exists=False for BOTH
##      windows, i.e. omega(beta_R,chi_X) != 0 (no weak lift exists in ANY
##      form) -- so there is no beta to correct in the first place. This
##      matches the note's own explicit instruction ("存在しない場合は3を
##      スキップ").
##   4. Output: dim_H1, image_dim (0/1/2), correction_possible (image_dim=2
##      -- meaning ANY future target (x,y) could be corrected, a
##      methodological/general-closure statement, NOT new information about
##      THESE 2 windows' already-established chirality).
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
LoadPackage("cohomolo");;

if not IsBound(CHIR3_ORDER) or not IsBound(CHIR3_ID) then
  Error("CHIR3_ORDER / CHIR3_ID must be set before Read()-ing this file");
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

BuildFqR := function(R, Ubar, Wbar)
  local pres;
  pres := BFSPresentation(R, Ubar, Wbar);;
  return pres.F / pres.relators;;
end;;

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
outRec := rec(order := CHIR3_ORDER, id := CHIR3_ID);;

Ghat := SmallGroup(CHIR3_ORDER, CHIR3_ID);;
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
    quoHom := NaturalHomomorphismByNormalSubgroup(Ghat, Xgrp);;
    R := Image(quoHom);;
    Ubar := Image(quoHom, U);; Wbar := Image(quoHom, W);;

    isAbelianX := IsAbelian(Xgrp);;
    outRec.status := "OK";;
    outRec.kappa := kappa;;
    outRec.R_order := Size(R);;

    if not isAbelianX then
      outRec.module_framework_applies := false;;
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

      isoRsmall := IsomorphismPermGroup(R);;
      UbarP := Image(isoRsmall, Ubar);;
      WbarP := Image(isoRsmall, Wbar);;
      Rperm := Group(UbarP, WbarP);;
      if Size(Rperm) <> Size(R) then
        Error("small-degree permutation representation of R is not faithful/generating -- unexpected");
      fi;
      FqR := BuildFqR(Rperm, UbarP, WbarP);;
      chr := CHR(Rperm, p, FqR, [matU, matW]);;

      h1dim := FirstCohomologyDimension(chr);;
      h2dim := SecondCohomologyDimension(chr);;
      outRec.dim_H1 := h1dim;;
      outRec.dim_H2 := h2dim;;   ## cross-check against CHIR-2's already-committed value

      ## X^R (fixed points of the module action) -- should be 0 given
      ## chi != 1 (already established in CHIR-2); verify directly here
      ## rather than assuming, since it feeds dim_B1.
      if d = 1 then
        xRfixed := (matU[1][1] = Z(p)^0) and (matW[1][1] = Z(p)^0);;
      else
        xRfixed := fail;;   ## not computed for d>1 (not needed for this window set, all d=1)
      fi;
      dimXR := (function() if xRfixed = true then return d; elif xRfixed = false then return 0; else return fail; fi; end)();;
      outRec.dim_X_fixed := dimXR;;

      if dimXR <> fail then
        dimB1 := d - dimXR;;
        dimZ1 := dimB1 + h1dim;;
        outRec.dim_B1 := dimB1;;
        outRec.dim_Z1 := dimZ1;;
        outRec.image_dim := Minimum(dimZ1, 2);;
        outRec.correction_possible_general := (outRec.image_dim = 2);;
      else
        outRec.dim_B1 := fail;; outRec.dim_Z1 := fail;; outRec.image_dim := fail;;
        outRec.correction_possible_general := fail;;
      fi;

      ## step 3 explicitly skipped, with justification (per the note's own
      ## "存在しない場合は3をスキップ" clause) -- CHIR-2 already
      ## established (exhaustive 9-pair search) that no weak lift exists
      ## for these 2 windows (eigenvector_lift_exists=False in
      ## search/certs/sg_chir2_20260806.json), i.e. omega != 0, so there is
      ## no beta to correct.
      outRec.step3_skipped := true;;
      outRec.step3_skip_reason := "CHIR-2 (search/certs/sg_chir2_20260806.json) already established eigenvector_lift_exists=False for this window via an exhaustive 9-pair search over X x X -- omega(beta_R,chi_X) != 0, no weak lift exists to correct. Matches the note's own explicit skip clause.";;
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
    ",\"module_framework_applies\":", JB(outRec.module_framework_applies));;
  if outRec.module_framework_applies then
    extra := Concatenation(
      ",\"module_dim\":", String(outRec.module_dim),
      ",\"dim_H1\":", String(outRec.dim_H1),
      ",\"dim_H1_ge1\":", JB(outRec.dim_H1 >= 1),
      ",\"dim_H2_crosscheck\":", String(outRec.dim_H2),
      ",\"dim_X_fixed\":", (function() if outRec.dim_X_fixed=fail then return "null"; else return String(outRec.dim_X_fixed); fi; end)(),
      ",\"dim_B1\":", (function() if outRec.dim_B1=fail then return "null"; else return String(outRec.dim_B1); fi; end)(),
      ",\"dim_Z1\":", (function() if outRec.dim_Z1=fail then return "null"; else return String(outRec.dim_Z1); fi; end)(),
      ",\"image_dim\":", (function() if outRec.image_dim=fail then return "null"; else return String(outRec.image_dim); fi; end)(),
      ",\"correction_possible_general\":", (function() if outRec.correction_possible_general=fail then return "null"; else return JB(outRec.correction_possible_general); fi; end)(),
      ",\"step3_skipped\":", JB(outRec.step3_skipped),
      ",\"step3_skip_reason\":", JStr(outRec.step3_skip_reason));;
  else
    extra := "";;
  fi;
  json := Concatenation(base, extra, "}\n");;
else
  json := Concatenation(
    "{\"order\":", String(outRec.order), ",\"id\":", String(outRec.id),
    ",\"status\":", JStr(outRec.status), ",\"wall_ms\":", String(outRec.wall_ms), "}\n");;
fi;

OUT_PATH := Concatenation("scratchpad/chir3_window_", String(CHIR3_ORDER), "_", String(CHIR3_ID), ".json");;
WriteFile(OUT_PATH, json);;
Print("Wrote ", OUT_PATH, " wall_ms=", outRec.wall_ms, " status=", outRec.status, "\n");
Print("W6_SG_CHIR3_SINGLE_DONE\n");
QUIT;
