## exact enumeration of the n=15 realizations (structconst says 72 / 120)
WacCT := function(p, n)
  return SortedList(List(Orbits(Group(p), [1..n]), Length));
end;;
S15 := SymmetricGroup(15);;
Exact := function(uu, target, label)
  local C, sols, orbs, a1, i, o, reps, G, dat;
  Print("\n=== ", label, " : u=", uu, " type ", WacCT(uu,15), " ===\n");
  C := Centralizer(S15, uu);
  Print("|C_S15(u)| = ", Size(C), "   expected #solutions = ", target, "\n");
  sols := []; reps := [];
  i := 0;
  while Length(sols) < target and i < 3000000 do
    i := i + 1;
    a1 := ((1,2)*(3,4)*(5,6)*(7,8)*(9,10)*(11,12)*(13,14)) ^ Random(S15);
    if WacCT(a1*uu^-1,15) = [3,3,3,3,3] and not a1 in sols then
      o := Orbit(C, a1, OnPoints);
      Print("  new C(u)-orbit of size ", Length(o), "\n");
      Append(sols, Filtered(o, z -> not z in sols));
      Add(reps, a1);
    fi;
  od;
  Print("  total solutions enumerated: ", Length(sols),
        "  (complete? ", Length(sols) = target, ")  [tries=", i, "]\n");
  dat := [];
  for a1 in reps do
    G := Group(a1, a1*uu^-1);
    Add(dat, [Size(G), SortedList(List(Orbits(G,[1..15]),Length)),
              IsTransitive(G,[1..15])]);
  od;
  Print("  orbit-representative groups (order, orbits, transitive): ", dat, "\n");
  Print("  => any of them equal to S15 ? ",
        ForAny(reps, a1 -> Group(a1, a1*uu^-1) = S15), "\n");
end;;
Exact((1,2,3,4,5,6,7,8,9)*(10,11)*(12,13)*(14,15), 72,  "lam=(9,2,2,2)");
Exact((1,2,3,4,5,6,7,8,9,10)*(11,12)*(13,14),      120, "lam=(10,2,2,1)");
Print("\nA15C_DONE\n");
QUIT;
