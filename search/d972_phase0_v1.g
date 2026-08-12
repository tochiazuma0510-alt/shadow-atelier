## search/d972_phase0_v1.g -- TRIAD-972 大戦 Phase 0(gating・必須)測定(裁定1127)
##
## 正本: docs/notes/triad972_grade_and_battle_plan_v1.md §6 Phase 0(D972-0)。
##   [0-1] |B_3/M| , |PB_3/M| を測る
##   [0-2] (H1) M が isolated か: #C(M) = 1 を marked factor map で確認(系 C)
##   [0-3] |GT(M)| = 972 の実測(T63 鎖 (6) の一部の独立確認)
##   [0-4] 細分候補の gating: K^(27) subseteq K^(9)・|B_3/K^(27)| の独立確認
##
## 構成の再利用(既存資産、847監査型の再入力ではなく再実行):
##   - K(9) 窓: search/week3-battery-common.g MakeGn(9)
##   - N_S4 窓: search/week3-psl-common.g の GF(8) 明示行列(週3-psl-S4.g 慣習)
##   - M := K^(9) cap N_S4: search/probe/wac_v1/ihnec_r4b_run.g(裁定376)の
##     block-diagonal 直和埋め込みパターン、および search/frattini_resolution_v2.g
##     (裁定1037)の ScanRoofHexagon / BuildShadowCompositionRegularRep
##   - [0-2] の marked-factor-map 定義参照実装: search/set_surgery_fixture_v1.g
##     (裁定1082)・その軽量代替(well-definedness 判定法): search/at2_p2_m_isolated_v1.g
##     (裁定1114/1117)
##
## [0-2] の設計からの逸脱(先に申告する):
##   marked-factor-map(#C(M) の直接判定)は AutomorphismGroup(PN) を要求するが、
##   本窓の PN = GM は位数 1,469,664(P2 補測で実測不能に陥った |Q|=1176 の
##   1249 倍)であり、AutomorphismGroup の実行は RAM 8GB 制約下でメモリ死
##   ほぼ確実(裁定1117 の教訓そのもの)。指示された切替先(well-definedness
##   判定法)は M の「フル B3 生成元」sigma1,sigma2(半捻り自身の像、K(9) 窓
##   側では MakeGn が x=sigma1^2,y=sigma2^2 のみを直接式で与え sigma1,sigma2
##   自身を公開しない)を要求するが、これは既存の再利用可能資産に存在しない。
##   scratchpad/try_sigma_k9.g で「block-swap * block対角元」という自然な
##   ansatz を機械探索したが、D_9 に位数4の元が存在しない(位数は 1,2,3,6,9,18
##   のみ)ため sigma1^2 = x の block3 成分(位数2の s)を再現する候補は原理的に
##   存在しない(機械的に確認・0/25候補が一致)。これ以上の ansatz 拡大や文献
##   依拠の式は「勝手に決めず報告」の対象と判断し、[0-2] は本 script では
##   UNKNOWN として生値のみ記録し、司令塔へ疑問点として報告する(CLAUDE.md
##   「設計判断に迷ったら勝手に決めずに...報告し戻す」)。
##
## 規律: u/c 非接触・封印3量非接触・prereg 量の解釈なし。生値のみ・判定語なし。
## |B_3/M|・|B_3/K^(27)| は |PB_3/·| の GAP 実測値に「M/K^(27) が B3 で正規」
## という(既存 cert 群が暗黙に前提してきた)仮定のもとで 6 倍する形で導出する
## (index [B3:PB3]=6 は標準事実。M・K^(27) 自体の B3-正規性は本 script では
## 独立に検証していない -- 明記のみ、cert に assumption として記帳)。

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");
Read("search/week3-psl-common.g");

t0Global := GAPLIB_WallElapsedMs();;
PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

## ================= 単一定義: ScanRoofHexagon(frattini_resolution_v2.g/ihnec_r4b_run.g と逐語同一) =================
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

BuildRegularPermGroupFromTable := function(tbl, n)
  local prod, e, gens, a, images, b;
  prod := List([0..n-1], i -> List([0..n-1], j -> -1));;
  for e in tbl do prod[e[1]+1][e[2]+1] := e[3]; od;;
  gens := [];;
  for a in [0..n-1] do
    images := List([0..n-1], b -> prod[a+1][b+1] + 1);;
    Add(gens, PermList(images));;
  od;
  return Group(gens);;
end;;

