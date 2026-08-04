## search/probe/hsp7_cond4_laneP_p5control/driver_precheck5_mutants.g
## NW-P7 (p=5 control) fail-closed pre-check item 5 (Sol F102-1.4).
## Reuses the EXISTING p=7 Lane P fixture (search/probe/hsp7_cond4_laneP/PQ_OUTPUT_Q_laneP.g,
## already on disk from the cond4 calibration run, cert search/certs/hsp7_cond4_laneP_20260804.json)
## -- does not touch p=5 sealed content. Demonstrates two of the three named mutants firing
## on the p=7 negative example family (13 calibration candidates: dummy family h4^t t=0..6,
## h3 negative, NW-P8 m-sweep fbar=1 x5). The third mutant (IsOne(f) instead of
## IsOne(N_rho(f))) is NOT killed by this p=7 data (matches real evaluator on all 13 items --
## this is the exact discriminating-power argument of lanespec Appendix A-1); its kill is
## demonstrated separately in driver_final_eval_p5.g against the NW-P7 p=5 main run itself
## (4/5 mismatch there). See main-conversation ruling 2026-08-05 (SendMessage exchange) for
## the three-way split of which mutant is killed by which data.

Read("search/probe/wac_v1/gap_output_prelude.g");
LoadPackage("anupq");

Print("=== NW-P7 pre-check item 5: mutant-kill demonstration on p=7 existing fixture ===\n");

## ---- rebuild K05fp (p-independent, identical to search/probe/hsp7_cond4_laneP/driver_step1) ----
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

## ---- read the EXISTING p=7 Q output (already on disk, from the cond4 calibration run) ----
outFile := "search/probe/hsp7_cond4_laneP/PQ_OUTPUT_Q_laneP.g";;
result := PQ_READ_AS_FUNC_WITH_VARS(outFile, ["F","MapImages"]);;
Qgrp := result.F;;
mapImages := result.MapImages;;
Print("Qgrp (p=7 fixture) read. NumberOfGenerators = ", Length(GeneratorsOfGroup(Qgrp)), " (expect 40)\n");
epi := GroupHomomorphismByImagesNC(K05fp, Qgrp, gK, mapImages);;
SetIsSurjective(epi, true);;
sizeQ := Size(Qgrp);;
Print("|Q(p=7)| = ", sizeQ, " ; = 7^40 ? ", sizeQ = 7^40, " (structural sanity vs existing cert)\n");

rhoImagesQ := List(rhoImages, w -> ImageElm(epi, w));;
epiGens := List(gK, g -> ImageElm(epi, g));;
rhoQ := GroupHomomorphismByImages(Qgrp, Qgrp, epiGens, rhoImagesQ);;
if rhoQ = fail then
  Error("STOP: rho-bar not well-defined on p=7 fixture Q -- fixture itself broken, cannot run mutant test.");
fi;

jh4Q := ImageElm(epi, jh4);;
jh3Q := ImageElm(epi, jh3);;
oneQ := One(Qgrp);;

## ---- REAL evaluator (identical formula to driver_step3_eval_pent.g / driver_final_eval_p5.g) ----
NrhoQ_real := function(fbar)
  local r1, r2, r3, r4;
  r1 := ImageElm(rhoQ, fbar);
  r2 := ImageElm(rhoQ, r1);
  r3 := ImageElm(rhoQ, r2);
  r4 := ImageElm(rhoQ, r3);
  return r4*r3*r2*r1*fbar;
end;;
PENT_real := function(fbar)
  return IsOne(NrhoQ_real(fbar));
end;;

## ---- build the 13-item p=7 calibration candidate list (values only, from Lane S cert / lanespec SS6 C-5) ----
## dummy family h4^t, t=0..6 (7 items) + h3 negative (1 item) + NW-P8 m-sweep fbar=1 x5 (5 items) = 13
p7cand := [];;
for t in [0..6] do
  Add(p7cand, rec(key := Concatenation("h4^", String(t)), fbar := jh4Q^t,
                   family := "dummy", t := t));
od;
Add(p7cand, rec(key := "h3", fbar := jh3Q, family := "h3neg", t := fail));
for m in [1,2,4,5,6] do
  Add(p7cand, rec(key := Concatenation("NWP8-m", String(m)), fbar := oneQ,
                   family := "NWP8", t := fail));
od;
Print("p7 candidate count (should be 13, matching lanespec SS6 C-5): ", Length(p7cand), "\n");

## ground-truth verdicts, cross-checked against search/certs/hsp7_cond4_laneP_20260804.json
## lane_specific_results (t=0 PASS, t=1..6 FAIL, h3 FAIL, all NWP8 PASS)
for c in p7cand do
  c.real_verdict := PENT_real(c.fbar);;
od;
Print("real evaluator verdicts (recomputed fresh in this driver, independent re-derivation): \n");
for c in p7cand do
  Print("  ", c.key, ": ", c.real_verdict, "\n");
od;

