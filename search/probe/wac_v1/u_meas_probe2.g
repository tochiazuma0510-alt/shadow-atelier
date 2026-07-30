# u_meas_probe2.g -- Nielsen class count for the M1 passport (field-of-moduli input)
#
# Window A : passport ((9,1),(9,1),(9,1)), degree 10, monodromy A10
# Window B : passport ((9),(9),(9)),       degree  9, monodromy PSL(2,8)
#
# Counts triples (X,Y,Z), XYZ=1, all of the prescribed type, up to simultaneous
# conjugacy, with the third entry pinned; orbits under C(Z).
# Raw measurements only.

Print("=== u_meas_probe2 : Nielsen classes of the passport ===\n");

MakeCycle := function(lst, n)
  local img, i, m;
  m := Length(lst);
  img := [1..n];
  for i in [1..m] do img[lst[i]] := lst[(i mod m)+1]; od;
  return PermList(img);
end;

############################################################
Print("\n---------- Window A : deg 10, type (9,1) x3 ----------\n");

nA := 10;;
cA := MakeCycle([1,2,3,4,5,6,7,8,9], 10);;   # this is X*Y = Z^-1
Print("A  c = ", cA, "  ord=", Order(cA), "\n");
A10 := AlternatingGroup(10);;
S10 := SymmetricGroup(10);;
Print("A  |C_S10(c)| = ", Size(Centralizer(S10,cA)),
      "   |C_A10(c)| = ", Size(Centralizer(A10,cA)), "\n");

solsA := [];;
for p in [1..10] do
  rest := Difference([1..10],[p]);;
  tailset := rest{[2..9]};;
  for qq in PermutationsList(tailset) do
    XX := MakeCycle(Concatenation([rest[1]], qq), 10);
    YY := XX^-1*cA;
    if Order(YY) = 9 and NrMovedPoints(YY) = 9 then
      Add(solsA, [XX,YY]);
    fi;
  od;
od;
Print("A  #solutions (X,Y) with XY=c, both 9-cycles = ", Length(solsA), "\n");

# monodromy group sizes
grpsizesA := [];;
genA := [];;
for pr in solsA do
  s := Size(Group(pr[1],pr[2]));
  Add(grpsizesA, s);
  if s = Size(A10) then Add(genA, pr); fi;
od;
Print("A  distinct |<X,Y>| = ", Set(grpsizesA), "\n");
Print("A  multiplicities   = ", List(Set(grpsizesA), s -> [s, Number(grpsizesA, x->x=s)]), "\n");
Print("A  #with <X,Y> = A10 : ", Length(genA), "\n");

# orbits under C_{S10}(c) = <c> (simultaneous conjugation)
CS := Centralizer(S10, cA);;
orbA := [];;
seen := [];;
for pr in genA do
  if not pr in seen then
    o := [];
    for gg in Elements(CS) do
      Add(o, [pr[1]^gg, pr[2]^gg]);
    od;
    o := Set(o);
    Append(seen, o);
    Add(orbA, o);
  fi;
od;
Print("A  #<c>-orbits on generating solutions = ", Length(orbA),
      "   orbit sizes = ", List(orbA, Length), "\n");
Print("A  => #S10-classes of dessins in this passport with monodromy A10 = ", Length(orbA), "\n");

# where does our window's own triple sit?
a1 := (1,2)(3,5)(4,10)(6,9);; b1 := (2,9,5)(3,4,10)(6,8,7);;
Xw := (b1^-1*a1)^2;; Yw := (a1*b1^-1)^2;; Zw := (Xw*Yw)^-1;;
Print("A  window triple: X*Y = ", Xw*Yw, "  (ord ", Order(Xw*Yw), ")\n");
hit := First([1..Length(orbA)], i -> ForAny(orbA[i], pr -> RepresentativeAction(S10,[pr[1],pr[2]],[Xw,Yw],OnTuples) <> fail));
Print("A  window triple lies in S10-class #", hit, " of ", Length(orbA), "\n");

############################################################
Print("\n---------- Window B : deg 9, type (9) x3 ----------\n");

q := 8;; zz := Z(q);;
enc := function(k)
  local e,i;
  e := Zero(GF(8));
  for i in [0..2] do
    if (QuoInt(k,2^i) mod 2) = 1 then e := e + zz^i; fi;
  od;
  return e;
end;;
SM := [[enc(1),enc(0)],[enc(1),enc(1)]];;
TM := [[enc(4),enc(3)],[enc(1),enc(5)]];;
P1 := NormedRowVectors(GF(8)^2);;
actB := ActionHomomorphism(SL(2,8), P1, OnLines);;
sB := Image(actB,SM);; tB := Image(actB,TM);;
PB := Group(sB,tB);;
S9 := SymmetricGroup(9);;

ord9 := Filtered(Elements(PB), g -> Order(g) = 9);;
Print("B  #elements of order 9 in P = ", Length(ord9), "\n");
cB := (tB^-1*sB)^2;;                       # a 9-cycle: use X itself as pinned c
cB := ((tB^-1*sB)^2 * (sB*tB^-1)^2)^1;;    # c := X*Y = Z^-1
Print("B  c = X*Y, ord = ", Order(cB), " movedpts = ", NrMovedPoints(cB), "\n");
Print("B  |C_P(c)| = ", Size(Centralizer(PB,cB)),
      "   |C_S9(c)| = ", Size(Centralizer(S9,cB)), "\n");

solsB := [];;
for XX in ord9 do
  YY := XX^-1*cB;
  if Order(YY) = 9 and NrMovedPoints(YY) = 9 then Add(solsB,[XX,YY]); fi;
od;
Print("B  #solutions (X,Y) in P with XY=c, both order 9 = ", Length(solsB), "\n");
genB := Filtered(solsB, pr -> Size(Group(pr[1],pr[2])) = 504);;
Print("B  #with <X,Y> = P = ", Length(genB), "\n");

# but the honest count is over all of S9, not just inside P:
solsB9 := [];;
ord9S9 := Filtered(Elements(S9), g -> Order(g) = 9 and NrMovedPoints(g) = 9);;
Print("B  #9-cycles in S9 = ", Length(ord9S9), "\n");
for XX in ord9S9 do
  YY := XX^-1*cB;
  if Order(YY) = 9 and NrMovedPoints(YY) = 9 then Add(solsB9,[XX,YY]); fi;
od;
Print("B  #solutions over S9 = ", Length(solsB9), "\n");
gsz := List(solsB9, pr -> Size(Group(pr[1],pr[2])));;
Print("B  distinct |<X,Y>| = ", Set(gsz), "\n");
Print("B  multiplicities   = ", List(Set(gsz), s -> [s, Number(gsz,x->x=s)]), "\n");
genB9 := Filtered(solsB9, pr -> Size(Group(pr[1],pr[2])) = 504);;
CSB := Centralizer(S9,cB);;
Print("B  |C_S9(c)| = ", Size(CSB), "\n");
orbB := [];; seenB := [];;
for pr in genB9 do
  if not pr in seenB then
    o := Set(List(Elements(CSB), gg -> [pr[1]^gg, pr[2]^gg]));
    Append(seenB, o);
    Add(orbB, o);
  fi;
od;
Print("B  #<c>-orbits on order-504 solutions = ", Length(orbB),
      "  sizes = ", List(orbB,Length), "\n");
Print("B  => #S9-classes of dessins in passport (9,9,9) with monodromy PSL(2,8) = ", Length(orbB), "\n");

Print("\n=== done ===\n");
QUIT;
