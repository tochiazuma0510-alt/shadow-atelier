# Audit probe: theoretical floors for the wall campaign (single-lane, non-registered)
Print("=== c_m(N) = phi(2M) ? ===\n");
bad := [];;
for M in [1..200] do
  cm := Length(Filtered([0..M-1], m -> Gcd(2*m+1, M) = 1));
  if cm <> Phi(2*M) then Add(bad, [M, cm, Phi(2*M)]); fi;
od;
Print("M in [1..200]: mismatches = ", bad, "\n");

Print("\n=== minimal order of a 2-generated finite group with |G'| >= 6 ===\n");
found := fail;;
for n in [1..60] do
  if found <> fail then break; fi;
  for i in [1..NrSmallGroups(n)] do
    G := SmallGroup(n,i);
    if Size(DerivedSubgroup(G)) >= 6 then
      if Length(MinimalGeneratingSet(G)) <= 2 then
        found := [n, i, StructureDescription(G), Size(DerivedSubgroup(G)),
                  StructureDescription(DerivedSubgroup(G))];
        break;
      fi;
    fi;
  od;
od;
Print("min: ", found, "\n");

Print("\n=== minimal order of a 2-generated finite group with NONABELIAN G' ===\n");
found2 := fail;;
for n in [1..80] do
  if found2 <> fail then break; fi;
  for i in [1..NrSmallGroups(n)] do
    G := SmallGroup(n,i);
    if not IsAbelian(DerivedSubgroup(G)) then
      if Length(MinimalGeneratingSet(G)) <= 2 then
        found2 := [n, i, StructureDescription(G), Size(DerivedSubgroup(G)),
                   StructureDescription(DerivedSubgroup(G))];
        break;
      fi;
    fi;
  od;
od;
Print("min: ", found2, "\n");

Print("\n=== minimal order of a 2-generated finite group with |G'| >= 60 ===\n");
found3 := fail;;
for n in [1..70] do
  if found3 <> fail then break; fi;
  for i in [1..NrSmallGroups(n)] do
    G := SmallGroup(n,i);
    if Size(DerivedSubgroup(G)) >= 60 then
      if Length(MinimalGeneratingSet(G)) <= 2 then
        found3 := [n, i, StructureDescription(G), Size(DerivedSubgroup(G))];
        break;
      fi;
    fi;
  od;
od;
Print("min: ", found3, "\n");

Print("\n=== minimal order of a 2-generated finite group with a NONSOLVABLE G' ===\n");
found4 := fail;;
for n in [1..130] do
  if found4 <> fail then break; fi;
  for i in [1..NrSmallGroups(n)] do
    G := SmallGroup(n,i);
    if not IsSolvableGroup(DerivedSubgroup(G)) then
      if Length(MinimalGeneratingSet(G)) <= 2 then
        found4 := [n, i, StructureDescription(G), Size(DerivedSubgroup(G))];
        break;
      fi;
    fi;
  od;
od;
Print("min: ", found4, "\n");
QUIT;
