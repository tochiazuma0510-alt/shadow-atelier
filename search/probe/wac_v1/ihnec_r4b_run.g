#############################################################################
## search/probe/wac_v1/ihnec_r4b_run.g
## IH-NEC R4b(裁定376 GO・§6.6 R4b・追補C.4 の残件・実装係)。
##
## 何をするか: docs/notes/ihnec_v1.md 命題 ROOF(4) の「独立確認」。屋根
## M := K^(9) ∩ N_S4 で B3/M の hexagon を GAP で直接検査し、|GT(M)|=972
## (P-IHN-4)を R4a(python・既存証明書からの組立)を一切読まずに独立に出す。
## 同時に P-IHN-1/2/3 の機械脚(方法 CMP・|PB3/M|・M_ord)も測る(追補C.4が
## R4a の射程外と明記した3項目)。
##
## 設計からの変更点(先に申告する — 追補C.1と同じ規律):
##  v1 §6.6 は「屋根での悉皆走査」を EnumerateReducedHexagon(既存の BFS+word
##  トラッキング版)の流用として想定していたと読めるが、それは全群 G_M
##  (位数 1,469,664)全体を BFS で辿り辞書に単語つきで記憶する実装であり、
##  本件では単語が不要(cert に要るのは f 自身と合否だけ)なのに全群を辞書に
##  乗せるのは RAM 8GB 制約に照らして不必要に重い。ROOF(4) の独立確認に必要
##  なのは「[G_M,G_M] の元 f それぞれで (3.10)(3.11) の簡約 hexagon と生成条件
##  を直接検査する」ことだけなので、本 driver は ScanRoofHexagon という新関数
##  (数学的判定式は EnumerateReducedHexagon と同一・逐語)を書き、列挙戦略だけ
##  を Elements(DerivedSubgroup(G)) の直接列挙(BFS・辞書なし)に替えた。
##  判定式(theta/tau・hex310・hex311・genA/genB)は単一箇所でのみ定義し
##  (CV-13 の精神・生成/受理の向き混用を避ける)、K9 単体・S4 単体・M の
##  3窓すべてに同一関数を通す。
##
## 独立性(v1 §6.6 注1・追補C.1 の要求): 本 driver は certificates/K9.v1.json・
## certificates/S4.v2.json を一切読まない。G9・P はいずれも GAP で生成器から
## 新規に構築する(K9: search/week3-battery-common.g の MakeGn(9)、S4:
## search/week3-psl-common.g の GF(8) 上の明示行列から)。R4a(python・既存
## 証明書の合成表を入力)とは独立な第2計算である。
##
## 自己検査(CV-13 の精神 — 生成/受理の向き自己検査 assert):
##  M 本体を検査する前に、同一の ScanRoofHexagon を K9 単体・S4 単体に適用し、
##  既知値 108 / 54(K9.v1.json・S4.v2.json に記録済みの機械測定値だが、ここ
##  では値を「読む」のではなく独立に「再現」する — cert ファイルはやはり
##  読まない)と一致することを fail-closed に assert する。不一致なら M の
##  計算に進まず即 Error で停止する(向き規約・生成器規約の誤りを M の巨大
##  計算に先立って捕まえる)。
##
## シャード: charmingSet_M(M_ord=18 での charming 集合・12元)を1 shard=1 m
## 値に分割する(宇宙の事前登録 = 窓 M 固定・分割は m の値で決定的)。
## 変数 R4B_TARGET_MS(m の値のリスト)を shard の preamble で注入する
## (mine の shards[].preamble 規約・lt_count_gen.g と同型)。未設定なら
## charmingSet_M 全体(12個)を1本で処理する(ローカル smoke 用フォールバック)。
## R4B_OUTPUT(出力パス)も同様に注入可能・未設定時は既定名。
##
## 宇宙の事前登録: 対象は (N_S4, K^(9)) の1対・屋根 M のみ。n=5 非接触。
## 予言 P-IHN-1〜7 は本 driver に一切埋め込まない(接触遮断・凍結済み)。
##
## 実行: .\gap.ps1 search\probe\wac_v1\ihnec_r4b_run.g  (ローカル試走・単一
## shard 全体一括、smoke用)。本番は mine 経由(shards[].preamble で
## R4B_TARGET_MS を1値ずつ注入)。
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_ihnecr4b_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then
    Error("ihnec_r4b_run: ComputeSha256File: sha256sum did not return a hash line for ", relpath);
  fi;
  return line{[1 .. 64]};
end;;

