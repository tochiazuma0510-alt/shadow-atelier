## tail-6 control window: n=19, ell=13, u=(13,2,2,2), a'=2^9 1, b'=3^6 1
## structconst = 1664 (ss_alt.g).  Same ell=13 as W-D-A18-13a (tail 5)
## => controlled tail 5 -> 6 comparison.
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
S19 := SymmetricGroup(19);; A19 := AlternatingGroup(19);;
uu := (1,2,3,4,5,6,7,8,9,10,11,12,13)*(14,15)*(16,17)*(18,19);;
uinv := uu^-1;;
a0 := WacBlock(9,2);;   # 2^9 1
id := ();;
Print("u type ord=", Order(uu), "  xbar ord=", Order(uu^2), "\n");
hits := 0;; found := fail;;
for i in [1..1500000] do
  a1 := a0 ^ Random(S19);
  b1 := a1 * uinv;
  if b1*b1*b1 = id and Number([1..19], z -> z^b1 = z) = 1 then
    hits := hits + 1;
    G := Group(a1,b1);
    if G = A19 or G = S19 then
      Print("FOUND at try ", i, "  image=S19? ", G = S19, "\n  a1 := ", a1, ";;\n  b1 := ", b1, ";;\n");
      found := rec(a1:=a1, b1:=b1); break;
    else
      Print("  hit ", hits, ": proper |G|=", Size(G), " orbits=",
            SortedList(List(Orbits(G,[1..19]),Length)), "\n");
    fi;
  fi;
od;
Print("class hits=", hits, "\n");
if found <> fail then
  S3 := SymmetricGroup(3);; D := DirectProduct(S19, S3);;   # k odd => image is S19; E = fibre product
  e1 := Embedding(D,1);; e2 := Embedding(D,2);;
  a := Image(e1,found.a1)*Image(e2,(1,3));;
  b := Image(e1,found.b1)*Image(e2,(1,3,2));;
  s1 := b^-1*a;; s2 := a^-1*b^2;;
  P := Group(s1^2,s2^2);;
  x1 := PreImagesRepresentative(e1, s1^2);;
  y1 := PreImagesRepresentative(e1, s2^2);;
  cy := Centralizer(A19,y1);; sx := Centralizer(S19,x1);;
  Print("\n[W-D-A19-13t6] braid=", s1*s2*s1=s2*s1*s2, " c=1:", (s1*s2)^3=One(D),
        " <s1,s2>=E:", Group(s1,s2)=D, "\n");
  Print("  [B3:N]=", Size(D), " |P|=", Size(P), " P=ker:",
        P=Kernel(Projection(D,2)), "\n");
  Print("  N_ord=", Order(s1^2), " c_m=", Phi(2*Order(s1^2)), "\n");
  Print("  C_P(ybar)=", Size(cy), " (", StructureDescription(cy),
        ") Syl2 dl=", DerivedLength(SylowSubgroup(cy,2)), "\n");
  Print("  Stab=", Size(sx), " (", StructureDescription(sx),
        ") |Syl2|=", Size(SylowSubgroup(sx,2)),
        " dl=", DerivedLength(SylowSubgroup(sx,2)), "\n");
  Print("  Xi budget=", Phi(2*Order(s1^2))*Size(cy)*Size(sx), "\n");
  Print("  JUDGE_S1_IMG := ", s1, ";;\n  JUDGE_S2_IMG := ", s2, ";;\n");
  Print("  degree(E)=", LargestMovedPoint(D), "\n");
fi;
Print("TAIL6_HUNT_DONE\n");
QUIT;
