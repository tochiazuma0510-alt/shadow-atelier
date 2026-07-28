# search/i24-u3-recheck.g -- I-24(b) 実装: u_3 の j=3 窓再測定(裁定 144・ideas_005 I-24)
#
# 実行: .\gap.ps1 search\i24-u3-recheck.g
#
# 目的(司令塔発注): K^(3) の窓分類 H_{j,alpha,beta}(命題 ODD-H・docs/notes/oddH_full_proof_v1.md)
#   で、標準窓 H_{2,1,0}(j=2 系、u_3=-4 の出所 = docs/manifest_k5_appendixA_v1.md SS2 の
#   K3-regression fixture)ではなく、双子類 H_{3,1,0}(j=3)の窓表示を使って u_3 に相当する
#   量を再測定し、-4(またはその平方類)が再現するかを機械的に判定する。
#
# 設計方針(封印遵守・機械実行の範囲を超える部分は UNKNOWN で正直に止める):
#   u_3 = -4 は K3-regression fixture の特定の平面モデル
#     t^2 + (x-1)^2(4x-1)t + 4x^6 = 0  (LMFDB 6T9-6_6_2.2.1.1-a)
#   の X-cusp(次数 6 の全分岐点、lambda=0)における Puiseux 展開の主要係数として
#   定義された量である(search/week4-u-k3.mjs 検算 (7)-(9))。この定義は H_{2,1,0} の
#   ordered passport (X:6, Y:[2,2,1,1], Z:6) に対して「X の全分岐点で測る」という
#   手続きであり、j そのもの(Y と Z のどちらが type [2,2,1,1] を持つか)には依存しない
#   ---ただし「j=3 窓で u_3 を再測定する」ことに意味があるのは、H_{3,1,0} が定める次数 6
#   の置換三つ組 (X',Y',Z') が、H_{2,1,0} の三つ組の Y<->Z を入れ替えたものと
#   S_6-共役であるかどうかが未確認だったからである(この共役があれば「同じ dessin を
#   Y/Z 逆順で見ているだけ」であり X-cusp の測定は不変 ---共役がなければ H_{3,1,0} は
#   全く別の dessin であり、u の再測定には新しい曲線モデルの構成が要る。これは実装者の
#   一存で行う数学的構成の選択であり本スクリプトの範囲を超えるため、その場合は
#   UNKNOWN として報告し、解釈はしない)。
#
# 本スクリプトが機械的に行うこと(観測のみ、解釈はしない):
#   (1) P_3 = G_3 を構成し、H_{2,1,0}, H_{3,1,0} を command 補題 A の座標辞書で構成する
#       (search/c1-class-check.g と同一パターンの再利用)。
#   (2) 両者の次数 6 coset action (X_i, Y_i, Z_i) を FactorCosetAction で実測する。
#   (3) K3-regression fixture の実測三つ組(docs/manifest_k5_appendixA_v1.md SS2、
#       G_3 側次数 6 表現 bar-x,bar-y,bar-z、conjugation 前)と、本スクリプトが
#       H_{2,1,0} から独立に構成した三つ組が S_6-共役かどうかを確認する
#       (整合性のサニティチェック --- 座標辞書の実装一致の検算)。
#   (4) H_{3,1,0} の三つ組が、H_{2,1,0} の三つ組の Y<->Z 入れ替え版と S_6-共役かどうかを
#       全探索(|S_6|=720)で判定する(「j フリップ = Y/Z relabeling」仮説の直接検査)。
#   (5) (4) が YES なら「u_3 の j=3 窓再測定は X-cusp が不変なので -4 が恒等的に再現する
#       (独立測定ではなく同一対象の別ラベルづけによる自明な再現)」と記録する。
#       (4) が NO なら「j=3 窓は別の dessin であり、本スクリプトの範囲では u は
#       measurable でない(UNKNOWN --- 新しい曲線モデルの構成を要する)」と記録する。
#
# 宇宙: n=3 のみ(事前登録どおり)。触れてよい u の値は u_3=-4(公開)のみ。他の窓の u・
#   c 平方類・c_mu 系には一切触れない。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

