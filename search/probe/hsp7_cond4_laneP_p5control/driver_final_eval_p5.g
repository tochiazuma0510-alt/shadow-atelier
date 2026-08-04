## search/probe/hsp7_cond4_laneP_p5control/driver_final_eval_p5.g
## NW-P7 (p=5 control). Reads PQ_OUTPUT_P5.g / PQ_OUTPUT_Q5.g (ANUPQ's own reader,
## PQ_READ_AS_FUNC_WITH_VARS), rebuilds P5=F2/(gamma5(F2)F2^5) and
## Q5=K05fp/(gamma5(K05fp)K05fp^5), defines rho-bar on Q5 fresh, then:
##  - fail-closed pre-checks 1-4 (Sol指定, F102-1.4)
##  - main run: PENT_W(h4^t), t=0..4 (NW-P7 frozen family, exactly 5 candidates)

Read("search/probe/wac_v1/gap_output_prelude.g");
LoadPackage("anupq");

Print("=== NW-P7 driver_final_eval_p5: P5/Q5 construction + pre-checks 1-4 + main run ===\n");

## ---- rebuild F2 + h4 (same as driver_stepP1, p非依存の定義) ----
F := FreeGroup("x","y");;
x := F.1;; y := F.2;;
h4 := Comm(Comm(Comm(x,y),x),x) * Comm(Comm(Comm(x,y),x),y)^4
      * Comm(Comm(Comm(x,y),y),y);;

## ---- rebuild K05fp + j(x),j(y) + jh4/jh3 (same as driver_stepQ1, inherited stage1-2) ----
FB := FreeGroup("s1","s2","s3");;
s1 := FB.1;; s2 := FB.2;; s3 := FB.3;;
relsB := [ s1*s3*s1^-1*s3^-1,
           s1*s2*s1*(s2*s1*s2)^-1,
           s2*s3*s2*(s3*s2*s3)^-1 ];;
B4 := FB / relsB;;
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

## ---- read PQ_OUTPUT_P5.g (ANUPQ's own public reader) ----
## NOTE: the ANUPQ PQ_OUTPUT file literally hardcodes the global variable names
## "F" and "MapImages" as text (see PQ_OUTPUT_P5.g/PQ_OUTPUT_Q5.g). The var-name
## list argument of PQ_READ_AS_FUNC_WITH_VARS must match these literal names
## (this is not a free choice of local aliases); the p=7 Lane P driver used the
## same literal ["F","MapImages"] pair for the same reason.
outFileP := "search/probe/hsp7_cond4_laneP_p5control/PQ_OUTPUT_P5.g";;
resultP := PQ_READ_AS_FUNC_WITH_VARS(outFileP, ["F","MapImages"]);;
P5grp := resultP.F;;
mapImagesP := resultP.MapImages;;
Print("P5grp read. NumberOfGenerators(P5grp) = ", Length(GeneratorsOfGroup(P5grp)), " (expect 8, Witt(2,1..4)=2+1+2+3=8)\n");
epiP := GroupHomomorphismByImagesNC(F, P5grp, [x,y], mapImagesP);;
SetIsSurjective(epiP, true);;
Print("Image(epiP) = P5grp? ", Image(epiP) = P5grp, "\n");

sizeP := Size(P5grp);;
Print("own_measurement: |P5| = ", sizeP, " (expect 5^8 = ", 5^8, ")\n");
Print("own_measurement: |P5| = 5^8 ? ", sizeP = 5^8, "\n");

## ---- read PQ_OUTPUT_Q5.g ----
outFileQ := "search/probe/hsp7_cond4_laneP_p5control/PQ_OUTPUT_Q5.g";;
resultQ := PQ_READ_AS_FUNC_WITH_VARS(outFileQ, ["F","MapImages"]);;
Q5grp := resultQ.F;;
mapImagesQ := resultQ.MapImages;;
Print("Q5grp read. NumberOfGenerators(Q5grp) = ", Length(GeneratorsOfGroup(Q5grp)), " (expect 40)\n");
epiQ := GroupHomomorphismByImagesNC(K05fp, Q5grp, gK, mapImagesQ);;
SetIsSurjective(epiQ, true);;
Print("Image(epiQ) = Q5grp? ", Image(epiQ) = Q5grp, "\n");

