# Audit probe (PRELIMINARY, single-lane, NON-registered): congruence windows N_p.
# usage: gap.ps1 congp.g   (edit plist below)
plist := [5,7];;
doaut := true;;

for p in plist do
Print("\n########## p = ", p, " ##########\n");
n := 2*p;;
R := ZmodnZ(n);;
o := One(R);;
s1m := [[1,1],[0,1]]*o;;
s2m := [[1,0],[-1,1]]*o;;
Em := Group(s1m,s2m);;
Print("braid ok: ", s1m*s2m*s1m = s2m*s1m*s2m, "   |E| = ", Size(Em),
      "  (6p(p^2-1) = ", 6*p*(p^2-1), ")\n");
iso := IsomorphismPermGroup(Em);;
G := Image(iso);;
S1 := Image(iso,s1m);;  S2 := Image(iso,s2m);;
Xg := S1^2;;  Yg := S2^2;;  Cc := (S1*S2*S1)^2;;
P := Subgroup(G,[Xg,Yg]);;
A := Subgroup(G,[Xg,Yg,Cc]);;
Nord := Lcm(Order(Xg),Order(Yg),Order(Cc));;
Pc := DerivedSubgroup(P);;
Print("ord(sigma1 N) = ", Order(S1), "   2*N_ord = ", 2*Nord, "   N_ord = ", Nord,
      "   c in N: ", Cc=One(G), "\n");
Print("|P_N| = ", Size(P), " (", StructureDescription(P), ")   |A| = ", Size(A),
      "   |Z(A)| = ", Size(Centre(A)), "   |[P,P]| = ", Size(Pc), "\n");
ms := Filtered([0..Nord-1], m -> Gcd(2*m+1, Nord) = 1);;
Print("c_m = ", Length(ms), " = phi(2N_ord) = ", Phi(2*Nord),
      "   candidates = ", Length(ms)*Size(Pc), "\n");

fs := AsList(Pc);;
GT := [];;
for m in ms do
  u := 2*m+1;
  for f in fs do
    if S1^u * f^-1 * S2^u * f = f^-1 * S1 * S2 * Xg^(-m) * Cc^m and
       f^-1 * S2^u * f * S1^u = S2 * S1 * Yg^(-m) * Cc^m * f then
      if Size(Subgroup(G,[Xg^u, f^-1*Yg^u*f])) = Size(P) then Add(GT,[m,f]); fi;
    fi;
  od;
od;
Print("|GT(N)| (charming+hexagon+surjective) = ", Length(GT), "\n");

settled := [];;  homs := [];;
for q in GT do
  u := 2*q[1]+1;
  h := GroupHomomorphismByImages(G, G, [S1,S2], [S1^u, q[2]^-1*S2^u*q[2]]);
  if h <> fail then Add(settled,q); Add(homs,h); fi;
od;
Print("settled = ", Length(settled), " / ", Length(GT), "   ISOLATED: ",
      Length(settled)=Length(GT), "\n");

keys := List(settled, q -> [q[1],q[2]]);;
nk := Length(keys);;
tbl := [];;  ok := true;;
for i in [1..nk] do
  row := [];
  for j in [1..nk] do
    pos := Position(keys, [ (2*keys[i][1]*keys[j][1]+keys[i][1]+keys[j][1]) mod Nord,
                            keys[i][2] * Image(homs[i], keys[j][2]) ]);
    if pos = fail then ok := false; fi;
    Add(row,pos);
  od;
  Add(tbl,row);
od;
Print("(3.53) closed on settled set: ", ok, "\n");
perms := List([1..nk], i -> PermList(tbl[i]));;
GN := Group(perms);;
Print("|G_N| = ", Size(GN), " = ", nk, "   struct = ", StructureDescription(GN), "\n");
Print("derived series = ", List(DerivedSeriesOfGroup(GN),Size),
      "   solvable = ", IsSolvableGroup(GN), "\n");
F0idx := Filtered([1..nk], i -> keys[i][1]=0);;
Print("|Im chi~| = ", Length(Set(List(keys,q->(2*q[1]+1) mod (2*Nord)))),
      " / phi(2N_ord) = ", Phi(2*Nord),
      "   |ker chi~| = ", Length(F0idx),
      "   T-A identity: ", Length(F0idx)*Phi(2*Nord) = nk, "\n");
Print("|[G_N,G_N]| = ", Size(DerivedSubgroup(GN)),
      "   kerchi = [G,G] : ", Size(DerivedSubgroup(GN)) = Length(F0idx), "\n");

# --- Theta kernel, and the proposed cheap sieves ---
ktidx := Filtered([1..nk], i -> Image(homs[i],S1)=S1 and Image(homs[i],S2)=S2);;
Print("ker Theta_N = ", Length(ktidx), "   its m-values = ", Set(List(ktidx,i->keys[i][1])), "\n");
CE := Centralizer(G,S2);;
Print("|C_E(sigma2 N)| = ", Size(CE), "   solvable = ", IsSolvableGroup(CE), "\n");
if doaut then
  AutA := AutomorphismGroup(A);;
  Print("|Aut(A)| = ", Size(AutA), "   solvable = ", IsSolvableGroup(AutA), "\n");
  ccY := AsList(ConjugacyClass(A,Yg));;
  Ulist := Filtered(AsList(AutA), a -> Image(a,Xg)=Xg and Image(a,Cc)=Cc and Image(a,Yg) in ccY);;
  U := Subgroup(AutA, Ulist);;
  Print("|U| (Stab(x,c) & y-class) = ", Size(U), "   solvable = ", IsSolvableGroup(U), "\n");
  hgens := [];;
  for m in ms do
    u := 2*m+1;
    for f in fs do
      a := GroupHomomorphismByImages(A,A,[Xg,Yg,Cc],[Xg^u, f^-1*Yg^u*f, Cc^u]);
      if a <> fail then if IsBijective(a) then Add(hgens,a); fi; fi;
    od;
  od;
  HN := Subgroup(AutA, hgens);;
  Print("|H_N| (Sol A2) = ", Size(HN), "   solvable = ", IsSolvableGroup(HN),
        "   #power-form autos = ", Length(hgens), "\n");
fi;
od;
QUIT;
