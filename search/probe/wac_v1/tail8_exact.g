#############################################################################
## search/probe/wac_v1/tail8_exact.g -- decide W-D-A21-13t8 exactly.
## Fix u; the solution set {a' in class 2^10 1 : a'u^-1 in class 3^7} has
## size = structconst = 4160 and is stable under conjugation by C_{S21}(u).
## Enumerate it by C(u)-orbits until the count reaches 4160 => complete.
## Single lane. NOT a ledger claim. No commit. No u (sealed symbol).
#############################################################################
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
uinv := uu^-1;;
a0 := WacBlock(10,2);;
id := ();;
TARGET := 4160;;
C := Centralizer(S21, uu);;
Print("|C_S21(u)| = ", Size(C), "   target #solutions = ", TARGET, "\n");

sols := [];; reps := [];; i := 0;;
while Length(sols) < TARGET and i < 40000000 do
  i := i + 1;
  a1 := a0 ^ Random(S21);
  b1 := a1 * uinv;
  if ForAll([1..21], z -> z^b1 <> z) and b1*b1*b1 = id then
    if not a1 in sols then
      o := Orbit(C, a1, OnPoints);
      Print("  new C(u)-orbit, size ", Length(o), "  (running total ",
            Length(sols) + Length(o), " / ", TARGET, ")  [try ", i, "]\n");
      Append(sols, Filtered(o, z -> not z in sols));
      Add(reps, a1);
    fi;
  fi;
od;
Print("enumerated ", Length(sols), " / ", TARGET,
      "   COMPLETE? ", Length(sols) = TARGET, "   [tries=", i, "]\n");
Print("orbit representatives: ", Length(reps), "\n");
for a1 in reps do
  b1 := a1 * uinv;
  G := Group(a1, b1);
  Print("   |<a',b'>|=", Size(G), " orbits=",
        SortedList(List(Orbits(G,[1..21]),Length)),
        " transitive=", IsTransitive(G,[1..21]),
        " = A21 ? ", G = A21, "\n");
od;
Print("ANY generating A21 ? ", ForAny(reps, z -> Group(z, z*uinv) = A21), "\n");
Print("TAIL8_EXACT_DONE\n");
QUIT;
