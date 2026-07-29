#############################################################################
## search/strike-a14.g -- WA-c third-strike (branch experiment) driver for
## W-D-A14-9a (裁定204)
##
## Generators MECHANICALLY DERIVED from the (D4) design rule in
## docs/notes/wac_second_strike_v1.md S0 -- x-bar = (ell,1^5) type, n=ell+5,
## here ell=9, n=14 -- via random (2,3)-generation search over A14 for a
## pair (a1,b1) with a1 of cycle type 2^6 1^2, b1 of cycle type 3^4 1^2, and
## u := b1^-1*a1 of order 18 with cycle type (9,2,2,1) on 14 points (so that
## x-bar := u^2 has type (9,1^5), matching (D4) with ell=9 exactly). This is
## the SAME construction pattern used in search/strike-a20.g / strike-a18.g,
## just with NO externally-supplied slate to transcribe against (unlike
## A20/A18, no docs/notes/a14_prediction_v1.md content is read here --
## measurement-side isolation per the coordinator's explicit instruction).
##
## Because there is no external slate here, the "slate-transcription
## consistency" check used for A20/A18 is replaced by a
## design-rule-consistency assert: the computed (a1,b1,s1,s2,xbar,ybar)
## are checked directly against the (D4) formula's own numeric predictions
## (N_ord=ell=9, |C_P(ybar)|=60*ell=540, |Stab_Aut(P)(xbar)|=120*ell=1080,
## charming count=phi(2*ell)=phi(18)=6) -- i.e. self-consistency against the
## design rule that generated the search target, not against a pre-computed
## external transcript (none exists / none was read).
##
## E = A14 x S3 (17-point permutation group), P = ker(E ->> S3) = A14,
## s1 = b^-1*a, s2 = a^-1*b^2 (same construction pattern as
## search/strike-a16.g / search/strike-a20.g / search/strike-a18.g).
##
## STAGE 1 (run here, locally): window assertions -- generation, parities,
## braid relation, c in N, P = A14, N_ord=9, ord(xbar)=ord(ybar)=9,
## charming count = phi(18) = 6, C_P(ybar) non-solvable order 540 (C9 x A5
## type), Stab_{Aut(P)}(xbar) non-solvable order 1080 (C9 x S5 type),
## AND the design-rule-consistency assert described above. Fail-closed
## throughout.
##
## STAGE 2: connects to kerchi-judge.g v1.3 (JUDGE_FORCE_SCAN_MODE :=
## "xi_restricted" forced from the outset -- |[P,P]| for P=A14 makes legacy
## infeasible; JUDGE_SKIP_LEGACY_CROSSCHECK is likewise set unconditionally
## from the outset here, per the W-D-A16-11a CI-hang postmortem, rather than
## added as an afterthought). Only a SINGLE charming-m layer is run locally,
## for timing/extrapolation purposes.
##
## *** STRIKE_RUN_STAGE2 is NOT set by this script. Full stage 2 awaits the
## coordinator's go-ahead and must not be self-triggered. ***
##
## *** docs/notes/a14_prediction_v1.md is NOT read by this script or by the
## implementer who wrote it -- measurement-side isolation. ***
##
## Output: search/certs/strike_a14_stage1_20260729.json
#############################################################################

Read("search/gaplib_common.g");

JUDGE_LIBRARY_ONLY := true;;
JUDGE_FORCE_SCAN_MODE := "xi_restricted";;      # forced from the outset (large P)
JUDGE_SKIP_LEGACY_CROSSCHECK := true;;          # forced from the outset (W-D-A16-11a postmortem)
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
## ---------------------- window construction (mechanically derived) -------
## (D4) design rule (docs/notes/wac_second_strike_v1.md S0): x-bar=(ell,1^5),
## n=ell+5, C_{A_n}(x-bar)=C_ell x A5 (60*ell), Stab=C_ell x S5 (120*ell),
## N_ord=ell, Xi=7200*ell^2*phi(2*ell). Here ell=9, n=14.
##
## (a1,b1) below found by random (2,3)-generation search over A14
## (search/_probe_a14_search*.g, shards 1-3; see driver-report for trial
## counts). NOT hand-copied from any external document.
#############################################################################
Print("=== strike-a14: building W-D-A14-9a ===\n");
a1 := PLACEHOLDER_A1;;   # 2^6 1^2 -- FILL IN once search hit is confirmed
b1 := PLACEHOLDER_B1;;   # 3^4 1^2 -- FILL IN once search hit is confirmed
A14 := AlternatingGroup(14);;  S14 := SymmetricGroup(14);;
S3 := SymmetricGroup(3);;
Dgrp := DirectProduct(A14, S3);;
embA := Embedding(Dgrp, 1);;  embS := Embedding(Dgrp, 2);;
agen := Image(embA, a1) * Image(embS, (1,3));;
bgen := Image(embA, b1) * Image(embS, (1,3,2));;
s1 := bgen^-1 * agen;;
s2 := agen^-1 * bgen^2;;

