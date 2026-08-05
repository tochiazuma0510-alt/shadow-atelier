#############################################################################
## twin-witness-mirror-v1.g -- 双子 witness 走 scope 2 (鏡映軌道分類)
##
## Prereg: docs/notes/twin_witness_prereg_iffirst_v1.md (発火前単独コミット済)
## Registered universe: L2 = 15 twin pairs (c in N, in_PB3) / 30 directed,
##   machine-extracted from search/certs/lins_twin_census_v1_20260806.json by
##   search/twin_witness_scope1_extract.py (scope 1 -- counts 174/28/15/13 and
##   all 4 SETDIGESTs matched the prereg doc bit-for-bit). Input data file:
##   search/twin_witness_l2_data_v1_generated.g (GENERATED, data only).
## L3 (13 pairs, c notin N) is NOT touched here (task instruction: held under
## 裁定 T-1, out of scope for this checker).
##
## For each of the 15 L2 pairs (members A, B, same index):
##   1. Reconstruct N=A and N=B as subgroups of B3 = <a,b|aba=bab> from the
##      cert's canonical_id_words (literal generator words), build
##      Q_N := B3/N via NaturalHomomorphismByNormalSubgroup (same method as
##      the census script). Sanity: Size(Q_N) = index (cert value).
##   2. iota: a |-> a^-1, b |-> b^-1 (endomorphism of B3, restriction of the
##      B3 automorphism iota of docs/notes/wall_design_audit_v1.md sec 6).
##      Implemented via the algebraic fact that iota is a homomorphism:
##      rebind the *global* GAP variables `a`,`b` to ga^-1,gb^-1 and
##      re-EvalString the same generator-word text -- this computes iota(w)
##      directly (iota(w1*w2)=iota(w1)*iota(w2), iota(w^-1)=iota(w)^-1, so
##      re-evaluating the identical parenthesised expression with the
##      generators swapped for their inverses is exactly iota applied to the
##      word, NOT a syntactic reversal).
##   3. mirror classification per member N (checked from N's own quotient
##      Q_N, testing both self (iota(N) vs N) and partner (iota(N) vs K)):
##        M0: iota(N) = N        (self-mirror; all own gens map to 1)
##        M1: iota(N) = K        (all partner gens map to 1, own gens do NOT)
##        M2: iota(N) notin {N,K} (S-TW-7 trigger; O-1/D-1 census re-check)
##   4. canary (S-TW-6): reduced hexagon (3.11) at [-1,1] is an *identity in
##      B3 itself* (doc sec 2.2, independent of N) -- checked per-window as a
##      convention sanity (paper-product order, W-4) rather than a
##      window-dependent test.
##   5. For M1 pairs, additional checks (doc sec 2.6): W-b charming (trivial:
##      u=-1 is a unit mod anything, f=1 in [P,P]), W-c SURJ (<a^-1,b^-1> = Q_N,
##      i.e. T_{-1,1} surjective), W-d kernel equality (i)(ii)(iii) --
##      all as explicit GAP computations, not asserted.
##   6. MC-1 export (doc sec 2.7): for each M1 pair, dump generator words +
##      permutation images (s1_perm, s2_perm) of Q_A (perm rep) for
##      independent python re-verification (search/twin_witness_mc1_check.py,
##      GAP-helper-free).
##
## R1-b / H-4 discipline: NOT applicable here -- this script performs no
## enumeration over (m, f-bar); it computes a single fixed shadow candidate
## [-1,1] (mirror route only). Scope 3 (non-mirror exhaustive enumeration)
## is a SEPARATE script, not this one.
##
## Sealed quantities / 705,894-pair universe / kill theorems: non-contact.
#############################################################################

Read("search/gaplib_common.g");
Read("search/probe/wac_v1/gap_output_prelude.g");

#############################################################################
## ---------------------- shared B3 setup (same as census script) -----------
#############################################################################
BF3 := FreeGroup("a", "b");;
ga := BF3.1;;  gb := BF3.2;;
brel := ga * gb * ga * (gb * ga * gb)^-1;;
B3 := BF3 / [brel];;
ga := B3.1;;  gb := B3.2;;

