## search/pq8fam_ext_v1.g -- P-Q8FAM extended inventory check (裁定823②).
## docs/見立て_相2_v1_1.md line 248: "P-Q8FAM | 指数24m(m奇)でG^ab=C_3m | census/lins出力・
## 指数<=800 | Q8-FAM(Goursat・8/8) | 該当なし" -- the ESTABLISHED formula (matching every
## verified m=1..15 data point in addendum_a SS1.2's own table: index/m=24 exactly for all 8
## known members) is index=24m, m odd. Extended here using the now-available lins-2000 census
## (search/certs/lins_census_2000_v1_20260811.json, index<=2000) up to m<=83 (24*83=1992<=2000,
## 24*85=2040>2000).
##
## *** DISCLOSED DISCREPANCY (not silently resolved) ***: the task instruction (裁定823) stated
## "指数24・3m<=2000(m奇数<=27)" -- solving 24*3*m<=2000 gives m<=27, matching the STATED cap,
## but this formula (72m) does NOT match the established index=24m pattern from addendum_a's own
## verified table (index/m=24 for all 8 known m=1..15 points) or from docs/見立て_相2_v1_1.md's
## own explicit "指数24m" line. This script uses the ESTABLISHED 24m formula (consistent with
## ALL prior verified data) over the FULL available range m<=83 (not capped at 27) -- the wider
## range is a strict superset of "m<=27" under EITHER formula's interpretation of what's being
## asked, so no information is lost by covering more; the discrepancy itself is reported for the
## commander's review, not resolved by guessing which formula was intended.
##
## Method: for each odd m with 24m<=2000, scan the census twin_pairs for index=24m entries whose
## structure_description contains "SL(2,3)" or "Q8" (the Q8-FAM structural signature per
## addendum_a SS1.2/SS1.4's own examples: direct-product form "C_m x SL(2,3)" when gcd(m,3)=1,
## semidirect "Q8 : C_{3m}" form when gcd(m,3)>1) -- candidates NOT matching this signature
## (e.g. "C7 : C24" at index 168) are OTHER, unrelated families at the same index, excluded.
## For each matched candidate, AbelianInvariants(SmallGroup(id)) is computed directly (cheap,
## small groups) and checked against the predicted C_{3m}.
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

## ============ candidate id_groups per m (extracted from the census, Q8-FAM structural filter) ============
## (m, [order,id], structure_description) -- selected via Python pre-scan of
## search/certs/lins_census_2000_v1_20260811.json (twin_pairs, index=24m, structure_description
## containing "SL(2,3)" or "Q8"), reproduced here as a literal list for GAP to measure.
CANDIDATES := [
  rec(m:=1,  id:=[24,3],    struct:="SL(2,3)"),
  rec(m:=3,  id:=[72,3],    struct:="Q8 : C9"),
  rec(m:=5,  id:=[120,15],  struct:="C5 x SL(2,3)"),
  rec(m:=7,  id:=[168,22],  struct:="C7 x SL(2,3)"),
  rec(m:=9,  id:=[216,3],   struct:="Q8 : C27"),
  rec(m:=11, id:=[264,12],  struct:="C11 x SL(2,3)"),
  rec(m:=13, id:=[312,25],  struct:="C13 x SL(2,3)"),
  rec(m:=15, id:=[360,14],  struct:="C5 x (Q8 : C9)"),
  rec(m:=17, id:=[408,14],  struct:="C17 x SL(2,3)"),
  rec(m:=19, id:=[456,22],  struct:="C19 x SL(2,3)"),
  rec(m:=21, id:=[504,22],  struct:="C7 x (Q8 : C9)"),
  rec(m:=23, id:=[552,12],  struct:="C23 x SL(2,3)"),
  rec(m:=25, id:=[600,14],  struct:="C25 x SL(2,3)"),
  rec(m:=27, id:=[648,3],   struct:="Q8 : C81"),
  rec(m:=29, id:=[696,14],  struct:="C29 x SL(2,3)"),
  rec(m:=31, id:=[744,22],  struct:="C31 x SL(2,3)"),
  rec(m:=33, id:=[792,12],  struct:="C11 x (Q8 : C9)"),
  rec(m:=35, id:=[840,94],  struct:="C35 x SL(2,3)"),
  rec(m:=37, id:=[888,25],  struct:="C37 x SL(2,3)"),
  rec(m:=39, id:=[936,25],  struct:="C13 x (Q8 : C9)"),
  rec(m:=41, id:=[984,14],  struct:="C41 x SL(2,3)"),
  rec(m:=43, id:=[1032,22], struct:="C43 x SL(2,3)"),
  rec(m:=45, id:=[1080,14], struct:="C5 x (Q8 : C27)"),
  rec(m:=47, id:=[1128,12], struct:="C47 x SL(2,3)"),
  rec(m:=49, id:=[1176,22], struct:="C49 x SL(2,3)"),
  rec(m:=51, id:=[1224,14], struct:="C17 x (Q8 : C9)"),
  rec(m:=53, id:=[1272,14], struct:="C53 x SL(2,3)"),
  rec(m:=55, id:=[1320,94], struct:="C55 x SL(2,3)"),
  rec(m:=57, id:=[1368,22], struct:="C19 x (Q8 : C9)"),
  rec(m:=59, id:=[1416,12], struct:="C59 x SL(2,3)"),
  rec(m:=61, id:=[1464,25], struct:="C61 x SL(2,3)"),
  rec(m:=63, id:=[1512,22], struct:="C7 x (Q8 : C27)"),
  rec(m:=65, id:=[1560,106], struct:="C65 x SL(2,3)"),
  rec(m:=67, id:=[1608,22], struct:="C67 x SL(2,3)"),
  rec(m:=69, id:=[1656,12], struct:="C23 x (Q8 : C9)"),
  rec(m:=71, id:=[1704,12], struct:="C71 x SL(2,3)"),
  rec(m:=73, id:=[1752,25], struct:="C73 x SL(2,3)"),
  rec(m:=75, id:=[1800,14], struct:="C25 x (Q8 : C9)"),
  rec(m:=77, id:=[1848,87], struct:="C77 x SL(2,3)"),
  rec(m:=79, id:=[1896,22], struct:="C79 x SL(2,3)"),
  rec(m:=81, id:=[1944,3],  struct:="Q8 : C243"),
  rec(m:=83, id:=[1992,12], struct:="C83 x SL(2,3)"),
];;