Print("degree of E = ", LargestMovedPoint(Dgrp), " (expect 17)\n");
Print("computed s1 := ", s1, ";;\n");
Print("computed s2 := ", s2, ";;\n");

#############################################################################
## ---------------------- STAGE 1: window assertions -------------------------
#############################################################################
Print("\n=== STAGE 1: window assertions ===\n");
allStage1Ok := true;;

allStage1Ok := StageAssert("<a1,b1> = A14", Group(a1,b1) = A14) and allStage1Ok;
allStage1Ok := StageAssert("a1^2=1 and b1^3=1", a1^2 = () and b1^3 = ()) and allStage1Ok;
allStage1Ok := StageAssert("a1 has cycle type 2^6 1^2",
                           SortedList(CycleLengths(a1,[1..14])) = [1,1,2,2,2,2,2,2]) and allStage1Ok;
allStage1Ok := StageAssert("b1 has cycle type 3^4 1^2",
                           SortedList(CycleLengths(b1,[1..14])) = [1,1,3,3,3,3]) and allStage1Ok;
allStage1Ok := StageAssert("braid relation s1*s2*s1 = s2*s1*s2",
                           s1*s2*s1 = s2*s1*s2) and allStage1Ok;

# *** design-rule-consistency assert (this task's specific requirement --
#     replaces the A20/A18 slate-transcription assert, since no external
#     slate exists / was read here) ***
allStage1Ok := StageAssert("u := b1^-1*a1 has order 18 (= 2*ell, ell=9)",
                           Order(b1^-1*a1) = 18) and allStage1Ok;
allStage1Ok := StageAssert("u has cycle type (9,2,2,1) on 14 points",
                           SortedList(CycleLengths(b1^-1*a1,[1..14])) = [1,2,2,9]) and allStage1Ok;
allStage1Ok := StageAssert("(u^2) has cycle type (9,1^5) -- matches (D4) x-bar=(ell,1^5), ell=9",
                           SortedList(CycleLengths((b1^-1*a1)^2,[1..14])) = [1,1,1,1,1,9]) and allStage1Ok;

W := MakeWindow(s1, s2);;
allStage1Ok := StageAssert("c in N (c = identity in Bq)",
                           W.c = Identity(W.Bq)) and allStage1Ok;
allStage1Ok := StageAssert("|E|=[B3:N] = 6*|A14| = 261534873600",
                           Size(W.Bq) = 261534873600) and allStage1Ok;
allStage1Ok := StageAssert("P = ker(E ->> S3) has |P| = |A14|",
                           Size(W.PN) = Size(A14)) and allStage1Ok;
pr2 := Projection(Dgrp, 2);;
allStage1Ok := StageAssert("P (as constructed) = Kernel of the S3 projection",
                           Group(s1^2, s2^2) = Kernel(pr2)) and allStage1Ok;
allStage1Ok := StageAssert("ord(s1) = 18", Order(s1) = 18) and allStage1Ok;
allStage1Ok := StageAssert("ord(xbar) = 9", Order(W.x) = 9) and allStage1Ok;
allStage1Ok := StageAssert("ord(ybar) = 9", Order(W.y) = 9) and allStage1Ok;
allStage1Ok := StageAssert("N_ord = lcm(9,9,1) = 9", W.Nord = 9) and allStage1Ok;
charmingSetA14 := Filtered([0 .. W.Nord - 1], m -> Gcd(2*m+1, W.Nord) = 1);;
allStage1Ok := StageAssert("charming m count = phi(18) = 6",
                           Length(charmingSetA14) = 6) and allStage1Ok;

CPy := Centralizer(W.PN, W.y);;
StabXbar := Centralizer(S14, W.x);;
allStage1Ok := StageAssert("C_P(ybar) non-solvable (|C_P(ybar)|=540, C9 x A5)",
                           (not IsSolvable(CPy)) and Size(CPy) = 540) and allStage1Ok;
allStage1Ok := StageAssert("Stab_{Aut(P)}(xbar) = C_S14(xbar) non-solvable (|.|=1080, C9 x S5)",
                           (not IsSolvable(StabXbar)) and Size(StabXbar) = 1080) and allStage1Ok;

Print("\nSTAGE 1 overall: ", PF(allStage1Ok), "\n");
if not allStage1Ok then
  Error("strike-a14.g: STAGE 1 failed -- see printed asserts above; refusing ",
        "to proceed to any stage-2 connection (fail-closed, per campaign policy)");
fi;

