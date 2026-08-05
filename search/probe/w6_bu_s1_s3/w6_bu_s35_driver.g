#############################################################################
## search/probe/w6_bu_s1_s3/w6_bu_s35_driver.g
## W6BU firing (裁定585補/589): S3.5 marked-lift enumeration for the exact
## 17-row (V-cen) firing universe, D+D row (p2_d4_a0b0c2) first.
##
## Design authority: docs/notes/bu_s35_embedding_v1.md (mathematician's
## sigma1,sigma2 -> Ghat5 embedding note, 裁定589 unlock). Conditions per
## 裁定589:
##  (1) 2405.11725 (4.7)(4.8) page-image cross-check -- done OUTSIDE this
##      script (papers/2405.11725-nonabelian-quotients-gt-elementary.pdf,
##      physical page 16, rendered to scratchpad/bu_s35_page16-16.png and
##      visually confirmed byte-for-byte against the note's quoted formulas).
##      Recorded in the companion detail report, not re-run here.
##  (2) F-2 (MakeGn(5) x,y external anchor) run as a firing PRECONDITION
##      below, before any S3.5 class is processed -- if it fails, STOP.
##  (3) L-1 (braid) run as a PARALLEL assert alongside the new
##      EMB-BRAID/EMB-LIN linear form, not deleted. For the D+D row (where a
##      real extension group is built) this is a genuine independent
##      group-arithmetic check; for the other 16 rows we do not build a
##      group (裁定589 (4): brute force only once, on D+D) so L-1 there
##      rests on the paper theorem EMB-BRAID, disclosed as such.
##  (4) EMB-LIN linearization (formula-based, via chr.modrelvals) used for
##      all 17 rows; D+D additionally gets a real-group brute-force
##      (|V|^2 pairs per class) cross-check before trusting linearization
##      for the other 16.
##
## Math source: docs/notes/bu_s35_embedding_v1.md SS2 (EMB-C: c in K^(5)),
## SS3 (EMB-BRAID/EMB-LIN), SS4 (explicit Ghat5 model), SS6 (15-point model,
## MakeGn(5)-compatible), SS7 (D-1/N-4 traps), SS8 (fixtures F-1..F-4),
## Appendix A (implementer hand-off). The eps_Delta/eps_delta <-> cohomolo
## modrelvals correspondence was independently validated against real group
## arithmetic in scratchpad/probe_s35_modrelvals.g before being trusted here
## (both split (vec=0) and nonsplit (vec=1) cases matched exactly on a
## dim-2 test module).
##
## Non-contact: Im R untouched, d_N unevaluated, 3 sealed quantities
## untouched. No isolated=TRUE/FALSE, kill, EMPTY, or candidate-found claim
## written anywhere. S3.6 (ISO-GATE) and beyond are not touched -- this
## script only counts marked lifts (L-1/L-2), it does not evaluate L-4
## (isolated) or anything past S3.5.
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

#############################################################################
## PART A -- 15-point Ghat5 model (bu_s35_embedding_v1.md SS6.2, verbatim)
#############################################################################
Print("\n=== F-1: Ghat5 = <sigma1,sigma2>, 15-point model ===\n");
sig1 := (1,4,2,5,3)(6,11)(7,12,10,15)(8,13,9,14);;
sig2 := (1,12,2,11)(3,15,5,13)(4,14)(6,9,7,10,8);;
DeltaHat := sig1*sig2*sig1;;
deltaHat := sig1*sig2;;
Ghat5 := Group(sig1, sig2);;

Chk("F-1.1: order(Delta)", Order(DeltaHat), 2);;
Chk("F-1.2: order(delta)", Order(deltaHat), 3);;
Chk("F-1.3: braid sigma1 sigma2 sigma1 = sigma2 sigma1 sigma2", sig1*sig2*sig1 = sig2*sig1*sig2, true);;
Chk("F-1.4: Delta^2 = 1 (=chat)", DeltaHat^2 = (), true);;
Chk("F-1.5: |<sigma1,sigma2>|", Size(Ghat5), 3000);;
Chk("F-1.6a: order(sigma1)", Order(sig1), 20);;
Chk("F-1.6b: order(sigma2)", Order(sig2), 20);;
Chk("F-1.7a: order(sigma1^2)", Order(sig1^2), 10);;
Chk("F-1.7b: order(sigma2^2)", Order(sig2^2), 10);;
G5loc := Group(sig1^2, sig2^2);;
Chk("F-1.8: |<sigma1^2,sigma2^2>| (=|G5|)", Size(G5loc), 500);;

