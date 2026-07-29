#############################################################################
## search/probe/wac_v1/a13_check.g
##  Mathematician's verification for the A13 mathcheck (W3-1, stage 1).
##  (1) W-E-A13-9t4 window assert (Prop 0.3 construction, c in N, N_ord=9,
##      charming set, Xi budget).
##  (2) W-D-A19-13t6 explicit window re-check (odd-k branch, Ree bookkeeping).
##  (3) N_ord = 9 vehicle census for tails t = 0,1,2,3 (exhaustive over all
##      involutions of S_n) -- is the tail-4 vehicle really unique?
##  (4) tail-4 recount: number of realizing pairs for u = (1..9)(10,11)(12,13).
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
## number of cycles on n points, fixed points included
NC := function(p, n)
  return n - NrMovedPoints(p) + Length(Cycles(p, MovedPoints(p)));
end;;

Print("#########################################################\n");
Print("## PART 1  W-E-A13-9t4 window assert\n");
Print("#########################################################\n");

n13 := 13;;
S13 := SymmetricGroup(13);; A13 := AlternatingGroup(13);;
a1 := (2,10)(3,8)(4,12)(5,6)(7,13)(9,11);;
u0 := (1,2,3,4,5,6,7,8,9)(10,11)(12,13);;
b1 := a1 * u0^-1;;
Print("b1 (rederived)        = ", b1, "\n");
Print("a1^2 = 1              ? ", a1^2 = (), "\n");
Print("b1^3 = 1              ? ", b1^3 = (), "\n");
Print("b1^-1*a1 = u0         ? ", b1^-1*a1 = u0, "\n");
Print("sign(a1)              = ", SignPerm(a1), "   (even => image A13)\n");
G13 := Group(a1,b1);;
Print("<a1,b1> = A13         ? ", G13 = A13, "   |G| = ", Size(G13), "\n");
Print("u  cyclestruct        = ", CycleStructurePerm(u0), "  ord = ", Order(u0), "\n");
xbar13 := u0^2;;
Print("xbar = u^2 cyclestr   = ", CycleStructurePerm(xbar13), "  ord = ", Order(xbar13), "\n");
Print("Ree bookkeeping: c(a')=", NC(a1,13), " c(b')=", NC(b1,13), " c(u')=", NC(u0,13),
      "  sum = ", NC(a1,13)+NC(b1,13)+NC(u0,13), "   n+2 = ", 15, "\n");
Print("genus of the cover    = ",
      ((3*13 - (NC(a1,13)+NC(b1,13)+NC(u0,13))) - 2*13 + 2)/2, "\n");

## Prop 0.3 : E = A13 x S3 inside S16 (1..13 = A13 factor, 14,15,16 = S3)
aE := a1 * (14,16);;
bE := b1 * (14,16,15);;
WinE := Group(aE,bE);;
Print("|E|                   = ", Size(WinE), "\n");
Print("|E| = 6*|A13|         ? ", Size(WinE) = 6*Size(A13), "\n");
Print("aE^2 = bE^3 = 1       ? ", aE^2 = () and bE^3 = (), "\n");
s1 := bE^-1*aE;; s2 := aE*bE^2;;
Print("braid s1s2s1=s2s1s2   ? ", s1*s2*s1 = s2*s1*s2, "\n");
cc := (s1*s2)^3;;
Print("c = (s1s2)^3 = 1      ? ", cc = (), "    <== c in N\n");
Print("ord(s1), ord(s2)      = ", Order(s1), ", ", Order(s2), "\n");
xb := s1^2;; yb := s2^2;;
PN := Group(xb,yb);;
Print("|<xbar,ybar>|         = ", Size(PN), "   = |A13| ? ", Size(PN) = Size(A13), "\n");
Print("ord(xbar), ord(ybar)  = ", Order(xb), ", ", Order(yb), "   ord(cbar) = ", Order(cc), "\n");
Print("N_ord = lcm(x,y,c)    = ", Lcm(Order(xb), Order(yb), Order(cc)), "\n");
Print("xbar type             = ", CycleStructurePerm(xb), "\n");
Print("ybar type             = ", CycleStructurePerm(yb), "\n");
Print("supports overlap in   = ", Length(Intersection(MovedPoints(xb), MovedPoints(yb))), " points\n");

CPy := Centralizer(PN, yb);;
StabX := Centralizer(S13, xbar13);;
Print("|C_P(ybar)|           = ", Size(CPy), "  struct = ", StructureDescription(CPy), "\n");
Print("|Stab_Aut(P)(xbar)|   = ", Size(StabX), "  struct = ", StructureDescription(StabX), "\n");
Print("Syl2(Stab) order/str  = ", Size(SylowSubgroup(StabX,2)), " / ",
      StructureDescription(SylowSubgroup(StabX,2)), "\n");
Print("Syl2(C_P(ybar))       = ", Size(SylowSubgroup(CPy,2)), " / ",
      StructureDescription(SylowSubgroup(CPy,2)), "\n");
