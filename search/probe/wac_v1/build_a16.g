#############################################################################
## search/probe/wac_v1/build_a16.g -- WA-c: build the window W-D-A16-11a
## E = A16 x S3 (degree 19), s1 = b^-1 a, s2 = a^-1 b^2.
## Single lane. NOT a ledger claim. No commit.
#############################################################################

WacCT := function(p, n)
  return SortedList(List(Orbits(Group(p), [1..n]), Length));
end;;

a1 := ( 1, 2)( 3,14)( 4,10)( 5,12)( 6, 8)( 7,16)( 9,13)(11,15);;
b1 := ( 2,11,14)( 3,15,10)( 4, 9,12)( 5,13, 8)( 6, 7,16);;
A16 := AlternatingGroup(16);; S16 := SymmetricGroup(16);;
Print("a1^2=1? ", a1^2 = (), "  b1^3=1? ", b1^3 = (), "  <a1,b1>=A16? ",
      Group(a1,b1) = A16, "\n");
uu := b1^-1*a1;;
Print("u type=", WacCT(uu,16), " ord=", Order(uu),
      "  u^2 type=", WacCT(uu^2,16), " ord=", Order(uu^2), "\n\n");

S3 := SymmetricGroup(3);;
D := DirectProduct(A16, S3);;
e1 := Embedding(D,1);; e2 := Embedding(D,2);;
a := Image(e1,a1)*Image(e2,(1,3));;
b := Image(e1,b1)*Image(e2,(1,3,2));;
s1 := b^-1*a;;  s2 := a^-1*b^2;;
Print("=== window checks ===\n");
Print("a^2=1? ", a^2=One(D), "  b^3=1? ", b^3=One(D), "\n");
Print("braid s1s2s1=s2s1s2 ? ", s1*s2*s1 = s2*s1*s2, "\n");
Print("c=(s1s2)^3=1 ? ", (s1*s2)^3 = One(D), "   (c in N)\n");
Print("ord(s1)=", Order(s1), " ord(s2)=", Order(s2), "\n");
Print("<s1,s2>=E ? ", Group(s1,s2)=D, "  |E|=[B3:N]=", Size(D), "\n");
P := Group(s1^2, s2^2);;
pr2 := Projection(D,2);;
Print("|P|=", Size(P), "  P=ker(E->>S3)? ", P = Kernel(pr2),
      "  P=|A16|? ", Size(P)=Size(A16), "\n");
Print("ord(xbar)=", Order(s1^2), " ord(ybar)=", Order(s2^2), "\n");
x1 := PreImagesRepresentative(e1, s1^2);;
y1 := PreImagesRepresentative(e1, s2^2);;
Print("xbar type=", WacCT(x1,16), "  ybar type=", WacCT(y1,16),
      "  support overlap=", Size(Intersection(MovedPoints(x1),MovedPoints(y1))), "\n");
Print("N_ord = lcm(11,11,1) = ", Lcm(Order(s1^2),Order(s2^2),1), "\n");
Print("charming m count = phi(2*N_ord) = ", Phi(2*Lcm(Order(s1^2),Order(s2^2),1)), "\n\n");

Print("=== Hol sieve quantities (Prop 7.1 / Cor 7.2) ===\n");
cy := Centralizer(A16, y1);;  cx := Centralizer(A16, x1);;
sx := Centralizer(S16, x1);;  sy := Centralizer(S16, y1);;
Print("C_P(ybar): |", Size(cy), "| solvable=", IsSolvableGroup(cy),
      " struct=", StructureDescription(cy), "\n");
Print("Stab_Aut(P)(xbar) = C_S16(xbar): |", Size(sx), "| solvable=",
      IsSolvableGroup(sx), " struct=", StructureDescription(sx), "\n");
Print("C_P(xbar)=", Size(cx), "  C_S16(ybar)=", Size(sy), "\n");
Print("=> BOTH nonsolvable: Cor 7.2 necessary condition SATISFIED\n\n");

Print("=== budgets ===\n");
Print("naive (judge v1.1 loop over [P,P]) = c_m * |[P,P]| = ",
      Phi(22), " * ", Size(DerivedSubgroup(P)), " = ",
      Phi(22)*Size(DerivedSubgroup(P)), "\n");
Print("Xi-restricted per m           = |C_P(ybar)| * |Stab| = ",
      Size(cy), " * ", Size(sx), " = ", Size(cy)*Size(sx), "\n");
Print("Xi-restricted total           = ", Phi(22)*Size(cy)*Size(sx), "\n");
Print("=> |ker chi~| <= ", Size(cy)*Size(sx),
      " ,  |G_N| <= ", Phi(22)*Size(cy)*Size(sx), "\n\n");

Print("=== judge input (mode (b)) ===\n");
Print("JUDGE_S1_IMG := ", s1, ";;\n");
Print("JUDGE_S2_IMG := ", s2, ";;\n");
Print("degree of E = ", LargestMovedPoint(D), "\n");
Print("\nBUILD_DONE\n");
QUIT;
