#############################################################################
## search/a20-kernel-structure.g -- kernel-structure capsule for W-D-A20-15a
## (裁定200 工程1)
##
## Same pattern as search/a16-kernel-structure.g, extended with
## Q_action_on_Kab (the KE-o field: Q's generators' action matrix on
## K^ab = K/[K,K]), per docs/notes/a20_prediction_v1.md S3's 8+1-field
## measurement spec. Field names below follow that spec's terminology
## exactly (group_order, ker_size, chi_image_order, Q_struct, K_struct,
## Kprime_order, Gprime_order, KmodGprime_struct, Q_action_on_Kab), plus
## the A18-4 spec's additional fields (Gprime_struct, ZK_order,
## ZK_equals_Gprime, derived_length_G, GmodGprime_invariant_factors) since
## the coordinator asked for a unified capsule covering both windows'
## field lists.
##
## Output: search/certs/a20_kernel_structure_20260729.json
#############################################################################

JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");

#############################################################################
## ---------------------- window construction (same as strike-a20.g) --------
#############################################################################
a1 := ( 1, 7)( 2,16)( 3, 5)( 4,20)( 6,17)( 8, 9)(10,15)(11,19)(12,13)(14,18);;
b1 := ( 1, 6,16)( 2,17, 5)( 3, 4,20)( 7,15, 9)(10,14,19)(11,18,13);;
A20 := AlternatingGroup(20);;
S20 := SymmetricGroup(20);;
S3 := SymmetricGroup(3);;
Dgrp := DirectProduct(A20, S3);;
embA := Embedding(Dgrp, 1);;  embS := Embedding(Dgrp, 2);;
agen := Image(embA, a1) * Image(embS, (1,3));;
bgen := Image(embA, b1) * Image(embS, (1,3,2));;
s1 := bgen^-1 * agen;;
s2 := agen^-1 * bgen^2;;
W := MakeWindow(s1, s2);;
ch := Filtered([0 .. W.Nord - 1], m -> Gcd(2*m+1, W.Nord) = 1);;

Print("=== reconstructing GTSh(N,N) for W-D-A20-15a ===\n");
corrRes := CorrectedShadows(W, ch);;
corr := corrRes.shadows;;
Print("scan_mode=", corrRes.scan_mode, " shadow_total=", Length(corr), "\n");

gi := GroupOfShadows(W, corr);;
Print("(3.53) closed=", gi.closed, "  |G|=", gi.order, "\n");
if not gi.closed then
  Error("a20-kernel-structure.g: (3.53) did not close -- refusing to report ",
        "structure of a group that was not confirmed to exist");
fi;
G := gi.G;;
K := gi.ker;;

#############################################################################
## ---------------------- basic invariants (spec fields 1,2,6,7) ------------
#############################################################################
Print("\n=== basic invariants ===\n");
GOrder := Size(G);;             # spec field 1: group_order
KOrder := Size(K);;             # spec field 2: ker_size
Gprime := DerivedSubgroup(G);;
GprimeOrder := Size(Gprime);;   # spec field 7: Gprime_order
GprimeStruct := StructureDescription(Gprime);;
Kprime := DerivedSubgroup(K);;
KprimeOrder := Size(Kprime);;   # spec field 6: Kprime_order
ZK := Center(K);;
ZKOrder := Size(ZK);;
Print("group_order=", GOrder, "  ker_size=", KOrder, "  Gprime_order=", GprimeOrder,
      "  Kprime_order=", KprimeOrder, "  Z(K)_order=", ZKOrder, "\n");
Print("K_is_abelian (IsAbelian(K))? ", IsAbelian(K), "\n");
KStruct := StructureDescription(K);;   # spec field 5: K_struct
Print("K_struct = ", KStruct, "\n");

# witness generators (matched back to explicit (m,f) shadow coordinates)
smallGensK := SmallGeneratingSet(K);;
fValsOfGens := [];;
for gk in smallGensK do
  pos := Position(gi.regs, gk);;
  if pos <> fail then
    Add(fValsOfGens, rec(idx := pos, f := corr[pos][2], m := corr[pos][1]));
  fi;
od;
Print("witness generators (", Length(fValsOfGens), "/", Length(smallGensK), " matched):\n");
for r in fValsOfGens do
  Print("  shadow_idx=", r.idx, " m=", r.m, " f=", r.f, "\n");
od;

