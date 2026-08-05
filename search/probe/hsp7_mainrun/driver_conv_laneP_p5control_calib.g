## search/probe/hsp7_mainrun/driver_conv_laneP_p5control_calib.g
## Lane P CONV-P re-calibration driver (裁定527発火・implementer, 2026-08-05).
## Re-runs the 5 registered p5control fixtures (NW-P7, t=0..4) through the
## CONV-P translation path (predicate_lib_laneP_conv.g) instead of the
## baseline's native jh4Q5^t words. Read-only w.r.t. the baseline:
## driver_final_eval_p5.g / predicate_lib_laneP.g's construction pattern is
## reproduced here (same P5/Q5/rho-bar/PENT5 construction, byte-identical
## group-theoretic content) but the CANDIDATE is now obtained by:
##   h4bar (in P5) --Pcgs(D5) exponent vector--> CONV-P --> Q5 element
## instead of being handed directly as jh4Q5 (a native K05fp/Q5 word). This
## is exactly the CONV-P conversion the note (SS1.4 接続ゲート) requires be
## checked, extended here from the p=7 window (where the note wrote it) to
## the p=5 control window (since p5control_5 is one of the 18 registered
## fixtures slated for CF/CONV-P re-calibration).
##
## Prints log lines in the SAME format driver_final_eval_p5.g used (the
## "=== NW-P7 MAIN RUN ===" block + "t=<t>: f=jh4^<t> (order-5 element in
## Q5^<t>), N_rho(f)=1 ? <bool>" lines), so
## search/probe/hsp7_ci_calib/parse_and_compare.py (unmodified) parses this
## driver's log exactly as it parses the baseline's.
Read("search/probe/wac_v1/gap_output_prelude.g");
LoadPackage("anupq");
Read("search/probe/hsp7_mainrun/predicate_lib_laneP_conv.g");    ## CONV-P (new)

Print("=== driver_conv_laneP_p5control_calib: P5/Q5 construction + CONV-P + NW-P7 main run ===\n");

## ---- rebuild F2 + h4 (same as driver_final_eval_p5.g, p非依存の定義) ----
F := FreeGroup("x","y");;
x := F.1;; y := F.2;;
h4 := Comm(Comm(Comm(x,y),x),x) * Comm(Comm(Comm(x,y),x),y)^4
      * Comm(Comm(Comm(x,y),y),y);;

## ---- rebuild K05fp + j(x),j(y) + jh4/jh3 (identical to driver_final_eval_p5.g) ----
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

## ---- read PQ_OUTPUT_P5.g / PQ_OUTPUT_Q5.g (identical to driver_final_eval_p5.g) ----
outFileP := "search/probe/hsp7_cond4_laneP_p5control/PQ_OUTPUT_P5.g";;
resultP := PQ_READ_AS_FUNC_WITH_VARS(outFileP, ["F","MapImages"]);;
P5grp := resultP.F;;
mapImagesP := resultP.MapImages;;
Print("P5grp read. NumberOfGenerators(P5grp) = ", Length(GeneratorsOfGroup(P5grp)), " (expect 8)\n");
epiP := GroupHomomorphismByImagesNC(F, P5grp, [x,y], mapImagesP);;
SetIsSurjective(epiP, true);;
Print("Image(epiP) = P5grp? ", Image(epiP) = P5grp, "\n");

sizeP := Size(P5grp);;
Print("own_measurement: |P5| = ", sizeP, " (expect 5^8 = ", 5^8, ")\n");

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

## ---- rho-bar on Q5 + PENT5 (identical formulas to driver_final_eval_p5.g) ----
rhoImagesQ := List(rhoImages, w -> ImageElm(epiQ, w));;
epiGensQ := List(gK, g -> ImageElm(epiQ, g));;
rhoQ5 := GroupHomomorphismByImages(Q5grp, Q5grp, epiGensQ, rhoImagesQ);;
if rhoQ5 = fail then
  Error("STOP: rho-bar not well-defined on Q5. S-6 fires. INTEGRITY_STOP.");
fi;
Print("rhoQ5 well-defined? ", rhoQ5 <> fail, "\n");

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

## ==================== CONV-P precompute (one-time, 6 PreImagesRepresentative calls) ====================
xbar5 := mapImagesP[1];;  ybar5 := mapImagesP[2];;
Print("\n=== CONV-P precompute (P5, D5=[P5,P5]) ===\n");
t0 := Runtime();;
convData := BuildConvP(P5grp, xbar5, ybar5, jx, jy, epiQ);;
t1 := Runtime();;
convSetupTime_ms := t1 - t0;;
Print("CONV-P setup time (6x PreImagesRepresentative + 6x Q5 evaluation): ", convSetupTime_ms, " ms\n");
Print("RelativeOrders(pcgsD5) = ", RelativeOrders(convData.pcgsD), " (expect [5,5,5,5,5,5])\n\n");

## ==================== connection gate (note SS1.4, extended to p=5 window) ====================
## h4bar (in P5) must be an element of D5=[P5,P5] (true: h4 is a weight-4
## commutator, lies in gamma_4(F2)N/N subset [P,P]). Its CONV-P image must
## equal jh4Q5 = ImageElm(epiQ, jh4) (the native word already used by the
## baseline driver) -- for t=0..4 (the NW-P7 frozen family) and also t=5,6
## (extending the note's t=0..6 check, cheap and free once precompute is
## done, no extra PreImagesRepresentative calls).
h4inP5 := ImageElm(epiP, h4);;
jh4Q5 := ImageElm(epiQ, jh4);;
Print("=== connection gate: CONV-P(h4bar^t) = jh4Q5^t ? (t=0..6) ===\n");
gateMismatch := 0;;
for t in [0..6] do
  convImg := ConvPElement(convData, h4inP5^t);;
  nativeImg := jh4Q5^t;;
  ok := (convImg = nativeImg);;
  if not ok then gateMismatch := gateMismatch + 1; fi;
  Print("t=", t, ": CONV-P(h4bar^", t, ") = jh4Q5^", t, " ? ", ok, "\n");