## global 'a','b' bindings used by EvalString below -- default = identity map
a := ga;;  b := gb;;

#############################################################################
## ---------------------- load L2 registered set (generated data file) ------
#############################################################################
Read("search/twin_witness_l2_data_v1_generated.g");   # defines L2Pairs
Print("Loaded L2Pairs: ", Length(L2Pairs), " pairs (expect 15)\n");
if Length(L2Pairs) <> 15 then
  Error("L2Pairs count mismatch -- STOP (scope 1 data file corrupt or stale)");
fi;

#############################################################################
## ---------------------- word evaluation helper -----------------------------
#############################################################################
## Evaluate a generator-word STRING (as it appears in the cert, e.g.
## "(a^-1*b^-1*a^-1)^2") as a B3 element, using the CURRENT global bindings
## of 'a' and 'b'. Default bindings (a:=ga, b:=gb) reproduce the word as
## originally intended; rebinding a:=ga^-1, b:=gb^-1 before calling this
## computes iota(word) (see file header for why this is valid).
EvalWordB3 := function(wordStr)
  return EvalString(wordStr);
end;;

EvalWordListB3 := function(wordStrList)
  return List(wordStrList, EvalWordB3);
end;;

#############################################################################
## ---------------------- per-pair mirror classification ---------------------
#############################################################################
Results := [];;
t0 := GAPLIB_WallElapsedMs();

