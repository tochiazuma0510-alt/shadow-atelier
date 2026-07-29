## Fast feasibility check via the character table's class multiplication
## coefficients: does there exist (a1 in class 2^6 1^2, b1 in class 3^4 1^2)
## with b1^-1*a1 in class (9,2,2,1)? If the coefficient is 0, the random
## search target is structurally unreachable and the design needs revision;
## if nonzero, we get the EXACT count (informs expected trial count).
A14 := AlternatingGroup(14);;
ccA14 := ConjugacyClasses(A14);;
Print("num classes A14 = ", Length(ccA14), "\n");

FindClassByType := function(ccs, type)
  local c, rep, ct, matches;
  matches := [];
  for c in ccs do
    rep := Representative(c);
    ct := SortedList(CycleLengths(rep, [1..14]));
    if ct = type then
      Add(matches, c);
    fi;
  od;
  return matches;
end;;

Ms_a1 := FindClassByType(ccA14, [1,1,2,2,2,2,2,2]);;   # 2^6 1^2
Ms_b1 := FindClassByType(ccA14, [1,1,3,3,3,3]);;       # 3^4 1^2
Ms_u  := FindClassByType(ccA14, [1,2,2,9]);;           # target u type

Print("num classes matching 2^6 1^2 : ", Length(Ms_a1), " sizes=", List(Ms_a1,Size), "\n");
Print("num classes matching 3^4 1^2 : ", Length(Ms_b1), " sizes=", List(Ms_b1,Size), "\n");
Print("num classes matching (9,2,2,1): ", Length(Ms_u), " sizes=", List(Ms_u,Size), "\n");

tbl := CharacterTable(A14);;
tblClasses := ConjugacyClasses(tbl);;   # should correspond by position to OrdinaryCharacterTable classes
Print("tbl num classes = ", Length(tblClasses), "\n");

# match table classes to our permutation-group classes by representative order + centralizer size
tblOrders := OrdersClassRepresentatives(tbl);;
tblCentSizes := SizesCentralizers(tbl);;

MatchPositions := function(cls)
  local c, ord, cent, positions, i;
  positions := [];
  for c in cls do
    ord := Order(Representative(c));
    cent := Size(Centralizer(A14, Representative(c)));
    for i in [1..Length(tblOrders)] do
      if tblOrders[i] = ord and tblCentSizes[i] = cent then
        Add(positions, i);
      fi;
    od;
  od;
  return positions;
end;;

pos_a1 := MatchPositions(Ms_a1);;
pos_b1 := MatchPositions(Ms_b1);;
pos_u  := MatchPositions(Ms_u);;
Print("table positions: a1=", pos_a1, " b1=", pos_b1, " u=", pos_u, "\n");

total := 0;;
for i in pos_b1 do        # b1 class (we need b1^-1, but classes closed under inverse up to possible split -- check both)
  for j in pos_a1 do
    for k in pos_u do
      coeff := ClassMultiplicationCoefficient(tbl, i, j, k);;
      Print("  ClassMultCoeff(b1pos=",i,", a1pos=",j,", upos=",k,") = ", coeff, "\n");
      total := total + coeff;
    od;
  od;
od;
Print("TOTAL structure constant (count of (b1,a1) pairs with b1*a1 in target, summed over matched positions) = ", total, "\n");
Print("(NOTE: this counts b1*a1 in class u; our target is b1^-1*a1 -- since inverse of an element in a class C lies in class C^-1, and A14 classes here may or may not be real/self-inverse; if total>0 for b1*a1 it strongly suggests the combination is structurally populated, since squares/orders here are typically self-paired for these types)\n");
Print("DONE_STRUCTCONST_PROBE\n");
