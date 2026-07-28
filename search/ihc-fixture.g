# search/ihc-fixture.g -- I-25 複素共役座標の fixture(裁定144・ideas_005_panorama.md I-25 節)
#
# Usage: .\gap.ps1 search\ihc-fixture.g
#
# 目的(発注書どおり): 各奇数 n in {3,5,7,9,11} で、shadow [2n-1, 1]
#   (正典 Rem 1.10 の複素共役候補: chi(c_hat) = -1 . f = 1) について機械確認する:
#   (1) charming 集合に属すること
#   (2) GT(K^(n)) の元として位数2であること
#   (3) Phi_{2n-1,1} が inner であること(oddH SS11.2 の予測 inn((1-2k)e1 q3) 型)
#
# 表記の確定(実装前に固定した読み・司令塔が報告で明示する解釈):
#   week1-定義ノート.md L163: GT-pair [m,f] = (m + N_ord Z, f N_{F2}) in Z/N_ord x F2/N_{F2}
#   すなわち「f=1」は f が F2/N_{F2} の恒等コセット、つまり G_n = F2/N_{F2} の中で
#   F(f の値) = Identity(G_n) であることを意味する(paper の f 自体であり、
#   phifam_v1.md FINDING Phi1 に出る「conjugator (1-2k)e1 q3」とは別物 --
#   後者は Phi_{m,f} を inn(・) として実現する側の元であって f そのものではない)。
#   Thm 4.3 (docs/notes/w2fam_v1.md L33-36): F = (2k, -2k, kappa(m)) in A、
#   kappa(m) = m+1 (m 奇) / -m (m 偶)(抽出_Kn定義_D1.md L70)。
#   m = 2n-1 は奇数(n 奇)ゆえ kappa(2n-1) = 2n = 0 mod n。よって k=0 で F=(0,0,0)=identity。
#   ゆえ shadow [2n-1, 1] は Thm 4.3 のパラメータ k=0 の instance として存在するはず、というのが
#   本 fixture の机上前提(candidate)。GAP は f = Identity(G_n) を直接使って独立に検算する
#   (この前提を仮定して埋め込むのではなく、f=Identity(G_n) が実際に簡約 hexagon + 全射性を
#   満たすかを独立に確認する)。
#
# 再利用(探索器内の共有・裁定どおり):
#   search/gaplib_common.g のヘルパー。
#   search/k9-package.g の BuildPn(n)(P_n = A rtimes Q の座標辞書つき具体表現)-- 逐語コピー
#   (BuildPn 自体は AbstractProd 経由で規約検算込みで構成される)。
#   search/week3-battery-common.g の AbstractProd/PF/JSON ヘルパー。
#
# 宇宙: n in {3,5,7,9,11}(発注書の事前登録どおり)。u・c の平方類・c_mu には触れない
# (本 fixture は複素共役の座標のみを扱い、封印対象に一切触れない)。
# 解釈しない(観測の記録に徹する)。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

