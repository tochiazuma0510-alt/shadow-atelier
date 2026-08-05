## search/probe/hsp7_cond4_laneP/pre2_xi_b2_20260805.g
## PRE-2 (docs/notes/nw7_mainrun_predictions_iffirst_v1.md sec.5, table row PRE-2;
## authorized by 裁定 554).
##
## Computes xi = D(g1), g1 = the raw Hall-commutator lift jh3 of h3=u1+u2
## (justified: PRE-1 (search/probe/hsp7_v1/pre1_psi_b1_20260805.py) found
## Psi = 0 EXACTLY over Q, so no gamma_4(P) correction is needed -- jh3 as
## already built and used in driver_step3_eval_pent.g IS an exact hexagon
## solution's Hall-commutator representative; PENT-HOM's ambiguity concern
## does not arise here), and decides branch B-2 of the prediction ticket:
##
##   boxed criterion (ticket sec.4.2):
##       |pent(m)| = 7  <=>  xi in F_7 * eta   (eta = D(h4), NW-P5, known != 0)
##       |pent(m)| = 1  otherwise
##
## This rebuilds the SAME Q = K(0,5)/W construction as
## search/probe/hsp7_cond4_laneP/driver_step3_eval_pent.g (own fresh
## measurement, same public ANUPQ reader, same anchors) rather than Read()-ing
## that file directly (it QUITs at the end). No modification of that file.
## Scope discipline: this is a single-point computation in the ALREADY-BUILT
## Q (order 7^40) -- NOT a re-run of the 705,894-candidate universe.

Read("search/probe/wac_v1/gap_output_prelude.g");
LoadPackage("anupq");

Print("=== PRE-2: xi = D(jh3) vs eta = D(jh4) in gamma_4(Q) ===\n");

## ---- rebuild K05fp + j(x),j(y) + h4/h3 words (verbatim reproduction of
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

## ---- j(h4), j(h3) in Q ----
jh4Q := ImageElm(epi, jh4);;
jh3Q := ImageElm(epi, jh3);;
Print("j(h4) = identity in Q? ", IsOne(jh4Q), " (expect false)\n");
Print("j(h3) = identity in Q? ", IsOne(jh3Q), " (expect false)\n");

## ---- D = N_rho (verbatim same operator as driver_step3's NrhoQ / PENT) ----
DfnQ := function(fbar)
  local r1, r2, r3, r4;
  r1 := ImageElm(rhoQ, fbar);
  r2 := ImageElm(rhoQ, r1);
  r3 := ImageElm(rhoQ, r2);
  r4 := ImageElm(rhoQ, r3);
  return r4*r3*r2*r1*fbar;
end;;

eta := DfnQ(jh4Q);;   # = D(h4), NW-P5 quantity
xi  := DfnQ(jh3Q);;   # = D(g1), g1 = jh3 (justified above: Psi=0)

Print("\n--- eta = D(jh4) ---\n");
Print("eta = 1 ? ", IsOne(eta), " (expect false, per NW-P5 / driver_step3 t=1 case)\n");
Print("eta in gamma_4(Q)? ", eta in gamma4, "\n");

Print("\n--- xi = D(jh3) ---\n");
Print("xi = 1 ? ", IsOne(xi), " (driver_step3 recorded: false)\n");
Print("xi in gamma_4(Q)? ", xi in gamma4, "\n");

if not (eta in gamma4 and xi in gamma4) then
  Error("PRE2_STOP: D(jh4) or D(jh3) does not land in gamma_4(Q) as PENT-HOM claims. STOP, report.");
fi;
if IsOne(eta) then
  Error("PRE2_STOP: eta = 1, contradicts NW-P5 (eta != 0). STOP, report.");
fi;

## ---- proportionality test in the F_7-vector space gamma_4(Q) ----
pcgsG4 := Pcgs(gamma4);;
Print("\nPcgs(gamma_4(Q)) length = ", Length(pcgsG4), " (expect 21)\n");
etaVec := ExponentsOfPcElement(pcgsG4, eta);;
xiVec  := ExponentsOfPcElement(pcgsG4, xi);;
Print("eta exponent vector (F_7^21): ", etaVec, "\n");
Print("xi  exponent vector (F_7^21): ", xiVec, "\n");

## find first nonzero coordinate of eta, compute candidate scalar k with xi =? k*eta
i0 := First([1..Length(etaVec)], i -> etaVec[i] <> 0);;
Print("first nonzero coord of eta: index ", i0, ", value ", etaVec[i0], "\n");
k := (xiVec[i0] * (etaVec[i0]^-1 mod 7)) mod 7;;
Print("candidate scalar k (xi =? k*eta), k = ", k, " (mod 7)\n");

checkVec := List([1..Length(etaVec)], i -> (k*etaVec[i]) mod 7);;
proportional := (checkVec = List(xiVec, x -> x mod 7));;
Print("xi == k*eta (mod 7) coordinatewise for all 21 coords? ", proportional, "\n");

## rank-based cross-check (independent of choice of i0): rank of the 2x21
## matrix [eta;xi] over GF(7) should be 1 iff proportional (and eta<>0).
mat := [ List(etaVec, x -> x mod 7)*One(GF(7)), List(xiVec, x -> x mod 7)*One(GF(7)) ];;
rk := RankMat(mat);;
Print("RankMat([eta;xi]) over GF(7) = ", rk, " (expect 1 iff proportional; eta<>0 so rank>=1)\n");
if (rk = 1) <> proportional then
  Error("PRE2_STOP: coordinatewise scalar test and RankMat test disagree. STOP, report.");
fi;

Print("\n=== BRANCH DECISION (B-2) ===\n");
if proportional then
  Print("xi in F_7*eta  ->  BRANCH B-2a : |pent(m)| = 7 (each non-empty layer), total 42\n");
else
  Print("xi NOT in F_7*eta  ->  BRANCH B-2b : |pent(m)| = 1 (each non-empty layer), total 6\n");
fi;

Print("\nPRE2_RESULT branch=", (function() if proportional then return "B-2a"; else return "B-2b"; fi; end)(),
      " k=", k, " rank=", rk, " eta_i0=", i0, "\n");

Print("PRE2_DONE\n");
QUIT;
