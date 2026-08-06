#############################################################################
## search/probe/w6_bu_s1_s3/w6_bu_s35_driver_v2_2.g
## W6BU S3.5 v2.2 repair driver -- Sol 便112 R-1 minimal repair (裁定637), laid
## ALONGSIDE v2.1 (w6_bu_s35_driver_v2_1.g and its cert are UNCHANGED; this is
## a new, parallel file, not an edit-in-place). Implements the "推奨する小修理"
## of sol/sol_reply_112_math38.md F112-1/R-1 exactly:
##   (v2.2-1) F-2.5/F-2.6 (docs/notes/bu_s35_embedding_v1.md SS8/SS7.4): replace
##       the v2.1 characteristic-polynomial similarity check (Sol: "無記帳の
##       fixture 弱化" -- similarity is NOT the fixture) with a DIRECT MATRIX
##       EQUALITY check in the explicit basis A = <tr(r,1),tr(r,2),tr(r,3)>
##       (the "MakeGn block basis" of SS7.4, i.e. the three single-block
##       5-cycles g1=(1,2,3,4,5), g2=(6,7,8,9,10), g3=(11,12,13,14,15) on the
##       15-point model -- verified equal to Amod = DerivedSubgroup(<sig1^2,
##       sig2^2>) below, not an arbitrary IsomorphismPcGroup pcgs basis).
##       Ad(g)(x) is computed as x^(g^-1) (GAP ^-operator convention; this is
##       the standard math convention Ad(g)(x)=g*x*g^-1). Declared basis =
##       "MakeGn" (native, no change-of-basis needed): checked against Theta
##       (Delta side) and d*T*d (delta side, d=diag(1,1,-1), SS7.4's boxed
##       basis-mismatch matrix). A SECOND, explicit SIMULTANEOUS change-of-
##       basis by d is then applied to BOTH Ad(Delta) and Ad(delta) (not just
##       delta) to also confirm the canon-basis equalities Ad(Delta)=Theta,
##       Ad(delta)=T directly (both bases recorded in cert; d applied
##       consistently to both generators together, per Sol's "同時
##       change-of-basis" requirement). This is a full entrywise equality
##       check over GF(5), not a characteristic-polynomial similarity check.
##   (v2.2-2) F-3.5 lane B: v2.1 only ran lane A (SolveAffine returning the
##       empty solution set) on the negative fixture. This driver adds a lane
##       B: full |V|^2 enumeration (V=F_2^2, so 4x4=16 pairs) testing L-1
##       (N_theta*a=eps_bad) AND L-2 (N_tau*b=eps_tau_bad) DIRECTLY per pair
##       (no SolveAffine/NullspaceMat call in this lane), confirming n_B=0 to
##       match n_A=0 as required by bu_s35_embedding_v1.md SS8 F-3.5 ("両方で
##       n_A=n_B=0").
##   (v2.2-3) Companion cert schema bumped to w6-bu-s35-v2.2-cert/v1; a
##       separate S3.6-only unlock manifest is written alongside (see
##       search/certs/w6_bu_s35_v2_2_s36_unlock_manifest_20260806.json).
## v2.1 driver/cert files are UNCHANGED by this file. The original v2.1
## header (below) is retained verbatim for provenance.
##
## ==== ORIGINAL v2.1 HEADER (unchanged, retained for provenance) ====
## W6BU S3.5 v2.1 repair driver -- falsifier judgment repair (裁定615), laid
## ALONGSIDE v2 (w6_bu_s35_driver_v2.g and its certs are UNCHANGED; this is a
## new, parallel file, not an edit-in-place). The six repair items:
##   (2) shard_provenance.self_sha256 fixed to be each shard JSON's OWN
##       hash (merge script side, not this driver).
##   (3) The 7 literal `true` booleans in the v2 cert (F_1_all_pass,
##       F_2_1_sigma1sq_eq_x, F_2_2_sigma2sq_eq_y, size_Phat_eq_3000_times_V,
##       piE_U0_eq_theta_and_piE_W0_eq_tau,
##       order_Uhat0_times_What0_matches_or_doubles_Ghat5_reference,
##       F_3_5_negative_fixture_pass) are now REAL measured booleans: F-1/
##       F-2.1/F-2.2/F-3.5 Chk() return values are captured (v1's own
##       "f2_1 := Chk(...)" pattern, which v2 had dropped); the three
##       phat_construction sanity checks are now asserted INSIDE
##       BuildPhatForClass on every single class build (not just eyeballed
##       once) and AND-reduced into one boolean per check across all 73
##       accepted classes.
##   (4) A check roster + total is added: CHECK_NAMES accumulates every
##       Chk() call's name (pass or fail), CHECK_TOTAL = Length(CHECK_NAMES)
##       -- fails_total now has an explicit denominator in the cert.
##   (5) Chk() is fail-SOFT (records failure, keeps running) -- this is
##       UNCHANGED from v2/v1, but is now explicitly disclosed in the cert
##       (see "check_semantics" block) rather than left implicit. Rationale
##       for keeping fail-soft (not hardening to fail-fast): a hard stop on
##       the first Chk failure, mid-row, would discard the already-computed
##       per-class L-3 data for all classes processed so far in that GAP
##       process and force a full shard re-run to get ANY data back; the
##       FAILS list + cert's own fails_total=0 gate already gives a
##       fail-CLOSED verdict at the cert-consumption layer (checker/compare
##       scripts refuse to grade a cert with fails_total != 0), so no
##       unsound PASS can leak through a fail-soft internal run. Reported to
##       司令塔 as the choice actually taken; open to being overruled.
##   (6) Fixture naming is unified via an explicit doc<->cert name map
##       (see "fixture_naming_map" in the cert) rather than by renaming
##       either side and risking silently breaking the other consumer.
##   SM-1 disclosure (added to L3_zero_disclosure): L-3 as computed is BLIND
##       to which of the 4 non-equivalent marked-lift windows (EMB-H1, 5
##       classes, 4 surjective + 1 trivial, all sharing one kernel up to a
##       scalar automorphism) a given (a,b) pair sits in -- marking-ness
##       itself is guaranteed by the L-1/L-2 conditions and the F-2 external
##       anchor fixtures (MakeGn(5) x,y byte-identity), NOT by L-3. L-3 only
##       measures surjectivity onto Phat; it does not re-verify marking.
##
## Original v2 header (裁定594 / Sol F110-2.5 minimal reclaim bundle 1-2):
##   (1) L-3 (full surjectivity onto Phat = V.Ghat5, NOT just onto the
##       S4-level extension E_S4) evaluated on ALL 1,263 affine solution
##       pairs across the 73 affine-solvable classes.
##   (2) Versioned v2 cert with SEPARATE count fields:
##         extension_classes=449, affine_solution_pairs=1263,
##         L3_surjective_lifts=<measured>, MARK-ISO_orbits=<measured>
##       plus explicit disclosure that the linear solver never physically
##       traverses the full 91,809-pair domain.
##   (3) D+D lane B extended to include L-3 (all 4 classes); explicit scope
##       statement that lane A/B cross-check is D+D-only (4 classes).
##   (4) F-2.5/F-2.6 computed for real (not "not computed"); F-3.5
##       affine-unsolvable negative fixture executed.
##
## THIS IS A NEW FILE. search/probe/w6_bu_s1_s3/w6_bu_s35_driver.g (v1) and
## its certs (search/certs/w6_bu_s35_firing_20260806.json,
## w6_bu_s35_math_detail_20260806.json) are UNCHANGED.
##
## Design authority for the Phat construction (fiber product
## Ghat5 x_{S4} E_S4, realized as an explicitly-generated subgroup of
## DirectProduct(Ghat5,E_S4) -- NOT full-domain enumeration): confirmed with
## 司令塔 (this session) as the standard "inflated extension" pullback,
## forced by VCEN-MOD (V inflated through Ghat5 -> S4). Validated at scale
## on the D+D row (p2_d4_a0b0c2, all 4 classes, 256 pairs) before this full
## 17-row run: Size(Phat)=3000*|V| every time; order(Uhat0*What0) in Phat
## matches order(Delta*delta) in Ghat5 for the split class and is exactly
## double for non-split classes (structural non-split detector, matches
## expectation) -- see scratchpad/test_phat_dd_4classes.g.
##
## KNOWN SLOW-STEP AVOIDANCE: NaturalHomomorphismByNormalSubgroup(Phat,Vhat)
## was empirically observed to hang (>5 min wall, no result) for a degree
## ~15+24|V| permutation group of order 3000|V|. We never call it. Instead:
## Phat's V-copy normality is asserted via IsNormal (cheap); the "does the
## quotient look like Ghat5" check is done via plain element orders
## (Order(Uhat0), Order(What0), Order(Uhat0*What0) vs the Ghat5-level
## reference), which only needs cycle-length computation on permutations.
## Surjectivity itself (L-3) uses Subgroup(Phat,[rho1,rho2]) + Size, which
## IS fast (Schreier-Sims on a moderate-degree perm group) -- this was
## already the exact operation used successfully in the v1 driver's D+D
## brute force block, just now compared against |Phat| instead of |E_S4|.
##
## Non-contact: Im R untouched, d_N unevaluated, 3 sealed quantities
## untouched. No isolated=TRUE/FALSE, kill, EMPTY, or candidate-found claim
## written anywhere. S3.6 and beyond untouched.
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
LoadPackage("cohomolo");;

