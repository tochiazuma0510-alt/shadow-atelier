## Diagnostic 4: try forcing a1's 2 fixed points and b1's 2 fixed points to
## be DISJOINT (a natural alternative split), to see if that avoids the
## intransitivity found in diag3.
n := 14;;
A14 := AlternatingGroup(n);;

# a1: 6 transpositions on a random 12-subset, 2 fixed; b1: 4 threecycles on
# a DIFFERENT random 12-subset chosen so that its 2 fixed points are exactly
# a1's moved points overlap structure varies -- here we just force disjoint
# fixed-point sets by construction: pick a1's fixed pair F_a (2 pts), then
# choose b1's fixed pair F_b from the OTHER 12 points (disjoint from F_a).
RandomOrder3General := function(n, k)
  local pts, gens, i, a, b, c;
  pts := Permuted([1..n], Random(SymmetricGroup(n)));
  gens := [];
  for i in [1..k] do
    a := pts[3*i-2];  b := pts[3*i-1];  c := pts[3*i];
    Add(gens, (a,b,c));
  od;
  return Product(gens);
end;;

RandomInvolutionGeneral := function(n, k)
  local pts, i, p1, p2, gens;
  pts := Permuted([1..n], Random(SymmetricGroup(n)));
  gens := [];
  for i in [1..k] do
    p1 := pts[2*i-1];  p2 := pts[2*i];
    Add(gens, (p1,p2));
  od;
  return Product(gens);
end;;

N := 3000;;
ctHit := 0;;
genHit := 0;;
found := fail;;
for trial in [1..N] do
  a1 := RandomInvolutionGeneral(n, 6);;
  fixedA := Difference([1..n], MovedPoints(a1));;
  b1 := RandomOrder3General(n, 4);;
  fixedB := Difference([1..n], MovedPoints(b1));;
  u := b1^-1*a1;;
  ct := SortedList(CycleLengths(u,[1..n]));;
  if ct = [1,2,2,9] then
    ctHit := ctHit + 1;
    isGen := (Group(a1,b1) = A14);;
    Print("trial=",trial," fixedA=",fixedA," fixedB=",fixedB,
          " overlap=", Length(Intersection(fixedA,fixedB)),
          " isGen=", isGen, "\n");
    if isGen then
      genHit := genHit + 1;
      if found = fail then found := rec(a1:=a1,b1:=b1); fi;
    fi;
  fi;
od;
Print("N=",N," ctHit=",ctHit," genHit=",genHit,"\n");
if found <> fail then
  Print("FOUND:\n a1 := ", found.a1, ";;\n b1 := ", found.b1, ";;\n");
fi;
Print("DONE_DIAG4\n");
