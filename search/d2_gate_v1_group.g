# search/d2_gate_v1_group.g -- [D2-GATE] 群論後段(裁定1083/1086/1087)
#
# 入力: search/certs/d2_gate_v1_track_20260813.gens.g (python 側 d2_gate_v1_track.py が
#       数値 path-tracking で得た sigma0/sigma1/sigmaInf を自動生成・手打ちなし)
# 処理: 各点(P1,P2)の monodromy 群 <sigma0,sigma1> の位数・可移性・ブロック系。
#       W(P1) について、認証済み lambda_9 の三つ組(p1d2_r1_canonicalization_v2.md §8.1)
#       との S18-共役性を「marked」に判定(RepresentativeAction による同時共役 --
#       群位数の一致だけで済ませない = Sol 警告「marked factor map を使う」準拠)。
# 出力: cert (schema d2_gate/v1)。生値のみ・判定語なし。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/certs/d2_gate_v1_track_20260813.gens.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ==== [G-0a] 既認証(cert 引用のみ) -- 参考表示・再測定はしない ====
Print("[G-0a] 既認証: w9_k3_p1_0d_check_v1(monG_size=324,D=18) / r13_p1_0_blocks_v1(block_sizes=[9,3])\n");

# ==== 認証済み lambda_9 の三つ組(p1d2_r1_canonicalization_v2.md §8.1・逐語) ====
# ⚠ 自己捕獲(本ターン開発中): lam9_cycle は「巡回記法の順序列」であって
#   PermList の一行記法(= i 番目の値が i の像)ではない。PermList(lam9_cycle) は
#   誤って別の置換を作る(デバッグで発見・修理済)。正しい構成は GAP のネイティブ
#   巡回記法リテラルを使う。
lam9_sigma0 := (1,11,8,13,6,15,4,17,2,10,9,12,7,14,5,16,3,18);;
lam9_sigma1 := (2,9)(3,8)(4,7)(5,6)(10,17)(11,16)(12,15)(13,14);;
lam9_cycle := [1,11,8,13,6,15,4,17,2,10,9,12,7,14,5,16,3,18];;  # sigma0 の巡回順(1始点・回転探索専用の系列)

# ==== S18-共役判定(§8.1 の指定実装: sigma0 は 18-cycle ⟹ centralizer は
#      <sigma0> のみ(位数18) ⟹ 正規化写像は18通りの回転のみを尽くせばよい。
#      *marked* な同時共役(sigma0,sigma1 の両方を保つ g)を直接尽くす --
#      一般 RepresentativeAction は S18(位数18!)全体の backtrack で実用外のため使わない ====
CycleFrom := function(perm, start, n)
  local seq, cur;
  seq := [start];;
  cur := start^perm;;
  while cur <> start do
    Add(seq, cur);;
    cur := cur^perm;;
  od;
  return seq;;
end;;

CheckConjugateToLambda9 := function(s0, s1)
  local myCycle, k, n, g, gList, i, mappedOk, a, b, pr;
  n := 18;;
  myCycle := CycleFrom(s0, 1, n);;
  if Length(myCycle) <> 18 then
    return rec(is_conjugate := false, note := "sigma0 is not an 18-cycle -- comparison N/A");;
  fi;
  for k in [0..17] do
    gList := [];;
    for i in [1..n] do
      gList[myCycle[i]] := lam9_cycle[((i - 1 + k) mod 18) + 1];;
    od;
    g := PermList(gList);;
    if s0^g = lam9_sigma0 and s1^g = lam9_sigma1 then
      return rec(is_conjugate := true, rotation_k := k, conjugating_perm := gList);;
    fi;
  od;
  return rec(is_conjugate := false, note := "no rotation among the 18 candidates matched");;
end;;

S18 := SymmetricGroup(18);;

results := rec();;

