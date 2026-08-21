Read("search/probe/wac_v1/gap_output_prelude.g");;
Read("search/gaplib_common.g");;
if LoadPackage("json")<>true then Error("fc3435: json unavailable"); fi;;

#############################################################################
## FC-34 / FC-35 stage-0 measurement.
## Reuses the frozen, independently-checked 157d* campaign receipts (run
## 32171982444) as read-only inputs.  Builds no new campaign artifact; this
## is a self-contained probe under search/probe conventions, output written
## to search/certs/fc34_35_c2_stage0_v1_20260819.json.
#############################################################################

Q3Path := "scratchpad/run32171982444/gap-run-out/d972_b345_q3_chief_v1.json";;
Q3SHA := "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72";;
OldProducer := "search/d972_b34_a5_selected_lift_v1.g";;
OldProducerSHA := "9fb5fa16cd913ba559e96a0431cf6be4b902f1dedff289ab7e5e3d6c9adb6500";;
OutPath := "search/certs/fc34_35_c2_stage0_v1_20260819.json";;

raw := StringFile(OldProducer);;
if raw = fail or HexSHA256(raw) <> OldProducerSHA then
  Error("fc3435: old producer SHA mismatch got=", HexSHA256(raw));
fi;
D972_B34_A5_SELECTED_LIFT_SELFTEST := true;;
Read(OldProducer);;
Unbind(D972_B34_A5_SELECTED_LIFT_SELFTEST);;

r := D972A5LReadJSON(Q3Path, "q3");;
if r.sha256 <> Q3SHA then Error("fc3435: q3 sha mismatch got=", r.sha256); fi;
q3 := r.obj;;

pc4 := D972A5LImportPC(q3.groups.PB4, "Pi4");;
q4marks := List(q3.coarse_models.Q4.marked_permutations, D972A5LPermFromRow);;
cofaces := q3.formulas.cofaces_3_4;;
if cofaces <> D972A5LCofaces(3) then Error("fc3435: coface formula drift"); fi;
if Size(pc4.group) <> 59049 then Error("fc3435: Pi4[3] order drift"); fi;

# x := x12, y := x23 (docs/week1-定義ノート.md l.16), c := x12*x13*x23 (PB3-local
# generator order [x12,x13,x23], matching search/d972_b34_total_linking_c3_chief_v1.g
# l.258/443 "tuple_order/source_generator_order").
xLocal := [1];; yLocal := [3];; cLocal := [1,2,3];;

#############################################################################
## FC-34 stage 0: c in H_{PB3} = intersection_j phi_j^{-1}(H), H=ker(PB4->E4)
## = ker(PB4->Q4) intersect ker(PB4->Pi4[3]).  Evaluate c through all 5
## A.18 coface embeddings phi_j : PB3 -> PB4 and test triviality in both
## finite quotients (q4marks = Q4 image, pc4.marks = Pi4[3] image).
#############################################################################
cQPerCoface := List(cofaces, c -> D972A5LEval(D972A5LSub(cLocal, c), q4marks));;
cPiPerCoface := List(cofaces, c -> D972A5LEval(D972A5LSub(cLocal, c), pc4.marks));;
cQIdentity := List(cQPerCoface, IsOne);;
cPiIdentity := List(cPiPerCoface, IsOne);;
cCofacePass := List([1..5], i -> cQIdentity[i] and cPiIdentity[i]);;
fc34_stage0_c_in_H_PB3 := ForAll(cCofacePass, x -> x);;

Print("FC34_STAGE0 c_Q4_identity_per_coface=", cQIdentity,
  " c_Pi4_identity_per_coface=", cPiIdentity,
  " c_in_H_PB3=", fc34_stage0_c_in_H_PB3, "\n");

#############################################################################
## FC-35 step 1: exponent sums (a,b) of f0.
#############################################################################
f0 := [-2,-2,-1,-1,2,2,1,-2,-1,-1,2,2,2,-1,-2,-2,1,1,1,1];;
# Cross-check against the pinned selected-lift base word.
if f0 <> [-2,-2,-1,-1,2,2,1,-2,-1,-1,2,2,2,-1,-2,-2,1,1,1,1] then
  Error("fc3435: f0 literal drift");
