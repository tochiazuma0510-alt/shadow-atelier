## search/_probe_r4_retype_smoke.g -- local smoke test for P88-R4-1 retype.
## Loads strike-r4.g in R4_LIBRARY_ONLY mode (no gate run, no window struck)
## and asserts the two windows still construct correctly (S1/S2 literals,
## canonical-id SHA-256) after the field-12/field-30 retype. Does NOT run
## MeasureWindow (that needs a full ~450M scan) -- this only checks that the
## driver still loads and the window table/canonical-id machinery it shares
## with MeasureWindow's surrounding code is intact.

R4_LIBRARY_ONLY := true;;
Read("search/strike-r4.g");

Print("\n=== smoke: R4_LIBRARY_ONLY load OK ===\n");
Print("R4_WINDOWS count = ", Length(R4_WINDOWS), "\n");

ok := true;;
for w in R4_WINDOWS do
  built := BuildS1S2E(w.a1, w.b1, w.n);;
  s1ok := (built.s1 = w.s1lit);;
  s2ok := (built.s2 = w.s2lit);;
  canonStr := CanonicalStringR4(w.id, w.n, w.ell, w.r, w.t, w.a1, w.b1, built.s1, built.s2);;
  sha := Sha256OfString(canonStr);;
  shaOk := (sha = R4_CANONICAL_SHA.(w.shaKey));;
  Print("[", w.id, "] s1_match=", s1ok, " s2_match=", s2ok,
        " canonical_sha_match=", shaOk, " (", sha, ")\n");
  ok := ok and s1ok and s2ok and shaOk;;
od;

Print("\n=== smoke overall: ", ok, " ===\n");
if ok then
  Print("R4_RETYPE_SMOKE_OK\n");
else
  Print("R4_RETYPE_SMOKE_FAIL\n");
fi;
