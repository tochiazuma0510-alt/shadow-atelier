#############################################################################
# search/r1_gap1_population72_census.g -- [R1-GAP-1] population-72 census cert
# (裁定1092・司令塔割り込み裁定1093)
#
# 目的: docs/notes/r1_declaration_draft_v1.md 【R1-GAP-1】の cert 化。
#   scratchpad/d2gap4_census2.g で得られていた「母集団72本・resolvent 4分割・
#   |Mon|分布」の producer 再計算(provenance 確立・candidate格)。
# 位置づけ: 裁定1093により、本 script は数学者の scratchpad script の方法節を
#   読んだ上での再実装(producer)であり、単独では cross-checked への格上げ
#   根拠にはならない。独立性の主張は crosscheck/check_r1_gap1_population72.py
#   側の申告欄を見よ。
#
# 数学的定義(r1_declaration_draft_v1.md 【R1-GAP-1】・d2gap4_gate_adjudication_v1.md
#   §3.1/§3.4 の定義部分に基づく):
#   母集団 = pi_1(E \ {Q0,Qinf,B1,B2,B3,B4}) 上の局所類 (3-cyc,3-cyc,transp,transp,
#     unram,unram) を持つ、次数3・S3-像 transitive な被覆全体(次数6の底
#     E->P^1_t の上に持ち上げた合成 monodromy(次数18)として実現)。
#   resolvent 不変量 = B1,B2 での局所置換の符号の組 (sgn(beta@B1),sgn(beta@B3))
#     不変量(2重被覆の分類。d2gap4_gate_adjudication_v1.md §3.4 の定義)。
#
# 入力(既認証 cert からの引用のみ・再測定しない):
#   qX,qY (次数6商 E->P^1_t) と target triple (sigma0,sigma1) は
#   search/certs/w9_k3_p1_0d_check_v1_20260812.json / d2_gate_v1_20260813.json /
#   scratchpad/lambda9_passport.g の出力値の引用(逐語)。
# 出力: cert (schema d2_census/v1)。生値のみ・判定語なし。
#############################################################################

Read("search/gaplib_common.g");;
SizeScreen([4096, 0]);;

S3 := SymmetricGroup(3);;
E3 := Elements(S3);;
THREE := Filtered(E3, g -> Order(g) = 3);;
TRANSP := Filtered(E3, g -> Order(g) = 2);;
Sgn := function(g) if Order(g) = 2 then return -1; else return 1; fi; end;;

# ---- degree-6 base data E -> P^1_t (measured; cf. w9_k3_p1_0d_check_v1 / lambda9_passport.g) ----
# qX = local monodromy at t=0 (single point Q0, e_E=6)  -> 6-cycle
# qY = local monodromy at t=1 (points B1={1},B2={6} e_E=1 ; B3={2,4},B4={3,5} e_E=2)
qX := [2,3,4,5,6,1];;          # i -> qX[i], i.e. (1,2,3,4,5,6)
qY := [1,4,5,2,3,6];;          # (2,4)(3,5), fixing 1 and 6

PT := function(i,j) return 3*(i-1) + j; end;;

# induce a degree-18 permutation from a degree-6 base permutation "q" (qX or qY)
# together with 6 local S3-elements alpha[1..6] attached to each block (=sheet
# of the degree-6 cover). This is the fiber-product / wreath-type construction
# for the degree-3 layer W -> E lying over the fixed degree-6 layer E -> P^1_t.
Induce := function(q, alpha)
  local l, i, j;
  l := [];
  for i in [1..6] do
    for j in [1..3] do
      l[PT(i,j)] := PT(q[i], j^alpha[i]);
    od;
  od;
  return PermList(l);
end;;

# ---- target triple lambda_9 (measured; verbatim from d2_gate_v1_20260813.json /
#      search/d2_gate_v1_group.g "lam9_sigma0/lam9_sigma1") ----
LX := (1,11,8,13,6,15,4,17,2,10,9,12,7,14,5,16,3,18);;
LY := (2,9)(3,8)(4,7)(5,6)(10,17)(11,16)(12,15)(13,14);;

