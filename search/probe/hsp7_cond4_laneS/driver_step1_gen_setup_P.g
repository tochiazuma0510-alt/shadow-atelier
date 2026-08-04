Print("Lane S step1: independent construction, own naming (not reading stage3 code)\n");
LoadPackage("anupq");
F := FreeGroup("x","y");
Pq(F : Prime := 7, ClassBound := 4, Exponent := 7,
   SetupFile := "search/probe/hsp7_cond4_laneS/pqsetup_P.txt");
Print("setup file written\n");
QUIT;
