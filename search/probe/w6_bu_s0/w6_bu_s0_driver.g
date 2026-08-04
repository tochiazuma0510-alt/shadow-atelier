#############################################################################
## search/probe/w6_bu_s0/w6_bu_s0_driver.g
## W6BU-S0: BOTTOM-UP census S0 calibration (asserts A-0..A-13).
## Design authority: docs/notes/w6_bottomup_design_v2.md SS7.2 (promoted to
## normative census spec, 裁定494), superseding v1's A-0..A-8 list for this
## scope. Authorization: sol/sol_reply_102_math29.md F102-6.3 (limited
## authorization: S0 calibration + H^2(S4,V) inventory/census ONLY -- no
## kill, no EMPTY-THM, no candidate use). A-6/A-7(v1, kill-stage calibration)
## are explicitly OUT of this order per v2 SS7.2 note.
##
## Non-contact: Im R_{N,K^(5)} untouched, d_N unevaluated, 3 sealed
## quantities untouched, no certificate reading. inference-contact event
## (裁定412) does not fire anywhere in this script.
##
## Two independent construction routes are cross-checked against each other
## where the design calls for it (A-1/A-2: PB3-permutation route MakeGn(5)
## vs. algebraic A(x)S4 semidirect-product route) -- this is a cross-check
## between two GAP-internal constructions, NOT a search/crosscheck
## separation (both live in the search/ tree; this script is exploratory
## tooling, not a settled-claim two-lane pipeline).
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
LoadPackage("cohomolo");;

FAILS := [];;
Chk := function(name, got, want)
  local ok;
  ok := (got = want);
  if not ok then Add(FAILS, rec(name := name, got := String(got), want := String(want))); fi;
  Print("  [", PF(ok), "] ", name, ": got=", got, " want=", want, "\n");
  return ok;
end;;

RESULTS := rec();;

#############################################################################
## A-0: order(theta*tau) in S4, theta=(1,2), tau=(1,3,4)
#############################################################################
Print("\n=== A-0 ===\n");
S4grp := Group((1,2),(1,3,4));;
theta := (1,2);; tau := (1,3,4);;
ordThetaTau := Order(theta*tau);;
Chk("A-0: order(theta*tau) in S4", ordThetaTau, 4);;
RESULTS.A0_order_theta_tau := ordThetaTau;;

## S4 presentation <a,b|a^2,b^3,(ab)^4> used throughout for CHR calls.
FS4 := FreeGroup(2);;
FqS4 := FS4 / [FS4.1^2, FS4.2^3, (FS4.1*FS4.2)^4];;
Chk("A-0b: |<a,b|a^2,b^3,(ab)^4>| = |S4|", Size(FqS4), 24);;

#############################################################################
## A-1/A-2: |Ghat5|/|G5|/|A| = 3000/500/125 ; Ghat5/A = S4 ; G5/A = V4=O2(S4)
## Two independent routes:
##  Route 1 (algebraic): Ghat5 := A(x)S4 via A-TRIV/GAMMA formulas
##    (4.7)(4.8): theta(n1,n2,n3)=(n2,n1,-n3), tau(n1,n2,n3)=(n3,n1,n2)
##    on A=F5^3 (already established/reused construction, addendum B).
##  Route 2 (PB3-permutation): MakeGn(5) (search/week3-battery-common.g,
##    reused verbatim across the project since W-6/W-5 tooling).
#############################################################################
Print("\n=== A-1/A-2 ===\n");
F5 := GF(5);; one := One(F5);;
thetaA := [[0,1,0],[1,0,0],[0,0,-1]] * one;;
tauA   := [[0,0,1],[1,0,0],[0,1,0]] * one;;
Chk("thetaA^2 = I (GAMMA formula sanity)", thetaA^2 = IdentityMat(3,F5), true);;
Chk("tauA^3 = I (GAMMA formula sanity)", tauA^3 = IdentityMat(3,F5), true);;
Chk("(thetaA*tauA)^4 = I (GAMMA formula sanity)", (thetaA*tauA)^4 = IdentityMat(3,F5), true);;

homS4toGL := GroupHomomorphismByImages(S4grp, GL(3,5), [theta,tau], [thetaA,tauA]);;
Chk("A-1pre: theta,tau -> GAMMA formula is a well-defined S4-hom", homS4toGL <> fail, true);;