## sanity cross-check against the recorded cert values (13 known verdicts)
knownVerdicts := rec();;
knownVerdicts.(  "h4^0") := true;;  knownVerdicts.(  "h4^1") := false;;
knownVerdicts.(  "h4^2") := false;; knownVerdicts.(  "h4^3") := false;;
knownVerdicts.(  "h4^4") := false;; knownVerdicts.(  "h4^5") := false;;
knownVerdicts.(  "h4^6") := false;; knownVerdicts.(  "h3")   := false;;
knownVerdicts.(  "NWP8-m1") := true;; knownVerdicts.(  "NWP8-m2") := true;;
knownVerdicts.(  "NWP8-m4") := true;; knownVerdicts.(  "NWP8-m5") := true;;
knownVerdicts.(  "NWP8-m6") := true;;
nSanityMismatch := 0;;
for c in p7cand do
  if c.real_verdict <> knownVerdicts.(c.key) then
    nSanityMismatch := nSanityMismatch + 1;
    Print("  SANITY MISMATCH at ", c.key, ": recomputed=", c.real_verdict, " cert=", knownVerdicts.(c.key), "\n");
  fi;
od;
Print("sanity cross-check vs existing cert (should be 0 mismatches): ", nSanityMismatch, "\n");
if nSanityMismatch > 0 then
  Error("STOP: recomputed p=7 verdicts disagree with existing cert. Fixture or code drift -- do not proceed.");
fi;

## ==================== MUTANT 1: "always PASS" (evaluation-function mutant) ====================
## source-map: replaces the body of PENT_real (line "return IsOne(NrhoQ_real(fbar));") with
## "return true;" unconditionally -- i.e. mutates the RETURN of the PENT function itself.
PENT_mutant_alwayspass := function(fbar)
  return true;
end;;
Print("\n=== MUTANT 1 (always PASS, evaluation-function mutant) ===\n");
Print("source-map: driver_step3_eval_pent.g / driver_final_eval_p5.g, function PENT(fbar) body\n");
Print("  real:   return IsOne(NrhoQ(fbar));\n");
Print("  mutant: return true;\n");
nMismatch1 := 0;;
for c in p7cand do
  mv := PENT_mutant_alwayspass(c.fbar);;
  if mv <> c.real_verdict then nMismatch1 := nMismatch1 + 1; fi;
od;
Print("mutant 1 verdict mismatches vs real evaluator (out of 13 p=7 candidates): ", nMismatch1, "\n");
Print("mutant 1 FIRED (verdict-mismatch fail-closed check trips)? ", nMismatch1 > 0, "\n");

## ==================== MUTANT 2: "identity-input-only enumeration" (candidate-generation mutant) ====================
## source-map: replaces the family-generation loop
##   "for t in [0..6] do ... Add(resultsNWP6, ...) od;"  (driver_step3_eval_pent.g line ~121)
## with "for t in [0] do ... od;" -- i.e. mutates the ENUMERATION bound, not the evaluation.
## Applying the identical mutation pattern to the dummy family that appears in this p=7
## fixture (7-member family) to demonstrate the count-check catches it structurally
## (this is the same defense mechanism as pre-check item 4 in driver_final_eval_p5.g).
p7_dummy_family_real := Filtered(p7cand, c -> c.family = "dummy");;
p7_dummy_family_mutant := Filtered(p7_dummy_family_real, c -> c.t = 0);;  ## mutant: "for t in [0]" only
Print("\n=== MUTANT 2 (identity-input-only enumeration, candidate-generation mutant) ===\n");
Print("source-map: driver_step3_eval_pent.g line ~121 'for t in [0..6] do' -> mutant 'for t in [0] do'\n");
Print("real enumerator candidate count (dummy family): ", Length(p7_dummy_family_real), " (expect 7)\n");
Print("mutant enumerator candidate count (dummy family): ", Length(p7_dummy_family_mutant), " (expect 1)\n");
countMismatch2 := Length(p7_dummy_family_real) <> Length(p7_dummy_family_mutant);;
Print("mutant 2 FIRED (frozen-count fail-closed check trips, same mechanism as pre-check item 4)? ", countMismatch2, "\n");

Print("\n=== SUMMARY (pre-check item 5) ===\n");
Print("mutant1_always_pass: nMismatch=", nMismatch1, "/13, fired=", nMismatch1>0, "\n");
Print("mutant2_identity_only_enum: count_real=", Length(p7_dummy_family_real), " count_mutant=", Length(p7_dummy_family_mutant), " fired=", countMismatch2, "\n");
Print("mutant3_IsOne_f_evaluator: NOT killed by p=7 data (see note in file header); killed_by=NW-P7 p=5 main run (driver_final_eval_p5.g), 4/5 mismatch there\n");
Print("mutant3_p7_check_for_completeness (should show 0 mismatch -> confirms NOT killed by p=7):\n");
nMismatch3_p7 := 0;;
for c in p7cand do
  mv3 := IsOne(c.fbar);;
  if mv3 <> c.real_verdict then nMismatch3_p7 := nMismatch3_p7 + 1; fi;
od;
Print("mutant3 (IsOne(f)) verdict mismatches vs real evaluator on p=7 fixture (out of 13): ", nMismatch3_p7, " (expect 0 -- confirms this mutant is invisible to p=7 data alone)\n");

Print("STAGE_PRECHECK5_DONE\n");
QUIT;