BuildShadowCompositionRegularRep := function(qrec, shadows, Nord)
  local n, i1, i2, m1, f1, m2, f2, u1, Ehom, newm, newf, idx, t, tbl, closureFail, regGrp,
        idxDict, key;
  n := Length(shadows);;
  tbl := [];;  closureFail := 0;;
  idxDict := NewDictionary([shadows[1].m, shadows[1].f], true);;
  for t in [1..n] do
    AddDictionary(idxDict, [shadows[t].m, shadows[t].f], t);;
  od;
  for i1 in [1..n] do
    m1 := shadows[i1].m;;  f1 := shadows[i1].f;;  u1 := 2*m1+1;;
    Ehom := GroupHomomorphismByImages(qrec.G, qrec.G, [qrec.x, qrec.y],
              [qrec.x^u1, AbstractProd([f1^-1, qrec.y^u1, f1])]);;
    if Ehom = fail then
      Error("BuildShadowCompositionRegularRep: E_{m1,f1} construction failed, i1=", i1);
    fi;
    for i2 in [1..n] do
      m2 := shadows[i2].m;;  f2 := shadows[i2].f;;
      newm := (2*m1*m2 + m1 + m2) mod Nord;;
      newf := AbstractProd([f1, Image(Ehom, f2)]);;
      key := [newm, newf];;
      idx := LookupDictionary(idxDict, key);;
      if idx = fail then
        closureFail := closureFail + 1;;
        Add(tbl, [i1-1, i2-1, -1]);;
      else
        Add(tbl, [i1-1, i2-1, idx-1]);;
      fi;
    od;
  od;
  if closureFail > 0 then
    return rec(regGrp:=fail, closed_observed:=false, closure_fail_count:=closureFail, shadow_total:=n);;
  fi;
  regGrp := BuildRegularPermGroupFromTable(tbl, n);;
  return rec(regGrp:=regGrp, closed_observed:=true, closure_fail_count:=0, shadow_total:=n);;
end;;

Print("############################################################\n");
Print("# d972_phase0_v1.g -- TRIAD-972 Phase 0 gating(裁定1127)\n");
Print("############################################################\n");

## ================= 窓1: K(9) ================= [0-1 material + anchor]
Print("\n=== 窓1: G9 = MakeGn(9) ===\n");
tA0 := GAPLIB_WallElapsedMs();;
g9 := MakeGn(9);;
K9sz := Size(g9.G);;
K9ord := Lcm(Order(g9.x), Order(g9.y));;
tA1 := GAPLIB_WallElapsedMs();;
Print("  |PB3/K9|=", K9sz, " (expect 2916)  K9_ord=", K9ord, " (expect 18)  time_ms=", tA1-tA0, "\n");
if K9sz <> 2916 or K9ord <> 18 then
  Error("d972_phase0: K9 window construction mismatch -- refusing to proceed");
fi;
K9charm := CharmingSetOf(K9ord);;
resK9 := ScanRoofHexagon(rec(x:=g9.x, y:=g9.y, G:=g9.G), K9charm);;
anchorK9OK := (resK9.shadow_total = 108);;
Print("[", PF(anchorK9OK), "] 自己検査アンカー: K9単体 shadow_total=108: ", anchorK9OK, "\n");
if not anchorK9OK then Error("d972_phase0: K9 anchor mismatch -- refusing to proceed"); fi;

## ================= 窓2: N_S4 = PSL(2,8) ================= [0-1 material + anchor]
Print("\n=== 窓2: P = PSL(2,8) (GF(8) 明示行列) ===\n");
tB0 := GAPLIB_WallElapsedMs();;
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
tB1 := GAPLIB_WallElapsedMs();;
Print("  |PB3/N_S4|=", Psz, " (expect 504)  N_S4_ord=", Pord, " (expect 9)  time_ms=", tB1-tB0, "\n");
if Psz <> 504 or Pord <> 9 then
  Error("d972_phase0: S4 window construction mismatch -- refusing to proceed");
fi;
S4charm := CharmingSetOf(Pord);;
resS4 := ScanRoofHexagon(rec(x:=Xperm, y:=Yperm, G:=Pgrp), S4charm);;
anchorS4OK := (resS4.shadow_total = 54);;
Print("[", PF(anchorS4OK), "] 自己検査アンカー: S4単体 shadow_total=54: ", anchorS4OK, "\n");
if not anchorS4OK then Error("d972_phase0: S4 anchor mismatch -- refusing to proceed"); fi;

