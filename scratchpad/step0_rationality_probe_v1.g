## Field of moduli prediction for the RIGID (C,C,C) triple, C = our order-9 class.
Read("search/drophunt_checker_producer_v2.g");;
G := Group(DCP2X4, DCP2Y4);;
cc := ConjugacyClasses(G);;
ourC := First(cc, c -> DCP2X4 in c);;
Print("FR_OUR_CLASS_ORDER ", Order(Representative(ourC)), " size ", Size(ourC), "\n");
Print("FR_XY_SAME_CLASS ", DCP2Y4 in ourC, "  ", (DCP2X4*DCP2Y4)^-1 in ourC, "\n");
g := Representative(ourC);;
Print("FR_POWER_MAP  k in (Z/9)^*  ->  is g^k in the SAME class?\n");
stab := [];;
for k in [1,2,4,5,7,8] do
  same := g^k in ourC;;
  if same then Add(stab,k); fi;
  Print("   k=", k, "  g^k in C : ", same, "\n");
od;
Print("FR_STABILISER ", stab, "  order ", Length(stab), "\n");
Print("FR_ORBIT_LENGTH ", 6/Length(stab), "\n");
Print("FR_PREDICTED_FIELD_DEGREE ", Length(stab) = 2, " -> fixed field of a subgroup of order ",
      Length(stab), " in (Z/9)^* (=C6);  degree over Q = ", 6/Length(stab), "\n");
## which classes are the images
Print("FR_ORBIT_OF_C  ", List([1,2,4,5,7,8], k -> PositionProperty(cc, c -> g^k in c)), "\n");
QUIT;
