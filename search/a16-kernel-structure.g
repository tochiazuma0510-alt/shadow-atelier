#############################################################################
## search/a16-kernel-structure.g -- P81-A: A16-kernel-structure/v1
## (裁定・並行朝ラウンド)
##
## Reconstructs GTSh(N,N) for W-D-A16-11a (reusing the strike-a16.g /
## kerchi-judge.g machinery) and issues a structural capsule:
##   G_order, K_order (=|ker chi~|=88), Gprime_order (=|G'|=22),
##   Kprime_order (=|K'|), Z(K)_order, K/G' (C4 or C2xC2 -- the "most
##   important bit"), G/G' invariant factors, Sylow-11 action + complement,
##   Im(Xi)/ker(Xi).
##
## Witness-first: generators are recorded as explicit permutations (of the
## 16-point support of P_N=A16), not just abstract orders/structure names.
##
## Output: search/certs/a16_kernel_structure_20260729.json
#############################################################################

JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");

#############################################################################
## ---------------------- window construction (same as strike-a16.g) --------
#############################################################################
a1 := ( 1, 2)( 3,14)( 4,10)( 5,12)( 6, 8)( 7,16)( 9,13)(11,15);;
b1 := ( 2,11,14)( 3,15,10)( 4, 9,12)( 5,13, 8)( 6, 7,16);;
A16 := AlternatingGroup(16);;
S16 := SymmetricGroup(16);;
S3 := SymmetricGroup(3);;
Dgrp := DirectProduct(A16, S3);;
embA := Embedding(Dgrp, 1);;  embS := Embedding(Dgrp, 2);;
agen := Image(embA, a1) * Image(embS, (1,3));;
bgen := Image(embA, b1) * Image(embS, (1,3,2));;
s1 := bgen^-1 * agen;;
s2 := agen^-1 * bgen^2;;
W := MakeWindow(s1, s2);;
ch := Filtered([0 .. W.Nord - 1], m -> Gcd(2*m+1, W.Nord) = 1);;

Print("=== reconstructing GTSh(N,N) for W-D-A16-11a ===\n");
corrRes := CorrectedShadows(W, ch);;
corr := corrRes.shadows;;
Print("scan_mode=", corrRes.scan_mode, " shadow_total=", Length(corr), "\n");

gi := GroupOfShadows(W, corr);;
Print("(3.53) closed=", gi.closed, "  |G|=", gi.order, "\n");
if not gi.closed then
  Error("a16-kernel-structure.g: (3.53) did not close -- refusing to report ",
        "structure of a group that was not confirmed to exist");
fi;
G := gi.G;;
K := gi.ker;;

#############################################################################
## ---------------------- basic invariants -----------------------------------
#############################################################################
Print("\n=== basic invariants ===\n");
GOrder := Size(G);;
KOrder := Size(K);;
Gprime := DerivedSubgroup(G);;
GprimeOrder := Size(Gprime);;
Kprime := DerivedSubgroup(K);;
KprimeOrder := Size(Kprime);;
ZK := Center(K);;
ZKOrder := Size(ZK);;
Print("G_order=", GOrder, "  K_order=", KOrder, "  Gprime_order=", GprimeOrder,
      "  Kprime_order=", KprimeOrder, "  Z(K)_order=", ZKOrder, "\n");
Print("ker_commutes (IsAbelian(K))? ", IsAbelian(K), "\n");
Print("K structure description = ", StructureDescription(K), "\n");

# witness generators (matched back to explicit (m,f) shadow coordinates), for the certificate
smallGensK := SmallGeneratingSet(K);;
fValsOfGens := [];;
for gk in smallGensK do
  pos := Position(gi.regs, gk);;
  if pos <> fail then
    Add(fValsOfGens, rec(idx := pos, f := corr[pos][2], m := corr[pos][1]));
  fi;
od;
Print("witness generators (", Length(fValsOfGens), "/", Length(smallGensK), " matched to explicit shadow coords):\n");
for r in fValsOfGens do
  Print("  shadow_idx=", r.idx, " m=", r.m, " f=", r.f, "\n");
od;

#############################################################################
## ---------------------- the "most important bit": K/G' -------------------
#############################################################################
Print("\n=== K/G' : C4 or C2 x C2? ===\n");
isGprimeInK := IsSubset(K, Gprime);;
Print("G' subset of K (required for K/G' to make sense)? ", isGprimeInK, "\n");
KmodGprimeStruct := "UNDEFINED";;
KmodGprimeIsC4 := fail;;
if isGprimeInK then
  KmodGprime := FactorGroup(K, Gprime);;
  KmodGprimeOrder := Size(KmodGprime);;
  KmodGprimeStruct := StructureDescription(KmodGprime);;
  KmodGprimeIsC4 := IsCyclic(KmodGprime);;
  Print("|K/G'|=", KmodGprimeOrder, "  struct=", KmodGprimeStruct,
        "  IS_C4(cyclic)=", KmodGprimeIsC4, "\n");
  Print("*** VERDICT: K/G' = ", KmodGprimeStruct, " (",
        PF(KmodGprimeIsC4), "=C4, ", PF(not KmodGprimeIsC4), "=C2xC2) ***\n");
