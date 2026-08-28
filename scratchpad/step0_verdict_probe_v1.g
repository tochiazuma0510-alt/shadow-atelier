## STEP 0 verdict probe: genus of every order-triple, and rigidity of (9,9,9).
Read("search/drophunt_checker_producer_v2.g");;
G := Group(DCP2X4, DCP2Y4);;
CT := function(p) return SortedList(List(Orbits(Group(p),[1..9]),Length)); end;;
Print("SV_ORDER ", Size(G), "\n");
cc := ConjugacyClasses(G);;
Print("SV_CLASSES  (order, size, cycletype)\n");
for c in cc do
  Print("   ord=", Order(Representative(c)), " size=", Size(c),
        " cycletype=", CT(Representative(c)), "\n");
od;
## genus of an order-triple, using the (unique) cycle type per element order
ncyc := function(o)
  local c;
  c := First(cc, k -> Order(Representative(k)) = o);
  return Length(CT(Representative(c)));
end;;
gen := function(t)
  local s;
  s := -18 + Sum(t, o -> 9 - ncyc(o));
  return (s+2)/2;
end;;
Print("\nSV_GENUS_OF_LISTED_TRIPLES\n");
for t in [[7,2,3],[7,7,2],[7,3,3],[7,7,3],[9,2,3],[9,7,2],[9,9,9]] do
  Print("   ", t, "  -> genus ", gen(t), "\n");
od;
## rigidity: structure constants for triples of order-9 classes
nine := Filtered(cc, c -> Order(Representative(c)) = 9);;
Print("\nSV_ORDER9_CLASSES ", Length(nine), "  sizes ", List(nine,Size), "\n");
Print("SV_RIGIDITY  (C0,C1,Cinf) -> #{(a,b): a in C0, b in C1, (ab)^-1 in Cinf} / |G| , generates?\n");
for i in [1..Length(nine)] do for j in [1..Length(nine)] do for k in [1..Length(nine)] do
  n := 0;; ngen := 0;;
  for a in Elements(nine[i]) do
    for b in Elements(nine[j]) do
      if (a*b)^-1 in nine[k] then
        n := n + 1;;
        if Group(a,b) = G then ngen := ngen + 1;; fi;
      fi;
    od;
  od;
  Print("   (", i, ",", j, ",", k, ") count=", n, "  gen_count=", ngen,
        "  count/|G|=", n/Size(G), "  gen/|Inn|=", ngen/Size(G), "\n");
od; od; od;
## our own marked pair: which classes?
Print("\nSV_OUR_PAIR_CLASSES  X in class#", PositionProperty(cc, c -> DCP2X4 in c),
      "  Y in class#", PositionProperty(cc, c -> DCP2Y4 in c),
      "  (XY)^-1 in class#", PositionProperty(cc, c -> (DCP2X4*DCP2Y4)^-1 in c), "\n");
QUIT;