FAILS := [];;
CHECK_NAMES := [];;    ## v2.1 item (4): roster of every Chk() call, pass or fail
Chk := function(name, got, want)
  local ok;
  ok := (got = want);
  Add(CHECK_NAMES, name);;
  if not ok then Add(FAILS, rec(name := name, got := String(got), want := String(want))); fi;
  Print("  [", PF(ok), "] ", name, ": got=", got, " want=", want, "\n");
  return ok;
end;;

#############################################################################
## PART A -- Ghat5 (15-point model, verbatim from bu_s35_embedding_v1.md SS6.2
## / v1 driver), plus the quotient map p_G: Ghat5 -> S4grp used to build Phat.
#############################################################################
Print("\n=== PART A: Ghat5, F-1, F-2 (external anchor) ===\n");
sig1 := (1,4,2,5,3)(6,11)(7,12,10,15)(8,13,9,14);;
sig2 := (1,12,2,11)(3,15,5,13)(4,14)(6,9,7,10,8);;
DeltaHat := sig1*sig2*sig1;;
deltaHat := sig1*sig2;;
Ghat5 := Group(sig1, sig2);;

f11 := Chk("F-1.1: order(Delta)", Order(DeltaHat), 2);;
f12 := Chk("F-1.2: order(delta)", Order(deltaHat), 3);;
f13 := Chk("F-1.3: braid", sig1*sig2*sig1 = sig2*sig1*sig2, true);;
f14 := Chk("F-1.4: Delta^2=1", DeltaHat^2 = (), true);;
f15 := Chk("F-1.5: |Ghat5|", Size(Ghat5), 3000);;
F1_ALL_PASS := f11 and f12 and f13 and f14 and f15;;   ## v2.1 item (3): real, not hardcoded

g5anchor := MakeGn(5);;
F21_PASS := Chk("F-2.1: sigma1^2 = MakeGn(5).x", sig1^2 = g5anchor.x, true);;
F22_PASS := Chk("F-2.2: sigma2^2 = MakeGn(5).y", sig2^2 = g5anchor.y, true);;

S4grp := Group((1,2),(1,3,4));;
theta := (1,2);; tau := (1,3,4);;
FS4 := FreeGroup(2);;
FqS4 := FS4 / [FS4.1^2, FS4.2^3, (FS4.1*FS4.2)^4];;

G5loc := Group(sig1^2, sig2^2);;
Amod := DerivedSubgroup(G5loc);;
Chk("A: |Amod|", Size(Amod), 125);;
Chk("A: IsNormal(Ghat5,Amod)", IsNormal(Ghat5,Amod), true);;

quoGhat5 := NaturalHomomorphismByNormalSubgroup(Ghat5, Amod);;
Sbar := Image(quoGhat5);;
Chk("A: |Ghat5/Amod|", Size(Sbar), 24);;
thetaImg := Image(quoGhat5, DeltaHat);; tauImg := Image(quoGhat5, deltaHat);;
isoSbarToS4 := GroupHomomorphismByImages(Sbar, S4grp, [thetaImg,tauImg], [theta,tau]);;
Chk("A: isoSbarToS4 well-defined", isoSbarToS4 = fail, false);;
p_G := CompositionMapping(isoSbarToS4, quoGhat5);;
Chk("A: p_G(Delta)=theta", Image(p_G,DeltaHat), theta);;
Chk("A: p_G(delta)=tau", Image(p_G,deltaHat), tau);;

## ---- F-2.5/F-2.6 (v2.2 REPAIR): DIRECT MATRIX EQUALITY in the explicit
## "MakeGn block basis" A = <tr(r,1),tr(r,2),tr(r,3)> (bu_s35_embedding_v1.md
## SS7.4/SS8), with an explicit SIMULTANEOUS change-of-basis to the canon
## basis also checked. NOT a characteristic-polynomial similarity check
## (Sol 便112 R-1: charpoly-only was ruled a "無記帳の fixture 弱化").
##
## Block-basis generators: single-block 5-cycles on the 15-point model
## (same point layout as MakeGn(5): block i = points (i-1)*5+1..i*5).
g1 := (1,2,3,4,5);;
g2 := (6,7,8,9,10);;
g3 := (11,12,13,14,15);;
Chk("v2.2: g1 in Amod", g1 in Amod, true);;
Chk("v2.2: g2 in Amod", g2 in Amod, true);;
Chk("v2.2: g3 in Amod", g3 in Amod, true);;
BlockBasisGrp := Group(g1,g2,g3);;
Chk("v2.2: Group(g1,g2,g3) = Amod (block basis spans A exactly)", BlockBasisGrp = Amod, true);;

## CoordA(h): decompose h = g1^e1*g2^e2*g3^e3 (unique since g1,g2,g3 commute
## with pairwise-disjoint support) by reading the image of each block's
## point-1 representative. Valid for any h in Group(g1,g2,g3) = Amod
## (checked above).
CoordA := function(h)
  local e1, e2, e3;
  e1 := (1^h - 1) mod 5;
  e2 := (6^h - 6) mod 5;
  e3 := (11^h - 11) mod 5;
  return [e1,e2,e3] * Z(5)^0;
end;;

## Ad(g)(x) := g*x*g^-1 (standard math convention). GAP's ^-operator is
## right-conjugation (x^g = g^-1*x*g), so Ad(g)(x) = x^(g^-1) in GAP syntax.
## AdMatrix column j = CoordA(Ad(g)(gens[j])); GAP matrices are row-major
## (mat*vec convention), so AdMatrix = TransposedMat(list-of-columns).
AdMatrixBlockBasis := function(g)
  local cols;
  cols := List([g1,g2,g3], gi -> CoordA(gi^(g^-1)));;
  return TransposedMat(cols);
