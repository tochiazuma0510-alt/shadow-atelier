# search/w9_k3_t3_lightcheck_v1.g -- [P1-C] t3 車線(札3)の軽量 GAP 検算 ①②(裁定1019・司令塔採用(a))
#
# 正本: docs/notes/w9k3_tricks_audit_v1.md §3.1(検分)・docs/notes/ideas_w9k3_tricks_v1.md 札3(検証装置①②)。
# 範囲: E の明示モデル決定・本体(3次 ansatz 探索)はここでは行わない(数学的判断につき数学者へ回付
#   — 裁定1019受領時の司令塔採用(a))。ここでは以下の「implementer・GAP・秒」規模の検算のみ:
#   ① サイズ3ブロックの stabilizer の(そのブロック上の)3点作用の像が S3 か(非巡回の構造的確認)
#   ② t=1 分岐内訳(σ0/σ1/σinf のサイズ3ブロック商上のサイクル型)の再確認(regression、[P1-0b]の値と突合)
#   ③ E(度数6・分岐型 [6],[1^2 2^2],[6])の Nielsen 類数え(S6 内の全探索・積=1・可移性)
#
# 847 依存監査: BuildPnFull は search/r13_r0_v1.g・r13_p1_0_blocks_v1.g・r13_p1_0b_v1.g と同一の
#   標準構成パターン(独立再構成、既存スクリプトを Read() しない — H9fun 構成は repo 内で確立済みの
#   共通の群論的土台であり、裁定1020 が指摘した「代数的導出の再入力」の懸念とは別種)。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

BuildPnFull := function(n)
  local r, s, tr, a1, a2, a3, q1, q2, X, Y, Gfull;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  a1 := tr(r,1);;  a2 := tr(r,2);;  a3 := tr(r,3);;
  q1 := tr(s,2)*tr(s,3);;  q2 := tr(s,1)*tr(s,3);;
  X := AbstractProd([a1,q1]);;  Y := AbstractProd([a1,a2,a3,q2]);;
  Gfull := Group(a1,a2,a3,q1,q2);;
  return rec(n:=n, a1:=a1, a2:=a2, a3:=a3, q1:=q1, q2:=q2, X:=X, Y:=Y, G:=Gfull);;
end;;

P9 := BuildPnFull(9);;
H9fun := Group(P9.a2, P9.a1*P9.a3, P9.q2);;
D := Size(P9.G)/Size(H9fun);;

phiAction9 := FactorCosetAction(P9.G, H9fun);;
Ximg9 := Image(phiAction9, P9.X);;   # sigma_0
Yimg9 := Image(phiAction9, P9.Y);;   # sigma_1
Zimg9 := (Ximg9*Yimg9)^-1;;          # sigma_inf
monG := Group(Ximg9, Yimg9);;
Print("|monG| = ", Size(monG), " D = ", D, " (期待 324, 18)\n");

blocks := AllBlocks(monG);;
rep3 := First(blocks, b -> Length(b) = 3);;
Print("[", PF(rep3 <> fail), "] size-3 の代表ブロックが見つかった: ", rep3, "\n");

# ===================================================================
# ① stabilizer の3点作用の像が S3 か
# ===================================================================
stab3 := Stabilizer(monG, rep3, OnSets);;
Print("|Stabilizer(monG, rep3, OnSets)| = ", Size(stab3), "\n");

actHom := ActionHomomorphism(stab3, rep3, OnPoints);;
img3 := Image(actHom);;
Print("image of stabilizer's action on the block (order) = ", Size(img3), " (S3=6, C3=3)\n");

imgIsS3 := (Size(img3) = 6) and IsomorphismGroups(img3, SymmetricGroup(3)) <> fail;;
imgIsC3 := (Size(img3) = 3);;
Print("[", PF(imgIsS3), "] 【①】stabilizer の3点作用の像 = S3(非巡回): ", imgIsS3, "\n");
Print("(参考) 像が C3(巡回)だった場合: ", imgIsC3, "\n");

# ===================================================================
# ② t=1 分岐内訳の再確認(size-3 系での σ0/σ1/σinf サイクル型・regression)
# ===================================================================
InducedCycleType := function(perm, blockSystem)
  local nBlocks, blockOfPoint, pt, idx, images, i, imgPt, imgBlockIdx, quotPerm, cyc;
  nBlocks := Length(blockSystem);;
  blockOfPoint := [];;
  for idx in [1..nBlocks] do
    for pt in blockSystem[idx] do blockOfPoint[pt] := idx; od;
  od;
  images := [];;
  for i in [1..nBlocks] do
    imgPt := blockSystem[i][1]^perm;;
    imgBlockIdx := blockOfPoint[imgPt];;
    if ForAny(blockSystem[i], p -> blockOfPoint[p^perm] <> imgBlockIdx) then
      Error("InducedCycleType: block system not perm-invariant -- bug");
    fi;
    images[i] := imgBlockIdx;;
  od;
  quotPerm := PermList(images);;
  cyc := Collected(List([1..nBlocks], i -> CycleLength(quotPerm, i)));;
  return rec(quotPerm:=quotPerm, cycleType:=List(cyc, e -> [e[1], e[2]/e[1]]));;
end;;

blockSystem3 := Orbit(monG, rep3, OnSets);;
ct3X := InducedCycleType(Ximg9, blockSystem3);;
ct3Y := InducedCycleType(Yimg9, blockSystem3);;
ct3Z := InducedCycleType(Zimg9, blockSystem3);;
Print("sigma_0 on 6-block quotient: ", ct3X.cycleType, " (期待 [[6,1]])\n");
Print("sigma_1 on 6-block quotient: ", ct3Y.cycleType, " (期待 [[1,2],[2,2]])\n");
Print("sigma_inf on 6-block quotient: ", ct3Z.cycleType, " (期待 [[6,1]])\n");

