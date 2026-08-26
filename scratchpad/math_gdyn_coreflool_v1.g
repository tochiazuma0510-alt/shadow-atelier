# math_gdyn_coreflool_v1.g -- CORE-FLOOR: exact [F2 : C(N_c)] for abelian N_c, and bound checks.
# C(N_c) := { h in H_T : h|_u in N_c for all u }  = Core_{F2}( psi_T^{-1}(N_c) )
# For N_c with Q := F2/N_c elementary abelian p-group, Sigma : H_T -> Q^12 factors through
# H_T^ab (x) Fp = Fp^13, so [H_T : C] = p^rank, rank = rank of the 12*dim(Q) conjugate functionals.
LogTo();
A := AlternatingGroup(4);;
a := (2,3,4);; b := (1,2,3);; z := (a*b)^-1;;
els := Elements(A);;
Ca := Subgroup(A,[a]);; Cb := Subgroup(A,[b]);; Cz := Subgroup(A,[z]);;
lcos := function(H) return Set(List(els, u -> Set(List(Elements(H), h -> u*h)))); end;;
cA := lcos(Ca);; cB := lcos(Cb);; cZ := lcos(Cz);;
Print("left cosets 4/4/6 : ", [Length(cA),Length(cB),Length(cZ)], "\n");
# coordinate index of an inertia point
idx := function(c)
  local i;
  i := Position(cA,c); if i <> fail then return i; fi;
  i := Position(cB,c); if i <> fail then return 4+i; fi;
  i := Position(cZ,c); if i <> fail then return 8+i; fi;
  return fail; end;;
# the three special points:  0-point = <a> ; 1-point = <b> ; inf-point = r0<b>, r0 = a*b*a^-1
r0 := a*b*a^-1;;
p0 := Set(List(Elements(Ca), h -> One(A)*h));;
p1 := Set(List(Elements(Cb), h -> One(A)*h));;
pI := Set(List(Elements(Cb), h -> r0*h));;
i0 := idx(p0);; i1 := idx(p1);; iI := idx(pI);;
Print("special coords (0,1,inf) = ", [i0,i1,iI], " distinct ? ", Length(Set([i0,i1,iI]))=3, "\n");
# deck action of u on coordinates: coset c |-> u*c
act := function(u)
  local perm, i, c;
  perm := [];
  for c in cA do Add(perm, idx(Set(List(c, w -> u*w)))); od;
  for c in cB do Add(perm, idx(Set(List(c, w -> u*w)))); od;
  for c in cZ do Add(perm, idx(Set(List(c, w -> u*w)))); od;
  return perm; end;;
Print("deck action is a permutation of [1..14] for all u ? ",
      ForAll(els, u -> Set(act(u)) = [1..14]), "\n");
Print("blocks preserved (vertices/faces/edges) ? ",
      ForAll(els, u -> Set(act(u){[1..4]})=[1..4] and Set(act(u){[5..8]})=[5..8]
                       and Set(act(u){[9..14]})=[9..14]), "\n");

conjvec := function(v, u)   # (mu o c_{r_u})(gamma_c) = mu(gamma_{u c})
  local pm; pm := act(u);
  return List([1..14], i -> v[pm[i]]); end;;

rank_of := function(base)   # base = list of base functionals (integer vectors of length 14)
  local rows, v, u;
  rows := [];
  for v in base do for u in els do Add(rows, conjvec(v,u)*One(GF(3))); od; od;
  return RankMat(rows); end;;

# ---- case 1 : N_c = the S3-stable index-3 window  (mu(x)=mu(y)=mu(z)=1 in F3) ----
mu := List([1..14], i -> 0);; mu[i0] := 1; mu[i1] := 1; mu[iI] := 1;;
Print("\n[case 1] N_c = S3-stable index-3 window (Q = F3)\n");
Print("  mu (14 coords) = ", mu, "  sum mod 3 = ", Sum(mu) mod 3, "\n");
r := rank_of([mu]);;
Print("  rank_F3 of the 12 conjugates = ", r, " of 13\n");
Print("  [H_T : C(N_c)] = 3^", r, " = ", 3^r, "\n");
Print("  [F2  : C(N_c)] = 12 * 3^", r, " = ", 12*3^r, "\n");

# ---- case 2 : N_c = V_3 = F2^3[F2,F2]  (Q = F3^2) ----
l1 := List([1..14], i -> 0);; l1[i0] := 1; l1[iI] := 2;;
l2 := List([1..14], i -> 0);; l2[i1] := 1; l2[iI] := 2;;
Print("\n[case 2] N_c = V_3 = F2^3[F2,F2] (Q = F3^2, index 9)\n");
Print("  lambda1 = ", l1, "\n  lambda2 = ", l2, "\n");
r2 := rank_of([l1,l2]);;
Print("  rank_F3 of the 24 conjugates = ", r2, " of 13\n");
Print("  [H_T : C(V_3)] = 3^", r2, " = ", 3^r2, "\n");
Print("  [F2  : C(V_3)] = 12 * 3^", r2, " = ", 12*3^r2, "\n");

# ---- consistency with the A4-abelianization rank 7 from spec v1.1 sec 8.2 ----
nu := List([1..14], i -> 0);; nu[i0] := 1; nu[i1] := -1 mod 3;;
Print("\n[cross-check] A4-abelianization character nu (nu(z)=0):\n  nu = ", nu, "\n");
Print("  rank of its 12 conjugates = ", rank_of([nu]), " (spec v1.1 sec 8.2 measured 7)\n");

# ---- bound arithmetic ----
Print("\n[bounds] d = 12, N_c index 12 :\n");
Print("  d * (index)^d = 12*12^12 = ", 12*12^12, "\n");
Print("  implementer measured Core_{F2}(K) index ~ 5.28e12 ; below bound ? ",
      5.28*10^12 < Float(12*12^12), "\n");
Print("  12^12 = ", 12^12, " ; 1728^3 = ", 1728^3, " ; 1728^4 = ", 1728^4, "\n");
Print("DONE\n");
QUIT;
