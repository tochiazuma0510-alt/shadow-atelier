# c2f-probe.g -- FINDING C2F の白黒判定(数学者・委嘱 裁定146)
# 目的: |Im(GT(N) -> Aut(G_N))| = |GT(N)|/2 が (a) 真の核か (b) 構成の見落としか。
# 手順: 座標列挙 -> Phi 明示構成 -> ファイバ同定 -> 核元座標 -> B3/N 水準での区別
# 実行: .\gap.ps1 <このファイルの絶対パス>

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

Print("############################################################\n");
Print("# c2f-probe: FINDING C2F 白黒判定\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;

# --------------------------------------------------------------------
# helper: BFS 語を任意の (xImg,yImg) で評価(paper 積 = AbstractProd)
# --------------------------------------------------------------------
EvalWordIn := function(word, xImg, yImg)
  local lst, letter;
  lst := [];
  for letter in word do
    if letter[1] = 'x' or letter[1] = "x" then Add(lst, xImg^letter[2]);
    else Add(lst, yImg^letter[2]); fi;
  od;
  if Length(lst) = 0 then return xImg^0; fi;
  return AbstractProd(lst);
end;;

# helper: Phi_{m,f} を G 上の置換として実現
MakePhiPerm := function(qrec, elts, idxDict, m, f)
  local u, PhiHom, images, i, img;
  u := 2*m+1;
  PhiHom := GroupHomomorphismByImages(qrec.G, qrec.G, [qrec.x, qrec.y],
              [qrec.x^u, AbstractProd([f^-1, qrec.y^u, f])]);
  if PhiHom = fail then Error("Phi construction failed m=", m); fi;
  if not IsBijective(PhiHom) then Error("Phi not bijective m=", m); fi;
  images := [];
  for i in [1..Length(elts)] do
    img := Image(PhiHom, elts[i]);
    images[i] := LookupDictionary(idxDict, img);
  od;
  return rec(perm := PermList(images), hom := PhiHom);
end;;

# --------------------------------------------------------------------
# 主解析
# --------------------------------------------------------------------
AnalyzeWindow := function(name, qrec, shadows, doB3)
  local G, elts, n, idxDict, i, Nord, Z, D, recs, sh, pr, key, fibers, fkeys,
        kidx, kernel, j, s, phiId, nDistinct, dict2, seen, lab, u,
        S1, S2, X3, Y3, Delta, Cc, isoQ, Gf, np, b3ok, m, f, lhs, rhs,
        h33, h34, sig1img, sig2img, differs, compTable, closed, a, b, na, nf,
        posOf, prodIdx, regPerms, GTabs, dl, H, prev, len, kercentral,
        elemsB3, bfs, wordOf, kerElts, allf, ordS1;

  Print("\n============================================================\n");
  Print("# ", name, "\n");
  Print("============================================================\n");
  G := qrec.G;
  elts := Elements(G);
  n := Length(elts);
  idxDict := NewDictionary(elts[1], true);
  for i in [1..n] do AddDictionary(idxDict, elts[i], i); od;
  Nord := Lcm(Order(qrec.x), Order(qrec.y));
  Z := Centre(G);
  D := DerivedSubgroup(G);
  Print("|G| = ", n, "   ord(x) = ", Order(qrec.x), "   ord(y) = ", Order(qrec.y),
        "   Nord = lcm = ", Nord, "\n");
  if IsBound(qrec.c) then
    Print("ord(c-image in G) = ", Order(qrec.c), "  (c in N <=> 1)\n");
  fi;
  Print("|Z(G)| = ", Size(Z), "   |[G,G]| = ", Size(D),
        "   [G,G] <= Z(G)? ", IsSubset(Z, D), "\n");
  Print("shadow 総数 = ", Length(shadows), "\n");

  bfs := BFSWords(qrec);
  wordOf := bfs.wordOf;

  # ---- (1)(2) 座標列挙 + Phi 明示構成 ----
  Print("\n-- (1)(2) shadow 座標と Phi の生成元像 --\n");
  recs := [];
  for i in [1..Length(shadows)] do
    sh := shadows[i];
    pr := MakePhiPerm(qrec, elts, idxDict, sh.m, sh.f);
    Add(recs, rec(m := sh.m, f := sh.f, word := sh.word, perm := pr.perm, hom := pr.hom,
                  u := 2*sh.m+1));
  od;
  for i in [1..Length(recs)] do
    s := recs[i];
    Print("  [", i, "] m=", s.m, " u=2m+1=", s.u, " u mod Nord=", s.u mod Nord,
          " | f in Z(G)? ", s.f in Z, " f=1? ", s.f = Identity(G),
          " ord(f)=", Order(s.f), " f_word=", s.word, "\n");
    Print("        Phi(x)=x^", s.u, " ; Phi(y)=f^-1 y^", s.u, " f ; ",
          " Phi=id? ", s.perm = (), "\n");
  od;

  # ---- (3) 同一 Phi を与える対の同定 ----
  Print("\n-- (3) Phi のファイバ(同一自己同型を与える shadow の組) --\n");
  fibers := [];
  fkeys := [];
  for i in [1..Length(recs)] do
    j := Position(fkeys, recs[i].perm);
    if j = fail then
      Add(fkeys, recs[i].perm);
      Add(fibers, [i]);
    else
      Add(fibers[j], i);
    fi;
  od;
  Print("  |shadow| = ", Length(recs), "   |Im(Phi)| = ", Length(fkeys),
        "   比 = ", Length(recs), "/", Length(fkeys), "\n");
  Print("  ファイバの大きさの多重集合 = ", Collected(List(fibers, Length)), "\n");
  for i in [1..Length(fibers)] do
    if Length(fibers[i]) > 1 then
      Print("    fiber #", i, ": ", List(fibers[i], j -> [recs[j].m, recs[j].word]), "\n");
    fi;
  od;

  # ---- (4) 核 ----
  Print("\n-- (4) 核 ker(GT(N) -> Aut(G_N)) --\n");
  kernel := Filtered([1..Length(recs)], i -> recs[i].perm = ());
  Print("  |ker| = ", Length(kernel), "\n");
  kerElts := [];
  for i in kernel do
    s := recs[i];
    Add(kerElts, i);
    Print("    核元: m=", s.m, "  u=", s.u, "  u mod Nord=", s.u mod Nord,
          "  f_word=", s.word, "  f in Z(G)? ", s.f in Z,
          "  f=1? ", s.f = Identity(G), "  ord(f)=", Order(s.f), "\n");
  od;
  # 複素共役型 [Nord-1, 1] の所在
  j := First([1..Length(recs)], i -> recs[i].m = (Nord-1) and recs[i].f = Identity(G));
  if j = fail then
    Print("  [Nord-1, 1] は shadow に**現れない**\n");
  else
    Print("  [Nord-1, 1] = [", Nord-1, ",1] は shadow #", j, " ; Phi=id? ",
          recs[j].perm = (), "  (核に入るか)\n");
    Print("      Phi(x)=x^", recs[j].u, " = x^-1? ", qrec.x^(recs[j].u) = qrec.x^-1,
          " ; Phi(y)= y^-1? ",
          AbstractProd([recs[j].f^-1, qrec.y^(recs[j].u), recs[j].f]) = qrec.y^-1, "\n");
  fi;
  # u = -1 mod Nord となる全 shadow(chirality 候補)
  Print("  u ≡ -1 (mod Nord) の shadow: ",
        List(Filtered(recs, s -> (s.u mod Nord) = ((-1) mod Nord)), s -> [s.m, s.word]), "\n");

  # ---- (5) 合成則 (3.53) による GT(N) の群構造(閉性・核の中心性・導来長) ----
  Print("\n-- (5) 合成則 (3.53) による GT(N) 自身の群構造 --\n");
  compTable := [];
  closed := true;
  for a in [1..Length(recs)] do
    compTable[a] := [];
    for b in [1..Length(recs)] do
      na := (2*recs[a].m*recs[b].m + recs[a].m + recs[b].m) mod Nord;
      nf := AbstractProd([recs[a].f, Image(recs[a].hom, recs[b].f)]);
      j := First([1..Length(recs)], k -> recs[k].m = na and recs[k].f = nf);
      if j = fail then
        closed := false;
        Print("    [CLOSURE FAIL] (", recs[a].m, ",", recs[a].word, ") o (",
              recs[b].m, ",", recs[b].word, ") -> m=", na, " not in shadow set\n");
        compTable[a][b] := 0;
      else
        compTable[a][b] := j;
      fi;
    od;
  od;
  Print("  合成の閉性: ", PF(closed), "\n");
  if closed then
    regPerms := List([1..Length(recs)], a -> PermList(compTable[a]));
    GTabs := Group(regPerms);
    Print("  |GT(N)| (合成則から) = ", Size(GTabs), "  (= shadow 数 ", Length(recs), "? ",
          Size(GTabs) = Length(recs), ")\n");
    # 導来長
    H := GTabs; len := 0;
    while not IsTrivial(H) and len < 10 do
      prev := H; H := DerivedSubgroup(H); len := len + 1;
      if Size(H) = Size(prev) then len := -1; break; fi;
    od;
    Print("  GT(N) の導来長 = ", len, "\n");
    # 核の中心性・部分群性
    if Length(kernel) > 0 then
      kercentral := true;
      for i in kernel do
        for a in [1..Length(recs)] do
          if compTable[i][a] <> compTable[a][i] then kercentral := false; fi;
        od;
      od;
      Print("  核は GT(N) の中心に入るか: ", kercentral, "\n");
      Print("  核元の位数(合成則): ",
            List(kernel, i -> Order(regPerms[i])), "\n");
    fi;
  fi;

  # ---- (6) B3/N 水準での区別(決定的検査) ----
  if doB3 then
    Print("\n-- (6) B3/N 水準(sigma_1 を持つ本来の水準)での検査 --\n");
    np := n;
    if not IsBound(qrec.c) then
      Print("    [SKIP] qrec.c が無い\n");
    else
      lab := BuildQTGeneral(G, qrec.x, qrec.y, qrec.c);
      S1 := lab.s1; S2 := lab.s2;
      Print("    |B3/N| = ", Size(Group(S1,S2)), "  (期待 6*|G| = ", 6*np, ")\n");
      Print("    braid 関係 s1s2s1 = s2s1s2 : ",
            PF(AbstractProd([S1,S2,S1]) = AbstractProd([S2,S1,S2])), "\n");
      X3 := S1^2; Y3 := S2^2;
      Delta := AbstractProd([S1,S2,S1]); Cc := Delta^2;
      ordS1 := Order(S1);
      Print("    ord(sigma_1 mod N) = ", ordS1, "  ord(x mod N) = ", Order(X3),
            "  ord(c mod N) = ", Order(Cc), "\n");
      isoQ := GroupHomomorphismByImages(G, Group(X3,Y3), [qrec.x,qrec.y],[X3,Y3]);
      if isoQ = fail or not IsBijective(isoQ) then
        Print("    [SKIP] Q -> <x,y> ⊂ B3/N の同型が作れない\n");
      else
        Print("    Q = PB3/N ↪ B3/N の同型: OK (|<X,Y>| = ", Size(Group(X3,Y3)), ")\n");
        b3ok := true;
        for i in [1..Length(recs)] do
          m := recs[i].m; u := recs[i].u; Gf := Image(isoQ, recs[i].f);
          # (3.3) sigma1^u f^-1 sigma2^u f = f^-1 sigma1 sigma2 x^-m c^m
          lhs := AbstractProd([S1^u, Gf^-1, S2^u, Gf]);
          rhs := AbstractProd([Gf^-1, S1, S2, X3^(-m), Cc^m]);
          h33 := (lhs = rhs);
          # (3.4) f^-1 sigma2^u f sigma1^u = sigma2 sigma1 y^-m c^m f
          lhs := AbstractProd([Gf^-1, S2^u, Gf, S1^u]);
          rhs := AbstractProd([S2, S1, Y3^(-m), Cc^m, Gf]);
          h34 := (lhs = rhs);
          if not (h33 and h34) then
            b3ok := false;
            Print("    [FULL HEX FAIL] m=", m, " f_word=", recs[i].word,
                  "  (3.3)=", h33, " (3.4)=", h34, "\n");
          fi;
        od;
        Print("    full hexagon (3.3)(3.4) in B3/N: ", PF(b3ok),
              " (", Length(recs), " shadows)\n");
        # T_{m,f} の生成元像で核元が識別されるか
        Print("    T_{m,f}(sigma_1), T_{m,f}(sigma_2) による核元の識別:\n");
        for i in kernel do
          m := recs[i].m; u := recs[i].u; Gf := Image(isoQ, recs[i].f);
          sig1img := S1^u;
          sig2img := AbstractProd([Gf^-1, S2^u, Gf]);
          differs := (sig1img <> S1) or (sig2img <> S2);
          Print("      核元 m=", m, " f_word=", recs[i].word,
                " : T(s1)=s1^", u, " ≠ s1 ? ", sig1img <> S1,
                " ; T(s2) ≠ s2 ? ", sig2img <> S2,
                " ==> B3/N 上で id と異なる? ", differs, "\n");
          Print("            u mod 2*Nord = ", u mod (2*Nord),
                " ; u mod ord(sigma_1)=", ordS1, " -> ", u mod ordS1, "\n");
        od;
      fi;
    fi;
  fi;
  return rec(name:=name, nshadow:=Length(recs), nimage:=Length(fkeys),
             nkernel:=Length(kernel), Nord:=Nord);
end;;

summary := [];;

# ====================================================================
# N_Q (最小例・stage 1a: Q8)
# ====================================================================
q8rec := MakeQ8();;
qrecNQ := rec(x:=q8rec.x, y:=q8rec.y, c:=q8rec.c, G:=q8rec.G);;
NordNQ := Lcm(Order(q8rec.x), Order(q8rec.y));;
charmingNQ := Filtered([0..NordNQ-1], mm -> Gcd(2*mm+1, NordNQ) = 1);;
gtNQ := EnumerateReducedHexagon(qrecNQ, charmingNQ);;
Add(summary, AnalyzeWindow("N_Q  (Q8, stage 1a)", qrecNQ, gtNQ.shadows, true));;

# ====================================================================
# N_2 (stage 2a: P2 = Heis(4,2))
# ====================================================================
p2rec := MakeHeis(4,2);;
qrecN2 := rec(x:=p2rec.x, y:=p2rec.y, c:=p2rec.c, G:=p2rec.G);;
NordN2 := Lcm(Order(p2rec.x), Order(p2rec.y));;
charmingN2 := Filtered([0..NordN2-1], mm -> Gcd(2*mm+1, NordN2) = 1);;
gtN2 := EnumerateReducedHexagon(qrecN2, charmingN2);;
Add(summary, AnalyzeWindow("N_2  (P2 = Heis(4,2), stage 2a)", qrecN2, gtN2.shadows, true));;

# ====================================================================
# N_3 (stage 2b: P3, order 128)
# ====================================================================
p3rec := MakeP3();;
qrecN3 := rec(x:=p3rec.x, y:=p3rec.y, c:=p3rec.c, G:=p3rec.G);;
NordN3 := Lcm(Order(p3rec.x), Order(p3rec.y));;
charmingN3 := Filtered([0..NordN3-1], mm -> Gcd(2*mm+1, NordN3) = 1);;
gtN3 := EnumerateReducedHexagon(qrecN3, charmingN3);;
Add(summary, AnalyzeWindow("N_3  (P3, order 128, stage 2b)", qrecN3, gtN3.shadows, true));;

# ====================================================================
# 対照: K(3) (Phi-fam 単射証明済み) -- 核が空であることの確認
# ====================================================================
BuildPn := function(n)
  local r, s, tr, a1, a2, a3, q1, q2, q3, X, Y, Xchk, Ychk, Gfull;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  a1 := tr(r,1);  a2 := tr(r,2);  a3 := tr(r,3);
  q1 := tr(s,2) * tr(s,3);
  q2 := tr(s,1) * tr(s,3);
  q3 := tr(s,1) * tr(s,2);
  X := AbstractProd([a1, q1]);
  Y := AbstractProd([a1, a2, a3, q2]);
  Xchk := tr(r,1) * tr(s,2) * tr(s,3);
  Ychk := tr(s*r,1) * tr(r,2) * tr(s*r,3);
  if X <> Xchk or Y <> Ychk then Error("BuildPn convention mismatch n=", n); fi;
  Gfull := Group(a1, a2, a3, q1, q2);
  return rec(n:=n, X:=X, Y:=Y, G:=Gfull);
end;;

P3n := BuildPn(3);;
qrecK3 := rec(x:=P3n.X, y:=P3n.Y, c:=(), G:=P3n.G);;
NordK3 := Lcm(Order(P3n.X), Order(P3n.Y));;
charmingK3 := Filtered([0..NordK3-1], mm -> Gcd(2*mm+1, NordK3) = 1);;
gtK3 := EnumerateReducedHexagon(qrecK3, charmingK3);;
Add(summary, AnalyzeWindow("K(3) 対照 (G_3, 単射既証)", qrecK3, gtK3.shadows, false));;

# ====================================================================
# 総括
# ====================================================================
Print("\n############################################################\n");
Print("# 総括\n");
Print("############################################################\n");
for r in summary do
  Print(r.name, " : Nord=", r.Nord, "  |shadow|=", r.nshadow,
        "  |Im|=", r.nimage, "  |ker|=", r.nkernel, "\n");
od;

t1 := GAPLIB_WallElapsedMs();;
Print("\n経過(壁時計) = ", (t1-t0)/1000.0, " s\n");
Print("\nC2F-PROBE DONE\n");
QUIT;