end;;

AdDeltaBlock := AdMatrixBlockBasis(DeltaHat);;
AdDeltaTauBlock := AdMatrixBlockBasis(deltaHat);;
Print("Ad(Delta)|_A (MakeGn block basis) = ", AdDeltaBlock, "\n");
Print("Ad(delta)|_A (MakeGn block basis) = ", AdDeltaTauBlock, "\n");

## canon (4.7)/(4.8) matrices (bu_s35_embedding_v1.md SS1) and the SS7.4
## basis-mismatch matrix d = diag(1,1,-1).
ThetaCanon := [[0,1,0],[1,0,0],[0,0,-1]]*Z(5)^0;;
TCanon := [[0,0,1],[1,0,0],[0,1,0]]*Z(5)^0;;
DBasisChange := [[1,0,0],[0,1,0],[0,0,-1]]*Z(5)^0;;   ## d = diag(1,1,-1)

## MakeGn-basis check (native, no change-of-basis): Ad(Delta)=Theta, Ad(delta)=d.T.d
dTd := DBasisChange * TCanon * DBasisChange;;
f25_makegn_pass := (AdDeltaBlock = ThetaCanon);;
f26_makegn_pass := (AdDeltaTauBlock = dTd);;
Chk("F-2.5 (MakeGn basis): Ad(Delta)|_A = Theta EXACTLY", f25_makegn_pass, true);;
Chk("F-2.6 (MakeGn basis): Ad(delta)|_A = d.T.d EXACTLY (d=diag(1,1,-1))", f26_makegn_pass, true);;

## canon-basis check: apply the SAME change-of-basis d SIMULTANEOUSLY to
## both Ad(Delta) and Ad(delta) (Sol 便112 R-1: "同時 change-of-basis を明示").
AdDeltaCanon := DBasisChange * AdDeltaBlock * DBasisChange;;
AdDeltaTauCanon := DBasisChange * AdDeltaTauBlock * DBasisChange;;
f25_canon_pass := (AdDeltaCanon = ThetaCanon);;
f26_canon_pass := (AdDeltaTauCanon = TCanon);;
Chk("F-2.5 (canon basis, via simultaneous d-conjugation): Ad(Delta)|_A = Theta EXACTLY", f25_canon_pass, true);;
Chk("F-2.6 (canon basis, via simultaneous d-conjugation): Ad(delta)|_A = T EXACTLY", f26_canon_pass, true);;

f25_pass := f25_makegn_pass and f25_canon_pass;;
f26_pass := f26_makegn_pass and f26_canon_pass;;
f25_basis := (function() if f25_pass then return "EXACT match to Theta in BOTH MakeGn (native) and canon (via explicit simultaneous d-conjugation, d=diag(1,1,-1)) bases -- direct entrywise equality, not charpoly similarity"; else return "MISMATCH"; fi; end)();;
f26_basis := (function() if f26_pass then return "EXACT match: d.T.d in MakeGn (native) basis, T in canon (via explicit simultaneous d-conjugation) basis -- direct entrywise equality, not charpoly similarity"; else return "MISMATCH"; fi; end)();;
Print("F-2.5 basis match: ", f25_basis, "\n");
Print("F-2.6 basis match: ", f26_basis, "\n");

#############################################################################
## PART B -- shared S4 module-building setup (verbatim from v1 driver)
#############################################################################
V4norm := Filtered(NormalSubgroups(S4grp), n -> Size(n) = 4)[1];;
quoS3 := NaturalHomomorphismByNormalSubgroup(S4grp, V4norm);;
S3q := Image(quoS3);;
gl22 := GL(2,2);;
isoS3toGL22 := IsomorphismGroups(S3q, gl22);;

triv_a := [[Z(2)^0]];; triv_b := [[Z(2)^0]];;
reg2_a := [[Z(2)^0,Z(2)^0],[0*Z(2),Z(2)^0]];;
reg2_b := IdentityMat(2,GF(2));;
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

BuildVCenModuleP2 := function(a,b,c)
  local matsA, matsB, i, ma, mb;
  matsA := [];; matsB := [];;
  for i in [1..a] do Add(matsA, triv_a); Add(matsB, triv_b); od;
  for i in [1..b] do Add(matsA, reg2_a); Add(matsB, reg2_b); od;
  for i in [1..c] do Add(matsA, D_a); Add(matsB, D_b); od;
  return rec(ma := BlockDiag(matsA), mb := BlockDiag(matsB));
end;;

gl23 := GL(2,3);;
eltsGL23 := Elements(gl23);;
homsP3 := [];;
for aElt in eltsGL23 do
  if aElt^2 = aElt^0 then
    for bElt in eltsGL23 do
      if bElt^3 = bElt^0 then
        if (aElt*bElt)^2 = (aElt*bElt)^0 then Add(homsP3, [aElt,bElt]); fi;
      fi;
    od;
  fi;
od;
repsP3 := [];;
for pr in homsP3 do
  found := false;;
  for g in eltsGL23 do
    for rp in repsP3 do
      if pr[1]^g = rp[1] and pr[2]^g = rp[2] then found := true; break; fi;
    od;
    if found then break; fi;
  od;
  if not found then Add(repsP3, pr); fi;
od;

ParseP2Triple := function(modId)
  local aPos, bPos, cPos, aStr, bStr, cStr;
  aPos := PositionSublist(modId, "_a") + 2;
  bPos := PositionSublist(modId, "b");
  cPos := PositionSublist(modId, "c");
  aStr := modId{[aPos .. bPos-1]};
  bStr := modId{[bPos+1 .. cPos-1]};
  cStr := modId{[cPos+1 .. Length(modId)]};
  return [Int(aStr), Int(bStr), Int(cStr)];
end;;
ParseP3Index := function(modId)
  local parts;
  parts := SplitString(modId, "_");
  return Int(parts[Length(parts)]);
end;;

RowIds := [
  "p2_d2_a0b0c1", "p2_d2_a0b1c0", "p2_d2_a2b0c0",
  "p2_d3_a1b0c1", "p2_d3_a1b1c0", "p2_d3_a3b0c0",
  "p2_d4_a0b0c2", "p2_d4_a0b1c1", "p2_d4_a0b2c0",
  "p2_d4_a2b0c1", "p2_d4_a2b1c0", "p2_d4_a4b0c0",
  "p3_d2_bruteforce_1", "p3_d2_bruteforce_2", "p3_d2_bruteforce_3",
  "p3_d2_bruteforce_4", "p3_d2_bruteforce_5"
];;
## Shard support (gaplib_common.g convention: split when a run risks the 600s
## wall-clock cap). Set V2_ROW_SUBSET (a list of module_ids) and
## V2_OUT_SUFFIX (a string) BEFORE Read()-ing this file to run only a subset
## and write to a shard-specific output path; a merge script combines the
## shard JSONs afterwards. Default (unset) = full 17-row run, default path.
if not IsBound(V2_ROW_SUBSET) then V2_ROW_SUBSET := RowIds; fi;
if not IsBound(V2_OUT_SUFFIX) then V2_OUT_SUFFIX := ""; fi;
ProcessOrder := Filtered(Concatenation(["p2_d4_a0b0c2"], Filtered(RowIds, r -> r <> "p2_d4_a0b0c2")),
    r -> r in V2_ROW_SUBSET);;

