#############################################################################
## search/kerchi-judge-v13-calibration.g -- KJ-1.3 regression calibration
## (裁定171・速達blocker, docs/notes/wac_reverse_design_v1.md S3.4 item 4)
##
## Requirement: CorrectedShadowsLegacy (exhaustive) and CorrectedShadowsXi
## (Prop 3.1 restricted scan) must produce IDENTICAL shadow sets on windows
## small enough for BOTH to run. Per the coordinator's instruction, this is
## checked on: D1's p=5 and p=7 congruence windows, and W-C-N5cong.
##
## NOTE (reported, not silently smoothed over): W-C-N5cong, as constructed
## throughout this campaign (wall-miner-v1.g / kerchi-judge.g's own
## self-test fixture 1), IS the p=5 window -- both are S3 x SL(2,F5) built
## the same way. So this script's three named checks are p=5 (labeled
## "D1-p5"), p=7 ("D1-p7"), and N5cong ("W-C-N5cong") where the latter two
## sections use IDENTICAL matrices/construction to the p=5 section; N5cong
## is not a fourth, independent window. This is flagged here rather than
## silently presenting 3 "different" calibration passes.
##
## Each window is judged twice (JUDGE_FORCE_SCAN_MODE="legacy" then
## "xi_restricted") and the two shadow sets are compared for EXACT equality
## (not just counts). Per the coordinator: if calibration fails, v1.3 is to
## be considered invalid -- so this script's own PASS/FAIL verdict is load
## bearing, not decorative.
##
## Output: search/certs/kerchi_judge_v13_calibration_20260729.json
#############################################################################

JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");

CAL_RESULTS := [];;
CAL_FAILS := 0;;

# CalibrateWindow(label, s1, s2): runs JudgeWindow twice (forcing legacy, then
# xi_restricted) on the SAME window and checks the two shadow sets agree
# exactly (not just shadow_total -- literal set equality, obtained by
# re-invoking CorrectedShadowsLegacy/CorrectedShadowsXi directly rather than
# trusting JudgeWindow's shadow_total alone).
CalibrateWindow := function(label, s1, s2)
  local W, ch, legRes, xiRes, setsEqual, row;
  W := MakeWindow(s1, s2);
  ch := Filtered([0 .. W.Nord - 1], m -> Gcd(2*m+1, W.Nord) = 1);
  Print("\n=== calibrating ", label, " ===\n");
  Print("  |Bq|=", Size(W.Bq), " |PN|=", Size(W.PN), " N_ord=", W.Nord,
        " charming_count=", Length(ch), "\n");

  legRes := CorrectedShadowsLegacy(W, ch);
  xiRes := CorrectedShadowsXi(W, ch);
  setsEqual := (Set(legRes.shadows) = Set(xiRes.shadows));

  row := rec(label := label, abs_Bq := Size(W.Bq), abs_PN := Size(W.PN),
             N_ord := W.Nord, charming_count := Length(ch),
             legacy_shadow_total := Length(legRes.shadows),
             xi_shadow_total := Length(xiRes.shadows),
             legacy_settled_fail_count := legRes.settled_fail_count,
             xi_settled_fail_count := xiRes.settled_fail_count,
             xi_scanned_count := xiRes.scanned_count,
             xi_theoretical_upper_bound := xiRes.theoretical_upper_bound_xi,
             legacy_candidate_count := Size(DerivedSubgroup(W.PN)) * Length(ch),
             sets_equal := setsEqual);
  if row.legacy_candidate_count > 0 and row.xi_scanned_count > 0 then
    row.compression := Float(row.legacy_candidate_count) / Float(row.xi_scanned_count);
  else
    row.compression := -1;
  fi;

  Print("  legacy: shadow_total=", row.legacy_shadow_total,
        " settled_fail=", row.legacy_settled_fail_count, "\n");
  Print("  xi:     shadow_total=", row.xi_shadow_total,
        " settled_fail=", row.xi_settled_fail_count,
        " scanned=", row.xi_scanned_count, "/", row.xi_theoretical_upper_bound,
        " compression=", row.compression, "\n");
  Print("  SETS EQUAL? ", setsEqual, "\n");
  if not setsEqual then
    CAL_FAILS := CAL_FAILS + 1;
    Print("  *** CALIBRATION FAIL for ", label, " ***\n");
  fi;

  Add(CAL_RESULTS, row);
  return row;
end;;

#############################################################################
## ---------------------- D1-p5 (= W-C-N5cong) --------------------------------
#############################################################################
M1_2 := [[1,1],[0,1]]*One(GF(2));; M2_2 := [[1,0],[1,1]]*One(GF(2));;
M1_5 := [[1,1],[0,1]]*One(GF(5));; M2_5 := [[1,0],[4,1]]*One(GF(5));;
psi2_5 := IsomorphismPermGroup(Group(M1_2, M2_2));;
psi5 := IsomorphismPermGroup(Group(M1_5, M2_5));;
DP5 := DirectProduct(Image(psi2_5), Image(psi5));;
e1_5 := Embedding(DP5,1);; e2_5 := Embedding(DP5,2);;
s1p5 := Image(e1_5, Image(psi2_5, M1_2)) * Image(e2_5, Image(psi5, M1_5));;
s2p5 := Image(e1_5, Image(psi2_5, M2_2)) * Image(e2_5, Image(psi5, M2_5));;
CalibrateWindow("D1-p5", s1p5, s2p5);;