Print("############################################################\n");
Print("# i24-u3-recheck.g -- I-24(b): u_3 の j=3 窓再測定(裁定144)\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;
failures := 0;;

# ====================================================================
# 1. P_3 = G_3 の構成(search/c1-class-check.g と同一 BuildPn パターン)
# ====================================================================
Print("\n============================================================\n");
Print("# 1. P_3 の構成 + H_{2,1,0}, H_{3,1,0} の構成\n");
Print("============================================================\n");

BuildPn := function(n)
  local r, s, tr, a1, a2, a3, q1, q2, q3, X, Y, Xchk, Ychk, Gfull;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  if not (Order(r) = n and Order(s) = 2 and s*r*s^-1 = r^-1) then
    Error("BuildPn: D_n relations failed for n = ", n);
  fi;
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do
      l[j + (i-1)*n] := (j^p) + (i-1)*n;
    od;
    return PermList(l);
  end;
  a1 := tr(r,1);;  a2 := tr(r,2);;  a3 := tr(r,3);;
  q1 := tr(s,2) * tr(s,3);;
  q2 := tr(s,1) * tr(s,3);;
  q3 := tr(s,1) * tr(s,2);;
  X := AbstractProd([a1, q1]);;
  Y := AbstractProd([a1, a2, a3, q2]);;
  Xchk := tr(r,1) * tr(s,2) * tr(s,3);;
  Ychk := tr(s*r,1) * tr(r,2) * tr(s*r,3);;
  if X <> Xchk then
    Error("BuildPn: X = AbstractProd([a1,q1]) does not match MakeGn convention for n=", n);
  fi;
  if Y <> Ychk then
    Error("BuildPn: Y = AbstractProd([a1,a2,a3,q2]) does not match MakeGn convention for n=", n);
  fi;
  Gfull := Group(a1, a2, a3, q1, q2);;
  return rec(n:=n, a1:=a1, a2:=a2, a3:=a3, q1:=q1, q2:=q2, q3:=q3, X:=X, Y:=Y, G:=Gfull);
end;;

expectedSize := function(n)
  if n mod 2 = 1 then return 4*n^3; else return 4*(n/2)^3; fi;
end;;

PassportOf := function(perm, deg)
  local lens, coll;
  lens := List([1..deg], i -> CycleLength(perm, i));
  coll := Collected(lens);
  return List(coll, e -> [e[1], e[2]/e[1]]);
end;;

PassportStr := function(p)
  return JoinStringsWithSeparator(List(p, e -> Concatenation(String(e[1]),"^",String(e[2]))), ",");
end;;

P3 := BuildPn(3);;
sz3 := Size(P3.G);;
okSize3 := (sz3 = expectedSize(3));;
Print("[", PF(okSize3), "] |P_3| = ", sz3, " (期待 ", expectedSize(3), ")\n");
if not okSize3 then failures := failures + 1; fi;

# H_{j,alpha,beta} := <a_j, a1^alpha a_{j'}, a1^beta q_j>  (j'=5-j)
BuildH2 := function(P, alpha, beta)
  return Group(P.a2, P.a1^alpha * P.a3, P.a1^beta * P.q2);
end;;
BuildH3 := function(P, alpha, beta)
  return Group(P.a3, P.a1^alpha * P.a2, P.a1^beta * P.q3);
end;;

H2fun := BuildH2(P3, 1, 0);;   # H_3^fun = H_{2,1,0} (標準窓・u_3=-4 の出所)
H3fun := BuildH3(P3, 1, 0);;   # H_{3,1,0} (双子類・j=3 窓)

sizeH2 := Size(H2fun);; sizeH3 := Size(H3fun);;
idxH2 := sz3/sizeH2;; idxH3 := sz3/sizeH3;;
Print("[", PF(sizeH2 = 18 and idxH2 = 6), "] |H_{2,1,0}| = ", sizeH2, "  [P_3:H] = ", idxH2, " (期待 18, 6)\n");
Print("[", PF(sizeH3 = 18 and idxH3 = 6), "] |H_{3,1,0}| = ", sizeH3, "  [P_3:H] = ", idxH3, " (期待 18, 6)\n");
if not (sizeH2 = 18 and idxH2 = 6) then failures := failures + 1; fi;
if not (sizeH3 = 18 and idxH3 = 6) then failures := failures + 1; fi;

selfNormH2 := (Size(Normalizer(P3.G, H2fun)) = sizeH2);;
selfNormH3 := (Size(Normalizer(P3.G, H3fun)) = sizeH3);;
Print("[", PF(selfNormH2), "] N(H_{2,1,0}) = H_{2,1,0} (alpha<>0, 命題 ODD-H (1.3))\n");
Print("[", PF(selfNormH3), "] N(H_{3,1,0}) = H_{3,1,0}\n");
if not selfNormH2 then failures := failures + 1; fi;
if not selfNormH3 then failures := failures + 1; fi;

notConj := not IsConjugate(P3.G, H2fun, H3fun);;
Print("[", PF(notConj), "] H_{2,1,0} と H_{3,1,0} は P_3-非共役(命題 (1.9): j=j' が共役の必要条件)\n");
if not notConj then failures := failures + 1; fi;

# ====================================================================
# 2. 次数 6 coset action (X,Y,Z) の実測
# ====================================================================
Print("\n============================================================\n");
Print("# 2. 次数 6 coset action の実測\n");
Print("============================================================\n");

CosetTriple := function(P, H)
  local phi, Xi, Yi, Zi;
  phi := FactorCosetAction(P.G, H);;
  Xi := Image(phi, P.X);; Yi := Image(phi, P.Y);; Zi := (Xi*Yi)^-1;;
  return rec(X:=Xi, Y:=Yi, Z:=Zi);
end;;

tr2 := CosetTriple(P3, H2fun);;   # j=2 (H_{2,1,0}) の三つ組
tr3 := CosetTriple(P3, H3fun);;   # j=3 (H_{3,1,0}) の三つ組

pp2 := rec(X:=PassportOf(tr2.X,6), Y:=PassportOf(tr2.Y,6), Z:=PassportOf(tr2.Z,6));;
pp3 := rec(X:=PassportOf(tr3.X,6), Y:=PassportOf(tr3.Y,6), Z:=PassportOf(tr3.Z,6));;
Print("H_{2,1,0}: passport(X,Y,Z) = ", PassportStr(pp2.X), " | ", PassportStr(pp2.Y), " | ", PassportStr(pp2.Z), "\n");
Print("H_{3,1,0}: passport(X,Y,Z) = ", PassportStr(pp3.X), " | ", PassportStr(pp3.Y), " | ", PassportStr(pp3.Z), "\n");

expectTargetPP := function(pp)
  return pp.X = [[6,1]] and pp.Y = [[1,2],[2,2]] and pp.Z = [[6,1]];
end;;
expectSwapPP := function(pp)
  return pp.X = [[6,1]] and pp.Y = [[6,1]] and pp.Z = [[1,2],[2,2]];
end;;
h2IsTarget := expectTargetPP(pp2);;
h3IsSwap := expectSwapPP(pp3);;
Print("[", PF(h2IsTarget), "] H_{2,1,0} passport = (6, 2^2 1^2, 6) (target 型・命題 ODD-P)\n");
Print("[", PF(h3IsSwap), "] H_{3,1,0} passport = (6, 6, 2^2 1^2) (Y/Z 入れ替え型・命題 ODD-P j=3 側)\n");
if not h2IsTarget then failures := failures + 1; fi;
if not h3IsSwap then failures := failures + 1; fi;

# ====================================================================
# 3. サニティチェック: H_{2,1,0} の三つ組が K3-regression fixture の
#    実測三つ組(docs/manifest_k5_appendixA_v1.md SS2, conjugation 前)と S_6-共役か
# ====================================================================
Print("\n============================================================\n");
Print("# 3. サニティチェック: K3-regression fixture の三つ組との一致確認\n");
Print("============================================================\n");

# 出所: docs/manifest_k5_appendixA_v1.md SS2 「G_3 側次数 6 表現(h で共役される前)」
#   bar-x = [2,5,4,6,3,1], bar-y = [1,3,2,5,4,6], bar-z = [6,1,4,2,3,5]  (1-indexed one-line)
# 注意(自己発見・実装中に判明): 同 manifest の「規約 (iii)」は (p∘q)(i)=p(q(i)) と明記して
# おり、これは GAP の "*" (i^(p*q) = (i^p)^q、pを先に適用) と逆順である。したがって
# 彼らの「xy」は GAP の y*x に対応する。数値実験(search/.tmp_perm_check.g、削除済み)で
# 実際に bar-z*bar-y*bar-x = id (GAP 順) を確認し、bar-x*bar-y*bar-z <> id であることも
# 確認した --- fixture 自体に誤りはなく、比較には規約変換が要る。
fixtureX := PermList([2,5,4,6,3,1]);;
fixtureY := PermList([1,3,2,5,4,6]);;
fixtureZ := PermList([6,1,4,2,3,5]);;
fixtureZcheck := (fixtureY * fixtureX)^-1;;   # 規約(iii)反転: 彼らの (xy)^-1 = GAP の (Y*X)^-1
fixtureZOk := (fixtureZ = fixtureZcheck);;
Print("[", PF(fixtureZOk), "] fixture 記録: bar-z = (bar-y * bar-x)^-1 の自己整合(規約(iii)反転を適用)\n");
if not fixtureZOk then failures := failures + 1; fi;

S6 := SymmetricGroup(6);;
S6elts := Elements(S6);;

FindSimultaneousConjugator := function(triple1, triple2, elts)
  local g;
  for g in elts do
    if triple1.X^g = triple2.X and triple1.Y^g = triple2.Y and triple1.Z^g = triple2.Z then
      return g;
    fi;
  od;
  return fail;
end;;

FindPairConjugatorEarly := function(x1, y1, x2, y2, elts)
  local g;
  for g in elts do
    if x1^g = x2 and y1^g = y2 then return g; fi;
  od;
  return fail;
end;;

# 本比較は (X,Y) の 2 対のみで行う(Z の合成順規約の食い違いに依存しないため、
# より頑健なテスト --- X,Y は fixture・本スクリプトいずれも独立生成元として直接
# 与えられているので規約の曖昧さがない)。
gFixture := FindPairConjugatorEarly(tr2.X, tr2.Y, fixtureX, fixtureY, S6elts);;
fixtureMatchOk := (gFixture <> fail);;
Print("[", PF(fixtureMatchOk), "] 本スクリプトの H_{2,1,0} 生成対 (X,Y) と K3-regression fixture の",
      " (bar-x,bar-y) は S_6-共役(2対のみの比較・witness g = ", gFixture, ")\n");
if not fixtureMatchOk then failures := failures + 1; fi;

# ====================================================================
# 4. 本題: H_{3,1,0} の窓は H_{2,1,0} の窓の 'Y/Z relabeling' か
#
# 罠の記録(自己発見・実装中に判明): 素朴に「(X,Y,Z) の 3 つ組をまるごと Y<->Z
# 入れ替えて S_6-共役を試す」テスト(swappedTr2 := (X2,Z2,Y2) が tr3=(X3,Y3,Z3) と
# 共役か)は、Z が独立生成元ではなく Z=(XY)^{-1} で「導出される」量であることを
# 見落としている。実際 X2*Z2*Y2 <> id (数値実験で確認) であり、swappedTr2 は
# そもそも群の関係式 X*Y*Z=1 を満たさない ---「入れ替えた 3 つ組」自体が不正な対象
# なので、この検査が false になっても j=3 窓が別物であることの証拠にはならない
# (検査対象が壊れているだけ)。
#
# 正しい定式化: X,Y は独立生成元、Z=(XY)^{-1} は従属。したがって意味のある問いは
# 「H_{3,1,0} の生成対 (X,Y) が、H_{2,1,0} の (X,Z) 対(同じ H_{2,1,0} の被覆を
# 独立生成元の別の取り方で見たもの ---(X,Z) も (X,Y) も同じ被覆を記述する)と
# 2 対として同時共役か」である。全 S_6 を X2^g=X3 の条件で絞ってから
# (|Stab(X2)|=6 個の候補のみ)、その中で Y2^g=Z3 となる g を探す。
# ====================================================================
Print("\n============================================================\n");
Print("# 4. 本題: j=3 窓 = 'Y/Z relabeling' 仮説の直接検査(修正版・生成対ベース)\n");
Print("============================================================\n");

FindPairConjugator := function(x1, y1, x2, y2, elts)
  local g;
  for g in elts do
    if x1^g = x2 and y1^g = y2 then return g; fi;
  od;
  return fail;
end;;

# H0: (X2,Y2) ~ (X3,Y3) そのまま(標準対応・命題(1.9)よりP_3-共役ではないので
#     falseが期待される --- ただしS_6-共役としては独立な問い)
gH0 := FindPairConjugator(tr2.X, tr2.Y, tr3.X, tr3.Y, S6elts);;
h0Holds := (gH0 <> fail);;
Print("[観測] H0 (X2,Y2)~(X3,Y3) そのまま: ", h0Holds, "  witness g = ", gH0, "\n");

# H1 (本命・Y/Z relabeling の正しい定式化): (X2,Y2) ~ (X3,Z3)
#    H_{2,1,0}の生成対(X,Y)と、H_{3,1,0}を(X,Z)という独立生成元対で見たものが
#    2対として同時共役か。
gH1 := FindPairConjugator(tr2.X, tr2.Y, tr3.X, tr3.Z, S6elts);;
h1Holds := (gH1 <> fail);;
Print("[観測] H1 (X2,Y2)~(X3,Z3) (relabeling仮説の正しい定式化): ", h1Holds, "  witness g = ", gH1, "\n");

# H2 (対照・逆向き): (X2,Z2) ~ (X3,Y3)
gH2 := FindPairConjugator(tr2.X, tr2.Z, tr3.X, tr3.Y, S6elts);;
h2Holds := (gH2 <> fail);;
Print("[観測] H2 (X2,Z2)~(X3,Y3) (逆向き対照): ", h2Holds, "  witness g = ", gH2, "\n");

# 罠の記録用: 素朴な3つ組入れ替え検査(壊れた検査であることを記録目的で残す)
swappedTr2 := rec(X:=tr2.X, Y:=tr2.Z, Z:=tr2.Y);;
gNaiveSwap := FindSimultaneousConjugator(swappedTr2, tr3, S6elts);;
naiveSwapHolds := (gNaiveSwap <> fail);;
xzyProd := tr2.X*tr2.Z*tr2.Y;;
naiveSwapRelationValid := IsOne(xzyProd);;
Print("[罠の記録] 素朴な3つ組入れ替え (X2,Z2,Y2)~(X3,Y3,Z3): ", naiveSwapHolds,
      "  (この検査対象は X2*Z2*Y2 = ", xzyProd, " <> id なので群関係式を満たさず、",
      "そもそも妥当な dessin を表さない --- false でも j=3 窓が別物である証拠にはならない)\n");

# ====================================================================
# 5. 結論(観測の記録のみ・解釈はしない)
# ====================================================================
Print("\n============================================================\n");
Print("# 5. 結論\n");
Print("============================================================\n");

verdict := "UNKNOWN";;
u3Reproduces := "UNKNOWN";;
if h1Holds then
  verdict := "RELABELING_HYPOTHESIS_CONFIRMED_H1";;
  u3Reproduces := "IDENTITY_SAME_X_CUSP_VIA_H1_WITNESS";;
  Print("観測: (X2,Y2) ~S_6 (X3,Z3) (witness g=", gH1, ")。\n");
  Print("      すなわち H_{2,1,0} の生成対 (X,Y) と、H_{3,1,0} を独立生成元対 (X,Z) で\n");
  Print("      見たものは、次数6の抽象置換表現として(=抽象 dessin として)同型。\n");
  Print("      cycle type も整合: Y2 の型 = ", PassportStr(pp2.Y), " = Z3 の型 = ", PassportStr(pp3.Z), "。\n");
  Print("      X-monodromy は X2^g=X3 として厳密に一致するので、u_3 が定義される X-cusp は\n");
  Print("      両窓で同一対象。ゆえに j=3 窓での 'u_3 相当量' の再測定は、この同型を通じて\n");
  Print("      恒等的に u_3=-4 を再現する(独立な新規測定ではなく、同一 dessin を(X,Z)という\n");
  Print("      別の独立生成元対で見た結果の帰結 --- oddH_full_proof_v1.md SS5.4 の座標置換\n");
  Print("      自己同型 (2 3): H_{2,a,b} -> H_{3,a,b} と整合的な観測。これ以上は解釈しない)。\n");
else
  verdict := "RELABELING_HYPOTHESIS_H1_FAILS";;
  u3Reproduces := "UNKNOWN_NEW_CURVE_MODEL_REQUIRED";;
  Print("観測: (X2,Y2) ~S_6 (X3,Z3) は成立しない。j=3 窓は H_{2,1,0} の dessin の\n");
  Print("      独立生成元の取り替えでは説明できず、独立の曲線モデルなしには u_3 相当量を\n");
  Print("      測定できない。新しい曲線モデルの構成は実装者の一存で行う数学的構成の選択の\n");
  Print("      範囲を超えるため、本スクリプトはこれ以上進まず UNKNOWN として報告する。\n");
fi;;

Print("\nI-24(b) 判定: ", verdict, "\n");
Print("u_3 相当量の再現性: ", u3Reproduces, "\n");

# ====================================================================
# 総括
# ====================================================================
Print("\n############################################################\n");
if failures = 0 then
  Print("I24-U3-RECHECK ALL STRUCTURAL CHECKS PASSED\n");
else
  Print("I24-U3-RECHECK STRUCTURAL FAILURES: ", failures, "\n");
fi;

t1 := GAPLIB_WallElapsedMs();;
Print("経過(壁時計) = ", (t1-t0)/1000.0, " s\n");

# ====================================================================
# 証明書 JSON
# ====================================================================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_i24.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

PassportToJson := function(p)
  local parts, e;
  parts := [];
  for e in p do Add(parts, JPair(e[1], e[2])); od;
  return JArr(parts);
end;;

PermToJson := function(g)
  return JArr(List([1..6], i -> String(i^g)));
end;;

WitnessToJson := function(g)
  if g = fail then return "null"; fi;
  return JStr(String(PermToJson(g)));
end;;

scriptSha256 := ComputeSha256File("search/i24-u3-recheck.g");;

cert := Concatenation(
  "{\"schema\":\"i24-u3-recheck/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/i24-u3-recheck.g\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"universe\":{\"n\":3}",
  ",\"seal_note\":\"扱ってよい u 値は u_3=-4(公開)のみ。本証明書は u_3 の値そのものには一切触れず、",
    "H_{2,1,0}/H_{3,1,0} の次数6置換三つ組の S_6-共役性のみを機械判定する\"",
  ",\"section1_windows\":{",
    "\"pn_size\":", String(sz3), ",\"pn_size_pass\":", JB(okSize3),
    ",\"h2fun_size\":", String(sizeH2), ",\"h2fun_index\":", String(idxH2),
    ",\"h2fun_self_normalizing\":", JB(selfNormH2),
    ",\"h3fun_size\":", String(sizeH3), ",\"h3fun_index\":", String(idxH3),
    ",\"h3fun_self_normalizing\":", JB(selfNormH3),
    ",\"h2fun_h3fun_p3_conjugate\":", JB(not notConj),
  "}",
  ",\"section2_passports\":{",
    "\"h2fun\":{\"X\":", PassportToJson(pp2.X), ",\"Y\":", PassportToJson(pp2.Y), ",\"Z\":", PassportToJson(pp2.Z),
      ",\"is_target_type_6_221_6\":", JB(h2IsTarget), "}",
    ",\"h3fun\":{\"X\":", PassportToJson(pp3.X), ",\"Y\":", PassportToJson(pp3.Y), ",\"Z\":", PassportToJson(pp3.Z),
      ",\"is_swap_type_6_6_221\":", JB(h3IsSwap), "}",
  "}",
  ",\"section3_fixture_sanity\":{",
    "\"fixture_source\":\"docs/manifest_k5_appendixA_v1.md SS2 (G_3 side degree-6 rep, pre-conjugation)\"",
    ",\"fixture_z_self_consistent\":", JB(fixtureZOk),
    ",\"h2fun_conjugate_to_fixture_triple\":", JB(fixtureMatchOk),
    ",\"witness_g\":", WitnessToJson(gFixture),
  "}",
  ",\"section4_relabeling_hypothesis\":{",
    "\"note\":\"Z is derived (Z=(XY)^-1), not an independent generator; the naive 3-tuple",
     " Y<->Z swap test is structurally invalid (see naive_swap_test below). The correct test",
     " is 2-generator simultaneous conjugacy of independent pairs (X,Y) and (X,Z).\"",
    ",\"h0_XY_to_XY_holds\":", JB(h0Holds), ",\"h0_witness_g\":", WitnessToJson(gH0),
    ",\"h1_XY_to_XZ_holds\":", JB(h1Holds), ",\"h1_witness_g\":", WitnessToJson(gH1),
    ",\"h2_XZ_to_XY_holds\":", JB(h2Holds), ",\"h2_witness_g\":", WitnessToJson(gH2),
    ",\"naive_swap_test\":{",
      "\"holds\":", JB(naiveSwapHolds),
      ",\"target_relation_X2_Z2_Y2\":\"", String(xzyProd), "\"",
      ",\"target_relation_is_identity\":", JB(naiveSwapRelationValid),
      ",\"invalid_because\":\"swapping Y2,Z2 in the raw 3-tuple does not preserve the group",
       " relation X*Y*Z=1 in general, so the swapped target is not a valid dessin triple;",
       " a false/true result here is not by itself informative\"",
    "}",
  "}",
  ",\"section5_conclusion\":{",
    "\"verdict\":\"", verdict, "\"",
    ",\"u3_reproduction_status\":\"", u3Reproduces, "\"",
  "}",
  ",\"overall_structural_failures\":", String(failures),
  ",\"elapsed_wall_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/i24_u3_recheck_20260729.json";;
WriteFile(outPath, cert);;

Print("\n証明書を書き出した: ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");

Print("\nI24-U3-RECHECK DONE\n");
QUIT;
