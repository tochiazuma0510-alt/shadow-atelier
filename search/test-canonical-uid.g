#############################################################################
## search/test-canonical-uid.g -- P81-F regression: canonical UID selftest
##
## Regression per coordinator's ruling (2026-07-30, W7 correction):
##   (1) same-window invariance: (a1,b1) -> (a1^g, b1^g) for several random
##       g in Sym(n) (SIMULTANEOUS conjugation of BOTH generators) must give
##       the SAME uid_sha256. Swap invariance is explicitly NOT required
##       (ordered pair -- braid asymmetry) and is not tested here.
##   (2) cross-window distinctness: the three known windows W-D-A16-11a /
##       W-D-A18-13a / W-D-A20-15a must have pairwise distinct uid_sha256.
##   (3) LID-1 (literal-word hash) is reported alongside uid_sha256 as a
##       separate ID -- and, as a sanity check (not a hard requirement),
##       is shown to typically CHANGE under the same conjugation that
##       leaves uid_sha256 fixed (demonstrating the two IDs measure
##       different things: display vs. window identity).
##
## Input source: search/w62-windows.g (a1,b1,n verbatim from
## search/strike-a{16,18,20}.g), per the coordinator's W7 ruling.
##
## Output: search/certs/canonical_uid_selftest_20260730.json
#############################################################################

Read("search/canonical-uid.g");   # also pulls in gaplib_common.g, w62-windows.g

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

T0 := GAPLIB_WallElapsedMs();;

N_CONJ_TRIALS := 3;;   # random simultaneous-conjugation trials per window

#############################################################################
## ---------------------- baseline UID/LID-1 for the 3 known windows --------
#############################################################################
Print("=== baseline canonical UID / LID-1 for the 3 known W-D windows ===\n");
baseline := [];;
for w in W62_WINDOWS do
  r := WindowCanonicalUID(w.id, w.n, w.a1, w.b1);
  Add(baseline, r);
  Print("  ", w.id, " (n=", w.n, "):\n");
  Print("    uid_sha256  = ", r.uid_sha256, "\n");
  Print("    lid1_sha256 = ", r.lid1_sha256, "\n");
od;

#############################################################################
## ---------------------- (1) simultaneous-conjugation invariance -----------
#############################################################################
Print("\n=== (1) simultaneous-conjugation invariance (", N_CONJ_TRIALS, " random g per window) ===\n");
conjResults := [];;
allConjUidStable := true;;
anyLid1ChangedUnderConj := false;;
for wi in [1 .. Length(W62_WINDOWS)] do
  w := W62_WINDOWS[wi];;
  base := baseline[wi];;
  Sn := SymmetricGroup(w.n);;
  for t in [1 .. N_CONJ_TRIALS] do
    g := Random(Sn);;
    a1g := w.a1 ^ g;;
    b1g := w.b1 ^ g;;
    rc := WindowCanonicalUID(w.id, w.n, a1g, b1g);;
    uidStable := (rc.uid_sha256 = base.uid_sha256);;
    lid1Changed := (rc.lid1_sha256 <> base.lid1_sha256);;
    if not uidStable then allConjUidStable := false; fi;
    if lid1Changed then anyLid1ChangedUnderConj := true; fi;
    Add(conjResults, rec(id := w.id, trial := t, g := String(g),
          uid_sha256 := rc.uid_sha256, uid_stable := uidStable,
          lid1_sha256 := rc.lid1_sha256, lid1_changed := lid1Changed));
    Print("  ", w.id, " trial ", t, ": uid_stable=", PF(uidStable),
          "  lid1_changed=", PF(lid1Changed), "\n");
  od;
od;
Print("\nall_conjugation_trials_uid_stable = ", PF(allConjUidStable), "\n");
Print("any_lid1_changed_under_conjugation = ", PF(anyLid1ChangedUnderConj), "\n");

#############################################################################
## ---------------------- (2) cross-window distinctness ---------------------
#############################################################################
Print("\n=== (2) cross-window distinctness ===\n");
crossPairs := [];;
allCrossDistinct := true;;
for i in [1 .. Length(baseline)] do
  for j in [i+1 .. Length(baseline)] do
    distinct := (baseline[i].uid_sha256 <> baseline[j].uid_sha256);;
    if not distinct then allCrossDistinct := false; fi;
    Add(crossPairs, rec(id_a := baseline[i].id, id_b := baseline[j].id, distinct := distinct));
    Print("  ", baseline[i].id, " vs ", baseline[j].id, ": distinct=", PF(distinct), "\n");
  od;
od;
Print("\nall_cross_window_uid_distinct = ", PF(allCrossDistinct), "\n");

overallPass := allConjUidStable and allCrossDistinct;;
Print("\n=== OVERALL: ", PF(overallPass), " ===\n");

