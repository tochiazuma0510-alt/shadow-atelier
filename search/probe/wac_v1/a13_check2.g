#############################################################################
## search/probe/wac_v1/a13_check2.g
##  Follow-up to a13_check.g: extract canonical realizing pairs and full window
##  asserts for the NEW N_ord = 9 vehicles found at tails t = 1, 2, 3
##  (t=0 is Ree-permissible but exhaustively non-realizable; t=4 is the known
##   W-E-A13-9t4).  Odd-k branches use the fibre product E = S3 x_{C2} S_n.
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

## find the lexicographically first realizing pair for a given (n, u)
FindPair := function(nn, uu)
  local Snn, Ann, k, cls, a, b, G, best;
  Snn := SymmetricGroup(nn); Ann := AlternatingGroup(nn);
  for k in [1..Int(nn/2)] do
    cls := AsList(ConjugacyClass(Snn, WacBlock(k,2)));
    for a in cls do
      b := a * uu^-1;
      if b^3 = () and b <> () then
        G := Group(a,b);
        if G = Ann or G = Snn then return [a, b, G = Ann]; fi;
      fi;
    od;
  od;
  return fail;
end;;

## full window assert for a (2,3)-pair (a1,b1) generating A_n (even) or S_n (odd)
Window := function(nn, a1, b1, id)
  local sh, aE, bE, WinE, s1, s2, cc, xb, yb, PN, Nord, CPy, StabX, Snn, Ann,
        charm, xbar, cm, Xi, naive, Sy;
  Snn := SymmetricGroup(nn); Ann := AlternatingGroup(nn);
  Print("\n===== ", id, "   (n=", nn, ") =====\n");
  Print("a1 = ", a1, "\n");
  Print("b1 = ", b1, "\n");
  Print("a1^2=1 ", a1^2=(), "  b1^3=1 ", b1^3=(),
        "  sign(a1)=", SignPerm(a1), "  sign(b1)=", SignPerm(b1), "\n");
  Print("<a1,b1> = ", Size(Group(a1,b1)), "   A_n ? ", Group(a1,b1)=Ann,
        "   S_n ? ", Group(a1,b1)=Snn, "\n");
  xbar := (b1^-1*a1)^2;
  Print("u type ", CycleStructurePerm(b1^-1*a1), " ord ", Order(b1^-1*a1),
        "   xbar type ", CycleStructurePerm(xbar), " ord ", Order(xbar), "\n");
  Print("Ree c(a)+c(b)+c(u) = ", NC(a1,nn), "+", NC(b1,nn), "+", NC(b1^-1*a1,nn),
        " = ", NC(a1,nn)+NC(b1,nn)+NC(b1^-1*a1,nn), "   n+2 = ", nn+2,
        "   genus = ",
        ((3*nn - (NC(a1,nn)+NC(b1,nn)+NC(b1^-1*a1,nn))) - 2*nn + 2)/2, "\n");
  ## E inside S_{n+3}
  aE := a1 * (nn+1, nn+3);
  bE := b1 * (nn+1, nn+3, nn+2);
  WinE := Group(aE, bE);
  Print("|E| = ", Size(WinE), "   = 6|A_n| ? ", Size(WinE) = 6*Size(Ann), "\n");
  s1 := bE^-1*aE; s2 := aE*bE^2;
  Print("braid ? ", s1*s2*s1 = s2*s1*s2, "   ord(s1)=", Order(s1), "\n");
  cc := (s1*s2)^3;
  Print("c = (s1s2)^3 = 1 ? ", cc = (), "   <== c in N\n");
  xb := s1^2; yb := s2^2; PN := Group(xb,yb);
  Print("|P| = ", Size(PN), "   = |A_n| ? ", Size(PN) = Size(Ann), "\n");
  Nord := Lcm(Order(xb), Order(yb), Order(cc));
  Print("ord(x)=", Order(xb), " ord(y)=", Order(yb), " ord(c)=", Order(cc),
        "   N_ord = ", Nord, "\n");
  CPy := Centralizer(PN, yb);
  StabX := Centralizer(Snn, xbar);
  Print("C_P(ybar)  = ", Size(CPy), "  ", StructureDescription(CPy),
        "   Syl2 = ", Size(SylowSubgroup(CPy,2)), "\n");
  Print("Stab(xbar) = ", Size(StabX), "  ", StructureDescription(StabX),
        "   Syl2 = ", Size(SylowSubgroup(StabX,2)), " ",
        StructureDescription(SylowSubgroup(StabX,2)), "\n");
  Print("Stab solvable ? ", IsSolvable(StabX), "   [P,P]=P ? ",
        DerivedSubgroup(PN)=PN, "\n");
  charm := Filtered([0..Nord-1], m -> GcdInt(2*m+1, Nord) = 1);
  cm := Length(charm);
  Print("charming m = ", charm, "  cm = ", cm, "\n");
  Xi := cm * Size(CPy) * Size(StabX);
  naive := cm * Size(Ann);
  Print("Xi budget    = ", Xi, "\n");
  Print("naive budget = ", naive, "\n");
  Print("judge preamble:\n");
  Print("JUDGE_S1_IMG := ", s1, ";;\n");
  Print("JUDGE_S2_IMG := ", s2, ";;\n");
  Print("JUDGE_ID := \"", id, "\";;   ## degree(E) = ", nn+3, "\n");
  return;
end;;

Print("################ t=1 : n=10, u = 9-cycle ################\n");
p := FindPair(10, WacCyc([1..9]));;
Window(10, p[1], p[2], "W-E-A10-9t1");

Print("\n################ t=2 : n=11, u = (1..9)(10,11) ################\n");
p := FindPair(11, WacCyc([1..9])*(10,11));;
Window(11, p[1], p[2], "W-E-A11-9t2");

Print("\n################ t=3 : n=12, u = (1..9)(10,11) ################\n");
p := FindPair(12, WacCyc([1..9])*(10,11));;
Window(12, p[1], p[2], "W-E-A12-9t3");

Print("\n################ t=4 : n=13 (known window, for comparison) ###\n");
a13 := (2,10)(3,8)(4,12)(5,6)(7,13)(9,11);;
u13 := (1,2,3,4,5,6,7,8,9)(10,11)(12,13);;
Window(13, a13, a13*u13^-1, "W-E-A13-9t4");

Print("\nA13_CHECK2_DONE\n");
QUIT;
