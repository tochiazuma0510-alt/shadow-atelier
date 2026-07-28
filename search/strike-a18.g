#############################################################################
## search/strike-a18.g -- WA-c second-strike driver for W-D-A18-13a
## (裁定195 工程2)
##
## Generators MACHINE-TRANSCRIBED (not hand-copied) from
## docs/notes/wac_second_strike_v1.md S1.2 -- both the (a1,b1) generating
## pair AND the literal JUDGE_S1_IMG/JUDGE_S2_IMG permutations given there
## are embedded verbatim below; STAGE 1 includes an assert that the two
## independently-transcribed representations (the one built here from
## (a1,b1) via the Prop 0.3 embedding, and the literal JUDGE_S1_IMG/
## JUDGE_S2_IMG lines from the slate) agree exactly.
##
## E = A18 x S3 (21-point permutation group), P = ker(E ->> S3) = A18,
## s1 = b^-1*a, s2 = a^-1*b^2 (same construction pattern as
## search/strike-a16.g / search/probe/wac_v1/ss_alt2.g).
##
## STAGE 1 (run here, locally): window assertions -- braid relation, c in N,
## P = A18, N_ord=13, C_P(ybar)/Stab_{Aut(P)}(xbar) both non-solvable with
## the slate's stated orders (780/1560), AND the transcription-consistency
## assert described above. Fail-closed throughout.
##
## STAGE 2: connects to kerchi-judge.g v1.3 (JUDGE_FORCE_SCAN_MODE :=
## "xi_restricted" forced -- |[P,P]|=|A18| makes legacy infeasible). Only a
## SINGLE charming-m layer is run locally here, for timing/extrapolation.
## The FULL stage-2 run is gated behind STRIKE_RUN_STAGE2 and is NOT
## triggered by this script by default -- awaits the coordinator's
## go-ahead, per the recommended launch order (2 -> 1 -> 3, i.e. Sp45 then
## A20 then A18) in the slate doc S3.
## JUDGE_SKIP_LEGACY_CROSSCHECK is set unconditionally in that gated block
## (lesson from the W-D-A16-11a CI hang: the
## crosscheck_vs_EnumerateReducedHexagon path is infeasible for any P this
## large and must be disabled before any full run).
##
## Output: search/certs/strike_a18_stage1_20260729.json
#############################################################################

Read("search/gaplib_common.g");

JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");

STAGE1_ASSERTS := [];;
StageAssert := function(label, ok)
  Add(STAGE1_ASSERTS, rec(label := label, ok := ok));
  Print("[", PF(ok), "] ", label, "\n");
  if not ok then
    Print("*** STAGE 1 ASSERT FAILED: ", label, " -- refusing to proceed to stage 2 ***\n");
  fi;
  return ok;
end;;

#############################################################################
## ---------------------- window construction (machine-transcribed) ---------
## Source: docs/notes/wac_second_strike_v1.md S1.2 "W-D-A18-13a"
#############################################################################
Print("=== strike-a18: building W-D-A18-13a ===\n");
a1 := ( 1,17)( 2, 6)( 3,14)( 5,15)( 7,16)( 8,13)(10,12)(11,18);;   # 2^8 1^2
b1 := ( 1,16, 6)( 2, 5,14)( 3,15, 4)( 7,17,13)( 8,12, 9)(10,11,18);; # 3^6
A18 := AlternatingGroup(18);;  S18 := SymmetricGroup(18);;
S3 := SymmetricGroup(3);;
Dgrp := DirectProduct(A18, S3);;
embA := Embedding(Dgrp, 1);;  embS := Embedding(Dgrp, 2);;
agen := Image(embA, a1) * Image(embS, (1,3));;
bgen := Image(embA, b1) * Image(embS, (1,3,2));;
s1 := bgen^-1 * agen;;
s2 := agen^-1 * bgen^2;;

Print("degree of E = ", LargestMovedPoint(Dgrp), " (expect 21)\n");
Print("computed s1 := ", s1, ";;\n");
Print("computed s2 := ", s2, ";;\n");

# literal slate lines, machine-transcribed verbatim from S1.2 of the slate doc:
JUDGE_S1_IMG_SLATE := ( 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13)(14,15)(16,17)(19,20);;
JUDGE_S2_IMG_SLATE := ( 1, 7)( 2,16,13, 9,12,18,10, 8,17, 6,14, 4,15)( 3, 5)(20,21);;

#############################################################################
## ---------------------- STAGE 1: window assertions -------------------------
#############################################################################
Print("\n=== STAGE 1: window assertions ===\n");
allStage1Ok := true;;

allStage1Ok := StageAssert("<a1,b1> = A18", Group(a1,b1) = A18) and allStage1Ok;
allStage1Ok := StageAssert("a1^2=1 and b1^3=1", a1^2 = () and b1^3 = ()) and allStage1Ok;
allStage1Ok := StageAssert("braid relation s1*s2*s1 = s2*s1*s2",
                           s1*s2*s1 = s2*s1*s2) and allStage1Ok;