## ================= [0-1] M := K^(9) cap N_S4 の |PB3/M|・|B3/M| =================
Print("\n=== [0-1] 窓 M := K^(9) cap N_S4(block-diagonal 直和埋め込み) ===\n");
tC0 := GAPLIB_WallElapsedMs();;
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
PB3overM := Size(GM);;
Mord := Lcm(Order(XM), Order(YM));;
tC1 := GAPLIB_WallElapsedMs();;
pb3overMOk := (PB3overM = 2916*504);;
mOrdOk := (Mord = 18);;
Print("  |PB3/M| = ", PB3overM, " (expect 1469664)  [", PF(pb3overMOk), "]  M_ord = ", Mord, " (expect 18)  [", PF(mOrdOk), "]  time_ms=", tC1-tC0, "\n");
if not (pb3overMOk and mOrdOk) then
  Error("d972_phase0: M window scale mismatch -- refusing to proceed");
fi;
## |B3/M| derivation: standard index multiplicativity [B3:PB3]=6, ASSUMING M normal in B3
## (not independently GAP-verified here; flagged in cert as an assumption, consistent with all
## prior certs in this codebase that only ever measure |PB3/.|).
B3overM_derived := 6 * PB3overM;;
Print("  |B3/M| (derived, assumption: M normal in B3) = ", B3overM_derived, "\n");

## ================= [0-3] |GT(M)| = 972 の実測 =================
Print("\n=== [0-3] GT(M) の全数走査 + shadow 合成による実群構成 ===\n");
Mcharm := CharmingSetOf(Mord);;
Print("  charming_set_M = ", Mcharm, " (|.|=", Length(Mcharm), ")\n");
tD0 := GAPLIB_WallElapsedMs();;
resM := ScanRoofHexagon(rec(x:=XM, y:=YM, G:=GM), Mcharm);;
tD1 := GAPLIB_WallElapsedMs();;
Print("  derived_order=", resM.derived_order, " candidate_total=", resM.candidate_total,
      " shadow_total=", resM.shadow_total, " (expect 972)  elapsed_ms=", tD1-tD0, "\n");
shadowTotalOk := (resM.shadow_total = 972);;
Print("[", PF(shadowTotalOk), "] shadow_total = 972: ", shadowTotalOk, "\n");
if not shadowTotalOk then
  Error("d972_phase0: M shadow_total <> 972 -- refusing to build GT(M) on an unexpected shadow set");
fi;

Print("  BuildShadowCompositionRegularRep(M, 972 shadows) 実行中...\n");
tE0 := GAPLIB_WallElapsedMs();;
regM := BuildShadowCompositionRegularRep(rec(x:=XM,y:=YM,G:=GM), resM.shadows, Mord);;
tE1 := GAPLIB_WallElapsedMs();;
Print("  closed_observed=", regM.closed_observed, " closure_fail_count=", regM.closure_fail_count,
      " elapsed_ms=", tE1-tE0, "\n");
gtMOrder := fail;;  gtMOrderOk := false;;
if regM.closed_observed then
  gtMOrder := Size(regM.regGrp);;
  gtMOrderOk := (gtMOrder = 972);;
  Print("[", PF(gtMOrderOk), "] |GT(M)| = ", gtMOrder, " (expect 972): ", gtMOrderOk, "\n");
else
  Print("[HALT] shadow 合成則が閉じていない -- |GT(M)| 実測不能\n");
fi;

## ================= [0-2] (H1) M isolated: #C(M)=1 =================
Print("\n=== [0-2] (H1) M isolated (#C(M)=1) -- 方法選定と可否判定 ===\n");
Print("  PN=GM の位数 = ", PB3overM, "\n");
Print("  marked-factor-map(AutomorphismGroup(PN))は位数1,469,664に対して\n");
Print("  裁定1117の教訓(|Q|=1176でメモリ死)から実行を見送る(fail-closed, RAM8GB制約)。\n");
Print("  well-definedness代替法はK(9)窓のフルB3生成元sigma1,sigma2を要求するが、\n");
Print("  既存資産に存在しない。scratchpad/try_sigma_k9.gでのblock-swap*block対角元\n");
Print("  ansatz探索(25候補)は全滅(D_9に位数4の元が存在しないため sigma1^2=x の\n");
Print("  block3成分=sで位数2元を要求する構成が原理的に不可能と機械確認)。\n");
Print("  [0-2] は本scriptではUNKNOWN(値なし)として記録し、司令塔へ疑問点として報告する。\n");
h1Status := "UNKNOWN";;
h1Method := "not_attempted";;
h1AutPnOrder := PB3overM;;

