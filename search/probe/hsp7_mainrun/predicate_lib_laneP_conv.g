## search/probe/hsp7_mainrun/predicate_lib_laneP_conv.g
## Lane P P->Q CONVERSION (CONV-P) library -- NEW file, per 裁定527
## (docs/notes/hsp7_mainrun_conversion_v1.md SS1, construction CONV-P /
## lemma CONV-WD / lemma CONV-INJ). Does NOT modify predicate_lib_laneP.g
## (unchanged, read-only pinned baseline: Qgrp/rhoQ/PENT/NrhoQ construction).
##
## Purpose: translate a candidate f-bar given as a Pcgs(D) exponent vector
## (D:=[P,P], candidate_key_lib.g's e in {0,...,ord-1}^6) into the
## corresponding element of Q = K05fp/W, WITHOUT expanding it into an
## (x,y)-word and WITHOUT calling PreImagesRepresentative per candidate.
##
## Construction CONV-P (SS1.1):
##   (one-time precompute, 6 calls total)
##     1. pcgsD := Pcgs(D), D := DerivedSubgroup(P)  (6 generators, guaranteed
##        by BasisFromP-style structural checks -- this library re-checks it).
##     2. for each i, w_i in F(x,y) with epiFree(w_i) = pcgsD[i]
##        (PreImagesRepresentative against epiFree: FreeGroup(x,y) -> P,
##        x|->xbar, y|->ybar -- called exactly 6 times, never per candidate).
##        Gate (mandatory, cheap, decisive): epiFree(w_i) = pcgsD[i], checked
##        for all 6 immediately (CONV-P SS1.1 "必須ゲート").
##     3. Ghat_i := ImageElm(epi, MappedWord(w_i, [Fx,Fy], [jx,jy])) in Q
##        (evaluate w_i in K05fp by substituting the free generators with
##        jx,jy = kX12,kX23, then push through epi: K05fp -> Q).
##   (per candidate, given exponent vector e = [e1..e6])
##     jbar(fbar) := Ghat_1^e1 * Ghat_2^e2 * ... * Ghat_6^e6
##       (LEFT TO RIGHT, same order as the candidate key's own normal form
##       g1^e1...g6^e6 -- D=[P,P] is NON-ABELIAN, order matters, SS1.1 trap).
##
## well-defined-ness (CONV-WD) and injectivity (CONV-INJ) are proved in the
## note (SS1.2/SS1.3); this library does not re-derive them, only implements
## the resulting formula and the mandatory gate.
Read("search/probe/wac_v1/gap_output_prelude.g");

## BuildConvP(Pgroup, xbar, ybar, jx, jy, epi): one-time precompute.
## Pgroup: P (e.g. P5grp for the p=5 control window, or the p=7 main-run P).
## xbar,ybar: the 2 generators of Pgroup (Pgroup = <xbar,ybar>).
## jx,jy: the corresponding elements of K05fp (jx=kX12, jy=kX23 in the
##   existing lane driver naming -- the SAME j:F2=K(0,4) -> K(0,5) embedding
##   used throughout, x|->x12, y|->x23).
## epi: the group homomorphism K05fp -> Q used by the calibration driver
##   (predicate_lib_laneP.g's `epi` / driver_final_eval_p5.g's `epiQ`).
## Returns rec(P, D, pcgsD, ws, Ghat, gate_pass) -- gate_pass=false STOPS
## (Error) immediately, per the note's "必須ゲート" (mandatory, not advisory).
BuildConvP := function(Pgroup, xbar, ybar, jx, jy, epi)
  local D, pcgsD, n, FXY, Fx, Fy, epiFree, ws, Ghat, i, w, gateOk, wImg;
  D := DerivedSubgroup(Pgroup);
  pcgsD := Pcgs(D);
  n := Length(pcgsD);
  if n <> 6 then
    Error("CONV_P_STOP: Pcgs(D) has ", n, " generators, expected 6. Do not silently reshape the universe.");
  fi;

  FXY := FreeGroup("x", "y");
  Fx := FXY.1;;  Fy := FXY.2;;
  epiFree := GroupHomomorphismByImagesNC(FXY, Pgroup, [Fx, Fy], [xbar, ybar]);
  SetIsSurjective(epiFree, true);

  ws := [];;  Ghat := [];;  gateOk := true;;
  for i in [1..n] do
    w := PreImagesRepresentative(epiFree, pcgsD[i]);
    if w = fail then
      Error("CONV_P_STOP: PreImagesRepresentative failed for pcgs generator ", i,
            " -- epiFree not surjective onto D? (should be surjective onto all of P)");
    fi;
    wImg := ImageElm(epiFree, w);
    if wImg <> pcgsD[i] then
      gateOk := false;
      Print("CONV_P_GATE_FAIL at generator ", i, ": epiFree(w_", i, ") = ", wImg,
            " <> pcgsD[", i, "] = ", pcgsD[i], "\n");
    fi;
    Add(ws, w);
    Add(Ghat, ImageElm(epi, MappedWord(w, [Fx, Fy], [jx, jy])));
  od;
  if not gateOk then
    Error("CONV_P_STOP: mandatory gate (epiFree(w_i) = pcgsD[i], all 6) failed. See CONV_P_GATE_FAIL lines above.");
  fi;
  Print("CONV-P gate: all 6 precomputed w_i satisfy epiFree(w_i) = pcgsD[i]. PASS.\n");

  return rec(P := Pgroup, D := D, pcgsD := pcgsD, ws := ws, Ghat := Ghat, n := n);
end;;

## ConvPElement(convData, fbar): translate fbar (an element of convData.D =
## [P,P]) into its image in Q, via the precomputed Ghat_i and fbar's own
## Pcgs(D) exponent vector. LEFT-TO-RIGHT product, matching the candidate
## key's own normal form convention (candidate_key_lib.g ExpVectorToElement).
ConvPElement := function(convData, fbar)
  local e, acc, i;
  e := ExponentsOfPcElement(convData.pcgsD, fbar);
  if e = fail then
    Error("CONV_P_STOP: fbar is not an element of D=[P,P] (ExponentsOfPcElement failed)");
  fi;
  acc := One(convData.Ghat[1]);
  for i in [1..convData.n] do
    acc := acc * convData.Ghat[i]^e[i];
  od;
  return acc;
end;;