# *** transcription-consistency assert (this task's specific requirement) ***
allStage1Ok := StageAssert("computed s1 (from a1,b1 via Prop 0.3) = literal JUDGE_S1_IMG from the slate",
                           s1 = JUDGE_S1_IMG_SLATE) and allStage1Ok;
allStage1Ok := StageAssert("computed s2 (from a1,b1 via Prop 0.3) = literal JUDGE_S2_IMG from the slate",
                           s2 = JUDGE_S2_IMG_SLATE) and allStage1Ok;

W := MakeWindow(s1, s2);;
allStage1Ok := StageAssert("c in N (c = identity in Bq)",
                           W.c = Identity(W.Bq)) and allStage1Ok;
allStage1Ok := StageAssert("|E|=[B3:N] = 6*|A18| = 19207121117184000",
                           Size(W.Bq) = 19207121117184000) and allStage1Ok;
allStage1Ok := StageAssert("P = ker(E ->> S3) has |P| = |A18|",
                           Size(W.PN) = Size(A18)) and allStage1Ok;
pr2 := Projection(Dgrp, 2);;
allStage1Ok := StageAssert("P (as constructed) = Kernel of the S3 projection",
                           Group(s1^2, s2^2) = Kernel(pr2)) and allStage1Ok;
allStage1Ok := StageAssert("ord(s1) = 26", Order(s1) = 26) and allStage1Ok;
allStage1Ok := StageAssert("ord(xbar) = 13", Order(W.x) = 13) and allStage1Ok;
allStage1Ok := StageAssert("ord(ybar) = 13", Order(W.y) = 13) and allStage1Ok;
allStage1Ok := StageAssert("N_ord = lcm(13,13,1) = 13", W.Nord = 13) and allStage1Ok;
charmingSetA18 := Filtered([0 .. W.Nord - 1], m -> Gcd(2*m+1, W.Nord) = 1);;
allStage1Ok := StageAssert("charming m count = phi(26) = 12",
                           Length(charmingSetA18) = 12) and allStage1Ok;

CPy := Centralizer(W.PN, W.y);;
StabXbar := Centralizer(S18, W.x);;
allStage1Ok := StageAssert("C_P(ybar) non-solvable (|C_P(ybar)|=780, C13 x A5)",
                           (not IsSolvable(CPy)) and Size(CPy) = 780) and allStage1Ok;
allStage1Ok := StageAssert("Stab_{Aut(P)}(xbar) = C_S18(xbar) non-solvable (|.|=1560, C13 x S5)",
                           (not IsSolvable(StabXbar)) and Size(StabXbar) = 1560) and allStage1Ok;

Print("\nSTAGE 1 overall: ", PF(allStage1Ok), "\n");
if not allStage1Ok then
  Error("strike-a18.g: STAGE 1 failed -- see printed asserts above; refusing ",
        "to proceed to any stage-2 connection (fail-closed, per campaign policy)");
fi;

#############################################################################
## ---------------------- STAGE 2: connect to kerchi-judge v1.3 (Xi forced) -
##   NOT fully run locally (per the coordinator's instruction) -- only a
##   single charming-m layer is timed here, for extrapolation purposes.
#############################################################################
Print("\n=== STAGE 2: connect to kerchi-judge v1.3 (JUDGE_FORCE_SCAN_MODE := \"xi_restricted\") ===\n");
Print("(full run deferred -- launch order per the slate is 2(Sp45) -> 1(A20) -> 3(A18); ",
      "only a single m-layer timing trial is run here)\n");

Print("charmingSet = ", charmingSetA18, "\n");
mTrial := charmingSetA18[2];;   # a non-degenerate m (not m=0)
Print("timing trial: single m-layer, m=", mTrial, " ...\n");

t0 := GAPLIB_WallElapsedMs();;
xiTrialRes := CorrectedShadowsXi(W, [mTrial]);;
t1 := GAPLIB_WallElapsedMs();;
singleMElapsedMs := t1 - t0;;

Print("  elapsed_ms=", singleMElapsedMs, "  shadow_total(this m)=", Length(xiTrialRes.shadows),
      "  scanned_count=", xiTrialRes.scanned_count,
      "  theoretical_upper_bound=", xiTrialRes.theoretical_upper_bound_xi,
      "  settled_fail_count=", xiTrialRes.settled_fail_count, "\n");

if singleMElapsedMs > 5 * 60 * 1000 then
  Print("  [CAP WARNING] single-m trial exceeded 5 minutes -- stopping here, ",
        "estimate below is based on this one (slow) sample only\n");
fi;

estimatedTotalXiMs := singleMElapsedMs * Length(charmingSetA18);;
Print("  extrapolated total for all ", Length(charmingSetA18),
      " charming m (CorrectedShadowsXi phase only, UNIFORM-COST ASSUMPTION): ",
      estimatedTotalXiMs, " ms (", estimatedTotalXiMs/1000.0/60.0, " min)\n");
Print("  NOTE: this extrapolation does NOT include the (3.53) closure / ",
      "GroupOfShadows phase, not locally timed here.\n");