#############################################################################
## ---- 単一定義: 簡約 hexagon 判定式(theta/tau・hex310・hex311・生成条件) ----
##  EnumerateReducedHexagon(week3-battery-common.g)と数学的に逐語同一。
##  K9単体・S4単体・M の3窓すべてがこの1関数だけを通る(CV-13 の精神)。
##  列挙戦略のみ変更: BFS+word辞書(既存関数)ではなく
##  Elements(DerivedSubgroup(G)) の直接列挙(RAM節約・word不要)。
#############################################################################
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

CharmingSetOf := function(nOrd)
  return Filtered([0 .. nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);
end;;

#############################################################################
## ---- 窓1: K9 = PB3/K^(9)(week3-battery-common.g MakeGn(9)・certは読まない) ----
#############################################################################
Print("=== 窓1: G9 = MakeGn(9) ===\n");
t0 := Runtime();;
g9 := MakeGn(9);;
K9sz := Size(g9.G);;
K9ord := Lcm(Order(g9.x), Order(g9.y));;
t1 := Runtime();;
Print("  |PB3/K9|=", K9sz, " (expect 2916)  K9_ord=", K9ord, " (expect 18)  time_ms=", t1-t0, "\n");
if K9sz <> 2916 or K9ord <> 18 then
  Error("ihnec_r4b_run: K9 window construction mismatch -- refusing to proceed");
fi;
K9charm := CharmingSetOf(K9ord);;
Print("  charming_set(K9) = ", K9charm, "  (|.|=", Length(K9charm), ", expect 12)\n");

#############################################################################
## ---- 窓2: P = PB3/N_S4 = PSL(2,8)(week3-psl-S4.g の GF(8) 明示行列。certは読まない) ----
#############################################################################
Print("\n=== 窓2: P = PSL(2,8) (S,T from GF(8) matrices, week3-psl-S4.g conventions) ===\n");
t0 := Runtime();;
CheckGF8();;
Smat := MakeMatGF8(1,0,1,1);;
Tmat := MakeMatGF8(4,3,1,5);;
Sperm := MatToPermGF8(Smat);;
Tperm := MatToPermGF8(Tmat);;
wPerm := Sperm * Tperm^-1;;
Xperm := wPerm^2;;
Yperm := Sperm^-1 * Xperm * Sperm;;
Pgrp := Group(Xperm, Yperm);;
Psz := Size(Pgrp);;
Pord := Lcm(Order(Xperm), Order(Yperm));;
t1 := Runtime();;
Print("  |PB3/N_S4|=", Psz, " (expect 504)  N_S4_ord=", Pord, " (expect 9)  time_ms=", t1-t0, "\n");
if Psz <> 504 or Pord <> 9 then
  Error("ihnec_r4b_run: S4 window construction mismatch -- refusing to proceed");
fi;
S4charm := CharmingSetOf(Pord);;
Print("  charming_set(S4) = ", S4charm, "  (expect [0,2,3,5,6,8])\n");
if S4charm <> [0,2,3,5,6,8] then
  Error("ihnec_r4b_run: S4 charming set mismatch -- refusing to proceed");
fi;

#############################################################################
## ---- 自己検査アンカー(CV-13 の精神): ScanRoofHexagon を K9単体・S4単体に
##      適用し、既知値108/54(独立再現・cert読込みなし)と一致するか fail-closed
##      に assert する。M の巨大計算に進む前に向き規約の誤りを捕まえる。
#############################################################################
Print("\n=== 自己検査アンカー: ScanRoofHexagon(K9単体) ==\n");
t0 := Runtime();;
qrecK9 := rec(x := g9.x, y := g9.y, G := g9.G);;
resK9 := ScanRoofHexagon(qrecK9, K9charm);;
t1 := Runtime();;
Print("  candidate_total=", resK9.candidate_total, " h10_fail=", resK9.h10_fail,
      " h11_fail=", resK9.h11_fail, " generation_fail=", resK9.generation_fail,
      " shadow_total=", resK9.shadow_total, " (expect 108)  time_ms=", t1-t0, "\n");
anchorK9OK := (resK9.shadow_total = 108);;
if not anchorK9OK then
  Error("ihnec_r4b_run: ANCHOR FAILURE -- K9-alone ScanRoofHexagon gives ",
        resK9.shadow_total, " shadows, expected 108. Refusing to proceed to the ",
        "roof computation with an unverified orientation/convention.");
fi;

Print("\n=== 自己検査アンカー: ScanRoofHexagon(S4単体) ==\n");
t0 := Runtime();;
qrecS4 := rec(x := Xperm, y := Yperm, G := Pgrp);;
resS4 := ScanRoofHexagon(qrecS4, S4charm);;
t1 := Runtime();;
Print("  candidate_total=", resS4.candidate_total, " h10_fail=", resS4.h10_fail,
      " h11_fail=", resS4.h11_fail, " generation_fail=", resS4.generation_fail,
      " shadow_total=", resS4.shadow_total, " (expect 54)  time_ms=", t1-t0, "\n");
anchorS4OK := (resS4.shadow_total = 54);;
if not anchorS4OK then
  Error("ihnec_r4b_run: ANCHOR FAILURE -- S4-alone ScanRoofHexagon gives ",
        resS4.shadow_total, " shadows, expected 54. Refusing to proceed.");
fi;

#############################################################################
## ---- P-IHN-1(方法CMP手順3): 比較可能性(両向き GroupHomomorphismByImages) ----
#############################################################################
Print("\n=== P-IHN-1: 比較可能性(方法CMP手順3・両向き) ===\n");
homNS4toK9 := GroupHomomorphismByImages(Pgrp, g9.G, [Xperm, Yperm], [g9.x, g9.y]);;
homK9toNS4 := GroupHomomorphismByImages(g9.G, Pgrp, [g9.x, g9.y], [Xperm, Yperm]);;
cmpNS4subK9 := (homNS4toK9 <> fail);;
cmpK9subNS4 := (homK9toNS4 <> fail);;
Print("  N_S4 subseteq K9 ? ", cmpNS4subK9, " (expect false/fail)\n");
Print("  K9 subseteq N_S4 ? ", cmpK9subNS4, " (expect false/fail)\n");
comparable := cmpNS4subK9 or cmpK9subNS4;;
Print("  比較不能(両方 fail) ? ", not comparable, "  (P-IHN-1 予言 = 比較不能)\n");

#############################################################################
## ---- 屋根 M := K9 ∩ N_S4: block-diagonal embed on 27+9=36 points ----
#############################################################################
Print("\n=== 屋根 M := K^(9) cap N_S4 の構成(27+9=36点の block-diagonal 埋め込み) ===\n");
t0 := Runtime();;
ShiftPerm := function(p, offset, size)
  local l, j;
  l := [1 .. offset+size];
  for j in [1 .. size] do l[offset+j] := offset + (j^p); od;
  return PermList(l);
end;;
DirectSumPerm := function(p1, deg1, p2, deg2)
  return p1 * ShiftPerm(p2, deg1, deg2);
end;;
XM := DirectSumPerm(g9.x, 27, Xperm, 9);;
YM := DirectSumPerm(g9.y, 27, Yperm, 9);;
GM := Group(XM, YM);;
t1 := Runtime();;
Print("  built XM,YM,GM  time_ms=", t1-t0, "\n");

#############################################################################
## ---- P-IHN-2 / P-IHN-3: |PB3/M| と M_ord(機械測定・ROOF(1)(2)の独立確認) ----
#############################################################################
Print("\n=== P-IHN-2/3: |PB3/M| と M_ord (機械測定) ===\n");
t0 := Runtime();;
PB3overM := Size(GM);;
t1 := Runtime();;
Print("  |PB3/M| = ", PB3overM, " (expect 1469664 = 2916*504)  time_ms=", t1-t0, "\n");
pihn2OK := (PB3overM = 2916*504);;
if not pihn2OK then
  Print("*** P-IHN-2 MISS: |PB3/M| = ", PB3overM, " <> 1469664 -- ROOF(1) does NOT hold as predicted ***\n");
fi;

t0 := Runtime();;
Mord := Lcm(Order(XM), Order(YM));;
t1 := Runtime();;
Print("  M_ord = Lcm(ord XM, ord YM) = ", Mord, " (expect 18)  time_ms=", t1-t0, "\n");
pihn3OK := (Mord = 18);;
if not pihn3OK then
  Print("*** P-IHN-3 MISS: M_ord = ", Mord, " <> 18 -- ROOF(2) does NOT hold as predicted ***\n");
fi;

Mcharm := CharmingSetOf(Mord);;
Print("  charming_set(M) = ", Mcharm, "  (|.|=", Length(Mcharm), ", expect 12)\n");

#############################################################################
## ---- shard 選択: R4B_TARGET_MS(preamble 注入)。未設定なら全12値を1本で処理 ----
#############################################################################
if not IsBound(R4B_TARGET_MS) then
  R4B_TARGET_MS := ShallowCopy(Mcharm);;
  Print("\n[shard] R4B_TARGET_MS 未設定 -- charmingSet(M) 全体(", Length(Mcharm),
        "値)を1本で処理する(ローカル smoke フォールバック)\n");
else
  Print("\n[shard] R4B_TARGET_MS = ", R4B_TARGET_MS, " (preamble 注入)\n");
fi;
if not IsSubset(Mcharm, R4B_TARGET_MS) then
  Error("ihnec_r4b_run: R4B_TARGET_MS contains a value not in charmingSet(M)=", Mcharm,
        " -- got ", R4B_TARGET_MS, ". Refusing to proceed (universe drift guard).");
fi;
if not IsBound(R4B_OUTPUT) then
  R4B_OUTPUT := "search/certs/ihnec_r4b_run_20260801.json";;
fi;

#############################################################################
## ---- R4b 主計算: 屋根 M での直接悉皆走査(ROOF(4)の独立確認) ----
#############################################################################
Print("\n=== R4b 主計算: ScanRoofHexagon(M, R4B_TARGET_MS) ===\n");
qrecM := rec(x := XM, y := YM, G := GM);;
t0 := Runtime();;
resM := ScanRoofHexagon(qrecM, R4B_TARGET_MS);;
t1 := Runtime();;
Print("  target_ms=", R4B_TARGET_MS, "\n");
Print("  derived_order=", resM.derived_order, " (expect 367416 = 729*504)\n");
Print("  candidate_total=", resM.candidate_total, " h10_fail=", resM.h10_fail,
      " h11_fail=", resM.h11_fail, " generation_fail=", resM.generation_fail,
      " shadow_total=", resM.shadow_total, "  time_ms=", t1-t0, "\n");
shadowSumCheck := (resM.candidate_total - resM.h10_fail - resM.h11_fail - resM.generation_fail
                    = resM.shadow_total);;
Print("  引き算整合性チェック = ", shadowSumCheck, "\n");
if not shadowSumCheck then
  Error("ihnec_r4b_run: shadow accounting does not balance -- refusing to write a cert");
fi;

#############################################################################
## ---- R5相当: このshardが担当するmでの reduction 像(R_{M,K9}・R_{M,N_S4}) ----
#############################################################################
imgK9mods := Set(List(resM.shadows, s -> s.m mod K9ord));;
imgS4mods := Set(List(resM.shadows, s -> s.m mod Pord));;
Print("  このshardのm値がK9側に落とす像(mod 18) = ", imgK9mods, "\n");
Print("  このshardのm値がS4側に落とす像(mod 9)  = ", imgS4mods, "\n");

#############################################################################
## ---- JSON 出力 ----
#############################################################################
ShadowJson := function(s)
  return Concatenation("{\"m\":", String(s.m), ",\"f\":", JStr(String(s.f)), "}");
end;;

SHADOW_SAMPLE_CAP := 2000;;
shadowsTruncated := (Length(resM.shadows) > SHADOW_SAMPLE_CAP);;
shadowsOut := resM.shadows;;
if shadowsTruncated then
  shadowsOut := resM.shadows{[1 .. SHADOW_SAMPLE_CAP]};;
fi;;

selfSha := ComputeSha256File("search/probe/wac_v1/ihnec_r4b_run.g");;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"ihnec-r4b/v1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/ihnec_r4b_run.g\",\n",
  "  \"card_label\":\"IH-NEC R4b(裁定376 GO・命題ROOF(4)独立確認・追補C.4残件のP-IHN-1/2/3機械脚)\",\n",
  "  \"design_doc\":\"docs/notes/ihnec_v1.md v1 SS6.6 R4b + 追補C.4\",\n",
  "  \"note\":\"R4a(scratchpad/ihnec_r4a_run.py)とは独立: certificates/K9.v1.json・S4.v2.jsonを一切読まない。G9・PともGAPで生成器から新規構築。数学的判定式(theta/tau・hex310・hex311・生成条件)はK9単体/S4単体/Mの3窓で単一関数ScanRoofHexagonを共有(生成/受理の向き混用を避けるCV-13の精神)。M本体の計算前にK9単体=108・S4単体=54の既知値と独立再現一致をfail-closedに自己検査済み。\",\n",
  "  \"anchors\":{\n",
  "    \"k9_alone_shadow_total\":", String(resK9.shadow_total), ",\n",
  "    \"k9_alone_expected\":108,\n",
  "    \"k9_alone_pass\":", JB(anchorK9OK), ",\n",
  "    \"s4_alone_shadow_total\":", String(resS4.shadow_total), ",\n",
  "    \"s4_alone_expected\":54,\n",
  "    \"s4_alone_pass\":", JB(anchorS4OK), "\n",
  "  },\n",
  "  \"p_ihn_1\":{\n",
  "    \"n_s4_subseteq_k9\":", JB(cmpNS4subK9), ",\n",
  "    \"k9_subseteq_n_s4\":", JB(cmpK9subNS4), ",\n",
  "    \"incomparable\":", JB(not comparable), ",\n",
  "    \"prediction_matches\":", JB(not comparable), "\n",
  "  },\n",
  "  \"p_ihn_2\":{\n",
  "    \"pb3_over_m\":", String(PB3overM), ",\n",
  "    \"expected\":", String(2916*504), ",\n",
  "    \"pass\":", JB(pihn2OK), "\n",
  "  },\n",
  "  \"p_ihn_3\":{\n",
  "    \"m_ord\":", String(Mord), ",\n",
  "    \"expected\":18,\n",
  "    \"pass\":", JB(pihn3OK), "\n",
  "  },\n",
  "  \"charming_set_m\":", JArr(List(Mcharm, String)), ",\n",
  "  \"shard\":{\n",
  "    \"target_ms\":", JArr(List(R4B_TARGET_MS, String)), ",\n",
  "    \"universe_charming_set_m\":", JArr(List(Mcharm, String)), "\n",
  "  },\n",
  "  \"scan\":{\n",
  "    \"derived_order\":", String(resM.derived_order), ",\n",
  "    \"derived_order_expected\":367416,\n",
  "    \"candidate_total\":", String(resM.candidate_total), ",\n",
  "    \"h10_fail\":", String(resM.h10_fail), ",\n",
  "    \"h11_fail\":", String(resM.h11_fail), ",\n",
  "    \"generation_fail\":", String(resM.generation_fail), ",\n",
  "    \"shadow_total\":", String(resM.shadow_total), ",\n",
  "    \"shadow_accounting_balances\":", JB(shadowSumCheck), "\n",
  "  },\n",
  "  \"shadows_sample\":{\n",
  "    \"truncated\":", JB(shadowsTruncated), ",\n",
  "    \"cap\":", String(SHADOW_SAMPLE_CAP), ",\n",
  "    \"count_in_sample\":", String(Length(shadowsOut)), ",\n",
  "    \"items\":", JArr(List(shadowsOut, ShadowJson)), "\n",
  "  },\n",
  "  \"reduction_images_this_shard\":{\n",
  "    \"note\":\"このshardが担当するR4B_TARGET_MSの範囲内でのみ計算した部分像(全shard集約後にP-IHN-5/6の108/108・54/54を検算する材料)\",\n",
  "    \"k9_m_image_mod18\":", JArr(List(imgK9mods, String)), ",\n",
  "    \"s4_m_image_mod9\":", JArr(List(imgS4mods, String)), "\n",
  "  },\n",
  "  \"conventions_used\":{\n",
  "    \"ledger_version\":\"conventions_ledger_v1_3\",\n",
  "    \"perm_composition\":\"gap_native_right_action\",\n",
  "    \"reduced_hexagon_predicate\":\"逐語 search/week3-battery-common.g EnumerateReducedHexagon と数学的に同一(f*theta(f)=1・tau^2(y^m f) tau(y^m f) (y^m f)=1・生成条件)。列挙戦略のみ変更(BFS+word辞書 -> Elements(DerivedSubgroup(G)) 直接列挙・word不要のためRAM節約)\",\n",
  "    \"comparison_target\":\"n/a(単系統GAP探索。二実装照合ではない)\",\n",
  "    \"independence_note\":\"certificates/K9.v1.json・S4.v2.jsonを読まない。G9・PはGAPで生成器から新規構築(週3-*-common.gの既存関数を再利用)。R4a(python・既存証明書入力)とは独立な第2計算\"\n",
  "  },\n",
  "  \"cross_checked_status\":{\"status\":\"n/a\",\"reason\":\"単系統GAP探索(quotient-shortcut reduced hexagon)。cross-checkedを主張しない。R4bはR4aと独立(入力を共有しない)が、両者とも数学的な照合器(独立実装によるcrosscheck)ではない\"},\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"wall_ms_total\":", String(GAPLIB_WallElapsedMs()), "\n",
  "  }\n",
  "}\n");;

WriteFile(R4B_OUTPUT, cert);;
Print("\nWrote ", R4B_OUTPUT, "\n");
Print("\nIHNEC_R4B_DRIVER_DONE\n");
QUIT;
