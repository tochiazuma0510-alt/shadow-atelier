# search/ihc-fixture-v3.g -- I-25 複素共役座標の fixture v3 (裁定160 / sgn_c_resolution_v1.md SS7-8 修理)
#
# Usage: .\gap.ps1 search\ihc-fixture-v3.g
#
# v1(search/ihc-fixture.g)・v2(search/ihc-fixture-v2.g)は不変。本ファイルは新規。
#
# 背景(docs/notes/sgn_c_resolution_v1.md, 裁定 sol/裁定_160_SGNc解決.md):
#   FINDING SGN-c hat の根因は v2 の DecomposeConjugator (L84) が生の GAP 積
#   `conj * Inverse(q)` で分解していたこと。W-4 (week3-battery-common.g L46-54,
#   week1-定義ノート.md SS1.5.1) の下でこれは紙面正規形 conj = a.q の a ではなく、
#   conj = q.a' の a' (a' = q.a, q の A 上の線形作用) を計算していた。
#   副次的に v2 の「paperG := nativeG^-1」も前提が逆: W-4 の下で GAP の X^g は
#   既に紙面の inn(g)(X) = g X g^-1 である。
#
# 4つの修理(sgn_c_resolution_v1.md SS7 の処方どおり):
#   (1) 分解を AbstractProd([conj, Inverse(q)]) に置換 -- 紙面正規形 conj = a.q の a を返す。
#   (2) 「paperG := nativeG^-1」を撤去。native 探索で見つかる g がそのまま紙面 conjugator。
#   (3) discrimination の3分類を撤去し、a' = q.a の変換規則そのものを assert する
#       (QTransform 関数 + conversion_rule_check 欄)。
#   (4) 証明書に規約欄(normal_form / inn_convention / product_convention)を機械可読で持たせる。
#
# カナリア3軸分離(sgn_c_resolution_v1.md SS8):
#   (i)   c hat 本体 (m=2n-1, k=0): dv1=+1 が期待値。(A)(B)(C) いずれも縮退した元の判定。
#   (ii)  (A)軸: m=0 族の非対合 conjugator inn(a1^(-2k)) (k=2)。h=a1^(-2k) は非対合
#         (n が奇数かつ n を4k=8で割り切らないため)。native探索が h を返し h^-1 を
#         返さないことを確認する (repair (2) の直接検証)。
#   (iii) (B)軸: dv2<>0 の人工 conjugator (paper (dv1,dv2,dv3)=(1,2,0) を q1/q2/q3 の
#         各ラベルで構成)。修理後の分解が構成どおりに厳密復元し、旧(buggy)分解が
#         QTransform 規則ちょうど通りにずれることを assert する。
#
# 宇宙: n in {3,5,7,9,11} (v1/v2 と同一。事前登録範囲を変更しない)。u・c の平方類・c_mu には触れない。
# 解釈しない。v1/v2 ファイルと証明書は不変。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

