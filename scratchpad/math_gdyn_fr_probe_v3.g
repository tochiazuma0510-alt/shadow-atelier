# math_gdyn_fr_probe_v3.g -- FR group-machine form (stateset = free GROUP), contraction test
LogTo();
LoadPackage("fr");;
F := FreeGroup("a");;
M := FRMachine(F, [[One(F), F.1]], [(1,2)]);;      # a = <1,a> sigma  (adding machine)
Print("machine : ", M, "\n");
Print("StateSet = ", StateSet(M), "\n");
a := FRElement(M, F.1);;
Print("Activity(a,3) = ", Activity(a,3), "\n");
Print("IsContracting(M) = ", IsContracting(M), "\n");
Print("NucleusOfFRMachine(M) = ", NucleusOfFRMachine(M), "\n");
G := Group(a);;
Print("IsContracting(G) = ", IsContracting(G), "\n");
Print("IsOne(a^4) = ", IsOne(a^4), "  (a^4 <> 1 in Z ; FR decides via nucleus)\n");
Print("--- a 2-generator, 12-letter template (shape only; states are placeholders) ---\n");
F2 := FreeGroup("x","y");;
tx := List([1..12], i -> One(F2));;  tx[1] := F2.1;;
ty := List([1..12], i -> One(F2));;  ty[1] := F2.2;;
px := (1,2,3)(4,5,6)(7,8,9)(10,11,12);;
py := (1,4,7)(2,5,10)(3,8,11)(6,9,12);;
MT := FRMachine(F2, [tx,ty], [px,py]);;
Print("12-letter 2-generator machine built ? ", MT <> fail, "\n");
Print("  |<Activity(x,2),Activity(y,2)>| = ",
      Size(Group(Activity(FRElement(MT,F2.1),2), Activity(FRElement(MT,F2.2),2))), "\n");
Print("  IsContracting(MT) = ", IsContracting(MT), "   <- placeholder states, not psi_T\n");
Print("DONE\n");
QUIT;
