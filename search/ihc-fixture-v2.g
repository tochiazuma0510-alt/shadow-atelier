# search/ihc-fixture-v2.g -- I-25 複素共役座標の fixture v2(便 78 検分 F78-2.4 修理)
#
# Usage: .\gap.ps1 search\ihc-fixture-v2.g
#
# 目的(F78-2.4 の 3 修理を反映):
#   v1(search/ihc-fixture.g, 証明書 ihc_fixture_20260728.json)は、GT-元 Phi_{2n-1,1} を
#   実現する inner automorphism の conjugator "innerG" を GAP の共役規約(X^g = g^-1 X g)
#   でブルートフォース探索したあと、その同じ innerG を「紙面の inn(g)(h)=g h g^-1 規約」の
#   予測分解 "(1-2k)e1 q3"(oddH SS11.2)と比較していた。これは規約が食い違ったまま突合する
#   バグで、Sol 便 78 が指摘した通り第五判定(matches_predicted_form)は qLabel="q3"/dv2=0/dv3=0
#   しか検査せず、係数 dv1(符号)を素通りしていた。
#
#   v2 の修理:
#     (1) native_conjugator(GAP規約: X^g=g^-1 X g をそのまま満たす g)と
#         paper_conjugator(紙面規約: inn(h)(X)=h X h^-1 をそのまま満たす h)を別欄に持つ。
#         変換式は g^-1 X g = h X h^-1 と書けるので h = g^-1(相互変換式をこの1箇所に固定)。
#     (2) 両方を同一の分解関数(v = conj * Inverse(q_label), v = a1^i a2^j a3^k)で分解し、
#         dv1 まで含めて記録する。
#     (3) matches_predicted_form_exact は paper_conjugator の分解(dv1,dv2,dv3,qLabel)を
#         予測 (dv1,dv2,dv3,qLabel) = (1,0,0,"q3") と exact 照合する(dv1 を含む)。
#     (4) native と paper の分解を比較し、判別根拠(discrimination)欄に次を機械的に記録する:
#         - "identical": 分解が完全一致(native=paper)
#         - "dv1_negated_only": qLabel/dv2/dv3 が一致し dv1 の符号のみが逆
#           (逆元を取ると a1-指数の符号だけが反転するという規約変換の効果と整合するパターン
#            -- ただしこれは経験的分類であり、q3 との交換関係を独立に証明したものではない)
#         - "irregular_pattern": 上記のいずれでもない(真の drift の可能性を排除できない)
#         結論は下さない(観測の記録に徹する)。
#
# 宇宙: n in {3,5,7,9,11}(v1 と同一)。u・c の平方類・c_mu には触れない。
# 解釈しない。v1 ファイル(search/ihc-fixture.g・search/certs/ihc_fixture_20260728.json)は不変。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

Print("############################################################\n");
Print("# ihc-fixture-v2.g -- I-25 Ih(c_hat)=[2n-1,1] fixture v2 (n=3,5,7,9,11), F78-2.4 repair\n");
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

# 分解ヘルパー(v1 の分解ロジックを関数として単離・native/paper 両方に同一関数を適用する
# ことで「相互変換式をコード内で一箇所に固定」する: 変換自体は呼び出し側で conj := g / g^-1
# の選択としてのみ行い、分解アルゴリズムそのものは共通化する)
DecomposeConjugator := function(conj, Pn, n)
  local Agrp, qCandidates, qp, v, i, j, k, outer, dv1, dv2, dv3, qLabel, decompLabel, found;
  Agrp := Group(Pn.a1, Pn.a2, Pn.a3);;
  qCandidates := [ ["1", One(Pn.G)], ["q1", Pn.q1], ["q2", Pn.q2], ["q3", Pn.q3] ];;
  dv1 := fail;;  dv2 := fail;;  dv3 := fail;;  qLabel := "n/a";;  decompLabel := "n/a";;  found := false;;
  for qp in qCandidates do
    v := conj * Inverse(qp[2]);;
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

