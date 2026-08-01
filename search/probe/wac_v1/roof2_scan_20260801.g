#############################################################################
## search/probe/wac_v1/roof2_scan_20260801.g
## M2 = K^(9) cap L = K^(9) cap N0 の屋根走査(裁定400・凍結予言 P-R2-1..11)。
## 仕様の正本: docs/notes/roof2_cv9_freeze_v1.md SS5(実装仕様・段R2-0..R2-12)。
##
## 位置づけ(SS5.0 逐語):
##  - GAP 単系統。二系統になるのは「紙(定理M2)」であって実装ではない ->
##    cross-checked を請求しない。請求するのは「予言先行の的中」まで。
##  - 証明書非読: certificates/*.json(K3/K9/L01)は一切読まない。期待値は
##    driver 内のリテラル定数として hard assert する(接触遮断)。
##  - 判定関数 ScanRoofHexagon は search/probe/wac_v1/ihnec_r4b_run.g L77-116
##    (SHA-256 5bf6bc551eb7309c0b83adc363c15985973d9cb04e2cde9e7e34fe45c5277aa2)
##    を逐語再利用する(改造禁止)。H3 の座標規約(HMul/IdxOfElem/H3RegPerm)は
##    search/week3-L-explorer.g SS201-224 を逐語採用する。
##  - シャード不要: raw候補 26,244・群位数78,732(972屋根 4,408,992 の1/168)。
##    600秒 cap に大幅な余裕があるため1実行(事前登録)。
##
## 宇宙の事前登録: 対象は M2 = K^(9) cap L の1点のみ。n=5 非接触・他窓は触らない。
## 予言 P-R2-1..11 は本 driver に一切埋め込まない(接触遮断・凍結済み)。
##
## 実行順序: 先に別プロセスで
##   .\gap.ps1 search\probe\wac_v1\roof2_a4_anchor_run.g
## を走らせ search/certs/roof2_a4_anchor_20260801.json を作ってから、本 driver
## (別プロセス)を .\gap.ps1 search\probe\wac_v1\roof2_scan_20260801.g で走らせる。
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_roof2scan_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then
    Error("roof2_scan: ComputeSha256File: sha256sum did not return a hash line for ", relpath);
  fi;
  return line{[1 .. 64]};
end;;

# 小さな数値フィールド読取り(自分自身が別プロセスで生成した scratch cert
# search/certs/roof2_a4_anchor_20260801.json を読むだけ。certificates/*.json
# の frozen 参照証明書は一切読まない -- SS5.0 の「証明書非読」に抵触しない)。
ReadJsonIntField := function(path, key)
  local f, line, pattern, pos, rest, i, digitStr;
  f := InputTextFile(path);
  if f = fail then Error("ReadJsonIntField: cannot open ", path); fi;
  pattern := Concatenation("\"", key, "\":");
  while true do
    line := ReadLine(f);
    if line = fail then
      CloseStream(f);
      Error("ReadJsonIntField: key \"", key, "\" not found in ", path);
    fi;
    pos := PositionSublist(line, pattern);
    if pos <> fail then
      CloseStream(f);
      rest := line{[pos + Length(pattern) .. Length(line)]};
      digitStr := "";
      for i in [1 .. Length(rest)] do
        if rest[i] in "0123456789" then
          Append(digitStr, [rest[i]]);
        elif Length(digitStr) > 0 then
          break;
        fi;
      od;
      if Length(digitStr) = 0 then
        Error("ReadJsonIntField: no digits found for key ", key, " in ", path);
      fi;
      return Int(digitStr);
    fi;
  od;
end;;