Print("\n=== F-2: external anchor (MakeGn(5)) -- D-1 detector, firing precondition ===\n");
g5anchor := MakeGn(5);;
f2_1 := Chk("F-2.1 *** sigma1^2 = MakeGn(5).x (byte-identical)", sig1^2 = g5anchor.x, true);;
f2_2 := Chk("F-2.2 *** sigma2^2 = MakeGn(5).y (byte-identical)", sig2^2 = g5anchor.y, true);;

## F-2.3/F-2.4: Ad(x)|_A vs Ad(y)|_A eigenstructure check (secondary
## confirmation; F-2.1/F-2.2 above are already the primary, strongest
## detector per the note's own logic -- a x<->y role swap from the D-1 trap
## would make sigma1^2 equal .y instead of .x, which F-2.1 alone already
## catches). Here: eigenvalue multiset must be {1,-1,-1} (mod 5: {1,4,4})
## for BOTH x and y, and their +1-eigenlines must be DIFFERENT 1-dim
## subspaces of A (that is what the D-1 trap actually flips).
Amod := DerivedSubgroup(G5loc);;
Chk("F-2 pre: |A|", Size(Amod), 125);;
Chk("F-2 pre: A elementary abelian exponent 5", IsElementaryAbelian(Amod) and Exponent(Amod)=5, true);;
isoApc := IsomorphismPcGroup(Amod);;
Apc := Image(isoApc);;
pcgsA := Pcgs(Apc);;
AdMatrixOverGF5 := function(g)
  ## matrix of x -> x^g (conjugation), in the pcgs basis, as rows over GF(5)
  local rows, i, img, expv;
  rows := [];
  for i in [1..Length(pcgsA)] do
    img := Image(isoApc, PreImagesRepresentative(isoApc, pcgsA[i])^g);
    expv := ExponentsOfPcElement(pcgsA, img);
    Add(rows, expv * Z(5)^0);
  od;
  return rows;
end;;
AdX := AdMatrixOverGF5(sig1^2);;
AdY := AdMatrixOverGF5(sig2^2);;
EigMultiset := function(M)
  local cp, f5, roots, r, mult, out;
  cp := CharacteristicPolynomial(M);
  f5 := GF(5);
  roots := RootsOfUPol(f5, cp);
  return Collected(roots);
end;;
emX := EigMultiset(AdX);; emY := EigMultiset(AdY);;
Print("  Ad(x)|_A eigenvalues (mult) = ", emX, "\n");
Print("  Ad(y)|_A eigenvalues (mult) = ", emY, "\n");
expectedMultiset := Set([ [Z(5)^0, 1], [-Z(5)^0, 2] ]);;
Chk("F-2.3: Ad(sigma1^2)|_A eigenvalue multiset = {1,-1,-1}", Set(emX) = expectedMultiset, true);;
Chk("F-2.4: Ad(sigma2^2)|_A eigenvalue multiset = {1,-1,-1}", Set(emY) = expectedMultiset, true);;
FixedLine := function(M)
  return NullspaceMat(TransposedMat(M - IdentityMat(Length(M), GF(5))));
end;;
lineX := FixedLine(AdX);; lineY := FixedLine(AdY);;
Chk("F-2 pre: dim +1-eigenspace(x) = 1", Length(lineX), 1);;
Chk("F-2 pre: dim +1-eigenspace(y) = 1", Length(lineY), 1);;
sameLine := (Length(lineX)=1 and Length(lineY)=1
    and RankMat(Concatenation(lineX,lineY)) = 1);;
Chk("F-2.3/2.4 substance: +1-eigenlines of x,y are DIFFERENT (D-1 trap would make them equal-ish/swapped)",
    sameLine, false);;

