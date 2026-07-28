# search/k9-package.g -- n=9 群論層パッケージ
#
# 実行: .\gap.ps1 search\k9-package.g
#
# 正本:
#   docs/week1-定義ノート.md          -- Thm 4.3(GT(K^(n)) 明示式)・hexagon (3.3)(3.4)・
#                                         簡約 hexagon (3.10)(3.11)・charming・K_ord
#   sol/sol_reply_73_math.md Q1.1     -- P_n = A_n rtimes Q の座標辞書(a_i, q_i の符号表)
#   docs/notes/hfun_functoriality_v1.md -- H^fun = H_{2,1,0} = <a_2, a_1 a_3, q_2>、
#                                         命題 HF-1(a-d)・HF-2(quotient functoriality)
#   docs/week4-BFC攻略_opus_v2.md S13.1 -- 窓条件 (W1)-(W5) の定義表(唯一の正本箇所。
#                                         week1-定義ノートには「窓条件節」という名の節は
#                                         存在しない -- 発注書の言及先はおそらくこちら。
#                                         下記タスク2の報告部で明示的に注記する)
#
# 既存基盤の再利用(探索器レイヤー内の共有・crosscheck とは無関係):
#   search/week3-battery-common.g の MakeGn / EnumerateReducedHexagon / AbstractProd 等。
#   EnumerateReducedHexagon は c_in_N=true (K^(n) は psi_n(c)=1 により常に c in K^(n)) の
#   ときの quotient-shortcut theta/tau を用いる既存较正済み手法(1a/1b/2a/2b 等で使用実績)。
#   search/gaplib_common.g の JSON/WriteFile/sha256 ヘルパー。
#
# 宇宙: n=9 のみ(発注書の事前登録どおり)。副読として n=3 を使うのは HF-2 の
#   reduction target としてのみであり、新規対象として登録するものではない
#   (week1-定義ノート.md 較正スイート v2 の n=3 は既に登録済み対象)。
#
# 規律: u・c の平方類・c_mu には触れない。解釈しない(観測の記録に徹する)。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

