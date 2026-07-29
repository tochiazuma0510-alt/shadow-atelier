## tail-8 minimal window: n=21, u=(13,2,2,2,2), a'=2^10 1, b'=3^7
## sample b' (class 3^7) and set a' = b'*u.  structconst = 4160.
## FAST test: a' has type 2^10 1  <=>  a'^2 = () and exactly 1 fixed point.
WacCyc := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;
WacBlock := function(blocks, len)
  local p, i, base;
  p := (); base := 0;
  for i in [1..blocks] do
    p := p * WacCyc(List([1..len], j -> base+j)); base := base + len;
  od;
  return p;
end;;
S21 := SymmetricGroup(21);; A21 := AlternatingGroup(21);;
uu := (1,2,3,4,5,6,7,8,9,10,11,12,13)*(14,15)*(16,17)*(18,19)*(20,21);;
a0 := WacBlock(10,2);;   # 2^10 1  (sample from THIS class: 300x better)
id := ();;
hits := 0;; gen := 0;; found := fail;;
uinv := uu^-1;;
for i in [1..6000000] do
  if i mod 2000000 = 0 then Print("  ... ", i, " tries, hits=", hits, "\n"); fi;
  a1 := a0 ^ Random(S21);
  b1 := a1 * uinv;
  if ForAll([1..21], z -> z^b1 <> z) and b1*b1*b1 = id then
    hits := hits + 1;
    G := Group(a1,b1);
    if G = A21 then
      gen := gen + 1;
      Print("FOUND at try ", i, "\n");
      Print("a1 := ", a1, ";;\n");
      Print("b1 := ", b1, ";;\n");
      Print("check b1^-1*a1 = u ? ", b1^-1*a1 = uu,
            "  ord(a1)=", Order(a1), " ord(b1)=", Order(b1), "\n");
      found := rec(a1:=a1, b1:=b1);
      break;
    else
      Print("  class hit ", hits, ": proper subgroup |G|=", Size(G),
            " orbits=", SortedList(List(Orbits(G,[1..21]),Length)), "\n");
    fi;
  fi;
od;
Print("class hits=", hits, "  generating A21: ", gen, "\n");

if found <> fail then
  S3 := SymmetricGroup(3);;
  D := DirectProduct(A21, S3);;
  e1 := Embedding(D,1);; e2 := Embedding(D,2);;
  a := Image(e1,found.a1)*Image(e2,(1,3));;
  b := Image(e1,found.b1)*Image(e2,(1,3,2));;
  s1 := b^-1*a;; s2 := a^-1*b^2;;
  P := Group(s1^2, s2^2);;
  x1 := PreImagesRepresentative(e1, s1^2);;
  y1 := PreImagesRepresentative(e1, s2^2);;
  cy := Centralizer(A21, y1);; sx := Centralizer(S21, x1);;
  Print("\n[W-D-A21-13t8] braid=", s1*s2*s1 = s2*s1*s2,
        "  c=(s1s2)^3=1: ", (s1*s2)^3 = One(D),
        "  <s1,s2>=E: ", Group(s1,s2)=D, "\n");
  Print("  [B3:N]=", Size(D), "  |P|=", Size(P),
        "  P=ker: ", P = Kernel(Projection(D,2)), "\n");
  Print("  ord(s1)=", Order(s1), " N_ord=", Order(s1^2),
        " c_m=", Phi(2*Order(s1^2)), "\n");
  Print("  C_P(ybar)=", Size(cy), " solv=", IsSolvableGroup(cy),
        "  Syl2 dl=", DerivedLength(SylowSubgroup(cy,2)), "\n");
  Print("  Stab=", Size(sx), " solv=", IsSolvableGroup(sx),
        "  Syl2 dl=", DerivedLength(SylowSubgroup(sx,2)),
        "  |Syl2|=", Size(SylowSubgroup(sx,2)), "\n");
  Print("  Xi budget=", Phi(2*Order(s1^2))*Size(cy)*Size(sx), "\n");
  Print("  JUDGE_S1_IMG := ", s1, ";;\n  JUDGE_S2_IMG := ", s2, ";;\n");
  Print("  degree(E)=", LargestMovedPoint(D), "\n");
fi;
Print("TAIL8_HUNT_DONE\n");
QUIT;