# native/paper 分解を比較し、判別根拠を機械的に分類する(結論は下さない・観測のみ)
DiscriminateDecomps := function(nativeDec, paperDec)
  if not (nativeDec.found and paperDec.found) then
    return "not_applicable: at least one of native/paper decomposition not found";;
  fi;
  if nativeDec.qLabel = paperDec.qLabel and nativeDec.dv2 = paperDec.dv2
     and nativeDec.dv3 = paperDec.dv3 and nativeDec.dv1 = paperDec.dv1 then
    return "identical: native decomposition equals paper decomposition exactly";;
  fi;
  if nativeDec.qLabel = paperDec.qLabel and nativeDec.dv2 = paperDec.dv2
     and nativeDec.dv3 = paperDec.dv3 and nativeDec.dv1 = -paperDec.dv1 then
    return "dv1_negated_only: qLabel/dv2/dv3 identical, dv1 signs are exact negatives of each other (empirical pattern consistent with, but not independently proved equal to, the native<->paper inverse-conjugator relation; not asserted as harmless without further proof)";;
  fi;
  return "irregular_pattern: native and paper decompositions differ in qLabel and/or dv2/dv3 (not merely a dv1 sign flip) -- true drift not ruled out";;
end;;

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

  # ---- (3) inner automorphism 検索(native conjugator: GAP 規約 X^g=g^-1 X g をそのまま満たす g) ----
  innerFound := false;;  nativeG := fail;;
  for g in Elements(G) do
    if Xg^g = Xg^u and Yg^g = Yg^u then
      innerFound := true;;  nativeG := g;;  break;;
    fi;
  od;
  Print("[", PF(innerFound), "] (3) Phi_{2n-1,1} は inner (exists g in G_n: X^g=X^u, Y^g=Y^u, GAP規約)\n");

  # ---- (F78-2.4 修理 (1)(2)): native/paper conjugator を別欄に持ち、変換式をここ1箇所に固定 ----
  # 紙面規約 inn(h)(X) := h X h^-1. GAP規約 X^g := g^-1 X g. 両者を同一自己同型に対して
  # 解くと g^-1 X g = h X h^-1 、すなわち h = g^-1 (この1行が相互変換式の唯一の定義箇所)。
  nativeDecomp := rec(found:=false, dv1:=fail, dv2:=fail, dv3:=fail, qLabel:="n/a", decompLabel:="n/a");;
  paperDecomp := rec(found:=false, dv1:=fail, dv2:=fail, dv3:=fail, qLabel:="n/a", decompLabel:="n/a");;
  paperG := fail;;
  discrimination := "not_applicable: inner automorphism not found";;
  matchesPredictedFormExact := false;;
  if innerFound then
    paperG := nativeG^-1;;
    nativeDecomp := DecomposeConjugator(nativeG, Pn, n);;
    paperDecomp := DecomposeConjugator(paperG, Pn, n);;
    discrimination := DiscriminateDecomps(nativeDecomp, paperDecomp);;
    matchesPredictedFormExact := paperDecomp.found and (paperDecomp.qLabel = "q3")
      and (paperDecomp.dv1 = 1) and (paperDecomp.dv2 = 0) and (paperDecomp.dv3 = 0);;
  fi;
  # 旧来(v1, native conjugator を予測分解と緩く照合)の値も継続比較のために保持する
  matchesPredictedFormLoose := nativeDecomp.found and (nativeDecomp.qLabel = "q3")
    and (nativeDecomp.dv2 = 0) and (nativeDecomp.dv3 = 0);;

  Print("  native(GAP規約)分解: ", nativeDecomp.decompLabel, "\n");
  Print("  paper(紙面規約=h=g^-1)分解: ", paperDecomp.decompLabel, "\n");
  Print("  [", PF(matchesPredictedFormLoose), "] v1 相当(緩い・dv1未検査): qLabel=q3,dv2=0,dv3=0 のみ\n");
  Print("  [", PF(matchesPredictedFormExact), "] v2 exact(dv1まで検査): paper分解=(1,0,0)*q3 予測と一致\n");
  Print("  discrimination: ", discrimination, "\n");

  Add(results, rec(
    n:=n, m:=m, u:=u, n_ord:=Nord,
    charming:=charmingOK, hex310:=hex310, hex311:=hex311, surjective:=surj,
    is_shadow:=isShadow, order2:=order2,
    inner_found:=innerFound,
    native_decomp:=nativeDecomp.decompLabel, native_q_label:=nativeDecomp.qLabel,
    native_dv1:=nativeDecomp.dv1, native_dv2:=nativeDecomp.dv2, native_dv3:=nativeDecomp.dv3,
    paper_decomp:=paperDecomp.decompLabel, paper_q_label:=paperDecomp.qLabel,
    paper_dv1:=paperDecomp.dv1, paper_dv2:=paperDecomp.dv2, paper_dv3:=paperDecomp.dv3,
    matches_predicted_form_loose_v1:=matchesPredictedFormLoose,
    matches_predicted_form_exact:=matchesPredictedFormExact,
    discrimination:=discrimination
  ));;
