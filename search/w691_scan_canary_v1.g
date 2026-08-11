## search/w691_scan_canary_v1.g -- W691-SCAN canary (裁定823, docs/見立て_相2_v1_1.md §3
## rank-3 experiment "W691-SCAN"). Canary = GL(2,7) (falsifier's counterexample object, the
## p=7,d=6 member of the SAME family H={M in GL(2,p): det M in mu_d} targeted for p=691).
## For p=7, mu_6 = ALL of F_7^* (since |F_7^*|=6=d exactly), so H=GL(2,7) itself (order 2016) --
## matching falsifier's own finding (docs/見立て_相2_v1_1.md §1.4: "反例 GL(2,7)").
##
## *** SCOPE NOTE (disclosed, per commander's own explicit instruction) ***: this script covers
## ONLY the canary (GL(2,7), order 2016 -- small enough for full-element-pair enumeration,
## ~4M pairs, per the commander's own feasibility note). The actual p=691-scale targets
## (H_d, d in {2,3,6}, orders ~10^8-10^9) are NOT attempted here -- docs/見立て_相2_v1_1.md §3's
## own text ("各々...①(2,3)-生成(全元対)...") does not specify a method that scales to that
## size (full-pair enumeration at that order is computationally impossible: ~10^16-10^18 pairs),
## and per the commander's own explicit instruction ("方法が明記されていなければ推測せず
## STOP照会"), this is reported as an open gap requiring commander/mathematician guidance on a
## scalable method, rather than guessed at.
##
## Three checks performed on GL(2,7) (order 2016):
##  ① (2,3)-generation via ALL (order-2, order-3) element pairs (NOT conjugacy-class
##     representatives -- falsifier's own explicit warning, docs/見立て_相2_v1_1.md §1.4:
##     "(2,3)-生成の判定は全元対で行う。共役類代表対では偽陰性(8/8でFALSEの実走あり)").
##     Reports: does at least one such pair generate the full group; total count of
##     generating pairs found (raw, informational).
##  ② existence of an order-8 element with det=1 (the "non-split torus" element identified by
##     falsifier: order 8 | q^2-1=48 but 8 does not divide q-1=6, confirming non-split; det=1
##     since the norm of a primitive 8th-root-of-unity-in-F_49 down to F_7 is 1 for this
##     specific order/embedding -- checked directly, not assumed).
##  ③ B3-realization: existence of a braid-generating pair (a,b) with a*b*a=b*a*b AND
##     <a,b>=G, scanned over ALL pairs (same full-pair discipline as ①, same feasibility
##     bound ~4M pairs).
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

G := GL(2, 7);;
gOrder := Size(G);;
Print("|GL(2,7)| = ", gOrder, " (expect 2016)\n");

elts := Elements(G);;
Print("Elements enumerated: ", Length(elts), "\n");

## ---- check 1: (2,3)-generation, ALL pairs ----
ord2elts := Filtered(elts, x -> Order(x) = 2);;
ord3elts := Filtered(elts, x -> Order(x) = 3);;
Print("order-2 elements: ", Length(ord2elts), " order-3 elements: ", Length(ord3elts), "\n");

pairCount23 := 0;;
genCount23 := 0;;
firstGen23 := fail;;
for a in ord2elts do
  for b in ord3elts do
    pairCount23 := pairCount23 + 1;
    if Size(Subgroup(G, [a,b])) = gOrder then
      genCount23 := genCount23 + 1;
      if firstGen23 = fail then firstGen23 := [a,b]; fi;
    fi;
  od;
od;
Print("(2,3)-generation: pairs_checked=", pairCount23, " generating_pairs_found=", genCount23,
      " at_least_one_generates=", (genCount23 > 0), "\n");

## ---- check 2: order-8 element with det=1 ----
ord8DetEq1 := Filtered(elts, x -> Order(x) = 8 and Determinant(x) = One(GF(7)));;
Print("order-8 elements with det=1: ", Length(ord8DetEq1), " exists=", Length(ord8DetEq1) > 0, "\n");
sampleOrd8 := fail;;
if Length(ord8DetEq1) > 0 then sampleOrd8 := ord8DetEq1[1]; fi;

