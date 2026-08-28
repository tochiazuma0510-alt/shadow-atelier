## GATE 1b: ambiguity group of the simultaneous-conjugacy identification, and
## how many [9],[9],[9] genus-4 9T27 classes exist (= how many LMFDB rows we
## would have to disambiguate).
Read("search/drophunt_checker_producer_v2.g");;
PPX := DCP2X4;; PPY := DCP2Y4;;
G := Group(PPX,PPY);; S9 := SymmetricGroup(9);;
Print("QQ_CENTRALISER_IN_S9 ", Size(Centralizer(S9, G)),
      "   (=1 means the simultaneous conjugator is UNIQUE)\n");
Print("QQ_NORMALISER_IN_S9 ", Size(Normalizer(S9, G)), "  index_over_G ",
      Size(Normalizer(S9,G))/Size(G), "\n");
## all ordered pairs (a,b) in G with a,b,(ab)^-1 all 9-cycles, up to simultaneous
## conjugacy by N_{S9}(G) (the full ambiguity available to a database match)
nine := Filtered(Elements(G), g -> Order(g)=9);;
Print("QQ_ORDER9_ELEMENTS ", Length(nine), "\n");
prs := [];;
for a in nine do for b in nine do
  if Order(a*b)=9 then Add(prs,[a,b]); fi;
od; od;
Print("QQ_TRIPLES_ALL999 ", Length(prs), "\n");
N := Normalizer(S9,G);;
reps := [];;
for p in prs do
  if ForAll(reps, r -> RepresentativeAction(N, r, p, OnPairs) = fail) then
    Add(reps, p);
  fi;
od;
Print("QQ_CLASSES_UP_TO_NS9 ", Length(reps), "\n");
reps2 := [];;
for p in prs do
  if ForAll(reps2, r -> RepresentativeAction(G, r, p, OnPairs) = fail) then
    Add(reps2, p);
  fi;
od;
Print("QQ_CLASSES_UP_TO_G ", Length(reps2), "\n");
## genus-0 impossibility when both marked generators are 9-cycles
Print("QQ_GENUS_FORMULA 2g-2 = 7 - c_inf ;  c_inf=1 -> g=4 ; g=0 needs c_inf=9 = identity (impossible for a transitive triple)\n");
QUIT;
