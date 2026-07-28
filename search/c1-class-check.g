# search/c1-class-check.g -- 予測 T63-P1(裁定 106)caveat C1 の機械決定
#
# 実行: .\gap.ps1 search\c1-class-check.g
#
# 目的: K^(3) の実測窓(u_3 = -4 の出所、docs/manifest_k5_appendixA_v1.md SS2
#   「K3 regression fixture」)が sol_reply_73_math.md Q1.2 の分類 H_{j,alpha,beta}
#   のどの (j,[alpha]) 類に属するかを機械決定する。n=3 では
#   [alpha] in ((Z/3)\{0})/{+-1} = {[1]} の一類のみなので、閉じるべき問いは
#   「j=2 か j=3 か」(=測定窓が H_3^fun=H_{2,1,0} と P_3-共役か)に帰着する
#   (docs/notes/t63_reconnaissance_v1.md caveat C1、司令塔発注のコメント参照)。
#
# 正典・記録:
#   sol/sol_reply_73_math.md Q1.1(座標表 a_i/q_i)・Q1.2((1.2) H_{j,alpha,beta} の定義)・
#     Q1.3((1.9)(1.10) P_n-共役の判定)・Q6.1((6.1) H_n^fun = H_{2,1,0})
#   docs/manifest_k5_appendixA_v1.md SS2 -- K3 regression fixture: lambda 割当
#     (X->0 型[6], Y->1 型[2,2,1,1], Z->infty 型[6])・u_3=-4 の出所
#   search/week4-k3-v2-repairs.mjs (T3 節、"target" = ordered passport
#     (tX=6, tY=2.2.1.1, tZ=6) を満たす self-normalizing 部分群 6 個) -- 測定窓の
#     P_3-共役類の定義そのもの(次数 6 coset 表現でのフィルタ条件を引用)
#   search/k9-package.g -- BuildPn(n) の a_i/q_i 構成(AbstractProd の積順序罠に
#     注意、コメント参照)。本スクリプトは同じ BuildPn パターンを n=3 に適用する。
#
# 積順序の罠(k9-package.g のコメントを踏襲): 論文の抽象語 "a1 q1" 等を GAP で
#   素朴に左から右へ掛けると、a_i と q_j が同じブロックを共有する場合に paper/GAP
#   語規約の反転が効く。AbstractProd (week3-battery-common.g) を使い、
#   MakeGn 慣例(x = tr(r,1)*tr(s,2)*tr(s,3) 等)との一致を Error で保証する。
#
# 宇宙: n=3 のみ(発注書の事前登録どおり)。u の値には u_3=-4(開示済み)以外
#   触れない。解釈はしない(観測の記録に徹する)。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

