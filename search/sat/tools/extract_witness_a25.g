#############################################################################
## search/sat/tools/extract_witness_a25.g -- bounded random search for ONE
## explicit (a,b) pair satisfying the class-only constraints of the n=25
## second SAT target (ell=17, n=25, Sol reply 84 sec 6.3), for SAT-checker
## self-test calibration ONLY -- NOT a census, NOT a 2-transitivity search.
## Fixed u = (1..17)(18,19)(20,21)(22,23)(24,25) (sealed symbol, per the
## commander's task spec / sol/sol_reply_84_math11.md sec 6.3).
## a: type 2^12 1 (12 transpositions, 1 fixed point).
## b := a*u^-1 required: type 3^8 1 (b^3=1, EXACTLY ONE fixed point --
## note this differs from the n=21 target, where b was fixed-point-free).
## Prints explicit permutation images machine-readably (no value here is
## hand-copied) plus the orbit partition under <a,b> (for interpretive
## context only -- transitivity/2-transitivity is NOT the goal of this
## bounded random search and a "false" here is expected and uninformative).
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
N := 25;;
S25 := SymmetricGroup(N);;
uu := (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17)*(18,19)*(20,21)*(22,23)*(24,25);;
uinv := uu^-1;;
a0 := WacBlock(12,2);;
id := ();;
BUDGET := 5000000;;

found := false;; i := 0;;
while (not found) and i < BUDGET do
  i := i + 1;
  a1 := a0 ^ Random(S25);
  b1 := a1 * uinv;
  if Length(Filtered([1..N], z -> z^b1 = z)) = 1 and b1*b1*b1 = id then
    found := true;
  fi;
od;

if found then
  Print("FOUND try=", i, "\n");
  Print("a_images=", List([1..N], k -> k^a1), "\n");
  Print("b_images=", List([1..N], k -> k^b1), "\n");
  Print("u_images=", List([1..N], k -> k^uu), "\n");
  Print("uinv_images=", List([1..N], k -> k^uinv), "\n");
  G := Group(a1,b1);;
  Print("orbits=", SortedList(List(Orbits(G,[1..N]),Length)), "\n");
  Print("transitive=", IsTransitive(G,[1..N]), "\n");
else
  Print("NOT_FOUND within budget ", BUDGET, "\n");
fi;
Print("WITNESS_EXTRACT_DONE\n");
QUIT;