#############################################################################
## ---- 単一定義: ScanRoofHexagon(ihnec_r4b_run.g L77-116 の逐語再利用) ----
#############################################################################
CharmingSetOf := function(nOrd)
  return Filtered([0 .. nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);
end;;

ScanRoofHexagon := function(qrec, charmingSet)
  local G, D, Delts, thetaHom, tauHom, zElt, h10Fail, h11Fail, genFail, shadows,
        m, u, f, thetaf, hex310, ymf, tauymf, tau2ymf, hex311, genA, genB, surj,
        candidateTotal, i;
  G := qrec.G;
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  thetaHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, qrec.x]);
  tauHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, zElt]);
  if thetaHom = fail or tauHom = fail then
    Error("ScanRoofHexagon: theta/tau homomorphism construction failed");
  fi;
  D := DerivedSubgroup(G);
  Delts := Elements(D);
  h10Fail := 0;  h11Fail := 0;  genFail := 0;  shadows := [];
  candidateTotal := Length(Delts) * Length(charmingSet);
  for m in charmingSet do
    u := 2*m + 1;
    for i in [1 .. Length(Delts)] do
      f := Delts[i];
      thetaf := Image(thetaHom, f);
      hex310 := AbstractProd([f, thetaf]) = Identity(G);
      if not hex310 then h10Fail := h10Fail + 1; continue; fi;
      ymf := AbstractProd([qrec.y^m, f]);
      tauymf := Image(tauHom, ymf);
      tau2ymf := Image(tauHom, tauymf);
      hex311 := AbstractProd([tau2ymf, tauymf, ymf]) = Identity(G);
      if not hex311 then h11Fail := h11Fail + 1; continue; fi;
      genA := qrec.x^u;
      genB := AbstractProd([f^-1, qrec.y^u, f]);
      surj := Size(Group(genA, genB)) = Size(G);
      if not surj then
        genFail := genFail + 1;
      else
        Add(shadows, rec(m := m, f := f));
      fi;
    od;
  od;
  return rec(candidate_total := candidateTotal, h10_fail := h10Fail, h11_fail := h11Fail,
             generation_fail := genFail, shadow_total := Length(shadows), shadows := shadows,
             derived_order := Length(Delts));
end;;

#############################################################################
## ---- H3 = Heisenberg mod 3, regular rep (week3-L-explorer.g SS201-224 逐語) ----
#############################################################################
HMul := function(p, q)
  return [ (p[1]+q[1]) mod 3, (p[2]+q[2]) mod 3, (p[3]+q[3]+p[1]*q[2]) mod 3 ];
end;;
IdxOfElem := function(e) return 9*e[1] + 3*e[2] + e[3] + 1; end;;
ElemOfIdx := function(idx)
  local k, a, b, e;
  k := idx - 1;
  a := QuoInt(k, 9);  k := k mod 9;
  b := QuoInt(k, 3);  e := k mod 3;
  return [a,b,e];
end;;
H3RegPerm := function(d)
  local l, idx;
  l := [];
  for idx in [1..27] do
    l[idx] := IdxOfElem(HMul(d, ElemOfIdx(idx)));
  od;
  return PermList(l);
end;;

# ---- block-diagonal direct-sum embedding (ihnec_r4b_run.g 逐語) ----
ShiftPerm := function(p, offset, size)
  local l, j;
  l := [1 .. offset+size];
  for j in [1 .. size] do l[offset+j] := offset + (j^p); od;
  return PermList(l);
end;;
DirectSumPerm := function(p1, deg1, p2, deg2)
  return p1 * ShiftPerm(p2, deg1, deg2);
end;;

#############################################################################
## ---- R2-0: G9・H3・Q := G9 x H3(54点 block-diagonal) ----
#############################################################################
Print("=== R2-0: G9 = MakeGn(9), H3 (Heisenberg mod 3, regular rep), Q = G9 x H3 ===\n");
g9 := MakeGn(9);;
Xh := [1,0,0];;  Yh := [0,1,0];;
Xp := H3RegPerm(Xh);;  Yp := H3RegPerm(Yh);;
H3grp := Group(Xp, Yp);;

if not (Xp^3 = () and Yp^3 = () and (Xp*Yp)^3 = ()) then
  Error("roof2_scan: H3 fixture FAILED: X^3=Y^3=(XY)^3=1 required");
fi;
commXY := Xp^-1 * Yp^-1 * Xp * Yp;;
if Order(commXY) <> 3 then
  Error("roof2_scan: H3 fixture FAILED: [X,Y] order != 3 (got ", Order(commXY), ")");
fi;
if not (commXY*Xp = Xp*commXY and commXY*Yp = Yp*commXY) then
  Error("roof2_scan: H3 fixture FAILED: [X,Y] not central");
fi;

if Size(g9.G) <> 2916 then
  Error("roof2_scan: |G9|=", Size(g9.G), " <> 2916 -- refusing to proceed");
