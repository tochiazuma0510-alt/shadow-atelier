#############################################################################
## scratchpad/extract_witness_n21.g -- bounded random search for ONE
## explicit (a,b) pair satisfying the class-only constraints of the n=21
## tail-8 SAT target (W-D-A21-13t8), for SAT-checker self-test calibration
## ONLY. This is NOT a re-derivation of the 4160-solution census (that is
## tail8_exact.g's job, already done and reported in wac_tail8_v1.md).
## Fixed u = (1..13)(14 15)(16 17)(18 19)(20 21) (sealed symbol, same as
## tail8_exact.g). Stops at the first hit within a bounded try budget and
## prints the explicit permutation images machine-readably (JSON-ish line)
## so no value here is hand-copied.
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
S21 := SymmetricGroup(21);;
uu := (1,2,3,4,5,6,7,8,9,10,11,12,13)*(14,15)*(16,17)*(18,19)*(20,21);;
uinv := uu^-1;;
a0 := WacBlock(10,2);;
id := ();;
BUDGET := 5000000;;

found := false;; i := 0;;
while (not found) and i < BUDGET do
  i := i + 1;
  a1 := a0 ^ Random(S21);
  b1 := a1 * uinv;
  if ForAll([1..21], z -> z^b1 <> z) and b1*b1*b1 = id then
    found := true;
  fi;
od;

if found then
  Print("FOUND try=", i, "\n");
  Print("a_images=", List([1..21], k -> k^a1), "\n");
  Print("b_images=", List([1..21], k -> k^b1), "\n");
  Print("u_images=", List([1..21], k -> k^uu), "\n");
  Print("uinv_images=", List([1..21], k -> k^uinv), "\n");
  G := Group(a1,b1);;
  Print("orbits=", SortedList(List(Orbits(G,[1..21]),Length)), "\n");
  Print("transitive=", IsTransitive(G,[1..21]), "\n");
else
  Print("NOT_FOUND within budget ", BUDGET, "\n");
fi;
Print("WITNESS_EXTRACT_DONE\n");
QUIT;
