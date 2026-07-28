# c2f-probe2.g -- FINDING C2F 第2段: M_Q, M_3 + 全窓での B3/N 水準単射性
# 核が F2/N_F2 水準でのみ現れ、B3/N 水準では消えることを機械で確定する。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

Print("############################################################\n");
Print("# c2f-probe2: M_Q / M_3 + B3/N 水準単射性\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;

EvalWordIn := function(word, xImg, yImg)
  local lst, letter;
  lst := [];
  for letter in word do
    if letter[1] = "x" then Add(lst, xImg^letter[2]);
    else Add(lst, yImg^letter[2]); fi;
  od;
  if Length(lst) = 0 then return xImg^0; fi;
  return AbstractProd(lst);
end;;

Analyze2 := function(name, qrec, shadows, doB3)
  local G, elts, n, idxDict, i, Nord, Z, D, recs, sh, u, PhiHom, images, img, j,
        fkeys, kernel, s, S1, S2, X3, Y3, Delta, Cc, ordS1, Gf, pairs, key,
        lhs, rhs, h33, h34, b3ok, nb3, m, f, wOK, ff, lab;
  Print("\n============================================================\n");
  Print("# ", name, "\n");
  Print("============================================================\n");
  G := qrec.G;  elts := Elements(G);  n := Length(elts);
  idxDict := NewDictionary(elts[1], true);
  for i in [1..n] do AddDictionary(idxDict, elts[i], i); od;
  Nord := Lcm(Order(qrec.x), Order(qrec.y));
  Z := Centre(G);  D := DerivedSubgroup(G);
  Print("|G| = ", n, "  ord(x)=", Order(qrec.x), " ord(y)=", Order(qrec.y),
        " Nord=", Nord, "  ord(c in G)=", Order(qrec.c), "\n");
  Print("|Z(G)|=", Size(Z), " |[G,G]|=", Size(D), " [G,G]<=Z(G)? ", IsSubset(Z,D),
        "  |Z(G) cap [G,G]| = ", Size(Intersection(Z,D)), "\n");
  Print("shadow 総数 = ", Length(shadows), "\n");

  # --- Phi 構成 ---
  recs := [];
  for sh in shadows do
    u := 2*sh.m+1;
    PhiHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y],
                [qrec.x^u, AbstractProd([sh.f^-1, qrec.y^u, sh.f])]);
    if PhiHom = fail or not IsBijective(PhiHom) then Error("Phi bad m=", sh.m); fi;
    images := [];
    for i in [1..n] do
      img := Image(PhiHom, elts[i]);
      images[i] := LookupDictionary(idxDict, img);
    od;
    Add(recs, rec(m:=sh.m, f:=sh.f, word:=sh.word, u:=u, perm:=PermList(images)));
  od;

  # --- ファイバと核 ---
  fkeys := [];
  for i in [1..Length(recs)] do
    if Position(fkeys, recs[i].perm) = fail then Add(fkeys, recs[i].perm); fi;
  od;
  kernel := Filtered([1..Length(recs)], i -> recs[i].perm = ());
  Print("|shadow|=", Length(recs), "  |Im(GT->Aut(G_N))|=", Length(fkeys),
        "  |ker|=", Length(kernel), "\n");
  Print("核元の座標:\n");
  for i in kernel do
    s := recs[i];
    Print("   m=", s.m, " u=", s.u, " u mod Nord=", s.u mod Nord,
          " | f=1? ", s.f = Identity(G), " ord(f)=", Order(s.f),
          " f in Z(G)? ", s.f in Z, " f in [G,G]? ", s.f in D,
          " f_word=", s.word, "\n");
  od;

  # --- BFS 語の自己整合(語 -> f の再現)---
  wOK := true;
  for i in [1..Length(recs)] do
    if EvalWordIn(recs[i].word, qrec.x, qrec.y) <> recs[i].f then wOK := false; fi;
  od;
  Print("BFS 語の自己整合(word -> f 再現): ", PF(wOK), "\n");

  # --- B3/N 水準 ---
  if doB3 then
    lab := BuildQTGeneral(G, qrec.x, qrec.y, qrec.c);
    S1 := lab.s1;  S2 := lab.s2;
    X3 := S1^2;  Y3 := S2^2;
    Delta := AbstractProd([S1,S2,S1]);  Cc := Delta^2;
    ordS1 := Order(S1);
    Print("B3/N: braid 関係 ", PF(AbstractProd([S1,S2,S1]) = AbstractProd([S2,S1,S2])),
          "  |<X,Y>|=", Size(Group(X3,Y3)), " (=|G|? ", Size(Group(X3,Y3)) = n, ")",
          "  ord(sigma_1)=", ordS1, "  ord(c)=", Order(Cc), "\n");
    b3ok := true;  pairs := [];
    for i in [1..Length(recs)] do
      m := recs[i].m;  u := recs[i].u;
      Gf := EvalWordIn(recs[i].word, X3, Y3);
      lhs := AbstractProd([S1^u, Gf^-1, S2^u, Gf]);
      rhs := AbstractProd([Gf^-1, S1, S2, X3^(-m), Cc^m]);
      h33 := (lhs = rhs);
      lhs := AbstractProd([Gf^-1, S2^u, Gf, S1^u]);
      rhs := AbstractProd([S2, S1, Y3^(-m), Cc^m, Gf]);
      h34 := (lhs = rhs);
      if not (h33 and h34) then
        b3ok := false;
        Print("   [FULL HEX FAIL] m=", m, " (3.3)=", h33, " (3.4)=", h34, "\n");
      fi;
      key := [S1^u, AbstractProd([Gf^-1, S2^u, Gf])];
      if Position(pairs, key) = fail then Add(pairs, key); fi;
    od;
    Print("full hexagon (3.3)(3.4) in B3/N: ", PF(b3ok), " (", Length(recs), " shadows)\n");
    Print("**B3/N 水準の像** |{ (T(s1),T(s2)) }| = ", Length(pairs),
          "  (= |shadow| ", Length(recs), " ? ", Length(pairs) = Length(recs),
          ")  ==> GT(N) -> End(B3/N) 単射: ", PF(Length(pairs) = Length(recs)), "\n");
    for i in kernel do
      m := recs[i].m;  u := recs[i].u;
      Gf := EvalWordIn(recs[i].word, X3, Y3);
      Print("   核元 m=", m, ": T(s1)=s1^", u, " ≠ s1? ", S1^u <> S1,
            " ; T(s2) ≠ s2? ", AbstractProd([Gf^-1, S2^u, Gf]) <> S2,
            " ; f は B3/N の中心か? ", Gf in Centre(Group(S1,S2)), "\n");
    od;
  fi;
  return rec(name:=name, ns:=Length(recs), ni:=Length(fkeys), nk:=Length(kernel));