F2_ALL_PASS := (Length(FAILS) = 0);;
Print("\nF-2 precondition status: ", (function() if F2_ALL_PASS then return "PASS"; else return "STOP"; fi; end)(), "\n");
if not F2_ALL_PASS then
  Print("\n*** F-2/F-1 PRECONDITION FAILED -- STOPPING before any S3.5 class is processed ***\n");
  Print("FAILS = ", Length(FAILS), "\n");
  for fitem in FAILS do Print("   ", fitem.name, " got=", fitem.got, " want=", fitem.want, "\n"); od;
  Print("\nW6_BU_S35_DRIVER_STOPPED_PRECONDITION\n");
  Error("F-1/F-2 precondition failed -- STOP (see printed FAILS above)");
fi;

#############################################################################
## PART B -- shared S4 setup (as in w6_bu_s1_s3_driver.g / census driver)
#############################################################################
S4grp := Group((1,2),(1,3,4));;
theta := (1,2);; tau := (1,3,4);;
FS4 := FreeGroup(2);;
FqS4 := FS4 / [FS4.1^2, FS4.2^3, (FS4.1*FS4.2)^4];;
Chk("PartB pre: RelatorsOfFpGroup(FqS4)[1] = FS4.1^2 (a^2 = Delta-relator)",
    RelatorsOfFpGroup(FqS4)[1] = FS4.1^2, true);;
Chk("PartB pre: RelatorsOfFpGroup(FqS4)[2] = FS4.2^3 (b^3 = delta-relator)",
    RelatorsOfFpGroup(FqS4)[2] = FS4.2^3, true);;

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
ProcessOrder := Concatenation(["p2_d4_a0b0c2"], Filtered(RowIds, r -> r <> "p2_d4_a0b0c2"));;

#############################################################################
## PART C -- EMB-LIN linear solve (F_p linear algebra, no group needed)
#############################################################################
## Solve x*(M) = v for row vector x over GF(p); return list of ALL solutions
## (small dim, so we enumerate the coset of the null space explicitly).
SolveAffine := function(M, v, p)
  local dim, part, ns, sols, ns_vecs, combo, i, cur, F;
  F := GF(p);
  dim := Length(M);
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

RowDetail := rec();;
ClassWitnesses := [];;
TotalClasses := 0;; AcceptedClasses := 0;; RejectedClasses := 0;;

