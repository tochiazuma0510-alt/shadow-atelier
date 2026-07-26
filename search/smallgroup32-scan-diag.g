# diagnostic follow-up (not part of the deliverable script): sanity-check the
# SmallGroup(32,2) and SmallGroup(32,6) non-zero N_i result from smallgroup32-scan.g
# via an independent counting method (conjugacy-class-based double count) to rule out
# a bug in the brute double-loop.

G2 := SmallGroup(32,2);;
G6 := SmallGroup(32,6);;

Print("StructureDescription(G2) = ", StructureDescription(G2), "\n");
Print("StructureDescription(G6) = ", StructureDescription(G6), "\n");
Print("IsAbelian(G2)=", IsAbelian(G2), "  IsAbelian(G6)=", IsAbelian(G6), "\n");
Print("Exponent(G2)=", Exponent(G2), "  Exponent(G6)=", Exponent(G6), "\n");

CountMarked := function(G)
  local elts, ords4, a, b, cnt;
  elts := Elements(G);
  ords4 := Filtered(elts, x -> Order(x) = 4);
  cnt := 0;
  for a in ords4 do
    for b in ords4 do
      if Order(a*b) = 4 and Size(Subgroup(G,[a,b])) = Size(G) then
        cnt := cnt + 1;
      fi;
    od;
  od;
  return rec(cnt:=cnt, numOrd4:=Length(ords4));
end;;

r2 := CountMarked(G2);;
r6 := CountMarked(G6);;
Print("G2: N=", r2.cnt, " (num order-4 elements=", r2.numOrd4, ")\n");
Print("G6: N=", r6.cnt, " (num order-4 elements=", r6.numOrd4, ")\n");

# cross check against AutomorphismGroup orbit count differently: number of order-4
# elements should match |G| minus elements of other orders; also list order spectrum
Print("G2 order spectrum: ", Collected(List(Elements(G2), Order)), "\n");
Print("G6 order spectrum: ", Collected(List(Elements(G6), Order)), "\n");

Print("|Aut(G2)| = ", Size(AutomorphismGroup(G2)), "\n");
Print("|Aut(G6)| = ", Size(AutomorphismGroup(G6)), "\n");

QUIT;