Print("############################################################\n");
Print("# ihc-fixture-v3.g -- I-25 Ih(c_hat)=[2n-1,1] fixture v3 (n=3,5,7,9,11), 裁定160 repair\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;

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

# ---- 修理 (1): 分解を紙面正規形 conj = a.q の a に揃える (AbstractProd 経由) ----
# W-4 の下で paper "conj . q^-1" は raw Inverse(q) * conj ではなく、AbstractProd([conj, Inverse(q)])
# を通して初めて正しく計算される (raw B*A = paper "AB" の反転規約)。
DecomposeConjugatorPaper := function(conj, Pn, n)
  local Agrp, qCandidates, qp, v, i, j, k, outer, dv1, dv2, dv3, qLabel, decompLabel, found;
  Agrp := Group(Pn.a1, Pn.a2, Pn.a3);;
  qCandidates := [ ["1", One(Pn.G)], ["q1", Pn.q1], ["q2", Pn.q2], ["q3", Pn.q3] ];;
  dv1 := fail;;  dv2 := fail;;  dv3 := fail;;  qLabel := "n/a";;  decompLabel := "n/a";;  found := false;;
  for qp in qCandidates do
    v := AbstractProd([conj, Inverse(qp[2])]);;   # 紙面 conj . q^-1 (W-4 経由・修理(1))
    if v in Agrp then
      outer := false;;
      for i in [0..n-1] do
        for j in [0..n-1] do
          for k in [0..n-1] do
            if Pn.a1^i * Pn.a2^j * Pn.a3^k = v then
              dv1 := i;;  dv2 := j;;  dv3 := k;;  qLabel := qp[1];;
              decompLabel := Concatenation("(", String(i), ",", String(j), ",", String(k), ").", qp[1]);;
              outer := true;;  found := true;;  break;;
            fi;
          od;
          if outer then break; fi;
        od;
        if outer then break; fi;
      od;
      break;;
    fi;
  od;
  return rec(found:=found, dv1:=dv1, dv2:=dv2, dv3:=dv3, qLabel:=qLabel, decompLabel:=decompLabel);;
end;;

# ---- v2 の未修理版を「旧読み」として保持 (S1 の変換規則を assert するためだけに使う。
# 判定には一切使わない。conversion_rule_check の右辺の実測値を作る目的専用) ----
DecomposeConjugatorRawBuggy := function(conj, Pn, n)
  local Agrp, qCandidates, qp, v, i, j, k, outer, dv1, dv2, dv3, qLabel, decompLabel, found;
  Agrp := Group(Pn.a1, Pn.a2, Pn.a3);;
  qCandidates := [ ["1", One(Pn.G)], ["q1", Pn.q1], ["q2", Pn.q2], ["q3", Pn.q3] ];;
  dv1 := fail;;  dv2 := fail;;  dv3 := fail;;  qLabel := "n/a";;  decompLabel := "n/a";;  found := false;;
  for qp in qCandidates do
    v := conj * Inverse(qp[2]);;   # v2 の生 GAP 積そのまま (未修理・比較専用)
    if v in Agrp then
      outer := false;;
      for i in [0..n-1] do
        for j in [0..n-1] do
          for k in [0..n-1] do
            if Pn.a1^i * Pn.a2^j * Pn.a3^k = v then
              dv1 := i;;  dv2 := j;;  dv3 := k;;  qLabel := qp[1];;
              decompLabel := Concatenation("(", String(i), ",", String(j), ",", String(k), ")*", qp[1]);;
              outer := true;;  found := true;;  break;;
            fi;
          od;
          if outer then break; fi;
        od;
        if outer then break; fi;
      od;
      break;;
    fi;
  od;
  return rec(found:=found, dv1:=dv1, dv2:=dv2, dv3:=dv3, qLabel:=qLabel, decompLabel:=decompLabel);;
end;;

# ---- 修理 (3): discrimination の3分類を撤去し、a' = q.a の変換規則そのものを assert する ----
# q1 = diag(+,-,-), q2 = diag(-,+,-), q3 = diag(-,-,+) (A 上の線形作用, oddH 補題A)。
QTransform := function(qLabel, v1, v2, v3, n)
  if qLabel = "1" then return [v1 mod n, v2 mod n, v3 mod n]; fi;
  if qLabel = "q1" then return [v1 mod n, (-v2) mod n, (-v3) mod n]; fi;
  if qLabel = "q2" then return [(-v1) mod n, v2 mod n, (-v3) mod n]; fi;
  if qLabel = "q3" then return [(-v1) mod n, (-v2) mod n, v3 mod n]; fi;
  Error("QTransform: unknown qLabel ", qLabel);
end;;

TripleEq := function(t1, t2) return (t1[1]=t2[1]) and (t1[2]=t2[2]) and (t1[3]=t2[3]); end;;

ns := [3, 5, 7, 9, 11];;
results := [];;

for n in ns do
  Print("\n============================================================\n");
  Print("# n = ", n, "\n");
  Print("============================================================\n");

  Pn := BuildPn(n);;
  G := Pn.G;;  Xg := Pn.X;;  Yg := Pn.Y;;
  ordX := Order(Xg);;  ordY := Order(Yg);;
  Nord := Lcm(ordX, ordY);;
  m := 2*n - 1;;
  u := 2*m + 1;;

  Print("|G_n| = ", Size(G), "  ord(X)=", ordX, "  ord(Y)=", ordY, "  N_ord=", Nord, "\n");
  Print("m = 2n-1 = ", m, "   u = 2m+1 = ", u, "\n");

  # ---- (1) charming ----
  charmingOK := (Gcd(u, Nord) = 1);;
  Print("[", PF(charmingOK), "] (1) charming: gcd(u,N_ord) = gcd(", u, ",", Nord, ") = ",
        Gcd(u,Nord), " = 1 ?\n");

  # ---- shadow validity: f = Identity(G) directly ----
  f := Identity(G);;
  zElt := AbstractProd([Xg, Yg])^-1;;
  thetaHom := GroupHomomorphismByImages(G, G, [Xg, Yg], [Yg, Xg]);;
  tauHom := GroupHomomorphismByImages(G, G, [Xg, Yg], [Yg, zElt]);;
  if thetaHom = fail or tauHom = fail then
    Error("theta/tau homomorphism construction failed for n=", n);
  fi;

  thetaf := Image(thetaHom, f);;
  hex310 := AbstractProd([f, thetaf]) = Identity(G);;

  ymf := AbstractProd([Yg^m, f]);;
  tauymf := Image(tauHom, ymf);;
  tau2ymf := Image(tauHom, tauymf);;
  hex311 := AbstractProd([tau2ymf, tauymf, ymf]) = Identity(G);;

  genA := Xg^u;;
  genB := AbstractProd([f^-1, Yg^u, f]);;
  surj := (Size(Group(genA, genB)) = Size(G));;

  isShadow := charmingOK and hex310 and hex311 and surj;;
  Print("[", PF(hex310), "] (3.10) f*theta(f) = 1 (f=Identity(G))\n");
  Print("[", PF(hex311), "] (3.11) tau^2(y^m f)*tau(y^m f)*(y^m f) = 1\n");
  Print("[", PF(surj), "] <X^u, f^-1 Y^u f> = G_n (全射)\n");
  Print("[", PF(isShadow), "] [2n-1,1] は GT-shadow である\n");

  # ---- (2) 位数2 ----
  Xu2 := Xg^(u*u);;  Yu2 := Yg^(u*u);;
  fixesGens := (Xu2 = Xg) and (Yu2 = Yg);;
  isIdentityPhi := (Xg^u = Xg) and (Yg^u = Yg);;
  order2 := isShadow and fixesGens and (not isIdentityPhi);;
  Print("[", PF(fixesGens), "] Phi^2 = id (X^(u^2)=X, Y^(u^2)=Y)\n");
  Print("[", PF(not isIdentityPhi), "] Phi <> id (X^u<>X または Y^u<>Y)\n");
  Print("[", PF(order2), "] (2) GT(K^(n)) の元としての位数 = 2\n");

  # ==========================================================================
  # TEST (i): c_hat 本体 -- native 探索がそのまま紙面 conjugator (修理(2))
  # ==========================================================================
  innerFound := false;;  nativeG := fail;;
  for g in Elements(G) do
    if Xg^g = Xg^u and Yg^g = Yg^u then
      innerFound := true;;  nativeG := g;;  break;;
    fi;
  od;
  Print("[", PF(innerFound), "] (3) Phi_{2n-1,1} は inner (exists g in G_n: X^g=X^u, Y^g=Y^u, GAP規約)\n");

  chatDecomp := rec(found:=false, dv1:=fail, dv2:=fail, dv3:=fail, qLabel:="n/a", decompLabel:="n/a");;
  chatMatchesExact := false;;
  chatInvolution := fail;;
  chatRawDecomp := rec(found:=false, dv1:=fail, dv2:=fail, dv3:=fail, qLabel:="n/a", decompLabel:="n/a");;
  chatConversionRuleCheck := fail;;
  if innerFound then
    # 修理(2): nativeG 自身が紙面 conjugator h。「paperG := nativeG^-1」は不要かつ逆向き。
    chatDecomp := DecomposeConjugatorPaper(nativeG, Pn, n);;
    chatMatchesExact := chatDecomp.found and (chatDecomp.qLabel = "q3")
      and (chatDecomp.dv1 = 1) and (chatDecomp.dv2 = 0) and (chatDecomp.dv3 = 0);;
    chatInvolution := (nativeG^2 = Identity(G));;
    chatRawDecomp := DecomposeConjugatorRawBuggy(nativeG, Pn, n);;
    if chatDecomp.found and chatRawDecomp.found then
      chatConversionRuleCheck := TripleEq(
        [chatRawDecomp.dv1, chatRawDecomp.dv2, chatRawDecomp.dv3],
        QTransform(chatDecomp.qLabel, chatDecomp.dv1, chatDecomp.dv2, chatDecomp.dv3, n));;
    fi;
  fi;
  Print("  (i) 紙面(修理後)分解: ", chatDecomp.decompLabel, "   [", PF(chatMatchesExact),
        "] = (1,0,0).q3 予測と exact 一致\n");
  Print("      involution(g^2=1): ", chatInvolution, "\n");
  Print("      旧(buggy)分解: ", chatRawDecomp.decompLabel, "   [", PF(chatConversionRuleCheck),
        "] 変換規則 raw = QTransform(qLabel, paper) の assert\n");

  # ==========================================================================
  # TEST (ii): (A)軸カナリア -- m=0 族, 非対合 conjugator inn(a1^(-2k)), k=2
  # (docs/notes/w2fam_v1.md SS3.5 / phifam_v1.md L132 の inn(a1^(-2k)) 実現、確定済み数学)
  # ==========================================================================
  kk := 2;;
  m0 := 0;;
  charmingM0 := (Gcd(2*m0+1, Nord) = 1);;   # gcd(1,N_ord)=1 は自明に真 (SGN-3 の明示 assert)
  hPred := Pn.a1^(-2*kk);;
  XI := AbstractProd([hPred, Xg, hPred^-1]);;
  YI := AbstractProd([hPred, Yg, hPred^-1]);;
  nativeG2 := fail;;
  for g in Elements(G) do
    if Xg^g = XI and Yg^g = YI then nativeG2 := g;; break;; fi;
  od;
  axisAFound := (nativeG2 <> fail);;
  axisANativeEqualsHPred := false;;  axisANativeEqualsHPredInv := false;;
  axisAHPredInvolution := fail;;
  axisADecomp := rec(found:=false, dv1:=fail, dv2:=fail, dv3:=fail, qLabel:="n/a", decompLabel:="n/a");;
  if axisAFound then
    axisANativeEqualsHPred := (nativeG2 = hPred);;
    axisANativeEqualsHPredInv := (nativeG2 = hPred^-1);;
    axisAHPredInvolution := (hPred^2 = Identity(G));;
    axisADecomp := DecomposeConjugatorPaper(nativeG2, Pn, n);;
  fi;
  Print("  (ii) axis-A: m=0,k=", kk, "  charming(m=0)=", PF(charmingM0),
        "  native found=", PF(axisAFound), "\n");
  Print("       native = h_pred(=a1^(-2k))? ", PF(axisANativeEqualsHPred),
        "   native = h_pred^-1? ", PF(axisANativeEqualsHPredInv),
        "   h_pred involution? ", axisAHPredInvolution, "\n");
  Print("       紙面分解(修理後): ", axisADecomp.decompLabel, "\n");

  # ==========================================================================
  # TEST (iii): (B)軸カナリア -- dv2<>0 の人工 conjugator, q1/q2/q3 それぞれで round-trip
  # 構成: paper (p1,p2,p3)=(1,2,0) を各 qLabel と合わせた h = q * a1^p1 a2^p2 a3^p3 (raw)
  # (raw q*a が紙面 "a.q" になることは W: paper "AB" = raw B*A の直接帰結、下で assert)
  # ==========================================================================
  axisBLabels := ["q1", "q2", "q3"];;
  axisBQElts := [Pn.q1, Pn.q2, Pn.q3];;
  p1 := 1;;  p2 := 2;;  p3 := 0;;
  axisBResults := [];;
  for i in [1..3] do
    qLbl := axisBLabels[i];;  qElt := axisBQElts[i];;
    aWord := Pn.a1^p1 * Pn.a2^p2 * Pn.a3^p3;;
    hSynth := qElt * aWord;;   # raw q*a = paper "a.q" (W の直接帰結)
    # sanity: AbstractProd([aWord,qElt]) (paper "a.q" の別経路) と一致すること
    sanityCheck := (AbstractProd([aWord, qElt]) = hSynth);;
    corrDecomp := DecomposeConjugatorPaper(hSynth, Pn, n);;
    rawDecomp := DecomposeConjugatorRawBuggy(hSynth, Pn, n);;
    corrExact := corrDecomp.found and (corrDecomp.qLabel = qLbl)
      and (corrDecomp.dv1 = p1) and (corrDecomp.dv2 = p2) and (corrDecomp.dv3 = p3);;
    ruleCheck := fail;;
    if corrDecomp.found and rawDecomp.found then
      ruleCheck := TripleEq([rawDecomp.dv1, rawDecomp.dv2, rawDecomp.dv3],
        QTransform(corrDecomp.qLabel, corrDecomp.dv1, corrDecomp.dv2, corrDecomp.dv3, n));;
    fi;
    Add(axisBResults, rec(qLabel:=qLbl, sanity:=sanityCheck, corr_decomp:=corrDecomp.decompLabel,
      corr_exact:=corrExact, raw_decomp:=rawDecomp.decompLabel, rule_check:=ruleCheck));;
    Print("  (iii) axis-B q=", qLbl, ": sanity=", PF(sanityCheck),
          "  corr=", corrDecomp.decompLabel, " [", PF(corrExact), "]",
          "  raw=", rawDecomp.decompLabel, " [rule_check=", PF(ruleCheck), "]\n");
  od;

  Add(results, rec(
    n:=n, m:=m, u:=u, n_ord:=Nord,
    charming:=charmingOK, hex310:=hex310, hex311:=hex311, surjective:=surj,
    is_shadow:=isShadow, order2:=order2, inner_found:=innerFound,
    chat_decomp:=chatDecomp.decompLabel, chat_q_label:=chatDecomp.qLabel,
    chat_dv1:=chatDecomp.dv1, chat_dv2:=chatDecomp.dv2, chat_dv3:=chatDecomp.dv3,
    chat_matches_predicted_exact:=chatMatchesExact, chat_involution:=chatInvolution,
    chat_raw_decomp:=chatRawDecomp.decompLabel, chat_conversion_rule_check:=chatConversionRuleCheck,
    axisA_m:=m0, axisA_k:=kk, axisA_charming_m0:=charmingM0, axisA_found:=axisAFound,
    axisA_native_equals_h_pred:=axisANativeEqualsHPred,
    axisA_native_equals_h_pred_inverse:=axisANativeEqualsHPredInv,
    axisA_h_pred_involution:=axisAHPredInvolution,
    axisA_decomp:=axisADecomp.decompLabel, axisA_q_label:=axisADecomp.qLabel,
    axisA_dv1:=axisADecomp.dv1, axisA_dv2:=axisADecomp.dv2, axisA_dv3:=axisADecomp.dv3,
    axisB_p1:=p1, axisB_p2:=p2, axisB_p3:=p3, axisB_results:=axisBResults
  ));;
od;;

# ====================================================================
# 総括表
# ====================================================================
Print("\n############################################################\n");
Print("# 総括: I-25 判定表 v3 (3軸カナリア分離版)\n");
Print("############################################################\n");
Print("n  | is_shadow | order2 | inner | chat_exact | chat_inv | chat_rule | axisA(=h/=h^-1/inv) | axisB(q1/q2/q3 exact,rule)\n");
for r in results do
  Print(r.n, "  | ", PF(r.is_shadow), " | ", PF(r.order2), " | ", PF(r.inner_found), " | ",
        PF(r.chat_matches_predicted_exact), " | ", r.chat_involution, " | ",
        PF(r.chat_conversion_rule_check), " | ",
        PF(r.axisA_native_equals_h_pred), "/", PF(r.axisA_native_equals_h_pred_inverse), "/",
        r.axisA_h_pred_involution, " | ",
        JoinC(List(r.axisB_results, b -> Concatenation(b.qLabel, ":", PF(b.corr_exact), ",", PF(b.rule_check))), " "),
        "\n");
od;

t1 := GAPLIB_WallElapsedMs();;
Print("\n経過(壁時計) = ", (t1-t0)/1000.0, " s\n");

# ====================================================================
# 証明書 JSON
# ====================================================================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_ihc_v3.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

FieldToJson := function(v)
  if v = fail then return JStr("fail"); fi;
  if IsString(v) then return JStr(v); fi;
  if IsBool(v) then return JB(v); fi;
  return String(v);
end;;

AxisBResultToJson := function(b)
  return Concatenation(
    "{\"q_label\":", JStr(b.qLabel),
    ",\"sanity_paper_normal_form_construction\":", JB(b.sanity),
    ",\"corrected_decomp\":", JStr(b.corr_decomp),
    ",\"corrected_exact_roundtrip\":", JB(b.corr_exact),
    ",\"raw_buggy_decomp\":", JStr(b.raw_decomp),
    ",\"conversion_rule_check\":", FieldToJson(b.rule_check),
    "}"
  );
end;;

ResultToJson := function(r)
  local axisBArr;
  axisBArr := JArr(List(r.axisB_results, AxisBResultToJson));;
  return Concatenation(
    "{\"n\":", String(r.n), ",\"m\":", String(r.m), ",\"u\":", String(r.u),
    ",\"n_ord\":", String(r.n_ord),
    ",\"charming\":", JB(r.charming),
    ",\"hex310\":", JB(r.hex310), ",\"hex311\":", JB(r.hex311),
    ",\"surjective\":", JB(r.surjective),
    ",\"is_shadow\":", JB(r.is_shadow),
    ",\"order2\":", JB(r.order2),
    ",\"inner_found\":", JB(r.inner_found),
    ",\"test_i_chat\":{",
      "\"conjugator_decomp\":", JStr(r.chat_decomp),
      ",\"q_label\":", JStr(r.chat_q_label),
      ",\"dv1\":", FieldToJson(r.chat_dv1),
      ",\"dv2\":", FieldToJson(r.chat_dv2),
      ",\"dv3\":", FieldToJson(r.chat_dv3),
      ",\"matches_predicted_form_exact\":", JB(r.chat_matches_predicted_exact),
      ",\"involution\":", FieldToJson(r.chat_involution),
      ",\"raw_buggy_decomp_for_rule_demo\":", JStr(r.chat_raw_decomp),
      ",\"conversion_rule_check\":", FieldToJson(r.chat_conversion_rule_check),
    "}",
    ",\"test_ii_axisA_m0_family\":{",
      "\"m\":", String(r.axisA_m), ",\"k\":", String(r.axisA_k),
      ",\"charming_m0\":", JB(r.axisA_charming_m0),
      ",\"native_found\":", JB(r.axisA_found),
      ",\"native_equals_h_predicted\":", JB(r.axisA_native_equals_h_pred),
      ",\"native_equals_h_predicted_inverse\":", JB(r.axisA_native_equals_h_pred_inverse),
      ",\"h_predicted_involution\":", FieldToJson(r.axisA_h_pred_involution),
      ",\"conjugator_decomp\":", JStr(r.axisA_decomp),
      ",\"q_label\":", JStr(r.axisA_q_label),
      ",\"dv1\":", FieldToJson(r.axisA_dv1),
      ",\"dv2\":", FieldToJson(r.axisA_dv2),
      ",\"dv3\":", FieldToJson(r.axisA_dv3),
    "}",
    ",\"test_iii_axisB_synthetic\":{",
      "\"constructed_paper_triple\":[", String(r.axisB_p1), ",", String(r.axisB_p2), ",", String(r.axisB_p3), "]",
      ",\"per_q_label\":", axisBArr,
    "}",
    "}"
  );
end;;

resultsJson := JArr(List(results, ResultToJson));;

scriptSha256 := ComputeSha256File("search/ihc-fixture-v3.g");;

cert := Concatenation(
  "{\"schema\":\"ihc-fixture/v3\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/ihc-fixture-v3.g\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"universe\":{\"n_values\":[3,5,7,9,11]}",
  ",\"design_source\":\"docs/notes/sgn_c_resolution_v1.md SS7(修理仕様)+SS8(カナリア仕様) / sol/裁定_160_SGNc解決.md\"",
  ",\"convention\":{",
    "\"normal_form\":\"a.q (paper, a in A=<a1,a2,a3>, q in {1,q1,q2,q3})\"",
    ",\"inn_convention\":\"inn(h)(X) = h X h^-1 (paper). GAP's X^g literally equals this with g=h (no inversion, cf. week1-定義ノート.md SS1.5.1 W-1/W-4 + docs/notes/sgn_c_resolution_v1.md SS4.2)\"",
    ",\"product_convention\":\"W-4 (search/week3-battery-common.g AbstractProd = reversed GAP raw product; paper word w1 w2 ... wk <-> raw wk*...*w1)\"",
    ",\"q_action_on_A\":\"q1=diag(+,-,-), q2=diag(-,+,-), q3=diag(-,-,+) (oddH 補題A). QTransform(q,a)=q.a is the rule checked by conversion_rule_check fields\"",
  "}",
  ",\"repair_note\":\"v2 (search/ihc-fixture-v2.g) の DecomposeConjugator は生 GAP 積 conj*Inverse(q) で",
   "分解しており、これは紙面正規形 conj=a.q の a ではなく conj=q.a' の a' (a'=q.a) を返していた",
   "(FINDING SGN-c hat の根因)。v3 では AbstractProd([conj,Inverse(q)]) に置換(修理1)、",
   "paperG:=nativeG^-1 を撤去(修理2、GAP の X^g は既に紙面 inn(g)(X)=gXg^-1)、",
   "discrimination の3分類を a'=q.a の変換規則そのものの assert に差替(修理3)、",
   "規約を証明書の機械可読フィールドへ昇格(修理4)。旧(buggy)分解関数は",
   "conversion_rule_check の右辺を作る目的でのみ残し、判定には使わない。\"",
  ",\"results\":", resultsJson,
  ",\"elapsed_wall_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/ihc_fixture_v3_20260729.json";;
WriteFile(outPath, cert);;

Print("\n証明書を書き出した: ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
Print("\nIHC-FIXTURE-V3 DONE\n");
QUIT;
