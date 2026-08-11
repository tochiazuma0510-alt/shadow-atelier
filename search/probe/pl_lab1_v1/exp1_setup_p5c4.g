## exp1_setup_p5c4.g -- generate ANUPQ setup file for P_{4,5} = F2/(gamma_5(F2)F2^5)
## (control case, Lazard domain, smallest test of the whole pipeline)
LoadPackage("anupq");;
F2 := FreeGroup("x","y");;
Pq(F2 : Prime := 5, ClassBound := 4, Exponent := 5,
        SetupFile := "search/probe/pl_lab1_v1/pq_setup_p5c4.txt" );;
Print("SETUP_WRITTEN\n");
QUIT;