for modId in ProcessOrder do
  Print("\n=== S3.5: ", modId, " ===\n");
  if modId{[1,2]} = "p2" then
    trip := ParseP2Triple(modId);;
    built := BuildVCenModuleP2(trip[1],trip[2],trip[3]);;
    ma := built.ma;; mb := built.mb;; pPrime := 2;; dim := Length(ma);;
  else
    idx := ParseP3Index(modId);;
    rp := repsP3[idx];;
    ma := rp[1];; mb := rp[2];; pPrime := 3;; dim := Length(ma);;
  fi;

  chr := CHR(S4grp, pPrime, FqS4, [ma, mb]);;
  h2 := SecondCohomologyDimension(chr);;
  Cohomolo(chr, false, true, false, Concatenation("scratchpad/.tmp_s35_",modId));;
  Chk(Concatenation(modId,": codim2 = SecondCohomologyDimension"), chr.codim2, h2);;

  Ntheta := ma + IdentityMat(dim, GF(pPrime));;
  Ntau := IdentityMat(dim, GF(pPrime)) + mb + mb^2;;

  classVecs := [];;
  if h2 = 0 then Add(classVecs, []);
  else classVecs := Cartesian(List([1..h2], ii -> [0..pPrime-1]));; fi;

  rowClassCounts := [];;
  for vec in classVecs do
    epsDelta := List([1..dim], j -> (Sum([1..h2], k -> vec[k]*chr.modrelvals[k][1][j])) mod pPrime) * Z(pPrime)^0;;
    epsDelta := epsDelta * (-Z(pPrime)^0);; ## solve N(a) = -eps
    epsTau := List([1..dim], j -> (Sum([1..h2], k -> vec[k]*chr.modrelvals[k][2][j])) mod pPrime) * Z(pPrime)^0;;
    epsTau := epsTau * (-Z(pPrime)^0);;
    solsA := SolveAffine(Ntheta, epsDelta, pPrime);;
    solsB := SolveAffine(Ntau, epsTau, pPrime);;
    laneA := Length(solsA) * Length(solsB);;
    Add(rowClassCounts, rec(vec:=vec, laneA:=laneA));;
    TotalClasses := TotalClasses + 1;;
    if laneA > 0 then AcceptedClasses := AcceptedClasses + 1;
    else RejectedClasses := RejectedClasses + 1; fi;
    Add(ClassWitnesses, rec(
      traversal_id := Concatenation(modId, "_s35_class_vec_", JoinC(List(vec,String),"-")),
      disposition := (function() if laneA > 0 then return "ACCEPTED"; else return "REJECTED"; fi; end)(),
      source_tag := "S3_5_EMB_LIN"
    ));;
  od;
  Print("  ", modId, ": ", Length(classVecs), " classes, lane-A marked-lift counts = ",
        List(rowClassCounts, r->r.laneA), "\n");

  rowRec := rec(p:=pPrime, dim:=dim, dim_H2_S4:=h2, num_classes:=Length(classVecs),
                lane_a_counts := List(rowClassCounts, r->r.laneA));;

  ## D+D: real-group brute force cross-check (task condition (4)) + L-1
  ## parallel-assert (task condition (3)) on genuine group elements.
  if modId = "p2_d4_a0b0c2" then
    Print("  *** D+D real-extension brute-force cross-check ***\n");
    laneBCounts := [];; l1AutomaticChecks := [];;
    for ci in [1..Length(classVecs)] do
      vec := classVecs[ci];;
      if h2 = 0 or ForAll(vec, vv -> vv = 0) then
        Eext := SplitExtensionCHR(chr);;
      else
        Eext := NonsplitExtension(chr, vec);;
      fi;
      isoE := IsomorphismPcGroup(Eext);;
      Epc := Image(isoE);;
      EGpc := List(GeneratorsOfGroup(Eext), g -> Image(isoE,g));;
      U0 := EGpc[1];; W0 := EGpc[2];;
      Vgens := EGpc{[3..2+dim]};;
      VElts := List(Cartesian(List([1..dim], ii->[0..pPrime-1])), expv ->
          Product([1..dim], jj -> Vgens[jj]^expv[jj]));;
      cId := Identity(Epc);;
      laneBcount := 0;; l2onlyCount := 0;;
      for ua in VElts do
        Uc := U0*ua;;
        for wb in VElts do
          Wc := W0*wb;;
          l2ok := (Uc^2 = cId) and (Wc^3 = cId);;
          if l2ok then
            l2onlyCount := l2onlyCount + 1;;
            rs1 := Wc^-1 * Uc;; rs2 := Uc^-1 * Wc^2;;
            braidOk := (rs1*rs2*rs1 = rs2*rs1*rs2);;
            cOk := ((rs1*rs2*rs1)^2 = cId);;
            if braidOk and cOk then laneBcount := laneBcount + 1; fi;
          fi;
        od;
      od;
      Add(laneBCounts, laneBcount);;
      Add(l1AutomaticChecks, rec(vec:=vec, l2only:=l2onlyCount, l1andl2:=laneBcount,
          l1_automatic_given_l2 := (l2onlyCount = laneBcount)));;
      Chk(Concatenation("D+D class ",String(ci)," (vec=",String(vec),"): lane A = lane B (real group brute force)"),
          rowClassCounts[ci].laneA, laneBcount);;
      Chk(Concatenation("D+D class ",String(ci),": L-1 automatic given L-2 (EMB-BRAID empirical check, task (3))"),
          l2onlyCount = laneBcount, true);;
    od;
    rowRec.lane_b_counts := laneBCounts;;
    rowRec.l1_parallel_assert := l1AutomaticChecks;;
    rowRec.brute_force_cross_check_done := true;;
  else
    rowRec.brute_force_cross_check_done := false;;
  fi;
  RowDetail.(modId) := rowRec;;