fi;
if Size(H3grp) <> 27 then
  Error("roof2_scan: |H3|=", Size(H3grp), " <> 27 -- refusing to proceed");
fi;
DH3size := Size(DerivedSubgroup(H3grp));;
if DH3size <> 3 then
  Error("roof2_scan: |[H3,H3]|=", DH3size, " <> 3 -- refusing to proceed");
fi;

XM := DirectSumPerm(g9.x, 27, Xp, 27);;
YM := DirectSumPerm(g9.y, 27, Yp, 27);;
Q := Group(XM, YM);;
Qsize := Size(Q);;
if Qsize <> 78732 then
  Error("roof2_scan: |Q|=", Qsize, " <> 78732 -- refusing to proceed");
fi;
DQ := DerivedSubgroup(Q);;
DQsize := Size(DQ);;
if DQsize <> 2187 then
  Error("roof2_scan: |[Q,Q]|=", DQsize, " <> 2187 -- refusing to proceed");
fi;
Print("  |G9|=", Size(g9.G), " |H3|=", Size(H3grp), " |[H3,H3]|=", DH3size,
      " |Q|=", Qsize, " |[Q,Q]|=", DQsize, "\n");

#############################################################################
## ---- R2-1: M2_ord・charming set ----
#############################################################################
Print("\n=== R2-1: M2_ord, charming set ===\n");
M2ord := Lcm(Order(XM), Order(YM));;
Print("  M2_ord = ", M2ord, " (expect 18)\n");
if M2ord <> 18 then
  Error("roof2_scan: M2_ord=", M2ord, " <> 18 -- refusing to proceed");
fi;
M2charm := CharmingSetOf(M2ord);;
expectedCharm := [0,2,3,5,6,8,9,11,12,14,15,17];;
Print("  charming_set(M2) = ", M2charm, "\n");
if M2charm <> expectedCharm then
  Error("roof2_scan: charming set mismatch: got ", M2charm, " expected ", expectedCharm);
fi;

#############################################################################
## ---- R2-2 アンカー A1: ScanRoofHexagon(K9 単体) ----
#############################################################################
Print("\n=== R2-2 アンカー A1: ScanRoofHexagon(K9 単体) ===\n");
K9charm := CharmingSetOf(18);;
qrecK9 := rec(x := g9.x, y := g9.y, G := g9.G);;
t0 := Runtime();;
resK9 := ScanRoofHexagon(qrecK9, K9charm);;
t1 := Runtime();;
Print("  shadow_total=", resK9.shadow_total, " (expect 108)  time_ms=", t1-t0, "\n");
anchorA1OK := (resK9.shadow_total = 108);;
if not anchorA1OK then
  Error("roof2_scan: ANCHOR A1 FAILURE -- K9-alone shadow_total=", resK9.shadow_total, " <> 108");
fi;

#############################################################################
## ---- R2-3 アンカー A2: ScanRoofHexagon(L 単体, Q_L = G3 x H3) ----
#############################################################################
Print("\n=== R2-3 アンカー A2: ScanRoofHexagon(L 単体, Q_L = G3 x H3) ===\n");
g3 := MakeGn(3);;
if Size(g3.G) <> 108 then
  Error("roof2_scan: |G3|=", Size(g3.G), " <> 108 -- refusing to proceed");
fi;
XL := DirectSumPerm(g3.x, 9, Xp, 27);;
YL := DirectSumPerm(g3.y, 9, Yp, 27);;
QL := Group(XL, YL);;
QLsize := Size(QL);;
if QLsize <> 2916 then
  Error("roof2_scan: |Q_L|=", QLsize, " <> 2916 -- refusing to proceed");
fi;
Lord := Lcm(Order(XL), Order(YL));;
Print("  L_ord = ", Lord, " (expect 6)\n");
if Lord <> 6 then
  Error("roof2_scan: L_ord=", Lord, " <> 6 -- refusing to proceed");
fi;
Lcharm := CharmingSetOf(Lord);;
Print("  charming_set(L) = ", Lcharm, "\n");
qrecL := rec(x := XL, y := YL, G := QL);;
t0 := Runtime();;
resL := ScanRoofHexagon(qrecL, Lcharm);;
t1 := Runtime();;
Print("  shadow_total=", resL.shadow_total, " (expect 36)  time_ms=", t1-t0, "\n");
anchorA2OK := (resL.shadow_total = 36);;
if not anchorA2OK then
  Error("roof2_scan: ANCHOR A2 FAILURE -- L-alone shadow_total=", resL.shadow_total, " <> 36");
