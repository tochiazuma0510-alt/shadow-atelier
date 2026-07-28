## n <= 6 leg of Lemma 3.1: max |C_{A_n}(x)| and max |Stab_{Aut(A_n)}(x)| over x <> 1
for n in [4,5,6] do
  An := AlternatingGroup(n);;
  A := AutomorphismGroup(An);;
  mc := 0;; ms := 0;; worstc := ();; worsts := ();;
  for cl in ConjugacyClasses(An) do
    x := Representative(cl);
    if x = One(An) then continue; fi;
    c := Size(Centralizer(An, x));
    if c > mc then mc := c; worstc := x; fi;
  od;
  for x in An do
    if x = One(An) then continue; fi;
    s := Size(Stabilizer(A, x, function(g,al) return Image(al,g); end));
    if s > ms then ms := s; worsts := x; fi;
  od;
  Print("n=", n, "  |A_n|=", Size(An), "  |Aut|=", Size(A),
        "   max |C_{A_n}(x)| = ", mc, " at ", worstc,
        "   max |Stab_Aut(x)| = ", ms, " at ", worsts,
        "   both < 60 ? ", mc < 60 and ms < 60, "\n");
od;
Print("SMALL_N_DONE\n");
QUIT;
