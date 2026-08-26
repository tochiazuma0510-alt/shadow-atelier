# math_gdyn_fr_probe_v1.g -- FR capability probe for the ker(F2 -> IMG(T)) question
LogTo();
ok := LoadPackage("fr");;
Print("fr loaded : ", ok, "  version ", InstalledPackageVersion("fr"), "\n");
probe := function(name)
  local f;
  f := ValueGlobal(name);
  Print("  ", name, " : ", IsBound(f) and f <> fail, "\n");
end;;
Print("--- available FR operations ---\n");
for nm in ["NucleusOfFRMachine","NucleusOfFRSemigroup","IsContracting","IsLevelTransitive",
           "IsBoundedFRMachine","IsFinitaryFRElement","StateSet","Activity","LimitStates",
           "FRMachineNC","IMGMachine","PolynomialIMGMachine","IsomorphismFRGroup",
           "FRGroup","Nucleus","IsFRElement","DecompositionOfFRElement"] do
  if IsBoundGlobal(nm) then Print("  ", nm, " : BOUND\n"); else Print("  ", nm, " : absent\n"); fi;
od;

Print("--- smoke test on the adding machine (known contracting, nucleus {1,a,a^-1}) ---\n");
M := FRMachine([[[],[1]]],[(1,2)]);;
G := FRGroup(M);;
Print("  FRGroup built : ", G <> fail, "  Size level3 = ",
      Size(Group(List(GeneratorsOfGroup(G), g -> Activity(g,3)))), "\n");
if IsBoundGlobal("IsContracting") then
  Print("  IsContracting(G) = ", IsContracting(G), "\n");
fi;
if IsBoundGlobal("NucleusOfFRSemigroup") then
  Print("  NucleusOfFRSemigroup(G) = ", NucleusOfFRSemigroup(G), "\n");
fi;
Print("--- word-problem probe: is a nontrivial word trivial on the tree ? ---\n");
a := GeneratorsOfGroup(G)[1];;
Print("  a^4 activity at level 2 = ", Activity(a^4,2), "  (trivial ? ", Activity(a^4,2)=(), ")\n");
Print("  a^4 activity at level 3 = ", Activity(a^4,3), "  (trivial ? ", Activity(a^4,3)=(), ")\n");
Print("  => finite-depth triviality does NOT imply tree-triviality (a^4 <> 1 in Z)\n");
Print("DONE\n");
QUIT;
