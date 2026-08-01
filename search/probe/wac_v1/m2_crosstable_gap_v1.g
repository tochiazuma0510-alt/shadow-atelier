# m2_crosstable_gap_v1.g -- GAP-side n-parameterized cross table for the (M2) family
# identification note (docs/notes/m2_family_identification_v1.md, theorem M2-GEO).
# Commander order 2026-08-01 (small task, delivered via SendMessage to implementer).
#
# PURPOSE: generalize search/probe/wac_v1/cbeta_crosstable.g (which was hard-wired to
# n=7, alpha,alphaPrime in {1,2,3}) to n in {3,7,9,11,13}, alpha,alphaPrime ranging over
# ALL unit classes mod +-1, and cross-check against the M2-GEO prediction (identity
# matrix). The prediction is NOT written into this script's search logic -- it is only
# compared AFTER the raw cross table is computed (see bottom block).
#
# INDEPENDENCE: this script imports ONLY search/probe/wac_v1/cbeta_model_indep.g
# (GAP-native BuildModel / BuildAbstract / TripleConjugate, itself independent of the
# python cbeta_model.py / cbeta_nielsen.py / m2_family_check.py). It does not import
# m2_family_check.py or read its output. This keeps the GAP run a genuinely separate
# system from the python spot-check reported in m2_family_identification_v1.md Sec 9
# (which is itself single-system / not cross-checked). Two independent machine systems
# (python and GAP) now both compute the identity-diagonal claim.
#
# n=5 DISCIPLINE (K^(5) blind, same regime as m2_family_check.py's ALLOWED_N):
ALLOWED_N := [3,7,9,11,13];;
if 5 in ALLOWED_N then
    Error("FATAL: 5 must not be in ALLOWED_N (K^(5) is blind)");
fi;;

Read("search/probe/wac_v1/cbeta_model_indep.g");;

# GAP wraps Print/PrintTo output at the terminal width by default, which corrupts
# JSON (mid-token line breaks with a trailing backslash). Widen it before writing
# the cert file.
SizeScreen([1000000, 1000000]);;

# ---------- helpers ----------
GcdInt2 := function(a,b) return GcdInt(a,b); end;;

UnitsModN := function(n)
    local u, r;
    r := [];;
    for u in [1..n-1] do
        if GcdInt(u,n) = 1 then Add(r,u); fi;
    od;
    return r;
end;;

# representatives of (Z/n)^x / {+-1}, smallest-first, same rule as m2_family_check.py:
# walk units in increasing order, keep u if (n-u) mod n is not already a kept rep.
RepsModPM := function(n)
    local units, reps, u, negu;
    units := UnitsModN(n);;
    reps := [];;
    for u in units do
        negu := (n - u) mod n;
        if not (negu in reps) then Add(reps, u); fi;
    od;
    return reps;
end;;

JBool := function(b)
    if b = true then return "true";
    elif b = false then return "false";
    else return "null"; fi;
end;;

JIntList := function(L)
    return Concatenation("[", JoinStringsWithSeparator(List(L, String), ","), "]");
end;;

JBoolMatrix := function(M)
    local rows;
    rows := List(M, row -> Concatenation("[", JoinStringsWithSeparator(List(row, JBool), ","), "]"));
    return Concatenation("[", JoinStringsWithSeparator(rows, ","), "]");
end;;

# ---------- per-n computation ----------
# out : list of strings, appended to and joined at the end -> written as one JSON file.
out := [];;
AddL := function(s) Add(out, s); end;;

AddL("{");
AddL("  \"generated_by\": \"search/probe/wac_v1/m2_crosstable_gap_v1.g\",");
AddL("  \"gap_invocation\": \".\\\\gap.ps1 search\\\\probe\\\\wac_v1\\\\m2_crosstable_gap_v1.g\",");
AddL("  \"independent_of\": \"m2_family_check.py (python) -- imports only cbeta_model_indep.g\",");
AddL("  \"allowed_n\": [3,7,9,11,13],");
AddL("  \"n5_excluded\": true,");
AddL("  \"n5_exclusion_method\": \"hard assert on ALLOWED_N literal at script top; QUIT if violated\",");
AddL("  \"conventions_used\": {");
AddL("    \"ledger_version\": \"conventions_ledger_v1\",");
AddL("    \"perm_composition\": \"gap_native_right_action_x_to_the_g\",");
AddL("    \"conjugation\": \"gap_native x^g\",");
AddL("    \"coset_side\": \"right (RightCosets, OnRight, as in cbeta_model_indep.g / u7_cbeta_marked_triple.g)\",");
AddL("    \"triple_relator_order\": \"ORDER-A: g0img*g1img*giimg = One (see cbeta_model_indep.g S9 note); this script uses ORDER-A only\",");
AddL("    \"chi_P_criterion\": \"exact only (m.triples / m.C0 / m.Cinf built from exact chi0/chiInf match); conjugacy_class variant not separately recomputed here -- see orbit_group field\",");
AddL("    \"comparison_target\": \"for each alpha, model triple set is tested against abstract window H_{2,alphaPrime,0} for EVERY alphaPrime in (Z/n)^x / {+-1} via TripleConjugate (full Sym(2n) simultaneous-conjugacy test, BFS canonical form)\",");
AddL("    \"alpha_reps\": \"smallest representative of each {alpha,-alpha mod n} pair, ascending scan order (same rule as m2_family_check.py RepsModPM)\"");
AddL("  },");
AddL("  \"comparison_target_doc\": \"docs/notes/m2_family_identification_v1.md theorem M2-GEO (Sec 6) and its Sec 9 spot-check table -- prediction (identity diagonal) is read AFTER this script's raw cross table is computed, not injected into the search\",");
AddL("  \"orbit_group_legend\": {");
AddL("    \"exact\": \"translation subgroup A <= Gamma_n, order n^2 -- theorem NIE(3): T(eta,delta) is a single simply-transitive A-orbit\",");
AddL("    \"class\": \"Gamma_n itself, order 4n^2 -- theorem NIE(4): T^cl is a single free Gamma_n-orbit (this script's m.orbits, computed by conjugating the exact triple set under the full model monodromy group Mperm = Gamma_n)\"");
AddL("  },");
AddL("  \"per_n\": {");