Print("############################################################\n");
Print("# c1-class-check.g -- C1 caveat: K^(3) 実測窓の (j,[alpha]) 類の機械決定\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;
failures := 0;;

# ====================================================================
# BuildPn(n) -- k9-package.g と同一パターン(n=3 用)
# ====================================================================
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

# 完全な cycle passport (長さ, 個数) の昇順リスト
PassportOf := function(perm, deg)
  local lens, coll;
  lens := List([1..deg], i -> CycleLength(perm, i));
  coll := Collected(lens);
  return List(coll, e -> [e[1], e[2]/e[1]]);
end;;

PassportStr := function(p)
  return JoinStringsWithSeparator(List(p, e -> Concatenation(String(e[1]),"^",String(e[2]))), ",");
end;;

# ====================================================================
# 1. P_3 = G_3 の構成
# ====================================================================
Print("\n============================================================\n");
Print("# 1. P_3 = G_3 の構成(座標: sol_reply_73_math.md Q1.1)\n");
Print("============================================================\n");

P3 := BuildPn(3);;
sz3 := Size(P3.G);;
okSize3 := (sz3 = expectedSize(3));;
Print("[", PF(okSize3), "] |P_3| = ", sz3, " (期待 ", expectedSize(3), ")\n");
if not okSize3 then failures := failures + 1; fi;

Nord3 := Lcm(Order(P3.X), Order(P3.Y));;
Print("ord(X)=", Order(P3.X), "  ord(Y)=", Order(P3.Y), "  N_ord=lcm=", Nord3, "\n");

# ====================================================================
# 2. H_3^fun = H_{2,1,0} と H_{3,1,0} の構成(Sol 便73 (1.2)(6.1))
# ====================================================================
Print("\n============================================================\n");
Print("# 2. H_{2,1,0} = H_3^fun と H_{3,1,0} の構成\n");
Print("============================================================\n");

# H_{2,alpha,beta} := <a2, a1^alpha a3, a1^beta q2>
BuildH2 := function(P, alpha, beta)
  return Group(P.a2, P.a1^alpha * P.a3, P.a1^beta * P.q2);
end;;
# H_{3,alpha,beta} := <a3, a1^alpha a2, a1^beta q3>
BuildH3 := function(P, alpha, beta)
  return Group(P.a3, P.a1^alpha * P.a2, P.a1^beta * P.q3);
end;;

H2fun := BuildH2(P3, 1, 0);;   # H_3^fun (Sol 便73 (6.1))
H3fun := BuildH3(P3, 1, 0);;

sizeH2 := Size(H2fun);; sizeH3 := Size(H3fun);;
idxH2 := sz3/sizeH2;; idxH3 := sz3/sizeH3;;
Print("[", PF(sizeH2 = 18 and idxH2 = 6), "] |H_{2,1,0}| = ", sizeH2, " (期待 2n^2=18)   [P_3:H] = ", idxH2, " (期待 2n=6)\n");
Print("[", PF(sizeH3 = 18 and idxH3 = 6), "] |H_{3,1,0}| = ", sizeH3, " (期待 2n^2=18)   [P_3:H] = ", idxH3, " (期待 2n=6)\n");
if not (sizeH2 = 18 and idxH2 = 6) then failures := failures + 1; fi;
if not (sizeH3 = 18 and idxH3 = 6) then failures := failures + 1; fi;

NG_H2 := Normalizer(P3.G, H2fun);;
NG_H3 := Normalizer(P3.G, H3fun);;
w3H2 := (Size(NG_H2) = Size(H2fun));;
w3H3 := (Size(NG_H3) = Size(H3fun));;
Print("[", PF(w3H2), "] N_{P_3}(H_{2,1,0}) = H_{2,1,0} (alpha<>0 で自己正規化: 命題 ODD-H (1.3))\n");
Print("[", PF(w3H3), "] N_{P_3}(H_{3,1,0}) = H_{3,1,0}\n");
if not w3H2 then failures := failures + 1; fi;
if not w3H3 then failures := failures + 1; fi;

# H_{2,1,0} と H_{3,1,0} は j が異なるので P_3-共役ではないはず ((1.9): j=j' 必須)
notConjH2H3 := not IsConjugate(P3.G, H2fun, H3fun);;
Print("[", PF(notConjH2H3), "] H_{2,1,0} と H_{3,1,0} は P_3-非共役(命題 (1.9): j=j' が必要条件)\n");
if not notConjH2H3 then failures := failures + 1; fi;

# ====================================================================
# 3. H_{2,1,0}・H_{3,1,0} それぞれの次数 6 coset 表現・ordered passport
# ====================================================================
Print("\n============================================================\n");
Print("# 3. ordered passport (X,Y,Z) の実測(自己正規化した H ごと)\n");
Print("============================================================\n");

PassportTriple := function(P, H)
  local phi, Xi, Yi, Zi, idx;
  idx := Size(P.G)/Size(H);;
  phi := FactorCosetAction(P.G, H);;
  Xi := Image(phi, P.X);; Yi := Image(phi, P.Y);; Zi := (Xi*Yi)^-1;;
  return rec(idx:=idx, pX:=PassportOf(Xi,idx), pY:=PassportOf(Yi,idx), pZ:=PassportOf(Zi,idx));
end;;

ppH2 := PassportTriple(P3, H2fun);;
ppH3 := PassportTriple(P3, H3fun);;
Print("H_{2,1,0}: passport(X)=", PassportStr(ppH2.pX), "  passport(Y)=", PassportStr(ppH2.pY), "  passport(Z)=", PassportStr(ppH2.pZ), "\n");
Print("H_{3,1,0}: passport(X)=", PassportStr(ppH3.pX), "  passport(Y)=", PassportStr(ppH3.pY), "  passport(Z)=", PassportStr(ppH3.pZ), "\n");

# 「target」条件(week4-k3-v2-repairs.mjs T3 節・u_3 fixture の lambda 割当と同一):
#   passport(X) = [6], passport(Y) = [2,2,1,1](順序つき (2,2),(1,1)), passport(Z) = [6]
isTargetPassport := function(pp)
  return pp.pX = [[6,1]] and pp.pY = [[1,2],[2,2]] and pp.pZ = [[6,1]];
end;;
H2isTarget := isTargetPassport(ppH2);;
H3isTarget := isTargetPassport(ppH3);;
Print("[", PF(H2isTarget <> H3isTarget), "] ちょうど一方だけが target 型(6,2^2 1^2,6)であるべき(命題 (1.13)(1.14)・Q1.5 の j 選択と対応)\n");
Print("  H_{2,1,0} が target 型か: ", H2isTarget, "\n");
Print("  H_{3,1,0} が target 型か: ", H3isTarget, "\n");
if H2isTarget = H3isTarget then failures := failures + 1; fi;

# ====================================================================
# 4. 全 12 個の good H (自己正規化・qualifying) を直接列挙し、
#    target 型(6,2^2 1^2,6)の 6 個の P_3-共役類を機械同定する
# ====================================================================
Print("\n============================================================\n");
Print("# 4. good H (12 個) の全列挙と target クラスの同定\n");
Print("============================================================\n");

# 命題 ODD-H により qualifying H は H_{j,alpha,beta}, j in {2,3}, alpha,beta in Z/3
# の 2*3*3=18 個(alpha=0 含む)。good(自己正規化)は alpha<>0 の 2*2*3=12 個。
allCandidates := [];;
for j in [2,3] do
  for alpha in [0,1,2] do
    for beta in [0,1,2] do
      if j = 2 then H := BuildH2(P3, alpha, beta); else H := BuildH3(P3, alpha, beta); fi;
      Add(allCandidates, rec(j:=j, alpha:=alpha, beta:=beta, H:=H));
    od;
  od;
od;;
Print("qualifying 候補総数(alpha=0 含む) = ", Length(allCandidates), " (期待 18)\n");

goodCandidates := Filtered(allCandidates, c -> c.alpha <> 0);;
Print("good(自己正規化のはず)候補数 = ", Length(goodCandidates), " (期待 12)\n");

# 実際に自己正規化を検算(命題 ODD-H (1.3) の直接確認)
goodSelfNormCheck := ForAll(goodCandidates, c -> Size(Normalizer(P3.G, c.H)) = Size(c.H));;
Print("[", PF(goodSelfNormCheck), "] 12 個の good 候補すべてが実際に自己正規化(N_{P_3}(H)=H)\n");
if not goodSelfNormCheck then failures := failures + 1; fi;

badSelfNormCheck := ForAll(Filtered(allCandidates, c -> c.alpha = 0), c -> Size(Normalizer(P3.G, c.H)) > Size(c.H));;
Print("[", PF(badSelfNormCheck), "] alpha=0 の 6 個は自己正規化でない(命題 (1.3) の逆方向)\n");
if not badSelfNormCheck then failures := failures + 1; fi;

# それぞれの passport を計算し、target 型(6,2^2 1^2,6)を満たすものだけ抽出
for c in goodCandidates do
  pp := PassportTriple(P3, c.H);;
  c.isTarget := isTargetPassport(pp);;
  c.pp := pp;;
od;;

targetSet := Filtered(goodCandidates, c -> c.isTarget);;
otherSet := Filtered(goodCandidates, c -> not c.isTarget);;
Print("target 型(6,2^2 1^2,6)の候補数 = ", Length(targetSet), " (期待 6)\n");
Print("target 型でない候補数 = ", Length(otherSet), " (期待 6)\n");
targetCountOk := (Length(targetSet) = 6) and (Length(otherSet) = 6);;
Print("[", PF(targetCountOk), "] target/other の分割が 6/6\n");
if not targetCountOk then failures := failures + 1; fi;

# targetSet の j はすべて同一であるべき(命題 (1.9): P_3-共役は j を保つ)
targetJs := Set(List(targetSet, c -> c.j));;
Print("target 集合の j 値(集合) = ", targetJs, "\n");
targetJUniform := (Length(targetJs) = 1);;
Print("[", PF(targetJUniform), "] target 集合はすべて同じ j を持つ\n");
if not targetJUniform then failures := failures + 1; fi;

# targetSet が実際に単一の P_3-共役類をなすか(全ペア IsConjugate)
targetAllConj := true;;
for i in [1..Length(targetSet)] do
  for k in [1..Length(targetSet)] do
    if not IsConjugate(P3.G, targetSet[i].H, targetSet[k].H) then targetAllConj := false; fi;
  od;
od;;
Print("[", PF(targetAllConj), "] target 集合の 6 個が単一の P_3-共役類をなす\n");
if not targetAllConj then failures := failures + 1; fi;

# ====================================================================
# 5. 結論: target 集合(=測定窓の共役類)は H_2 側(j=2, H_3^fun)か H_3 側か
# ====================================================================
Print("\n============================================================\n");
Print("# 5. 結論\n");
Print("============================================================\n");

targetJValue := fail;;
if Length(targetJs) = 1 then targetJValue := targetJs[1]; fi;

measuredConjToH2fun := ForAny(targetSet, c -> IsConjugate(P3.G, c.H, H2fun));;
measuredConjToH3fun := ForAny(targetSet, c -> IsConjugate(P3.G, c.H, H3fun));;
Print("[", PF(measuredConjToH2fun <> measuredConjToH3fun), "] target 集合はちょうど一方(H_{2,1,0} か H_{3,1,0})とだけ P_3-共役\n");
Print("  target ~ H_{2,1,0}(=H_3^fun) : ", measuredConjToH2fun, "\n");
Print("  target ~ H_{3,1,0}          : ", measuredConjToH3fun, "\n");
if measuredConjToH2fun = measuredConjToH3fun then failures := failures + 1; fi;

c1Verdict := "UNKNOWN";;
if measuredConjToH2fun and not measuredConjToH3fun then
  c1Verdict := "CLOSED_MATCH";;   # 測定窓は H_3^fun と同じ (j,[alpha]) 類
elif measuredConjToH3fun and not measuredConjToH2fun then
  c1Verdict := "CLOSED_MISMATCH";;  # 測定窓は H_3^fun と異なる (j,[alpha]) 類
fi;;
Print("\nC1 caveat 判定: ", c1Verdict, "\n");
Print("  (j, [alpha]) の測定窓側 = (", targetJValue, ", [1])\n");
Print("  H_3^fun = H_{2,1,0} の (j,[alpha]) = (2, [1])\n");

# ====================================================================
# 総括
# ====================================================================
Print("\n############################################################\n");
if failures = 0 then
  Print("C1-CLASS-CHECK ALL PASSED\n");
else
  Print("C1-CLASS-CHECK FAILURES: ", failures, "\n");
fi;

t1 := GAPLIB_WallElapsedMs();;
Print("経過(壁時計) = ", (t1-t0)/1000.0, " s\n");

# ====================================================================
# 証明書 JSON
# ====================================================================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_c1.txt";;
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
  for e in p do
    Add(parts, JPair(e[1], e[2]));
  od;
  return JArr(parts);
end;;

TargetSetToJson := function(lst)
  local parts, c;
  parts := [];
  for c in lst do
    Add(parts, Concatenation(
      "{\"j\":", String(c.j), ",\"alpha\":", String(c.alpha), ",\"beta\":", String(c.beta),
      ",\"passport_X\":", PassportToJson(c.pp.pX),
      ",\"passport_Y\":", PassportToJson(c.pp.pY),
      ",\"passport_Z\":", PassportToJson(c.pp.pZ), "}"));
  od;
  return JArr(parts);
end;;

scriptSha256 := ComputeSha256File("search/c1-class-check.g");;

cert := Concatenation(
  "{\"schema\":\"c1-class-check/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/c1-class-check.g\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"universe\":{\"n\":3}",
  ",\"section1_p3\":{",
    "\"pn_size\":", String(sz3), ",\"pn_size_expected\":", String(expectedSize(3)), ",\"pn_size_pass\":", JB(okSize3),
    ",\"n_ord\":", String(Nord3),
  "}",
  ",\"section2_h2h3fun\":{",
    "\"h2fun_size\":", String(sizeH2), ",\"h2fun_index\":", String(idxH2), ",\"h2fun_self_normalizing\":", JB(w3H2),
    ",\"h3fun_size\":", String(sizeH3), ",\"h3fun_index\":", String(idxH3), ",\"h3fun_self_normalizing\":", JB(w3H3),
    ",\"h2fun_h3fun_not_conjugate\":", JB(notConjH2H3),
  "}",
  ",\"section3_passports\":{",
    "\"h2fun\":{\"X\":", PassportToJson(ppH2.pX), ",\"Y\":", PassportToJson(ppH2.pY), ",\"Z\":", PassportToJson(ppH2.pZ),
      ",\"is_target_type\":", JB(H2isTarget), "}",
    ",\"h3fun\":{\"X\":", PassportToJson(ppH3.pX), ",\"Y\":", PassportToJson(ppH3.pY), ",\"Z\":", PassportToJson(ppH3.pZ),
      ",\"is_target_type\":", JB(H3isTarget), "}",
    ",\"exactly_one_target_pass\":", JB(H2isTarget <> H3isTarget),
  "}",
  ",\"section4_good_enumeration\":{",
    "\"qualifying_total\":", String(Length(allCandidates)), ",\"qualifying_expected\":18",
    ",\"good_total\":", String(Length(goodCandidates)), ",\"good_expected\":12",
    ",\"good_self_normalizing_check_pass\":", JB(goodSelfNormCheck),
    ",\"alpha0_not_self_normalizing_check_pass\":", JB(badSelfNormCheck),
    ",\"target_set_size\":", String(Length(targetSet)), ",\"target_set_expected\":6",
    ",\"other_set_size\":", String(Length(otherSet)), ",\"other_set_expected\":6",
    ",\"target_j_uniform\":", JB(targetJUniform),
    ",\"target_j_value\":", String(targetJValue),
    ",\"target_all_mutually_conjugate\":", JB(targetAllConj),
    ",\"target_set_detail\":", TargetSetToJson(targetSet),
  "}",
  ",\"section5_conclusion\":{",
    "\"measured_window_conjugate_to_h2fun\":", JB(measuredConjToH2fun),
    ",\"measured_window_conjugate_to_h3fun\":", JB(measuredConjToH3fun),
    ",\"c1_verdict\":\"", c1Verdict, "\"",
  "}",
  ",\"overall_failures\":", String(failures),
  ",\"elapsed_wall_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/c1_class_check_20260728.json";;
WriteFile(outPath, cert);;

Print("\n証明書を書き出した: ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");

Print("\nC1-CLASS-CHECK DONE\n");
QUIT;
