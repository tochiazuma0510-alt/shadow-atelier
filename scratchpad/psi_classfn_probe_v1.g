## Is Psi a CLASS FUNCTION on PSL(2,8) (resp. PGammaL(2,8)) restricted to T?
## If not, Frobenius-up-to-conjugacy (= Dedekind factorisation type) cannot determine Psi.
Read("scratchpad/pi_psi_table.g");;
T  := List(PIT, r -> r[1]);;
PS := List(PIT, r -> r[2]);;
G  := Group(T);;                       # = PSL(2,8), order 504
N  := Normalizer(SymmetricGroup(9), G);;
Print("G_ORDER ", Size(G), "   N_ORDER ", Size(N), "\n");

viol := 0;; pairs := 0;; ex := [];;
for i in [1..27] do for j in [i+1..27] do
  if IsConjugate(G, T[i], T[j]) then
    pairs := pairs + 1;;
    if PS[i] <> PS[j] then viol := viol + 1;;
      if Length(ex) < 4 then Add(ex, [Order(T[i]), PS[i], PS[j]]); fi;
    fi;
  fi;
od; od;
Print("PSL_CONJ_PAIRS ", pairs, "  PSI_VIOLATIONS ", viol,
      "  PSI_IS_PSL_CLASS_FUNCTION ", viol = 0, "\n");
Print("  examples [order, Psi_i, Psi_j] = ", ex, "\n");

viol2 := 0;; pairs2 := 0;;
for i in [1..27] do for j in [i+1..27] do
  if IsConjugate(N, T[i], T[j]) then
    pairs2 := pairs2 + 1;;
    if PS[i] <> PS[j] then viol2 := viol2 + 1;; fi;
  fi;
od; od;
Print("PGammaL_CONJ_PAIRS ", pairs2, "  PSI_VIOLATIONS ", viol2,
      "  PSI_IS_PGammaL_CLASS_FUNCTION ", viol2 = 0, "\n");

## cycle-type (= Dedekind data) resolution
ct := function(p) return Collected(List(Orbits(Group(p),[1..9]), Length)); end;;
d := NewDictionary(ct(()), true);;
Print("CYCLETYPE_TO_PSI\n");
for t in Set(List(T, ct)) do
  Print("  ", t, " -> Psi values ",
    Set(List(Filtered([1..27], i -> ct(T[i]) = t), i -> PS[i])), "\n");
od;
## order-3 elements: single PSL class 3A -- decisive
o3 := Filtered([1..27], i -> Order(T[i]) = 3);;
Print("ORDER3_IN_T ", Length(o3), "  all_PSL_conjugate ",
  ForAll(o3, i -> IsConjugate(G, T[o3[1]], T[i])),
  "  their_Psi ", List(o3, i -> PS[i]), "\n");
QUIT;