# normalise a triple with sigma0 an 18-cycle to test S18-conjugacy (marked) against
# the target: relabel via sigma0's cycle so sigma0 -> (1,2,...,18), then two
# triples are conjugate (respecting sigma0) iff the resulting Y's differ by a
# power of the standard 18-cycle.
NormY := function(X, Y)
  local pts, p, k, rel, l, i;
  pts := [1]; p := 1;
  for k in [2..18] do p := p^X; pts[k] := p; od;
  rel := [];
  for k in [1..18] do rel[pts[k]] := k; od;
  l := [];
  for i in [1..18] do l[ rel[i] ] := rel[ i^Y ]; od;
  return PermList(l);
end;;
std := PermList(Concatenation([2..18],[1]));;
LN := NormY(LX, LY);;
LClass := Set(List([0..17], k -> LN^(std^k)));;

# ---- enumeration ----
# gauge: alpha_1..alpha_5 = id (spanning tree along qX's 6-cycle), alpha_6 free
#        (local monodromy at Q0 = single ramification point, forced 3-cycle).
# beta_1 (at B1), beta_6 (at B2) free transpositions (simple branch points).
# beta_2 at (block "2"), beta_3 at (block "3") free in S3 (unramified pair
#        B3={2,4}: beta_4 = beta_2^-1 forced by "no branching" at B3;
#        B4={3,5}: beta_5 = beta_3^-1 forced by "no branching" at B4).
rows := [];;
nTot := 0;;
for a6 in THREE do
 for b1 in TRANSP do
  for b6 in TRANSP do
   for b2 in E3 do
    for b3 in E3 do
      nTot := nTot + 1;
      alpha := [(),(),(),(),(),a6];
      beta  := [b1, b2, b3, b2^-1, b3^-1, b6];
      Xp := Induce(qX, alpha);;
      Yp := Induce(qY, beta);;
      Zp := (Xp*Yp)^-1;;
      if Order(Xp) = 18 and CycleStructurePerm(Yp) = [8] and Order(Zp) = 18 then
        GG9 := Group(Xp, Yp);;
        if IsTransitive(GG9, [1..18]) then
          Add(rows, rec( res := [Sgn(b2), Sgn(b3)],
                         siz := Size(GG9),
                         isL := (NormY(Xp,Yp) in LClass),
                         Xp := Xp, Yp := Yp ));
        fi;
      fi;
    od;
   od;
  od;
 od;
od;;

nConn := Length(rows);;
Print("[raw] total gauge assignments tested     = ", nTot, "\n");
Print("[raw] passport-passing & transitive       = ", nConn, "  (/6 gauge = ", nConn/6, " covers)\n");

resClasses := [[1,1],[1,-1],[-1,1],[-1,-1]];;
resSizes := List(resClasses, r -> Length(Filtered(rows, x -> x.res = r)) / 6);;
Print("[raw] resolvent class sizes (covers)      = ", resSizes, "\n");

monDistByClass := [];;
for r in resClasses do
  sub := Filtered(rows, x -> x.res = r);;
  Add(monDistByClass, Collected(List(sub, x -> x.siz)));;
od;;
Print("[raw] |Mon| distribution by class (assignment-count; /6 = covers): ", monDistByClass, "\n");

matched := Filtered(rows, x -> x.isL);;
Print("[raw] assignments matching lambda_9 target (S18-conj,marked) = ", Length(matched),
      "  (/6 = ", Length(matched)/6, " cover)\n");

matchClass := fail;; matchMon := fail;; matchBlocks := fail;; matchNontrivBlocks := fail;;
if Length(matched) > 0 then
  matchClass := matched[1].res;;
  matchMon := matched[1].siz;;
  Gm := Group(matched[1].Xp, matched[1].Yp);;
  blks := AllBlocks(Gm);;
  matchBlocks := Set(List(blks, b -> Length(b)));;
  matchNontrivBlocks := Length(blks);;
  Print("[raw] matched cover: resolvent class = ", matchClass, "  |Mon| = ", matchMon,
        "  block_sizes = ", matchBlocks, "  nontrivial_block_reps = ", matchNontrivBlocks, "\n");
fi;;

