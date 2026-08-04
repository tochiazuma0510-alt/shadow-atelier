# driver_step3_selftest.g -- run SelfTestStateMachine and report; fail-closed if any
# mismatch or braid-relation failure is found (would falsify the hand-derived inverse
# tables in statemachine_lib.g before they are trusted on the real P / P x C7).
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/probe/hsp7_cond4_laneV/statemachine_lib.g");

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

r := SelfTestStateMachine();;
Print("total_points = ", r.total_points, "\n");
Print("[", PF(r.forward_mismatches = 0), "] forward_mismatches (ApplyGen vs BuildQTGeneral PermList) = ", r.forward_mismatches, "\n");
Print("[", PF(r.inverse_roundtrip_mismatches = 0), "] inverse_roundtrip_mismatches (gen then gen^-1 != identity) = ", r.inverse_roundtrip_mismatches, "\n");
Print("[", PF(r.braid_relation_fail = 0), "] braid_relation_fail (s1 s2 s1 != s2 s1 s2 in ApplyGen machine) = ", r.braid_relation_fail, "\n");

Print("\n(note: r.braid_relation_fail on the ARBITRARY-element S4 toy is EXPECTED to be\n",
      "nonzero -- confirmed independently that even BuildQTGeneral's own PermList fails\n",
      "the braid relation for arbitrary phiX/phiY/phiC; the table only represents a\n",
      "genuine B3-quotient when phiX/phiY/phiC come from an actual B3-compatible triple.\n",
      "See SelfTestBraidOnGenuineInstance below for the real validity check.)\n\n");

r2 := SelfTestBraidOnGenuineInstance();;
Print("main_points (dihedral G3, c->1) = ", r2.main_points, "\n");
Print("[", PF(r2.main_braid_fail = 0), "] main_braid_fail = ", r2.main_braid_fail, "\n");
Print("ctrl_points (G3 x C5, control-style embedding) = ", r2.ctrl_points, "\n");
Print("[", PF(r2.ctrl_braid_fail = 0), "] ctrl_braid_fail = ", r2.ctrl_braid_fail, "\n");

allOK := (r.forward_mismatches = 0) and (r.inverse_roundtrip_mismatches = 0)
         and (r2.main_braid_fail = 0) and (r2.ctrl_braid_fail = 0);;
if allOK then
  Print("\n[GATE PASS] state machine self-test: table matches BuildQTGeneral exactly ",
        "(forward+inverse, ", r.total_points, " toy points), AND braid relation holds ",
        "on genuine main-window-style (", r2.main_points, " pts) and control-window-style (",
        r2.ctrl_points, " pts) instances.\n");
else
  Print("\n[STOP] state machine self-test FAILED -- do not trust ApplyGen on the real P/P x C7.\n");
fi;
QUIT;
