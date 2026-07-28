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
tally := NewDictionary([1], true);;
types := [];;
cnt := 0;; gencnt := 0;;
for i in [1..5000] do
  a1 := WacBlock(Random([2,4,6]), 2) ^ Random(Sn);
  b1 := WacBlock(Random([1,2,3,4]), 3) ^ Random(Sn);
  u := b1^-1 * a1;
  ty := WacCT(u, n);
  Add(types, ty);
  if ty = [1,1,2,2,7] then
    cnt := cnt + 1;
    if Group(a1,b1) = An then gencnt := gencnt + 1; fi;
  fi;
od;
Print("type [1,1,2,2,7] hits: ", cnt, "  of which generate A13: ", gencnt, "\n");
Print("distinct types seen: ", Length(Set(types)), "\n");
srt := Collected(types);;
SortBy(srt, r -> -r[2]);
Print("top 12 types:\n");
for r in srt{[1..Minimum(12,Length(srt))]} do Print("  ", r[1], " -> ", r[2], "\n"); od;
Print("ord(u)=14 count: ", Number(types, t -> Lcm(t) = 14), "\n");
Print("DIAG_DONE\n");
QUIT;
