#############################################################################
## search/kerchi-judge-v11-regression.g -- KJ-1 regression driver (裁定169)
##
## Loads search/kerchi-judge.g in library-only mode (JUDGE_LIBRARY_ONLY) and
## re-runs, through the v1.1 (settled-clause-fixed) (F2) predicate:
##   (1) the W-C-N5cong fixture (known answer: ABELIAN, |GTSh|=40)
##   (2) window W-A-B3idx126-s2 (the KJ-1 counterexample: v1 reported
##       UNSCREENED -- (3.53) closure failed because two m=2 candidates
##       silently were NOT well-defined homomorphisms despite passing the
##       three original (F2) conditions)
##   (3) all 17 c-notin-N windows re-computed in search/wall-miner-v4.g
##       (compared against v4's RECORDED shadow_total / ker_size /
##       ta_assert_holds values, read from
##       search/certs/wall_miner_v4_20260729.json -- baked in below as a
##       literal table rather than re-parsed at runtime, since GAP has no
##       JSON parser in this repo's toolchain; see gaplib_common.g's
##       ReadJsonStringField for why only single-string-field reads are
##       supported, not structured arrays)
##
## For each of the 17+1 windows, this reports whether v1.1 changed
## shadow_total / ker_size / ta_assert_holds relative to the v4 baseline --
## a MISMATCH is not a bug in this driver, it is the whole point of running
## it (rough is fine, but the asserts and the comparison itself must be
## honest).
##
## Output: search/certs/kerchi_judge_v11_regression_20260729.json
#############################################################################

JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");

Read("search/gaplib_common.g");   # WriteFile/JStr/JB/JArr already defined by
                                   # kerchi-judge.g's own Read of it; re-reading
                                   # is a harmless no-op redefinition (same file).

# ---- v4 baseline (search/certs/wall_miner_v4_20260729.json, literal transcription) ----
V4_BASELINE := [
  rec(id:="W-A-B3idx96-s2",  shadow_total:=4,  ker_size:=1, ta_holds:=true),
  rec(id:="W-A-B3idx96-s4",  shadow_total:=4,  ker_size:=1, ta_holds:=true),
  rec(id:="W-A-B3idx108-s1", shadow_total:=4,  ker_size:=1, ta_holds:=true),
  rec(id:="W-A-B3idx120-s2", shadow_total:=8,  ker_size:=1, ta_holds:=true),
  rec(id:="W-A-B3idx144-s1", shadow_total:=12, ker_size:=3, ta_holds:=true),
  rec(id:="W-A-B3idx144-s3", shadow_total:=12, ker_size:=3, ta_holds:=true),
  rec(id:="W-A-B3idx144-s4", shadow_total:=4,  ker_size:=1, ta_holds:=true),
  rec(id:="W-A-B3idx144-s6", shadow_total:=8,  ker_size:=1, ta_holds:=true),
  rec(id:="W-A-B3idx162-s2", shadow_total:=2,  ker_size:=1, ta_holds:=true),
  rec(id:="W-A-B3idx162-s3", shadow_total:=6,  ker_size:=1, ta_holds:=true),
  rec(id:="W-A-B3idx162-s4", shadow_total:=6,  ker_size:=1, ta_holds:=true),
  rec(id:="W-A-B3idx168-s2", shadow_total:=12, ker_size:=1, ta_holds:=true),
  rec(id:="W-A-B3idx192-s2", shadow_total:=8,  ker_size:=1, ta_holds:=true),
  rec(id:="W-A-B3idx192-s3", shadow_total:=4,  ker_size:=1, ta_holds:=true),
  rec(id:="W-A-B3idx192-s4", shadow_total:=8,  ker_size:=1, ta_holds:=true),
  rec(id:="W-A-B3idx192-s5", shadow_total:=4,  ker_size:=1, ta_holds:=true),
  rec(id:="W-A-B3idx192-s6", shadow_total:=4,  ker_size:=1, ta_holds:=true)
];;

REGRESSION_RESULTS := [];;

