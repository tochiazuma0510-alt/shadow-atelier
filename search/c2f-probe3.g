# c2f-probe3.g -- FINDING C2F 仕上げ:
#  (A) B3/N 水準での GT(N) -> Aut(B3/N) 単射性を全 5 対象で確認
#  (B) GT(N) 自身(合成則 3.53)の導来長 = 像の導来長との差
#  (C) 機構の判定基準 Z(PB3/N) = 1 => Phi 単射 の検査(K(n) 族・N_A)

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

t0 := GAPLIB_WallElapsedMs();;
Print("############################################################\n");
Print("# c2f-probe3\n");
Print("############################################################\n");

EvalWordIn := function(word, xImg, yImg)
  local lst, letter;
  lst := [];
  for letter in word do
    if letter[1] = "x" then Add(lst, xImg^letter[2]); else Add(lst, yImg^letter[2]); fi;
  od;
  if Length(lst) = 0 then return xImg^0; fi;
  return AbstractProd(lst);
end;;

Probe3 := function(name, qrec, shadows, doB3)
  local G, elts, n, idxDict, i, Nord, recs, sh, u, PhiHom, images, img, j, fkeys,
        kernel, S1, S2, X3, Y3, Cc, pairs, key, Gf, m, lhs, rhs, h33, h34, b3ok,
        compTable, closed, a, b, na, nf, regPerms, GTabs, H, prev, len, kc, s, ZA;
  Print("\n=== ", name, " ===\n");
  G := qrec.G;  elts := Elements(G);  n := Length(elts);
  idxDict := NewDictionary(elts[1], true);
  for i in [1..n] do AddDictionary(idxDict, elts[i], i); od;
  Nord := Lcm(Order(qrec.x), Order(qrec.y));
  ZA := Centre(G);
  recs := [];
  for sh in shadows do
    u := 2*sh.m+1;
    PhiHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y],
                [qrec.x^u, AbstractProd([sh.f^-1, qrec.y^u, sh.f])]);
    images := [];
    for i in [1..n] do
      img := Image(PhiHom, elts[i]);
      images[i] := LookupDictionary(idxDict, img);
    od;
    Add(recs, rec(m:=sh.m, f:=sh.f, word:=sh.word, u:=u, perm:=PermList(images), hom:=PhiHom));
  od;
  fkeys := [];
  for i in [1..Length(recs)] do
    if Position(fkeys, recs[i].perm) = fail then Add(fkeys, recs[i].perm); fi;
  od;
  kernel := Filtered([1..Length(recs)], i -> recs[i].perm = ());
  Print("|Z(PB3/N)| = ", Size(ZA), "   |shadow|=", Length(recs),
        "  |Im in Aut(PB3/N)|=", Length(fkeys), "  |ker Phi|=", Length(kernel), "\n");

  # ---- (B) GT(N) 自身の導来長 ----
  compTable := [];  closed := true;
  for a in [1..Length(recs)] do
    compTable[a] := [];
    for b in [1..Length(recs)] do
      na := (2*recs[a].m*recs[b].m + recs[a].m + recs[b].m) mod Nord;
      nf := AbstractProd([recs[a].f, Image(recs[a].hom, recs[b].f)]);
      j := First([1..Length(recs)], k -> recs[k].m = na and recs[k].f = nf);
      if j = fail then closed := false; compTable[a][b] := 0;
      else compTable[a][b] := j; fi;
    od;
  od;
  Print("  (3.53) 合成の閉性: ", PF(closed), "\n");
  if closed then
    regPerms := List([1..Length(recs)], a -> PermList(compTable[a]));
    GTabs := Group(regPerms);
    H := GTabs;  len := 0;
    while not IsTrivial(H) and len < 10 do
      prev := H;  H := DerivedSubgroup(H);  len := len + 1;
      if Size(H) = Size(prev) then len := -1; break; fi;
    od;
    Print("  |GT(N)| = ", Size(GTabs), "   **GT(N) 自身の導来長 = ", len, "**",
          "   可換? ", IsAbelian(GTabs), "\n");
    kc := true;
    for i in kernel do
      for a in [1..Length(recs)] do
        if compTable[i][a] <> compTable[a][i] then kc := false; fi;
      od;
    od;
    Print("  ker は GT(N) の中心に含まれるか: ", kc,
          "   ker の元の位数: ", List(kernel, i -> Order(regPerms[i])), "\n");
  fi;

  # ---- (A) B3/N 水準単射性 ----
  if doB3 then
    b3ok := BuildQTGeneral(G, qrec.x, qrec.y, qrec.c);
    S1 := b3ok.s1;  S2 := b3ok.s2;
    X3 := S1^2;  Y3 := S2^2;  Cc := AbstractProd([S1,S2,S1])^2;
    Print("  B3/N: braid ", PF(AbstractProd([S1,S2,S1]) = AbstractProd([S2,S1,S2])),
          "  |<X,Y>|=", Size(Group(X3,Y3)), "  ord(sigma_1)=", Order(S1),
          "  ord(x)=", Order(X3), "  ord(c)=", Order(Cc), "\n");
    pairs := [];  b3ok := true;
    for i in [1..Length(recs)] do
      m := recs[i].m;  u := recs[i].u;  Gf := EvalWordIn(recs[i].word, X3, Y3);
      lhs := AbstractProd([S1^u, Gf^-1, S2^u, Gf]);
      rhs := AbstractProd([Gf^-1, S1, S2, X3^(-m), Cc^m]);
      h33 := (lhs = rhs);
      lhs := AbstractProd([Gf^-1, S2^u, Gf, S1^u]);
      rhs := AbstractProd([S2, S1, Y3^(-m), Cc^m, Gf]);
      h34 := (lhs = rhs);
      if not (h33 and h34) then b3ok := false;
        Print("   [FULL HEX FAIL] m=", m, " (3.3)=", h33, " (3.4)=", h34, "\n"); fi;
      key := [S1^u, AbstractProd([Gf^-1, S2^u, Gf])];
      if Position(pairs, key) = fail then Add(pairs, key); fi;
    od;
    Print("  full hexagon (3.3)(3.4) in B3/N: ", PF(b3ok), " (", Length(recs), "/",
          Length(recs), ")\n");
    Print("  **|Im in Aut(B3/N)| = ", Length(pairs), "**  単射? ",
          PF(Length(pairs) = Length(recs)), "\n");
  fi;
  return rec(name:=name);