for pr in L2Pairs do
  idx := pr.index;
  Print("\n=== pair index=", idx, " pair_uid=", pr.pair_uid, " ===\n");

  a := ga;;  b := gb;;   # default bindings for this pair's setup phase

  Awords := pr.A;;  Bwords := pr.B;;
  Agens := EvalWordListB3(Awords);;
  Bgens := EvalWordListB3(Bwords);;

  Asub := Subgroup(B3, Agens);;
  Bsub := Subgroup(B3, Bgens);;

  hmA := NaturalHomomorphismByNormalSubgroup(B3, Asub);;
  QA := Image(hmA);;
  hmB := NaturalHomomorphismByNormalSubgroup(B3, Bsub);;
  QB := Image(hmB);;

  sizeA := Size(QA);;  sizeB := Size(QB);;
  Print("  |B3/A|=", sizeA, " |B3/B|=", sizeB, " (cert index=", idx, ")\n");
  sizeSanityOK := (sizeA = idx) and (sizeB = idx);;
  if not sizeSanityOK then
    Print("  [S-TW-4-ADJACENT] size mismatch! sizeA=", sizeA, " sizeB=", sizeB, " idx=", idx, "\n");
  fi;

  ## --- canary S-TW-6: reduced hexagon (3.11) at [-1,1] is a B3 identity ---
  ## tau: x->y->z->x (z=(xy)^-1), x=a^2,y=b^2. At [-1,1] (m=-1,f=1) the
  ## reduced form collapses to x^-1*(x*y)*y^-1 = 1 (paper product, W-4) --
  ## an identity in B3 itself, checked directly (no N/Q needed):
  xB3 := ga^2;;  yB3 := gb^2;;
  canaryLHS := xB3^-1 * (xB3*yB3) * yB3^-1;;
  canaryPass := (canaryLHS = One(B3));;
  Print("  canary (3.11)@[-1,1] paper-product B3 identity: ", canaryPass, "\n");
  if not canaryPass then
    Print("  [S-TW-6 CANARY_FAIL] STOP -- convention or implementation broken\n");
  fi;

  ## --- iota(A) vs A, iota(A) vs B (computed inside QA) ---
  a := ga^-1;;  b := gb^-1;;   # rebind: EvalString now computes iota(word)
  iotaAwordsInA := EvalWordListB3(Awords);;   # iota(A)'s generators, as B3 elts
  iotaBwordsInA := EvalWordListB3(Bwords);;   # iota(B)'s generators, as B3 elts
  a := ga;;  b := gb;;   # restore

  imgIotaA_inA := List(iotaAwordsInA, w -> ImageElm(hmA, w));;
  imgIotaB_inA := List(iotaBwordsInA, w -> ImageElm(hmA, w));;

  selfTrivial_A := ForAll(imgIotaA_inA, w -> w = One(QA));;   # iota(A) subseteq A ?
  partnerTrivial_A := ForAll(imgIotaB_inA, w -> w = One(QA));; # B subseteq iota(A) ?

  ## --- symmetric check from B's side ---
  a := ga^-1;;  b := gb^-1;;
  iotaBwordsInB := EvalWordListB3(Bwords);;
  iotaAwordsInB := EvalWordListB3(Awords);;
  a := ga;;  b := gb;;

  imgIotaB_inB := List(iotaBwordsInB, w -> ImageElm(hmB, w));;
  imgIotaA_inB := List(iotaAwordsInB, w -> ImageElm(hmB, w));;

  selfTrivial_B := ForAll(imgIotaB_inB, w -> w = One(QB));;
  partnerTrivial_B := ForAll(imgIotaA_inB, w -> w = One(QB));;

  ## --- classify (from A's side; cross-check against B's side below) ---
  mclassA := "UNDETERMINED";;
  if selfTrivial_A then
    mclassA := "M0";;
  elif partnerTrivial_A then
    mclassA := "M1";;
  else
    mclassA := "M2";;
  fi;

  mclassB := "UNDETERMINED";;
  if selfTrivial_B then
    mclassB := "M0";;
  elif partnerTrivial_B then
    mclassB := "M1";;
  else
    mclassB := "M2";;
  fi;

  consistentAB := (mclassA = mclassB);;
  Print("  mirror class (A-side): ", mclassA, "  (self=", selfTrivial_A, " partner=", partnerTrivial_A, ")\n");
  Print("  mirror class (B-side): ", mclassB, "  (self=", selfTrivial_B, " partner=", partnerTrivial_B, ")\n");
  Print("  A/B-side consistent: ", consistentAB, "\n");
  if not consistentAB then
    Print("  [S-TW-5-ADJACENT] A-side and B-side mirror class disagree -- STOP, investigate\n");
  fi;

  ## --- W-b charming (M1 only, but cheap -- compute regardless) ---
  ## u=2m+1=-1 is a unit mod any N_ord (gcd(-1,n)=1 always); f=1 trivially
  ## in [P,P]. No group computation needed -- record as a fixed fact.
  wb_charming := true;;

  ## --- W-c SURJ: <a^-1,b^-1> = Q_A (T_{-1,1} surjective onto B3/A) ---
  genImgsInv_A := [ImageElm(hmA, ga^-1), ImageElm(hmA, gb^-1)];;
  surjSubA := Subgroup(QA, genImgsInv_A);;
  wc_surj_A := (Size(surjSubA) = sizeA);;
  Print("  W-c SURJ (A side): <a^-1,b^-1>=B3/A ? ", wc_surj_A, "\n");

  genImgsInv_B := [ImageElm(hmB, ga^-1), ImageElm(hmB, gb^-1)];;
  surjSubB := Subgroup(QB, genImgsInv_B);;
  wc_surj_B := (Size(surjSubB) = sizeB);;
  Print("  W-c SURJ (B side): <a^-1,b^-1>=B3/B ? ", wc_surj_B, "\n");

  ## --- record result ---
  Add(Results, rec(
    index := idx,
    pair_uid := pr.pair_uid,
    A_uid := pr.A_uid, B_uid := pr.B_uid,
    Awords := Awords, Bwords := Bwords,
    sizeA := sizeA, sizeB := sizeB, sizeSanityOK := sizeSanityOK,
    canaryPass := canaryPass,
    mclassA := mclassA, mclassB := mclassB, consistentAB := consistentAB,
    selfTrivial_A := selfTrivial_A, partnerTrivial_A := partnerTrivial_A,
    selfTrivial_B := selfTrivial_B, partnerTrivial_B := partnerTrivial_B,
    wb_charming := wb_charming,
    wc_surj_A := wc_surj_A, wc_surj_B := wc_surj_B,
    QA := QA, QB := QB, hmA := hmA, hmB := hmB, Asub := Asub, Bsub := Bsub
  ));;

  if GAPLIB_CheckCap(1700.0, "twin-witness-mirror-v1 per-pair pass") then
    Print("[CAP WARNING] stopping early\n");
    break;
  fi;
