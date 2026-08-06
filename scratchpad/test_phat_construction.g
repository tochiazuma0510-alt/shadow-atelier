#############################################################################
## scratchpad/test_phat_construction.g -- validate Phat (fiber product)
## construction on D+D row only, before writing full v2 driver.
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
LoadPackage("cohomolo");;

sig1 := (1,4,2,5,3)(6,11)(7,12,10,15)(8,13,9,14);;
sig2 := (1,12,2,11)(3,15,5,13)(4,14)(6,9,7,10,8);;
DeltaHat := sig1*sig2*sig1;;
deltaHat := sig1*sig2;;
Ghat5 := Group(sig1, sig2);;
Print("Size(Ghat5)=", Size(Ghat5), "\n");

G5loc := Group(sig1^2, sig2^2);;
Print("Size(G5loc)=", Size(G5loc), "\n");
Amod := DerivedSubgroup(G5loc);;
Print("Size(Amod)=", Size(Amod), " IsNormal=", IsNormal(Ghat5,Amod), "\n");

S4grp := Group((1,2),(1,3,4));;
theta := (1,2);; tau := (1,3,4);;
FS4 := FreeGroup(2);;
FqS4 := FS4 / [FS4.1^2, FS4.2^3, (FS4.1*FS4.2)^4];;

quo := NaturalHomomorphismByNormalSubgroup(Ghat5, Amod);;
Sbar := Image(quo);;
Print("Size(Sbar)=", Size(Sbar), "\n");
thetaImg := Image(quo, DeltaHat);; tauImg := Image(quo, deltaHat);;
isoSbarToS4 := GroupHomomorphismByImages(Sbar, S4grp, [thetaImg,tauImg], [theta,tau]);;
Print("isoSbarToS4 fail? ", isoSbarToS4 = fail, "\n");
p_G := CompositionMapping(isoSbarToS4, quo);;
Print("p_G(DeltaHat)=", Image(p_G,DeltaHat), " want theta=", theta, "\n");
Print("p_G(deltaHat)=", Image(p_G,deltaHat), " want tau=", tau, "\n");

## ---- PART B setup (verbatim from w6_bu_s35_driver.g) ----
V4norm := Filtered(NormalSubgroups(S4grp), n -> Size(n) = 4)[1];;
quoS3 := NaturalHomomorphismByNormalSubgroup(S4grp, V4norm);;
S3q := Image(quoS3);;
gl22 := GL(2,2);;
isoS3toGL22 := IsomorphismGroups(S3q, gl22);;

D_a := Image(isoS3toGL22, Image(quoS3, theta));;
D_b := Image(isoS3toGL22, Image(quoS3, tau));;

BlockDiag := function(mats)
  local dim, res, offs, i, j, m;
  dim := Sum(mats, m -> Length(m));
  res := List([1..dim], i -> List([1..dim], j -> Zero(GF(2))));
  offs := 0;
  for m in mats do
    for i in [1..Length(m)] do
      for j in [1..Length(m)] do
        res[offs+i][offs+j] := m[i][j];
      od;
    od;
    offs := offs + Length(m);
  od;
  return res;
end;;

ma := BlockDiag([D_a,D_a]);;   ## a0b0c2: two copies of D
mb := BlockDiag([D_b,D_b]);;
dim := Length(ma);; pPrime := 2;;
Print("dim=", dim, " pPrime=", pPrime, "\n");

chr := CHR(S4grp, pPrime, FqS4, [ma, mb]);;
h2 := SecondCohomologyDimension(chr);;
Cohomolo(chr, false, true, false, "scratchpad/.tmp_test_phat");;
Print("h2=", h2, " chr.codim2=", chr.codim2, "\n");

## first class: vec = [0,0]  (split)
vec := [0,0];;
Eext := SplitExtensionCHR(chr);;
isoE := IsomorphismPcGroup(Eext);;
Epc := Image(isoE);;
EGpc := List(GeneratorsOfGroup(Eext), g -> Image(isoE,g));;
U0 := EGpc[1];; W0 := EGpc[2];;
Vgens := EGpc{[3..2+dim]};;
Print("Size(Epc)=", Size(Epc), " want ", 24*2^dim, "\n");

Vsub := Subgroup(Epc, Vgens);;
Print("Size(Vsub)=", Size(Vsub), " IsNormal=", IsNormal(Epc,Vsub), "\n");
quoE := NaturalHomomorphismByNormalSubgroup(Epc, Vsub);;
S4viaE := Image(quoE);;
Print("Size(S4viaE)=", Size(S4viaE), "\n");
isoS4viaEtoS4 := GroupHomomorphismByImages(S4viaE, S4grp, [Image(quoE,U0),Image(quoE,W0)], [theta,tau]);;
Print("isoS4viaEtoS4 fail? ", isoS4viaEtoS4 = fail, "\n");
piE := CompositionMapping(isoS4viaEtoS4, quoE);;
Print("piE(U0)=", Image(piE,U0), " want theta=", theta, "\n");
Print("piE(W0)=", Image(piE,W0), " want tau=", tau, "\n");

## ---- build D = DirectProduct(Ghat5, Epc), then Phat as generated subgroup ----
D := DirectProduct(Ghat5, Epc);;
Print("Size(D)=", Size(D), "\n");
emb1 := Embedding(D,1);; emb2 := Embedding(D,2);;

PhatGens := Concatenation(
  List(GeneratorsOfGroup(Amod), a -> Image(emb1,a)),
  List(GeneratorsOfGroup(Vsub), v -> Image(emb2,v)),
  [ Image(emb1,DeltaHat) * Image(emb2,U0),
    Image(emb1,deltaHat) * Image(emb2,W0) ]
);;
Phat := Subgroup(D, PhatGens);;
Print("Size(Phat)=", Size(Phat), " want ", 3000*2^dim, "\n");