fi;

#############################################################################
## ---- R2-4 アンカー A3: ScanRoofHexagon(N0 単体 = H3)・集合等号 ----
#############################################################################
Print("\n=== R2-4 アンカー A3: ScanRoofHexagon(N0 単体 = H3), 集合等号 ===\n");
N0ord := Lcm(Order(Xp), Order(Yp));;
Print("  N0_ord = ", N0ord, " (expect 3)\n");
if N0ord <> 3 then
  Error("roof2_scan: N0_ord=", N0ord, " <> 3 -- refusing to proceed");
fi;
N0charm := CharmingSetOf(N0ord);;
Print("  charming_set(N0) = ", N0charm, " (expect [0,2])\n");
if N0charm <> [0,2] then
  Error("roof2_scan: N0 charming set mismatch: got ", N0charm);
fi;
qrecN0 := rec(x := Xp, y := Yp, G := H3grp);;
t0 := Runtime();;
resN0 := ScanRoofHexagon(qrecN0, N0charm);;
t1 := Runtime();;
Print("  shadow_total=", resN0.shadow_total, " (expect 6)  time_ms=", t1-t0, "\n");
anchorA3CountOK := (resN0.shadow_total = 6);;
if not anchorA3CountOK then
  Error("roof2_scan: ANCHOR A3 FAILURE -- N0-alone shadow_total=", resN0.shadow_total, " <> 6");
fi;
Zelt := commXY;;  # [X,Y] = Z in H3
predictedN0Pairs := [];;
for mmv in [0,2] do
  for aav in [0..2] do
    Add(predictedN0Pairs, [mmv, Zelt^aav]);
  od;
od;
actualN0Pairs := List(resN0.shadows, s -> [s.m, s.f]);;
N0SetEqual := (Set(actualN0Pairs) = Set(predictedN0Pairs));;
Print("  N0-alone shadow set = predicted {(m,Z^a): m in {0,2}, a in Z/3} ? ", N0SetEqual, "\n");
if not N0SetEqual then
  Error("roof2_scan: ANCHOR A3 SET-EQUALITY FAILURE -- N0-alone shadow set != {(m,Z^a)}");
fi;

#############################################################################
## ---- R2-5 アンカー A4: 972屋根の m=0 シャード(既存 R4b driver 無改変・別プロセス) ----
#############################################################################
Print("\n=== R2-5 アンカー A4: 972屋根 m=0 シャード(別プロセスの結果を読む) ===\n");
a4Path := "search/certs/roof2_a4_anchor_20260801.json";;
if not IsExistingFile(a4Path) then
  Error("roof2_scan: anchor A4 cert not found at ", a4Path,
        " -- run '.\\gap.ps1 search\\probe\\wac_v1\\roof2_a4_anchor_run.g' first (separate process, unmodified R4b driver)");
fi;
a4ShadowTotal := ReadJsonIntField(a4Path, "shadow_total");;
Print("  roof972 m=0 shard shadow_total (独立プロセスでの ihnec_r4b_run.g 無改変再走) = ",
      a4ShadowTotal, " (expect 81)\n");
anchorA4OK := (a4ShadowTotal = 81);;
if not anchorA4OK then
  Error("roof2_scan: ANCHOR A4 FAILURE -- roof972 m=0 shard shadow_total=", a4ShadowTotal, " <> 81");
fi;

#############################################################################
## ---- R2-6 主計算: ScanRoofHexagon(M2, charming_set(M2)) ----
#############################################################################
Print("\n=== R2-6 主計算: ScanRoofHexagon(M2, charming_set(M2)) ===\n");
qrecM2 := rec(x := XM, y := YM, G := Q);;
t0 := Runtime();;
resM2 := ScanRoofHexagon(qrecM2, M2charm);;
t1 := Runtime();;
Print("  derived_order=", resM2.derived_order, " (expect 2187)\n");
Print("  candidate_total=", resM2.candidate_total, " (expect 26244)\n");
Print("  h10_fail=", resM2.h10_fail, " h11_fail=", resM2.h11_fail,
      " generation_fail=", resM2.generation_fail, "\n");
