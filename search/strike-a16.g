#############################################################################
## search/strike-a16.g -- WA-c first-strike driver for W-D-A16-11a (裁定181)
##
## Reuses the window construction from search/probe/wac_v1/build_a16.g and
## the window diagnostics from docs/notes/wac_reverse_design_v1.md S3
## (E = A16 x S3, 19-point permutation group; P = ker(E ->> S3) = A16;
## s1 = b^-1*a, s2 = a^-1*b^2 for a specific (2,3)-generating pair of A16
## found in that document's search).
##
## STAGE 1 (run here, locally): window assertions -- braid relation, c in N,
## P = A16, ord(xbar)=ord(ybar)=11, C_P(ybar)/Stab_{Aut(P)}(xbar) both
## non-solvable (the Cor 7.2 necessary condition this window was selected
## to satisfy). All fail-closed: this script Errors (does not silently
## continue) if the window fails to build as expected.
##
## STAGE 2 (connected here, NOT fully run locally per the coordinator's
## instruction): kerchi-judge.g v1.3 with JUDGE_FORCE_SCAN_MODE :=
## "xi_restricted" forced (never legacy -- |[P,P]|=|A16|~1.05e13 makes
## legacy's Elements(DerivedSubgroup(P)) infeasible, exactly the case v1.3
## was built for). Only a SINGLE charming-m layer is actually run locally
## here, purely to measure wall-clock cost and extrapolate; the full
## judgment (all charming m + (3.53) closure) is left for CI.
##
## *** IMPORTANT FINDING (2026-07-29, found while preparing this driver,
## FIXED in search/kerchi-judge.g before this driver was written -- see that
## file's CorrectedShadowsXi comments): the GENERIC AutomorphismGroup(P) +
## Stabilizer(AutP,xbar,actFun) path that CorrectedShadowsXi originally used
## (calibrated fine on the small SL(2,5)/SL(2,7) windows) does NOT complete
## in practical time for P=A16 (|Aut(P)|=16!~2.09e13) -- confirmed hung
## past 90s just on the Stabilizer() call, before even reaching the m-loop.
## A targeted, spec-sanctioned fast path was added to CorrectedShadowsXi
## (docs/notes/wac_reverse_design_v1.md S3.4 item 2 already says "P=A_n の
## 場合は S_n 内の共役元探索で足りる"): when P is recognized as the natural
## A_n (n<>6), Aut(P)=S_n is used directly via the DEDICATED
## Centralizer(Sym(n),xbar) / RepresentativeAction(Sym(n),xbar,xbar^u)
## calls (no custom action function -- those were ALSO found to be slow
## even on a genuine permutation group; only the argument-free dedicated
## forms reliably trigger GAP's fast conjugacy algorithms). This fix was
## re-verified against search/kerchi-judge-v13-calibration.g (still 0 fails,
## unaffected since SL(2,5)/SL(2,7) are not alternating groups) before this
## driver was finalized. Without this fix, stage 2 as specified below would
## not have been practically runnable at all, in CI or otherwise.
##
## Output: search/certs/strike_a16_stage1_20260729.json
#############################################################################

Read("search/gaplib_common.g");

JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");   # MakeWindow, CorrectedShadowsXi, AbstractProd, TH, RtOf, etc.

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
## ---------------------- window construction (from build_a16.g) ------------
#############################################################################
Print("=== strike-a16: building W-D-A16-11a ===\n");
a1 := ( 1, 2)( 3,14)( 4,10)( 5,12)( 6, 8)( 7,16)( 9,13)(11,15);;
b1 := ( 2,11,14)( 3,15,10)( 4, 9,12)( 5,13, 8)( 6, 7,16);;
A16 := AlternatingGroup(16);;  S16 := SymmetricGroup(16);;
S3 := SymmetricGroup(3);;
Dgrp := DirectProduct(A16, S3);;
embA := Embedding(Dgrp, 1);;  embS := Embedding(Dgrp, 2);;
agen := Image(embA, a1) * Image(embS, (1,3));;
bgen := Image(embA, b1) * Image(embS, (1,3,2));;
s1 := bgen^-1 * agen;;
s2 := agen^-1 * bgen^2;;

Print("degree of E = ", LargestMovedPoint(Dgrp), " (expect 19)\n");
Print("JUDGE_S1_IMG := ", s1, ";;\n");
Print("JUDGE_S2_IMG := ", s2, ";;\n");

#############################################################################
## ---------------------- STAGE 1: window assertions -------------------------
#############################################################################
Print("\n=== STAGE 1: window assertions ===\n");
allStage1Ok := true;;