perNStrs := [];;
overallDiag := true;;

for n in ALLOWED_N do
    reps := RepsModPM(n);;
    units := UnitsModN(n);;

    # abstract side, one build per rep
    absRecs := [];;
    for ap in reps do
        Add(absRecs, [ap, BuildAbstract(n, ap)]);
    od;;

    # model side, one build per rep (r0=1, rinf=(-alpha) mod n, alphaLabel=alpha)
    modRecs := [];;
    for a in reps do
        Add(modRecs, [a, BuildModel(n, 1, (-a) mod n, a)]);
    od;;

    # cross table
    tbl := [];;
    for md in modRecs do
        a := md[1];; m := md[2];;
        row := [];;
        for pr in absRecs do
            ap := pr[1];; ab := pr[2];;
            matched := false;;
            for t in m.triples do
                if TripleConjugate(t[1], t[2], m.deg, ab.X, ab.Y, ab.deg) = true then
                    matched := true; break;
                fi;
            od;
            Add(row, matched);
        od;
        Add(tbl, row);
    od;;

    # identity diagonal check against reps-index identity (row i matches col i iff a=ap,
    # since reps are the SAME list on both axes)
    isIdentity := true;;
    for i in [1..Length(reps)] do
        for j in [1..Length(reps)] do
            if tbl[i][j] <> (i = j) then isIdentity := false; fi;
        od;
    od;;
    if not isIdentity then overallDiag := false; fi;;

    absStrs := [];;
    for pr in absRecs do
        ap := pr[1];; ab := pr[2];;
        Add(absStrs, Concatenation(
            "{\"alphaPrime\":", String(ap),
            ",\"G7order\":", String(ab.G7order),
            ",\"Horder\":", String(ab.Horder),
            ",\"Morder\":", String(ab.Morder),
            ",\"transitive\":", JBool(ab.transitive), "}"));
    od;;

    modStrs := [];;
    for md in modRecs do
        a := md[1];; m := md[2];;
        Add(modStrs, Concatenation(
            "{\"alpha\":", String(a),
            ",\"Mperm_order\":", String(Size(m.Mperm)),
            ",\"expected_4nsq\":", String(4*n*n),
            ",\"n_triples_exact\":", String(Length(m.triples)),
            ",\"expected_nsq\":", String(n*n),
            ",\"orbit_group_exact\":\"A(translations,order_nsq)\"",
            ",\"n_orbits_class\":", String(Length(m.orbits)),
            ",\"orbit_sizes_class\":", JIntList(List(m.orbits,Length)),
            ",\"orbit_group_class\":\"Gamma_n(order_4nsq)\"",
            "}"));
    od;;

    nStr := Concatenation(
        "    \"", String(n), "\": {",
        "\"units\":", JIntList(units), ",",
        "\"reps_mod_pm1\":", JIntList(reps), ",",
        "\"phi_n_over_2\":", String(Length(reps)), ",",
        "\"abstract_side\":[", JoinStringsWithSeparator(absStrs, ","), "],",
        "\"model_side\":[", JoinStringsWithSeparator(modStrs, ","), "],",
        "\"cross_table\":", JBoolMatrix(tbl), ",",
        "\"cross_table_rows_are_model_alpha\":", JIntList(reps), ",",
        "\"cross_table_cols_are_abstract_alphaPrime\":", JIntList(reps), ",",
        "\"identity_diagonal\":", JBool(isIdentity),
        "}");;
    Add(perNStrs, nStr);
    Print("n=", n, " reps=", reps, " identity_diagonal=", isIdentity, "\n");
od;;

AddL(JoinStringsWithSeparator(perNStrs, ",\n"));
AddL("  },");
AddL(Concatenation("  \"overall_identity_diagonal_all_n\": ", JBool(overallDiag), ","));
AddL("  \"machine_piped\": true,");
AddL("  \"note\": \"raw cross table computed first; M2-GEO identity-diagonal prediction from docs/notes/m2_family_identification_v1.md compared only in overall_identity_diagonal_all_n / per-n identity_diagonal fields, computed structurally (i=j check on the SAME reps list for both axes), not hand-copied from the note\"");
AddL("}");

outStr := JoinStringsWithSeparator(out, "\n");;
PrintTo("search/certs/m2_crosstable_gap_20260801.json", outStr);;
Print("\nWROTE search/certs/m2_crosstable_gap_20260801.json\n");
Print("overall_identity_diagonal_all_n = ", overallDiag, "\n");
Print("DONE\n");
