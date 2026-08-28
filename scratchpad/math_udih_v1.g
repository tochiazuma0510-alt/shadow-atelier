# gate: identify the dihedral degree-9 cover with an index-9 cusp (passport, genus, rigidity, Aut)
LogTo();
D9 := DihedralGroup(IsPermGroup, 18);;
Print("D9 order = ", Size(D9), "  StructureDescription = ", StructureDescription(D9), "\n");
# degree-9 action: point stabilizer = a reflection (order 2)
refl := First(Elements(D9), g -> Order(g) = 2 and not g in Centre(D9));;
H := Subgroup(D9, [refl]);;
Print("point stabilizer order = ", Size(H), "  index = ", Index(D9,H), "\n");
act := FactorCosetAction(D9, H);;
G := Image(act);;
Print("degree-9 monodromy group = ", StructureDescription(G), " order ", Size(G),
      " transitive ? ", IsTransitive(G, [1..9]), "\n");
Print("Aut(cover) = N_G(Stab)/Stab : |N| = ", Size(Normalizer(D9,H)), " => Aut order = ",
      Size(Normalizer(D9,H))/Size(H), "\n");
# cycle types available
types := Set(List(Elements(G), g -> CycleStructurePerm(g)));;
Print("cycle structures in the degree-9 action: ", types, "\n");
nine := Filtered(Elements(G), g -> Order(g)=9);;
invol := Filtered(Elements(G), g -> Order(g)=2);;
Print("#(9-cycles) = ", Length(nine), "  #(involutions) = ", Length(invol), "\n");
Print("involution cycle type = ", CycleStructurePerm(invol[1]), " (expect 2^4 * fix1)\n");
# triples with product 1 generating G
tri := 0;;
for a in nine do for b in invol do
  c := (a*b)^-1;
  if Order(c) = 2 and Size(Subgroup(G,[a,b])) = 18 then tri := tri + 1; fi;
od; od;
Print("#(sigma0 9-cycle, sigma1 invol, sigma_inf invol, product 1, generating) = ", tri, "\n");
Print("  up to conjugacy in G (|G|=18, centre trivial for odd dihedral): ", tri/18, "\n");
# Riemann-Hurwitz for passport (9 ; 2^4 1 ; 2^4 1), degree 9
d := 9;; R := (9-1) + 4*(2-1) + 4*(2-1);;
Print("RH: sum(e-1) = 8+4+4 = ", R, " ; 2g-2 = -2d + R = ", -2*d+R, " => g = ", (-2*d+R+2)/2, "\n");
# impossibility of a CYCLIC C9 cover with an index-9 point and passport (9,3,3)
Print("cyclic C9 with (ord9, ord3, ord3), product 1 : need 1+3a+3b = 0 mod 9 -> 3|1 : ",
      ForAny([0..8], a -> ForAny([0..8], b -> (1+3*a+3*b) mod 9 = 0)), " (false = impossible)\n");
Print("DONE\n");
QUIT;