allStage1Ok := StageAssert("<a1,b1> = A16", Group(a1,b1) = A16) and allStage1Ok;
allStage1Ok := StageAssert("a1^2=1 and b1^3=1", a1^2 = () and b1^3 = ()) and allStage1Ok;
allStage1Ok := StageAssert("braid relation s1*s2*s1 = s2*s1*s2",
                           s1*s2*s1 = s2*s1*s2) and allStage1Ok;

W := MakeWindow(s1, s2);;
allStage1Ok := StageAssert("c in N (c = identity in Bq)",
                           W.c = Identity(W.Bq)) and allStage1Ok;
allStage1Ok := StageAssert("|E|=[B3:N] = 6*|A16| = 62768369664000",
                           Size(W.Bq) = 62768369664000) and allStage1Ok;
allStage1Ok := StageAssert("P = ker(E ->> S3) has |P| = |A16| = 10461394944000",
                           Size(W.PN) = Size(A16)) and allStage1Ok;
pr2 := Projection(Dgrp, 2);;
allStage1Ok := StageAssert("P (as constructed) = Kernel of the S3 projection",
                           Group(s1^2, s2^2) = Kernel(pr2)) and allStage1Ok;
allStage1Ok := StageAssert("ord(xbar) = 11", Order(W.x) = 11) and allStage1Ok;
allStage1Ok := StageAssert("ord(ybar) = 11", Order(W.y) = 11) and allStage1Ok;
allStage1Ok := StageAssert("N_ord = lcm(11,11,1) = 11", W.Nord = 11) and allStage1Ok;
charmingSetA16 := Filtered([0 .. W.Nord - 1], m -> Gcd(2*m+1, W.Nord) = 1);;
allStage1Ok := StageAssert("charming m count = phi(22) = 10",
                           Length(charmingSetA16) = 10) and allStage1Ok;

CPy := Centralizer(W.PN, W.y);;
StabXbar := Centralizer(S16, W.x);;
allStage1Ok := StageAssert("C_P(ybar) non-solvable (|C_P(ybar)|=660, C11 x A5)",
                           (not IsSolvable(CPy)) and Size(CPy) = 660) and allStage1Ok;
allStage1Ok := StageAssert("Stab_{Aut(P)}(xbar) = C_S16(xbar) non-solvable (|.|=1320, C11 x S5)",
                           (not IsSolvable(StabXbar)) and Size(StabXbar) = 1320) and allStage1Ok;

Print("\nSTAGE 1 overall: ", PF(allStage1Ok), "\n");
if not allStage1Ok then
  Error("strike-a16.g: STAGE 1 failed -- see printed asserts above; refusing ",
        "to proceed to any stage-2 connection (fail-closed, per campaign policy)");
fi;

#############################################################################
## ---------------------- STAGE 2: connect to kerchi-judge v1.3 (Xi forced) -
##   NOT fully run locally (per the coordinator's instruction) -- only a
##   single charming-m layer is timed here, for extrapolation purposes.
#############################################################################
Print("\n=== STAGE 2: connect to kerchi-judge v1.3 (JUDGE_FORCE_SCAN_MODE := \"xi_restricted\") ===\n");
Print("(full run deferred to CI; only a single m-layer timing trial is run here)\n");

Print("charmingSet = ", charmingSetA16, "\n");
mTrial := charmingSetA16[2];;   # a non-degenerate m (not m=0, where u=1 is a trivial edge case)
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

# extrapolate: 10 charming m total, assume roughly uniform per-m cost (an
# assumption, not a proof -- flagged as such in the JSON/report)
estimatedTotalXiMs := singleMElapsedMs * Length(charmingSetA16);;
Print("  extrapolated total for all ", Length(charmingSetA16),
      " charming m (CorrectedShadowsXi phase only, UNIFORM-COST ASSUMPTION): ",
      estimatedTotalXiMs, " ms (", estimatedTotalXiMs/1000.0/60.0, " min)\n");
Print("  NOTE: this extrapolation does NOT include the subsequent (3.53) ",
      "closure / GroupOfShadows phase (regular representation over the full ",
      "shadow set, O(N^2) position lookups) -- that phase was NOT locally ",
      "timed here (would require a full stage-2 run, which this driver was ",
      "instructed not to do). Recommend generous headroom in the CI timeout ",
      "for that reason.\n");

#############################################################################
## ---------------------- CI recommendation -----------------------------------
#############################################################################
recommendedTimeoutMin := 30;;   # see report: measured phase ~1 min, generous headroom
                                 # for the untimed GroupOfShadows phase + CI overhead
