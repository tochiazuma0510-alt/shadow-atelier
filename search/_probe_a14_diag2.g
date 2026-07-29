## Diagnostic 2: same as diag but ALSO check Group(a1,b1)=A14, to see if the
## generation condition is the (unexpected) bottleneck.
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

N := 3000;;
ctHit := 0;;
genHit := 0;;
bothHit := 0;;
found := fail;;
t0 := Runtime();;
for trial in [1..N] do
  a1 := RandomInvolution(n, 6);;
  b1 := RandomOrder3(n, 4);;
  u := b1^-1*a1;;
  ct := SortedList(CycleLengths(u,[1..n]));;
  isCtHit := (ct = [1,2,2,9]);;
  if isCtHit then ctHit := ctHit + 1; fi;
  if isCtHit then
    isGen := (Group(a1,b1) = A14);;
    if isGen then
      genHit := genHit + 1;
      bothHit := bothHit + 1;
      if found = fail then
        found := rec(a1:=a1, b1:=b1);;
      fi;
    fi;
  fi;
od;
Print("N=", N, " ctHit=", ctHit, " (ct-and-gen)bothHit=", bothHit, " time_ms=", Runtime()-t0, "\n");
if found <> fail then
  Print("FOUND EXAMPLE:\n");
  Print("a1 := ", found.a1, ";;\n");
  Print("b1 := ", found.b1, ";;\n");
fi;
Print("DONE_DIAG2\n");
