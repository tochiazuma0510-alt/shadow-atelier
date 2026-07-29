## shard 3 of A14 (D4, ell=9) generator search -- independent GAP process, parallel to shard 1/2
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

t0 := Runtime();;
trials := 0;;
found := fail;;
for trial in [1..3000000] do
  trials := trials + 1;
  a1 := RandomInvolution(n, 6);;
  b1 := RandomOrder3(n, 4);;
  if Group(a1,b1) = A14 then
    u := b1^-1*a1;;
    if Order(u) = 18 then
      ct := SortedList(CycleLengths(u,[1..n]));;
      if ct = [1,2,2,9] then
        found := rec(a1:=a1, b1:=b1, u:=u);;
        break;
      fi;
    fi;
  fi;
  if trial mod 50000 = 0 then
    Print("[shard3] progress trial=", trial, " elapsed_ms=", Runtime()-t0, "\n");
  fi;
od;
Print("[shard3] trials=", trials, " time=", Runtime()-t0, " found=", found<>fail, "\n");
if found <> fail then
  Print("[shard3] a1 := ", found.a1, ";;\n");
  Print("[shard3] b1 := ", found.b1, ";;\n");
  Print("[shard3] u type check: ", SortedList(CycleLengths(found.u,[1..n])), "\n");
fi;
Print("[shard3] DONE\n");