#############################################################################
## PART C -- helpers: affine solve, vector->Vsub element, Phat builder, L-3
#############################################################################
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

## Builds Phat = Ghat5 x_{S4} E_S4 (fiber product, realized as an explicitly
## generated subgroup of DirectProduct(Ghat5,Epc) -- no ambient-domain
## enumeration) for a given (chr,vec) class. Returns a record with Phat,
## Uhat0, What0, Vgens (as Epc elements), emb2 (embedding Epc -> D), and
## sizePhat, plus the diagnostic order(Uhat0*What0).
## v2.1 item (3): this function now ALSO builds piE (Epc -> S4grp, the
## projection killed by v2 -- v2's "piE_U0_eq_theta_and_piE_W0_eq_tau":true
## was a hardcoded literal with piE never even constructed in the
## production driver, only in the throwaway test script. Fixed here: piE is
## built and both projection checks are actually run, every single class.
## Three global accumulators (SIZE_PHAT_CHECK_ALL, PIE_CHECK_ALL,
## ORDER_CHECK_ALL, defined further down before the main loop) are
## AND-reduced across all calls.
BuildPhatForClass := function(chr, vec, dim, pPrime)
  local Eext, isoE, Epc, EGpc, U0, W0, Vgens, Vsub, D, emb1, emb2,
        PhatGens, Phat, Uhat0, What0, quoE, S4viaE, isoS4viaEtoS4, piE,
        sizeOk, pieOk, refOrder, prodOrder, orderOk;
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

  ## piE: Epc -> S4grp (kill the V-subgroup, then identify the quotient with
  ## S4grp via the two chosen generator images) -- the actual, real check.
  quoE := NaturalHomomorphismByNormalSubgroup(Epc, Vsub);;
  S4viaE := Image(quoE);;
  isoS4viaEtoS4 := GroupHomomorphismByImages(S4viaE, S4grp, [Image(quoE,U0),Image(quoE,W0)], [theta,tau]);;
  piE := CompositionMapping(isoS4viaEtoS4, quoE);;
  pieOk := (Image(piE,U0) = theta) and (Image(piE,W0) = tau);;

  D := DirectProduct(Ghat5, Epc);;
  emb1 := Embedding(D,1);; emb2 := Embedding(D,2);;
  PhatGens := Concatenation(
    List(GeneratorsOfGroup(Amod), a -> Image(emb1,a)),
    List(GeneratorsOfGroup(Vsub), v -> Image(emb2,v)),
    [ Image(emb1,DeltaHat) * Image(emb2,U0),
      Image(emb1,deltaHat) * Image(emb2,W0) ]
  );;
  Phat := Subgroup(D, PhatGens);;
  Uhat0 := Image(emb1,DeltaHat) * Image(emb2,U0);;
  What0 := Image(emb1,deltaHat) * Image(emb2,W0);;

  sizeOk := (Size(Phat) = 3000 * pPrime^dim);;
  refOrder := Order(DeltaHat*deltaHat);;
  prodOrder := Order(Uhat0*What0);;
  orderOk := (prodOrder = refOrder) or (prodOrder = 2*refOrder);;

  SIZE_PHAT_CHECK_ALL := SIZE_PHAT_CHECK_ALL and sizeOk;;
  PIE_CHECK_ALL := PIE_CHECK_ALL and pieOk;;
  ORDER_CHECK_ALL := ORDER_CHECK_ALL and orderOk;;
  Add(CHECK_NAMES, Concatenation("phat-build size=3000*|V|: vec=",String(vec)));;
  Add(CHECK_NAMES, Concatenation("phat-build piE(U0)=theta,piE(W0)=tau: vec=",String(vec)));;
  Add(CHECK_NAMES, Concatenation("phat-build order(Uhat0*What0) matches/doubles ref: vec=",String(vec)));;
  if not sizeOk then Add(FAILS, rec(name:=Concatenation("phat-build size vec=",String(vec)), got:=String(Size(Phat)), want:=String(3000*pPrime^dim))); fi;
  if not pieOk then Add(FAILS, rec(name:=Concatenation("phat-build piE vec=",String(vec)), got:="false", want:="true")); fi;
  if not orderOk then Add(FAILS, rec(name:=Concatenation("phat-build order vec=",String(vec)), got:=String(prodOrder), want:=Concatenation(String(refOrder)," or ",String(2*refOrder)))); fi;

  return rec(Phat := Phat, sizePhat := Size(Phat), Uhat0 := Uhat0, What0 := What0,
             Vgens := Vgens, emb2 := emb2, orderProd := prodOrder,
             sizeOk := sizeOk, pieOk := pieOk, orderOk := orderOk);
end;;

#############################################################################
## PART D -- main loop over 17 rows: EMB-LIN (lane A) + per-pair L-3
#############################################################################
RowDetail := rec();;
ClassWitnesses := [];;
TotalClasses := 0;; AcceptedClasses := 0;; RejectedClasses := 0;;
TotalAffinePairs := 0;; TotalL3Surjective := 0;; TotalMarkIsoOrbits := 0;;

## v2.1 item (3): global AND-accumulators for the 3 phat_construction sanity
## checks, updated inside BuildPhatForClass on EVERY accepted-class build in
## THIS shard (73 classes total across the full 3-shard run; whichever
## subset this shard processes). true only if it held for every build seen
## in this process.
SIZE_PHAT_CHECK_ALL := true;;
PIE_CHECK_ALL := true;;
ORDER_CHECK_ALL := true;;

DD_LaneB_L3 := [];;   ## D+D row: lane B per-class L-3 surjective counts