Print("Stab solvable         ? ", IsSolvable(StabX), "   (Cor 7.2 needs NON-solvable)\n");
Print("[P,P] = P (perfect)   ? ", DerivedSubgroup(PN) = PN, "   (charming f-condition vacuous)\n");

Nord := 9;;
charm := Filtered([0..Nord-1], m -> GcdInt(2*m+1, Nord) = 1);;
Print("charming m            = ", charm, "  count = ", Length(charm),
      "  phi(Nord) = ", Phi(Nord), "  phi(2*Nord) = ", Phi(2*Nord), "\n");
for m in charm do
  Print("   m=", m, "  2m+1 mod 9 = ", (2*m+1) mod 9,
        "  xbar^(2m+1) type ", CycleStructurePerm(xbar13^(2*m+1)),
        "  A_m nonempty ? ", RepresentativeAction(S13, xbar13, xbar13^(2*m+1)) <> fail,
        "  C_P(ybar^(2m+1)) = ", Size(Centralizer(PN, yb^(2*m+1))), "\n");
od;
Print("Xi budget = cm*|C_P(y)|*|Stab| = ",
      Length(charm)*Size(CPy)*Size(StabX), "\n");
Print("naive budget = cm*|[P,P]|      = ", Length(charm)*Size(A13), "\n");

Print("\n#########################################################\n");
Print("## PART 2  W-D-A19-13t6 re-check (odd-k branch)\n");
Print("#########################################################\n");
a19 := (1,19)(3,18)(4,13)(5,15)(6,11)(7,17)(8,9)(10,16)(12,14);;
b19 := (1,18,2)(3,19,13)(4,12,15)(5,14,11)(6,10,17)(7,16,9);;
Print("a^2=1 ? ", a19^2 = (), "   b^3=1 ? ", b19^3 = (),
      "   sign(a)=", SignPerm(a19), "  sign(b)=", SignPerm(b19), "\n");
u19 := b19^-1*a19;;
Print("u type ", CycleStructurePerm(u19), "  ord ", Order(u19),
      "   xbar type ", CycleStructurePerm(u19^2), "  ord ", Order(u19^2), "\n");
Print("Ree: c(a)=", NC(a19,19), " c(b)=", NC(b19,19), " c(u)=", NC(u19,19),
      "  sum = ", NC(a19,19)+NC(b19,19)+NC(u19,19), "   n+2 = 21\n");
G19 := Group(a19,b19);;
Print("<a,b> = S19 ? ", G19 = SymmetricGroup(19), "   |G| = ", Size(G19), "\n");

Print("\n#########################################################\n");
Print("## PART 3  N_ord = 9 vehicle census, tails t = 0,1,2,3\n");
Print("#########################################################\n");

Census := function(nn, uu)
  local Snn, Ann, k, cls, a, b, hits, sizes, sgn, G, rep, ok;
  Snn := SymmetricGroup(nn); Ann := AlternatingGroup(nn);
  hits := 0; sizes := [];
  for k in [1..Int(nn/2)] do
    cls := AsList(ConjugacyClass(Snn, WacBlock(k,2)));
    for a in cls do
      b := a * uu^-1;
      if b^3 = () and b <> () then
        hits := hits + 1;
        G := Group(a,b);
        ok := "other";
        if G = Ann then ok := "A_n"; elif G = Snn then ok := "S_n"; fi;
        Add(sizes, [k, SignPerm(a), Size(G), ok]);
      fi;
    od;
  od;
  Print("   n=", nn, "  u=", CycleStructurePerm(uu),
        "  #(a with b^3=1) = ", hits, "\n");
  Print("      c(u) = ", NC(uu,nn), "\n");
  for rep in Set(sizes) do
    Print("      [k=", rep[1], " sign=", rep[2], " |<a,b>|=", rep[3], " ", rep[4], "] x ",
          Number(sizes, z -> z = rep), "\n");
  od;
  Print("      ANY = A_n ? ", ForAny(sizes, z -> z[4] = "A_n"),
        "   ANY = S_n ? ", ForAny(sizes, z -> z[4] = "S_n"), "\n");
  return;
end;;

Print("-- t=0 : n=9,  u = (1..9)\n");
Census(9, WacCyc([1..9]));
Print("-- t=1 : n=10, u = (1..9), point 10 fixed\n");
Census(10, WacCyc([1..9]));
Print("-- t=2 : n=11, u = (1..9)(10,11)\n");
Census(11, WacCyc([1..9])*(10,11));
Print("-- t=2b: n=11, u = (1..9), points 10,11 fixed\n");
Census(11, WacCyc([1..9]));
Print("-- t=3 : n=12, u = (1..9)(10,11), point 12 fixed\n");
Census(12, WacCyc([1..9])*(10,11));
Print("-- t=3b: n=12, u = (1..9), points 10,11,12 fixed\n");
Census(12, WacCyc([1..9]));

Print("\n#########################################################\n");
Print("## PART 4  tail-4 recount, u = (1..9)(10,11)(12,13)\n");
Print("#########################################################\n");
Census(13, WacCyc([1..9])*(10,11)*(12,13));

Print("\nA13_CHECK_DONE\n");
QUIT;
