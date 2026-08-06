Read("search/probe/wac_v1/gap_output_prelude.g");
# Ribet-window feasibility, next-step probe (裁定703 / 裁定710).
# Object under test (full): G_p = H ⋊ S3, H = extraspecial(p^3, exponent p) Heisenberg group,
#   S3 acting on H/Z(H) = F_p^2 via the faithful standard 2-dim representation (det=-1 on
#   transpositions, det=+1 on 3-cycles), extended to Z(H) via det (Lambda^2 action).
# p = 691.
#
# Ruling 710 (2026-08-06): full G_p SplitExtension construction abandoned (timed out
# repeatedly on this machine, both via a permutation-group S3 source and a pc-pc
# SmallGroup(6,1) source -- see scratchpad/rw_g2/probe9..13 logs). (i) Z(G_p)=1 and
# (ii) G_p^ab=C_2 are NOT machine-reconfirmed here; they are paper-side results
# (theorem LADDER-WIN, candidate, ruling 710) proved uniformly for p>=5.
# This script machine-confirms only (iii): (2,3)-generation, via the Frattini
# reduction R0(p) := F_p^2 ⋊ S3 = G_p / Z(H) (order 6p^2), using the reduction lemma
# Phi(G_p) = Z(H) (paper-side, candidate) -- if X generates R0(p) then X generates G_p.
#
# The (2,3)-generation search itself uses the structural shortcut (irreducibility of
# F_p^2 as F_p[S3]-module under this action, p=691 does not divide |S3|=6): any
# subgroup K <= R0(p) with K -> S3 onto has K intersect F_p^2 in {0, F_p^2}. So a
# handful of random order-(2,3) witness pairs, checked via Size(<x,y>) = |R0(p)|, is
# a fully rigorous (not heuristic) generation certificate once a hit is found.

Reset(GlobalMersenneTwister, 20260806);;
p := 691;;
F := GF(p);;
one := One(F);; zero := Zero(F);;

# r = transposition image (order 2, det -1), s = 3-cycle image (order 3, det +1)
Amat := [[zero, -one],[one,-one]] * one;;   # "s"
Bmat := [[zero,one],[one,zero]] * one;;      # "r"

Print("=== action identification (ruling 710 cert requirement) ===\n");
Print("r (2x2, mod ", p, ") = ", List(Bmat, row -> List(row, IntFFE)), "\n");
Print("s (2x2, mod ", p, ") = ", List(Amat, row -> List(row, IntFFE)), "\n");
Print("det(r) = ", IntFFE(DeterminantMat(Bmat)), " (expect ", p-1, " = -1 mod p)\n");
Print("det(s) = ", IntFFE(DeterminantMat(Amat)), " (expect 1)\n");
Print("order(r) = ", Order(Bmat), " order(s) = ", Order(Amat), "\n");
S3mat := Group(Amat,Bmat);;
Print("faithfulness: Size(<r,s> in GL2(F_p)) = ", Size(S3mat), " (expect 6)\n");

# R0(p) = F_p^2 rtimes S3, realized as 3x3 affine matrices over F_p (subgroup of AGL(2,p))
AA := [[Amat[1][1],Amat[1][2],zero],[Amat[2][1],Amat[2][2],zero],[zero,zero,one]];;
BB := [[Bmat[1][1],Bmat[1][2],zero],[Bmat[2][1],Bmat[2][2],zero],[zero,zero,one]];;
T1 := [[one,zero,one],[zero,one,zero],[zero,zero,one]];;
T2 := [[one,zero,zero],[zero,one,one],[zero,zero,one]];;
R0 := Group(AA,BB,T1,T2);;
sizeG := Size(R0);;
Print("\n=== R0(p) = F_p^2 : S3 ===\n");
Print("Size(R0) = ", sizeG, "  expected 6*p^2 = ", 6*p^2, "  match = ", sizeG = 6*p^2, "\n");

BuildElt := function(lin, v)
    return [[lin[1][1],lin[1][2],v[1]],[lin[2][1],lin[2][2],v[2]],[zero,zero,one]];
end;;
id3 := IdentityMat(3,F);;

Print("\n=== (iii) (2,3)-generation search (cap 20 random witness pairs) ===\n");
found := false;;
witnessVx := fail;; witnessVy := fail;;
attempts := 0;;
for trial in [1..20] do
    attempts := attempts + 1;
    repeat
        vx := [Random(F), Random(F)];
        x := BuildElt(Bmat, vx);
    until x^2 = id3;
    repeat
        vy := [Random(F), Random(F)];
        y := BuildElt(Amat, vy);
    until y^3 = id3;
    sz := Size(Group(x,y));
    Print("trial ", trial, ": vx_int=", List(vx,IntFFE), " vy_int=", List(vy,IntFFE),
          " Size(<x,y>)=", sz, " match=", sz = sizeG, "\n");
    if sz = sizeG then
        found := true;
        witnessVx := List(vx,IntFFE); witnessVy := List(vy,IntFFE);
        break;
    fi;
od;
Print("\nFOUND = ", found, "  attempts_used = ", attempts, "\n");
if found then
    Print("WITNESS vx_int=", witnessVx, " vy_int=", witnessVy, "\n");
fi;

Print("\n(i) Z(G_p)=1 and (ii) G_p^ab=C_2: WAIVED for machine reconfirmation here per\n");
Print("ruling 710 -- paper-side theorem LADDER-WIN (candidate), not GAP-recomputed.\n");
