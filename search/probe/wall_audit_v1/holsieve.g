# (1) numeric verification of the "Hol sieve": F_0 -> Aut(P_N), [0,f] |-> E_{0,f}
#     is an injective-on-V homomorphism with image in U = Stab_Aut(P)(x) & y-class.
# (2) feasibility scan for the design criterion  C_P(ybar) nonsolvable.

p := 5;;
R := ZmodnZ(2*p);;  o := One(R);;
Em := Group([[1,1],[0,1]]*o, [[1,0],[-1,1]]*o);;
iso := IsomorphismPermGroup(Em);;
G := Image(iso);;
S1 := Image(iso,[[1,1],[0,1]]*o);;  S2 := Image(iso,[[1,0],[-1,1]]*o);;
Xg := S1^2;; Yg := S2^2;; Cc := (S1*S2*S1)^2;;
P := Subgroup(G,[Xg,Yg]);;
Nord := Lcm(Order(Xg),Order(Yg),Order(Cc));;
Pc := DerivedSubgroup(P);;
# m = 0 layer
F0 := [];;
for f in AsList(Pc) do
  if S1 * f^-1 * S2 * f = f^-1 * S1 * S2 and
     f^-1 * S2 * f * S1 = S2 * S1 * f and
     Size(Subgroup(G,[Xg, f^-1*Yg*f])) = Size(P) then Add(F0,f); fi;
od;
Print("|F_0| = ", Length(F0), "\n");
# E_{0,f} on P : x -> x, y -> f^-1 y f
Es := List(F0, f -> GroupHomomorphismByImages(P,P,[Xg,Yg],[Xg, f^-1*Yg*f]));;
Print("all E_{0,f} are automorphisms of P_N: ",
      ForAll(Es, e -> e <> fail and IsBijective(e)), "\n");
# check the composition law  [0,f1].[0,f2] = [0, f1*E1(f2)]  closes and E is a hom
homok := true;;
for i in [1..Length(F0)] do
  for j in [1..Length(F0)] do
    ff := F0[i] * Image(Es[i], F0[j]);
    k := Position(F0, ff);
    if k = fail then homok := false;
    elif Es[k] <> CompositionMapping(Es[i], Es[j]) then homok := false; fi;
  od;
od;
Print("F_0 closed AND f |-> E_{0,f} is a homomorphism into Aut(P_N): ", homok, "\n");
V := Centralizer(P, Yg);;
Print("V = C_{P_N}(y) : order ", Size(V), "  solvable ", IsSolvableGroup(V), "\n");
AutP := AutomorphismGroup(P);;
StabX := Stabilizer(AutP, Xg, function(g,a) return Image(a,g); end);;
Print("Stab_{Aut(P_N)}(x) : order ", Size(StabX), "  solvable ", IsSolvableGroup(StabX), "\n");
Print("image of F_0 in Aut(P_N) has order ", Size(Group(Es)),
      "; kernel of F_0 -> Aut(P) has order ",
      Length(Filtered([1..Length(F0)], i -> Es[i] = IdentityMapping(P))), "\n");
Print("dl bound 1+dl(V)+dl(StabX) = ",
      1 + Length(DerivedSeriesOfGroup(V)) - 1 + Length(DerivedSeriesOfGroup(StabX)) - 1, "\n");

Print("\n=== (2) design criterion feasibility: P = <x,y>, x~y, C_P(y) nonsolvable ===\n");
for nn in [9,10,11,12] do
  An := AlternatingGroup(nn);
  # y of order 3 : product of k disjoint 3-cycles, k = 2
  y := (1,2,3)(4,5,6);
  Cy := Centralizer(An, y);
  Print("n = ", nn, "  |C_{A_n}(y)| = ", Size(Cy), "  solvable = ", IsSolvableGroup(Cy));
  hit := 0;
  for t in [1..400] do
    g := Random(An);
    x := y^g;
    if Subgroup(An,[x,y]) = An then hit := hit + 1; fi;
  od;
  Print("   <y^g,y> = A_n in ", hit, "/400 random tries\n");
od;
QUIT;