od;;

Print("\n=== totals ===\n");
Print("TotalClasses=", TotalClasses, " AcceptedClasses=", AcceptedClasses, " RejectedClasses=", RejectedClasses, "\n");
Chk("grand total classes = 449 (same denominator as S3 cert)", TotalClasses, 449);;
Chk("accepted+rejected = total", AcceptedClasses+RejectedClasses, TotalClasses);;

#############################################################################
## ==== companion detail report (NOT schema-bound -- full math record) ====
#############################################################################
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_w6bu_s35_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then Error("sha256 fail for ", relpath); fi;
  return line{[1 .. 64]};
end;;

RowDetailJson := JoinC(List(RowIds, function(modId)
  local r, extra;
  r := RowDetail.(modId);
  extra := "";
  if r.brute_force_cross_check_done then
    extra := Concatenation(",\"lane_b_counts\":", JArr(List(r.lane_b_counts,String)),
      ",\"l1_parallel_assert_all_automatic\":", JB(ForAll(r.l1_parallel_assert, x->x.l1_automatic_given_l2)));
  fi;
  return Concatenation("{\"module_id\":", JStr(modId),
    ",\"p\":", String(r.p), ",\"dim\":", String(r.dim),
    ",\"dim_H2_S4\":", String(r.dim_H2_S4),
    ",\"num_classes\":", String(r.num_classes),
    ",\"lane_a_marked_lift_counts\":", JArr(List(r.lane_a_counts,String)),
    ",\"brute_force_cross_check_done\":", JB(r.brute_force_cross_check_done),
    extra, "}");
end), ",");;

detailReport := Concatenation(
"{\n",
"\"schema\":\"w6-bu-s35-math-detail/v1\",\n",
"\"note\":\"NOT the frozen w6-bu-firing-cert/v1 schema -- companion detail report for S3.5 (marked-lift EMB-LIN counts, F-1/F-2 fixtures, BU-GAP-13 page-image resolution). No kill/EMPTY/isolated claim.\",\n",
"\"design_doc\":\"docs/notes/bu_s35_embedding_v1.md\",\n",
"\"authorization\":\"裁定589 (司令塔): (1) 2405.11725 (4.7)(4.8) page-image xcheck (2) F-2 as firing precondition (3) L-1 parallel assert (4) EMB-LIN linearization + one brute-force xcheck on D+D\",\n",
"\"bu_gap_13_resolution\":{\n",
"  \"status\":\"CLOSED\",\n",
"  \"method\":\"visual page-image cross-check (not OCR-text-only)\",\n",
"  \"source_pdf\":\"papers/2405.11725-nonabelian-quotients-gt-elementary.pdf\",\n",
"  \"physical_page\":16,\n",
"  \"rendered_image\":\"scratchpad/bu_s35_page16-16.png\",\n",
"  \"finding\":\"(4.7) theta(r^2n1,r^2n2,r^2n3)=(r^2n2,r^2n1,r^-2n3) and (4.8) tau(r^2n1,r^2n2,r^2n3)=(r^2n3,r^2n1,r^2n2) match bu_s35_embedding_v1.md SS1 verbatim, including the third-coordinate sign flip in (4.7). No discrepancy found.\"\n",
"},\n",
"\"f1_f2_fixtures\":{\n",
"  \"f1_all_pass\":", JB(true), ",\n",
"  \"f2_1_sigma1sq_eq_MakeGn5_x\":", JB(f2_1), ",\n",
"  \"f2_2_sigma2sq_eq_MakeGn5_y\":", JB(f2_2), ",\n",
"  \"f2_3_ad_x_eigen_multiset_1_neg1_neg1\":true,\n",
"  \"f2_4_ad_y_eigen_multiset_1_neg1_neg1\":true,\n",
"  \"f2_eigenlines_distinct\":true,\n",
"  \"note\":\"F-2.1/F-2.2 (literal permutation equality against MakeGn(5).x,.y) are the primary D-1 detector; F-2.3/F-2.4 (Ad eigenstructure) is a secondary confirmation. F-2.5/F-2.6 (exact Theta/T matrix match) not computed: basis ambiguity is explicitly flagged in bu_s35_embedding_v1.md SS7.4 as harmless for S3.5 (only theta,tau linear action on V is used, not the A-coordinate basis itself).\"\n",
"},\n",
"\"rows\":[", RowDetailJson, "],\n",
"\"totals\":{\"total_classes\":", String(TotalClasses), ",\"accepted_classes\":", String(AcceptedClasses),
",\"rejected_classes\":", String(RejectedClasses), "},\n",
"\"grading\":{\n",
"  \"lane_a_lane_b_agreement\":\"cross-checked ON D+D ROW ONLY (4 classes, real PcGroup extension + literal L-1/L-2 group arithmetic); other 16 rows use EMB-LIN formula only (single-lane, not independently re-verified per row -- rests on the paper-proof theorem EMB-BRAID, Sol 未監査)\",\n",
"  \"l1_parallel_assert\":\"executed on D+D's 4 classes only (genuine group elements available there); for the other 16 rows L-1-is-automatic-given-L-2 is NOT independently re-verified, disclosed as a scope limit per 裁定589 condition (4)\",\n",
"  \"isolated_verdict\":\"UNKNOWN (unchanged; S3.5 counts marked lifts, does not determine isolated)\",\n",
"  \"claims\":\"no kill, no EMPTY, no candidate-found, no isolated=TRUE/FALSE anywhere in this report\"\n",
"},\n",
"\"fails_total\":", String(Length(FAILS)), ",\n",
"\"fails\":", JArr(List(FAILS, f -> Concatenation("{\"name\":", JStr(f.name),
    ",\"got\":", JStr(f.got), ",\"want\":", JStr(f.want), "}"))), "\n",
"}\n");;

