Read("scratchpad/pi_psi_table.g");;
T  := List(PIT, r -> r[1]);;
PS := List(PIT, r -> r[2]);;
G  := Group(T);;
Print("T_SIZE ", Length(T), "  <T>_ORDER ", Size(G), "  IsSimple ", IsSimple(G), "\n");
T0 := List(Filtered(PIT, r -> r[2] = 0), r -> r[1]);;
T1 := List(Filtered(PIT, r -> r[2] = 1), r -> r[1]);;
T2 := List(Filtered(PIT, r -> r[2] = 2), r -> r[1]);;
Print("FIBRE_SIZES ", [Length(T0), Length(T1), Length(T2)], "\n");
H := Group(T0);;
Print("T0_GENERATES_ORDER ", Size(H), "  T0_IS_SUBGROUP ", Size(H) = Length(T0), "\n");
if Size(H) = 9 then
  Print("H_IS_ELEM_ABELIAN ", IsElementaryAbelian(H),
        "  H_IS_SYLOW3 ", Size(H) = 9 and IsSubgroup(G,H), "\n");
  Print("T1_IS_COSET ", Length(Set(List(T1, t -> RightCoset(H,t)))) = 1,
        "  T2_IS_COSET ", Length(Set(List(T2, t -> RightCoset(H,t)))) = 1, "\n");
  Print("T1_IS_LEFTCOSET ", Length(Set(List(T1, t -> H*t))) = 1, "\n");
  N := Normalizer(G, H);;
  Print("NORMALIZER_ORDER ", Size(N), "  T_SUBSET_N ", ForAll(T, t -> t in N), "\n");
  if ForAll(T, t -> t in N) then
    q := NaturalHomomorphismByNormalSubgroup(N, H);;
    Print("N/H_ORDER ", Size(Image(q)), "  N/H_ISCYCLIC ", IsCyclic(Image(q)), "\n");
    Print("PSI_IS_N/H_INDEX ",
      Length(Set(List([1..Length(T)], i -> [Image(q,T[i]), PS[i]]))) = Size(Image(q)), "\n");
  fi;
fi;
Print("ELEMENT_ORDERS_BY_FIBRE\n");
Print("  Psi=0 : ", Collected(List(T0, Order)), "\n");
Print("  Psi=1 : ", Collected(List(T1, Order)), "\n");
Print("  Psi=2 : ", Collected(List(T2, Order)), "\n");
Print("T_IS_CLOSED_UNDER_INV ", ForAll(T, t -> t^-1 in T), "\n");
Print("PSI_ANTISYM_ON_INV ",
  ForAll([1..Length(T)], i -> not (T[i]^-1 in T) or
     PS[Position(T, T[i]^-1)] = (-PS[i]) mod 3), "\n");
QUIT;