A5mod := GF(5)^3;;
Ghat5 := SemidirectProduct(S4grp, homS4toGL, A5mod);;
Chk("A-1: |Ghat5| (route 1: A x| S4)", Size(Ghat5), 3000);;

embA := Embedding(Ghat5,2);;
Aimg := Image(embA);;
Chk("A-1: |A| (route 1)", Size(Aimg), 125);;
Chk("A-1b: A normal in Ghat5", IsNormal(Ghat5,Aimg), true);;

quoHom := NaturalHomomorphismByNormalSubgroup(Ghat5, Aimg);;
S4fromQuo := Image(quoHom);;
Chk("A-2: |Ghat5/A|", Size(S4fromQuo), 24);;
Chk("A-2b: Ghat5/A isomorphic to S4grp", IsomorphismGroups(S4fromQuo,S4grp) <> fail, true);;

V4list := Filtered(NormalSubgroups(S4fromQuo), n -> Size(n)=4);;
Chk("A-2c: unique order-4 normal subgroup of Ghat5/A (=V4=O2(S4))", Length(V4list), 1);;
V4q := V4list[1];;
G5sub := PreImage(quoHom, V4q);;
Chk("A-1: |G5| (route 1, preimage of V4)", Size(G5sub), 500);;
Aderived_r1 := DerivedSubgroup(G5sub);;
Chk("A-1: |[G5,G5]| (route 1)", Size(Aderived_r1), 125);;
Chk("A-1c: [G5,G5] elementary abelian exponent 5 (route1)",
    IsElementaryAbelian(Aderived_r1) and Exponent(Aderived_r1)=5, true);;
Chk("A-1d: [G5,G5] = A (route1, same subgroup)", Aderived_r1 = Aimg, true);;

## Route 2 cross-check
g5pb3 := MakeGn(5);;
Chk("A-1: |G5| (route 2: PB3/K^(5) via MakeGn)", Size(g5pb3.G), 500);;
Aderived_r2 := DerivedSubgroup(g5pb3.G);;
Chk("A-1: |[G5,G5]| (route 2)", Size(Aderived_r2), 125);;
invR1 := AbelianInvariants(G5sub/Aderived_r1);;
invR2 := AbelianInvariants(g5pb3.G/Aderived_r2);;
Chk("A-2d: G5/A abelian invariants agree across the two routes (cross-check)", invR1 = invR2, true);;
Chk("A-2e: G5/A = C2 x C2 (matches V4=O2(S4))", invR2, [2,2]);;

RESULTS.A1_Ghat5_order := Size(Ghat5);;
RESULTS.A1_G5_order := Size(G5sub);;
RESULTS.A1_A_order := Size(Aimg);;
RESULTS.A2_Ghat5_mod_A_is_S4 := true;;
RESULTS.A2_G5_mod_A_invariants := invR2;;
RESULTS.A2_cross_check_routes_agree := (invR1 = invR2);;

#############################################################################
## A-3/A-4: A-TRIV lemma. F_p[A] nontrivial irreducibles: dim 4, all 31 of
## them (Frobenius orbits of mult-by-p on F5^3\{0}, p in {2,3}).
## S4-orbits (via GAMMA formula action) on P^2(F5) (31 points): min size 3.
#############################################################################
Print("\n=== A-3/A-4 ===\n");
FrobOrbitCount := function(p)
  local vecs, seen, orbits, v, orb, cur, i;
  vecs := Cartesian(List([1,2,3], i -> AsList(F5)));;
  vecs := Filtered(vecs, v -> v <> [Zero(F5),Zero(F5),Zero(F5)]);;
  seen := [];; orbits := [];;
  for v in vecs do
    if not v in seen then
      orb := [v]; cur := v;
      for i in [1..10] do
        cur := List(cur, x -> p*x);
        if cur = v then break; fi;
        Add(orb, cur);
      od;
      Append(seen, orb); seen := Set(seen);
      Add(orbits, Length(orb));
    fi;
  od;
  return rec(numOrbits := Length(orbits), orbitSizes := Set(orbits), totalVecs := Length(vecs));
end;;

