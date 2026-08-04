## search/probe/hsp7_cond4_laneP/driver_step3_eval_pent.g
## Lane P, HS 発火条件4較正走. Reads the PQ_OUTPUT produced by ANUPQ's own pq
## standalone (driver_step2), rebuilds K05fp (inherited stage1-2), builds
## Q=K05fp/W as a PcGroup with its ANUPQ epimorphism (ANUPQ's own public
## reader PQ_READ_AS_FUNC_WITH_VARS -- not a self-written parser, 付録B),
## defines rho-bar on Q fresh (not stage4 code), verifies structural anchors,
## then evaluates PENT_W on all Lane P calibration candidates.

Read("search/probe/wac_v1/gap_output_prelude.g");
LoadPackage("anupq");

Print("=== Lane P driver_step3: Q construction + PENT_W evaluation ===\n");

## ---- rebuild K05fp + j(x),j(y) + h4/h3 words (same as driver_step1, inherited stage1-2) ----
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

## ---- new (Lane P): read PQ_OUTPUT via ANUPQ's own public reader ----
outFile := "search/probe/hsp7_cond4_laneP/PQ_OUTPUT_Q_laneP.g";;
result := PQ_READ_AS_FUNC_WITH_VARS(outFile, ["F","MapImages"]);;
Qgrp := result.F;;
mapImages := result.MapImages;;
Print("Qgrp read. NumberOfGenerators(Qgrp) = ", Length(GeneratorsOfGroup(Qgrp)), " (expect 40)\n");

epi := GroupHomomorphismByImagesNC(K05fp, Qgrp, gK, mapImages);;
SetIsSurjective(epi, true);;
Qcheck := Image(epi);;
Print("Image(epi) = Qgrp? ", Qcheck = Qgrp, "\n");

## ---- structural anchors (own measurement, fresh -- S-7' equivalent for Lane P) ----
sizeQ := Size(Qgrp);;
Print("own_measurement: |Q| = ", sizeQ, "\n");
Print("own_measurement: |Q| = 7^40 ? ", sizeQ = 7^40, "\n");

lcsQ := LowerCentralSeriesOfGroup(Qgrp);;
Print("own_measurement: length(LCS) = ", Length(lcsQ), " (gamma_1..gamma_k, expect gamma_5 trivial)\n");
gamma4size := Size(lcsQ[4]);;
gamma5size := Size(lcsQ[5]);;
Print("own_measurement: |gamma_4(Q)| = ", gamma4size, "\n");
Print("own_measurement: |gamma_5(Q)| = ", gamma5size, " (expect 1)\n");
Print("own_measurement: gamma_5(Q) trivial? ", gamma5size = 1, "\n");
dimGamma4 := LogInt(gamma4size, 7);;
Print("own_measurement: dim_F7 gamma_4(Q) = ", dimGamma4, " (expect 21)\n");

## rho-bar on Q: images of the 6 generators of K05fp under rho, pushed through epi.
rhoImagesQ := List(rhoImages, w -> ImageElm(epi, w));;
epiGens := List(gK, g -> ImageElm(epi, g));;
Print("epiGens generate Qgrp? ", Subgroup(Qgrp, epiGens) = Qgrp, "\n");

rhoQ := GroupHomomorphismByImages(Qgrp, Qgrp, epiGens, rhoImagesQ);;
Print("rhoQ well-defined (GroupHomomorphismByImages did not fail)? ", rhoQ <> fail, "\n");
if rhoQ = fail then
  Error("STAGE3_STOP: rho-bar not well-defined on Q. S-6 fires. INTEGRITY_STOP.");
fi;

rhoBijective := IsBijective(rhoQ);;
Print("own_measurement: rhoQ bijective? ", rhoBijective, "\n");

rhoId := IdentityMapping(Qgrp);;
rho5 := rhoQ*rhoQ*rhoQ*rhoQ*rhoQ;;
Print("own_measurement: rhoQ^5 = id? ", ForAll(epiGens, g -> ImageElm(rho5,g) = g), "\n");
Print("own_measurement: rhoQ <> id? ", ForAny(epiGens, g -> ImageElm(rhoQ,g) <> g), "\n");

## ---- j(h4), j(h3) in Q ----
jh4Q := ImageElm(epi, jh4);;
jh3Q := ImageElm(epi, jh3);;
Print("j(h4) = identity in Q? ", IsOne(jh4Q), " (expect false)\n");
Print("j(h3) = identity in Q? ", IsOne(jh3Q), "\n");

## ---- N_rho helper: N_rho(fbar) := rho^4(fbar) rho^3(fbar) rho^2(fbar) rho(fbar) fbar ----
## Direct order (our own PENT-NORM formula, standard left-to-right group
## multiplication -- not a literal HS transcription, so no W-1 reversal here;
## this mirrors how hsp7_cond2_p7_20260804.json computed N_rho(j(h4)) (same
## direct order, independently confirmed correct against NW-P5 prediction).
NrhoQ := function(fbar)
  local r1, r2, r3, r4;
  r1 := ImageElm(rhoQ, fbar);
  r2 := ImageElm(rhoQ, r1);
  r3 := ImageElm(rhoQ, r2);
  r4 := ImageElm(rhoQ, r3);
  return r4*r3*r2*r1*fbar;
end;;

PENT := function(fbar)
  return IsOne(NrhoQ(fbar));
end;;

Print("\n--- NW-P6: dummy family h4^t, t=0..6 ---\n");
resultsNWP6 := [];;
for t in [0..6] do
  ft := jh4Q^t;;
  verdict := PENT(ft);;
  Print("t=", t, ": f=jh4^", t, ", N_rho(f)=1 ? ", verdict, "\n");
  Add(resultsNWP6, rec(t := t, pent := verdict));
od;

Print("\n--- h3 negative example PENT ---\n");
h3verdict := PENT(jh3Q);;
Print("h3: N_rho(j(h3))=1 ? ", h3verdict, "\n");

Print("\n--- NW-P8 PENT side: m in {1,2,4,5,6}, fbar=1 (trivial) ---\n");
oneQ := One(Qgrp);;
oneVerdict := PENT(oneQ);;
Print("PENT(1) = ", oneVerdict, " (expect true, m-independent per HSP-WD)\n");
resultsNWP8 := [];;
for m in [1,2,4,5,6] do
  Add(resultsNWP8, rec(m := m, pent := oneVerdict));
  Print("m=", m, ", fbar=1: PENT = ", oneVerdict, "\n");
od;

Print("\n=== SUMMARY ===\n");
Print("size_Q=", sizeQ, "\n");
Print("dim_gamma4_Q_F7=", dimGamma4, "\n");
Print("gamma5_Q_trivial=", gamma5size=1, "\n");
Print("rho_bijective=", rhoBijective, "\n");
Print("jh4_neq_1=", not IsOne(jh4Q), "\n");
Print("jh3_neq_1=", not IsOne(jh3Q), "\n");

Print("STAGE3_DONE\n");
QUIT;
