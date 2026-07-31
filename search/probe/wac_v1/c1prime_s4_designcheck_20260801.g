#############################################################################
## search/probe/wac_v1/c1prime_s4_designcheck_20260801.g
##  Mathematician (Opus 5) design-stage checks for docs/notes/c1prime_s4_design_v1.md.
##  Steps 0/1/2 of that note's work plan.  NO measured u-value is touched;
##  this is pure finite group theory about degree-9 transitive groups.
##
##   step 0  : Size / StructureDescription of TransitiveGroup(9,27)
##             (resolves the 9T27 = PSL(2,8) vs PGammaL(2,8) notation clash).
##   step 2  : exhaustive over ALL transitive groups of degree 9 -- which ones
##             admit a triple (X,Y,Z) of 9-cycles with X*Y*Z = 1 generating a
##             transitive group?  (upper bound for the geometric monodromy,
##             route G1-c: replaces Frobenius sampling by an exhaustive list.)
##   step 1  : for P = PSL(2,8) in its degree-9 action: enumerate ALL such
##             triples with <X,Y> = P, cluster into dessins (orbits under
##             P-conjugacy and under N_{S9}(P)-conjugacy), record the class
##             vector of each and the Out(P)=C3 orbit structure on them.
##             -> answers design items D-a / D-b (is the diagonal dessin unique?).
##  Single GAP lane.  NOT a ledger claim.
#############################################################################

Print("== step 0: the 9T27 notation ==\n");
for k in [1..34] do
  G := TransitiveGroup(9,k);
  if Size(G) in [504,1512] then
    Print("  9T",k,"  size=",Size(G),"  struct=",StructureDescription(G),"\n");
  fi;
od;
G27 := TransitiveGroup(9,27);;
Print("  TransitiveGroup(9,27): size=",Size(G27),
      "  struct=",StructureDescription(G27),"\n");

Print("\n== step 2: which degree-9 transitive groups admit (9-cyc)^3 = 1, transitive ==\n");
adm := [];;
for k in [1..34] do
  G := TransitiveGroup(9,k);
  n9 := Filtered(Elements(G), g -> Order(g)=9);
  ok := false;
  if Length(n9) > 0 then
    for x in n9 do
      for y in n9 do
        z := (x*y)^-1;
        if Order(z)=9 and IsTransitive(Group(x,y),[1..9]) then
          ok := true; break;
        fi;
      od;
      if ok then break; fi;
    od;
  fi;
  if ok then
    Add(adm,[k,Size(G),StructureDescription(G)]);
  fi;
od;
Print("  admitting groups (T-number, order, structure):\n");
for r in adm do Print("   9T",r[1],"  ",r[2],"  ",r[3],"\n"); od;
Print("  count = ",Length(adm)," of 34\n");

Print("\n== step 1: dessins with passport ((9),(9),(9)) and monodromy PSL(2,8) ==\n");
## locate PSL(2,8) in its natural degree-9 action among the transitive groups
psl := First(List([1..34], k -> TransitiveGroup(9,k)),
             G -> Size(G)=504 and IsSimpleGroup(G));;
Print("  P found: size=",Size(psl),"  simple? ",IsSimpleGroup(psl),
      "  struct=",StructureDescription(psl),"\n");
NS := Normalizer(SymmetricGroup(9), psl);;
Print("  |N_{S9}(P)| = ",Size(NS),"  struct=",StructureDescription(NS),
      "  [N:P] = ",Size(NS)/Size(psl),"\n");

cl9 := Filtered(ConjugacyClasses(psl), c -> Order(Representative(c))=9);;
Print("  # P-classes of order-9 elements = ",Length(cl9),
      "   sizes = ",List(cl9,Size),"\n");
ClassIdx := function(g)
  return First([1..Length(cl9)], i -> g in cl9[i]);
end;;

elts9 := Filtered(Elements(psl), g -> Order(g)=9);;
Print("  # order-9 elements = ",Length(elts9),"\n");
triples := [];;
for x in elts9 do
  for y in elts9 do
    z := (x*y)^-1;
    if Order(z)=9 and Group(x,y)=psl then
      Add(triples,[x,y,z]);
    fi;
  od;
od;
Print("  # ordered triples (X,Y,Z), all order 9, XYZ=1, <X,Y>=P : ",
      Length(triples),"\n");

## cluster into dessins = orbits under conjugation
Cluster := function(grp)
  local orbs, t, found, o, g, im;
  orbs := [];
  for t in triples do
    found := false;
    for o in orbs do
      for g in Elements(grp) do
        if List(o[1], a -> a^g) = t then found := true; break; fi;
      od;
      if found then Add(o,t); break; fi;
    od;
    if not found then Add(orbs,[t]); fi;
  od;
  return orbs;
end;;
orbP  := Cluster(psl);;
Print("  # dessins up to P-conjugacy (inner)      = ",Length(orbP),
      "   orbit sizes = ",List(orbP,Length),"\n");
orbNS := Cluster(NS);;
Print("  # dessins up to N_{S9}(P)-conjugacy      = ",Length(orbNS),
      "   orbit sizes = ",List(orbNS,Length),"\n");

Print("\n  class vectors of the P-conjugacy dessins:\n");
cvs := [];;
for o in orbP do
  cv := List(o[1], ClassIdx);
  Add(cvs, cv);
  Print("   ",cv,"   diagonal? ",Length(Set(cv))=1,
        "   (orbit size ",Length(o),")\n");
od;
Print("  # diagonal class vectors among them = ",
      Number(cvs, v -> Length(Set(v))=1),"\n");
Print("  distinct class vectors = ",Length(Set(cvs))," of ",Length(cvs)," dessins\n");

## Out(P) = C3 action on the P-dessins, realised by N_{S9}(P)/P
Print("\n  Out-action (N_{S9}(P)/P) orbit structure on the P-dessins:\n");
reps := List(orbP, o -> o[1]);;
IdxOf := function(t)
  local i, g;
  for i in [1..Length(orbP)] do
    for g in Elements(psl) do
      if List(orbP[i][1], a -> a^g) = t then return i; fi;
    od;
  od;
  return fail;
end;;
cosreps := List(RightCosets(NS,psl), c -> Representative(c));;
Print("   coset reps of P in N: ",Length(cosreps),"\n");
for h in cosreps do
  Print("    h -> permutation of dessin indices: ",
        List([1..Length(reps)], i -> IdxOf(List(reps[i], a -> a^h))),"\n");
od;

Print("\n== DONE ==\n");
QUIT;
