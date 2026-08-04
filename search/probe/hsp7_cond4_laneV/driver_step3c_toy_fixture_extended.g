# driver_step3c_toy_fixture_extended.g -- CV-9 副検問 B-2 (c-nontrivial cell +
# negative fixture) and non-blocking m2 (A5-CONV-analog letter-order fidelity
# on the real P, exercising the NEW ApplyFreeWord/LetterRepAssocWord path that
# v2 introduced). docs/notes/hsp7_cond4_cv9_reading_v1.md SS4 M3/m1/m2.
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/probe/hsp7_cond4_laneV/statemachine_lib.g");
LoadPackage("anupq");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ================= B-2 part 1: extended TOY fixture (c-alive + negative) =================
ext := TestToyFixtureExtended();;
if not ext.ok then
  Print("[STOP] extended TOY fixture construction failed: ", ext.reason, "\n");
  Error("extended TOY fixture construction failed");
fi;
Print("Size(control TOY B3/N0) = ", ext.size_control_B3N0, " (expect 486)\n");
Print("Order(c) in control TOY = ", ext.order_c_control, " (expect 3, c must survive)\n\n");
Print("cell | m | k | literal(3.3,3.4) | fixed(3.3,3.4) | agree\n");
for row in ext.results do
  Print(row.cell, " | ", row.m, " | ", row.k, " | ",
        PF(row.literal_hex33), "/", PF(row.literal_hex34), " | ",
        PF(row.fixed_hex33), "/", PF(row.fixed_hex34), " | ", row.agree, "\n");
od;
Print("\nextended mismatches = ", ext.mismatches, " (0 required)\n");
if ext.mismatches > 0 then
  Print("[STOP] extended TOY fixture mismatch.\n");
  Error("extended TOY fixture mismatch");
fi;
Print("[GATE PASS] extended TOY fixture: c-alive cells all PASS (agree with literal), ",
      "negative fixture f=x correctly FAILS in both literal and fixed evaluator ",
      "(evaluator demonstrated non-constant).\n\n");

# ================= m2: letter-order fidelity on the REAL P (A5-CONV-analog for
# the new free-group/ApplyFreeWord path v2 introduced). Compares ApplyFreeWord's
# result (sigma-word expansion via LetterRepAssocWord) against DIRECT pcgs
# multiplication of the same word in P, for a word with mixed signs/generators
# (not just x^k or y^k, which would not exercise interleaving). =================
Read("search/probe/hsp7_cond4_laneV/PQ_OUTPUT_P.g");
P := F;;
xbar := MapImages[1];;
ybar := MapImages[2];;

FreeXY2 := FreeGroup("x","y");;
Fx2 := FreeXY2.1;;  Fy2 := FreeXY2.2;;
testWord := Fx2 * Fy2^-1 * Fx2^2 * Fy2^3 * Fx2^-1;;   # mixed signs, interleaved
directVal := xbar * ybar^-1 * xbar^2 * ybar^3 * xbar^-1;;   # same word, direct pcgs multiplication
viaApplyFreeWord := ApplyFreeWord([1, Identity(P)], testWord, xbar, ybar, Identity(P));;
Print("direct pcgs value   : ", directVal, "\n");
Print("ApplyFreeWord result: t=", viaApplyFreeWord[1], " d=", viaApplyFreeWord[2], "\n");
letterOrderOK := (viaApplyFreeWord[1] = 1) and (viaApplyFreeWord[2] = directVal);;
Print("[", PF(letterOrderOK), "] letter-order fidelity (ApplyFreeWord == direct pcgs multiplication) on real P\n");

if not letterOrderOK then
  Print("[STOP] letter-order fidelity check FAILED on real P -- the new LetterRepAssocWord/",
        "ApplyFreeWord path may be reversing or misordering letters.\n");
  Error("letter-order fidelity check FAILED");
fi;
Print("\n[DONE] driver_step3c_toy_fixture_extended.g complete.\n");
QUIT;
