Read("search/probe/wac_v1/gap_output_prelude.g");
# A5-CONV (docs/week1-定義ノート.md SS1.5.4, verbatim; also hsp7_cond4_lanespec_v1.md SS0.2 v1.2).
# Fixture (A1.v2.json marking): t=(1,2,3), a=(1,4,5).
# Definitions are PAPER products; per SS0.2 note they must be typed REVERSED into GAP
# (paper "AB" = GAP "B*A"): paper X=a*t^-1 -> GAP t^-1*a ; paper Y=t*X*t^-1 -> GAP t^-1*X*t.
tt := (1,2,3);
aa := (1,4,5);
XX := tt^-1 * aa;
YY := tt^-1 * XX * tt;
Print("X = ", XX, "  (expect (1,3,2,4,5))\n");
Print("Y = ", YY, "  (expect (1,3,4,5,2))\n");

# main judgment (3 lines, F10-audited): ev(y x^-1) = X^-1*Y
ev := XX^-1 * YY;
Print("ev(y x^-1) = X^-1*Y = ", ev, "\n");

if ev = (1,2,4) then
  Print("A5-CONV RESULT: correct\n");
elif ev = (2,5,3) then
  Print("A5-CONV RESULT: reversed\n");
else
  Print("A5-CONV RESULT: other -- ", ev, "\n");
fi;
QUIT;
