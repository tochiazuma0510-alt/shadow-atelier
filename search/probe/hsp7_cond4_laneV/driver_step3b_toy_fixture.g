# driver_step3b_toy_fixture.g -- mandatory permanent regression fixture
# (docs/notes/hsp7_hexagon_arbitration_v1.md SS5.4 item 4). Runs
# TestToyFixtureLiteralVsFixed(): a LITERAL (fp-group + IsomorphismPermGroup)
# construction of a small scale-model B3/N (order 162), independent of the
# state machine, compared against EvalFullHexagonFixed (the repaired
# evaluator, repair A: pure-Q factors expanded to sigma-words and pushed
# through the validated ApplyGen). Fail-closed: if this does not show 0
# mismatches, the repaired evaluator must not be trusted on the real P/P x C7.
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/probe/hsp7_cond4_laneV/statemachine_lib.g");

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

r := TestToyFixtureLiteralVsFixed();;
if not r.ok then
  Print("[STOP] TOY fixture construction itself failed: ", r.reason, "\n");
  Error("TOY fixture construction failed");
fi;

Print("Size(B3/N) = ", r.size_B3N, " (expect 162)\n");
Print("Size(Q) = ", r.size_Q, " (expect 27)\n\n");
Print("m | k | literal(3.3,3.4) | fixed(3.3,3.4) | agree\n");
for row in r.results do
  Print(row.m, " | ", row.k, " | ",
        PF(row.literal_hex33), "/", PF(row.literal_hex34), " | ",
        PF(row.fixed_hex33), "/", PF(row.fixed_hex34), " | ",
        row.agree, "\n");
od;

Print("\nmismatches = ", r.mismatches, " (of ", Length(r.results), " (m,k) cells; 0 required)\n");

if r.mismatches = 0 then
  Print("\n[GATE PASS] TOY fixture: literal and fixed evaluator agree on all cells, ",
        "and literal itself confirms Prop 3.4's all-PASS prediction (theta-anti-fixed, ",
        "tau-fixed a). EvalFullHexagonFixed may be trusted on the real P / P x C7.\n");
else
  Print("\n[STOP] TOY fixture mismatch -- do NOT trust EvalFullHexagonFixed on the real construction.\n");
  Error("TOY fixture mismatch");
fi;
QUIT;