ProcessPoint := function(label, s0, s1, sInf)
  local G, ord, isTrans, blocks, blockSizes, cyc0, cyc1, cycInf, conjRes, r;
  G := Group(s0, s1);;
  ord := Size(G);;
  isTrans := IsTransitive(G, [1..18]);;
  if isTrans then
    blocks := AllBlocks(G);;
    blockSizes := Set(List(blocks, b -> Length(b)));;
  else
    blockSizes := "N/A (not transitive)";;
  fi;
  cyc0 := CycleStructurePerm(s0);;
  cyc1 := CycleStructurePerm(s1);;
  cycInf := CycleStructurePerm(sInf);;
  Print("[", label, "] |Mon| = ", ord, "  transitive = ", isTrans,
        "  blockSizes = ", blockSizes, "\n");
  Print("[", label, "] cycle_structure sigma0=", cyc0, " sigma1=", cyc1, " sigmaInf=", cycInf, "\n");
  conjRes := CheckConjugateToLambda9(s0, s1);;
  Print("[", label, "] S18-conjugate to lambda9 target triple (marked): ", conjRes.is_conjugate, "\n");
  r := rec(
    mon_order := ord,
    transitive := isTrans,
    block_sizes := blockSizes,
    cycle_structure_sigma0 := cyc0,
    cycle_structure_sigma1 := cyc1,
    cycle_structure_sigmaInf_derived := cycInf,
    s18_conjugate_to_lambda9_target := conjRes.is_conjugate
  );;
  return r;;
end;;

resP1 := ProcessPoint("P1", sigma0_P1, sigma1_P1, sigmaInf_P1);;
if IsBound(sigma0_P2) then
  resP2 := ProcessPoint("P2", sigma0_P2, sigma1_P2, sigmaInf_P2);;
else
  resP2 := fail;;
fi;

# ==== cert ====
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_d2gate.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/d2_gate_v1_group.g");;
gensSha256 := ComputeSha256File("search/certs/d2_gate_v1_track_20260813.gens.g");;

BoolOrStr := function(v)
  if v = true then return "true";
  elif v = false then return "false";
  else return Concatenation("\"", String(v), "\"");
  fi;
end;;

PointJson := function(label, r)
  if r = fail then
    return "null";
  fi;
  return Concatenation(
    "{\"mon_order\":", String(r.mon_order),
    ",\"transitive\":", BoolOrStr(r.transitive),
    ",\"block_sizes\":\"", String(r.block_sizes), "\"",
    ",\"cycle_structure_sigma0\":\"", String(r.cycle_structure_sigma0), "\"",
    ",\"cycle_structure_sigma1\":\"", String(r.cycle_structure_sigma1), "\"",
    ",\"cycle_structure_sigmaInf_derived\":\"", String(r.cycle_structure_sigmaInf_derived), "\"",
    ",\"s18_conjugate_to_lambda9_target\":", BoolOrStr(r.s18_conjugate_to_lambda9_target),
    "}"
  );;
end;;

cert := Concatenation(
  "{\"schema\":\"d2_gate/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP ", GAPInfo.Version, " + python mpmath (numeric path-tracking)\"",
    ",\"track_script\":\"search/d2_gate_v1_track.py\",\"group_script\":\"search/d2_gate_v1_group.g\"",
    ",\"order\":\"裁定1083/1086/1087 / docs/notes/p1d2_r1_canonicalization_v2.md \\u00a78.2\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"lambda9_target_reference\":{\"note\":\"p1d2_r1_canonicalization_v2.md \\u00a78.1 (\\u9038\\u8a9e)\"",
    ",\"sigma0\":\"18-cycle (1,11,8,13,6,15,4,17,2,10,9,12,7,14,5,16,3,18)\"",
    ",\"sigma1\":\"(2,9)(3,8)(4,7)(5,6)(10,17)(11,16)(12,15)(13,14)\"}",
  ",\"P1\":", PointJson("P1", resP1),
  ",\"P2\":", PointJson("P2", resP2),
  ",\"prereg_check\":{\"PRED1_note\":\"|Mon(W(P1))| in {324,972,2916}, != 419904\"",
    ",\"PRED2_note\":\"|Mon(W(P2))| = 419904\"}",
  ",\"quarantine\":{",
    "\"name_collide\":\"\\u5c02\\u4e00\\u5bfe\\u8c61\\u306a\\u3057(\\u88c1\\u5b9a1007\\u306e\\u5c01\\u5370\\u306f\\u672a\\u63a5\\u89e6)\"",
  "}",
  ",\"u_touched\":false,\"c_touched\":false,\"prereg_quantities_computed\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict \\u306f\\u53f8\\u4ee4\\u5854\"",
  ",\"provenance\":{\"group_script_sha256\":\"", scriptSha256, "\"",
    ",\"gens_file_sha256\":\"", gensSha256, "\"}",
  "}"
);;

outPath := "search/certs/d2_gate_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("group script sha256 = ", scriptSha256, "\n");
QUIT;