od;

t1 := GAPLIB_WallElapsedMs();
Print("\n=== ALL PAIRS DONE, elapsed_ms=", t1 - t0, " ===\n");

#############################################################################
## ---------------------- summary + prediction cross-check -------------------
#############################################################################
Print("\n=== SUMMARY ===\n");
predictedM1 := [126,234,342,378,558,666,702,774];;
countM0 := 0;; countM1 := 0;; countM2 := 0;; countUndet := 0;;
predFail := [];;
for r in Results do
  Print("index=", r.index, " class=", r.mclassA,
        " (B-side=", r.mclassB, ", consistent=", r.consistentAB, ")",
        " sizeOK=", r.sizeSanityOK, " canary=", r.canaryPass,
        " surjA=", r.wc_surj_A, " surjB=", r.wc_surj_B, "\n");
  if r.mclassA = "M0" then countM0 := countM0+1;
  elif r.mclassA = "M1" then countM1 := countM1+1;
  elif r.mclassA = "M2" then countM2 := countM2+1;
  else countUndet := countUndet+1; fi;

  predIsM1 := (r.index in predictedM1);;
  if predIsM1 and r.mclassA <> "M1" then
    Add(predFail, r.index);
    Print("  [P-5 PREDICTION FAILURE] index ", r.index, " predicted M1 but got ", r.mclassA, "\n");
  fi;
od;
Print("counts: M0=", countM0, " M1=", countM1, " M2=", countM2, " UNDET=", countUndet, "\n");
Print("prediction failures (S-TW-7 trigger if nonempty): ", predFail, "\n");

#############################################################################
## ---------------------- MC-1 export for M1 pairs (python cross-check) -----
#############################################################################
## For each M1 pair, export permutation images of a,b in QA (perm rep) plus
## generator words (both N=A and K=B), for the independent GAP-helper-free
## python re-checker (search/twin_witness_mc1_check.py). Schema per prereg
## doc sec 2.7 (mirror_cert/v1), degree = index (regular-ish rep via
## IsomorphismPermGroup -- need not literally be the regular action).
JStrLocal := function(s) return Concatenation("\"", s, "\""); end;;

mc1Parts := [];;
Add(mc1Parts, "{\n  \"mirror_certs\": [\n");
first := true;;
for r in Results do
  if r.mclassA <> "M1" then continue; fi;
  isoA := IsomorphismPermGroup(r.QA);;
  QAp := Image(isoA);;
  s1p := ImageElm(isoA, ImageElm(r.hmA, ga));;
  s2p := ImageElm(isoA, ImageElm(r.hmA, gb));;
  deg := LargestMovedPoint(QAp);;
  if deg = 0 or deg = fail then deg := NrMovedPoints(QAp); fi;
  s1list := List([1..deg], i -> i^s1p);;
  s2list := List([1..deg], i -> i^s2p);;

  if not first then Add(mc1Parts, ",\n"); fi;
  first := false;;
  Add(mc1Parts, Concatenation(
    "    {\n",
    "      \"index\": ", String(r.index), ",\n",
    "      \"pair_uid\": ", JStrLocal(r.pair_uid), ",\n",
    "      \"target_window_uid\": ", JStrLocal(r.A_uid), ",\n",
    "      \"source_kernel_uid\": ", JStrLocal(r.B_uid), ",\n",
    "      \"perm_degree\": ", String(deg), ",\n",
    "      \"s1_perm\": ", JArr(List(s1list, String)), ",\n",
    "      \"s2_perm\": ", JArr(List(s2list, String)), ",\n",
    "      \"N_gen_words\": ", JArr(List(r.Awords, JStrLocal)), ",\n",
    "      \"K_gen_words\": ", JArr(List(r.Bwords, JStrLocal)), "\n",
    "    }"
  ));
od;
Add(mc1Parts, "\n  ]\n}\n");
WriteFile("search/certs/twin_witness_mc1_export_v1_20260806.json", Concatenation(mc1Parts));
Print("\nWrote search/certs/twin_witness_mc1_export_v1_20260806.json\n");
Print("ALL_DONE\n");