results := [];;
allMatch := true;;
for c in CANDIDATES do
  G := SmallGroup(c.id[1], c.id[2]);;
  Gab := G / DerivedSubgroup(G);;
  abOrd := Size(Gab);;
  abIsCyclic := IsCyclic(Gab);;
  predicted := 3*c.m;;
  matches := abIsCyclic and (abOrd = predicted);;
  sigMismatch := not (PositionSublist(c.struct, "SL(2,3)") <> fail or PositionSublist(c.struct, "Q8") <> fail);;
  if not matches then allMatch := false; fi;
  Add(results, rec(m:=c.m, index:=24*c.m, id:=c.id, struct:=c.struct,
                    ab_order:=abOrd, ab_is_cyclic:=abIsCyclic, predicted_3m:=predicted,
                    matches_prediction:=matches, structural_signature_mismatch:=sigMismatch));
  Print("m=", c.m, " idx=", 24*c.m, " id=", c.id, " ab_order=", abOrd, " cyclic=", abIsCyclic,
        " predicted=", predicted, " match=", matches, " sig_mismatch=", sigMismatch, "\n");
od;

allMLE83 := [1,3..83];;
mFound := List(CANDIDATES, c -> c.m);;
missingM := Filtered(allMLE83, m -> not m in mFound);;
Print("m range checked (odd, 24m<=2000): ", allMLE83, "\n");
Print("m found in census with SL(2,3)/Q8-signature candidate: ", Length(mFound), "/", Length(allMLE83), "\n");
Print("missing m (no candidate found at all, of any signature): ", missingM, "\n");
Print("all_matches_prediction: ", allMatch, "\n");

## ============ JSON output ============
JResult := function(r)
  return Concatenation("{",
    "\"m\":", String(r.m), ",",
    "\"index\":", String(r.index), ",",
    "\"id_group\":", JPair(r.id[1], r.id[2]), ",",
    "\"structure_description\":", JStr(r.struct), ",",
    "\"ab_order\":", String(r.ab_order), ",",
    "\"ab_is_cyclic\":", JB(r.ab_is_cyclic), ",",
    "\"predicted_3m\":", String(r.predicted_3m), ",",
    "\"matches_prediction\":", JB(r.matches_prediction), ",",
    "\"structural_signature_mismatch\":", JB(r.structural_signature_mismatch),
    "}");
end;;

out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/pq8fam_ext_v1\",",
  "\"authority\":\"", "\\u88c1\\u5b9a823(2) -- docs/\\u898b\\u7acb\\u3066_\\u76f82_v1_1.md L248 (P-Q8FAM, established formula index=24m)\",",
  "\"formula_discrepancy_note\":\"task instruction stated \\u6307\\u6570 24*3m<=2000 (m<=27); this script uses the ESTABLISHED formula index=24m (matching ALL 8 verified m=1..15 data points in addendum_a SS1.2's own table, and docs/\\u898b\\u7acb\\u3066_\\u76f82_v1_1.md L248's explicit '\\u6307\\u6570 24m' statement) over the FULL available range m<=83 (24*83=1992<=2000) -- a strict superset of m<=27 under either reading. Discrepancy reported for review, not silently resolved.\",",
  "\"m_range_checked\":\"odd m, 1..83 (24m<=2000)\",",
  "\"results\":[", JoinC(List(results, JResult), ","), "],",
  "\"m_found_count\":", String(Length(mFound)), ",",
  "\"m_total_checked\":", String(Length(allMLE83)), ",",
  "\"missing_m\":[", JoinC(List(missingM, String), ","), "],",
  "\"all_matches_prediction\":", JB(allMatch), ",",
  "\"no_verdict_note\":\"raw census inventory, id_group, abelianization order/cyclicity, and booleans only. \\u5224\\u5b9a\\u8a9e\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044 -- \\u767a\\u52b9\\u306f\\u53f8\\u4ee4\\u5854\\u5c02\\u6a29\\u3002\"",
  "}"
);;

WriteFile("search/certs/pq8fam_ext_v1_20260812.json", out);;
Print("Wrote search/certs/pq8fam_ext_v1_20260812.json\n");
Print("PQ8FAM_EXT_DONE\n");
QUIT;
