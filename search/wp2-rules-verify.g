# WP2: 司令塔導出の transversal 規則 12 個の機械検算
# (i) 忠実 Artin 表現 B3 -> Aut(F3) で恒等式 t*s = p*t' を検証
# (ii) 12n 点モデル(n=5,8)の較正: braid・位数 6|G_n|・psi_n 座標との整合

F3 := FreeGroup("a1", "a2", "a3");;
gens := GeneratorsOfGroup(F3);;
a1 := gens[1];; a2 := gens[2];; a3 := gens[3];;

# Artin 作用(語は左から順に適用 = 右作用合成)
S1 := [ a1*a2*a1^-1, a1, a3 ];;      # sigma1
S2 := [ a1, a2*a3*a2^-1, a2 ];;      # sigma2
S1i := [ a2, a2^-1*a1*a2, a3 ];;     # sigma1^-1
S2i := [ a1, a3, a3^-1*a2*a3 ];;     # sigma2^-1

IdAut := [ a1, a2, a3 ];;
Comp := function(A, B)   # A then B
  return List(A, w -> MappedWord(w, gens, B));
end;;
AutOfWord := function(word)   # word = list over {1,-1,2,-2} (σ1, σ1^-1, σ2, σ2^-1)
  local A, k, T;
  A := IdAut;
  for k in word do
    if k = 1 then T := S1; elif k = -1 then T := S1i;
    elif k = 2 then T := S2; else T := S2i; fi;
    A := Comp(A, T);
  od;
  return A;
end;;

# 語の部品
Wx := [1,1];;  Wy := [2,2];;  Wc := [1,2,1,1,2,1];;
Wxi := [-1,-1];;  Wyi := [-2,-2];;
W_yixic := Concatenation(Wyi, Wxi, Wc);;   # y^-1 x^-1 c
W_xiyic := Concatenation(Wxi, Wyi, Wc);;   # x^-1 y^-1 c
Tw := [ [], [1], [2], [1,2], [2,1], [1,2,1] ];;   # T の語(e, s1, s2, s1s2, s2s1, Delta)

# 規則表: rules[sigma][t] = [p の語, t' の番号]
rulesS1 := [ [ [], 2 ], [ Wx, 1 ], [ [], 5 ], [ [], 6 ], [ W_xiyic, 3 ], [ Wy, 4 ] ];;
rulesS2 := [ [ [], 3 ], [ [], 4 ], [ Wy, 1 ], [ W_yixic, 2 ], [ [], 6 ], [ Wx, 5 ] ];;

fails := 0;;
for t in [1..6] do
  for sg in [1, 2] do
    if sg = 1 then rule := rulesS1[t]; sw := [1]; else rule := rulesS2[t]; sw := [2]; fi;
    lhs := AutOfWord(Concatenation(Tw[t], sw));
    rhs := AutOfWord(Concatenation(rule[1], Tw[rule[2]]));
    ok := (lhs = rhs);
    Print("規則 (t=", t, ", sigma", sg, ") -> (p, t'=", rule[2], "): ", ok, "\n");
    if not ok then fails := fails + 1; fi;
  od;
od;
if fails = 0 then Print("(i) 12 恒等式 ALL VERIFIED (Artin faithful rep)\n");
else Print("(i) FAILURES: ", fails, "\n"); fi;

# ---------- (ii) 12n 点モデルの較正 ----------
MakeDn := function(n)
  local r, s;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  return [r, s];
end;;

