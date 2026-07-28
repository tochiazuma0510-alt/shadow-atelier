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
S15 := SymmetricGroup(15);;
inv := WacBlock(7,2);;
Scan := function(uu, label, tries)
  local i, a1, b1, G, dat;
  dat := [];
  for i in [1..tries] do
    a1 := inv ^ Random(S15);
    b1 := a1 * uu^-1;
    if WacCT(b1,15) = [3,3,3,3,3] then
      G := Group(a1,b1);
      Add(dat, [Size(G), SortedList(List(Orbits(G,[1..15]),Length)),
                IsTransitive(G,[1..15])]);
    fi;
  od;
  Print("\n", label, ": realizations sampled = ", Length(dat), "\n");
  Print("  (order, orbit shape, transitive) tally:\n");
  for r in Collected(dat) do Print("    ", r, "\n"); od;
end;;
Scan((1,2,3,4,5,6,7,8,9)*(10,11)*(12,13)*(14,15), "lam=(9,2,2,2)", 900000);
Scan((1,2,3,4,5,6,7,8,9,10)*(11,12)*(13,14), "lam=(10,2,2,1)", 900000);
Print("\nA15B_DONE\n");
QUIT;
