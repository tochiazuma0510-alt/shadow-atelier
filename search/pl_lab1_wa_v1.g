## search/pl_lab1_wa_v1.g -- PL-LAB-1 段 W-a のみ(裁定774/776/779).
## Constructs P_{c,p} := F_2/(gamma_{c+1}(F_2) F_2^p) via ANUPQ for all 5
## targets (2 controls + 2 main + 1 further-post-Lazard), verifies order,
## exponent, and LCS-layer dimensions against the naive free-Lie Witt(2,k)
## prediction.
##
## *** SCOPE (裁定779 explicit hold) ***
## This script performs ONLY W-a (pc-group construction + structural
## canaries: order, exponent, LCS dims vs Witt numbers). It does NOT
## compute hexagon solution-space dimensions, does NOT compute def(c,p),
## and does NOT compare against "dim S_k" -- that comparison target has an
## unresolved design-side ambiguity (裁定779: PL-LAB-1's cited "dim
## S_k(k=1..8)=0,0,1,0,1,0,1,1" sequence, per its only found definition in
## docs/notes/b_type_synthesis_design_v1.md line 237, requires a THIRD
## condition "ker nu_k" tied to an unrelated auxiliary structure (a
## K(0,5)/pentagon-5-cycle object) that P_{c,p}'s pure hexagon (B_3-only)
## window does not possess -- confirmed by 裁定779 as a design-side
## omission, referred back to the design author; the correct comparison
## target (either an "H_k"-style hexagon-only ladder, or a rebuilt "S_k"
## restricted to this window) is pending a design addendum.
##
## *** FINDING (structural, W-a-only, not gated by the above) ***
## The measured LCS layer dimensions match the free-Lie Witt(2,k)
## prediction EXACTLY for all k < p in every target (both Lazard-domain
## controls (5,4)/(7,6) match at every degree; the two class=p main
## targets (5,5)/(7,7) also match at every degree k<p) -- and the first
## (and, where checked, only) deviation occurs EXACTLY at degree k=p in
## both (5,5) [k=5: measured 2 vs Witt 6] and (7,7) [k=7: measured 12 vs
## Witt 18]. This is the expected Hall-Petrescu / Lazard-breakdown
## signature (addendum's own §2.4 event table: "p の p 冪写像が交換子か
## ら独立な情報を gamma_p に落とす"), not a canary failure -- recorded
## here as a raw structural fact, no verdict language.
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

WITT := [2,1,2,3,6,9,18,30];;  # Witt(2,k), k=1..8 (free Lie, 2 generators; frozen per design doc §2.2)

TARGETS := [
  rec(label:="p5c4_control", p:=5, c:=4, path:="search/probe/pl_lab1_v1/PQ_OUTPUT_p5c4.g", role:="W-f control (Lazard domain, c<p)", kind:="control"),
  rec(label:="p5c5_main",    p:=5, c:=5, path:="search/probe/pl_lab1_v1/PQ_OUTPUT_p5c5.g", role:="main target (c=p)", kind:="main"),
  rec(label:="p5c6_extra",   p:=5, c:=6, path:="search/probe/pl_lab1_v1/PQ_OUTPUT_p5c6.g", role:="further post-Lazard (c>p)", kind:="extra"),
  rec(label:="p7c6_control", p:=7, c:=6, path:="search/probe/pl_lab1_v1/PQ_OUTPUT_p7c6.g", role:="W-f control (Lazard domain, c<p)", kind:="control"),
  rec(label:="p7c7_main",    p:=7, c:=7, path:="search/probe/pl_lab1_v1/PQ_OUTPUT_p7c7.g", role:="main target (c=p)", kind:="main"),
];;

results := [];;
for t in TARGETS do
  Read(t.path);
  P := F;;  xG := MapImages[1];;  yG := MapImages[2];;
  Unbind(F);;  Unbind(MapImages);;

  order := Size(P);;
  wittPredict := t.p ^ Sum(WITT{[1..t.c]});;
  expOk := (xG^t.p = Identity(P)) and (yG^t.p = Identity(P));;

  lcs := LowerCentralSeriesOfGroup(P);;
  lcsDims := List([1..Length(lcs)-1], i -> LogInt(Size(lcs[i])/Size(lcs[i+1]), t.p));;
  wittList := WITT{[1..t.c]};;
  perDegreeMatch := List([1..Length(lcsDims)], i -> lcsDims[i] = wittList[i]);;
  gammaTrivial := Size(lcs[Length(lcs)]) = 1;;
  firstMismatchDeg := 0;;
  for i in [1..Length(perDegreeMatch)] do
    if not perDegreeMatch[i] then firstMismatchDeg := i; break; fi;
  od;

  Add(results, rec(
    label:=t.label, p:=t.p, c:=t.c, role:=t.role, kind:=t.kind,
    order:=order, witt_predicted_order:=wittPredict, order_matches_witt_predict:=(order=wittPredict),
    exponent_ok:=expOk,
    lcs_dims:=lcsDims, witt_list:=wittList, per_degree_match:=perDegreeMatch,
    all_degrees_match:=ForAll(perDegreeMatch, x->x),
    first_mismatch_degree:=firstMismatchDeg,  # 0 = no mismatch found
    gamma_c_plus_1_trivial:=gammaTrivial
  ));
  Print(t.label, ": order=", order, " exp_ok=", expOk, " lcs_dims=", lcsDims,
        " all_match=", ForAll(perDegreeMatch, x->x), " first_mismatch_deg=", firstMismatchDeg, "\n");
od;

