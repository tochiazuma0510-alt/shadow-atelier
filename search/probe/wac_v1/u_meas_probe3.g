# u_meas_probe3.g -- fingerprinting the 6 dessins in the S4 passport (9,9,9)
# and locating the window's own triple. Input for the C1' certificate schema.
# Raw measurements only.

Print("=== u_meas_probe3 : the 6 dessins of passport (9,9,9) / PSL(2,8) ===\n");

CT := function(p) local l; l := List(Orbits(Group(p),[1..9]),Length); Sort(l); return Reversed(l); end;

zz := Z(8);;
enc := function(k) local e,i; e := Zero(GF(8));
  for i in [0..2] do if (QuoInt(k,2^i) mod 2)=1 then e := e+zz^i; fi; od; return e; end;;
SM := [[enc(1),enc(0)],[enc(1),enc(1)]];;
TM := [[enc(4),enc(3)],[enc(1),enc(5)]];;
P1 := NormedRowVectors(GF(8)^2);;
act := ActionHomomorphism(SL(2,8), P1, OnLines);;
sB := Image(act,SM);; tB := Image(act,TM);;
PB := Group(sB,tB);;
S9 := SymmetricGroup(9);;
X0 := (tB^-1*sB)^2;;  Y0 := (sB*tB^-1)^2;;  c := X0*Y0;;
Print("window triple: ord(X,Y,Z) = ", [Order(X0),Order(Y0),Order((X0*Y0)^-1)], "\n");

ord9 := Filtered(Elements(S9), g -> Order(g)=9 and NrMovedPoints(g)=9);;
sols := [];;
for XX in ord9 do
  YY := XX^-1*c;
  if Order(YY)=9 and NrMovedPoints(YY)=9 and Size(Group(XX,YY))=504 then Add(sols,[XX,YY]); fi;
od;
Print("#solutions with monodromy 504 = ", Length(sols), "\n");

CS := Centralizer(S9,c);;
classes := [];;  seen := [];;
for pr in sols do
  if not pr in seen then
    o := Set(List(Elements(CS), g -> [pr[1]^g, pr[2]^g]));
    Append(seen,o); Add(classes,o);
  fi;
od;
Print("#S9-classes = ", Length(classes), "\n");

# fingerprint: cycle types of a fixed short word list, taken on a representative
words := function(pr) local X,Y;
  X := pr[1]; Y := pr[2];
  return [CT(X*Y), CT(X*Y^-1), CT(X^2*Y), CT(X*Y^2), CT(X^2*Y^2), CT(X^-1*Y), CT(X^3*Y)];
end;;
for i in [1..Length(classes)] do
  Print("class ", i, "  fingerprint = ", words(classes[i][1]), "\n");
od;

# where is the window's own triple?
here := First([1..Length(classes)], i -> [X0,Y0] in classes[i]);
Print("window triple is in class ", here, "\n");

# mirror involution (X,Y) -> (Y^-1, X^-1) : same product c^-1 conj; test as a map on classes
Print("\n-- action of (X,Y) -> (X^-1,Y^-1)^{conj to keep XY=c} : skipped (changes c)\n");

# Out(PSL(2,8)) = C3 : the field Frobenius on GF(8). It normalises P in Sym(9).
NP := Normalizer(S9, PB);;
Print("|N_{S9}(P)| = ", Size(NP), "  (= |PGammaL(2,8)| = 1512 ?) ", Size(NP)=1512, "\n");
# elements of N normalising <c> act on the class set
NC := Intersection(NP, Normalizer(S9, Group(c)));;
Print("|N_{S9}(P) cap N_{S9}(<c>)| = ", Size(NC), "\n");
perm := [];;
for g in Elements(NC) do
  # (X,Y)^g has product c^g = c^k ; only keep those with c^g = c
  if c^g = c then
    Add(perm, List([1..Length(classes)], i ->
      First([1..Length(classes)], j -> [classes[i][1][1]^g, classes[i][1][2]^g] in classes[j])));
  fi;
od;
Print("permutations of the 6 classes induced by centralising elements of N_{S9}(P): ", Set(perm), "\n");

# Frobenius: does it move the class?  take g in NP with c^g = c^2 (say) -- record orbit of classes
# under the full N_{S9}(P) acting on unordered dessin data:
allpairs := [];;
for i in [1..Length(classes)] do Add(allpairs, classes[i][1]); od;
orbrep := [];;
for i in [1..Length(classes)] do
  Add(orbrep, Set(List(Elements(NP), g -> First([1..Length(classes)], j ->
      RepresentativeAction(S9, [classes[i][1][1],classes[i][1][2]],
                               [classes[j][1][1],classes[j][1][2]], OnTuples) <> fail))));
od;
Print("N_{S9}(P)-orbits on the 6 classes (as index sets): ", Set(orbrep), "\n");

Print("=== done ===\n");
QUIT;
