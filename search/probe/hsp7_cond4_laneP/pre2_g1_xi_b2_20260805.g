## search/probe/hsp7_cond4_laneP/pre2_g1_xi_b2_20260805.g
## PRE-2 v2 (docs/notes/nw7_mainrun_predictions_iffirst_v1.md sec.5, table row PRE-2;
## originally authorized by 裁定 554; this v2 responds to 裁定 559 / Sol
## F106-2.4 (sol/sol_reply_106_math33.md), which found that the OLD script
## search/probe/hsp7_cond4_laneP/pre2_xi_b2_20260805.g measured
## xi_raw = D(jh3), but the raw Hall-commutator group element
##   r := Comm(Comm(x,y),x)*Comm(Comm(x,y),y)
## has log(r) = h3 + (v1+v2+v3) mod gamma_5 -- a NONZERO degree-4 correction
## (independently re-derived, honest group-BCH computation, in
## search/probe/hsp7_v1/pre2_g1_verify_20260805.py: raw r's hexagon-(3.11)
## degree-4 defect = 3*(v1+v2+v3) != 0 mod 7, exactly Sol's claimed value).
## So r is NOT an element of A = hex(0); the OLD script's xi is not D(g1) for
## any g1 in A, and its B-2b branch decision is UNSOUND (per F106-2.4, not
## adopted).
##
## This script computes the CORRECTED lift
##   s  := Comm(Comm(Comm(x,y),x),x) * Comm(Comm(Comm(x,y),x),y) * Comm(Comm(Comm(x,y),y),y)
##         (the gamma_4(P) group-commutator word representing v1+v2+v3; basis
##          words v1=[[[x,y],x],x], v2=[[[x,y],x],y], v3=[[[x,y],y],y] per
##          docs/notes/hs_prop7_translation_v1.md line 171; s's construction
##          mirrors jh4's own nested-Comm pattern, with all three coefficients
##          =1 instead of jh4's (1,4,1) -- independently confirmed correct,
##          with zero low-degree residue and exact deg4 = v1+v2+v3, by
##          pre2_g1_verify_20260805.py)
##   g1 := r * s^-1              (gamma_4(P) is central -- order immaterial,
##                                 confirmed independently: g1's honest-BCH log
##                                 has deg3 = h3 exactly and deg4 = 0 exactly,
##                                 i.e. g1 genuinely realizes an exact hex(0)
##                                 lift of h3, per pre2_g1_verify_20260805.py)
## and re-measures xi' = D(g1) in gamma_4(Q) (dim 21 over F_7), testing
## F_7-proportionality against eta = D(jh4) (the known-nonzero NW-P5
## quantity), exactly as the old script did for the (unsound) xi_raw.
##
## v1 script (pre2_xi_b2_20260805.g) is NOT modified. This is a new file.
## Its D(raw jh3) two vectors remain on record as diagnostic values (per
## F106-2.4's own instruction) -- not branch evidence.
##
## Scope discipline: rebuilds the ALREADY-CONSTRUCTED Q = K(0,5)/W (order
## 7^40, from the pre-existing ANUPQ artifact
## search/probe/hsp7_cond4_laneP/PQ_OUTPUT_Q_laneP.g) and evaluates D at a
## small fixed number of group elements (jh3, jh4, s, g1). This is a
## constant-size computation in a fixed finite group, NOT a run over the
## 705,894-pair universe. No candidate of that universe is touched.

Read("search/probe/wac_v1/gap_output_prelude.g");
LoadPackage("anupq");

Print("=== PRE-2 v2: xi' = D(g1), g1 = jh3 * s^-1 (corrected lift) vs eta = D(jh4) in gamma_4(Q) ===\n");

## ---- rebuild K05fp + j(x),j(y) + h4/h3/r/s/g1 words (verbatim reproduction of
## driver_step1/driver_step3's construction -- own fresh rebuild, not an
## import) ----
F := FreeGroup("s1","s2","s3");;
s1 := F.1;; s2 := F.2;; s3 := F.3;;
rels := [ s1*s3*s1^-1*s3^-1,
          s1*s2*s1*(s2*s1*s2)^-1,
          s2*s3*s2*(s3*s2*s3)^-1 ];;
