#############################################################################
## search/probe/wac_v1/a13_check3.g
##  Is there a tail-4 window with SQUAREFREE N_ord, i.e. the control that
##  isolates the "N_ord = 9 is not squarefree" variable of W-E-A13-9t4?
##  Ree sweep says the tail-4 family is {ell = 5, 9, 11, 13, 15, ...} (ell = 7 dead).
##  ell = 5 -> n = 9 : exhaustive over all involutions of S9.
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit. No sealed symbol.
#############################################################################
WacCyc := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;
WacBlock := function(blocks, len)
  local p, i, base;
  p := (); base := 0;
  for i in [1..blocks] do
    p := p * WacCyc(List([1..len], j -> base+j)); base := base + len;
  od;
  return p;
end;;
NC := function(p, n)
  return n - NrMovedPoints(p) + Length(Cycles(p, MovedPoints(p)));
end;;

nn := 9;;
uu := (1,2,3,4,5)(6,7)(8,9);;
S9 := SymmetricGroup(9);; A9 := AlternatingGroup(9);;
Print("u = ", uu, "  type ", CycleStructurePerm(uu), " ord ", Order(uu),
      "  xbar = ", uu^2, " type ", CycleStructurePerm(uu^2),
      " ord ", Order(uu^2), "\n");
Print("Ree: c(u) = ", NC(uu,9), "\n");
hits := 0;; good := [];; sizes := [];;
for k in [1..4] do
  for a in AsList(ConjugacyClass(S9, WacBlock(k,2))) do
    b := a * uu^-1;
    if b^3 = () and b <> () then
      hits := hits + 1;
      G := Group(a,b);
      Add(sizes, [k, Size(G)]);
      if G = A9 or G = S9 then Add(good, [a,b]); fi;
    fi;
  od;
od;
Print("#(a with b^3=1) = ", hits, "\n");
for rep in Set(sizes) do
  Print("   [k=", rep[1], " |<a,b>|=", rep[2], "] x ", Number(sizes, z->z=rep), "\n");
od;
Print("realizing pairs (A9 or S9): ", Length(good), "\n");
if Length(good) > 0 then
  a1 := good[1][1];; b1 := good[1][2];;
  Print("a1 = ", a1, "\nb1 = ", b1, "\n");
  Print("Ree c(a)+c(b)+c(u) = ", NC(a1,9), "+", NC(b1,9), "+", NC(uu,9),
        " = ", NC(a1,9)+NC(b1,9)+NC(uu,9), "   n+2 = 11\n");
  aE := a1*(10,12);; bE := b1*(10,12,11);;
  WinE := Group(aE,bE);;
  s1 := bE^-1*aE;; s2 := aE*bE^2;; cc := (s1*s2)^3;;
  xb := s1^2;; yb := s2^2;; PN := Group(xb,yb);;
  Print("|E| = ", Size(WinE), "  = 6|A9| ? ", Size(WinE)=6*Size(A9), "\n");
  Print("braid ? ", s1*s2*s1=s2*s1*s2, "   c=1 ? ", cc=(), "\n");
  Print("|P| = ", Size(PN), " = |A9| ? ", Size(PN)=Size(A9), "\n");
  Print("N_ord = ", Lcm(Order(xb),Order(yb),Order(cc)), "\n");
  CPy := Centralizer(PN, yb);;
  StabX := Centralizer(S9, uu^2);;
  Print("C_P(ybar) = ", Size(CPy), " ", StructureDescription(CPy), "\n");
  Print("Stab(xbar) = ", Size(StabX), " ", StructureDescription(StabX),
        "  Syl2 = ", Size(SylowSubgroup(StabX,2)), " ",
        StructureDescription(SylowSubgroup(StabX,2)), "\n");
  Print("Stab solvable ? ", IsSolvable(StabX), "\n");
  charm := Filtered([0..4], m -> GcdInt(2*m+1,5)=1);;
  Print("charming m = ", charm, " cm = ", Length(charm), "\n");
  Print("Xi budget = ", Length(charm)*Size(CPy)*Size(StabX), "\n");
  Print("naive budget = ", Length(charm)*Size(A9), "\n");
  Print("JUDGE_S1_IMG := ", s1, ";;\n");
  Print("JUDGE_S2_IMG := ", s2, ";;\n");
  Print("JUDGE_ID := \"W-E-A9-5t4\";;   ## degree(E) = 12\n");
fi;
Print("\nA13_CHECK3_DONE\n");
QUIT;