CompareRow := function(baseline, result)
  local row;
  row := rec(window_id := baseline.id,
             v4_shadow_total := baseline.shadow_total, v11_shadow_total := result.shadow_total,
             v4_ker_size := baseline.ker_size, v11_ker_size := result.ker_size,
             v4_ta_holds := baseline.ta_holds, v11_ta_holds := result.ta_assert_holds,
             settled_fail_count := result.settled_fail_count,
             verdict := result.verdict,
             unchanged := (baseline.shadow_total = result.shadow_total)
                          and (baseline.ker_size = result.ker_size)
                          and (baseline.ta_holds = result.ta_assert_holds));
  return row;
end;;

Print("=== KJ-1 regression: 17 wall-miner-v4 windows, re-judged with kerchi-judge v1.1 ===\n");
for bl in V4_BASELINE do
  res := JudgeFromLinsNode(192, bl.id);;
  row := CompareRow(bl, res);;
  Add(REGRESSION_RESULTS, row);
  Print("  ", bl.id, ": v4(shadow=", bl.shadow_total, ",ker=", bl.ker_size, ",TA=", bl.ta_holds,
        ")  v1.1(shadow=", res.shadow_total, ",ker=", res.ker_size, ",TA=", res.ta_assert_holds,
        ",settled_fail=", res.settled_fail_count, ")  UNCHANGED=", row.unchanged, "\n");
od;

Print("\n=== KJ-1 regression: W-C-N5cong fixture ===\n");
psi2 := IsomorphismPermGroup(Group([[1,1],[0,1]]*One(GF(2)), [[1,0],[1,1]]*One(GF(2))));;
psi5 := IsomorphismPermGroup(Group([[1,1],[0,1]]*One(GF(5)), [[1,0],[4,1]]*One(GF(5))));;
DP := DirectProduct(Image(psi2), Image(psi5));;
s1p5 := Image(Embedding(DP,1), Image(psi2,[[1,1],[0,1]]*One(GF(2)))) *
        Image(Embedding(DP,2), Image(psi5,[[1,1],[0,1]]*One(GF(5))));;
s2p5 := Image(Embedding(DP,1), Image(psi2,[[1,0],[1,1]]*One(GF(2)))) *
        Image(Embedding(DP,2), Image(psi5,[[1,0],[4,1]]*One(GF(5))));;
resP5 := JudgeWindow(s1p5, s2p5, "W-C-N5cong-regression");;
p5Baseline := rec(id:="W-C-N5cong", shadow_total:=40, ker_size:=5, ta_holds:=true);;
p5Row := CompareRow(p5Baseline, resP5);;
Print("  W-C-N5cong: baseline(shadow=40,ker=5,TA=true)  v1.1(shadow=", resP5.shadow_total,
      ",ker=", resP5.ker_size, ",TA=", resP5.ta_assert_holds,
      ",settled_fail=", resP5.settled_fail_count, ")  UNCHANGED=", p5Row.unchanged, "\n");

Print("\n=== KJ-1 focus case: W-A-B3idx126-s2 (the counterexample that motivated this fix) ===\n");
res126 := JudgeFromLinsNode(192, "W-A-B3idx126-s2");;
Print("  BEFORE (kerchi-judge v1, no settled clause): verdict=UNSCREENED (closure_353_holds=false),\n");
Print("    shadow_total=12, ker_size=6, crosscheck_vs_EnumerateReducedHexagon=true (both v1's (F2)\n");
Print("    and the pre-existing EnumerateReducedHexagon agreed on 12 shadows, but the (3.53)\n");
Print("    regular-representation construction failed to close because 2 of those m=2 shadows\n");
Print("    were not actually well-defined homomorphisms)\n");
Print("  AFTER  (kerchi-judge v1.1, settled clause added): verdict=", res126.verdict,
      "  shadow_total=", res126.shadow_total, "  ker_size=", res126.ker_size,
      "  settled_fail_count=", res126.settled_fail_count,
      "  ta_assert_holds=", res126.ta_assert_holds,
      "  closure_353_holds=", res126.closure_353_holds,
      "  crosscheck_vs_EnumerateReducedHexagon=", res126.crosscheck_vs_EnumerateReducedHexagon, "\n");
Print("  NOTE: crosscheck now reads ", res126.crosscheck_vs_EnumerateReducedHexagon,
      " -- EnumerateReducedHexagon (the pre-existing quotient-shortcut enumerator, used\n");