B4 := F / rels;;
b1 := B4.1;; b2 := B4.2;; b3 := B4.3;;
X12 := b1^2;; X23 := b2^2;; X34 := b3^2;;
X13 := b2*b1^2*b2^-1;; X24 := b3*b2^2*b3^-1;; X14 := b3*X13*b3^-1;;
gensPB4 := [X12,X13,X14,X23,X24,X34];;
PB4sub := Subgroup(B4, gensPB4);;
iso := IsomorphismFpGroupByGenerators(PB4sub, gensPB4);;
PB4fp := Image(iso);;
Delta2 := (b1*b2*b3)^4;;
Delta2img := ImageElm(iso, Delta2);;
FPB4 := FreeGroupOfFpGroup(PB4fp);;
relsPB4 := RelatorsOfFpGroup(PB4fp);;
Delta2word := UnderlyingElement(Delta2img);;
K05fp := FPB4 / Concatenation(relsPB4, [Delta2word]);;
gK := GeneratorsOfGroup(K05fp);;
kX12 := gK[1];; kX13 := gK[2];; kX14 := gK[3];;
kX23 := gK[4];; kX24 := gK[5];; kX34 := gK[6];;

x15 := (kX12*kX13*kX14)^-1;;
x25 := (kX12*kX23*kX24)^-1;;
x35 := (kX13*kX23*kX34)^-1;;
x45 := (kX14*kX24*kX34)^-1;;
rhoImages := [ x45, kX14, kX24, x15, x25, kX12 ];;

jx := kX12;; jy := kX23;;
jh4 := Comm(Comm(Comm(jx,jy),jx),jx) * Comm(Comm(Comm(jx,jy),jx),jy)^4
       * Comm(Comm(Comm(jx,jy),jy),jy);;
jh3 := Comm(Comm(jx,jy),jx) * Comm(Comm(jx,jy),jy);;

## corrected lift: s = gamma_4(P) group word for v1+v2+v3, g1 = jh3 * s^-1
sword := Comm(Comm(Comm(jx,jy),jx),jx) * Comm(Comm(Comm(jx,jy),jx),jy)
         * Comm(Comm(Comm(jx,jy),jy),jy);;
g1word := jh3 * sword^-1;;

## ---- read PQ_OUTPUT via ANUPQ's own public reader (same artifact as
## driver_step3; not regenerated, not modified) ----
outFile := "search/probe/hsp7_cond4_laneP/PQ_OUTPUT_Q_laneP.g";;
result := PQ_READ_AS_FUNC_WITH_VARS(outFile, ["F","MapImages"]);;
Qgrp := result.F;;
mapImages := result.MapImages;;
Print("Qgrp read. NumberOfGenerators(Qgrp) = ", Length(GeneratorsOfGroup(Qgrp)), " (expect 40)\n");

epi := GroupHomomorphismByImagesNC(K05fp, Qgrp, gK, mapImages);;
SetIsSurjective(epi, true);;
Qcheck := Image(epi);;
Print("Image(epi) = Qgrp? ", Qcheck = Qgrp, "\n");

## ---- own fresh anchors (S-7' style; must match driver_step3's recorded log) ----
sizeQ := Size(Qgrp);;
Print("own_measurement: |Q| = ", sizeQ, "\n");
Print("own_measurement: |Q| = 7^40 ? ", sizeQ = 7^40, "\n");

lcsQ := LowerCentralSeriesOfGroup(Qgrp);;
Print("own_measurement: length(LCS) = ", Length(lcsQ), " (expect 5)\n");
gamma4 := lcsQ[4];;
gamma5size := Size(lcsQ[5]);;
gamma4size := Size(gamma4);;
Print("own_measurement: |gamma_4(Q)| = ", gamma4size, "\n");
Print("own_measurement: |gamma_5(Q)| = ", gamma5size, " (expect 1)\n");
dimGamma4 := LogInt(gamma4size, 7);;
Print("own_measurement: dim_F7 gamma_4(Q) = ", dimGamma4, " (expect 21)\n");
Print("own_measurement: gamma_4(Q) elementary abelian (exponent 7)? ",
      Exponent(gamma4) = 7, "\n");
if not (gamma5size = 1 and gamma4size = 7^21 and Exponent(gamma4) = 7) then
  Error("PRE2_STOP: anchors do not match driver_step3_eval_pent.log. STOP, report.");
fi;