Print("  shadow_total=", resM2.shadow_total, " (expect 324)  time_ms=", t1-t0, "\n");
if resM2.derived_order <> 2187 then
  Error("roof2_scan: resM2.derived_order=", resM2.derived_order, " <> 2187");
fi;
if resM2.candidate_total <> 26244 then
  Error("roof2_scan: candidate_total=", resM2.candidate_total, " <> 26244");
fi;
shadowBalance := (resM2.candidate_total - resM2.h10_fail - resM2.h11_fail - resM2.generation_fail
                   = resM2.shadow_total);;
Print("  引き算整合性チェック = ", shadowBalance, "\n");
if not shadowBalance then
  Error("roof2_scan: shadow accounting does not balance -- refusing to write a cert");
fi;

#############################################################################
## ---- R2-7: chi_tilde 像・m あたり shadow 個数(P-R2-4 の記述的検算) ----
#############################################################################
Print("\n=== R2-7: chi_tilde=2m+1 mod 36 の像、m あたり shadow 個数 ===\n");
chiTildeImg := Set(List(M2charm, mm -> (2*mm+1) mod 36));;
Print("  |{2m+1 mod 36 : m in charming(M2)}| = ", Length(chiTildeImg), " (expect 12)\n");
perMCounts := List(M2charm, mm -> Length(Filtered(resM2.shadows, s -> s.m = mm)));;
Print("  shadow 個数 (m ごと) = ", perMCounts, " (各27を期待)\n");
perMAll27 := ForAll(perMCounts, cc -> cc = 27);;
Print("  全 m で 27 か ? ", perMAll27, "\n");

#############################################################################
## ---- R2-8: settled 検査(324全 shadow, 真の settled = 自己同型として延びるか) ----
#############################################################################
Print("\n=== R2-8: settled 検査(", resM2.shadow_total, " shadow) ===\n");
t0 := Runtime();;
settledFailCount := 0;;
for sh in resM2.shadows do
  uSh := 2*sh.m + 1;
  genASh := qrecM2.x^uSh;
  genBSh := AbstractProd([sh.f^-1, qrecM2.y^uSh, sh.f]);
  Thom := GroupHomomorphismByImages(Q, Q, [qrecM2.x, qrecM2.y], [genASh, genBSh]);
  if Thom = fail or not IsBijective(Thom) then
    settledFailCount := settledFailCount + 1;
  fi;
od;
t1 := Runtime();;
Print("  settled_fail = ", settledFailCount, " / ", Length(resM2.shadows),
      " (expect fail 0)  time_ms=", t1-t0, "\n");
if settledFailCount <> 0 then
  Print("*** P-R2-9 MISS: settled_fail=", settledFailCount,
        " <> 0 -- M2 may not be isolated ***\n");
fi;

#############################################################################
## ---- R2-9: Im R_{M2,K9}(第1射影の相異個数)・d = 108/|Im| ----
#############################################################################
Print("\n=== R2-9: Im R_{M2,K9} ===\n");
imgK9Pairs := Set(List(resM2.shadows, s -> [s.m, compOfBlock(s.f, 0, 27)]));;
imgK9Size := Length(imgK9Pairs);;
Print("  |Im R_{M2,K9}| = ", imgK9Size, " (expect 108)\n");
if imgK9Size = 0 then
  dVal := "undefined(0)";;
else
  dVal := 108 / imgK9Size;;
fi;
Print("  d = 108/|Im R_{M2,K9}| = ", dVal, "\n");

#############################################################################
## ---- R2-10: Im R_{M2,L} ----
#############################################################################
Print("\n=== R2-10: Im R_{M2,L} ===\n");
rho := GroupHomomorphismByImages(g9.G, g3.G, [g9.x, g9.y], [g3.x, g3.y]);;
if rho = fail then
  Error("roof2_scan: rho: G9 -> G3 homomorphism construction failed");
fi;
kerRho := Kernel(rho);;
kerRhoSize := Size(kerRho);;
Print("  |ker rho| = ", kerRhoSize, " (expect 27)\n");
if kerRhoSize <> 27 then
  Error("roof2_scan: |ker rho|=", kerRhoSize, " <> 27 -- refusing to proceed");
