# c2f-probe4.g -- M_3 の B3/N 水準確認(核元が sigma 水準で可視か)
SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
t0 := GAPLIB_WallElapsedMs();;

EvalWordIn := function(word, xImg, yImg)
  local lst, letter;
  lst := [];
  for letter in word do
    if letter[1] = "x" then Add(lst, xImg^letter[2]); else Add(lst, yImg^letter[2]); fi;
  od;
  if Length(lst) = 0 then return xImg^0; fi;
  return AbstractProd(lst);
end;;

gn3 := MakeGn(3);;  p3 := MakeP3();;
DP := DirectProduct(gn3.G, p3.G);;
xh := Image(Embedding(DP,1), gn3.x) * Image(Embedding(DP,2), p3.x);;
yh := Image(Embedding(DP,1), gn3.y) * Image(Embedding(DP,2), p3.y);;
G := Group(xh, yh);;
qrec := rec(x:=xh, y:=yh, c:=Identity(DP), G:=G);;
Nord := Lcm(Order(xh), Order(yh));;
gt := EnumerateReducedHexagon(qrec, Filtered([0..Nord-1], mm -> Gcd(2*mm+1,Nord)=1));;
Print("M_3: |G|=", Size(G), " Nord=", Nord, " shadows=", Length(gt.shadows), "\n");

lab := BuildQTGeneral(G, qrec.x, qrec.y, qrec.c);;
S1 := lab.s1;; S2 := lab.s2;;
X3 := S1^2;; Y3 := S2^2;; Cc := AbstractProd([S1,S2,S1])^2;;
Print("braid 関係: ", PF(AbstractProd([S1,S2,S1]) = AbstractProd([S2,S1,S2])),
      "  ord(sigma_1)=", Order(S1), " (期待 2*Nord=", 2*Nord, ")",
      "  ord(x)=", Order(X3), "  ord(c)=", Order(Cc), "\n");
Print("|<X,Y>| = ", Size(Group(X3,Y3)), " (= |G| ", Size(G), "? ",
      Size(Group(X3,Y3)) = Size(G), ")\n");

# full hexagon + B3 水準の像
pairs := [];; b3ok := true;;
for sh in gt.shadows do
  m := sh.m;; u := 2*m+1;; Gf := EvalWordIn(sh.word, X3, Y3);;
  if EvalWordIn(sh.word, qrec.x, qrec.y) <> sh.f then Error("word mismatch"); fi;
  h33 := AbstractProd([S1^u, Gf^-1, S2^u, Gf]) = AbstractProd([Gf^-1, S1, S2, X3^(-m), Cc^m]);;
  h34 := AbstractProd([Gf^-1, S2^u, Gf, S1^u]) = AbstractProd([S2, S1, Y3^(-m), Cc^m, Gf]);;
  if not (h33 and h34) then b3ok := false; Print("  [HEX FAIL] m=", m, "\n"); fi;
  key := [S1^u, AbstractProd([Gf^-1, S2^u, Gf])];;
  if Position(pairs, key) = fail then Add(pairs, key); fi;
od;
Print("full hexagon (3.3)(3.4) in B3/N: ", PF(b3ok), " (", Length(gt.shadows), " shadows)\n");
Print("**|Im in Aut(B3/N)| = ", Length(pairs), "**  (=|shadow| ", Length(gt.shadows), "? ",
      Length(pairs) = Length(gt.shadows), ")\n");

# 核元 [0, f0] の sigma 水準での可視性
f0word := [["x",1],["x",1],["y",1],["x",1],["y",1],["y",1],["x",1],["y",1]];;
Gf0 := EvalWordIn(f0word, X3, Y3);;
f0 := EvalWordIn(f0word, qrec.x, qrec.y);;
Print("核元 f0: ord=", Order(f0), " in Z(PB3/N)? ", f0 in Centre(G),
      " in [G,G]? ", f0 in DerivedSubgroup(G), "\n");
Print("  T(sigma_1)=sigma_1^1 = sigma_1 ? ", S1^1 = S1, "\n");
Print("  T(sigma_2)=f0^-1 sigma_2 f0 ≠ sigma_2 ? ",
      AbstractProd([Gf0^-1, S2, Gf0]) <> S2, "\n");
Print("  f0 は PB3/N の中心だが B3/N の中心か? ",
      AbstractProd([Gf0^-1, S1, Gf0]) = S1 and AbstractProd([Gf0^-1, S2, Gf0]) = S2, "\n");
t1 := GAPLIB_WallElapsedMs();;
Print("\n経過 = ", (t1-t0)/1000.0, " s\nC2F-PROBE4 DONE\n");
QUIT;