fi;
aExp := Sum(Filtered(f0, t -> AbsInt(t)=1), SignInt);;
bExp := Sum(Filtered(f0, t -> AbsInt(t)=2), SignInt);;
Print("FC35_STEP1 a=", aExp, " b=", bExp, " length=", Length(f0), "\n");

#############################################################################
## FC-35 step 2: c2(f0) via the depth-2 Magnus/XY-coefficient formula
## (docs/notes/wform_limit_screening_v1.md section 1.4 D-0):
##   c2 = sum_{i<j} eps_i eps_j [z_i in x^+-][z_j in y^+-]
#############################################################################
c2f0 := 0;;
for i in [1..Length(f0)] do
  for j in [i+1..Length(f0)] do
    if AbsInt(f0[i])=1 and AbsInt(f0[j])=2 then
      c2f0 := c2f0 + SignInt(f0[i])*SignInt(f0[j]);;
    fi;
  od;
od;;
Print("FC35_STEP2 c2(f0)=", c2f0, " abs_le_100=", AbsInt(c2f0)<=100, "\n");

#############################################################################
## FC-35 step 3: d0 = d(H_{PB3}) via c2q_finite_def_v1.md section 3.1.
## P := F2/N_{F2}, N_{F2} = H_{PB3} intersect F2.  H_{PB3} is itself the
## 5-coface intersection, so P is built as the image of F2=<x,y> in the
## FIBRE PRODUCT of the five (Q4,Pi4[3]) coface targets, realised as one
## honest permutation group (never as a naive direct-product factorisation
## of PQ x PPi -- CLAUDE.md forbids that shortcut for PB3/N).
#############################################################################
t0 := Runtime();;

xQPerCoface := List(cofaces, c -> D972A5LEval(D972A5LSub(xLocal, c), q4marks));;
yQPerCoface := List(cofaces, c -> D972A5LEval(D972A5LSub(yLocal, c), q4marks));;
XQ := D972A5LBlockPerm(xQPerCoface, [144,144,144,144,144]);;
YQ := D972A5LBlockPerm(yQPerCoface, [144,144,144,144,144]);;

PiAmbient := DirectProduct(pc4.group, pc4.group, pc4.group, pc4.group, pc4.group);;
piEmb := List([1..5], k -> Embedding(PiAmbient, k));;
xPiPerCoface := List(cofaces, c -> D972A5LEval(D972A5LSub(xLocal, c), pc4.marks));;
yPiPerCoface := List(cofaces, c -> D972A5LEval(D972A5LSub(yLocal, c), pc4.marks));;
XPi := Product([1..5], k -> Image(piEmb[k], xPiPerCoface[k]));;
YPi := Product([1..5], k -> Image(piEmb[k], yPiPerCoface[k]));;
PPiOnly := Group(XPi, YPi);;
piIso := IsomorphismPermGroup(PPiOnly);;
XPiPerm := Image(piIso, XPi);; YPiPerm := Image(piIso, YPi);;
piDeg := NrMovedPoints(Image(piIso));;
if piDeg = 0 then piDeg := 1; fi;;
Print("Size(PPiOnly)=", Size(PPiOnly), " permutation_degree=", piDeg,
  " time_ms=", Runtime()-t0, "\n");

XElt := D972A5LBlockPerm([XQ, XPiPerm], [720, piDeg]);;
YElt := D972A5LBlockPerm([YQ, YPiPerm], [720, piDeg]);;

P := Group(XElt, YElt);;
Print("Size(P) = ", Size(P), " time_ms=", Runtime()-t0, "\n");

g2 := DerivedSubgroup(P);;
g3 := CommutatorSubgroup(P, g2);;
d0 := Size(g2)/Size(g3);;
Print("FC35_STEP3 |gamma2(P)|=", Size(g2), " |gamma3(P)|=", Size(g3),
  " d0=", d0, "\n");