#############################################################################
## ---------------------- STAGE 2: connect to kerchi-judge v1.3 (Xi forced) -
##   NOT fully run locally -- only a single charming-m layer is timed here,
##   for extrapolation purposes.
#############################################################################
Print("\n=== STAGE 2: connect to kerchi-judge v1.3 (JUDGE_FORCE_SCAN_MODE := \"xi_restricted\") ===\n");
Print("(full run deferred -- awaits coordinator go-ahead; ",
      "only a single m-layer timing trial is run here)\n");

Print("charmingSet = ", charmingSetA14, "\n");
mTrial := charmingSetA14[2];;   # a non-degenerate m (not m=0)
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

estimatedTotalXiMs := singleMElapsedMs * Length(charmingSetA14);;
Print("  extrapolated total for all ", Length(charmingSetA14),
      " charming m (CorrectedShadowsXi phase only, UNIFORM-COST ASSUMPTION): ",
      estimatedTotalXiMs, " ms (", estimatedTotalXiMs/1000.0/60.0, " min)\n");
Print("  NOTE: this extrapolation does NOT include the (3.53) closure / ",
      "GroupOfShadows phase, not locally timed here.\n");

#############################################################################
## ---------------------- CI recommendation -----------------------------------
#############################################################################
recommendedTimeoutMin := 30;;
Print("\n=== CI recommendation (.github/workflows/gap-run.yml) ===\n");
Print("  script:      search/strike-a14.g\n");
Print("  preamble:    STRIKE_RUN_STAGE2:=true;;\n");
Print("  (JUDGE_FORCE_SCAN_MODE and JUDGE_SKIP_LEGACY_CROSSCHECK are already forced\n");
Print("   inside this script from the outset -- no extra preamble needed for those.)\n");
Print("  out_dir:     search/certs\n");
Print("  timeout_min: ", recommendedTimeoutMin, "\n");
Print("  *** full stage 2 awaits coordinator go-ahead (prediction frozen at commit 331cc1b) ***\n");

#############################################################################
## ---------------------- optional: full stage 2 (CI/go-ahead only, gated) --
#############################################################################
STAGE2_FULL_RESULT := fail;;
if IsBound(STRIKE_RUN_STAGE2) and STRIKE_RUN_STAGE2 = true then
  Print("\n=== STAGE 2 (FULL RUN -- STRIKE_RUN_STAGE2 bound true) ===\n");
  STAGE2_FULL_RESULT := JudgeWindow(s1, s2, "W-D-A14-9a");;
  RunAndWrite(STAGE2_FULL_RESULT, "search/certs/strike_a14_full_20260729.json");
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
Add(outParts, "  \"generated_by\": \"search/strike-a14.g\",\n");
Add(outParts, "  \"note\": \"WA-c third-strike (branch) driver for W-D-A14-9a; generators mechanically derived from (D4) design rule via random search (no external slate read); stage 1 (window asserts incl. design-rule-consistency, run locally) + stage 2 single-m timing trial (kerchi-judge v1.3, Xi-restricted forced from the outset); full stage 2 NOT run locally, awaits coordinator go-ahead. NOT a ledger claim.\",\n");
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
Add(outParts, Concatenation("  \"charming_count\": ", String(Length(charmingSetA14)), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_m\": ", String(mTrial), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_elapsed_ms\": ", String(singleMElapsedMs), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_shadow_total\": ", String(Length(xiTrialRes.shadows)), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_scanned_count\": ", String(xiTrialRes.scanned_count), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_theoretical_upper_bound\": ", String(xiTrialRes.theoretical_upper_bound_xi), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_settled_fail_count\": ", String(xiTrialRes.settled_fail_count), ",\n"));
Add(outParts, Concatenation("  \"estimated_total_xi_phase_ms_UNIFORM_ASSUMPTION\": ", String(estimatedTotalXiMs), ",\n"));
Add(outParts, "  \"estimate_caveat\": \"extrapolation assumes uniform per-candidate cost across all 6 charming m and does NOT include the (3.53) closure / GroupOfShadows phase, which was not locally timed\",\n");
Add(outParts, Concatenation("  \"recommended_ci_timeout_min\": ", String(recommendedTimeoutMin), ",\n"));
Add(outParts, "  \"awaits_go_ahead\": \"stage 2 full run withheld pending coordinator go-ahead (prediction frozen at commit 331cc1b)\",\n");
Add(outParts, Concatenation("  \"stage2_full_run_performed_locally\": ",
    JB(IsBound(STRIKE_RUN_STAGE2) and STRIKE_RUN_STAGE2 = true), "\n"));
Add(outParts, "}\n");

WriteFile("search/certs/strike_a14_stage1_20260729.json", Concatenation(outParts));
Print("\nWrote search/certs/strike_a14_stage1_20260729.json\n");
Print("STRIKE_A14_DRIVER_DONE\n");
