LogTo();
LoadPackage("fr");;
# adding machine as a Mealy automaton: state 1 = a, state 2 = identity
M := MealyMachine([[2,1],[2,2]], [(1,2),()]);;
Print("MealyMachine built : ", M <> fail, "\n");
a := MealyElement(M, 1);;
Print("Activity(a,3) = ", Activity(a,3), "\n");
Print("IsContracting(M) = ", IsContracting(M), "\n");
Print("NucleusOfFRMachine(M) = ", NucleusOfFRMachine(M), "\n");
G := Group(a);;
Print("IsContracting(G) = ", IsContracting(G), "\n");
Print("NucleusOfFRSemigroup(G) = ", NucleusOfFRSemigroup(G), "\n");
Print("IsOne(a^4) = ", IsOne(a^4), "\n");
Print("DONE\n");
QUIT;
