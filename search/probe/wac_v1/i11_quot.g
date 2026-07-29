## normal subgroup / quotient lattice of the census component groups (Goursat)
G1 := SmallGroup(324,160);;
Print("324 = ", StructureDescription(G1), "  AbelianInvariants = ",
      AbelianInvariants(G1), "  has index-2 subgroup ? ",
      ForAny(NormalSubgroups(G1), N -> Index(G1,N)=2), "\n");
G2 := SmallGroup(1512,779);;
Print("1512 = ", StructureDescription(G2), "  AbelianInvariants = ",
      AbelianInvariants(G2), "\n");
Print("   normal subgroup indices = ",
      SortedList(List(NormalSubgroups(G2), N -> Index(G2,N))), "\n");
G3 := SmallGroup(504,156);;
Print("504 = ", StructureDescription(G3), "  simple ? ", IsSimpleGroup(G3), "\n");
S11 := SymmetricGroup(11);;
Print("S11 normal indices = ",
      SortedList(List(NormalSubgroups(S11), N -> Index(S11,N))), "\n");
Print("A10 simple ? ", IsSimpleGroup(AlternatingGroup(10)),
      "   A13 simple ? ", IsSimpleGroup(AlternatingGroup(13)), "\n");
S3 := SymmetricGroup(3);;
Print("S3 normal indices = ",
      SortedList(List(NormalSubgroups(S3), N -> Index(S3,N))), "\n");
Print("I11_QUOT_DONE\n");
QUIT;