fi;
imgLPairs := Set(List(resM2.shadows, s ->
  [s.m mod Lord, Image(rho, compOfBlock(s.f, 0, 27)), compOfBlock(s.f, 27, 27)]));;
imgLSize := Length(imgLPairs);;
Print("  |Im R_{M2,L}| = ", imgLSize, " (expect 36)\n");

#############################################################################
## ---- R2-11 (★必須・トリップワイヤ本体): 合成像 Im R_{M2,K3} ----
#############################################################################
Print("\n=== R2-11 (TRIPWIRE) Im R_{M2,K3} ===\n");
imgK3Pairs := Set(List(resM2.shadows, s -> [s.m mod Lord, Image(rho, compOfBlock(s.f, 0, 27))]));;
imgK3Size := Length(imgK3Pairs);;
Print("  |Im R_{M2,K3}| = ", imgK3Size, " (expect 12)\n");
tripwireFired := (imgK3Size < 12);;
if tripwireFired then
  Print("*** TRIPWIRE FIRED: |Im R_{M2,K3}| = ", imgK3Size,
        " < 12 -- THEOREM K3 MAY BE FALSE. STOP AND REPORT TO COMMANDER IMMEDIATELY. ***\n");
fi;

#############################################################################
## ---- JSON 出力(gtsh-cert/v1 互換 + docs/notes/roof2_cv9_freeze_v1.md SS5.2 の追加欄) ----
#############################################################################
ShadowJson := function(s)
  return Concatenation("{\"m\":", String(s.m), ",\"f\":", JStr(String(s.f)), "}");
end;;
SHADOW_SAMPLE_CAP := 2000;;
shadowsTruncated := (Length(resM2.shadows) > SHADOW_SAMPLE_CAP);;
shadowsOut := resM2.shadows;;
if shadowsTruncated then
  shadowsOut := resM2.shadows{[1 .. SHADOW_SAMPLE_CAP]};;
fi;;