Print("############################################################\n");
Print("# ihc-fixture.g -- I-25 Ih(c_hat) = [2n-1,1] fixture (n=3,5,7,9,11)\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;

# ====================================================================
# BuildPn(n) -- k9-package.g より逐語コピー(座標辞書つき具体表現)
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

  # ---- shadow validity: f = Identity(G) directly (no BFS over D-words needed --
  #      Identity(G) is trivially in [F2,F2]/N; we test hexagon+generation directly) ----
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
  genB := AbstractProd([f^-1, Yg^u, f]);;   # f=1 なので genB = Y^u だが規約に忠実に AbstractProd を使う
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

  # ---- (3) inner automorphism 検索(全 |G| 元の brute force) ----
  innerFound := false;;  innerG := fail;;
  for g in Elements(G) do
    if Xg^g = Xg^u and Yg^g = Yg^u then
      innerFound := true;;  innerG := g;;  break;;
    fi;
  od;
  Print("[", PF(innerFound), "] (3) Phi_{2n-1,1} は inner (exists g in G_n: X^g=X^u, Y^g=Y^u)\n");

  # ---- 分解(診断: (v1,v2,v3)*q_j 形への同定・oddH SS11.2 予測との突合) ----
  decompLabel := "n/a";;
  qLabel := "n/a";;  dv1 := fail;;  dv2 := fail;;  dv3 := fail;;
  matchesPredictedForm := false;;
  if innerFound then
    Agrp := Group(Pn.a1, Pn.a2, Pn.a3);;
    qCandidates := [ ["1", One(G)], ["q1", Pn.q1], ["q2", Pn.q2], ["q3", Pn.q3] ];;
    for qp in qCandidates do
      v := innerG * Inverse(qp[2]);;
      if v in Agrp then
        outer := false;;
        for i in [0..n-1] do
          for j in [0..n-1] do
            for k in [0..n-1] do
              if Pn.a1^i * Pn.a2^j * Pn.a3^k = v then
                dv1 := i;;  dv2 := j;;  dv3 := k;;  qLabel := qp[1];;
                decompLabel := Concatenation("(", String(i), ",", String(j), ",", String(k),
                                             ")*", qp[1]);;
                outer := true;;  break;;
              fi;
            od;
            if outer then break; fi;
          od;
          if outer then break; fi;
        od;
        break;;
      fi;
    od;
    matchesPredictedForm := (qLabel = "q3") and (dv2 = 0) and (dv3 = 0);;
  fi;
  Print("  分解: innerG = ", decompLabel, "  (oddH SS11.2 予測型 (c)e1*q3 との一致 = ",
        PF(matchesPredictedForm), ")\n");

  Add(results, rec(
    n:=n, m:=m, u:=u, n_ord:=Nord,
    charming:=charmingOK, hex310:=hex310, hex311:=hex311, surjective:=surj,
    is_shadow:=isShadow, order2:=order2,
    inner_found:=innerFound, decomp:=decompLabel, q_label:=qLabel,
    dv1:=dv1, dv2:=dv2, dv3:=dv3, matches_predicted_form:=matchesPredictedForm
  ));;
od;;

# ====================================================================
# 総括表
# ====================================================================
Print("\n############################################################\n");
Print("# 総括: I-25 5点判定表\n");
Print("############################################################\n");
Print("n  | charming | is_shadow | order2 | inner | predicted_form | decomp\n");
for r in results do
  Print(r.n, "  | ", PF(r.charming), " | ", PF(r.is_shadow), " | ", PF(r.order2), " | ",
        PF(r.inner_found), " | ", PF(r.matches_predicted_form), " | ", r.decomp, "\n");
od;

t1 := GAPLIB_WallElapsedMs();;
Print("\n経過(壁時計) = ", (t1-t0)/1000.0, " s\n");

# ====================================================================
# 証明書 JSON
# ====================================================================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_ihc.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
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
    ",\"decomp\":", JStr(r.decomp),
    ",\"matches_predicted_form\":", JB(r.matches_predicted_form),
    "}"
  );
end;;

resultsJson := JArr(List(results, ResultToJson));;

scriptSha256 := ComputeSha256File("search/ihc-fixture.g");;

cert := Concatenation(
  "{\"schema\":\"ihc-fixture/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/ihc-fixture.g\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"universe\":{\"n_values\":[3,5,7,9,11]}",
  ",\"design_source\":\"ideas/ideas_005_panorama.md I-25 (裁定144 採用)\"",
  ",\"notation_note\":\"[m,f]=1 は f=Identity(G_n) (week1-定義ノート.md L163 の f in F2/N_F2 の恒等コセット). ",
   "phifam_v1.md FINDING Phi1 の 'conjugator (1-2k)e1 q3' は f そのものではなく Phi を inn(.) として ",
   "実現する側の元 -- 本fixtureはf=Identity(G_n)を直接使い独立に検算する。\"",
  ",\"results\":", resultsJson,
  ",\"elapsed_wall_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/ihc_fixture_20260728.json";;
WriteFile(outPath, cert);;

Print("\n証明書を書き出した: ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
Print("\nIHC-FIXTURE DONE\n");
QUIT;