#############################################################################
## ---------------------- D1-p7 -----------------------------------------------
#############################################################################
M1_2b := [[1,1],[0,1]]*One(GF(2));; M2_2b := [[1,0],[1,1]]*One(GF(2));;
M1_7 := [[1,1],[0,1]]*One(GF(7));; M2_7 := [[1,0],[6,1]]*One(GF(7));;
psi2_7 := IsomorphismPermGroup(Group(M1_2b, M2_2b));;
psi7 := IsomorphismPermGroup(Group(M1_7, M2_7));;
DP7 := DirectProduct(Image(psi2_7), Image(psi7));;
e1_7 := Embedding(DP7,1);; e2_7 := Embedding(DP7,2);;
s1p7 := Image(e1_7, Image(psi2_7, M1_2b)) * Image(e2_7, Image(psi7, M1_7));;
s2p7 := Image(e1_7, Image(psi2_7, M2_2b)) * Image(e2_7, Image(psi7, M2_7));;
CalibrateWindow("D1-p7", s1p7, s2p7);;

#############################################################################
## ---------------------- W-C-N5cong (== D1-p5, same construction; see header
##                        note -- checked again explicitly per the coordinator's
##                        named list, not skipped as "redundant") ------------
#############################################################################
CalibrateWindow("W-C-N5cong", s1p5, s2p5);;

#############################################################################
## ---------------------- summary + JSON --------------------------------------
#############################################################################
Print("\n============================================================\n");
Print("CALIBRATION FAILS = ", CAL_FAILS, " (of ", Length(CAL_RESULTS), " windows checked)\n");
if CAL_FAILS = 0 then
  Print("v1.3 CorrectedShadowsXi CALIBRATION: PASS (legacy == xi_restricted on all windows checked)\n");
else
  Print("v1.3 CorrectedShadowsXi CALIBRATION: FAIL -- v1.3 should be considered INVALID per the ",
        "coordinator's instruction until this is resolved\n");
fi;
Print("============================================================\n");

RowJson := function(r)
  return Concatenation("  {\n",
    "    \"label\":", JStr(r.label), ",\n",
    "    \"abs_Bq\":", String(r.abs_Bq), ",\n",
    "    \"abs_PN\":", String(r.abs_PN), ",\n",
    "    \"N_ord\":", String(r.N_ord), ",\n",
    "    \"charming_count\":", String(r.charming_count), ",\n",
    "    \"legacy_shadow_total\":", String(r.legacy_shadow_total), ",\n",
    "    \"xi_shadow_total\":", String(r.xi_shadow_total), ",\n",
    "    \"legacy_settled_fail_count\":", String(r.legacy_settled_fail_count), ",\n",
    "    \"xi_settled_fail_count\":", String(r.xi_settled_fail_count), ",\n",
    "    \"xi_scanned_count\":", String(r.xi_scanned_count), ",\n",
    "    \"xi_theoretical_upper_bound\":", String(r.xi_theoretical_upper_bound), ",\n",
    "    \"legacy_candidate_count\":", String(r.legacy_candidate_count), ",\n",
    "    \"compression\":", FloatOrNullJson(r.compression), ",\n",
    "    \"sets_equal\":", JB(r.sets_equal), "\n",
    "  }");
end;;

outParts := [];;
Add(outParts, "{\n");
Add(outParts, "  \"generated_by\": \"search/kerchi-judge-v13-calibration.g\",\n");
Add(outParts, "  \"note\": \"KJ-1.3 (ruling 171) regression calibration for CorrectedShadowsXi (Prop 3.1 Xi-restriction) vs CorrectedShadowsLegacy; W-C-N5cong is the SAME window as D1-p5 (both S3 x SL(2,F5)), checked again explicitly per the coordinator's named list rather than skipped as redundant -- see script header. NOT a ledger claim, no cross-check against an independently-implemented checker.\",\n");
Add(outParts, Concatenation("  \"calibration_fails\": ", String(CAL_FAILS), ",\n"));
Add(outParts, Concatenation("  \"calibration_pass\": ", JB(CAL_FAILS = 0), ",\n"));
Add(outParts, "  \"windows\": [\n");
for i in [1 .. Length(CAL_RESULTS)] do
  Add(outParts, RowJson(CAL_RESULTS[i]));
  if i < Length(CAL_RESULTS) then Add(outParts, ",\n"); else Add(outParts, "\n"); fi;
od;
Add(outParts, "  ]\n");
Add(outParts, "}\n");

WriteFile("search/certs/kerchi_judge_v13_calibration_20260729.json", Concatenation(outParts));
Print("Wrote search/certs/kerchi_judge_v13_calibration_20260729.json\n");
Print("KJ13_CALIBRATION_DONE\n");