#############################################################################
## ---------------------- chi_image_order / Q_struct (spec fields 3,4) ------
#############################################################################
Print("\n=== chi_image_order / Q_struct ===\n");
chiImageOrder := Length(Set(List(corr, k -> (2*k[1]+1) mod (2*W.Nord))));;   # spec field 3
Print("chi_image_order = ", chiImageOrder, "  (phi(2*N_ord)=", Phi(2*W.Nord), ")\n");

#############################################################################
## ---------------------- K/G' (spec field 8, P4 test) -----------------------
#############################################################################
Print("\n=== K/G' (KmodGprime_struct) ===\n");
isGprimeInK := IsSubset(K, Gprime);;
Print("G' subset of K? ", isGprimeInK, "\n");
KmodGprimeStruct := "UNDEFINED";;
KmodGprimeOrder := -1;;
if isGprimeInK then
  KmodGprime := FactorGroup(K, Gprime);;
  KmodGprimeOrder := Size(KmodGprime);;
  KmodGprimeStruct := StructureDescription(KmodGprime);;
  Print("|K/G'|=", KmodGprimeOrder, "  struct=", KmodGprimeStruct, "\n");
fi;
Print("Z(K) = G' (as subgroups)? ", ZK = Gprime, "\n");

#############################################################################
## ---------------------- G/G' invariant factors + derived_length(G) --------
#############################################################################
Print("\n=== G/G' invariant factors + derived_length(G) ===\n");
GmodGprime := FactorGroup(G, Gprime);;
GmodGprimeInvariants := AbelianInvariants(GmodGprime);;
Print("|G/G'|=", Size(GmodGprime), "  invariant factors=", GmodGprimeInvariants, "\n");
derivedLengthG := -1;;
if IsSolvable(G) then derivedLengthG := DerivedLength(G); fi;
Print("derived_length(G) = ", derivedLengthG, "\n");

#############################################################################
## ---------------------- Q_action_on_Kab (KE-o field, P4/P5 direct test) ---
## Q := G/K (abstract quotient), K^ab := K/[K,K]. Q acts on K^ab by
## conjugation (well-defined since inner automorphisms of K act trivially
## on K^ab). Computed via: lift Q's own generators to concrete elements of
## G (coset representatives), lift K^ab's generators back to K, conjugate,
## and re-project into K^ab.
#############################################################################
Print("\n=== Q_action_on_Kab ===\n");
natHomGK := NaturalHomomorphismByNormalSubgroup(G, K);;
Qgrp := Image(natHomGK);;
QOrder := Size(Qgrp);;
QStructDescr := StructureDescription(Qgrp);;
Print("|Q|=", QOrder, " struct=", QStructDescr, "\n");
qGens := GeneratorsOfGroup(Qgrp);;
qGenReps := List(qGens, q -> PreImagesRepresentative(natHomGK, q));;
qGenOrders := List(qGens, Order);;

natHomKab := NaturalHomomorphismByNormalSubgroup(K, Kprime);;
Kab := Image(natHomKab);;
KabOrder := Size(Kab);;
KabStruct := StructureDescription(Kab);;
KabInvariants := AbelianInvariants(Kab);;
Print("|K^ab|=", KabOrder, " struct=", KabStruct, " invariants=", KabInvariants, "\n");
kabGens := GeneratorsOfGroup(Kab);;
kabGenOrders := List(kabGens, Order);;
kLiftedGens := List(kabGens, kb -> PreImagesRepresentative(natHomKab, kb));;

qActionTable := [];;
for i in [1 .. Length(qGenReps)] do
  g := qGenReps[i];;
  rowImgs := [];;
  for j in [1 .. Length(kLiftedGens)] do
    kk := kLiftedGens[j];;
    conjK := g^-1 * kk * g;;
    inK := conjK in K;;
    imgKab := fail;;
    if inK then imgKab := Image(natHomKab, conjK); fi;
    Add(rowImgs, rec(kab_gen_index := j, kab_gen_order := kabGenOrders[j],
                      conj_in_K := inK, image_in_Kab := String(imgKab)));
    Print("  q_gen[", i, "] (order ", qGenOrders[i], ") * kab_gen[", j,
          "] (order ", kabGenOrders[j], ") -> conj_in_K=", inK,
          " image=", imgKab, "\n");
  od;
  Add(qActionTable, rec(q_gen_index := i, q_gen_order := qGenOrders[i], images := rowImgs));
od;