r2 := FrobOrbitCount(2);;
r3 := FrobOrbitCount(3);;
Chk("A-3: p=2, num F_p[A] nontrivial irreducibles (Frobenius orbits)", r2.numOrbits, 31);;
Chk("A-3: p=2, all orbits have dim 4", r2.orbitSizes, [4]);;
Chk("A-3: p=3, num F_p[A] nontrivial irreducibles", r3.numOrbits, 31);;
Chk("A-3: p=3, all orbits have dim 4", r3.orbitSizes, [4]);;

Normalize5 := function(v)
  local i;
  for i in [1..3] do
    if v[i] <> Zero(F5) then return List(v, x -> x*v[i]^-1); fi;
  od;
end;;
vecsAll := Cartesian(List([1,2,3], i -> AsList(F5)));;
vecsAll := Filtered(vecsAll, v -> v <> [Zero(F5),Zero(F5),Zero(F5)]);;
points := Set(List(vecsAll, Normalize5));;
Chk("A-4pre: |P^2(F5)|", Length(points), 31);;

Sgrp_onA := Group(thetaA, tauA);;
allEltsSgrp := Elements(Sgrp_onA);;
orbitSizesA4 := [];;
seenPts := [];;
for pt in points do
  if not pt in seenPts then
    orb := Set(List(allEltsSgrp, g -> Normalize5(pt*g)));;
    Append(seenPts, orb); seenPts := Set(seenPts);
    Add(orbitSizesA4, Length(orb));
  fi;
od;
Chk("A-4: minimal S4-orbit size on P^2(F5)", Minimum(orbitSizesA4), 3);;
RESULTS.A3_num_nontrivial_irred_A := r2.numOrbits;;
RESULTS.A3_irred_dim := 4;;
RESULTS.A4_min_orbit_size := Minimum(orbitSizesA4);;
RESULTS.A4_all_orbit_sizes := orbitSizesA4;;

#############################################################################
## A-5: dim H^2(S4, F2 trivial) = 2 (UCT)
#############################################################################
Print("\n=== A-5 ===\n");
mtriv2 := [ [[1]], [[1]] ] * Z(2);;
chrTriv2 := CHR(S4grp, 2, FqS4, mtriv2);;
h1triv2 := FirstCohomologyDimension(chrTriv2);;
h2triv2 := SecondCohomologyDimension(chrTriv2);;
Chk("A-5: dim H^2(S4,F2 trivial)", h2triv2, 2);;
Chk("A-5 sanity: dim H^1(S4,F2 trivial) (S4^ab=C2)", h1triv2, 1);;
RESULTS.A5_dimH2_S4_trivF2 := h2triv2;;

#############################################################################
## A-9: F2[S3] block decomposition F2C2 x M2(F2); dim2/3/4 module counts
## 3/3/6 (combinatorial count of (a,b,c) with a+2b+2c=dim, checked
## independently of the census script's own construction).
#############################################################################
Print("\n=== A-9 ===\n");
Gs3perm := Group((1,2),(1,2,3));;
ctS3 := CharacterTable(Gs3perm);;
pb := PrimeBlocks(ctS3,2);;
irrDims := List(Irr(ctS3), x -> x[1]);;
Print("  Irr dims = ", irrDims, "  PrimeBlocks(.,2).block = ", pb.block, "  defect=", pb.defect, "\n");
## Expect: two ordinary chars (trivial,sign, dim1 each) share one block of
## positive defect (=F2C2, 2-dim algebra); the dim-2 char (std) is alone in
## a defect-0 block (=M2(F2), semisimple).
blockOfDim1s := Set(List(Filtered([1..Length(irrDims)], i -> irrDims[i]=1), i -> pb.block[i]));;
blockOfDim2 := Set(List(Filtered([1..Length(irrDims)], i -> irrDims[i]=2), i -> pb.block[i]));;
Chk("A-9: the two dim-1 ordinary chars (triv,sgn) share ONE 2-modular block",
    Length(blockOfDim1s), 1);;
Chk("A-9: that block is distinct from the dim-2 char's block",
    Intersection(blockOfDim1s, blockOfDim2) = [], true);;

CountABC := function(dim)
  local n, aa;
  n := 0;
  aa := 0;
  while aa <= dim do
    if (dim - aa) mod 2 = 0 then n := n + ((dim-aa)/2 + 1); fi;
    aa := aa + 1;
  od;
  return n;
