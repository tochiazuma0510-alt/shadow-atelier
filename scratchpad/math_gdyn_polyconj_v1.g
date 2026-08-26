# gate: is T (resp. O) conjugate to a polynomial ?  Criterion: exists a totally ramified point (e = deg).
# For a GALOIS cover with deck group G: every fibre over a branch point has  #pts * e = deg  with e = |cyclic
# local monodromy|.  A totally ramified point needs a fibre of size 1, i.e. a cyclic subgroup of index 1,
# i.e. G itself cyclic.  A4 and S4 are not cyclic => no totally ramified point => not polynomial-conjugate.
LogTo();
for rec_ in [ rec(name:="T", G:=AlternatingGroup(4), d:=12, fib:=[[4,3],[4,3],[6,2]]),
              rec(name:="O", G:=SymmetricGroup(4),   d:=24, fib:=[[6,4],[12,2],[8,3]]) ] do
  G := rec_.G;; d := rec_.d;;
  Print("--- ", rec_.name, " : deg = ", d, ", deck group = ", StructureDescription(G),
        ", |G| = ", Size(G), " ---\n");
  Print("  |G| = deg ? ", Size(G) = d, "   G cyclic ? ", IsCyclic(G), "\n");
  Print("  fibres (#pts,e) = ", rec_.fib, "  each #pts*e = deg ? ",
        ForAll(rec_.fib, p -> p[1]*p[2] = d), "\n");
  Print("  max ramification index e_max = ", Maximum(List(rec_.fib, p -> p[2])),
        "  ; totally ramified needs e = ", d, "\n");
  Print("  exists fibre of size 1 ? ", ForAny(rec_.fib, p -> p[1] = 1), "\n");
  Print("  => totally ramified point exists ? ", ForAny(rec_.fib, p -> p[2] = d), "\n");
  Print("  => conjugate to a polynomial ? ", ForAny(rec_.fib, p -> p[2] = d),
        "   (criterion: needs a totally ramified FIXED point)\n");
  Print("  cyclic-subgroup-of-index-1 argument: G cyclic ? ", IsCyclic(G),
        " => no totally ramified point for a Galois cover with non-cyclic deck group\n");
  # orders of cyclic subgroups = possible ramification indices
  Print("  possible e (orders of elements of G) = ", Set(List(Elements(G), Order)), "\n");
od;
Print("CONCLUSION: neither T nor O is Moebius-conjugate to a polynomial.\n");
Print("=> BKN amenability route (polynomial-restricted) was never applicable to T. \n");
Print("DONE\n");
QUIT;