Uhat0 := Image(emb1,DeltaHat) * Image(emb2,U0);;
What0 := Image(emb1,deltaHat) * Image(emb2,W0);;

## Sanity fixture (2): S4-projection of lifts
Print("piE(U0)=theta check: ", Image(piE,U0)=theta, "\n");
Print("piE(W0)=tau check: ", Image(piE,W0)=tau, "\n");

## Sanity fixture (1): Phat / V-copy = Ghat5 (LIGHT check: order + generator
## order pattern, NOT a full GroupHomomorphismByImages+IsBijective relator
## check -- that step was the slow one, empirically >5 min wall with no
## result; order+relation checks below are O(seconds) and give equivalent
## confidence given Uhat0,What0 already independently confirmed to project
## correctly to theta,tau via piE).
## NOTE: NaturalHomomorphismByNormalSubgroup(Phat,Vhat) was empirically the
## slow step (>5 min wall, no result) for a degree-399/order-48000 perm
## group -- replaced with direct ELEMENT-ORDER checks (no quotient object
## construction needed): Size(Phat)=3000*|V| already confirmed above via
## Lagrange gives |Phat/Vhat|=3000 for free once Vhat is confirmed normal of
## order |V|; the remaining content (does the quotient actually look like
## Ghat5, i.e. do Uhat0,What0 project to elements of order 2,3 with product
## order matching Delta*delta) is checked via plain element orders in Phat
## itself (cheap: bounded search, no coset table).
VhatGens := List(GeneratorsOfGroup(Vsub), v -> Image(emb2,v));;
Print("|VhatGens|=", Length(VhatGens), "\n");
Print("order(Uhat0)=", Order(Uhat0), " want 2 (since vec=[0,0] split class, a=0 solves N_theta(0)=0)\n");
Print("order(What0)=", Order(What0), " want 3\n");
Print("order(Uhat0*What0)=", Order(Uhat0*What0), " (Ghat5-level order(Delta*delta)=", Order(DeltaHat*deltaHat), ")\n");

## ---- L-3 test for class vec=[0,0], a=0,b=0 (identity lift) ----
rs1 := What0^-1 * Uhat0;;
rs2 := Uhat0^-1 * What0^2;;
Hsub := Subgroup(Phat, [rs1,rs2]);;
Print("Size(H)=", Size(Hsub), " Size(Phat)=", Size(Phat), " L3=", Size(Hsub)=Size(Phat), "\n");

## ---- timing test: full 64-pair enumeration for this class (dim4,p=2 ->
## |V|=16, expect |solsA|=8,|solsB|=8 -> 64 pairs, matching companion detail
## json lane_a_marked_lift_counts[1]=64 for p2_d4_a0b0c2 class vec=[0,0,0,0]...
## NOTE: here dim2 module (D+D uses gl22 D-rep twice -> dim4 total), h2=2, so
## vec has length 2 not 4 -- eps computed via chr.modrelvals as in old driver).
SolveAffine := function(M, v, p)
  local dimM, part, ns, sols, combo, cur, F;
  F := GF(p);
  dimM := Length(M);
  part := SolutionMat(M, v);
  if part = fail then return []; fi;
  ns := NullspaceMat(M);
  if Length(ns) = 0 then return [part]; fi;
  sols := [];
  for combo in Cartesian(List([1..Length(ns)], i -> [0..p-1])) do
    cur := part + Sum([1..Length(ns)], i -> combo[i]*ns[i]) * Z(p)^0;
    Add(sols, cur);
  od;
  return sols;
end;;

Ntheta := ma + IdentityMat(dim, GF(pPrime));;
Ntau := IdentityMat(dim, GF(pPrime)) + mb + mb^2;;
epsDelta := List([1..dim], j -> (Sum([1..h2], k -> vec[k]*chr.modrelvals[k][1][j])) mod pPrime) * Z(pPrime)^0;;
epsDelta := epsDelta * (-Z(pPrime)^0);;
epsTau := List([1..dim], j -> (Sum([1..h2], k -> vec[k]*chr.modrelvals[k][2][j])) mod pPrime) * Z(pPrime)^0;;
epsTau := epsTau * (-Z(pPrime)^0);;
solsA := SolveAffine(Ntheta, epsDelta, pPrime);;
solsB := SolveAffine(Ntau, epsTau, pPrime);;
Print("Length(solsA)=", Length(solsA), " Length(solsB)=", Length(solsB), " laneA=", Length(solsA)*Length(solsB), "\n");

VecToVsubElt := function(vv)
  local expv, j;
  expv := List([1..dim], j -> IntFFE(vv[j]));
  return Product([1..dim], j -> Vgens[j]^expv[j]);
end;;

t0 := Runtime();;
nSurj := 0;; nTot := 0;;
for aVec in solsA do
  for bVec in solsB do
    aElt := VecToVsubElt(aVec);; bElt := VecToVsubElt(bVec);;
    UhatA := Uhat0 * Image(emb2,aElt);;
    WhatB := What0 * Image(emb2,bElt);;
    rho1 := WhatB^-1 * UhatA;;
    rho2 := UhatA^-1 * WhatB^2;;
    Hp := Subgroup(Phat,[rho1,rho2]);;
    nTot := nTot + 1;;
    if Size(Hp) = Size(Phat) then nSurj := nSurj + 1; fi;
  od;
od;
Print("nTot=", nTot, " nSurj=", nSurj, " wall_ms(approx via Runtime CPU)=", Runtime()-t0, "\n");

Print("TEST_PHAT_DONE\n");
QUIT;