end;;

# ---- N_Q ----
q8rec := MakeQ8();;
qrecNQ := rec(x:=q8rec.x, y:=q8rec.y, c:=q8rec.c, G:=q8rec.G);;
NordNQ := Lcm(Order(q8rec.x), Order(q8rec.y));;
gtNQ := EnumerateReducedHexagon(qrecNQ, Filtered([0..NordNQ-1], mm -> Gcd(2*mm+1, NordNQ)=1));;
Probe3("N_Q", qrecNQ, gtNQ.shadows, true);;

# ---- N_2 ----
p2rec := MakeHeis(4,2);;
qrecN2 := rec(x:=p2rec.x, y:=p2rec.y, c:=p2rec.c, G:=p2rec.G);;
NordN2 := Lcm(Order(p2rec.x), Order(p2rec.y));;
gtN2 := EnumerateReducedHexagon(qrecN2, Filtered([0..NordN2-1], mm -> Gcd(2*mm+1, NordN2)=1));;
Probe3("N_2", qrecN2, gtN2.shadows, true);;

# ---- N_3 ----
p3rec := MakeP3();;
qrecN3 := rec(x:=p3rec.x, y:=p3rec.y, c:=p3rec.c, G:=p3rec.G);;
NordN3 := Lcm(Order(p3rec.x), Order(p3rec.y));;
gtN3 := EnumerateReducedHexagon(qrecN3, Filtered([0..NordN3-1], mm -> Gcd(2*mm+1, NordN3)=1));;
Probe3("N_3", qrecN3, gtN3.shadows, true);;

# ---- M_Q(導来長のみ・B3 は probe2 で済) ----
gn3_1b := MakeGn(3);;  q8b := MakeQ8();;
xhatMQ := PermList(Concatenation(List([1..9], j -> j^gn3_1b.x), List([1..8], j -> 9 + (j^q8b.x))));;
yhatMQ := PermList(Concatenation(List([1..9], j -> j^gn3_1b.y), List([1..8], j -> 9 + (j^q8b.y))));;
qrecMQ := rec(x:=xhatMQ, y:=yhatMQ, c:=(), G:=Group(xhatMQ,yhatMQ));;
NordMQ := Lcm(Order(xhatMQ), Order(yhatMQ));;
gtMQ := EnumerateReducedHexagon(qrecMQ, Filtered([0..NordMQ-1], mm -> Gcd(2*mm+1, NordMQ)=1));;
Probe3("M_Q", qrecMQ, gtMQ.shadows, false);;

# ---- M_3(導来長のみ)----
gn3_3 := MakeGn(3);;  p3b := MakeP3();;
DP3 := DirectProduct(gn3_3.G, p3b.G);;
xhatM3 := Image(Embedding(DP3,1), gn3_3.x) * Image(Embedding(DP3,2), p3b.x);;
yhatM3 := Image(Embedding(DP3,1), gn3_3.y) * Image(Embedding(DP3,2), p3b.y);;
qrecM3 := rec(x:=xhatM3, y:=yhatM3, c:=Identity(DP3), G:=Group(xhatM3,yhatM3));;
NordM3 := Lcm(Order(xhatM3), Order(yhatM3));;
gtM3 := EnumerateReducedHexagon(qrecM3, Filtered([0..NordM3-1], mm -> Gcd(2*mm+1, NordM3)=1));;
Probe3("M_3", qrecM3, gtM3.shadows, false);;

# ---- (C) 判定基準の検査: Z(PB3/N) の位数一覧 ----
Print("\n############################################################\n");
Print("# (C) 判定基準: |Z(PB3/N)| と ker Phi の対応\n");
Print("############################################################\n");
BuildPn := function(n)
  local r, s, tr, a1, a2, a3, q1, q2, X, Y;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  a1 := tr(r,1);  a2 := tr(r,2);  a3 := tr(r,3);
  q1 := tr(s,2)*tr(s,3);  q2 := tr(s,1)*tr(s,3);
  X := AbstractProd([a1,q1]);  Y := AbstractProd([a1,a2,a3,q2]);
  return rec(X:=X, Y:=Y, G:=Group(a1,a2,a3,q1,q2));
end;;
for n in [3,5,7,9,11] do
  Pn := BuildPn(n);
  Print("  K(", n, "): |G_n| = ", Size(Pn.G), "  |Z(G_n)| = ", Size(Centre(Pn.G)), "\n");
od;
Print("  N_A : |A5| = 60  |Z| = ", Size(Centre(Group((1,3,2,4,5),(1,3,4,5,2)))), "\n");
zeta := (6,7,8,9,10);;
xMA5 := (1,3,2,4,5)*zeta^2;;  yMA5 := (1,3,4,5,2)*zeta^2;;
Print("  M_A5: |A5xC5| = ", Size(Group(xMA5,yMA5)), "  |Z| = ",
      Size(Centre(Group(xMA5,yMA5))), "\n");

t1 := GAPLIB_WallElapsedMs();;
Print("\n経過(壁時計) = ", (t1-t0)/1000.0, " s\n");
Print("\nC2F-PROBE3 DONE\n");
QUIT;