for modId in ProcessOrder do
  Print("\n=== S3.5 v2: ", modId, " ===\n");
  if modId{[1,2]} = "p2" then
    trip := ParseP2Triple(modId);;
    built := BuildVCenModuleP2(trip[1],trip[2],trip[3]);;
    maR := built.ma;; mbR := built.mb;; pPrime := 2;; dim := Length(maR);;
  else
    idx := ParseP3Index(modId);;
    rp := repsP3[idx];;
    maR := rp[1];; mbR := rp[2];; pPrime := 3;; dim := Length(maR);;
  fi;

  chr := CHR(S4grp, pPrime, FqS4, [maR, mbR]);;
  h2 := SecondCohomologyDimension(chr);;
  Cohomolo(chr, false, true, false, Concatenation("scratchpad/.tmp_s35v2_",modId));;
  Chk(Concatenation(modId,": codim2 = SecondCohomologyDimension"), chr.codim2, h2);;

  Ntheta := maR + IdentityMat(dim, GF(pPrime));;
  Ntau := IdentityMat(dim, GF(pPrime)) + mbR + mbR^2;;

  classVecs := [];;
  if h2 = 0 then Add(classVecs, []);
  else classVecs := Cartesian(List([1..h2], ii -> [0..pPrime-1]));; fi;

  rowAccepted := 0;; rowRejected := 0;; rowPairs := 0;; rowL3 := 0;; rowMarkIso := 0;;
  rowClassRecs := [];;

  for vec in classVecs do
    epsDelta := List([1..dim], j -> (Sum([1..h2], k -> vec[k]*chr.modrelvals[k][1][j])) mod pPrime) * Z(pPrime)^0;;
    epsDelta := epsDelta * (-Z(pPrime)^0);;
    epsTau := List([1..dim], j -> (Sum([1..h2], k -> vec[k]*chr.modrelvals[k][2][j])) mod pPrime) * Z(pPrime)^0;;
    epsTau := epsTau * (-Z(pPrime)^0);;
    solsA := SolveAffine(Ntheta, epsDelta, pPrime);;
    solsB := SolveAffine(Ntau, epsTau, pPrime);;
    laneA := Length(solsA) * Length(solsB);;
    TotalClasses := TotalClasses + 1;;

    if laneA = 0 then
      RejectedClasses := RejectedClasses + 1;; rowRejected := rowRejected + 1;;
      Add(ClassWitnesses, rec(
        traversal_id := Concatenation(modId, "_s35v2_class_vec_", JoinC(List(vec,String),"-")),
        disposition := "REJECTED", source_tag := "S3_5_V2_EMB_LIN"));;
      Add(rowClassRecs, rec(vec := vec, laneA := laneA, l3_surjective := 0,
          sizePhat := fail, sizeH_distribution := rec()));;
    else
      AcceptedClasses := AcceptedClasses + 1;; rowAccepted := rowAccepted + 1;;
      TotalAffinePairs := TotalAffinePairs + laneA;; rowPairs := rowPairs + laneA;;

      pb := BuildPhatForClass(chr, vec, dim, pPrime);;

      classSurjPairs := [];;   ## list of [aVec,bVec] that pass L-3
      sizeHTally := rec();;    ## 診断欄(②): |<rho(sigma1),rho(sigma2))>| の
                                ## 実測分布 -- 0 の理由を紙で追えるようにする
                                ## (司令塔 続行承認メッセージの防壁②)
      for aVec in solsA do
        for bVec in solsB do
          aElt := VecToElt(aVec, pb.Vgens, dim);; bElt := VecToElt(bVec, pb.Vgens, dim);;
          UhatA := pb.Uhat0 * Image(pb.emb2,aElt);;
          WhatB := pb.What0 * Image(pb.emb2,bElt);;
          rho1 := WhatB^-1 * UhatA;;
          rho2 := UhatA^-1 * WhatB^2;;
          Hp := Subgroup(pb.Phat,[rho1,rho2]);;
          sizeHkey := String(Size(Hp));;
          if IsBound(sizeHTally.(sizeHkey)) then
            sizeHTally.(sizeHkey) := sizeHTally.(sizeHkey) + 1;
          else
            sizeHTally.(sizeHkey) := 1;
          fi;
          if Size(Hp) = pb.sizePhat then
            Add(classSurjPairs, [aVec,bVec]);
          fi;
        od;
      od;
      rowL3 := rowL3 + Length(classSurjPairs);; TotalL3Surjective := TotalL3Surjective + Length(classSurjPairs);;
      Print("    class vec=",vec," sizePhat=",pb.sizePhat," |H| distribution=",
            List(RecNames(sizeHTally), k -> Concatenation(k,":",String(sizeHTally.(k)))), "\n");

      ## MARK-ISO orbits (w6_bottomup_design_v3.md SS1.1): among the L-3
      ## surjective pairs of THIS class, two lifts (a,b),(a',b') are
      ## MARK-ISO-equivalent iff related by V-conjugation (the B^1
      ## coboundary of EMB-H1, same shape, now for module V instead of A):
      ## gamma in V acts by (a,b) -> (a+(I-theta)gamma, b+(I-tau)gamma).
      if Length(classSurjPairs) > 0 then
        gammaOrbitReps := [];;
        seen := [];;
        for pr in classSurjPairs do
          key := Concatenation(String(pr[1]),"|",String(pr[2]));;
          if not (key in seen) then
            orbit := [];;
            for gammaCombo in Cartesian(List([1..dim], ii -> [0..pPrime-1])) do
              gammaVec := gammaCombo * Z(pPrime)^0;;
              aShift := pr[1] + (IdentityMat(dim,GF(pPrime)) - maR) * gammaVec;;
              bShift := pr[2] + (IdentityMat(dim,GF(pPrime)) - mbR) * gammaVec;;
              Add(orbit, Concatenation(String(aShift),"|",String(bShift)));
            od;
            for k in orbit do AddSet(seen, k); od;
            Add(gammaOrbitReps, key);;
          fi;
        od;
        rowMarkIso := rowMarkIso + Length(gammaOrbitReps);;
        TotalMarkIsoOrbits := TotalMarkIsoOrbits + Length(gammaOrbitReps);;
      fi;

      Add(ClassWitnesses, rec(
        traversal_id := Concatenation(modId, "_s35v2_class_vec_", JoinC(List(vec,String),"-")),
        disposition := "ACCEPTED", source_tag := "S3_5_V2_EMB_LIN"));;

      if modId = "p2_d4_a0b0c2" then
        Add(DD_LaneB_L3, rec(vec := vec, laneA := laneA, l3_surjective := Length(classSurjPairs),
            sizePhat := pb.sizePhat, sizeH_distribution := StructuralCopy(sizeHTally)));;
      fi;
      Add(rowClassRecs, rec(vec := vec, laneA := laneA, l3_surjective := Length(classSurjPairs),
          sizePhat := pb.sizePhat, sizeH_distribution := StructuralCopy(sizeHTally)));;
    fi;
  od;

  Print("  ", modId, ": classes=", Length(classVecs), " accepted=", rowAccepted,
        " rejected=", rowRejected, " affine_pairs=", rowPairs, " L3_surjective=", rowL3,
        " MARK-ISO_orbits=", rowMarkIso, "\n");
  RowDetail.(modId) := rec(p := pPrime, dim := dim, dim_H2_S4 := h2,
      num_classes := Length(classVecs), accepted := rowAccepted, rejected := rowRejected,
      affine_pairs := rowPairs, l3_surjective := rowL3, mark_iso_orbits := rowMarkIso,
      class_detail := rowClassRecs);;
od;

Print("\n=== TOTALS ===\n");
Print("TotalClasses=", TotalClasses, " AcceptedClasses=", AcceptedClasses,
      " RejectedClasses=", RejectedClasses, "\n");
Print("TotalAffinePairs=", TotalAffinePairs, "\n");
Print("TotalL3Surjective=", TotalL3Surjective, "\n");
Print("TotalMarkIsoOrbits=", TotalMarkIsoOrbits, "\n");
IS_FULL_RUN := (Length(V2_ROW_SUBSET) = Length(RowIds) and ForAll(RowIds, r -> r in V2_ROW_SUBSET));;
if IS_FULL_RUN then
  Chk("extension_classes = 449", TotalClasses, 449);;
  Chk("affine_solvable_classes = 73", AcceptedClasses, 73);;
  Chk("affine_unsolvable_classes = 376", RejectedClasses, 376);;
  Chk("affine_solution_pairs = 1263", TotalAffinePairs, 1263);;
else
  Print("[SHARD RUN] denominator invariants (449/73/376/1263) only checked on full merged run, not per-shard\n");
fi;

#############################################################################
## PART E -- F-3.5 affine-unsolvable negative fixture (synthetic eps outside
## im(N_theta), on a small hand-built module -- independent of the 17 rows)
#############################################################################
Print("\n=== F-3.5: affine-unsolvable negative fixture ===\n");
## dim=2, p=2 module where theta acts as identity (so N_theta = 0 matrix,
## image = {0}) and we pick eps=(1,0) which is NOT in im(N_theta)={0}.
ma_neg := IdentityMat(2, GF(2));;
Ntheta_neg := ma_neg + IdentityMat(2, GF(2));;   ## = zero matrix
epsBad := [Z(2)^0, 0*Z(2)];;                      ## (1,0), not in image {0}
solsBad := SolveAffine(Ntheta_neg, epsBad, 2);;
f351 := Chk("F-3.5: SolveAffine returns 0 solutions for eps not in im(N_theta)", Length(solsBad), 0);;
f352 := Chk("F-3.5: reports 'no solution' cleanly (not fail/error)", solsBad = [], true);;