rhoImagesQ := List(rhoImages, w -> ImageElm(epi, w));;
epiGens := List(gK, g -> ImageElm(epi, g));;
Print("epiGens generate Qgrp? ", Subgroup(Qgrp, epiGens) = Qgrp, "\n");

rhoQ := GroupHomomorphismByImages(Qgrp, Qgrp, epiGens, rhoImagesQ);;
Print("rhoQ well-defined? ", rhoQ <> fail, "\n");
if rhoQ = fail then
  Error("PRE2_STOP: rho-bar not well-defined on Q. S-6 fires. INTEGRITY_STOP.");
fi;
rho5 := rhoQ*rhoQ*rhoQ*rhoQ*rhoQ;;
Print("own_measurement: rhoQ^5 = id? ", ForAll(epiGens, g -> ImageElm(rho5,g) = g), "\n");

## ---- j(h4), j(h3), j(s), j(g1) in Q ----
jh4Q := ImageElm(epi, jh4);;
jh3Q := ImageElm(epi, jh3);;
sQ   := ImageElm(epi, sword);;
g1Q  := ImageElm(epi, g1word);;
Print("j(h4) = identity in Q? ", IsOne(jh4Q), " (expect false)\n");
Print("j(h3) = identity in Q? ", IsOne(jh3Q), " (expect false)\n");
Print("j(s)  = identity in Q? ", IsOne(sQ), "\n");
Print("j(g1) = identity in Q? ", IsOne(g1Q), "\n");

## structural check: g1Q should equal jh3Q * sQ^-1 in Q (sanity on epi being a
## homomorphism, and on g1word's definition)
Print("g1Q = jh3Q * sQ^-1 (epi homomorphism sanity)? ", g1Q = jh3Q*sQ^-1, "\n");

## structural check: sQ should lie in gamma_4(Q) (elementary abelian, central)
Print("sQ in gamma_4(Q)? ", sQ in gamma4, "\n");
if not (sQ in gamma4) then
  Error("PRE2_STOP: s does not land in gamma_4(Q) as expected. STOP, report.");
fi;
## centrality check of gamma_4(Q) in Q (justifies order-immateriality of g1 := r*s^-1)
Print("gamma_4(Q) central in Q? ", ForAll(epiGens, g -> ForAll(GeneratorsOfGroup(gamma4),
      h -> g*h = h*g)), "\n");

## ---- D = N_rho (verbatim same operator as driver_step3's NrhoQ / PENT) ----
DfnQ := function(fbar)
  local r1, r2, r3, r4;
  r1 := ImageElm(rhoQ, fbar);
  r2 := ImageElm(rhoQ, r1);
  r3 := ImageElm(rhoQ, r2);
  r4 := ImageElm(rhoQ, r3);
  return r4*r3*r2*r1*fbar;
end;;

eta     := DfnQ(jh4Q);;   # = D(h4), NW-P5 quantity
xi_raw  := DfnQ(jh3Q);;   # = D(raw jh3) -- DIAGNOSTIC ONLY per F106-2.4, NOT branch evidence
xiprime := DfnQ(g1Q);;    # = D(g1), g1 = jh3*s^-1 -- the CORRECTED quantity this script decides B-2 with

Print("\n--- eta = D(jh4) ---\n");
Print("eta = 1 ? ", IsOne(eta), " (expect false, per NW-P5 / driver_step3 t=1 case)\n");
Print("eta in gamma_4(Q)? ", eta in gamma4, "\n");

Print("\n--- xi_raw = D(jh3)  [DIAGNOSTIC ONLY, per F106-2.4 not branch evidence] ---\n");
Print("xi_raw = 1 ? ", IsOne(xi_raw), "\n");
Print("xi_raw in gamma_4(Q)? ", xi_raw in gamma4, "\n");

Print("\n--- xi' = D(g1), g1 = jh3*s^-1  [CORRECTED, THIS is the branch-B-2 quantity] ---\n");
Print("xi' = 1 ? ", IsOne(xiprime), "\n");
Print("xi' in gamma_4(Q)? ", xiprime in gamma4, "\n");

if not (eta in gamma4 and xi_raw in gamma4 and xiprime in gamma4) then
  Error("PRE2_STOP: D(jh4), D(jh3), or D(g1) does not land in gamma_4(Q) as PENT-HOM claims. STOP, report.");