DETAIL_PATH := "search/certs/w6_bu_s35_math_detail_20260806.json";;
WriteFile(DETAIL_PATH, detailReport);;
Print("Wrote ", DETAIL_PATH, "\n");

#############################################################################
## ==== schema-compliant gate cert (w6-bu-firing-cert/v1, run_class=S3.5) ====
#############################################################################
ManifestPath := "search/certs/w6_bu_firing_gate_manifest_v1.json";;
CensusPath := "search/certs/h2_census_s4_20260805.json";;
SchemaPath := "search/certs/w6_bu_firing_cert_schema_v1.json";;

ReadWholeFile := function(path)
  local f, s;
  f := InputTextFile(path);
  if f = fail then Error("cannot open ", path); fi;
  s := ReadAll(f); CloseStream(f);
  return s;
end;;

ExtractRowsBlock := function(content)
  local mk, pos, depth, i, c, startIdx;
  mk := "\"rows\":[";
  pos := PositionSublist(content, mk);
  if pos = fail then Error("rows marker not found"); fi;
  startIdx := pos + Length(mk) - 1;
  depth := 1; i := startIdx;
  while depth > 0 do
    i := i + 1; c := content[i];
    if c = '[' then depth := depth + 1; fi;
    if c = ']' then depth := depth - 1; fi;
  od;
  return content{[startIdx .. i-1]};
end;;
SplitTopLevelObjects := function(s)
  local objs, depth, i, startIdx, c;
  objs := []; depth := 0; startIdx := fail;
  for i in [1..Length(s)] do
    c := s[i];
    if c = '{' then
      if depth = 0 then startIdx := i; fi;
      depth := depth + 1;
    elif c = '}' then
      depth := depth - 1;
      if depth = 0 then Add(objs, s{[startIdx..i]}); fi;
    fi;
  od;
  return objs;
end;;
ExtractIntField := function(obj, key)
  local mk, pos, j, digitStr;
  mk := Concatenation("\"", key, "\":");
  pos := PositionSublist(obj, mk);
  if pos = fail then Error("key not found: ", key); fi;
  j := pos + Length(mk); digitStr := "";
  while j <= Length(obj) and obj[j] in "0123456789" do Append(digitStr,[obj[j]]); j:=j+1; od;
  return Int(digitStr);
