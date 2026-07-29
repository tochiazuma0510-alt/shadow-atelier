#############################################################################
## search/probe/wac_v1/tail8.g -- tail law verification (W6-1)
##  T-1: derived lengths of Syl_2(S_t), t = 4..9  (does dl jump at t=8?)
##  T-2: Ree feasibility of the tail-t family xbar = (ell, 1^t), t = 5..8
##  T-3: exact class structure constant for the minimal tail-8 window
## Single lane. NOT a ledger claim. No commit. No u (sealed symbol).
#############################################################################

Print("===== T-1: Syl_2(S_t) and its derived length =====\n");
for t in [4..10] do
  S := SymmetricGroup(t);
  Q := SylowSubgroup(S, 2);
  Print("  t=", t, "  |Syl_2(S_t)|=", Size(Q),
        "  dl=", DerivedLength(Q),
        "  struct=", StructureDescription(Q), "\n");
od;
Print("  (A_t leg, for C_P(ybar) = C_ell x A_t):\n");
for t in [4..10] do
  A := AlternatingGroup(t);
  Q := SylowSubgroup(A, 2);
  Print("  t=", t, "  |Syl_2(A_t)|=", Size(Q), "  dl=", DerivedLength(Q),
        "  struct=", StructureDescription(Q), "\n");
od;

Print("\n===== T-2: Ree feasibility of the tail-t family =====\n");
Print("  xbar=(ell,1^t), n=ell+t, u = ell-cycle + (m transpositions, f fixed)\n");
Print("  c(u)=1+t-m, sign(u)=(-1)^m => k = m mod 2, ord(u)=2*ell (m>=1) or ell\n\n");
for t in [5..8] do
  Print("  --- tail t=", t, " ---\n");
  found := false;
  for ell in [3,5..41] do
    n := ell + t;
    for m in Reversed([0..QuoInt(t,2)]) do
      cu := 1 + t - m;
      if m >= 1 then ordu := 2*ell; else ordu := ell; fi;
      if ordu < 7 then continue; fi;
      # best k of the required parity, best j
      kmax := QuoInt(n,2);
      if (kmax - m) mod 2 <> 0 then kmax := kmax - 1; fi;
      jmax := QuoInt(n,3);
      if kmax >= 1 and kmax + 2*jmax + 2 - n >= cu then
        Print("    ell=", ell, " n=", n, " m=", m, " c(u)=", cu,
              " Ree bound=", kmax + 2*jmax + 2 - n,
              "  k=", kmax, " j=", jmax, " ord(u)=", ordu,
              "  N_ord=", ell,
              "  |C_An(x)|=", ell*Factorial(t)/2,
              " |Stab|=", ell*Factorial(t),
              "  Xi=", Phi(2*ell)*(ell*Factorial(t)/2)*(ell*Factorial(t)), "\n");
        found := true;
        break;
      fi;
    od;
    if found then break; fi;
  od;
  if not found then Print("    NO ell <= 41 is Ree-compatible\n"); fi;
od;

Print("\n===== T-3: structure constant for the minimal tail-8 window =====\n");
n := 21;;
lamu := [13,2,2,2,2];;   # u
ka := 10;; jb := 7;;     # a' = 2^10 1^1 , b' = 3^7
Print("  n=", n, " lam(u)=", lamu, " a'=2^", ka, "1^", n-2*ka,
      " b'=3^", jb, "1^", n-3*jb, "\n");
Print("  computing CharacterTable(\"Symmetric\",21) ... ");
tbl := CharacterTable("Symmetric", n);;
parts := ClassParameters(tbl);;
Print("done (", Length(parts), " classes)\n");
pidx := function(p)
  return First([1..Length(parts)], i -> SortedList(parts[i][2]) = SortedList(p));
end;;
la := Concatenation(List([1..ka],z->2), List([1..n-2*ka],z->1));;
lb := Concatenation(List([1..jb],z->3), List([1..n-3*jb],z->1));;
cc := ClassMultiplicationCoefficient(tbl, pidx(la), pidx(lb), pidx(lamu));;
Print("  structconst( 2^10 1 , 3^7 , (13,2,2,2,2) ) = ", cc, "\n");
Print("  => class-level realizable ? ", cc > 0, "\n");

Print("\nTAIL8_DONE\n");
QUIT;
