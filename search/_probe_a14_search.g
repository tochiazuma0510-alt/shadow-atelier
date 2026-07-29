n := 14;;
A14 := AlternatingGroup(n);;

# random even involution: k disjoint transpositions on a random subset of n points
RandomInvolution := function(n, k)
  local pts, pairs, i, p1, p2, gens;
  pts := Permuted([1..n], Random(SymmetricGroup(n)));
  gens := [];
  for i in [1..k] do
    p1 := pts[2*i-1];  p2 := pts[2*i];
    Add(gens, (p1,p2));
  od;
  return Product(gens);
end;;

# random order-3 element: k disjoint 3-cycles on a random subset of n points
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
  a1 := RandomInvolution(n, 6);;    # 6 transpositions (12 pts), 2 fixed
  b1 := RandomOrder3(n, 4);;        # 4 threecycles (12 pts), 2 fixed
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
    Print("progress trial=", trial, " elapsed_ms=", Runtime()-t0, "\n");
  fi;
od;
Print("trials=", trials, " time=", Runtime()-t0, " found=", found<>fail, "\n");
if found <> fail then
  Print("a1 := ", found.a1, ";;\n");
  Print("b1 := ", found.b1, ";;\n");
  Print("u type check: ", SortedList(CycleLengths(found.u,[1..n])), "\n");
fi;
Print("DONE\n");
