LoadPackage("anupq");;
F2 := FreeGroup("x","y");;
Pq(F2 : Prime := 7, ClassBound := 4, Exponent := 7,
        SetupFile := "search/probe/pl_lab1_v1/pq_setup_p7c4.txt" );;
Print("SETUP_WRITTEN\n");
QUIT;