## ---- JSON output ----
JRec := function(r)
  local parts;
  parts := [
    Concatenation("\"label\":", JStr(r.label)),
    Concatenation("\"p\":", String(r.p)),
    Concatenation("\"c\":", String(r.c)),
    Concatenation("\"role\":", JStr(r.role)),
    Concatenation("\"kind\":", JStr(r.kind)),
    Concatenation("\"order\":", String(r.order)),
    Concatenation("\"witt_predicted_order\":", String(r.witt_predicted_order)),
    Concatenation("\"order_matches_witt_predict\":", JB(r.order_matches_witt_predict)),
    Concatenation("\"exponent_ok\":", JB(r.exponent_ok)),
    Concatenation("\"lcs_dims\":", JArr(List(r.lcs_dims, String))),
    Concatenation("\"witt_list\":", JArr(List(r.witt_list, String))),
    Concatenation("\"per_degree_match\":", JArr(List(r.per_degree_match, JB))),
    Concatenation("\"all_degrees_match\":", JB(r.all_degrees_match)),
    Concatenation("\"first_mismatch_degree\":", String(r.first_mismatch_degree)),
    Concatenation("\"gamma_c_plus_1_trivial\":", JB(r.gamma_c_plus_1_trivial))
  ];
  return Concatenation("{", JoinC(parts, ","), "}");
end;;

# structural sanity (must ALWAYS hold, regardless of Lazard breakdown):
# exponent really is p, and gamma_{c+1} really is trivial (construction integrity).
# Deliberately EXCLUDES order_matches_witt_predict, which is expected to be
# false for kind=main/extra targets (that IS the Lazard-breakdown finding,
# not a failure) -- conflating the two would mislabel an expected result as
# a canary failure.
structuralSanityOk := ForAll(results, r -> r.exponent_ok and r.gamma_c_plus_1_trivial);;
controlsAllMatch := ForAll(Filtered(results, r -> r.kind="control"), r -> r.all_degrees_match and r.order_matches_witt_predict);;
mainTargetsFirstMismatchAtP := ForAll(Filtered(results, r -> r.kind="main"), r -> r.first_mismatch_degree = r.p);;

out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/pl_lab1_wa_v1\",",
  "\"authority\":\"", "\\u88c1\\u5b9a774/776/779 (\\u53f8\\u4ee4\\u5854), docs/notes/post_lazard_window_design_v1.md \\u767a\\u6ce8\\u4ed5\\u69d8 PL-LAB-1 \\u6bb5W-a\\u306e\\u307f (\\u6bb5W-c\\u4ee5\\u964d\\u306f\\u8a2d\\u8a08\\u8ffd\\u88dc\\u7740\\u5f3e\\u307e\\u3067\\u4fdd\\u7559)\",",
  "\"scope_hold_note\":\"W-c\\u4ee5\\u964d(hexagon\\u89e3\\u7a7a\\u9593\\u30fbdef(c,p)\\u30fbdim S_k\\u6bd4\\u8f03)\\u306f\\u672a\\u5b9f\\u65bd\\u3002\\u6bd4\\u8f03\\u5bfe\\u8c61\\u306e\\u5b9a\\u7fa9\\u306b\\u8a2d\\u8a08\\u5074\\u306e\\u66d6\\u6627\\u3055\\u304c\\u3042\\u308a(\\u88c1\\u5b9a779\\u3067\\u78ba\\u8a8d\\u6e08\\u30fb\\u8a2d\\u8a08\\u8ffd\\u88dc\\u306e\\u7740\\u5f3e\\u5f85\\u3061)\\u3002\",",
  "\"witt_2_k_reference\":", JArr(List(WITT, String)), ",",
  "\"targets\":[", JoinC(List(results, JRec), ","), "],",
  "\"structural_sanity_all_pass\":", JB(structuralSanityOk), ",",
  "\"controls_all_degrees_match_witt\":", JB(controlsAllMatch), ",",
  "\"main_targets_first_mismatch_exactly_at_degree_p\":", JB(mainTargetsFirstMismatchAtP), ",",
  "\"finding_note\":\"LCS\\u5c64\\u6b21\\u5143\\u306fk<p\\u306e\\u5168\\u6bb5\\u3067Witt(2,k)\\u3068\\u5b8c\\u5168\\u4e00\\u81f4(\\u30b3\\u30f3\\u30c8\\u30ed\\u30fc\\u30eb2\\u4ef6\\u30fb\\u4e3b\\u6a19\\u76842\\u4ef6\\u3068\\u3082)\\u3002\\u521d\\u3081\\u3066\\u306e\\u4e0d\\u4e00\\u81f4\\u306f\\u4e3b\\u6a19\\u7684\\u306e\\u4e21\\u65b9\\u3067\\u3061\\u3087\\u3046\\u3069k=p\\u3067\\u767a\\u751f((5,5)\\u306fk=5\\u3067\\u6e2c\\u5b9a2 vs Witt6\\u3001(7,7)\\u306fk=7\\u3067\\u6e2c\\u5b9a12 vs Witt18)\\u3002\\u9084\\u5b9a\\u7684\\u3067\\u8a2d\\u8a08\\u306e\\u4e88\\u60f3\\u3068\\u6574\\u5408(Hall-Petrescu\\u306e\\u6f0f\\u308c)\\u3002\\u5224\\u5b9a\\u8a9e\\u306a\\u3057\\u3002\",",
  "\"no_verdict_note\":\"S-PL-4 compliance: raw structural values (order, exponent, LCS dims) and booleans only. dim S_k comparison / def(c,p) deferred per 裁定779.\",",
  "\"stop_code\":null",
  "}"
);;

WriteFile("search/certs/pl_lab1_wa_v1_20260811.json", out);;
Print("Wrote search/certs/pl_lab1_wa_v1_20260811.json\n");
Print("PL_LAB1_WA_DONE\n");
QUIT;