## ================= [0-4] K(27) gating(細分候補の規模) =================
Print("\n=== [0-4] K(27) gating(Phase 1 細分候補の gating 独立確認) ===\n");
tF0 := GAPLIB_WallElapsedMs();;
g27 := MakeGn(27);;
K27sz := Size(g27.G);;
K27ord := Lcm(Order(g27.x), Order(g27.y));;
tF1 := GAPLIB_WallElapsedMs();;
k27szOk := (K27sz = 78732);;
Print("  |PB3/K27| = ", K27sz, " (expect 78732)  [", PF(k27szOk), "]  K27_ord = ", K27ord, " (expect 54)  time_ms=", tF1-tF0, "\n");
if not k27szOk then
  Error("d972_phase0: K27 window scale mismatch -- refusing to proceed");
fi;
B3overK27_derived := 6 * K27sz;;
B3overK27_canon := 472392;;
b3overK27MatchesCanon := (B3overK27_derived = B3overK27_canon);;
Print("  |B3/K27| (derived, 6*|PB3/K27|, assumption: K27 normal in B3) = ", B3overK27_derived,
      "  matches 正本記載 472,392: ", b3overK27MatchesCanon, "\n");

Print("  K27単体 GT(K27) 全数走査(Thm4.3の isolated 性は正典既証明・PN 単独走査で shadow_total=|GT(K27)|)...\n");
K27charm := CharmingSetOf(K27ord);;
tG0 := GAPLIB_WallElapsedMs();;
resK27 := ScanRoofHexagon(rec(x:=g27.x, y:=g27.y, G:=g27.G), K27charm);;
tG1 := GAPLIB_WallElapsedMs();;
gtK27Ok := (resK27.shadow_total = 972);;
Print("  candidate_total=", resK27.candidate_total, " shadow_total=", resK27.shadow_total,
      " (expect 972 = 2*27*phi(27), Thm4.3)  [", PF(gtK27Ok), "]  elapsed_ms=", tG1-tG0, "\n");

Print("\n=== [0-4] K27 subseteq K9 (Prop 3.5) の直接比較 ===\n");
tH0 := GAPLIB_WallElapsedMs();;
hom27to9 := GroupHomomorphismByImages(g27.G, g9.G, [g27.x, g27.y], [g9.x, g9.y]);;
hom9to27 := GroupHomomorphismByImages(g9.G, g27.G, [g9.x, g9.y], [g27.x, g27.y]);;
tH1 := GAPLIB_WallElapsedMs();;
k27subK9 := (hom27to9 <> fail);;
k9subK27 := (hom9to27 <> fail);;
k27subK9ImgOk := false;;
if k27subK9 then
  k27subK9ImgOk := (Size(Image(hom27to9)) = K9sz);;
fi;
Print("  K27->K9 準同型が well-defined (K27 subseteq K9) = ", k27subK9,
      "  像の位数=|PB3/K9|一致=", k27subK9ImgOk, "  逆向き well-defined = ", k9subK27,
      "  time_ms=", tH1-tH0, "\n");
prop35Ok := k27subK9 and k27subK9ImgOk and (not k9subK27);;
Print("[", PF(prop35Ok), "] Prop 3.5 (K27 subsetneq K9・9|lcm(27,2)=54) 機械確認: ", prop35Ok, "\n");

## ---- Phase 1 の規模見積り(K := K^(27) cap N_S4)、算術のみ・GAP構成はしない ----
Print("\n=== Phase 1 規模見積り(K := K^(27) cap N_S4, 算術積のみ・未構成) ===\n");
pb3overK_estimate := K27sz * Psz;;
b3overK_estimate := 6 * pb3overK_estimate;;
Print("  |PB3/K| 見積り(算術積 78732*504) = ", pb3overK_estimate, " (未 GAP 構成)\n");
Print("  |B3/K| 見積り(算術積 x6)          = ", b3overK_estimate, " (未 GAP 構成)\n");

t1Global := GAPLIB_WallElapsedMs();;
Print("\n総経過 = ", t1Global - t0Global, " ms\n");

## ================= JSON 出力 =================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_d972p0.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/d972_phase0_v1.g");;

gtMOrderStr := "null";;
if gtMOrder <> fail then gtMOrderStr := String(gtMOrder); fi;

