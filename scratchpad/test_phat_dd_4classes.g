#############################################################################
## scratchpad/test_phat_dd_4classes.g -- L-3 (full P-hat surjectivity) over
## all 4 classes of the D+D row (p2_d4_a0b0c2), validating the fiber-product
## P-hat construction at scale before committing to the full 73-class run.
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
G5loc := Group(sig1^2, sig2^2);;
Amod := DerivedSubgroup(G5loc);;

S4grp := Group((1,2),(1,3,4));;
theta := (1,2);; tau := (1,3,4);;
FS4 := FreeGroup(2);;
FqS4 := FS4 / [FS4.1^2, FS4.2^3, (FS4.1*FS4.2)^4];;

quo := NaturalHomomorphismByNormalSubgroup(Ghat5, Amod);;
Sbar := Image(quo);;
thetaImg := Image(quo, DeltaHat);; tauImg := Image(quo, deltaHat);;
isoSbarToS4 := GroupHomomorphismByImages(Sbar, S4grp, [thetaImg,tauImg], [theta,tau]);;
p_G := CompositionMapping(isoSbarToS4, quo);;

V4norm := Filtered(NormalSubgroups(S4grp), n -> Size(n) = 4)[1];;
quoS3 := NaturalHomomorphismByNormalSubgroup(S4grp, V4norm);;
S3q := Image(quoS3);;
gl22 := GL(2,2);;
isoS3toGL22 := IsomorphismGroups(S3q, gl22);;
D_a := Image(isoS3toGL22, Image(quoS3, theta));;
D_b := Image(isoS3toGL22, Image(quoS3, tau));;

BlockDiag := function(mats)
  local dimm, res, offs, i, j, m;
  dimm := Sum(mats, m -> Length(m));
  res := List([1..dimm], i -> List([1..dimm], j -> Zero(GF(2))));
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

ma := BlockDiag([D_a,D_a]);;
mb := BlockDiag([D_b,D_b]);;
dim := Length(ma);; pPrime := 2;;
Print("dim=", dim, " pPrime=", pPrime, "\n");

chr := CHR(S4grp, pPrime, FqS4, [ma, mb]);;
h2 := SecondCohomologyDimension(chr);;
Cohomolo(chr, false, true, false, "scratchpad/.tmp_test_phat_dd4");;
Print("h2=", h2, "\n");

Ntheta := ma + IdentityMat(dim, GF(pPrime));;
Ntau := IdentityMat(dim, GF(pPrime)) + mb + mb^2;;

SolveAffine := function(M, v, p)
  local dimM, part, ns, sols, combo, cur;
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

VecToElt := function(vv, gens, dimm)
  local expv, j;
  expv := List([1..dimm], j -> IntFFE(vv[j]));
  return Product([1..dimm], j -> gens[j]^expv[j]);
end;;

classVecs := Cartesian(List([1..h2], ii -> [0..pPrime-1]));;
Print("num classes = ", Length(classVecs), "\n");

totalSurj := 0;; totalPairs := 0;;
for vec in classVecs do
  Print("\n=== class vec=", vec, " ===\n");
  if ForAll(vec, vv -> vv = 0) then
    Eext := SplitExtensionCHR(chr);;
  else
    Eext := NonsplitExtension(chr, vec);;
  fi;
  isoE := IsomorphismPcGroup(Eext);;
  Epc := Image(isoE);;
  EGpc := List(GeneratorsOfGroup(Eext), g -> Image(isoE,g));;
  U0 := EGpc[1];; W0 := EGpc[2];;
  Vgens := EGpc{[3..2+dim]};;
  Vsub := Subgroup(Epc, Vgens);;
  quoE := NaturalHomomorphismByNormalSubgroup(Epc, Vsub);;
  S4viaE := Image(quoE);;
  isoS4viaEtoS4 := GroupHomomorphismByImages(S4viaE, S4grp, [Image(quoE,U0),Image(quoE,W0)], [theta,tau]);;
  piE := CompositionMapping(isoS4viaEtoS4, quoE);;

  D := DirectProduct(Ghat5, Epc);;
  emb1 := Embedding(D,1);; emb2 := Embedding(D,2);;
  PhatGens := Concatenation(
    List(GeneratorsOfGroup(Amod), a -> Image(emb1,a)),
    List(GeneratorsOfGroup(Vsub), v -> Image(emb2,v)),
    [ Image(emb1,DeltaHat) * Image(emb2,U0),
      Image(emb1,deltaHat) * Image(emb2,W0) ]
  );;
  Phat := Subgroup(D, PhatGens);;
  sizePhat := Size(Phat);;
  Uhat0 := Image(emb1,DeltaHat) * Image(emb2,U0);;
  What0 := Image(emb1,deltaHat) * Image(emb2,W0);;
  Print("Size(Phat)=", sizePhat, " want ", 3000*2^dim,
        " | order(Uhat0*What0)=", Order(Uhat0*What0),
        " ref-order(Delta*delta)=", Order(DeltaHat*deltaHat), "\n");

  epsDelta := List([1..dim], j -> (Sum([1..h2], k -> vec[k]*chr.modrelvals[k][1][j])) mod pPrime) * Z(pPrime)^0;;
  epsDelta := epsDelta * (-Z(pPrime)^0);;
  epsTau := List([1..dim], j -> (Sum([1..h2], k -> vec[k]*chr.modrelvals[k][2][j])) mod pPrime) * Z(pPrime)^0;;
  epsTau := epsTau * (-Z(pPrime)^0);;
  solsA := SolveAffine(Ntheta, epsDelta, pPrime);;
  solsB := SolveAffine(Ntau, epsTau, pPrime);;
  Print("laneA(count)=", Length(solsA)*Length(solsB), "\n");

  classSurj := 0;; classTot := 0;;
  for aVec in solsA do
    for bVec in solsB do
      aElt := VecToElt(aVec, Vgens, dim);; bElt := VecToElt(bVec, Vgens, dim);;
      UhatA := Uhat0 * Image(emb2,aElt);;
      WhatB := What0 * Image(emb2,bElt);;
      rho1 := WhatB^-1 * UhatA;;
      rho2 := UhatA^-1 * WhatB^2;;
      Hp := Subgroup(Phat,[rho1,rho2]);;
      classTot := classTot + 1;;
      if Size(Hp) = sizePhat then classSurj := classSurj + 1; fi;
    od;
  od;
  Print("class L3: surj=", classSurj, " / tot=", classTot, "\n");
  totalSurj := totalSurj + classSurj;; totalPairs := totalPairs + classTot;;
od;

Print("\n=== D+D ROW TOTAL: L3_surjective=", totalSurj, " / affine_pairs=", totalPairs, " ===\n");
Print("TEST_DD4_DONE\n");
QUIT;