sizeQ := Size(Q5grp);;
Print("own_measurement: |Q5| = ", sizeQ, " (expect 5^40 = ", 5^40, ")\n");
Print("own_measurement: |Q5| = 5^40 ? ", sizeQ = 5^40, "\n");

lcsQ := LowerCentralSeriesOfGroup(Q5grp);;
gamma5size := Size(lcsQ[5]);;
Print("own_measurement: |gamma_5(Q5)| = ", gamma5size, " (expect 1)\n");
gamma4size := Size(lcsQ[4]);;
dimGamma4 := LogInt(gamma4size, 5);;
Print("own_measurement: dim_F5 gamma_4(Q5) = ", dimGamma4, " (expect 21, Witt-derived same as p=7 case)\n");

## ---- rho-bar on Q5 ----
rhoImagesQ := List(rhoImages, w -> ImageElm(epiQ, w));;
epiGensQ := List(gK, g -> ImageElm(epiQ, g));;
Print("epiGensQ generate Q5grp? ", Subgroup(Q5grp, epiGensQ) = Q5grp, "\n");
rhoQ5 := GroupHomomorphismByImages(Q5grp, Q5grp, epiGensQ, rhoImagesQ);;
Print("rhoQ5 well-defined (GroupHomomorphismByImages did not fail)? ", rhoQ5 <> fail, "\n");
if rhoQ5 = fail then
  Error("STOP: rho-bar not well-defined on Q5. S-6 fires. INTEGRITY_STOP.");
fi;
rho5Bijective := IsBijective(rhoQ5);;
Print("own_measurement: rhoQ5 bijective? ", rho5Bijective, "\n");
rho5pow5 := rhoQ5*rhoQ5*rhoQ5*rhoQ5*rhoQ5;;
rho5pow5eqid := ForAll(epiGensQ, g -> ImageElm(rho5pow5,g) = g);;
Print("own_measurement: rhoQ5^5 = id? ", rho5pow5eqid, "\n");
rho5neqid := ForAny(epiGensQ, g -> ImageElm(rhoQ5,g) <> g);;
Print("own_measurement: rhoQ5 <> id? ", rho5neqid, "\n");

## ---- N_rho / PENT (same direct-order formula as Lane P cond4 calibration, p非依存) ----
NrhoQ5 := function(fbar)
  local r1, r2, r3, r4;
  r1 := ImageElm(rhoQ5, fbar);
  r2 := ImageElm(rhoQ5, r1);
  r3 := ImageElm(rhoQ5, r2);
  r4 := ImageElm(rhoQ5, r3);
  return r4*r3*r2*r1*fbar;
end;;
PENT5 := function(fbar)
  return IsOne(NrhoQ5(fbar));
end;;

## ==================== FAIL-CLOSED PRE-CHECKS 1-4 (Sol F102-1.4) ====================
Print("\n=== PRE-CHECK 1: h4 has order 5 in P5 ===\n");
h4inP5 := ImageElm(epiP, h4);;
h4_neq1_P5 := not IsOne(h4inP5);;
orderH4_P5 := Order(h4inP5);;
Print("h4 in P5: nontrivial? ", h4_neq1_P5, " ; Order(h4 in P5) = ", orderH4_P5, " (expect 5)\n");
precheck1_pass := h4_neq1_P5 and (orderH4_P5 = 5);;
Print("PRE-CHECK 1 PASS? ", precheck1_pass, "\n");

Print("\n=== PRE-CHECK 2: j(h4) is nontrivial and has order 5 in Q5 ===\n");
jh4Q5 := ImageElm(epiQ, jh4);;
jh4_neq1_Q5 := not IsOne(jh4Q5);;
orderJh4_Q5 := Order(jh4Q5);;
Print("j(h4) in Q5: nontrivial? ", jh4_neq1_Q5, " ; Order(j(h4) in Q5) = ", orderJh4_Q5, " (expect 5)\n");
precheck2_pass := jh4_neq1_Q5 and (orderJh4_Q5 = 5);;
Print("PRE-CHECK 2 PASS? ", precheck2_pass, "\n");