fi;
if IsOne(eta) then
  Error("PRE2_STOP: eta = 1, contradicts NW-P5 (eta != 0). STOP, report.");
fi;

## ---- proportionality test in the F_7-vector space gamma_4(Q): eta vs xi_raw (diagnostic) ----
pcgsG4 := Pcgs(gamma4);;
Print("\nPcgs(gamma_4(Q)) length = ", Length(pcgsG4), " (expect 21)\n");
etaVec    := ExponentsOfPcElement(pcgsG4, eta);;
xiRawVec  := ExponentsOfPcElement(pcgsG4, xi_raw);;
xiPrimeVec:= ExponentsOfPcElement(pcgsG4, xiprime);;
sVec      := ExponentsOfPcElement(pcgsG4, sQ);;
Print("eta      exponent vector (F_7^21): ", etaVec, "\n");
Print("xi_raw   exponent vector (F_7^21) [diagnostic, = D(jh3), NOT g1]: ", xiRawVec, "\n");
Print("xi_prime exponent vector (F_7^21) [= D(g1), g1=jh3*s^-1, CORRECTED]: ", xiPrimeVec, "\n");
Print("s exponent vector (F_7^21) [sanity: should equal xi_raw - xi_prime mod 7]: ", sVec, "\n");
diffVec := List([1..21], i -> (xiRawVec[i] - xiPrimeVec[i]) mod 7);;
Print("xi_raw - xi_prime (mod 7, coordinatewise) == s exponent vector? ",
      diffVec = List(sVec, x -> x mod 7), "\n");

## proportionality test: xi_prime =? k*eta, for BOTH the diagnostic xi_raw and
## the corrected xi_prime (diagnostic printed for transparency; branch
## decision uses xi_prime only).
TestProportional := function(vecA, vecB, label)
  local i0, k, checkVec, proportional, mat, rk;
  i0 := First([1..Length(vecA)], i -> vecA[i] <> 0);;
  k := (vecB[i0] * (vecA[i0]^-1 mod 7)) mod 7;;
  checkVec := List([1..Length(vecA)], i -> (k*vecA[i]) mod 7);;
  proportional := (checkVec = List(vecB, x -> x mod 7));;
  mat := [ List(vecA, x -> x mod 7)*One(GF(7)), List(vecB, x -> x mod 7)*One(GF(7)) ];;
  rk := RankMat(mat);;
  Print("\n--- proportionality test: ", label, " ---\n");
  Print("first nonzero coord of eta: index ", i0, ", value ", vecA[i0], "\n");
  Print("candidate scalar k (vecB =? k*vecA), k = ", k, " (mod 7)\n");
  Print("vecB == k*vecA (mod 7) coordinatewise for all 21 coords? ", proportional, "\n");
  Print("RankMat([eta;vecB]) over GF(7) = ", rk, " (expect 1 iff proportional; eta<>0 so rank>=1)\n");
  if (rk = 1) <> proportional then
    Error("PRE2_STOP: coordinatewise scalar test and RankMat test disagree for ", label, ". STOP, report.");
  fi;
  return rec(i0 := i0, k := k, proportional := proportional, rk := rk);
end;;

diagResult := TestProportional(etaVec, xiRawVec, "eta vs xi_raw=D(jh3) [DIAGNOSTIC ONLY]");;
mainResult := TestProportional(etaVec, xiPrimeVec, "eta vs xi_prime=D(g1) [CORRECTED, BRANCH EVIDENCE]");;

Print("\n=== BRANCH DECISION (B-2), based on xi_prime = D(g1) ===\n");
if mainResult.proportional then
  Print("xi' in F_7*eta  ->  BRANCH B-2a : |pent(m)| = 7 (each non-empty layer), total 42\n");
else
  Print("xi' NOT in F_7*eta  ->  BRANCH B-2b : |pent(m)| = 1 (each non-empty layer), total 6\n");
fi;

Print("\nPRE2V2_RESULT branch=", (function() if mainResult.proportional then return "B-2a"; else return "B-2b"; fi; end)(),
      " k=", mainResult.k, " rank=", mainResult.rk, " eta_i0=", mainResult.i0,
      " diagnostic_xi_raw_proportional=", diagResult.proportional, "\n");

Print("PRE2V2_DONE\n");
QUIT;