CalibrateN := function(n)
  local rs, r, s, DnEl, pos, phi, phiOfWord, np, imgS1, imgS2, i, d, t, pt,
        s1p, s2p, G, expected, x, y, c, Gn, tr, xt, yt, hom, PBpart, Nord;
  rs := MakeDn(n);  r := rs[1];  s := rs[2];
  DnEl := Elements(Group(r, s));
  pos := function(g) return Position(DnEl, g); end;
  # phi: x -> s, y -> rs (= GAP の s*r), c -> 1
  phiOfWord := function(word)   # word over {1,-1,2,-2} は braid 語ではなく PB3 語部品なので
    return fail; end;;          # 使わない(下で直接値を与える)
  phi := rec( x := s, y := s*r, xi := s^-1, yi := (s*r)^-1 );
  # 規則の p 値(braid 語でなく既知の x,y,c 語だから直接評価)
  # p in {1, x, y, x^-1 y^-1 c, y^-1 x^-1 c}, phi(c) = 1
  # S1: t1->(1,2) t2->(x,1) t3->(1,5) t4->(1,6) t5->(x^-1 y^-1, 3) t6->(y,4)
  # S2: t1->(1,3) t2->(1,4) t3->(y,1) t4->(y^-1 x^-1, 2) t5->(1,6) t6->(x,5)
  np := Length(DnEl);   # 2n
  imgS1 := List([1..6*np], k -> 0);
  imgS2 := List([1..6*np], k -> 0);
  for t in [1..6] do
    for i in [1..np] do
      d := DnEl[i];
      pt := (t-1)*np + i;
      # sigma1
      if t = 1 then imgS1[pt] := (2-1)*np + pos(d);
      elif t = 2 then imgS1[pt] := (1-1)*np + pos(d * phi.x);
      elif t = 3 then imgS1[pt] := (5-1)*np + pos(d);
      elif t = 4 then imgS1[pt] := (6-1)*np + pos(d);
      elif t = 5 then imgS1[pt] := (3-1)*np + pos(d * phi.xi * phi.yi);
      else imgS1[pt] := (4-1)*np + pos(d * phi.y);
      fi;
      # sigma2
      if t = 1 then imgS2[pt] := (3-1)*np + pos(d);
      elif t = 2 then imgS2[pt] := (4-1)*np + pos(d);
      elif t = 3 then imgS2[pt] := (1-1)*np + pos(d * phi.y);
      elif t = 4 then imgS2[pt] := (2-1)*np + pos(d * phi.yi * phi.xi);
      elif t = 5 then imgS2[pt] := (6-1)*np + pos(d);
      else imgS2[pt] := (5-1)*np + pos(d * phi.x);
      fi;
    od;
  od;
  s1p := PermList(imgS1);  s2p := PermList(imgS2);
  Print("n=", n, "  braid 関係: ", s1p*s2p*s1p = s2p*s1p*s2p, "\n");
  G := Group(s1p, s2p);
  if n mod 2 = 1 then expected := 6*4*n^3; else expected := 6*4*(n/2)^3; fi;
  Print("n=", n, "  |<s1,s2>| = ", Size(G), " (期待 6|G_n| = ", expected, ") ",
        Size(G) = expected, "\n");
  x := s1p^2;  y := s2p^2;  c := (s1p*s2p*s1p)^2;
  Print("n=", n, "  c = 1 (中心が消える): ", c = (), "\n");
  Nord := Lcm(Order(x), Order(y));
  Print("n=", n, "  N_ord = ", Nord, " (期待 lcm(n,2) = ", Lcm(n,2), ") ", Nord = Lcm(n,2), "\n");
  # PB3 部分と psi_n 座標(G_n)の同型: x -> (r,s,s), y -> (rs,r,rs)
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  xt := tr(r,1) * tr(s,2) * tr(s,3);
  yt := tr(s*r,1) * tr(r,2) * tr(s*r,3);
  Gn := Group(xt, yt);
  PBpart := Group(x, y);
  hom := GroupHomomorphismByImages(PBpart, Gn, [x, y], [xt, yt]);
  Print("n=", n, "  PB3 部分 ~ G_n(x->(r,s,s), y->(rs,r,rs) が同型): ",
        hom <> fail and IsBijective(hom), "\n");
end;;

for n in [5, 8] do CalibrateN(n); od;
QUIT;