end;;
n2 := CountABC(2);; n3 := CountABC(3);; n4 := CountABC(4);;
Chk("A-9: dim2 (V-cen layer) module count", n2, 3);;
Chk("A-9: dim3 (V-cen layer) module count", n3, 3);;
Chk("A-9: dim4 (V-cen layer) module count", n4, 6);;
RESULTS.A9_block_decomp_confirmed := true;;
RESULTS.A9_counts_dim2_3_4 := [n2,n3,n4];;

#############################################################################
## A-10: K^(20) control (GAP reconstruction of erratum v2 SS3.5 python
## figures -- two-system numeric cross-check, not import).
#############################################################################
Print("\n=== A-10 ===\n");
g20 := MakeGn(20);;
g5chk := MakeGn(5);;
redHom20 := GroupHomomorphismByImages(g20.G, g5chk.G, [g20.x, g20.y], [g5chk.x, g5chk.y]);;
Chk("A-10pre: K20->K5 reduction hom well-defined and onto",
    (redHom20 <> fail) and (Size(Image(redHom20)) = Size(g5chk.G)), true);;
V20 := Kernel(redHom20);;
Zg20 := Center(g20.G);;
Dg20 := DerivedSubgroup(g20.G);;
W20 := Intersection(V20, Dg20);;
Chk("A-10: |G20|", Size(g20.G), 4000);;
Chk("A-10: |Z(G20)|", Size(Zg20), 8);;
Chk("A-10: |[G20,G20]|", Size(Dg20), 250);;
Chk("A-10: |W|=|V cap [G20,G20]|", Size(W20), 2);;
Chk("A-10: |V/W|", Size(V20)/Size(W20), 4);;
RESULTS.A10_g20 := rec(order:=Size(g20.G), Zorder:=Size(Zg20), derivedOrder:=Size(Dg20),
    Worder:=Size(W20), VmodWorder:=Size(V20)/Size(W20));;

#############################################################################
## A-11: LAT-Gamma. Gamma-stable index-2 sublattices of 2Z^2: count = 0.
## Gamma acts on Z^2=F2^ab by theta(a,b)=(b,a), tau(a,b)=(-b,a-b).
## The 3 index-2 sublattices of 2Z^2 (= the 3 nonzero elements of
## Hom(2Z^2,Z/2), a standard/complete list) are tested individually.
#############################################################################
Print("\n=== A-11 ===\n");
thetaLat := [[0,1],[1,0]];;
tauLat := [[0,-1],[1,-1]];;
Chk("A-11pre: thetaLat^2=I", thetaLat^2 = IdentityMat(2), true);;
Chk("A-11pre: tauLat^3=I", tauLat^3 = IdentityMat(2), true);;
IsLatStable := function(genMat, M)
  local i, sol;
  for i in [1..Length(genMat)] do
    sol := SolutionMat(genMat, genMat[i]*M);
    if sol = fail or not ForAll(sol, IsInt) then return false; fi;
  od;
  return true;
end;;
latCands := [ [[4,0],[0,2]], [[2,0],[0,4]], [[4,0],[2,2]] ];;
Chk("A-11pre: all 3 candidates have index 2 in 2Z^2 (det=8)",
    ForAll(latCands, L -> DeterminantMat(L) = 8), true);;
numStableLat := Length(Filtered(latCands,
    L -> IsLatStable(L,thetaLat) and IsLatStable(L,tauLat)));;
Chk("A-11: num Gamma-stable index-2 sublattices of 2Z^2", numStableLat, 0);;
RESULTS.A11_num_stable_index2_sublattices := numStableLat;;

#############################################################################
## A-12: VCEN-MOD calibration on K^(20): is K20's V an S3-inflate (V4 acts
## trivially)? Direct corollary of A-10 (Z(G20)=V => G20, hence its
## subgroup G5 and quotient V4=G5/A, act trivially on V by conjugation);
## also checked directly by conjugating V's generators by g20.x, g20.y
## (lifts of G5's generators).
#############################################################################
Print("\n=== A-12 ===\n");
Chk("A-12pre: Z(G20) = V (so V-cen holds for K20 by construction)", Zg20 = V20, true);;
v4triv := ForAll(GeneratorsOfGroup(V20), v -> v^g20.x = v and v^g20.y = v);;
Chk("A-12: V4 (=G5/A, via g20.x,g20.y lifts) acts trivially on V (direct conjugation check)",
    v4triv, true);;