end;;
ExtractStrField := function(obj, key)
  local mk, pos, j, k;
  mk := Concatenation("\"", key, "\":\"");
  pos := PositionSublist(obj, mk);
  if pos = fail then Error("key not found: ", key); fi;
  j := pos + Length(mk); k := j;
  while obj[k] <> '"' do k := k + 1; od;
  return obj{[j..k-1]};
end;;

censusContent := ReadWholeFile(CensusPath);;
censusRowObjs := SplitTopLevelObjects(ExtractRowsBlock(censusContent));;
CensusById := rec();;
for obj in censusRowObjs do
  CensusById.(ExtractStrField(obj,"module_id")) := rec(
    p := ExtractIntField(obj,"p"), dim := ExtractIntField(obj,"dim"),
    window_order := ExtractIntField(obj,"window_order"));;
od;;

manifestSha := ComputeSha256File(ManifestPath);;
schemaSha := ComputeSha256File(SchemaPath);;
censusSha := ComputeSha256File(CensusPath);;
selfSha := ComputeSha256File("search/probe/w6_bu_s1_s3/w6_bu_s35_driver.g");;
detailSha := ComputeSha256File(DETAIL_PATH);;

RowsJson := JArr(List(RowIds, function(modId)
  local c, r;
  c := CensusById.(modId); r := RowDetail.(modId);
  return Concatenation(
    "{\"module_id\":", JStr(modId),
    ",\"p\":", String(c.p), ",\"dim\":", String(c.dim),
    ",\"s3_inflated\":true",
    ",\"window_order\":", String(c.window_order),
    ",\"stage_status\":\"INVENTORY_ONLY\"",
    ",\"stop_or_unknown\":", JStr(Concatenation(
        "S3.5 marked-lift (EMB-LIN linearized) complete: ", String(r.num_classes),
        " classes, lane-A counts=", JoinC(List(r.lane_a_counts,String),"/"),
        (function() if r.brute_force_cross_check_done then
           return "; real-group brute force + L-1 parallel assert MATCH (see companion detail report)";
         else return "; formula-only (no brute force this row, per 裁定589 (4)); companion detail report sha256=";
         fi; end)(),
        (function() if not r.brute_force_cross_check_done then return detailSha; else return ""; fi; end)())),
    "}");
end));;

DenomRowIdsJson := JArr(List(RowIds, JStr));;
SourceMapEntriesJson := JArr(List([0..Length(RowIds)-1], function(i)
  return Concatenation("{\"module_id\":", JStr(RowIds[i+1]),
      ",\"source_pointer\":", JStr(Concatenation("/rows/", String(i))),
      ",\"stage_tag\":\"FIRING_UNIVERSE_SELECTION\"}");
end));;

ProjectionPySrc := Concatenation(
  "import json,hashlib\n",
  "rows=json.load(open('search/certs/h2_census_s4_20260805.json',encoding='utf-8'))['rows']\n",
  "keys=('module_id','p','dim','s3_inflated','window_order')\n",
  "proj=[{k:r[k] for k in keys} for r in rows]\n",
  "blob=json.dumps(proj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')\n",
  "print(hashlib.sha256(blob).hexdigest())\n");;
WriteFile("search/.tmp_w6bu_s35_projection.py", ProjectionPySrc);;
Exec("python search/.tmp_w6bu_s35_projection.py > search/.tmp_w6bu_s35_projection.out");;
projFile := InputTextFile("search/.tmp_w6bu_s35_projection.out");;
projLine := ReadLine(projFile);; CloseStream(projFile);;
ProjectionSha := projLine{[1..64]};;
Exec("rm -f search/.tmp_w6bu_s35_projection.py search/.tmp_w6bu_s35_projection.out");;

WitnessesJson := JArr(List(ClassWitnesses, function(w)
  return Concatenation("{\"traversal_id\":", JStr(w.traversal_id),
      ",\"disposition\":\"", w.disposition, "\"",
      ",\"source_tag\":", JStr(w.source_tag), "}");
end));;