Print("\n=== PRE-CHECK 3: rho-bar is a well-defined bijection of order 5 on Q5 ===\n");
precheck3_pass := (rhoQ5 <> fail) and rho5Bijective and rho5pow5eqid and rho5neqid;;
Print("well-defined=", rhoQ5<>fail, " bijective=", rho5Bijective, " rho^5=id=", rho5pow5eqid, " rho<>id=", rho5neqid, "\n");
Print("PRE-CHECK 3 PASS? ", precheck3_pass, "\n");

Print("\n=== PRE-CHECK 4: candidates are exactly the frozen h4^t, t=0..4 (5 items) ===\n");
candidates_NWP7 := List([0..4], t -> rec(t := t, fbar := jh4Q5^t));;
precheck4_pass := (Length(candidates_NWP7) = 5) and ForAll([0..4], i -> candidates_NWP7[i+1].t = i);;
Print("candidate count = ", Length(candidates_NWP7), " (expect 5); t-list = ", List(candidates_NWP7, r->r.t), "\n");
Print("PRE-CHECK 4 PASS? ", precheck4_pass, "\n");

allPrechecksPass := precheck1_pass and precheck2_pass and precheck3_pass and precheck4_pass;;
Print("\n=== ALL PRE-CHECKS 1-4 PASS? ", allPrechecksPass, " ===\n");
if not allPrechecksPass then
  Error("STOP: fail-closed pre-check 1-4 failed. NW-P7 main run NOT executed. premise broken.");
fi;

## ==================== MAIN RUN: PENT_W(h4^t), t=0..4 ====================
Print("\n=== NW-P7 MAIN RUN: PENT_W(jh4^t), t=0..4 ===\n");
resultsNWP7 := [];;
for t in [0..4] do
  ft := jh4Q5^t;;
  verdict := PENT5(ft);;
  Print("t=", t, ": f=jh4^", t, " (order-5 element in Q5^", t, "), N_rho(f)=1 ? ", verdict, "\n");
  Add(resultsNWP7, rec(t := t, pent := verdict));
od;

nPass := Length(Filtered(resultsNWP7, r -> r.pent = true));;
Print("\n=== NW-P7 SUMMARY: ", nPass, "/5 PASS (prediction: 5/5) ===\n");
predictionMatch := (nPass = 5);;
Print("prediction match (5/5 PASS)? ", predictionMatch, "\n");
Print("S-3 fired (NOT 5/5)? ", not predictionMatch, "\n");

## ==================== third-mutant kill-by-p5 confirmation (IsOne(f) mutant) ====================
Print("\n=== third mutant (IsOne(f) instead of IsOne(N_rho(f))) evaluated on NW-P7 candidates ===\n");
resultsMutant3_p5 := [];;
for t in [0..4] do
  ft := jh4Q5^t;;
  realVerdict := PENT5(ft);;
  mutantVerdict := IsOne(ft);;
  Add(resultsMutant3_p5, rec(t:=t, real:=realVerdict, mutant:=mutantVerdict, mismatch := (realVerdict<>mutantVerdict)));
  Print("t=", t, ": real=", realVerdict, " mutant(IsOne(f))=", mutantVerdict, " mismatch=", realVerdict<>mutantVerdict, "\n");
od;
nMismatch3 := Length(Filtered(resultsMutant3_p5, r -> r.mismatch));;
Print("third mutant mismatches on NW-P7 (out of 5): ", nMismatch3, " (expect 4, i.e. t=1..4; t=0 both agree since f=1 there too)\n");

Print("\n=== SUMMARY ===\n");
Print("size_P5=", sizeP, "\n");
Print("size_Q5=", sizeQ, "\n");
Print("dim_gamma4_Q5_F5=", dimGamma4, "\n");
Print("gamma5_Q5_trivial=", gamma5size=1, "\n");
Print("precheck1=", precheck1_pass, " precheck2=", precheck2_pass, " precheck3=", precheck3_pass, " precheck4=", precheck4_pass, "\n");
Print("NWP7_pass_count=", nPass, "/5\n");
Print("third_mutant_mismatch_count=", nMismatch3, "/5\n");

Print("STAGE_FINAL_DONE\n");
QUIT;
