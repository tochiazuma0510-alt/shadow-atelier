# driver_step0_a5conv.g -- Lane V (Verify), 0-te (all lanes common) fail-closed gate.
# Design source: docs/notes/hsp7_cond4_lanespec_v1.md (v1.2) SS0.2 (C-1, verbatim block),
# docs/week1-定義ノート.md SS1.5.4 (A5-CONV definition, source of the verbatim block).
#
# WARNING (verbatim from SS1.5.4, must be respected by the implementer):
#   The definition formulas X=a*t^-1, Y=t*X*t^-1, s=t*X^3 are PAPER products.
#   Typed literally into GAP they give a DIFFERENT permutation (GAP: i^(B*A) = (i^B)^A
#   for paper word "AB"). The falsifier's captured-by-number note says:
#   GAP `a*t^-1` = (1,4,5,3,2) (NOT the paper X) ; GAP `t^-1*a` = (1,3,2,4,5) = paper X.
#   So each defining formula must be typed REVERSED (W-1) to land on the correct value.
#
Read("search/probe/wac_v1/gap_output_prelude.g");

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

t := (1,2,3);;
a := (1,4,5);;

# paper X := a t^-1  -->  GAP: t^-1 * a   (W-1 reversal)   [renamed Xp: GAP reserves 'X']
Xp := t^-1 * a;;
# paper Y := t X t^-1 --> GAP: t^-1 * X * t   (W-1 reversal, conjugation "t (.) t^-1")
Yp := t^-1 * Xp * t;;
# paper s := t X^3    --> GAP: X^3 * t   (W-1 reversal)
sp := Xp^3 * t;;

Print("X computed = ", Xp, " (expect (1,3,2,4,5))\n");
Print("Y computed = ", Yp, " (expect (1,3,4,5,2))\n");
Print("s computed = ", sp, " (expect (1,4)(3,5))\n");

xOK := (Xp = (1,3,2,4,5));
yOK := (Yp = (1,3,4,5,2));
sOK := (sp = (1,4)(3,5));
Print("[", PF(xOK), "] X matches paper value\n");
Print("[", PF(yOK), "] Y matches paper value\n");
Print("[", PF(sOK), "] s matches paper value\n");

# main judgment (3 lines, per SS1.5.4 / mail 09 F10): paper word y x^-1, GAP form X^-1 * Y
evYXinv := Xp^-1 * Yp;;
Print("ev(y x^-1) computed (GAP: X^-1 * Y) = ", evYXinv, "\n");

result := "other";;
if evYXinv = (1,2,4) then
  result := "correct";
elif evYXinv = (2,5,3) then
  result := "reversed";
fi;
Print("A5-CONV result = ", result, "\n");

if not (xOK and yOK and sOK) then
  Print("[FAIL-CLOSED] X/Y/s fixture construction itself did not match the pinned paper values -- ",
        "stopping before main judgment is even trustworthy.\n");
fi;

if result <> "correct" then
  Print("\n[STOP] A5-CONV result is NOT 'correct' (got: ", result, "). ",
        "Fail-closed per SS0.2: no cert will be produced, no further calibration run executes.\n");
else
  Print("\n[GATE PASS] A5-CONV = correct. Proceeding is authorized.\n");
fi;

QUIT;