#############################################################################
## ---------------------- CI recommendation -----------------------------------
#############################################################################
recommendedTimeoutMin := 30;;
Print("\n=== CI recommendation (.github/workflows/gap-run.yml) ===\n");
Print("  script:      search/strike-a18.g\n");
Print("  preamble:    JUDGE_FORCE_SCAN_MODE:=\"xi_restricted\";; STRIKE_RUN_STAGE2:=true;;\n");
Print("  out_dir:     search/certs\n");
Print("  timeout_min: ", recommendedTimeoutMin, "\n");
Print("  *** launch order recommended by the slate: Sp45 -> A20 -> A18 -- await go-ahead ***\n");

#############################################################################
## ---------------------- optional: full stage 2 (CI/go-ahead only, gated) --
#############################################################################
STAGE2_FULL_RESULT := fail;;
if IsBound(STRIKE_RUN_STAGE2) and STRIKE_RUN_STAGE2 = true then
  Print("\n=== STAGE 2 (FULL RUN -- STRIKE_RUN_STAGE2 bound true) ===\n");
  JUDGE_FORCE_SCAN_MODE := "xi_restricted";;
  JUDGE_SKIP_LEGACY_CROSSCHECK := true;;   # mandatory -- see W-D-A16-11a CI-hang postmortem
  STAGE2_FULL_RESULT := JudgeWindow(s1, s2, "W-D-A18-13a");;
  RunAndWrite(STAGE2_FULL_RESULT, "search/certs/strike_a18_full_20260729.json");
else
  Print("\n(STRIKE_RUN_STAGE2 not set -- full stage 2 skipped, awaiting coordinator go-ahead)\n");
fi;

#############################################################################
## ---------------------- write stage-1 + timing-trial certificate -----------
#############################################################################
AssertJson := function(a)
  return Concatenation("{\"label\":", JStr(a.label), ",\"ok\":", JB(a.ok), "}");
end;;

outParts := [];;
Add(outParts, "{\n");
Add(outParts, "  \"generated_by\": \"search/strike-a18.g\",\n");
Add(outParts, "  \"note\": \"WA-c second-strike driver for W-D-A18-13a; stage 1 (window asserts incl. slate-transcription consistency, run locally) + stage 2 single-m timing trial (kerchi-judge v1.3, Xi-restricted forced); full stage 2 NOT run locally, awaits coordinator go-ahead. NOT a ledger claim.\",\n");
Add(outParts, Concatenation("  \"stage1_all_pass\": ", JB(allStage1Ok), ",\n"));
Add(outParts, "  \"stage1_asserts\": [\n");
for i in [1 .. Length(STAGE1_ASSERTS)] do
  Add(outParts, Concatenation("    ", AssertJson(STAGE1_ASSERTS[i])));
  if i < Length(STAGE1_ASSERTS) then Add(outParts, ",\n"); else Add(outParts, "\n"); fi;
od;
Add(outParts, "  ],\n");
Add(outParts, Concatenation("  \"window_size_E\": ", String(Size(W.Bq)), ",\n"));
Add(outParts, Concatenation("  \"window_size_P\": ", String(Size(W.PN)), ",\n"));
Add(outParts, Concatenation("  \"N_ord\": ", String(W.Nord), ",\n"));
Add(outParts, Concatenation("  \"charming_count\": ", String(Length(charmingSetA18)), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_m\": ", String(mTrial), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_elapsed_ms\": ", String(singleMElapsedMs), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_shadow_total\": ", String(Length(xiTrialRes.shadows)), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_scanned_count\": ", String(xiTrialRes.scanned_count), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_theoretical_upper_bound\": ", String(xiTrialRes.theoretical_upper_bound_xi), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_settled_fail_count\": ", String(xiTrialRes.settled_fail_count), ",\n"));
Add(outParts, Concatenation("  \"estimated_total_xi_phase_ms_UNIFORM_ASSUMPTION\": ", String(estimatedTotalXiMs), ",\n"));
Add(outParts, "  \"estimate_caveat\": \"extrapolation assumes uniform per-candidate cost across all 12 charming m and does NOT include the (3.53) closure / GroupOfShadows phase, which was not locally timed\",\n");
Add(outParts, Concatenation("  \"recommended_ci_timeout_min\": ", String(recommendedTimeoutMin), ",\n"));
Add(outParts, "  \"awaits_go_ahead\": \"stage 2 full run withheld pending coordinator go-ahead; launch order per slate is Sp45 -> A20 -> A18\",\n");
Add(outParts, Concatenation("  \"stage2_full_run_performed_locally\": ",
    JB(IsBound(STRIKE_RUN_STAGE2) and STRIKE_RUN_STAGE2 = true), "\n"));
Add(outParts, "}\n");

WriteFile("search/certs/strike_a18_stage1_20260729.json", Concatenation(outParts));
Print("\nWrote search/certs/strike_a18_stage1_20260729.json\n");
Print("STRIKE_A18_DRIVER_DONE\n");
