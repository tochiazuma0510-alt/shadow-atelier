Read("search/iso_census83_deep15_data.g");
BF3 := FreeGroup("a","b");;
brel := BF3.1*BF3.2*BF3.1*BF3.2^-1*BF3.1^-1*BF3.2^-1;;
B3 := BF3/[brel];; a := B3.1;; b := B3.2;;
targets := [154161, 154163];;
seen := [];; reps := [];;
for r1 in DEEP15 do
  if r1.id[1] = 1152 and (r1.id[2] in targets) and not (r1.id in seen) then
    Add(seen, r1.id); Add(reps, r1);
  fi;
od;;
for r1 in reps do
  Print("\n==== window ", r1.id, "\n");
  gens := List(r1.words, w -> EvalString(w));;
  N := Subgroup(B3, gens);;
  hm := NaturalHomomorphismByNormalSubgroup(B3, N);;
  iso := IsomorphismPermGroup(Image(hm));;
  s1 := Image(iso, Image(hm, a));;  s2 := Image(iso, Image(hm, b));;
  x := s1^2;; y := s2^2;; c := (s1*s2*s1)^2;; z := (x*y)^-1;;
  G := Group(x,y);;
  Print("|G|=", Size(G), " ord(x,y,z,c)=", [Order(x),Order(y),Order(z),Order(c)], "\n");
  Print("Gab=", AbelianInvariants(G), " IsNilpotent=", IsNilpotent(G), "\n");
  lcs := LowerCentralSeriesOfGroup(G);;
  Print("lcs sizes=", List(lcs, Size), "  (gamma2=gamma3 iff length 2 or repeat)\n");
  P := DerivedSubgroup(G);; FrP := FrattiniSubgroup(P);;
  Print("|P|=", Size(P), " |Phi(P)|=", Size(FrP), " d(P)=", LogInt(Size(P)/Size(FrP),2), "\n");
  W := NormalClosure(G, Subgroup(G,[x^3,y^3,z^3]));;
  Print("|W|=", Size(W), " W<=Phi(P)? ", IsSubgroup(FrP, W), "\n");
  Print("x^3 in Phi(P)? ", x^3 in FrP, "  y^3 in Phi(P)? ", y^3 in FrP, "  z^3 in Phi(P)? ", z^3 in FrP, "\n");
  # C3 = G/P acts on P/Phi(P): check fixed points of conjugation by x
  q := NaturalHomomorphismByNormalSubgroup(P, FrP);;
  V := Image(q);;
  Print("P/Phi(P) invariants=", AbelianInvariants(V), "\n");
  fix := Filtered(Elements(P), u -> Image(q, u^x) = Image(q,u));;
  imgfix := Set(List(fix, u -> Image(q,u)));;
  Print("|fixed subspace of Ad(x) on P/Phi(P)| = ", Size(imgfix), " (expect 1 = free C3-action)\n");
  # order of Ad(x) on P/Phi(P)
  ordAd := 1;; g0 := x;;
  while ForAny(Elements(P), u -> Image(q, u^g0) <> Image(q,u)) do ordAd := ordAd+1; g0 := g0*x; od;
  Print("order of Ad(x) on P/Phi(P) = ", ordAd, " (expect 3)\n");
od;
QUIT_GAP(0);