Print("\n=== CI recommendation (.github/workflows/gap-run.yml) ===\n");
Print("  script:      search/strike-a16.g\n");
Print("  preamble:    JUDGE_FORCE_SCAN_MODE:=\"xi_restricted\";; STRIKE_RUN_STAGE2:=true;;\n");
Print("  out_dir:     search/certs\n");
Print("  timeout_min: ", recommendedTimeoutMin, "\n");
Print("  (this driver, AS WRITTEN, still stops after stage 1 + the single-m timing\n");
Print("   trial unless STRIKE_RUN_STAGE2 is bound true -- see the dispatch block below)\n");

#############################################################################
## ---------------------- optional: full stage 2 (CI only, gated) ------------
#############################################################################
STAGE2_FULL_RESULT := fail;;
if IsBound(STRIKE_RUN_STAGE2) and STRIKE_RUN_STAGE2 = true then
  Print("\n=== STAGE 2 (FULL RUN -- STRIKE_RUN_STAGE2 bound true) ===\n");
  JUDGE_FORCE_SCAN_MODE := "xi_restricted";;
  # *** CRITICAL FIX (found diagnosing CI run 30392894007's 29-minute silent
  # hang, 2026-07-29): this window has c_in_N=true, so JudgeWindow's
  # crosscheck_vs_EnumerateReducedHexagon block fires unless explicitly
  # disabled. That block calls EnumerateReducedHexagon, whose BFSWords tries
  # to enumerate the WHOLE of P_N via x,y-words -- for |P_N|=|A16|~1.05e13
  # this cannot finish (the CI run was very likely still slowly thrashing
  # toward the 2g heap cap when the 30-minute CI timeout killed it, matching
  # the observed "STAGE 2 (FULL RUN) printed, then total silence" symptom --
  # the earlier local timing trial never hit this because it called
  # CorrectedShadowsXi directly, bypassing JudgeWindow's crosscheck block
  # entirely). search/wall-miner-v5.g already sets this same flag for the
  # same reason. Without this line, stage 2 will hang again exactly as it
  # did in the CI run.
  JUDGE_SKIP_LEGACY_CROSSCHECK := true;;
  STAGE2_FULL_RESULT := JudgeWindow(s1, s2, "W-D-A16-11a");;
  RunAndWrite(STAGE2_FULL_RESULT, "search/certs/strike_a16_full_20260729.json");
else
  Print("\n(STRIKE_RUN_STAGE2 not set -- full stage 2 skipped, as instructed for the local run)\n");
fi;

#############################################################################
## ---------------------- write stage-1 + timing-trial certificate -----------
#############################################################################
AssertJson := function(a)
  return Concatenation("{\"label\":", JStr(a.label), ",\"ok\":", JB(a.ok), "}");
end;;

outParts := [];;
Add(outParts, "{\n");
Add(outParts, "  \"generated_by\": \"search/strike-a16.g\",\n");
Add(outParts, "  \"note\": \"WA-c first-strike driver, stage 1 (window asserts, run locally) + stage 2 single-m timing trial (kerchi-judge v1.3, Xi-restricted forced); full stage 2 NOT run locally per instruction unless STRIKE_RUN_STAGE2 is bound. NOT a ledger claim.\",\n");
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
Add(outParts, Concatenation("  \"charming_count\": ", String(Length(charmingSetA16)), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_m\": ", String(mTrial), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_elapsed_ms\": ", String(singleMElapsedMs), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_shadow_total\": ", String(Length(xiTrialRes.shadows)), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_scanned_count\": ", String(xiTrialRes.scanned_count), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_theoretical_upper_bound\": ", String(xiTrialRes.theoretical_upper_bound_xi), ",\n"));
Add(outParts, Concatenation("  \"stage2_trial_settled_fail_count\": ", String(xiTrialRes.settled_fail_count), ",\n"));
Add(outParts, Concatenation("  \"estimated_total_xi_phase_ms_UNIFORM_ASSUMPTION\": ", String(estimatedTotalXiMs), ",\n"));
Add(outParts, "  \"estimate_caveat\": \"extrapolation assumes uniform per-candidate cost across all 10 charming m and does NOT include the (3.53) closure / GroupOfShadows phase, which was not locally timed\",\n");
Add(outParts, Concatenation("  \"recommended_ci_timeout_min\": ", String(recommendedTimeoutMin), ",\n"));
Add(outParts, Concatenation("  \"stage2_full_run_performed_locally\": ",
    JB(IsBound(STRIKE_RUN_STAGE2) and STRIKE_RUN_STAGE2 = true), "\n"));
Add(outParts, "}\n");

WriteFile("search/certs/strike_a16_stage1_20260729.json", Concatenation(outParts));
Print("\nWrote search/certs/strike_a16_stage1_20260729.json\n");
Print("STRIKE_A16_DRIVER_DONE\n");
