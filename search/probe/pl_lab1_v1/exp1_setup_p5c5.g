LoadPackage("anupq");;
F2 := FreeGroup("x","y");;
Pq(F2 : Prime := 5, ClassBound := 5, Exponent := 5,
        SetupFile := "search/probe/pl_lab1_v1/pq_setup_p5c5.txt" );;
Print("SETUP_WRITTEN\n");
QUIT;