# ---- cross-references to already-certified values (read-only comparison, no re-measurement) ----
d2gate_P1_mon := 324;;   # search/certs/d2_gate_v1_20260813.json .P1.mon_order (逐語引用)
t18n140_block_sizes := Set([9,3]);;        # search/certs/r13_p1_0_blocks_v1_20260812.json .block_sizes (逐語引用・順序無視のためSet化)
t18n140_nontrivial_block_systems := 2;;    # 同cert .nontrivial_block_systems_count (逐語引用)

# ---- provenance ----
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_r1gap1.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/r1_gap1_population72_census.g");;
d2gateCertSha256 := ComputeSha256File("search/certs/d2_gate_v1_20260813.json");;
blocksCertSha256 := ComputeSha256File("search/certs/r13_p1_0_blocks_v1_20260812.json");;

# ---- JSON cert ----
ResSizesJson := JArr(List([1..4], k -> JPair(JArr(List(resClasses[k], String)), resSizes[k])));;

MonDistJson := function(coll)
  return JArr(List(coll, p -> JPair(p[1], p[2])));
end;;
MonDistByClassJson := JArr(List([1..4], k ->
  Concatenation("{\"res\":", JArr(List(resClasses[k], String)),
                ",\"assignment_dist\":", MonDistJson(monDistByClass[k]), "}")));;

MatchJson := "null";;
if Length(matched) > 0 then
  MatchJson := Concatenation(
    "{\"resolvent_class\":", JArr(List(matchClass, String)),
    ",\"mon_order\":", String(matchMon),
    ",\"block_sizes\":", JArr(List(matchBlocks, String)),
    ",\"nontrivial_block_systems_count\":", String(matchNontrivBlocks),
    "}");;
fi;;

cert := Concatenation(
  "{\"schema\":\"d2_census/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP ", GAPInfo.Version, "\"",
    ",\"script\":\"search/r1_gap1_population72_census.g\"",
    ",\"order\":\"\\u88c1\\u5b9a1092/1093 / docs/notes/r1_declaration_draft_v1.md \\u3010R1-GAP-1\\u3011\"",
    ",\"role\":\"producer (reproduces scratchpad/d2gap4_census2.g method; provenance/candidate only, not independent)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"base_data\":{\"qX\":\"", String(qX), "\",\"qY\":\"", String(qY),
    "\",\"reference\":\"w9_k3_p1_0d_check_v1_20260812.json / lambda9_passport.g\"}",
  ",\"target_reference\":{\"sigma0\":\"18-cycle (1,11,8,13,6,15,4,17,2,10,9,12,7,14,5,16,3,18)\"",
    ",\"sigma1\":\"(2,9)(3,8)(4,7)(5,6)(10,17)(11,16)(12,15)(13,14)\"}",
  ",\"raw_assignment_count\":", String(nTot),
  ",\"connected_assignment_count\":", String(nConn),
  ",\"gauge_orbit_size\":6",
  ",\"population_total_covers\":", String(nConn/6),
  ",\"resolvent_class_sizes_covers\":", ResSizesJson,
  ",\"mon_order_distribution_by_class\":", MonDistByClassJson,
  ",\"target_match\":", MatchJson,
  ",\"cross_check_positive_control\":{",
    "\"d2_gate_v1_W_P1_mon_order\":", String(d2gate_P1_mon),
    ",\"matched_cover_mon_order_equal\":", JB(matchMon = d2gate_P1_mon),
    ",\"t18n140_block_sizes_r13_p1_0_blocks_v1\":", JArr(List(t18n140_block_sizes, String)),
    ",\"matched_cover_block_sizes_equal\":", JB(matchBlocks = t18n140_block_sizes),
    ",\"t18n140_nontrivial_block_systems_count_r13_p1_0_blocks_v1\":", String(t18n140_nontrivial_block_systems),
    ",\"matched_cover_nontrivial_block_systems_count_equal\":", JB(matchNontrivBlocks = t18n140_nontrivial_block_systems),
  "}",
  ",\"u_touched\":false,\"c_touched\":false,\"prereg_quantities_computed\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict \\u306f\\u53f8\\u4ee4\\u5854\"",
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"",
    ",\"d2_gate_v1_cert_sha256\":\"", d2gateCertSha256, "\"",
    ",\"r13_p1_0_blocks_v1_cert_sha256\":\"", blocksCertSha256, "\"}",
  "}"
);;

outPath := "search/certs/r1_gap1_population72_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
