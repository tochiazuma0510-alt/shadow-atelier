## Diagnostic 3: for ct-hit cases (u-type = [1,2,2,9]), report the actual
## size/structure of <a1,b1> to see why it's never = A14.
n := 14;;
A14 := AlternatingGroup(n);;

RandomInvolution := function(n, k)
  local pts, i, p1, p2, gens;
  pts := Permuted([1..n], Random(SymmetricGroup(n)));
  gens := [];
  for i in [1..k] do
    p1 := pts[2*i-1];  p2 := pts[2*i];
    Add(gens, (p1,p2));
  od;
  return Product(gens);
end;;

RandomOrder3 := function(n, k)
  local pts, gens, i, a, b, c;
  pts := Permuted([1..n], Random(SymmetricGroup(n)));
  gens := [];
  for i in [1..k] do
    a := pts[3*i-2];  b := pts[3*i-1];  c := pts[3*i];
    Add(gens, (a,b,c));
  od;
  return Product(gens);
end;;

N := 500;;
reported := 0;;
for trial in [1..N] do
  a1 := RandomInvolution(n, 6);;
  b1 := RandomOrder3(n, 4);;
  u := b1^-1*a1;;
  ct := SortedList(CycleLengths(u,[1..n]));;
  if ct = [1,2,2,9] then
    grp := Group(a1,b1);;
    Print("trial=",trial, " |<a1,b1>|=", Size(grp),
          " transitive=", IsTransitive(grp,[1..n]),
          " primitive=", (IsTransitive(grp,[1..n]) and IsPrimitive(grp,[1..n])), "\n");
    reported := reported + 1;
    if reported >= 15 then break; fi;
  fi;
od;
Print("DONE_DIAG3\n");