Print("############################################################\n");
Print("# k9-package.g -- n=9 GT(K^(9)) 較正 + H9^fun 窓 + HF-2 実測\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;

# ====================================================================
# 共通構成: BuildPn(n) -- P_n = A_n rtimes Q の座標辞書つき具体表現
#   D_n^3 の 3n 点上の置換として実装(MakeGn と同一の tr ブロック構成)。
#   a_i := 第 i 成分だけ r。 q_1 := (1,s,s), q_2 := (s,1,s), q_3 := (s,s,1)
#   (Sol 便73 Q1.1 の符号表・hfun_functoriality_v1.md S0 と同一の座標)。
#   X = a_1 q_1, Y = a_1 a_2 a_3 q_2 (hfun_functoriality_v1.md (0.1)) を
#   MakeGn 慣例の直接構成 tr(r,1)*tr(s,2)*tr(s,3) 等と突き合わせ、
#   一致しなければ Error で止める(座標辞書の実装レベル検証)。
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
  # 注意(実装上の罠・発見事項): 論文の抽象語 "a1 q1" / "a1 a2 a3 q2" を GAP で
  # 素朴に左から右へそのまま掛けると、a_i と q_j が同じブロックを共有する場合
  # (Y の場合の block1: a1 と q2、block3: a3 と q2)に paper/GAP 語規約(規約 W-1/W-2、
  # docs/week1-定義ノート.md S1.5)の反転が効いて MakeGn 慣例と食い違う。
  # 実測: 素朴な a1*a2*a3*q2 は block1/block3 で "r then s" (GAP r*s) を与えるが、
  # 必要なのは "s then r" (GAP s*r、MakeGn の rs=s*r 慣例) であった。
  # AbstractProd(week3-battery-common.g、既存の paper-word 反転規約)を使うと正しく
  # q2*a3*a2*a1 の順になり一致する。X は a1,q1 がブロックを共有しないため素朴な積でも
  # 一致するが、統一のため同じ AbstractProd を両方に用いる。
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

# 完全な cycle passport: [[cycle長, cycle長の個数], ...] (長さ昇順)
PassportOf := function(perm, deg)
  local lens, coll;
  lens := List([1..deg], i -> CycleLength(perm, i));
  coll := Collected(lens);
  return List(coll, e -> [e[1], e[2]/e[1]]);
end;;

failures := 0;;

# ====================================================================
# タスク1: GT(K^(9)) 較正
# ====================================================================
Print("\n============================================================\n");
Print("# タスク1: GT(K^(9)) 較正\n");
Print("============================================================\n");

P9 := BuildPn(9);;
sz9 := Size(P9.G);;
okSize9 := (sz9 = expectedSize(9));;
Print("[", PF(okSize9), "] |P_9| = ", sz9, " (期待 ", expectedSize(9), ")\n");
if not okSize9 then failures := failures + 1; fi;

Nord9 := Lcm(Order(P9.X), Order(P9.Y));;
okNord9 := (Nord9 = Lcm(9,2));;
Print("[", PF(okNord9), "] N_ord = lcm(ord X, ord Y) = ", Nord9, " (期待 ", Lcm(9,2), ")\n");
if not okNord9 then failures := failures + 1; fi;

# Thm 4.3 理論値: n=9 は奇数(alpha=0, n0=9)なので |GT(K^(9))| = 2*n0*phi(n0)
phi9 := Length(Filtered([1..9], k -> Gcd(k,9)=1));;
theoreticalGT9 := 2 * 9 * phi9;;
Print("理論値(Thm 4.3, n=n0=9, alpha=0): 2*n0*phi(n0) = 2*9*", phi9, " = ", theoreticalGT9, "\n");

# charming set X_9 = {m in [0..N_ord-1] | gcd(2m+1, N_ord)=1}
charmingSet9 := Filtered([0..Nord9-1], m -> Gcd(2*m+1, Nord9) = 1);;
Print("charming set X_9 (|X_9|=", Length(charmingSet9), "): ", charmingSet9, "\n");

qrec9 := rec(x:=P9.X, y:=P9.Y, G:=P9.G);;
gtResult9 := EnumerateReducedHexagon(qrec9, charmingSet9);;

Print("候補総数(|D-words| x |charming|) = ", gtResult9.candidate_total, "\n");
Print("(3.10) 失敗 = ", gtResult9.h10_fail, "  (3.11) 失敗 = ", gtResult9.h11_fail,
      "  生成不十分 = ", gtResult9.generation_fail, "\n");
Print("実測 |GT(K^(9))| = ", gtResult9.shadow_total, "\n");

gtCalibPass := (gtResult9.shadow_total = theoreticalGT9);;
Print("[", PF(gtCalibPass), "] GT(K^(9)) 較正: 実測 ", gtResult9.shadow_total,
      " = 理論値 ", theoreticalGT9, "\n");
if not gtCalibPass then failures := failures + 1; fi;

# m ごとの内訳(参考: 各 charming m に対し実際に何個の f が通ったか)
mCounts9 := [];;
for m in charmingSet9 do
  Add(mCounts9, rec(m:=m, count:=Length(Filtered(gtResult9.shadows, sh -> sh.m = m))));
od;
Print("m ごとの shadow 数: ");
for e in mCounts9 do Print("m=", e.m, ":", e.count, "  "); od;
Print("\n");

# ====================================================================
# タスク2: H_9^fun 窓パッケージ
# ====================================================================
Print("\n============================================================\n");
Print("# タスク2: H_9^fun 窓パッケージ\n");
Print("============================================================\n");

H9 := Group(P9.a2, P9.a1*P9.a3, P9.q2);;
sizeH9 := Size(H9);;
idxH9 := Size(P9.G) / sizeH9;;
Print("|H_9^fun| = ", sizeH9, " (期待 2*9^2=162)   [P_9:H_9^fun] = ", idxH9, " (期待 2*9=18)\n");
okH9size := (sizeH9 = 2*81) and (idxH9 = 18);;
Print("[", PF(okH9size), "] HF-1(a) の実測再現\n");
if not okH9size then failures := failures + 1; fi;

# W3: 自己正規化
NG_H9 := Normalizer(P9.G, H9);;
w3pass := (Size(NG_H9) = Size(H9));;
Print("[", PF(w3pass), "] (W3) N_{P_9}(H_9^fun) = H_9^fun : ", w3pass, "\n");
if not w3pass then failures := failures + 1; fi;

# W4: <X> が P_9/H 上推移的 かつ [P:H]=2n=M=ord(X)
phiAction9 := FactorCosetAction(P9.G, H9);;
Ximg9 := Image(phiAction9, P9.X);;
Yimg9 := Image(phiAction9, P9.Y);;
Zimg9 := (Ximg9 * Yimg9)^-1;;
orbX9 := Orbit(Group(Ximg9), 1);;
w4transitive := (Length(orbX9) = idxH9);;
w4orderX := (Order(P9.X) = idxH9);;
w4pass := w4transitive and w4orderX;;
Print("[", PF(w4pass), "] (W4) <X_9> が P_9/H_9^fun 上推移的 (軌道長=", Length(orbX9),
      ") かつ ord(X_9)=", Order(P9.X), " = [P:H]=", idxH9, "\n");
if not w4pass then failures := failures + 1; fi;

# ordered passport: (2n, 2^{n-1}1^2, 2n) = (18, 2^8 1^2, 18)  (n=9)
passX9 := PassportOf(Ximg9, idxH9);;
passY9 := PassportOf(Yimg9, idxH9);;
passZ9 := PassportOf(Zimg9, idxH9);;
Print("passport(X) = ", passX9, " (期待 [[18,1]])\n");
Print("passport(Y) = ", passY9, " (期待 [[1,2],[2,8]])\n");
Print("passport(Z) = ", passZ9, " (期待 [[18,1]])\n");
passportPass := (passX9 = [[18,1]]) and (passY9 = [[1,2],[2,8]]) and (passZ9 = [[18,1]]);;
Print("[", PF(passportPass), "] ordered passport (2n, 2^(n-1)1^2, 2n) = (18, 2^8 1^2, 18) の確認\n");
if not passportPass then failures := failures + 1; fi;

# ---- (W1)(W2)(CAL) の判定 ----
Print("\n--- (W1)(W2)(CAL) の判定 ---\n");
Print("[UNKNOWN] (W1): 定義(docs/week4-BFC攻略_opus_v2.md S13.1)は「N-bar 開・G_Q-安定」\n");
Print("  という Galois 側(算術)の条件であり、有限群 GAP 計算の射程外。本パッケージは計算しない。\n");
Print("[UNKNOWN] (W2): 定義は「完全列 + tilde-chi o Ih = chi_{2M}」という Galois 表現の\n");
Print("  比較条件であり、同様に算術側。GAP では計算できない。\n");
Print("[UNKNOWN] (CAL): 較正ゲート(alpha^Ih = alpha^std)は Rule 1 型の actual intertwiner\n");
Print("  データ(n=9 版の Z_{2*18}-link・chi_{2M} 具体形・F_0 = C_9 の Ih 側同定)を要し、\n");
Print("  現状 n=9 に対するこれらのデータは docs/ に見当たらない(K^(5)/K^(3)/A_5 のみ既出)。\n");
Print("  n=9 版 CAL は「定義に必要な入力が未整備」につき UNKNOWN。\n");

# ---- 補足(bonus, 発注書は明示要求していない): (W5) の H_9^fun 個体への直接検算 ----
# タスク1 で得た GT(K^(9)) の 108 shadow それぞれについて、T_{m,f}: x->x^u, y->f^-1 y^u f
# が定める自己同型 Phi_{m,f} のもとで Phi_{m,f}(H_9^fun) が H_9^fun と P_9-共役かどうかを
# 直接検算する(命題K5-1 / Sol便73 (1.13)(1.14) の予言、search/certs/w5_regression_20260728.json
# の n=9 regression は Phi(F_0)=inn(<X^2>) のみの安定性であり、これは全 GT(K^(9)) 元への
# より強い安定性を H_9^fun という個体について直接確かめるもの。既存 helper を再利用しない
# 独立の計算)。
Print("\n--- 補足(bonus): 108 shadow 全件での Phi_{m,f}(H_9^fun) ~ H_9^fun の直接検算 ---\n");
w5BonusFail := 0;;
w5BonusChecked := 0;;
w5BonusNonBijective := 0;;
for sh in gtResult9.shadows do
  u := 2*sh.m + 1;;
  f := sh.f;;
  # F10 修理(裁定 109): paper-word "f^-1 Y^u f" は AbstractProd(week3-battery-common.g、
  # BuildPn 内のコメント・W-4 規約)の反転を経て GAP 積 f * Y^u * f^-1 に対応する。
  # 素朴な GAP 積 f^-1 * Y^u * f をそのまま書くのは規約違反(F10 バグ)だったため修正。
  PhiHom := GroupHomomorphismByImages(P9.G, P9.G, [P9.X, P9.Y], [P9.X^u, AbstractProd([f^-1, P9.Y^u, f])]);;
  if PhiHom = fail then
    Print("[FAIL] m=", sh.m, ": Phi_{m,f} の構成に失敗(自己同型のはずが homomorphism 不成立)\n");
    w5BonusFail := w5BonusFail + 1;
  elif not IsBijective(PhiHom) then
    # F11 修理(裁定 109): GroupHomomorphismByImages <> fail は自己同型を意味しない
    # (準同型として構成できただけで単射・全射は別途保証が要る)。IsBijective を必須検査にする。
    Print("[FAIL] m=", sh.m, ": Phi_{m,f} は準同型として構成できたが IsBijective=false(自己同型でない)\n");
    w5BonusFail := w5BonusFail + 1;
    w5BonusNonBijective := w5BonusNonBijective + 1;
  else
    PhiH9 := Image(PhiHom, H9);;
    conj := IsConjugate(P9.G, PhiH9, H9);;
    w5BonusChecked := w5BonusChecked + 1;
    if not conj then
      w5BonusFail := w5BonusFail + 1;
      Print("[FAIL] m=", sh.m, ": Phi_{m,f}(H_9^fun) が H_9^fun と非共役\n");
    fi;
  fi;
od;
Print("[", PF(w5BonusFail = 0), "] 108 shadow 中 ", w5BonusChecked, " 件で Phi_{m,f}(H_9^fun) ~ H_9^fun を検査、",
      "非単射で除外 ", w5BonusNonBijective, " 件、不一致(非単射込み) ", w5BonusFail, " 件\n");
if w5BonusFail <> 0 then failures := failures + 1; fi;

# ====================================================================
# タスク3: HF-2 実測確認 (pi_{9,3}(H_9^fun) = H_3^fun、繊維が全て3点)
# ====================================================================
Print("\n============================================================\n");
Print("# タスク3: HF-2 実測確認 (n=9, d=3)\n");
Print("============================================================\n");

P3 := BuildPn(3);;
H3 := Group(P3.a2, P3.a1*P3.a3, P3.q2);;
Print("|P_3| = ", Size(P3.G), "   |H_3^fun| = ", Size(H3), "\n");

hom93 := GroupHomomorphismByImages(P9.G, P3.G,
           [P9.a1, P9.a2, P9.a3, P9.q1, P9.q2],
           [P3.a1, P3.a2, P3.a3, P3.q1, P3.q2]);;
homOk := (hom93 <> fail);;
Print("[", PF(homOk), "] pi_{9,3}: P_9 -> P_3 (marked quotient) の構成\n");
if not homOk then failures := failures + 1; fi;

imageH9 := Image(hom93, H9);;
hf2a := (imageH9 = H3);;
Print("[", PF(hf2a), "] HF-2(a): pi_{9,3}(H_9^fun) = H_3^fun : ", hf2a, "\n");
if not hf2a then failures := failures + 1; fi;

# 繊維の直接計算: P_9/H_9^fun (18 cosets) -> P_3/H_3^fun (6 cosets)、各繊維の濃度
cosets9 := RightCosets(P9.G, H9);;
cosets3 := RightCosets(P3.G, H3);;
Print("|P_9/H_9^fun| (cosets) = ", Length(cosets9), "   |P_3/H_3^fun| (cosets) = ", Length(cosets3), "\n");

fiberCount := List(cosets3, c -> 0);;
for c9 in cosets9 do
  gRep := Representative(c9);;
  gImg := Image(hom93, gRep);;
  idx3 := fail;;
  for kk in [1..Length(cosets3)] do
    if gImg in cosets3[kk] then idx3 := kk; break; fi;
  od;
  if idx3 = fail then
    Error("HF-2 fiber check: image coset not found (well-definedness broken)");
  fi;
  fiberCount[idx3] := fiberCount[idx3] + 1;
od;
Print("繊維の濃度(各 target coset ごとの source coset 数): ", fiberCount, "\n");
hf2b := ForAll(fiberCount, c -> c = 9/3);;
Print("[", PF(hf2b), "] HF-2(b): 全繊維の濃度が n/d=3 : ", hf2b, "\n");
if not hf2b then failures := failures + 1; fi;

# ====================================================================
# 総括
# ====================================================================
Print("\n############################################################\n");
if failures = 0 then
  Print("K9-PACKAGE ALL PASSED\n");
else
  Print("K9-PACKAGE FAILURES: ", failures, "\n");
fi;

t1 := GAPLIB_WallElapsedMs();;
Print("経過(壁時計) = ", (t1-t0)/1000.0, " s\n");

# ====================================================================
# 証明書 JSON
# ====================================================================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_k9.txt";;
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

mCountsJson := function(lst)
  local parts, e;
  parts := [];
  for e in lst do
    Add(parts, Concatenation("{\"m\":", String(e.m), ",\"count\":", String(e.count), "}"));
  od;
  return JArr(parts);
end;;

scriptSha256 := ComputeSha256File("search/k9-package.g");;

cert := Concatenation(
  "{\"schema\":\"k9-package/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/k9-package.g\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"universe\":{\"n\":9}",
  ",\"task1_gt_k9_calibration\":{",
    "\"pn_size\":", String(sz9), ",\"pn_size_expected\":", String(expectedSize(9)),
    ",\"pn_size_pass\":", JB(okSize9),
    ",\"n_ord\":", String(Nord9), ",\"n_ord_expected\":", String(Lcm(9,2)), ",\"n_ord_pass\":", JB(okNord9),
    ",\"theoretical_order\":", String(theoreticalGT9),
    ",\"charming_set\":", JArr(List(charmingSet9, String)),
    ",\"candidate_total\":", String(gtResult9.candidate_total),
    ",\"h10_fail\":", String(gtResult9.h10_fail),
    ",\"h11_fail\":", String(gtResult9.h11_fail),
    ",\"generation_fail\":", String(gtResult9.generation_fail),
    ",\"observed_order\":", String(gtResult9.shadow_total),
    ",\"calibration_pass\":", JB(gtCalibPass),
    ",\"m_counts\":", mCountsJson(mCounts9),
  "}",
  ",\"task2_h9fun_window\":{",
    "\"h_size\":", String(sizeH9), ",\"index\":", String(idxH9),
    ",\"hf1a_pass\":", JB(okH9size),
    ",\"w3_self_normalizing\":", JB(w3pass),
    ",\"w4_transitive\":", JB(w4transitive), ",\"w4_order_x_eq_index\":", JB(w4orderX),
    ",\"ordered_passport\":{\"X\":", PassportToJson(passX9),
      ",\"Y\":", PassportToJson(passY9), ",\"Z\":", PassportToJson(passZ9), "}",
    ",\"ordered_passport_expected\":{\"X\":[[18,1]],\"Y\":[[1,2],[2,8]],\"Z\":[[18,1]]}",
    ",\"ordered_passport_pass\":", JB(passportPass),
    ",\"w1_status\":\"UNKNOWN\",\"w1_reason\":\"arithmetic-side (Nbar open + G_Q-stable); not GAP-computable\"",
    ",\"w2_status\":\"UNKNOWN\",\"w2_reason\":\"arithmetic-side (exact sequence + chi_2M compatibility); not GAP-computable\"",
    ",\"cal_status\":\"UNKNOWN\",\"cal_reason\":\"n=9 Rule-1-style intertwiner / Z_36-link / chi_36 concrete form not present in docs/\"",
    ",\"w5_bonus_checked\":", String(w5BonusChecked), ",\"w5_bonus_fail\":", String(w5BonusFail),
    ",\"w5_bonus_nonbijective\":", String(w5BonusNonBijective),
    ",\"w5_bonus_all_pass\":", JB(w5BonusFail = 0),
  "}",
  ",\"task3_hf2_functoriality\":{",
    "\"hom_constructed\":", JB(homOk),
    ",\"hf2a_image_equals_h3\":", JB(hf2a),
    ",\"cosets9_count\":", String(Length(cosets9)), ",\"cosets3_count\":", String(Length(cosets3)),
    ",\"fiber_counts\":", JArr(List(fiberCount, String)),
    ",\"hf2b_all_fibers_eq_3\":", JB(hf2b),
  "}",
  ",\"overall_failures\":", String(failures),
  ",\"elapsed_wall_ms\":", String(t1-t0),
  ",\"supersedes\":\"search/certs/k9_package_20260728.json\"",
  ",\"repair_note\":\"裁定109 ODD-H監査 F10/F11 修理後の再発行。F10: L221 の f^-1*Y^u*f を",
   " AbstractProd([f^-1,Y^u,f])(=f*Y^u*f^-1、week3-battery-common.g W-4 反転規約)へ修正。",
   " F11: GroupHomomorphismByImages<>fail を自己同型と誤読していた点を修理し IsBijective を必須assert化。\"",
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/k9_package_20260728_r2.json";;
WriteFile(outPath, cert);;

Print("\n証明書を書き出した: ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");

Print("\nK9-PACKAGE DONE\n");
QUIT;