## v2.2 REPAIR: lane B (F-3.2, |V|^2 exhaustive enumeration) for THIS SAME
## negative fixture -- v2.1 only ran lane A (SolveAffine) here. bu_s35_
## embedding_v1.md SS8 F-3.5's frozen expectation is n_A=n_B=0 on BOTH
## lanes, not lane A alone. tau-side module chosen deliberately SOLVABLE
## (mb_neg=Identity, Ntau_neg=I+I+I=I mod 2=I, epsTauBad=(0,0) so b=(0,0)
## solves it) so the AND-enumeration genuinely exercises both halves of the
## pair and the n_B=0 result is driven by the theta-side unsolvability
## alone, not by a vacuous tau side.
mb_neg := IdentityMat(2, GF(2));;
Ntau_neg := IdentityMat(2,GF(2)) + mb_neg + mb_neg^2;;   ## = I+I+I = I (mod 2)
epsTauBad := [0*Z(2), 0*Z(2)];;                            ## (0,0), IS in image (b=(0,0))
solsBadTau := SolveAffine(Ntau_neg, epsTauBad, 2);;
Chk("F-3.5 lane B setup: tau-side IS solvable (n_A_tau>0, so the AND-test below is non-vacuous)", Length(solsBadTau) > 0, true);;

AllVecsF2Dim2 := Cartesian([0..1],[0..1]);;   ## |V|=4 for dim=2,p=2
laneB_matches := 0;;
for avv in AllVecsF2Dim2 do
  aVecTest := [avv[1],avv[2]] * Z(2)^0;;
  for bvv in AllVecsF2Dim2 do
    bVecTest := [bvv[1],bvv[2]] * Z(2)^0;;
    if (Ntheta_neg * aVecTest = epsBad) and (Ntau_neg * bVecTest = epsTauBad) then
      laneB_matches := laneB_matches + 1;;
    fi;
  od;
od;
Chk("F-3.5 lane B: |V|^2=16 exhaustive pair enumeration (direct matrix test, no SolveAffine) count", laneB_matches, 0);;

f353 := Chk("F-3.5 lane A: n_A = |solsBad(theta)| x |solsBadTau(tau)| = 0", Length(solsBad) * Length(solsBadTau), 0);;
f354 := Chk("F-3.5: n_A = n_B (both lanes agree at 0)", (Length(solsBad) * Length(solsBadTau)) = laneB_matches, true);;
F35_PASS := f351 and f352 and f353 and f354 and (laneB_matches = 0);;   ## v2.2: now covers BOTH lanes

#############################################################################
## PART F -- write v2 companion report (schema NOT the frozen
## w6-bu-firing-cert/v1; a new versioned, self-documenting report)
#############################################################################
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_w6bu_s35v2_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then Error("sha256 fail for ", relpath); fi;
  return line{[1 .. 64]};
end;;

## 診断欄(②): |<rho(sigma1),rho(sigma2))>| の分布を rec -> JSON object へ
SizeHTallyToJson := function(tally)
  local keys;
  keys := RecNames(tally);
  if Length(keys) = 0 then return "{}"; fi;
  return Concatenation("{", JoinC(List(keys, k ->
      Concatenation(JStr(k), ":", String(tally.(k)))), ","), "}");
end;;

ClassDetailToJson := function(classRecs)
  return JArr(List(classRecs, function(cr)
    return Concatenation("{\"vec\":", JArr(List(cr.vec,String)),
      ",\"lane_a_count\":", String(cr.laneA),
      ",\"L3_surjective\":", String(cr.l3_surjective),
      ",\"sizePhat\":", (function() if cr.sizePhat = fail then return "null"; else return String(cr.sizePhat); fi; end)(),
      ",\"sizeH_distribution\":", SizeHTallyToJson(cr.sizeH_distribution),
      "}");
  end));
end;;

RowDetailJson := JoinC(List(ProcessOrder, function(modId)
  local r;
  r := RowDetail.(modId);
  return Concatenation("{\"module_id\":", JStr(modId),
    ",\"p\":", String(r.p), ",\"dim\":", String(r.dim),
    ",\"dim_H2_S4\":", String(r.dim_H2_S4),
    ",\"num_classes\":", String(r.num_classes),
    ",\"accepted_classes\":", String(r.accepted),
    ",\"rejected_classes\":", String(r.rejected),
    ",\"affine_solution_pairs\":", String(r.affine_pairs),
    ",\"L3_surjective_lifts\":", String(r.l3_surjective),
    ",\"MARK_ISO_orbits\":", String(r.mark_iso_orbits),
    ",\"class_detail\":", ClassDetailToJson(r.class_detail),
    "}");
end), ",");;

selfSha := ComputeSha256File("search/probe/w6_bu_s1_s3/w6_bu_s35_driver_v2_2.g");;

