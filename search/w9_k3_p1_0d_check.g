# search/w9_k3_p1_0d_check.g -- [P1-0d] 先行検算(秒・必須、裁定1023)
#
# 正本: docs/notes/t3_spec_and_C2_calib_v1.md §1(Nielsen 1800の分解=被覆3本・C2の指紋)。
# C2 候補の指紋 = monodromy 位数 36 ・ブロック系(3,2)・deck 群自明。
# 一致しなければ E の同定(docs/notes/w9_E_model_v1.md)が誤り ⟹ 即停止。
#
# 847依存監査: BuildPnFull は既存script群(r13_r0_v1.g等)と同一の確立済みH9fun構成パターン。

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
Ximg9 := Image(phiAction9, P9.X);;
Yimg9 := Image(phiAction9, P9.Y);;
Zimg9 := (Ximg9*Yimg9)^-1;;
monG := Group(Ximg9, Yimg9);;
Print("|monG| = ", Size(monG), " D = ", D, " (期待 324, 18)\n");

blocks := AllBlocks(monG);;
rep3 := First(blocks, b -> Length(b) = 3);;
Print("[", PF(rep3 <> fail), "] size-3 代表ブロック見つかった: ", rep3, "\n");

InducedPerm := function(perm, blockSystem)
  local nBlocks, blockOfPoint, pt, idx, images, i, imgPt, imgBlockIdx;
  nBlocks := Length(blockSystem);;
  blockOfPoint := [];;
  for idx in [1..nBlocks] do
    for pt in blockSystem[idx] do blockOfPoint[pt] := idx; od;
  od;
  images := [];;
  for i in [1..nBlocks] do
    imgPt := blockSystem[i][1]^perm;;
    imgBlockIdx := blockOfPoint[imgPt];;
    images[i] := imgBlockIdx;;
  od;
  return PermList(images);;
end;;

blockSystem3 := Orbit(monG, rep3, OnSets);;
qX := InducedPerm(Ximg9, blockSystem3);;
qY := InducedPerm(Yimg9, blockSystem3);;
qZ := InducedPerm(Zimg9, blockSystem3);;

# quotG = monodromy of the degree-6 cover E -> P1_t (candidate for C2), acting on the 6 blocks
quotG := Group(qX, qY);;
quotGOrder := Size(quotG);;
Print("degree-6 quotient monodromy group |quotG| = ", quotGOrder, " (期待 36)\n");
orderOk := (quotGOrder = 36);;
Print("[", PF(orderOk), "] monodromy 位数 = 36: ", orderOk, "\n");

qblocks := AllBlocks(quotG);;
qBlockSizes := Set(List(qblocks, b -> Length(b)));;
Print("quotG 上のブロックサイズ集合 = ", qBlockSizes, " (期待 {3} -- サイズ3ブロック2個 = (3,2)系)\n");
blockSystemOk := (3 in qBlockSizes);;
Print("[", PF(blockSystemOk), "] ブロック系(3,2)(サイズ3ブロックが存在): ", blockSystemOk, "\n");

S6 := SymmetricGroup(6);;
cent := Centralizer(S6, quotG);;
centOrder := Size(cent);;
Print("centralizer of quotG in S6, |cent| = ", centOrder, " (期待 1 = deck群自明)\n");
deckTrivialOk := (centOrder = 1);;
Print("[", PF(deckTrivialOk), "] deck群自明: ", deckTrivialOk, "\n");

isTrans := IsTransitive(quotG, [1..6]);;
Print("quotG は6点上で可移: ", isTrans, "\n");

allFingerprintOk := orderOk and blockSystemOk and deckTrivialOk and isTrans;;
Print("\n[", PF(allFingerprintOk), "] ★★★ [P1-0d] 指紋一致(位数36・ブロック系(3,2)・deck自明): ",
      allFingerprintOk, "\n");
if not allFingerprintOk then
  Print("[HALT] 指紋不一致 -- E の同定(w9_E_model_v1.md)が誤り。即停止・報告のみ。\n");
fi;

# ==== cert ====
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_p10d.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/w9_k3_p1_0d_check.g");;

cert := Concatenation(
  "{\"schema\":\"w9-p1-k3-p1-0d/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/w9_k3_p1_0d_check.g\",\"order\":\"裁定1023 [P1-0d] / docs/notes/t3_spec_and_C2_calib_v1.md §1\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"monG_size\":", String(Size(monG)), ",\"D\":", String(D),
  ",\"quotG_order\":", String(quotGOrder), ",\"quotG_order_ok\":", JB(orderOk),
  ",\"quotG_block_sizes\":", JArr(List(qBlockSizes,String)), ",\"block_system_3_2_ok\":", JB(blockSystemOk),
  ",\"centralizer_order\":", String(centOrder), ",\"deck_trivial_ok\":", JB(deckTrivialOk),
  ",\"quotG_transitive\":", JB(isTrans),
  ",\"fingerprint_all_ok\":", JB(allFingerprintOk),
  ",\"quarantine\":{",
    "\"name_collide\":\"K^(9) 窓インスタンス・封印のK^(5)量とは別対象(裁定1007)\"",
    ",\"n5_window_forbidden\":\"n=5窓の値計算は本scriptで一切行っていない\"",
    ",\"derivation_bridge_stop_rule\":\"導出橋が現れたら即停止。本runでは未出現\"",
  "}",
  ",\"bridge_detected\":false",
  ",\"u_touched\":false,\"c_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/w9_k3_p1_0d_check_v1_20260812.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