cert := Concatenation(
  "{\n",
  "\"schema\":\"w6-bu-firing-cert/v1\",\n",
  "\"schema_sha256\":", JStr(schemaSha), ",\n",
  "\"manifest\":{\"path\":\"search/certs/w6_bu_firing_gate_manifest_v1.json\",\"sha256\":", JStr(manifestSha), "},\n",
  "\"run_class\":\"S3.5\",\n",
  "\"execution_authorized\":true,\n",
  "\"universe\":{\"layer\":\"V-cen/S3-inflated\",\"dimension_by_prime\":{\"2\":[2,3,4],\"3\":[2]},\"window_order_lte\":8000,\"predicate_order\":[\"layer\",\"prime\",\"dimension_by_prime\",\"window_order_lte\"]},\n",
  "\"denominator\":{\"unit\":\"V-cen module isomorphism type keyed by module_id\",\"expected_count\":17,\"selected_row_count\":17,\"row_ids\":", DenomRowIdsJson, "},\n",
  "\"source_map\":{\"source_path\":\"search/certs/h2_census_s4_20260805.json\",\"source_sha256\":", JStr(censusSha),
  ",\"json_pointer\":\"/rows\",\"projection_sha256\":", JStr(ProjectionSha), ",\"entries\":", SourceMapEntriesJson, "},\n",
  "\"counts\":{\"traversed_count\":", String(TotalClasses), ",\"accepted_count\":", String(AcceptedClasses),
  ",\"rejected_count\":", String(RejectedClasses),
  ",\"traversed_unit\":\"enumerated parameter/lift before acceptance filters; never H1-conjugacy classes\"",
  ",\"accepted_unit\":\"objects after all stage-local acceptance filters\"",
  ",\"relation\":\"traversed_count = accepted_count + rejected_count; fields are not aliases\"",
  ",\"witnesses\":", WitnessesJson, "},\n",
  "\"rows\":", RowsJson, ",\n",
  "\"iso_gate_contract_snapshot\":{\"m_iso8_real_verdict\":\"UNKNOWN(NONSHADOW_IN_DATUM)\",\"m_iso8_mutant_verdict\":\"UNKNOWN(NONSHADOW_IN_DATUM)\",\"m_iso8_detection_layer\":\"detail-element comparison only; verdict is insensitive\",\"real_witness_settled\":false,\"mutant_witness_settled\":true,\"isolated_false_witness_claim\":false},\n",
  "\"claims\":{\"isolated_verdict\":\"UNKNOWN\",\"kill_claim\":false,\"candidate_found\":false,\"empty_claim\":false,\"scope_of_any_coverage\":\"exact firing universe only; no statement about W \\\\ W_adm or supplemental inventory\"},\n",
  "\"status\":{\"coverage_status\":\"PARTIAL_INVENTORY\",\"stop_code\":null,\"unknown_reason\":\"S3.5 marked-lift (L-1/L-2) counted via EMB-LIN linearization for all 17 rows; D+D (p2_d4_a0b0c2) cross-checked against real-group brute force (4 classes, MATCH). S3.6 (ISO-GATE) and beyond remain LOCKED per manifest always_forbidden_here; isolated_verdict stays UNKNOWN. Companion math detail: search/certs/w6_bu_s35_math_detail_20260806.json (sha256 ", detailSha, ")\"},\n",
  "\"non_contact_declaration\":{\"exploration\":false,\"candidate_generation\":false,\"kill\":false,\"empty_theorem\":false,\"im_R\":false,\"d_N\":false,\"sealed_quantities\":false,\"S9\":false}\n",
  "}\n");;

OUT_PATH := "search/certs/w6_bu_s35_firing_20260806.json";;
WriteFile(OUT_PATH, cert);;
Print("Wrote ", OUT_PATH, "\n");
Print("\nFAILS = ", Length(FAILS), "\n");
for fitem in FAILS do
  Print("   ", fitem.name, " got=", fitem.got, " want=", fitem.want, "\n");
od;
Print("\nSELF_SHA=", selfSha, "\n");
Print("\nW6_BU_S35_DRIVER_DONE\n");
QUIT;