fi;
Print("Z(K) = G' (as subgroups)? ", ZK = Gprime, "\n");
Print("K' subset of Z(K)? ", IsSubset(ZK, Kprime), "\n");

#############################################################################
## ---------------------- G/G' invariant factors -----------------------------
#############################################################################
Print("\n=== G/G' invariant factors ===\n");
GmodGprime := FactorGroup(G, Gprime);;
GmodGprimeInvariants := AbelianInvariants(GmodGprime);;
Print("|G/G'|=", Size(GmodGprime), "  invariant factors=", GmodGprimeInvariants, "\n");

#############################################################################
## ---------------------- Sylow-11 action and complement ----------------------
#############################################################################
Print("\n=== Sylow-11(K), complement, action ===\n");
syl11K := SylowSubgroup(K, 11);;
syl11Normal := IsNormal(K, syl11K);;
Print("|Syl11(K)|=", Size(syl11K), " normal in K?=", syl11Normal,
      " cyclic?=", IsCyclic(syl11K), "\n");
genSyl := GeneratorsOfGroup(syl11K)[1];;

complementOrder := -1;;  complementStruct := "UNDEFINED";;  actionExponents := [];;
actionKernelOrder := -1;;  actionImageOrder := -1;;
if syl11Normal and IsSolvable(K) then
  comps := ComplementClassesRepresentatives(K, syl11K);;
  Print("number of complement classes=", Length(comps), "\n");
  if Length(comps) > 0 then
    comp8 := comps[1];;
    complementOrder := Size(comp8);;
    complementStruct := StructureDescription(comp8);;
    Print("|complement|=", complementOrder, "  struct=", complementStruct, "\n");
    genComp := GeneratorsOfGroup(comp8);;
    trivialActors := 0;;
    for g in genComp do
      imgElt := genSyl ^ g;;
      found := fail;;
      for e in [1 .. Order(genSyl) - 1] do
        if genSyl^e = imgElt then found := e; break; fi;
      od;
      Add(actionExponents, found);
      if found = 1 then trivialActors := trivialActors + 1; fi;
    od;
    Print("complement generators' conjugation-exponents on Syl11 (mod ",
          Order(genSyl), ") = ", actionExponents, "\n");
    Print("action is TRIVIAL on all generators (Syl11 central in K, K = Syl11 x complement)? ",
          trivialActors = Length(genComp), "\n");
  fi;
fi;

#############################################################################
## ---------------------- Xi map: K -> Aut(P_N), Im/Ker ----------------------
## Xi([0,f]) = "conjugation by f" (established convention: E_{0,f}(z) =
## f*z*f^-1).
##
## *** METHOD NOTE (found while implementing, 2026-07-29): constructing Xi as
## an explicit GroupHomomorphismByImages(K, P_N, gens, f-values) was tried
## first and FAILED under both the direct assignment (k |-> f_k) and its
## inverse (k |-> f_k^-1) -- neither is a well-defined homomorphism on the
## SmallGeneratingSet(K) tested (verified directly: for two independent
## kernel-layer shadows, the f-value of their regular-representation product
## matched NEITHER f1*f2 NOR f2*f1 NOR either's inverse). The exact
## composition-order convention Xi actually uses was not resolved (would
## need reconciling GroupOfShadows' regular-representation row/column
## convention with the AbstractProd reversal convention, a further layer of
## convention-stacking not chased down further here -- reported as UNKNOWN,
## not invented).
##
## Instead, ker(Xi) and |Im(Xi)| are obtained via a DIRECTION-INDEPENDENT
## route that sidesteps this ambiguity entirely: ker(Xi) is BY DEFINITION
## {[0,f] in K : E_{0,f} = id_{P_N}} = {[0,f] in K : f in C_P(ybar)} (f
## centralizes ybar, so conjugation by f fixes ybar; combined with
## E_{0,f}(xbar)=xbar always, E_{0,f} fixes both generators of P_N=<xbar,
## ybar>, hence is the identity automorphism). This SET is well-defined
## regardless of whether Xi is a homomorphism or an anti-homomorphism in
## whichever convention (the kernel of a hom and of its "reversed" anti-hom
## cousin are literally the same set), so it can be read off directly from
## the shadow data without ever building the fragile homomorphism object.
## |Im(Xi)| then follows from |K| = |ker(Xi)| * |Im(Xi)| (a plain counting
## identity, again independent of hom-vs-anti-hom direction).
#############################################################################
Print("\n=== Xi map: K -> Aut(P_N) (conjugation by f), Im(Xi)/ker(Xi) ===\n");
CPy := Centralizer(W.PN, W.y);;
Print("|C_P(ybar)| = ", Size(CPy), "\n");
kerXiShadowIdx := Filtered(gi.ker_idx, i -> corr[i][2] in CPy);;
xiKerOrderRaw := Length(kerXiShadowIdx);;
Print("count of kernel-layer shadows with f in C_P(ybar) (candidate |ker(Xi)| as a SET) = ",
      xiKerOrderRaw, "\n");