#############################################################################
## ---------------------- provenance (script hashes) -------------------------
#############################################################################
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_uid_selftest_sha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1..64]};
end;;

T1 := GAPLIB_WallElapsedMs();;

#############################################################################
## ---------------------- write JSON ------------------------------------------
#############################################################################
BaselineJson := function(r)
  return Concatenation("{\"id\":", JStr(r.id), ",\"n\":", String(r.n),
    ",\"uid_sha256\":", JStr(r.uid_sha256),
    ",\"lid1_sha256\":", JStr(r.lid1_sha256),
    ",\"uid_serialized_preview\":", JStr(r.uid_serialized_preview),
    ",\"lid1_serialized\":", JStr(r.lid1_serialized), "}");
end;;

ConjJson := function(r)
  return Concatenation("{\"id\":", JStr(r.id), ",\"trial\":", String(r.trial),
    ",\"g\":", JStr(r.g), ",\"uid_sha256\":", JStr(r.uid_sha256),
    ",\"uid_stable\":", JB(r.uid_stable),
    ",\"lid1_sha256\":", JStr(r.lid1_sha256),
    ",\"lid1_changed\":", JB(r.lid1_changed), "}");
end;;

CrossJson := function(r)
  return Concatenation("{\"id_a\":", JStr(r.id_a), ",\"id_b\":", JStr(r.id_b),
    ",\"distinct\":", JB(r.distinct), "}");
end;;

outParts := [];;
Add(outParts, "{\n");
Add(outParts, "  \"schema\": \"canonical-uid-selftest/v1\",\n");
Add(outParts, "  \"generated_by\": \"search/test-canonical-uid.g\",\n");
Add(outParts, "  \"task\": \"W7/P81-F canonical UID (judge v1.4) -- domain action-graph bliss canonical form, per coordinator ruling 2026-07-30\",\n");
Add(outParts, "  \"note\": \"UID = SHA-256 of the bliss-canonical, vertex-coloured domain action digraph (subdivision encoding, no multi-edges); LID-1 = SHA-256 of the literal generator words (display-dependent, NOT claimed window-invariant). NOT a ledger claim; single implementation, no independent crosscheck performed.\",\n");
Add(outParts, Concatenation("  \"input_source\": ", JStr(CANONICAL_UID_INPUT_SOURCE), ",\n"));
Add(outParts, Concatenation("  \"n_conjugation_trials_per_window\": ", String(N_CONJ_TRIALS), ",\n"));
Add(outParts, "  \"baseline\": [\n    ");
Add(outParts, JoinC(List(baseline, BaselineJson), ",\n    "));
Add(outParts, "\n  ],\n");
Add(outParts, "  \"conjugation_invariance_trials\": [\n    ");
Add(outParts, JoinC(List(conjResults, ConjJson), ",\n    "));
Add(outParts, "\n  ],\n");
Add(outParts, Concatenation("  \"all_conjugation_trials_uid_stable\": ", JB(allConjUidStable), ",\n"));
Add(outParts, Concatenation("  \"any_lid1_changed_under_conjugation\": ", JB(anyLid1ChangedUnderConj), ",\n"));
Add(outParts, "  \"cross_window_distinctness\": [\n    ");
Add(outParts, JoinC(List(crossPairs, CrossJson), ",\n    "));
Add(outParts, "\n  ],\n");
Add(outParts, Concatenation("  \"all_cross_window_uid_distinct\": ", JB(allCrossDistinct), ",\n"));
Add(outParts, Concatenation("  \"overall_pass\": ", JB(overallPass), ",\n"));
Add(outParts, Concatenation("  \"elapsed_ms\": ", String(T1 - T0), ",\n"));
Add(outParts, Concatenation("  \"gap_version\": ", JStr(GAPInfo.Version), ",\n"));
Add(outParts, Concatenation("  \"digraphs_pkg_version\": ", JStr(InstalledPackageVersion("digraphs")), ",\n"));
Add(outParts, "  \"provenance\": {\n");
Add(outParts, Concatenation("    \"canonical_uid_g_sha256\": ", JStr(ComputeSha256File("search/canonical-uid.g")), ",\n"));
Add(outParts, Concatenation("    \"test_canonical_uid_g_sha256\": ", JStr(ComputeSha256File("search/test-canonical-uid.g")), ",\n"));
Add(outParts, Concatenation("    \"w62_windows_g_sha256\": ", JStr(ComputeSha256File("search/w62-windows.g")), "\n"));
Add(outParts, "  }\n");
Add(outParts, "}\n");

WriteFile("search/certs/canonical_uid_selftest_20260730.json", Concatenation(outParts));
Print("\nWrote search/certs/canonical_uid_selftest_20260730.json\n");
Print("CANONICAL_UID_SELFTEST_DONE\n");
