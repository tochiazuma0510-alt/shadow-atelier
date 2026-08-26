# math_gdyn_fr_probe_v2.g -- FR contraction/nucleus smoke test (corrected constructor)
LogTo();
LoadPackage("fr");;
M := FRMachine([[[],[1]]],[(1,2)]);;          # adding machine  a = <1,a> sigma
a := FRElement(M,1);;
G := Group(a);;
Print("element built : ", a, "\n");
Print("Activity(a,3) = ", Activity(a,3), "\n");
Print("IsContracting(M) = ", IsContracting(M), "\n");
Print("NucleusOfFRMachine(M) = ", NucleusOfFRMachine(M), "\n");
Print("IsContracting(G) = ", IsContracting(G), "\n");
Print("NucleusOfFRSemigroup(G) = ", NucleusOfFRSemigroup(G), "\n");
Print("LimitStates(a) = ", LimitStates(a), "\n");
Print("--- word problem: is a^4 trivial as a tree automorphism ? ---\n");
Print("  Activity(a^4,2) = ", Activity(a^4,2), " trivial ? ", Activity(a^4,2)=(), "\n");
Print("  Activity(a^4,3) = ", Activity(a^4,3), " trivial ? ", Activity(a^4,3)=(), "\n");
Print("  IsOne(a^4) = ", IsOne(a^4), "   <- FR decides this using the nucleus\n");
Print("  => finite-depth triviality does NOT imply tree-triviality; IsOne is the decision\n");
Print("--- Grigorchuk (known contracting, nontrivial relations) ---\n");
if IsBoundGlobal("GrigorchukGroup") then
  Gg := GrigorchukGroup;;
  Print("  GrigorchukGroup available ; IsContracting = ", IsContracting(Gg), "\n");
  Print("  Nucleus size = ", Length(NucleusOfFRSemigroup(Gg)), "\n");
else
  Print("  GrigorchukGroup : absent\n");
fi;
Print("DONE\n");
QUIT;