RESULTS.A12_K20_is_S3_inflate := v4triv;;

#############################################################################
## A-13: Ext^1_{F2 S3}(D, F2) = 0.
#############################################################################
Print("\n=== A-13 ===\n");
V4norm := Filtered(NormalSubgroups(S4grp), n -> Size(n) = 4)[1];;
quoS3 := NaturalHomomorphismByNormalSubgroup(S4grp, V4norm);;
S3q := Image(quoS3);;
gl22 := GL(2,2);;
isoS3toGL := IsomorphismGroups(S3q, gl22);;
Dtheta := Image(isoS3toGL, Image(quoS3, theta));;
Dtau := Image(isoS3toGL, Image(quoS3, tau));;
Chk("A-13pre: Dtheta order 2", Order(Dtheta), 2);;
Chk("A-13pre: Dtau order 3", Order(Dtau), 3);;
## Dtheta,Dtau are IMAGES of theta,tau under S4->S3->GL(2,2); order can only
## drop (never rise) under a quotient/representation map, so this is NOT
## expected to equal A-0's S4-level order 4 -- the S3-level product order is
## checked immediately below instead (that is the correct invariant here).
Chk("A-13pre: (Dtheta*Dtau) order (S3-level image; NOT expected to equal A-0's S4-level 4)",
    Order(Dtheta*Dtau), 2);;

Gd := Group(Dtheta,Dtau);;
isoPerm := IsomorphismPermGroup(Gd);;
GdPerm := Image(isoPerm);;
thetaP := Image(isoPerm, Dtheta);; tauP := Image(isoPerm, Dtau);;
prodOrdS3 := Order(thetaP*tauP);;
Chk("A-13pre: prod order as ABSTRACT S3 elements (theta,tau images)", prodOrdS3, 2);;
FS3 := FreeGroup(2);;
FqS3 := FS3 / [FS3.1^2, FS3.2^3, (FS3.1*FS3.2)^prodOrdS3];;
Chk("A-13pre: |<a,b|a^2,b^3,(ab)^2>|", Size(FqS3), 6);;

DthetaStar := TransposedMat(Inverse(Dtheta));;
DtauStar := TransposedMat(Inverse(Dtau));;
mDstar := [ [DthetaStar[1],DthetaStar[2]], [DtauStar[1],DtauStar[2]] ];;
GdPermGens := Group(thetaP,tauP);;
chrExt := CHR(GdPermGens, 2, FqS3, mDstar);;
ext1_D_triv := FirstCohomologyDimension(chrExt);;
Chk("A-13: Ext^1_{F2S3}(D,F2) = H^1(S3,D^*)", ext1_D_triv, 0);;
RESULTS.A13_Ext1_D_triv := ext1_D_triv;;

#############################################################################
## ==== JSON output ====
#############################################################################
Print("\n=== writing cert ===\n");

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_w6bu_s0_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then
    Error("ComputeSha256File: sha256sum did not return a hash line for ", relpath);
  fi;
  return line{[1 .. 64]};
end;;

selfSha := ComputeSha256File("search/probe/w6_bu_s0/w6_bu_s0_driver.g");;
designSha := ComputeSha256File("docs/notes/w6_bottomup_design_v2.md");;