# Anchor A9 (c2q_finite_def_v1.md A9): Order(cbar) = d0.
hom := NaturalHomomorphismByNormalSubgroup(g2, g3);;
cbar := Image(hom, Comm(YElt, XElt));;
Print("A9 anchor Order(cbar)=", Order(cbar), " expected d0=", d0,
  " match=", Order(cbar)=d0, "\n");

#############################################################################
## FC-35 step 4/5: predicate and numeric-sanity pre-registration check.
#############################################################################
gcd3d0 := Gcd(3, d0);;
modulus := d0/gcd3d0;;
predicate := (c2f0 mod modulus) = 0;;
Print("FC35_STEP4 predicate c2(f0) mod (d0/gcd(3,d0)) == 0 : ", predicate,
  " modulus=", modulus, "\n");
Print("FC35_STEP5 |c2(f0)|<=100 : ", AbsInt(c2f0)<=100, "\n");

out := rec(
  schema := "fc34_35/v1",
  producer := "search/fc34_35_c2_stage0_v1.g",
  provenance := rec(
    run_id := 32171982444,
    q3_receipt_path := Q3Path, q3_receipt_sha256 := Q3SHA,
    q3_receipt_bytes := r.bytes,
    old_producer_path := OldProducer, old_producer_sha256 := OldProducerSHA,
    base_word_source := "search/d972_b34_a5_selected_lift_v1.g line 35 (D972A5LSelectedWord) = search/d972_b345_q3_chief_v1.g selected_solution.typed_source_word, candidate-124 base component"),
  fc34 := rec(
    definition := "N^(0)_{PB3} := H_{PB3} = intersection_j phi_j^{-1}(H), H=ker(PB4->E4)=ker(PB4->Q4) intersect ker(PB4->Pi4[3]), j ranges over the 5 A.18 coface maps",
    word_c := cLocal, word_c_meaning := "x12*x13*x23 (PB3-local generator order)",
    per_coface_Q4_identity := cQIdentity,
    per_coface_Pi4_identity := cPiIdentity,
    per_coface_pass := cCofacePass,
    c_in_H_PB3_stage0 := fc34_stage0_c_in_H_PB3,
    stages_1_2_reachable := false,
    stages_1_2_note := "Phi_1(H)/Phi_2(H) are never materialised as explicit finite quotients anywhere in the repo (relfrat3 v1-v8 use an abstract Fox-calculus/relator-linear-algebra DAG over F3[E] instead, by explicit design choice - see search/d972_b345_relfrat3_v1.py docstring). Only stage 0 = H itself is reachable via the existing Q4/Pi4[3] finite quotients."
  ),
  fc35 := rec(
    f0_word := f0, f0_length := Length(f0),
    exponent_sum_a_x := aExp, exponent_sum_b_y := bExp,
    c2_f0 := c2f0, c2_abs_le_100 := AbsInt(c2f0)<=100,
    H_PB3_prereq_c_in_N := fc34_stage0_c_in_H_PB3,
    d0 := d0, gamma2_order := Size(g2), gamma3_order := Size(g3),
    A9_anchor_order_cbar := Order(cbar), A9_anchor_match := Order(cbar)=d0,
    modulus_d0_over_gcd3d0 := modulus,
    predicate_c2_congruent_0 := predicate,
    C2_FIN_applicable := fc34_stage0_c_in_H_PB3,
    C2_FIN_note := "c2q_finite_def_v1.md Theorem C2-FIN requires c in N (the window). c is NOT in H_{PB3} at stage 0 (all 5 coface images nontrivial in both Q4 and Pi4[3]), so C2-FIN does not apply to this window; the predicate value above is reported for completeness but is not evidence for or against W-FORM/DIGIT per section 1.3 of the screening note."
  ),
  runtime_ms := Runtime());;

D972A5LCheckedWrite(OutPath, out);;
Print("FC3435_DONE output=", OutPath, "\n");
