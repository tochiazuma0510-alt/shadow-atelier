## Diagnostic 5: among pairs (a1,b1) [type 2^6 1^2 / 3^4 1^2] that DO
## generate A14, does u=b1^-1*a1 EVER have type [1,2,2,9]? Tabulate the
## u-type distribution restricted to generating pairs, over a decent sample.
n := 14;;
A14 := AlternatingGroup(n);;

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

N := 8000;;
genCount := 0;;
tally := rec();;
hit19 := 0;;
t0 := Runtime();;
for trial in [1..N] do
  a1 := RandomInvolutionGeneral(n, 6);;
  b1 := RandomOrder3General(n, 4);;
  if Group(a1,b1) = A14 then
    genCount := genCount + 1;
    u := b1^-1*a1;;
    ct := SortedList(CycleLengths(u,[1..n]));;
    key := String(ct);;
    if IsBound(tally.(key)) then tally.(key):=tally.(key)+1; else tally.(key):=1; fi;
    if ct = [1,2,2,9] then hit19 := hit19+1; fi;
  fi;
od;
Print("N=",N," genCount=",genCount," time_ms=",Runtime()-t0,"\n");
Print("hit19 (type [1,2,2,9] AMONG generating pairs) = ", hit19, "\n");
Print("u-type tally among generating pairs:\n");
for key in RecNames(tally) do
  Print("  ", key, " : ", tally.(key), "\n");
od;
Print("DONE_DIAG5\n");
