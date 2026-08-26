# math_gdyn_tpin_v3.g -- universality of r = x y x^-1, dessin/cycle data, psi construction attempt
LogTo();
A := AlternatingGroup(4);;
els := Elements(A);;
pairs := Filtered(Cartesian(els,els), p -> Order(p[1])=3 and Order(p[2])=3 and Order(p[1]*p[2])=2);;
Print("pairs = ", Length(pairs), "\n");
# universality: is  a*b*a^-1  always a valid representative, i.e. conjugates <b> onto <a> ?
bad := 0;; good := 0;;
for p in pairs do
  a := p[1];; b := p[2];; r := a*b*a^-1;;
  if r*b*r^-1 in Subgroup(A,[a]) then good := good+1; else bad := bad+1; fi;
od;
Print("UNIV r=aba^-1 valid : ", good, " / ", Length(pairs), "  (invalid ", bad, ")\n");
# and the two rejected candidates
bx := 0;; by := 0;;
for p in pairs do
  a := p[1];; b := p[2];;
  if a*b*a^-1 in Subgroup(A,[a]) then bx := bx+1; fi;      # r = x
  if b*b*b^-1 in Subgroup(A,[a]) then by := by+1; fi;      # r = y
od;
Print("UNIV r=x valid count : ", bx, " / ", Length(pairs), "\n");
Print("UNIV r=y valid count : ", by, " / ", Length(pairs), "\n");

a := pairs[1][1];; b := pairs[1][2];; z := (a*b)^-1;;
Print("model a=",a," b=",b," z=",z,"\n");
# dessin / Schreier data: right multiplication action on the 12 sheets
sheets := els;;
pos := function(u) return Position(sheets,u); end;;
ra := PermList(List(sheets, u -> pos(u*a)));;
rb := PermList(List(sheets, u -> pos(u*b)));;
rz := PermList(List(sheets, u -> pos(u*z)));;
Print("rho_a cycles = ", CycleStructurePerm(ra), " orbits ", Length(Orbits(Group(ra),[1..12])), "\n");
Print("rho_b cycles = ", CycleStructurePerm(rb), " orbits ", Length(Orbits(Group(rb),[1..12])), "\n");
Print("rho_z cycles = ", CycleStructurePerm(rz), " orbits ", Length(Orbits(Group(rz),[1..12])), "\n");
Print("ra*rb*rz = id ? ", ra*rb*rz = (), "\n");
Print("Euler check V-E+F = ", 4-12+6+4, " (black4+white4 - edges12 + faces6 = 2 expected: ",
      4+4-12+6, ")\n");
# the infinity point: the <b>-orbit whose stabilizer is <a>
r0 := a*b*a^-1;;
orb_inf := Set(Orbit(Group(rb), pos(r0)));;
orb_one := Set(Orbit(Group(rb), pos(One(A))));;
Print("orbit of sheet 1 under rho_b (point t=1)   : ", orb_one, "\n");
Print("orbit of sheet r0 under rho_b (point t=inf): ", orb_inf, "\n");
Print("disjoint ? ", Intersection(orb_one,orb_inf) = [], "\n");
Print("DONE-PART1\n");
QUIT;