Print("    unmodified since wall-miner-v1.g) has NO settled/well-definedness clause of its own,\n");
Print("    so it still reports the old (pre-fix) 12-shadow answer for this window; the v1.1\n");
Print("    divergence from it is itself a finding about EnumerateReducedHexagon, not\n");
Print("    interpreted further here.\n");

#############################################################################
## ---------------------- summary + JSON --------------------------------------
#############################################################################
changedCount := Length(Filtered(REGRESSION_RESULTS, r -> not r.unchanged));;
totalSettledFails17 := Sum(List(REGRESSION_RESULTS, r -> r.settled_fail_count));;

Print("\n=== SUMMARY ===\n");
Print("17 v4 windows re-judged: ", Length(REGRESSION_RESULTS), "\n");
Print("Windows where v1.1 CHANGED shadow_total/ker_size/ta_holds vs v4: ", changedCount, "\n");
Print("Total settled-clause rejections across the 17 windows: ", totalSettledFails17, "\n");
Print("W-C-N5cong fixture unchanged: ", p5Row.unchanged, " (settled_fail_count=", resP5.settled_fail_count, ")\n");
Print("W-A-B3idx126-s2: settled_fail_count=", res126.settled_fail_count,
      "  verdict now=", res126.verdict, " (was UNSCREENED before KJ-1)\n");

RowJson := function(r)
  return Concatenation("    {\"window_id\":", JStr(r.window_id),
    ",\"v4_shadow_total\":", String(r.v4_shadow_total),
    ",\"v11_shadow_total\":", String(r.v11_shadow_total),
    ",\"v4_ker_size\":", String(r.v4_ker_size),
    ",\"v11_ker_size\":", String(r.v11_ker_size),
    ",\"v4_ta_holds\":", JB(r.v4_ta_holds),
    ",\"v11_ta_holds\":", JB(r.v11_ta_holds),
    ",\"settled_fail_count\":", String(r.settled_fail_count),
    ",\"verdict\":", JStr(r.verdict),
    ",\"unchanged\":", JB(r.unchanged), "}");
end;;

outParts := [];;
Add(outParts, "{\n");
Add(outParts, "  \"generated_by\": \"search/kerchi-judge-v11-regression.g\",\n");
Add(outParts, "  \"note\": \"KJ-1 (ruling 169) regression check: kerchi-judge v1.1 (settled clause added) re-run on the 17 wall-miner-v4.g windows + W-C-N5cong + the W-A-B3idx126-s2 counterexample; NOT a ledger claim, no cross-check performed beyond the existing crosscheck_vs_EnumerateReducedHexagon field\",\n");
Add(outParts, Concatenation("  \"windows_17_changed_count\": ", String(changedCount), ",\n"));
Add(outParts, Concatenation("  \"windows_17_total_settled_fail_count\": ", String(totalSettledFails17), ",\n"));
Add(outParts, "  \"windows_17\": [\n");
for i in [1 .. Length(REGRESSION_RESULTS)] do
  Add(outParts, RowJson(REGRESSION_RESULTS[i]));
  if i < Length(REGRESSION_RESULTS) then Add(outParts, ",\n"); else Add(outParts, "\n"); fi;
od;
Add(outParts, "  ],\n");
Add(outParts, Concatenation("  \"p5_fixture\": ", RowJson(p5Row), ",\n"));
Add(outParts, Concatenation("  \"idx126_s2_focus_case\": {",
  "\"before_v1\": {\"verdict\":\"UNSCREENED\",\"shadow_total\":12,\"ker_size\":6,",
  "\"closure_353_holds\":false,\"crosscheck_vs_EnumerateReducedHexagon\":true},",
  "\"after_v1.1\": ", ResultJson(res126), "},\n"));
Add(outParts, "  \"verbatim_note\": \"a MISMATCH between v4-baseline and v1.1 columns is not a driver bug -- it is the regression check's actual finding, reported without interpretation\"\n");
Add(outParts, "}\n");

WriteFile("search/certs/kerchi_judge_v11_regression_20260729.json", Concatenation(outParts));
Print("\nWrote search/certs/kerchi_judge_v11_regression_20260729.json\n");
Print("KJ1_REGRESSION_DONE\n");