od;;

# ====================================================================
# 総括表
# ====================================================================
Print("\n############################################################\n");
Print("# 総括: I-25 判定表 v2 (25判定 + 第五判定 exact 版)\n");
Print("############################################################\n");
Print("n  | charming | is_shadow | order2 | inner | loose(v1) | exact(v2) | native_decomp | paper_decomp | discrimination\n");
for r in results do
  Print(r.n, "  | ", PF(r.charming), " | ", PF(r.is_shadow), " | ", PF(r.order2), " | ",
        PF(r.inner_found), " | ", PF(r.matches_predicted_form_loose_v1), " | ",
        PF(r.matches_predicted_form_exact), " | ", r.native_decomp, " | ", r.paper_decomp,
        " | ", r.discrimination, "\n");
od;

t1 := GAPLIB_WallElapsedMs();;
Print("\n経過(壁時計) = ", (t1-t0)/1000.0, " s\n");

# ====================================================================
# 証明書 JSON
# ====================================================================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_ihc_v2.txt";;
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

ResultToJson := function(r)
  return Concatenation(
    "{\"n\":", String(r.n), ",\"m\":", String(r.m), ",\"u\":", String(r.u),
    ",\"n_ord\":", String(r.n_ord),
    ",\"charming\":", JB(r.charming),
    ",\"hex310\":", JB(r.hex310), ",\"hex311\":", JB(r.hex311),
    ",\"surjective\":", JB(r.surjective),
    ",\"is_shadow\":", JB(r.is_shadow),
    ",\"order2\":", JB(r.order2),
    ",\"inner_found\":", JB(r.inner_found),
    ",\"native_decomp\":", JStr(r.native_decomp),
    ",\"native_q_label\":", JStr(r.native_q_label),
    ",\"native_dv1\":", FieldToJson(r.native_dv1),
    ",\"native_dv2\":", FieldToJson(r.native_dv2),
    ",\"native_dv3\":", FieldToJson(r.native_dv3),
    ",\"paper_decomp\":", JStr(r.paper_decomp),
    ",\"paper_q_label\":", JStr(r.paper_q_label),
    ",\"paper_dv1\":", FieldToJson(r.paper_dv1),
    ",\"paper_dv2\":", FieldToJson(r.paper_dv2),
    ",\"paper_dv3\":", FieldToJson(r.paper_dv3),
    ",\"matches_predicted_form_loose_v1\":", JB(r.matches_predicted_form_loose_v1),
    ",\"matches_predicted_form_exact\":", JB(r.matches_predicted_form_exact),
    ",\"discrimination\":", JStr(r.discrimination),
    "}"
  );
end;;

resultsJson := JArr(List(results, ResultToJson));;

scriptSha256 := ComputeSha256File("search/ihc-fixture-v2.g");;

cert := Concatenation(
  "{\"schema\":\"ihc-fixture/v2\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/ihc-fixture-v2.g\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"universe\":{\"n_values\":[3,5,7,9,11]}",
  ",\"design_source\":\"ideas/ideas_005_panorama.md I-25 (裁定144 採用) + sol/sol_reply_78_math5.md F78-2.4 (native/paper conjugator分離 + dv1 exact 検査 + 判別根拠 修理)\"",
  ",\"notation_note\":\"[m,f]=1 は f=Identity(G_n) (week1-定義ノート.md L163 の f in F2/N_F2 の恒等コセット). ",
   "native_conjugator = GAP規約 X^g=g^-1 X g をそのまま満たす g(v1 の innerG に相当・ブルートフォース探索で発見). ",
   "paper_conjugator = 紙面規約 inn(h)(X)=h X h^-1 をそのまま満たす h. 変換式は g^-1 X g = h X h^-1 より h = g^-1",
   "(この1関係だけがコード中で相互変換を定義する箇所). matches_predicted_form_exact は paper_conjugator の",
   "分解を oddH SS11.2 予測 (dv1,dv2,dv3,qLabel)=(1,0,0,q3) と exact 照合する(v1/loose は dv1 を検査していなかった).",
   "discrimination は native/paper 分解の関係を機械的に3分類する(identical/dv1_negated_only/irregular_pattern)-- ",
   "結論(convention artifact か真の drift か)は下さない、観測の記録のみ。\"",
  ",\"results\":", resultsJson,
  ",\"elapsed_wall_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/ihc_fixture_v2_20260729.json";;
WriteFile(outPath, cert);;

Print("\n証明書を書き出した: ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
Print("\nIHC-FIXTURE-V2 DONE\n");
QUIT;