end;;

summary := [];;

# ---- M_Q (stage 1b: G3 x_{C2^2} Q8, 17 点, |Q_M| = 216) ----
gn3_1b := MakeGn(3);;
q8rec_1b := MakeQ8();;
xhatMQ := PermList(Concatenation(List([1..9], j -> j^gn3_1b.x), List([1..8], j -> 9 + (j^q8rec_1b.x))));;
yhatMQ := PermList(Concatenation(List([1..9], j -> j^gn3_1b.y), List([1..8], j -> 9 + (j^q8rec_1b.y))));;
chatMQ := ();;   # c: G3 側は psi_3(c)=(1,1,1) で自明、Q8 側も MakeQ8 の c = 恒等 -> 全体で恒等
QM_MQ := Group(xhatMQ, yhatMQ);;
Print("M_Q: |Q_M| = ", Size(QM_MQ), " (期待 216)\n");
qrecMQ := rec(x:=xhatMQ, y:=yhatMQ, c:=chatMQ, G:=QM_MQ);;
NordMQ := Lcm(Order(xhatMQ), Order(yhatMQ));;
charmingMQ := Filtered([0..NordMQ-1], mm -> Gcd(2*mm+1, NordMQ) = 1);;
gtMQ := EnumerateReducedHexagon(qrecMQ, charmingMQ);;
Add(summary, Analyze2("M_Q (K^(3) cap N_Q, |Q_M|=216)", qrecMQ, gtMQ.shadows, true));;

# ---- N_A 対照 (A5, isolated 証明書・一致) ----
XhatA1 := (1,3,2,4,5);;
YhatA1 := (1,3,4,5,2);;
A5grp := Group(XhatA1, YhatA1);;
qrecNA := rec(x:=XhatA1, y:=YhatA1, c:=(), G:=A5grp);;
NordNA := Lcm(Order(XhatA1), Order(YhatA1));;
charmingNA := Filtered([0..NordNA-1], mm -> Gcd(2*mm+1, NordNA) = 1);;
gtNA := EnumerateReducedHexagon(qrecNA, charmingNA);;
Add(summary, Analyze2("N_A 対照 (A5)", qrecNA, gtNA.shadows, true));;

# ---- M_3 (stage 3: G3 x P3, |Q_M| = 3456) ----
gn3_3 := MakeGn(3);;
p3rec_3 := MakeP3();;
DP3 := DirectProduct(gn3_3.G, p3rec_3.G);;
emb1_3 := Embedding(DP3, 1);;
emb2_3 := Embedding(DP3, 2);;
xhatM3 := Image(emb1_3, gn3_3.x) * Image(emb2_3, p3rec_3.x);;
yhatM3 := Image(emb1_3, gn3_3.y) * Image(emb2_3, p3rec_3.y);;
chatM3 := Identity(DP3);;   # 両因子とも c は自明
QM_M3 := Group(xhatM3, yhatM3);;
Print("\nM_3: |Q_M| = ", Size(QM_M3), " (期待 3456)  ord(c)=", Order(chatM3), "\n");
qrecM3 := rec(x:=xhatM3, y:=yhatM3, c:=chatM3, G:=QM_M3);;
NordM3 := Lcm(Order(xhatM3), Order(yhatM3));;
charmingM3 := Filtered([0..NordM3-1], mm -> Gcd(2*mm+1, NordM3) = 1);;
gtM3 := EnumerateReducedHexagon(qrecM3, charmingM3);;
Add(summary, Analyze2("M_3 (K^(3) cap N_3, |Q_M|=3456)", qrecM3, gtM3.shadows, false));;

Print("\n############################################################\n");
for r in summary do
  Print(r.name, " : |shadow|=", r.ns, " |Im|=", r.ni, " |ker|=", r.nk, "\n");
od;
t1 := GAPLIB_WallElapsedMs();;
Print("\n経過(壁時計) = ", (t1-t0)/1000.0, " s\n");
Print("\nC2F-PROBE2 DONE\n");
QUIT;