report := Concatenation(
"{\n",
"\"schema\":\"w6-bu-s35-v2.2-cert/v1\",\n",
"\"note\":\"NOT the frozen w6-bu-firing-cert/v1 schema. v2.2: Sol 便112 F112-1/R-1 minimal repair (裁定637), laid ALONGSIDE v2.1 (v2.1 driver/cert UNCHANGED). Implements the '推奨する小修理' verbatim: (1) F-2.5/F-2.6 as DIRECT MATRIX EQUALITY in the explicit MakeGn block basis (native) PLUS the canon basis via an explicit SIMULTANEOUS change-of-basis d=diag(1,1,-1) applied to both Ad(Delta) and Ad(delta) together -- NOT a characteristic-polynomial similarity check as in v2/v2.1. (2) F-3.5 lane B: full |V|^2=16 exhaustive pair enumeration (direct matrix test, no SolveAffine) added alongside lane A, confirming n_A=n_B=0 on the negative fixture. See driver header for full item list.\",\n",
"\"design_doc\":\"docs/notes/bu_s35_embedding_v1.md\",\n",
"\"authorization\":\"裁定637 (司令塔), implementing sol/sol_reply_112_math38.md F112-1/R-1 '推奨する小修理' verbatim, this file\",\n",
"\"driver_self_sha256\":", JStr(selfSha), ",\n",
"\"driver_self_sha256_note\":\"sha256 of THIS driver script (w6_bu_s35_driver_v2_2.g) -- identical across all shards run from the same driver file; do not confuse with the per-SHARD-OUTPUT hash, which the merge script computes separately\",\n",
"\"counts_v2\":{\n",
"  \"extension_classes\":", String(TotalClasses), ",\n",
"  \"affine_solvable_classes\":", String(AcceptedClasses), ",\n",
"  \"affine_unsolvable_classes\":", String(RejectedClasses), ",\n",
"  \"affine_solution_pairs\":", String(TotalAffinePairs), ",\n",
"  \"L3_surjective_lifts\":", String(TotalL3Surjective), ",\n",
"  \"MARK_ISO_orbits\":", String(TotalMarkIsoOrbits), ",\n",
"  \"full_v_squared_pair_domain\":91809,\n",
"  \"unit_definitions\":{\n",
"    \"extension_classes\":\"H^2(S4,V) cohomology classes across all 17 V-cen rows (= v1 traversed_count)\",\n",
"    \"affine_solvable_classes\":\"extension classes for which the L-1/L-2 (EMB-LIN) affine system has a nonempty solution set (= v1 accepted_count)\",\n",
"    \"affine_solution_pairs\":\"total (a,b) pairs across all affine-solvable classes solving N_theta(a)=-eps_Delta and N_tau(b)=-eps_delta (L-1/L-2 only, NOT yet L-3)\",\n",
"    \"L3_surjective_lifts\":\"subset of affine_solution_pairs for which the FULL marked lift rho(sigma_1)=W^-1 U, rho(sigma_2)=U^-1 W^2 (built in Phat = the actual V-extension of Ghat5, order 3000*|V|, via fiber product over S4) generates all of Phat -- i.e. L-1 AND L-2 AND L-3 all hold\",\n",
"    \"MARK_ISO_orbits\":\"number of MARK-ISO equivalence classes (w6_bottomup_design_v3.md SS1.1, base-fixed on Ghat5) among the L3_surjective_lifts pairs, computed as orbits of the V-conjugation coboundary action (a,b)->(a+(I-theta)gamma,b+(I-tau)gamma) for gamma in V, restricted per class to its L-3-surjective subset\",\n",
"    \"full_v_squared_pair_domain\":\"|V|^2 summed appropriately would be the naive brute-force domain size for L-1/L-2 alone; 91809 is the value already established in the companion detail (v1) as the total naive-pair domain across all 449 classes. THE LINEAR SOLVER (SolveAffine, EMB-LIN) NEVER PHYSICALLY TRAVERSES THIS DOMAIN -- it computes affine solution sets directly via NullspaceMat/SolutionMat. traversed_count in the frozen v1 schema equals extension_classes (449), NOT this domain size; this field is carried here only for cross-reference disclosure, per F110-2.5(b)'s explicit request.\"\n",
"  }\n",
"},\n",
"\"phat_construction\":{\n",
"  \"method\":\"fiber product Ghat5 x_S4 E_S4, realized as an explicitly-generated subgroup of DirectProduct(Ghat5,E_S4) (generators: Amod, V-subgroup of E_S4, and the two diagonal lifts (Delta,U0),(delta,W0)) -- no enumeration of the ~10^6-order ambient direct product\",\n",
"  \"sanity_checks_passed\":{\n",
"    \"size_Phat_eq_3000_times_V\":", JB(SIZE_PHAT_CHECK_ALL), ",\n",
"    \"piE_U0_eq_theta_and_piE_W0_eq_tau\":", JB(PIE_CHECK_ALL), ",\n",
"    \"order_Uhat0_times_What0_matches_or_doubles_Ghat5_reference\":", JB(ORDER_CHECK_ALL), ",\n",
"    \"note\":\"v2.1 fix (item 3): these 3 booleans are now the AND-reduction of a REAL check executed inside BuildPhatForClass on EVERY accepted-class build processed by THIS shard (not a single hand-eyeballed instance, and not a hardcoded literal as in v2). piE (Epc -> S4grp) is now actually constructed here -- v2 never built it in the production driver at all, only in the throwaway test script; v2's identical claim was unfounded.\"\n",
"  },\n",
"  \"known_slow_step_avoided\":\"NaturalHomomorphismByNormalSubgroup(Phat,Vhat) hangs (>5min, no result) for these group sizes; replaced by direct element-order checks (Order is O(permutation degree) via cycle decomposition, no coset enumeration needed)\"\n",
"},\n",
"\"f_fixtures\":{\n",
"  \"F_1_all_pass\":", JB(F1_ALL_PASS), ",\n",
"  \"F_2_1_sigma1sq_eq_x\":", JB(F21_PASS), ",\"F_2_2_sigma2sq_eq_y\":", JB(F22_PASS), ",\n",
"  \"F_2_5_F_2_6_v2_2_method\":\"DIRECT MATRIX EQUALITY over GF(5), explicit basis, NOT charpoly similarity (v2.1's method). Basis A = <g1,g2,g3> = <tr(r,1),tr(r,2),tr(r,3)> (single-block 5-cycles on the 15-point model), verified = Amod exactly (v2.2_block_basis_eq_Amod below). Ad(g)(x):=g*x*g^-1 (standard math convention), computed in GAP as x^(g^-1).\",\n",
"  \"v2_2_block_basis_eq_Amod\":", JB(BlockBasisGrp = Amod), ",\n",
"  \"v2_2_declared_basis_native\":\"MakeGn\",\n",
"  \"v2_2_Ad_Delta_MakeGn_basis\":", JArr(List(AdDeltaBlock, r -> JArr(List(r, x -> String(IntFFE(x)))))), ",\n",
"  \"v2_2_Ad_delta_MakeGn_basis\":", JArr(List(AdDeltaTauBlock, r -> JArr(List(r, x -> String(IntFFE(x)))))), ",\n",
"  \"v2_2_Theta_canon\":", JArr(List(ThetaCanon, r -> JArr(List(r, x -> String(IntFFE(x)))))), ",\n",
"  \"v2_2_T_canon\":", JArr(List(TCanon, r -> JArr(List(r, x -> String(IntFFE(x)))))), ",\n",
"  \"v2_2_d_basis_change\":", JArr(List(DBasisChange, r -> JArr(List(r, x -> String(IntFFE(x)))))), ",\n",
"  \"v2_2_dTd_MakeGn_expected\":", JArr(List(dTd, r -> JArr(List(r, x -> String(IntFFE(x)))))), ",\n",
"  \"v2_2_Ad_Delta_canon_basis_via_simultaneous_d\":", JArr(List(AdDeltaCanon, r -> JArr(List(r, x -> String(IntFFE(x)))))), ",\n",
"  \"v2_2_Ad_delta_canon_basis_via_simultaneous_d\":", JArr(List(AdDeltaTauCanon, r -> JArr(List(r, x -> String(IntFFE(x)))))), ",\n",
"  \"F_2_5_makegn_basis_pass\":", JB(f25_makegn_pass), ",\"F_2_6_makegn_basis_pass\":", JB(f26_makegn_pass), ",\n",
"  \"F_2_5_canon_basis_pass\":", JB(f25_canon_pass), ",\"F_2_6_canon_basis_pass\":", JB(f26_canon_pass), ",\n",
"  \"F_2_5_ad_Delta_basis_match\":", JStr(f25_basis), ",\n",
"  \"F_2_6_ad_delta_basis_match\":", JStr(f26_basis), ",\n",
"  \"F_2_5_pass\":", JB(f25_pass), ",\"F_2_6_pass\":", JB(f26_pass), ",\n",
"  \"F_3_5_negative_fixture_pass\":", JB(F35_PASS), ",\n",
"  \"F_3_5_v2_2_lane_b_pairs_matched\":", String(laneB_matches), ",\n",
"  \"F_3_5_v2_2_lane_a_count\":", String(Length(solsBad) * Length(solsBadTau)), ",\n",
"  \"F_3_5_v2_2_note\":\"v2.1 only executed lane A (SolveAffine emptiness) on this negative fixture. v2.2 adds lane B: full |V|^2=16 exhaustive pair enumeration testing L-1 AND L-2 directly per pair (no SolveAffine call in this lane), matching bu_s35_embedding_v1.md SS8 F-3.5's frozen expectation n_A=n_B=0 on BOTH lanes. tau-side chosen solvable so the AND-test is non-vacuous; the theta side alone drives n=0.\",\n",
"  \"fixture_naming_map\":{\n",
"    \"note\":\"v2.1 fix (item 6): explicit doc(hyphen-dot)<->cert(underscore) name map, so a reader never has to guess the correspondence.\",\n",
"    \"F-1.1\":\"contributes to F_1_all_pass (order(Delta)=2)\",\n",
"    \"F-1.2\":\"contributes to F_1_all_pass (order(delta)=3)\",\n",
"    \"F-1.3\":\"contributes to F_1_all_pass (braid relation)\",\n",
"    \"F-1.4\":\"contributes to F_1_all_pass (Delta^2=1)\",\n",
"    \"F-1.5\":\"contributes to F_1_all_pass (|Ghat5|=3000)\",\n",
"    \"F-2.1\":\"F_2_1_sigma1sq_eq_x\",\n",
"    \"F-2.2\":\"F_2_2_sigma2sq_eq_y\",\n",
"    \"F-2.5\":\"F_2_5_pass (basis note in F_2_5_ad_Delta_basis_match)\",\n",
"    \"F-2.6\":\"F_2_6_pass (basis note in F_2_6_ad_delta_basis_match)\",\n",
"    \"F-3.5\":\"F_3_5_negative_fixture_pass\"\n",
"  }\n",
"},\n",
"\"check_semantics\":{\n",
"  \"note\":\"v2.1 items (4)+(5): Chk() is FAIL-SOFT (records a failure into FAILS and keeps running; does not stop the GAP process). This is UNCHANGED from v1/v2 -- disclosed explicitly here rather than left implicit, per 裁定615. Soundness is instead enforced at the cert-CONSUMPTION layer: fails_total below is the fail-CLOSED gate (a cert with fails_total != 0 must be refused by any checker/compare script), so a fail-soft internal run cannot leak an unsound PASS.\",\n",
"  \"checks_executed_total\":", String(Length(CHECK_NAMES)), ",\n",
"  \"checks_executed_names\":", JArr(List(CHECK_NAMES, JStr)), ",\n",
"  \"fails_total_denominator\":\"fails_total (below) is out of checks_executed_total (above); fails_total=0 required for cert to be usable\"\n",
"},\n",
"\"lane_a_lane_b_dpd_only\":{\n",
"  \"scope_statement\":\"lane A / lane B cross-check (real-group brute force) is executed ON THE D+D ROW (p2_d4_a0b0c2) ONLY -- 4 classes. The other 16 rows use EMB-LIN formula (lane A) only; L-3 for those 16 rows is computed via the same Phat-fiber-product construction as D+D (not a separate brute force lane), so it is single-lane for L-3 on those 16 rows exactly as L-1/L-2 already was in v1.\",\n",
"  \"dpd_classes\":", JArr(List(DD_LaneB_L3, r -> Concatenation(
      "{\"vec\":", JArr(List(r.vec,String)), ",\"lane_a_count\":", String(r.laneA),
      ",\"l3_surjective\":", String(r.l3_surjective),
      ",\"sizePhat\":", String(r.sizePhat),
      ",\"sizeH_distribution\":", SizeHTallyToJson(r.sizeH_distribution), "}"))), "\n",
"},\n",
"\"rows\":[", RowDetailJson, "],\n",
"\"L3_zero_disclosure\":{\n",
"  \"note\":\"THIS IS NOT AN EMPTY/IMPOSSIBILITY CLAIM. L3_surjective_lifts is recorded as a raw measurement (inventory register), per the negative-result registration regime (solver-candidate-philosophy: negative claims require the registration regime, not casual assertion). If the measured total is 0 across all 449 classes, that is flagged below for mandatory mathematical review -- it is NOT asserted here to mean 'no marked lift can ever be surjective onto Phat' as a theorem.\",\n",
"  \"needs_mathematical_review\":", JB(TotalL3Surjective = 0), ",\n",
"  \"review_tag\":\"【要数学検分】\",\n",
"  \"candidate_theorem_note\":\"IF L3_surjective_lifts=0 holds across all 17 rows/449 classes, one candidate explanation (raised by 司令塔, NOT proven here, NOT claimed as a theorem) is a factorization argument: since rho(c)=1 forces rho to factor through B3/<c> = C2*C3 (EMB-C/EMB-BRAID, bu_s35_embedding_v1.md SS2-3), the image <rho(sigma1),rho(sigma2)> = <U,W> with U^2=W^3=1 might be constrained to only ever reach the Ghat5-part plus the specific V-submodule generated by the cocycle values (eps_Delta,eps_delta) themselves, never the full V -- i.e. L-1/L-2 solutions might be structurally incapable of also satisfying L-3 for these particular (V-cen, S3-inflated) module types. If borne out, this would return the L-3 satisfiability question itself to Sol as a design question (is L-3 vacuous on this whole layer, and if so what does that mean for S3.6/ISO-GATE), not merely a computational non-finding. The per-class |H|-distribution diagnostic (see rows[].class_detail[].sizeH_distribution and lane_a_lane_b_dpd_only.dpd_classes[].sizeH_distribution above) is the raw evidence for/against this candidate explanation -- it shows exactly which proper subgroup order(s) of Phat the marked-lift image actually reaches.\",\n",
"  \"SM_1\":\"L-3 as computed here is BLIND to which marked-lift window a given (a,b) pair sits in. Definition MARK-ISO (w6_bottomup_design_v3.md SS1.1) shows the marked lifts of q (base-fixed) fall into H^1(C2*C3,A) ~= F_5 = 5 classes, 4 of which are surjective onto Ghat5 and all share ONE kernel (related by a scalar automorphism, EMB-H1 in bu_s35_embedding_v1.md SS5.1) -- i.e. which of the 4 you land in is not itself part of what makes rho a valid marked lift. L-3 (this report) only tests surjectivity of <rho(sigma1),rho(sigma2)> onto Phat; it does NOT re-derive or re-verify marking. Marking-ness is guaranteed upstream by (a) L-1/L-2 (rho(c)=1, braid, both checked before any Phat/L-3 machinery runs) and (b) the F-2 external-anchor fixtures (MakeGn(5).x,.y byte-identity, F-2.1/F-2.2 above), which are the D-1 trap detector per bu_s35_embedding_v1.md SS7.3. A reader must not read a positive L3_surjective_lifts count as also having independently reconfirmed marking -- that reconfirmation is F-2's job, not L-3's.\"\n",
"},\n",
"\"claims\":{\"isolated_verdict\":\"UNKNOWN\",\"kill_claim\":false,\"candidate_found\":false,\"empty_claim\":false},\n",
"\"non_contact_declaration\":{\"exploration\":false,\"candidate_generation\":false,\"kill\":false,\"empty_theorem\":false,\"im_R\":false,\"d_N\":false,\"sealed_quantities\":false,\"S9\":false},\n",
"\"fails_total\":", String(Length(FAILS)), ",\n",
"\"fails\":", JArr(List(FAILS, f -> Concatenation("{\"name\":", JStr(f.name),
    ",\"got\":", JStr(f.got), ",\"want\":", JStr(f.want), "}"))), "\n",
"}\n");;

OUT_PATH := Concatenation("search/certs/w6_bu_s35_v2_2_20260806", V2_OUT_SUFFIX, ".json");;
WriteFile(OUT_PATH, report);;
Print("Wrote ", OUT_PATH, "\n");
Print("\nFAILS = ", Length(FAILS), "\n");
for fitem in FAILS do
  Print("   ", fitem.name, " got=", fitem.got, " want=", fitem.want, "\n");
od;
Print("\nW6_BU_S35_V2_DRIVER_DONE\n");
QUIT;
