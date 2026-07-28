WacCT := function(p, n)
  return SortedList(List(Orbits(Group(p), [1..n]), Length));
end;;
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
    p := p * WacCyc(List([1..len], j -> base + j)); base := base + len;
  od;
  return p;
end;;

n := 13;;
Sn := SymmetricGroup(n);; An := AlternatingGroup(n);;
Print("|A13| = ", Size(An), "\n");
seen := [];;
for i in [1..4000] do
  a1 := WacBlock(Random([2,4,6]), 2) ^ Random(Sn);
  b1 := WacBlock(Random([1,2,3,4]), 3) ^ Random(Sn);
  u := b1^-1 * a1;
  if WacCT(u, n) = [1,1,2,2,7] then
    G := Group(a1,b1);
    Add(seen, [Size(G), WacCT(a1,n), WacCT(b1,n), IsTransitive(G,[1..13])]);
  fi;
od;
Print("hits: ", Length(seen), "\n");
Print("sizes seen: ", Collected(List(seen, r->r[1])), "\n");
Print("(a1type,b1type,trans) collected:\n");
for r in Collected(List(seen, r->[r[2],r[3],r[4]])) do Print("  ",r,"\n"); od;
Print("\n--- now check whether ANY (2,3)-gen of A13 exists at all (random) ---\n");
g23 := 0;; orders := [];;
for i in [1..3000] do
  a1 := WacBlock(Random([2,4,6]), 2) ^ Random(Sn);
  b1 := WacBlock(Random([1,2,3,4]), 3) ^ Random(Sn);
  if Group(a1,b1) = An then
    g23 := g23 + 1;
    Add(orders, Order(b1^-1*a1));
  fi;
od;
Print("(2,3)-generating pairs of A13 found: ", g23, " / 3000\n");
Print("ord(u) distribution among them: ", Collected(orders), "\n");
Print("DIAG2_DONE\n");
QUIT;