## ---- check 3: B3-realization (braid pair), ALL pairs ----
pairCountBraid := 0;;
genCountBraid := 0;;
firstGenBraid := fail;;
for a in elts do
  for b in elts do
    if a*b*a = b*a*b then
      pairCountBraid := pairCountBraid + 1;
      if Size(Subgroup(G, [a,b])) = gOrder then
        genCountBraid := genCountBraid + 1;
        if firstGenBraid = fail then firstGenBraid := [a,b]; fi;
      fi;
    fi;
  od;
od;
Print("braid pairs (a*b*a=b*a*b): total_found=", pairCountBraid,
      " generating_pairs_found=", genCountBraid, " at_least_one_generates=", (genCountBraid > 0), "\n");

## ============ JSON output ============
JMat := function(m)
  return Concatenation("[[", String(IntFFE(m[1][1])), ",", String(IntFFE(m[1][2])), "],[",
                        String(IntFFE(m[2][1])), ",", String(IntFFE(m[2][2])), "]]");
end;;

firstGen23Str := "null";;
if firstGen23 <> fail then
  firstGen23Str := Concatenation("[", JMat(firstGen23[1]), ",", JMat(firstGen23[2]), "]");
fi;
firstGenBraidStr := "null";;
if firstGenBraid <> fail then
  firstGenBraidStr := Concatenation("[", JMat(firstGenBraid[1]), ",", JMat(firstGenBraid[2]), "]");
fi;
sampleOrd8Str := "null";;
if sampleOrd8 <> fail then sampleOrd8Str := JMat(sampleOrd8); fi;

out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/w691_scan_canary_v1\",",
  "\"authority\":\"", "\\u88c1\\u5b9a823 -- docs/\\u898b\\u7acb\\u3066_\\u76f82_v1_1.md \\u00a73 (W691-SCAN, canary lane only)\",",
  "\"scope_note\":\"CANARY ONLY (GL(2,7), order 2016). The p=691-scale targets (H_d, d in {2,3,6}, order ~10^8-10^9) are NOT attempted -- no scalable full-pair method is specified in the source doc for that scale; reported as an open gap requiring guidance, per the commander's own explicit instruction not to guess.\",",
  "\"group\":\"GL(2,7)\",",
  "\"group_order\":", String(gOrder), ",",
  "\"group_order_expected\":2016,",
  "\"check1_23_generation\":{",
    "\"order2_element_count\":", String(Length(ord2elts)), ",",
    "\"order3_element_count\":", String(Length(ord3elts)), ",",
    "\"pairs_checked\":", String(pairCount23), ",",
    "\"generating_pairs_found\":", String(genCount23), ",",
    "\"at_least_one_generates\":", JB(genCount23 > 0), ",",
    "\"method\":\"ALL element pairs (not conjugacy-class representatives, per falsifier's explicit false-negative warning)\",",
    "\"sample_generating_pair\":", firstGen23Str,
  "},",
  "\"check2_order8_det1\":{",
    "\"order8_det1_element_count\":", String(Length(ord8DetEq1)), ",",
    "\"exists\":", JB(Length(ord8DetEq1) > 0), ",",
    "\"sample_element\":", sampleOrd8Str,
  "},",
  "\"check3_braid_realization\":{",
    "\"braid_pairs_total_found\":", String(pairCountBraid), ",",
    "\"generating_pairs_found\":", String(genCountBraid), ",",
    "\"at_least_one_generates\":", JB(genCountBraid > 0), ",",
    "\"method\":\"ALL element pairs (a,b) in G^2 with a*b*a=b*a*b, checked for full generation\",",
    "\"sample_generating_pair\":", firstGenBraidStr,
  "},",
  "\"no_verdict_note\":\"raw counts, sample witnesses, and booleans only. \\u5224\\u5b9a\\u8a9e\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044 -- \\u767a\\u52b9\\u306f\\u53f8\\u4ee4\\u5854\\u5c02\\u6a29\\u3002\"",
  "}"
);;

WriteFile("search/certs/w691_scan_canary_v1_20260812.json", out);;
Print("Wrote search/certs/w691_scan_canary_v1_20260812.json\n");
Print("W691_SCAN_CANARY_DONE\n");
QUIT;
