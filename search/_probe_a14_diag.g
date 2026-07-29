## Diagnostic: sample many (a1,b1) pairs of the target classes and tabulate
## the cycle type distribution of u=b1^-1*a1, to sanity-check the class-
## multiplication-coefficient estimate (~1/40 probability) against the
## observed 7M-trial zero-hit random search.
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

tally := rec();;
N := 20000;;
hitCount := 0;;
for trial in [1..N] do
  a1 := RandomInvolution(n, 6);;
  b1 := RandomOrder3(n, 4);;
  u := b1^-1*a1;;
  ct := SortedList(CycleLengths(u,[1..n]));;
  key := String(ct);;
  if IsBound(tally.(key)) then
    tally.(key) := tally.(key) + 1;
  else
    tally.(key) := 1;
  fi;
  if ct = [1,2,2,9] then
    hitCount := hitCount + 1;
  fi;
od;
Print("N=", N, " hitCount(type=[1,2,2,9])=", hitCount, "\n");
Print("full tally:\n");
for key in RecNames(tally) do
  Print("  ", key, " : ", tally.(key), "\n");
od;
Print("DONE_DIAG\n");