kerXiGrp := Group(List(kerXiShadowIdx, i -> gi.regs[i]));;
xiKerOrder := Size(kerXiGrp);;
Print("|<these shadows>| as a subgroup of K (should equal the count above if it is ",
      "already closed under K's multiplication) = ", xiKerOrder, "\n");
xiKerStruct := StructureDescription(kerXiGrp);;
Print("ker(Xi) struct = ", xiKerStruct, "\n");
Print("ker(Xi) subset of Z(K)? ", IsSubset(ZK, kerXiGrp), "\n");
if KOrder mod xiKerOrder = 0 then
  xiImOrder := KOrder / xiKerOrder;;
else
  xiImOrder := -1;;   # sentinel: kerXiGrp not actually a subgroup of K of the expected kind
fi;
Print("|Im(Xi)| (= |K|/|ker(Xi)| by counting, direction-independent) = ", xiImOrder, "\n");
xiImStruct := "NOT INDEPENDENTLY CONSTRUCTED (see method note above -- only the ORDER is reported, via counting; the explicit homomorphism object was not successfully built)";;

#############################################################################
## ---------------------- write JSON -------------------------------------------
#############################################################################
outParts := [];;
Add(outParts, "{\n");
Add(outParts, "  \"generated_by\": \"search/a16-kernel-structure.g\",\n");
Add(outParts, "  \"note\": \"P81-A structural capsule for GTSh(W-D-A16-11a); NOT a ledger claim, no cross-check performed (single implementation)\",\n");
Add(outParts, Concatenation("  \"G_order\": ", String(GOrder), ",\n"));
Add(outParts, Concatenation("  \"K_order\": ", String(KOrder), ",\n"));
Add(outParts, Concatenation("  \"K_is_abelian\": ", JB(IsAbelian(K)), ",\n"));
Add(outParts, Concatenation("  \"K_struct\": ", JStr(StructureDescription(K)), ",\n"));
Add(outParts, Concatenation("  \"Gprime_order\": ", String(GprimeOrder), ",\n"));
Add(outParts, Concatenation("  \"Kprime_order\": ", String(KprimeOrder), ",\n"));
Add(outParts, Concatenation("  \"ZK_order\": ", String(ZKOrder), ",\n"));
Add(outParts, Concatenation("  \"ZK_equals_Gprime\": ", JB(ZK = Gprime), ",\n"));
Add(outParts, Concatenation("  \"Gprime_subset_of_K\": ", JB(isGprimeInK), ",\n"));
Add(outParts, Concatenation("  \"KmodGprime_struct\": ", JStr(KmodGprimeStruct), ",\n"));
Add(outParts, Concatenation("  \"KmodGprime_is_C4\": ", JB(KmodGprimeIsC4), ",\n"));
Add(outParts, Concatenation("  \"GmodGprime_invariant_factors\": ", JArr(List(GmodGprimeInvariants, String)), ",\n"));
Add(outParts, Concatenation("  \"Syl11_order\": ", String(Size(syl11K)), ",\n"));
Add(outParts, Concatenation("  \"Syl11_normal_in_K\": ", JB(syl11Normal), ",\n"));
Add(outParts, Concatenation("  \"complement_order\": ", String(complementOrder), ",\n"));
Add(outParts, Concatenation("  \"complement_struct\": ", JStr(complementStruct), ",\n"));
Add(outParts, Concatenation("  \"complement_action_exponents_on_Syl11\": ", JArr(List(actionExponents, String)), ",\n"));
Add(outParts, Concatenation("  \"CPy_order\": ", String(Size(CPy)), ",\n"));
Add(outParts, Concatenation("  \"kerXi_order\": ", String(xiKerOrder), ",\n"));
Add(outParts, Concatenation("  \"kerXi_struct\": ", JStr(xiKerStruct), ",\n"));
Add(outParts, Concatenation("  \"kerXi_subset_of_ZK\": ", JB(IsSubset(ZK, kerXiGrp)), ",\n"));
Add(outParts, Concatenation("  \"ImXi_order\": ", String(xiImOrder), ",\n"));
Add(outParts, Concatenation("  \"ImXi_note\": ", JStr(xiImStruct), ",\n"));
Add(outParts, "  \"witness_generators\": [\n");
for i in [1 .. Length(fValsOfGens)] do
  Add(outParts, Concatenation("    {\"shadow_idx\":", String(fValsOfGens[i].idx),
      ",\"m\":", String(fValsOfGens[i].m), ",\"f_perm\":", JStr(String(fValsOfGens[i].f)), "}"));
  if i < Length(fValsOfGens) then Add(outParts, ",\n"); else Add(outParts, "\n"); fi;
od;
Add(outParts, "  ]\n");
Add(outParts, "}\n");

WriteFile("search/certs/a16_kernel_structure_20260729.json", Concatenation(outParts));
Print("\nWrote search/certs/a16_kernel_structure_20260729.json\n");
Print("A16_KERNEL_STRUCTURE_DONE\n");