od;
Print("connection gate mismatches = ", gateMismatch, " / 7\n");
if gateMismatch > 0 then
  Error("CONNECTION_GATE_STOP: CONV-P disagrees with the native jh4Q5 path -- do not proceed to main run.");
fi;
Print("[GATE PASS] CONV-P reproduces the native Q5 element for h4bar^t, t=0..6.\n\n");

## ==================== MAIN RUN: PENT5(CONV-P(h4bar^t)), t=0..4, two-path timed ====================
Print("=== NW-P7 MAIN RUN ===\n");
resultsNWP7 := [];;
convTimes := [];;
nativeTimes := [];;
twoPathMismatch := 0;;
for t in [0..4] do
  tA := Runtime();;
  ftConv := ConvPElement(convData, h4inP5^t);;
  verdictConv := PENT5(ftConv);;
  tB := Runtime();;
  Add(convTimes, tB - tA);

  tA := Runtime();;
  ftNative := jh4Q5^t;;
  verdictNative := PENT5(ftNative);;
  tB := Runtime();;
  Add(nativeTimes, tB - tA);

  if verdictConv <> verdictNative then
    twoPathMismatch := twoPathMismatch + 1;
    Print("TWO_PATH_MISMATCH at t=", t, ": conv=", verdictConv, " native=", verdictNative, "\n");
  fi;
  Print("t=", t, ": f=jh4^", t, " (order-5 element in Q5^", t, "), N_rho(f)=1 ? ", verdictConv, "\n");
  Add(resultsNWP7, rec(t := t, pent := verdictConv, pent_native := verdictNative));
od;

nPass := Length(Filtered(resultsNWP7, r -> r.pent = true));;
Print("\n=== NW-P7 SUMMARY: ", nPass, "/5 PASS (prediction: 5/5) ===\n");
Print("two-path mismatch count (CONV-P vs native jh4Q5, 5 candidates) = ", twoPathMismatch, "\n");

## ---- timing: single pass (coarse) + repeated benchmark ----
avgConv := Sum(convTimes) / Length(convTimes);;
avgNative := Sum(nativeTimes) / Length(nativeTimes);;
Print("\n=== TIMING single-pass ===\n");
Print("avg CONV-P (translation+PENT5) = ", avgConv, " ms/candidate\n");
Print("avg native (jh4Q5^t + PENT5) = ", avgNative, " ms/candidate\n");
Print("raw CONV-P times (ms): ", convTimes, "\n");
Print("raw native times (ms): ", nativeTimes, "\n");

REPS := 500;;
t0 := Runtime();;
for rep in [1..REPS] do
  for t in [0..4] do
    dummy1 := PENT5(ConvPElement(convData, h4inP5^t));
  od;
od;
t1 := Runtime();;
totalConv_ms := t1 - t0;;
perCandConv_ms := totalConv_ms / (REPS*5);;

t0 := Runtime();;
for rep in [1..REPS] do
  for t in [0..4] do
    dummy2 := PENT5(jh4Q5^t);
  od;
od;
t1 := Runtime();;
totalNative_ms := t1 - t0;;
perCandNative_ms := totalNative_ms / (REPS*5);;

Print("\n=== TIMING repeated benchmark (REPS=", REPS, ", 5 candidates, includes PENT5 both sides) ===\n");
Print("total CONV-P(+PENT5) time = ", totalConv_ms, " ms over ", REPS*5, " calls => per-candidate = ", perCandConv_ms, " ms\n");
Print("total native(+PENT5) time = ", totalNative_ms, " ms over ", REPS*5, " calls => per-candidate = ", perCandNative_ms, " ms\n");
Print("NOTE: PENT5 itself (4x ImageElm on rhoQ5, shared by both paths) dominates here -- CONV-P's OWN\n");
Print("      marginal cost is (perCandConv_ms - perCandNative_ms) relative to the translation step only,\n");
Print("      since the native path has zero translation cost by construction (jh4Q5 already IS a Q5 word).\n");
Print("      This benchmark measures CONV-P's translation overhead added on top of a shared PENT5 call,\n");
Print("      NOT a baseline-vs-CF reduction factor (unlike Lane V, Lane P's baseline had no per-candidate\n");
Print("      translation step to begin with for h4/h3 -- the note's SS1.5 cost table (<=23 pc multiplications\n");
Print("      per candidate) is the intended comparison point, not this native-word special case).\n");

Print("\n=== SUMMARY ===\n");
Print("size_P5=", sizeP, "\n");
Print("size_Q5=", sizeQ, "\n");
Print("NWP7_pass_count=", nPass, "/5\n");
Print("connection_gate_mismatch=", gateMismatch, "/7\n");
Print("two_path_mismatch=", twoPathMismatch, "/5\n");
Print("conv_p_setup_time_ms=", convSetupTime_ms, "\n");
Print("per_candidate_conv_ms=", perCandConv_ms, "\n");
Print("per_candidate_native_ms=", perCandNative_ms, "\n");

Print("\nSTAGE_FINAL_DONE\n");
QUIT;