selfSha := ComputeSha256File("search/probe/wac_v1/roof2_scan_20260801.g");;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"gtsh-cert/v1+roof2\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/roof2_scan_20260801.g\",\n",
  "  \"card_label\":\"M2屋根走査(裁定400・docs/notes/roof2_cv9_freeze_v1.md 凍結予言 P-R2-1..11)\",\n",
  "  \"design_doc\":\"docs/notes/roof2_cv9_freeze_v1.md SS5\",\n",
  "  \"target\":{\n",
  "    \"id\":\"M2\",\n",
  "    \"family\":\"general\",\n",
  "    \"construction\":{\"g9\":\"MakeGn(9)\",\"h3\":\"(a,b,e) coords, X=(1,0,0), Y=(0,1,0)\",",
  "\"note\":\"M2 = K^(9) cap N0 = K^(9) cap L\"}\n",
  "  },\n",
  "  \"invariants\":{\"index_PB3\":", String(Qsize), ",\"index_B3\":", String(Qsize*6),
  ",\"N_ord\":", String(M2ord), ",\"derived_order\":", String(DQsize), "},\n",
  "  \"anchors\":{\n",
  "    \"k9_alone\":", String(resK9.shadow_total), ",\"k9_alone_expected\":108,",
  "\"k9_alone_pass\":", JB(anchorA1OK), ",\n",
  "    \"l_alone\":", String(resL.shadow_total), ",\"l_alone_expected\":36,",
  "\"l_alone_pass\":", JB(anchorA2OK), ",\n",
  "    \"n0_alone\":", String(resN0.shadow_total), ",\"n0_alone_expected\":6,",
  "\"n0_alone_pass\":", JB(anchorA3CountOK), ",\n",
  "    \"n0_set_equality\":", JB(N0SetEqual), ",\n",
  "    \"roof972_m0_shard\":", String(a4ShadowTotal), ",\"roof972_m0_shard_expected\":81,",
  "\"roof972_m0_shard_pass\":", JB(anchorA4OK), "\n",
  "  },\n",
  "  \"counts\":{\n",
  "    \"raw_candidates\":", String(resM2.candidate_total), ",\n",
  "    \"h10_fail\":", String(resM2.h10_fail), ",\n",
  "    \"h11_fail\":", String(resM2.h11_fail), ",\n",
  "    \"generation_fail\":", String(resM2.generation_fail), ",\n",
  "    \"shadow_total\":", String(resM2.shadow_total), ",\n",
  "    \"shadow_accounting_balances\":", JB(shadowBalance), ",\n",
  "    \"per_m_shadow_counts\":", JArr(List(perMCounts, String)), ",\n",
  "    \"per_m_all_27\":", JB(perMAll27), ",\n",
  "    \"chi_tilde_image_mod36_count\":", String(Length(chiTildeImg)), "\n",
  "  },\n",
  "  \"settled\":{\n",
  "    \"total\":", String(Length(resM2.shadows)), ",\n",
  "    \"settled_fail\":", String(settledFailCount), "\n",
  "  },\n",
  "  \"reduction\":[\n",
  "    {\"to\":\"K9\",\"image_size\":", String(imgK9Size), ",\"expected\":108,",
  "\"surjective\":", JB(imgK9Size = 108), ",\"d\":", String(dVal), "},\n",
  "    {\"to\":\"L\",\"image_size\":", String(imgLSize), ",\"expected\":36,",
  "\"surjective\":", JB(imgLSize = 36), "},\n",
  "    {\"to\":\"K3\",\"image_size\":", String(imgK3Size), ",\"expected\":12,",
  "\"surjective\":", JB(imgK3Size = 12), ",\"tripwire_fired\":", JB(tripwireFired), "}\n",
  "  ],\n",
  "  \"shadows_sample\":{\n",
  "    \"truncated\":", JB(shadowsTruncated), ",\n",
  "    \"cap\":", String(SHADOW_SAMPLE_CAP), ",\n",
  "    \"count_in_sample\":", String(Length(shadowsOut)), ",\n",
  "    \"items\":", JArr(List(shadowsOut, ShadowJson)), "\n",
  "  },\n",
  "  \"conventions_used\":{\n",
  "    \"ledger_version\":\"conventions_ledger_v1_3\",\n",
  "    \"perm_composition\":\"gap_native_right_action\",\n",
  "    \"reduced_hexagon_predicate\":\"逐語 search/probe/wac_v1/ihnec_r4b_run.g ScanRoofHexagon(L77-116, SHA-256 5bf6bc551eb7309c0b83adc363c15985973d9cb04e2cde9e7e34fe45c5277aa2) と数学的に同一。改造なし。\",\n",
  "    \"h3_element\":\"(a,b,e) in (Z/3)^3, X=(1,0,0), Y=(0,1,0), product (a,b,e)(a',b',e')=(a+a',b+b',e+e'+a*b') mod 3 (search/week3-L-explorer.g SS201-224 逐語)\",\n",
  "    \"comparison_target\":\"n/a(単系統GAP探索。二実装照合ではない)\",\n",
  "    \"independence_note\":\"certificates/K3.v1.json・K9.v1.json・L01.v1.jsonを読まない。G9・H3・G3はGAPで生成器から新規構築。R2-5アンカーのみ別プロセスが生成した scratch cert search/certs/roof2_a4_anchor_20260801.json を数値読取り(証明書非読はcertificates/*.jsonの参照に限る)\"\n",
  "  },\n",
  "  \"cross_checked_status\":{\"status\":\"n/a\",\"reason\":\"単系統GAP探索(ScanRoofHexagon逐語再利用)。cross-checkedを主張しない。二系統目は紙(定理M2)であって実装ではない。請求するのは予言先行の的中まで。\"},\n",
  "  \"scope\":{\n",
  "    \"isolated_K9\":\"canon Thm 4.3\",\n",
  "    \"isolated_N0\":\"paper (補題N0, Sol監査未)\",\n",
  "    \"isolated_M2\":\"paper (定理M2(ii), Sol監査未)\",\n",
  "    \"lane\":\"GAP single lane\"\n",
  "  },\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"plan_frozen_doc\":\"docs/notes/roof2_cv9_freeze_v1.md\",\n",
  "    \"wall_ms_total\":", String(GAPLIB_WallElapsedMs()), "\n",
  "  }\n",
  "}\n");;

WriteFile("search/certs/roof2_scan_20260801.json", cert);;
Print("\nWrote search/certs/roof2_scan_20260801.json\n");
Print("\nROOF2_SCAN_DRIVER_DONE\n");
QUIT;