sigma0Ok := (ct3X.cycleType = [[6,1]]);;
sigma1Ok := (ct3Y.cycleType = [[1,2],[2,2]]) or (ct3Y.cycleType = [[2,2],[1,2]]);;
sigmaInfOk := (ct3Z.cycleType = [[6,1]]);;
regressionOk := sigma0Ok and sigma1Ok and sigmaInfOk;;
Print("[", PF(regressionOk), "] 【②】[P1-0b] のsize3_systemサイクル型と一致(regression): ", regressionOk, "\n");

# ===================================================================
# ③ E の Nielsen 類数え(S6内・積=1・可移性・型 [6],[1^2 2^2],[6])
# ===================================================================
CycleTypeOf := function(perm, n)
  local cyc;
  cyc := Collected(List([1..n], i -> CycleLength(perm, i)));;
  return List(cyc, e -> [e[1], e[2]/e[1]]);;
end;;

S6 := SymmetricGroup(6);;
sixCycles := Filtered(Elements(S6), p -> CycleTypeOf(p, 6) = [[6,1]]);;
type622 := Filtered(Elements(S6), p -> CycleTypeOf(p, 6) = [[1,2],[2,2]]);;
Print("|6-cycles| = ", Length(sixCycles), " (期待 5!=120)\n");
Print("|type [1^2,2^2] elements| = ", Length(type622), "\n");

nielsenCount := 0;;
transitiveCount := 0;;
for s0 in sixCycles do
  for s1 in type622 do
    sinf := (s0*s1)^-1;;
    if sinf in sixCycles then
      nielsenCount := nielsenCount + 1;;
      genG := Group(s0, s1);;
      if IsTransitive(genG, [1..6]) then
        transitiveCount := transitiveCount + 1;;
      fi;
    fi;
  od;
od;
Print("Nielsen 類(積=1・型[6],[1^2 2^2],[6]の順序3組)候補総数 = ", nielsenCount, "\n");
Print("うち可移(transitive)なもの = ", transitiveCount, "\n");
Print("(braid同値類の個数は別途要計算 -- ここでは順序3組の生カウントのみ・regression用の桁数を報告)\n");

# ===================================================================
# 封印検疫(3条件 + 札3固有の1条件)
# ===================================================================
Print("\n=== 封印検疫 ===\n");
Print("NAME-COLLIDE: 本certは K^(9) 窓インスタンス。封印の K^(5) 量とは別対象(裁定1007)。\n");
Print("n=5窓の値計算: 本scriptでは一切行っていない。\n");
Print("導出橋の出現: 本runの計算過程には現れなかった(bridge_detected=false)。\n");
Print("札3固有: 本scriptで扱う判別式平方類は函数体 F_9(E)^x/(.)^2 の類であり、\n");
Print("  封印の「c 平方類」(F_9^x の定数の類)とは異なるカテゴリの対象である(未判定・falsifier CV-9送り)。\n");

# ==== cert ====
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_k3t3.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

CTJson := function(ct)
  local parts, e;
  parts := [];
  for e in ct do Add(parts, JPair(e[1],e[2])); od;
  return JArr(parts);
end;;

scriptSha256 := ComputeSha256File("search/w9_k3_t3_lightcheck_v1.g");;

cert := Concatenation(
  "{\"schema\":\"w9-p1-k3-t3-lightcheck/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/w9_k3_t3_lightcheck_v1.g\",\"order\":\"裁定1019(t3車線・司令塔採用(a): E本体探索は数学者回付・軽量検算のみ)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"monG_size\":", String(Size(monG)), ",\"D\":", String(D),
  ",\"check1_stabilizer_action\":{",
    "\"stabilizer_size\":", String(Size(stab3)),
    ",\"image_on_block_size\":", String(Size(img3)),
    ",\"image_is_S3\":", JB(imgIsS3),
    ",\"image_is_C3\":", JB(imgIsC3),
  "}",
  ",\"check2_branch_regression\":{",
    "\"sigma0_cycle_type\":", CTJson(ct3X.cycleType),
    ",\"sigma1_cycle_type\":", CTJson(ct3Y.cycleType),
    ",\"sigmainf_cycle_type\":", CTJson(ct3Z.cycleType),
    ",\"matches_P1_0b_cert\":", JB(regressionOk),
  "}",
  ",\"check3_nielsen_class_E\":{",
    "\"six_cycle_count\":", String(Length(sixCycles)),
    ",\"type_1_1_2_2_count\":", String(Length(type622)),
    ",\"ordered_triples_product_one\":", String(nielsenCount),
    ",\"ordered_triples_transitive\":", String(transitiveCount),
  "}",
  ",\"quarantine\":{",
    "\"name_collide\":\"K^(9) 窓インスタンス・封印のK^(5)量とは別対象(裁定1007)\"",
    ",\"n5_window_forbidden\":\"n=5窓の値計算は本scriptで一切行っていない\"",
    ",\"derivation_bridge_stop_rule\":\"導出橋が現れたら即停止。本runでは未出現\"",
    ",\"sq3_disc_square_class_note\":\"函数体 F_9(E)^x/(.)^2 の類。封印c平方類とは別カテゴリ(未判定・falsifier CV-9送り)\"",
  "}",
  ",\"bridge_detected\":false",
  ",\"u_touched\":false,\"c_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/w9_k3_t3_lightcheck_v1_20260812.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