#############################################################################
## ---------------------- write JSON -------------------------------------------
#############################################################################
QActionRowJson := function(row)
  local imgsJson, k;
  imgsJson := [];
  for k in row.images do
    Add(imgsJson, Concatenation("{\"kab_gen_index\":", String(k.kab_gen_index),
        ",\"kab_gen_order\":", String(k.kab_gen_order),
        ",\"conj_in_K\":", JB(k.conj_in_K),
        ",\"image_in_Kab\":", JStr(k.image_in_Kab), "}"));
  od;
  return Concatenation("{\"q_gen_index\":", String(row.q_gen_index),
      ",\"q_gen_order\":", String(row.q_gen_order),
      ",\"images\":", JArr(imgsJson), "}");
end;;

outParts := [];;
Add(outParts, "{\n");
Add(outParts, "  \"generated_by\": \"search/a20-kernel-structure.g\",\n");
Add(outParts, "  \"note\": \"kernel-structure capsule for GTSh(W-D-A20-15a), field names per docs/notes/a20_prediction_v1.md S3; NOT a ledger claim, no cross-check performed (single implementation)\",\n");
Add(outParts, Concatenation("  \"group_order\": ", String(GOrder), ",\n"));
Add(outParts, Concatenation("  \"ker_size\": ", String(KOrder), ",\n"));
Add(outParts, Concatenation("  \"chi_image_order\": ", String(chiImageOrder), ",\n"));
Add(outParts, Concatenation("  \"Q_struct\": ", JStr(QStructDescr), ",\n"));
Add(outParts, Concatenation("  \"Q_invariant_factors\": ", JArr(List(AbelianInvariants(Qgrp), String)), ",\n"));
Add(outParts, Concatenation("  \"K_struct\": ", JStr(KStruct), ",\n"));
Add(outParts, Concatenation("  \"K_is_abelian\": ", JB(IsAbelian(K)), ",\n"));
Add(outParts, Concatenation("  \"Kprime_order\": ", String(KprimeOrder), ",\n"));
Add(outParts, Concatenation("  \"Gprime_order\": ", String(GprimeOrder), ",\n"));
Add(outParts, Concatenation("  \"Gprime_struct\": ", JStr(GprimeStruct), ",\n"));
Add(outParts, Concatenation("  \"ZK_order\": ", String(ZKOrder), ",\n"));
Add(outParts, Concatenation("  \"ZK_equals_Gprime\": ", JB(ZK = Gprime), ",\n"));
Add(outParts, Concatenation("  \"Gprime_subset_of_K\": ", JB(isGprimeInK), ",\n"));
Add(outParts, Concatenation("  \"KmodGprime_struct\": ", JStr(KmodGprimeStruct), ",\n"));
Add(outParts, Concatenation("  \"KmodGprime_order\": ", String(KmodGprimeOrder), ",\n"));
Add(outParts, Concatenation("  \"derived_length_G\": ", String(derivedLengthG), ",\n"));
Add(outParts, Concatenation("  \"GmodGprime_invariant_factors\": ", JArr(List(GmodGprimeInvariants, String)), ",\n"));
Add(outParts, Concatenation("  \"Kab_order\": ", String(KabOrder), ",\n"));
Add(outParts, Concatenation("  \"Kab_struct\": ", JStr(KabStruct), ",\n"));
Add(outParts, Concatenation("  \"Kab_invariant_factors\": ", JArr(List(KabInvariants, String)), ",\n"));
Add(outParts, "  \"Q_action_on_Kab\": [\n");
for i in [1 .. Length(qActionTable)] do
  Add(outParts, Concatenation("    ", QActionRowJson(qActionTable[i])));
  if i < Length(qActionTable) then Add(outParts, ",\n"); else Add(outParts, "\n"); fi;
od;
Add(outParts, "  ],\n");
Add(outParts, "  \"witness_generators\": [\n");
for i in [1 .. Length(fValsOfGens)] do
  Add(outParts, Concatenation("    {\"shadow_idx\":", String(fValsOfGens[i].idx),
      ",\"m\":", String(fValsOfGens[i].m), ",\"f_perm\":", JStr(String(fValsOfGens[i].f)), "}"));
  if i < Length(fValsOfGens) then Add(outParts, ",\n"); else Add(outParts, "\n"); fi;
od;
Add(outParts, "  ]\n");
Add(outParts, "}\n");

WriteFile("search/certs/a20_kernel_structure_20260729.json", Concatenation(outParts));
Print("\nWrote search/certs/a20_kernel_structure_20260729.json\n");
Print("A20_KERNEL_STRUCTURE_DONE\n");
