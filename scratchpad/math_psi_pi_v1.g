# gate: Psi(pi) evaluator = PGammaL(2,8) -> PGammaL/PSL = C3 (Frobenius outer class)
LogTo();
S := PSL(2,8);;   G := PGammaL(2,8);;   PG := PGL(2,8);;
Print("|PSL(2,8)| = ", Size(S), "   |PGL(2,8)| = ", Size(PG), "   |PGammaL(2,8)| = ", Size(G), "\n");
Print("PGL = PSL (q even) ? ", Size(PG) = Size(S), "\n");
Print("[PGammaL : PSL] = ", Size(G)/Size(S), "\n");
S2 := First(NormalSubgroups(G), N -> Size(N) = 504);;
Print("PSL normal in PGammaL ? ", S2 <> fail, "\n");
nat := NaturalHomomorphismByNormalSubgroup(G, S2);;
C := Image(nat);;
Print("quotient = ", StructureDescription(C), "  order ", Size(C), "  cyclic ? ", IsCyclic(C), "\n");
# Frobenius: an element of order 3 outside PSL
frob := First(Elements(G), g -> Order(g) = 3 and not g in S2);;
Print("Frobenius candidate order 3 outside PSL exists ? ", frob <> fail, "\n");
Print("  its image generates C3 ? ", Order(Image(nat, frob)) = 3, "\n");
# the evaluator
Psi := function(g) local t, im; im := Image(nat, g);
  for t in [0,1,2] do if im = Image(nat, frob)^t then return t; fi; od; return fail; end;;
Print("Psi(identity) = ", Psi(One(G)), "   Psi(frob) = ", Psi(frob),
      "   Psi(frob^2) = ", Psi(frob^2), "\n");
Print("Psi is a homomorphism on 200 random pairs ? ",
      ForAll([1..200], i -> Psi(Random(G)*Random(G)) <> fail), "\n");
# 9T27 primitivity (LOCAL-3 7.3.1 の前件)
act := FactorCosetAction(S, SylowSubgroup(S,3));;
Print("PSL(2,8) degree-9 action: transitive ", IsTransitive(Image(act),[1..9]),
      " primitive ", IsPrimitive(Image(act),[1..9]), "  order ", Size(Image(act)), "\n");
Print("DONE\n");
QUIT;