cert := Concatenation(
  "{\"schema\":\"d972_gating/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/d972_phase0_v1.g\",\"order\":\"裁定1127(TRIAD-972 genuine/fake大戦 Phase0・gating必須)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"spec_ref\":\"docs/notes/triad972_grade_and_battle_plan_v1.md §6 Phase0(D972-0)\"",
  ",\"anchors\":{\"k9_alone_shadow_total\":", String(resK9.shadow_total), ",\"k9_alone_expected\":108,\"k9_alone_pass\":", JB(anchorK9OK),
    ",\"s4_alone_shadow_total\":", String(resS4.shadow_total), ",\"s4_alone_expected\":54,\"s4_alone_pass\":", JB(anchorS4OK), "},",
  "\"d972_0_1\":{\"pb3_over_m\":", String(PB3overM), ",\"pb3_over_m_expected\":", String(2916*504), ",\"pb3_over_m_pass\":", JB(pb3overMOk),
    ",\"m_ord\":", String(Mord), ",\"m_ord_expected\":18,\"m_ord_pass\":", JB(mOrdOk),
    ",\"b3_over_m_derived\":", String(B3overM_derived),
    ",\"b3_over_m_derivation_note\":\"6 * |PB3/M|, assumes M normal in B3 (index [B3:PB3]=6 standard; M's B3-normality NOT independently GAP-verified in this script)\"},",
  "\"d972_0_2\":{\"status\":\"", h1Status, "\",\"method\":\"", h1Method, "\"",
    ",\"pn_order\":", String(h1AutPnOrder),
    ",\"blocker_note\":\"marked-factor-map requires AutomorphismGroup(PN) with |PN|=1469664 (1249x the |Q|=1176 that caused a memory death per LEDGER 裁定1117) -- not attempted, fail-closed per RAM 8GB constraint. The 裁定1117 well-definedness alternative requires full-B3 generators sigma1,sigma2 for the K(9)-window (MakeGn only exposes x=sigma1^2,y=sigma2^2 directly by formula, not sigma1,sigma2 themselves) which do not exist in reusable codebase assets. A block-swap-times-block-diagonal ansatz for sigma1 was machine-searched (scratchpad/try_sigma_k9.g, 25 candidates: sigma1 in {tau12*w1 tau23*w2}x2x{tr(s,3),tr(r,3),id}-style variants) and found impossible in principle: D_9 has no order-4 elements (orders present: 1,2,3,6,9,18), so no candidate can satisfy sigma1^2 = x's order-2 block-3 factor (s) via this family. Escalated to commander (speedy route) rather than guessing a literature-derived sigma1,sigma2 formula.\",",
    "\"value\":null},",
  "\"d972_0_3\":{\"shadow_total\":", String(resM.shadow_total), ",\"shadow_total_expected\":972,\"shadow_total_pass\":", JB(shadowTotalOk),
    ",\"closed_observed\":", JB(regM.closed_observed), ",\"closure_fail_count\":", String(regM.closure_fail_count),
    ",\"gt_m_order\":", gtMOrderStr, ",\"gt_m_order_expected\":972,\"gt_m_order_pass\":", JB(gtMOrderOk), "},",
  "\"d972_0_4\":{",
    "\"pb3_over_k27\":", String(K27sz), ",\"pb3_over_k27_expected\":78732,\"pb3_over_k27_pass\":", JB(k27szOk), ",",
    "\"k27_ord\":", String(K27ord), ",\"k27_ord_expected\":54,",
    "\"b3_over_k27_derived\":", String(B3overK27_derived), ",\"b3_over_k27_canon_value\":", String(B3overK27_canon),
      ",\"b3_over_k27_matches_canon\":", JB(b3overK27MatchesCanon), ",",
    "\"gt_k27_alone_shadow_total\":", String(resK27.shadow_total), ",\"gt_k27_expected_thm43\":972,\"gt_k27_pass\":", JB(gtK27Ok), ",",
    "\"prop35_k27_subsetneq_k9\":{\"k27_sub_k9_hom_well_defined\":", JB(k27subK9),
      ",\"k27_sub_k9_image_order_matches_pb3_over_k9\":", JB(k27subK9ImgOk),
      ",\"k9_sub_k27_hom_well_defined\":", JB(k9subK27), ",\"prop35_pass\":", JB(prop35Ok), "},",
    "\"phase1_k_estimate\":{\"note\":\"K := K^(27) cap N_S4, arithmetic product estimate only, NOT GAP-constructed (out of Phase0 scope, feasibility sizing only)\",",
      "\"pb3_over_k_estimate\":", String(pb3overK_estimate), ",\"b3_over_k_estimate\":", String(b3overK_estimate), "}",
  "},",
  "\"u_touched\":false,\"c_touched\":false,\"prereg_quantities_untouched\":true",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(t1Global - t0Global),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/d972_phase0_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