assertBlock := Concatenation(
  "{",
  "\"A0_order_theta_tau\":", String(RESULTS.A0_order_theta_tau), ",",
  "\"A1_Ghat5_order\":", String(RESULTS.A1_Ghat5_order), ",",
  "\"A1_G5_order\":", String(RESULTS.A1_G5_order), ",",
  "\"A1_A_order\":", String(RESULTS.A1_A_order), ",",
  "\"A1_cross_check_two_routes_agree\":", JB(RESULTS.A2_cross_check_routes_agree), ",",
  "\"A2_Ghat5_mod_A_is_S4\":", JB(RESULTS.A2_Ghat5_mod_A_is_S4), ",",
  "\"A2_G5_mod_A_invariants\":", JArr(List(RESULTS.A2_G5_mod_A_invariants,String)), ",",
  "\"A3_num_nontrivial_irred_A\":", String(RESULTS.A3_num_nontrivial_irred_A), ",",
  "\"A3_irred_dim\":", String(RESULTS.A3_irred_dim), ",",
  "\"A4_min_orbit_size\":", String(RESULTS.A4_min_orbit_size), ",",
  "\"A4_all_orbit_sizes\":", JArr(List(RESULTS.A4_all_orbit_sizes,String)), ",",
  "\"A5_dimH2_S4_trivF2\":", String(RESULTS.A5_dimH2_S4_trivF2), ",",
  "\"A9_block_decomp_confirmed\":", JB(RESULTS.A9_block_decomp_confirmed), ",",
  "\"A9_counts_dim2_3_4\":", JArr(List(RESULTS.A9_counts_dim2_3_4,String)), ",",
  "\"A10_g20\":{\"order\":", String(RESULTS.A10_g20.order),
    ",\"Z_order\":", String(RESULTS.A10_g20.Zorder),
    ",\"derived_order\":", String(RESULTS.A10_g20.derivedOrder),
    ",\"W_order\":", String(RESULTS.A10_g20.Worder),
    ",\"V_mod_W_order\":", String(RESULTS.A10_g20.VmodWorder), "},",
  "\"A11_num_stable_index2_sublattices\":", String(RESULTS.A11_num_stable_index2_sublattices), ",",
  "\"A12_K20_is_S3_inflate\":", JB(RESULTS.A12_K20_is_S3_inflate), ",",
  "\"A13_Ext1_D_triv\":", String(RESULTS.A13_Ext1_D_triv),
  "}");;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"w6-bu-s0/v1\",\n",
  "  \"generated_by\":\"search/probe/w6_bu_s0/w6_bu_s0_driver.g\",\n",
  "  \"card_label\":\"W6BU-S0: BOTTOM-UP census S0 calibration (A-0..A-13, per w6_bottomup_design_v2.md SS7.2)\",\n",
  "  \"design_doc\":\"docs/notes/w6_bottomup_design_v2.md\",\n",
  "  \"authorization\":\"sol/sol_reply_102_math29.md F102-6.3 (限定認可: S0較正 + H^2(S4,V)在庫表/census のみ. 棄却・EMPTY-THM・候補発見への使用は範囲外)\",\n",
  "  \"tier\":\"calibration\",\n",
  "  \"scope_statement\":\"本certは較正のみ. kill/棄却/候補発見/EMPTY-THM のいずれにも使用しない. C4/C9/非可換核【BU-GAP-1】はSCOPE_OUTのまま(空と主張しない).\",\n",
  "  \"seal_declaration\":{\"touches_c_hat_mu\":false,\"touches_psl_sealed_fields\":false,\n",
  "    \"touches_wall_campaign_pbit\":false,\"touches_u_values\":false,\"touches_im_R\":false,\n",
  "    \"touches_d_N\":false,\"reads_certificates\":false},\n",
  "  \"asserts\":", assertBlock, ",\n",
  "  \"fails_total\":", String(Length(FAILS)), ",\n",
  "  \"fails\":", JArr(List(FAILS, f -> Concatenation("{\"name\":", JStr(f.name),
      ",\"got\":", JStr(f.got), ",\"want\":", JStr(f.want), "}"))), ",\n",
  "  \"stop_rule_status\":", (function()
      if Length(FAILS) > 0 then return "\"PREREGISTRATION_FALSIFIED / INTEGRITY_STOP (S-BU-1)\"";
      else return "\"S0_PASS -- all A-0..A-13 asserts match design v2 SS7.2 expected values\""; fi;
    end)(), ",\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"design_doc_v2_sha256\":", JStr(designSha), ",\n",
  "    \"wall_ms_total\":", String(GAPLIB_WallElapsedMs()), "\n",
  "  }\n",
  "}\n");;

OUT_PATH := "search/certs/k5gen_w6_bu_s0_20260805.json";;
WriteFile(OUT_PATH, cert);;
Print("Wrote ", OUT_PATH, "\n");
Print("\nFAILS = ", Length(FAILS), "\n");
for fitem in FAILS do
  Print("   ", fitem.name, " got=", fitem.got, " want=", fitem.want, "\n");
od;
Print("\nW6_BU_S0_DRIVER_DONE\n");
QUIT;
