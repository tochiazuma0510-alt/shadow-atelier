# week3-psl-S1.g -- PSL window S1: PSL(2,7), case A (split-inner), k=e=7, 1008 B3 points.
# workorder 4. Spec: search/manifest_spec_v2_psl.md (sole normative source for this implementation).
#
# Usage: .\gap.ps1 search\week3-psl-S1.g
#
# Convention notes (verified by direct matrix smoke test before writing this script, not assumed):
#  - paper's word "AB" = GAP's "B*A" (established throughout this project; re-verified here against
#    the spec's own worked values: w=T^-1 S matches GAP's S*T^-1; Y=S X S^-1 matches GAP's S^-1 X S).
#  - c_in_N=true for all PSL windows (sec.2.1) -> evaluation_mode=quotient_ok -> reuse the SAME
#    EnumerateReducedHexagon machinery (theta/tau via GroupHomomorphismByImages) already validated
#    across six prior stages (1a/1b/2a/2b/A1/3), rather than re-deriving the (H-a)/(H-b') reformulation
#    from partial spec text -- mathematically equivalent (both are Prop 3.4's reduced hexagon), and
#    this path is fully spec-projection-legitimate (evaluation_mode is spec-disclosed as quotient_ok).
#  - Aut(PSL(2,7)) = PGL(2,7) (q=7 prime, no field automorphisms) acting by conjugation -- built here
#    from the SAME PGL(2,7) matrix enumeration as the ambient group, per spec sec.4.2 (no
#    AutomorphismGroup() call).

SizeScreen([4096, 0]);;
startTime := Runtime();;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

capStage := 600.0;;
haltStage := false;;
q := 7;;

# ================================================================================
# marking (spec sec.2.2, S1 row) -- explicit matrices, self-derived w/X/Y/w2 (fixture PU-F2/F3)
# ================================================================================
Smat := MakeMat(q, 2,1,1,5);;
Tmat := MakeMat(q, 4,0,2,2);;
Sperm := MatToPerm(q, Smat);;
Tperm := MatToPerm(q, Tmat);;

fixtureOK := true;;

# ---- PU-F5: inner/outer (det S square?) ----
detS := DetMat2(Smat);;
sIsInner := IsSquareInGF(q, detS);;
fPU5 := sIsInner;;   # spec: S1 S is inner
Print("[", PF(fPU5), "] PU-F5: det(S)=", detS, " is_square=", sIsInner, " (expect inner=true for S1)\n");
if not fPU5 then fixtureOK := false; fi;

# ---- PU-F2: orders ----
fPU2a := (Order(Sperm) = 2);;
fPU2b := (Order(Tperm) = 3);;
wPerm := Sperm * Tperm^-1;;   # paper w = T^-1 S -> GAP S*T^-1 (reversal, verified by smoke test)
eOrd := Order(wPerm);;
fPU2c := (eOrd = 7);;
Xperm := wPerm^2;;
kOrd := Order(Xperm);;
fPU2d := (kOrd = 7);;
Print("[", PF(fPU2a), "] PU-F2: ord(S)=", Order(Sperm), " (expect 2)\n");
Print("[", PF(fPU2b), "] PU-F2: ord(T)=", Order(Tperm), " (expect 3)\n");
Print("[", PF(fPU2c), "] PU-F2: ord(w)=", eOrd, " (expect e=7)\n");
Print("[", PF(fPU2d), "] PU-F2: ord(X)=", kOrd, " (expect k=7)\n");
if not (fPU2a and fPU2b and fPU2c and fPU2d) then fixtureOK := false; fi;

# ---- PU-F3: XYZ=1, Y=TXT^-1=SXS^-1, Z=T^2XT^-2, w2^2=Y ----
Yperm := Sperm^-1 * Xperm * Sperm;;   # paper SXS^-1 -> GAP S^-1 X S (reversal)
YviaT := Tperm^-1 * Xperm * Tperm;;   # paper TXT^-1 -> GAP T^-1 X T
Zperm := Tperm^-2 * Xperm * Tperm^2;; # paper T^2 X T^-2 -> GAP T^-2 X T^2
w2perm := Tperm^-1 * Sperm;;          # paper w2 = S T^-1 -> GAP T^-1 S (reversal)
fPU3a := (Zperm * Yperm * Xperm = ());;   # paper XYZ=1 -> GAP Z*Y*X=1 (full reversal, matches A1 precedent)
fPU3b := (Yperm = YviaT);;
fPU3c := (w2perm^2 = Yperm);;
Print("[", PF(fPU3a), "] PU-F3: XYZ=1\n");
Print("[", PF(fPU3b), "] PU-F3: Y = TXT^-1 = SXS^-1\n");
Print("[", PF(fPU3c), "] PU-F3: w2^2 = Y\n");
if not (fPU3a and fPU3b and fPU3c) then fixtureOK := false; fi;

# ---- check against spec table's explicit w/X/Y/w2 matrices (independent double-check) ----
wCheckMat := MakeMat(q, 1,4,0,1);;   XCheckMat := MakeMat(q, 1,1,0,1);;
YCheckMat := MakeMat(q, 0,1,5,1);;   w2CheckMat := MakeMat(q, 1,2,3,3);;
fMatCheck := (wPerm = MatToPerm(q,wCheckMat)) and (Xperm = MatToPerm(q,XCheckMat))
             and (Yperm = MatToPerm(q,YCheckMat)) and (w2perm = MatToPerm(q,w2CheckMat));;
Print("[", PF(fMatCheck), "] spec table w/X/Y/w2 matrices match derived values\n");
if not fMatCheck then fixtureOK := false; fi;

# ---- PU-F4: <S,T>=Ghat, <X,Y>=G ----
Ghat := Group(Sperm, Tperm);;
ghatSize := Size(Ghat);;
Gg := Group(Xperm, Yperm);;
gSize := Size(Gg);;
fPU4a := (ghatSize = 168);;
fPU4b := (gSize = 168);;
Print("[", PF(fPU4a), "] PU-F4: |<S,T>| = ", ghatSize, " (expect 168)\n");
Print("[", PF(fPU4b), "] PU-F4: |<X,Y>| = ", gSize, " (expect 168)\n");
if not (fPU4a and fPU4b) then fixtureOK := false; fi;

# ---- PU-F1: group orders, PB3 index, B3 points ----
f1a := (ghatSize = 168);;
b3Points := 6 * gSize;;
f1b := (b3Points = 1008);;
Print("[", PF(f1a), "] PU-F1: |Ghat|=", ghatSize, " (expect 168)\n");
Print("[", PF(f1b), "] PU-F1: B3 points = ", b3Points, " (expect 1008)\n");
if not (f1a and f1b) then fixtureOK := false; fi;

# ---- PU-F13: group order self-check formulas ----
fPU13a := ((q^3-q)/Gcd(2,q-1) = 168);;   # |PSL(2,7)|
fPU13b := ((q^3-q) = 336);;              # |PGL(2,7)|
Print("[", PF(fPU13a), "] PU-F13: |PSL(2,7)| formula = ", (q^3-q)/Gcd(2,q-1), " (expect 168)\n");
Print("[", PF(fPU13b), "] PU-F13: |PGL(2,7)| formula = ", q^3-q, " (expect 336)\n");
if not (fPU13a and fPU13b) then fixtureOK := false; fi;

if not fixtureOK then
  Print("\n[UNKNOWN] S1: fixture mismatch -- halting.\n");
  haltStage := true;
fi;

# ================================================================================
# Aut(Ghat) = PGL(2,7) (q prime, no Frobenius) via explicit matrix enumeration (spec sec.4.2)
# ================================================================================
if not haltStage then

t0 := Runtime();;
pglElts := BuildPGLElements(q);;
t1 := Runtime();;
Print("\nPGL(2,7) enumerated: ", Length(pglElts), " elements (expect 336), time_ms=", t1-t0, "\n");
fAut := (Length(pglElts) = 336);;
Print("[", PF(fAut), "] |Aut(Ghat)| = |PGL(2,7)| = ", Length(pglElts), "\n");
if not fAut then fixtureOK := false; haltStage := true; fi;

fi;

if not haltStage then

# ---- PU-F6: exact order (G-01) via QxT model ----
nOrd := kOrd;;
charmingSet := Filtered([0..nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);;
fPU9a := (charmingSet = [0,1,2,4,5,6]);;
Print("[", PF(fPU9a), "] PU-F9: charming_set = ", charmingSet, " (expect [0,1,2,4,5,6])\n");
if not fPU9a then fixtureOK := false; fi;
phiCheck := Length(charmingSet);;
fPU9b := (phiCheck = 6);;
Print("[", PF(fPU9b), "] PU-F9: |X| = phi(2k) = ", phiCheck, " (expect 6)\n");
if not fPU9b then fixtureOK := false; fi;
# bijection check m -> 2m+1 mod 2k onto (Z/2k)^*
targetUnits := Filtered([0..2*nOrd-1], u -> Gcd(u,2*nOrd)=1);;
mapImg := List(charmingSet, m -> (2*m+1) mod (2*nOrd));;
fPU9c := (Set(mapImg) = Set(targetUnits)) and (Length(Set(mapImg)) = Length(charmingSet));;
Print("[", PF(fPU9c), "] PU-F9: m->2m+1 mod 2k is a bijection onto (Z/2k)^* (", Length(targetUnits), " units)\n");
if not fPU9c then fixtureOK := false; fi;

derivedOrder := gSize;;  # G perfect, [G,G]=G
candidateTotalExpected := Length(charmingSet) * derivedOrder;;
fPU10 := (candidateTotalExpected = 1008);;
Print("[", PF(fPU10), "] PU-F10: candidate_total = ", candidateTotalExpected, " (expect 1008)\n");
if not fPU10 then fixtureOK := false; fi;

# ---- PU-F7: c in N ----
fPU7 := (Sperm^2 = ());;
Print("[", PF(fPU7), "] PU-F7: S^2=1 (c_in_N)\n");
if not fPU7 then fixtureOK := false; fi;

if not fixtureOK then
  Print("\n[UNKNOWN] S1: fixture mismatch (post-Aut) -- halting.\n");
  haltStage := true;
fi;

fi;

# ================================================================================
# PU-F11: A5-CONV word-convention calibration (reuse of the A1 pattern from workorder1/2)
# ================================================================================
if not haltStage then

A5X := (1,3,2,4,5);;  A5Y := (1,3,4,5,2);;
A5 := Group(A5X, A5Y);;
evYXinv := AbstractProd([A5Y, A5X^-1]);;   # paper "y x^-1" -> GAP form via AbstractProd convention
fPU11a := (evYXinv = (1,2,4));;
Print("[", PF(fPU11a), "] PU-F11: ev(y x^-1) = ", evYXinv, " (expect (1 2 4))\n");
a5rec := rec(x:=A5X, y:=A5Y, c:=(), G:=A5);;
a5Result := EnumerateReducedHexagon(a5rec, [0,1,3,4]);;
fPU11b := (a5Result.shadow_total = 20);;
Print("[", PF(fPU11b), "] PU-F11: A1 hexagon 20/20 (observed shadow_total=", a5Result.shadow_total, ")\n");
if not (fPU11a and fPU11b) then fixtureOK := false; haltStage := true;
  Print("\n[UNKNOWN] S1: PU-F11 word-convention calibration FAILED -- halting per spec sec.1.4 item4.\n");
fi;

fi;

# ================================================================================
# PU-F12: W78 control (PSL(2,11), excluded window) -- class_coefficient=10, generation_pass_count=0
# for an inner order-5 element
# ================================================================================
if not haltStage then

q11 := 11;;
S11 := MakeMat(q11, 1,0,0,1);;  # placeholder; we need an actual inner order-5 element of PSL(2,11)
# construct PSL(2,11) via any valid (S,T)-like generating pair is unnecessary here -- we only need
# the FULL element list of PSL(2,11) (order 660) and a representative order-5 element v, then count
# T3 x T2 pairs with rg=v (paper) directly per spec's class_coefficient definition (sec.1.3).
t0 := Runtime();;
pgl11 := BuildPGLElements(q11);;
t1 := Runtime();;
Print("\nPGL(2,11) enumerated: ", Length(pgl11), " elements (expect 1320), time_ms=", t1-t0, "\n");
psl11Elts := Filtered(pgl11, e -> IsSquareInGF(q11, DetMat2(e.mat)));;
Print("PSL(2,11) subset: ", Length(psl11Elts), " elements (expect 660)\n");
psl11Perms := List(psl11Elts, e -> e.perm);;
fPU12size := (Length(psl11Perms) = 660);;
if not fPU12size then
  Print("[FAIL] PU-F12 precondition: PSL(2,11) size wrong, halting\n");
  haltStage := true;
else
  v5 := First(psl11Perms, x -> Order(x) = 5);;
  cc := ClassCoefficient(psl11Perms, v5);;
  fPU12a := (cc = 10);;
  Print("[", PF(fPU12a), "] PU-F12 control: class_coefficient(order-5 elt) = ", cc, " (expect 10)\n");
  # generation_pass_count for this control m: <v5^u, ...> style is not directly applicable (this is
  # a raw class-coefficient control, not a full (m,f) shadow search); spec's PU-F12 statement is
  # specifically about class_coefficient vs generation_pass_count DIVERGING (W78) -- we check the
  # divergence by confirming NO pair (r,g) with rg=v5 generates all of PSL(2,11) (i.e. every
  # (r,g) decomposition of v5 lands inside a proper subgroup, matching "falls into A5 order 60").
  genFailAll := true;;
  t3elts := Filtered(psl11Perms, x -> Order(x)=3);;
  t2elts := Filtered(psl11Perms, x -> Order(x)=2);;
  for r in t3elts do
    for g in t2elts do
      if g*r = v5 then
        if Size(Group(r,g)) = 660 then genFailAll := false; fi;
      fi;
    od;
  od;
  fPU12b := genFailAll;;
  Print("[", PF(fPU12b), "] PU-F12 control: generation_pass_count = 0 (no (r,g) decomposition generates all of PSL(2,11))\n");
  if not (fPU12a and fPU12b) then
    Print("\n[UNKNOWN] S1: PU-F12 control FAILED -- halting per spec sec.1.2/W78.\n");
    haltStage := true;
  fi;
fi;

fi;

Print("\nfixture gate elapsed ms: ", Runtime()-startTime, "\n");

# ================================================================================
# enumeration (reduced hexagon, quotient shortcut) -- reuse common.g EnumerateReducedHexagon
# ================================================================================
if not haltStage then

qrec := rec(x:=Xperm, y:=Yperm, c:=(), G:=Gg);;
t0 := Runtime();;
result := EnumerateReducedHexagon(qrec, charmingSet);;
t1 := Runtime();;
Print("\nreduced hexagon enumeration: time_ms=", t1-t0, "\n");
Print("candidate_total=", result.candidate_total, " h10_fail=", result.h10_fail,
      " h11_fail=", result.h11_fail, " generation_fail=", result.generation_fail,
      " shadow_total=", result.shadow_total, "\n");
shadowSumCheck := (result.candidate_total - result.h10_fail - result.h11_fail - result.generation_fail
                    = result.shadow_total);;
Print("[", PF(shadowSumCheck), "] shadow_total 引き算整合性チェック\n");

# ---- exact order via QxT model ----
t0 := Runtime();;
qt := BuildQTGeneral(Gg, Xperm, Yperm, ());;
t1 := Runtime();;
Print("QxT model built: np=", qt.np, " total_points=", 6*qt.np, " time_ms=", t1-t0, "\n");
braidOk := (qt.s1*qt.s2*qt.s1 = qt.s2*qt.s1*qt.s2);;
Print("[", PF(braidOk), "] QxT braid relation\n");
deltaBPerm := qt.s1*qt.s2;;  DeltaPerm := qt.s1*qt.s2*qt.s1;;
exactOrder := Order(deltaBPerm^-1 * DeltaPerm);;
fPU6 := (exactOrder = 14);;
Print("[", PF(fPU6), "] PU-F6: ord_Q(deltaB^-1 Delta) = ", exactOrder, " (expect 14 = 2k)\n");
if not fPU6 then Print("  [ANOMALY] PU-F6 failed post-enumeration -- reporting, cannot un-enumerate\n"); fi;

# ---- S3 marking (G-02), independent of N (same standard block) ----
sig1S3 := (1,2);;  sig2S3 := (2,3);;
deltaS3 := sig1S3*sig2S3*sig1S3;;  deltaBS3 := sig2S3*sig1S3;;
conj := (1,2,3);;
fPU8a := (deltaS3^conj = (1,2));;  fPU8b := (deltaBS3^conj = (1,2,3));;
Print("[", PF(fPU8a and fPU8b), "] PU-F8: S3 marking\n");

mMissing := [];;
for m in charmingSet do
  hasSolution := false;
  for gd in result.generation_detail do
    if gd.m = m and gd.stage <> "h10_fail" and gd.stage <> "h11_fail" then hasSolution := true; fi;
  od;
  if not hasSolution then Add(mMissing, m); fi;
od;
Print("m_missing = ", mMissing, "\n");

frobeniusZero := [];;
for m in charmingSet do
  ccVal := ClassCoefficient(List(Elements(Gg)), Xperm^(2*m+1));;
  if ccVal = 0 then Add(frobeniusZero, m); fi;
od;
Print("frobenius_zero (class_coefficient=0) = ", frobeniusZero, "\n");

# ================================================================================
# PU-F14: centralizer witness for w in Aut(Ghat)=PGL(2,7)
# ================================================================================
t0 := Runtime();;
centW := CentralizerWitness(pglElts, wPerm);;
t1 := Runtime();;
Print("\nC_Aut(w): order=", centW.order, " generator_mats count=", Length(centW.generator_mats),
      ", time_ms=", t1-t0, "\n");

# ================================================================================
# settled witness search (per-shadow) over Aut(Ghat)=PGL(2,7), 336 elements
# ================================================================================
settledDetail := [];;  settledCount := 0;;
t0 := Runtime();;
for sh in result.shadows do
  m := sh.m;  u := 2*m+1;  f := sh.f;
  targetX := Xperm^u;;
  targetY := AbstractProd([f^-1, Yperm^u, f]);;   # = f*Y^u*f^-1, AbstractProd/genB convention
  witness := fail;;
  for e in pglElts do
    h := e.perm;;
    if h^-1*Xperm*h = targetX and h^-1*Yperm*h = targetY then witness := e; break; fi;
  od;
  if witness <> fail then
    settledCount := settledCount + 1;
    Add(settledDetail, rec(m:=m, f_word:=sh.word, settled:=true, witness_mat:=witness.mat));
  else
    Add(settledDetail, rec(m:=m, f_word:=sh.word, settled:=false));
  fi;
od;
t1 := Runtime();;
Print("settled witness search: ", settledCount, "/", Length(result.shadows), " settled, time_ms=", t1-t0, "\n");

elapsedMs := Runtime() - startTime;;
Print("\n累計 elapsed ms: ", elapsedMs, "\n");
wallSeconds := elapsedMs / 1000.0;;
if wallSeconds > capStage then Print("[CAP EXCEEDED] S1\n"); fi;

# ================================================================================
# certificate assembly (gtsh-cert/v2-psl)
# ================================================================================
markingJson := Concatenation(
  "{\"S\":", JStr(MatToStr(Smat)), ",\"T\":", JStr(MatToStr(Tmat)),
  ",\"w\":", JStr(MatToStr(wCheckMat)), ",\"X\":", JStr(MatToStr(XCheckMat)),
  ",\"Y\":", JStr(MatToStr(YCheckMat)), ",\"w2\":", JStr(MatToStr(w2CheckMat)),
  ",\"det_S\":", String(IntFFE(detS)), ",\"det_S_is_square\":", JB(sIsInner),
  ",\"ord_S\":", String(Order(Sperm)), ",\"ord_T\":", String(Order(Tperm)),
  ",\"ord_w\":", String(eOrd), ",\"ord_X\":", String(kOrd), ",\"s_is_inner\":", JB(sIsInner), "}");;

genDetailJson := [];;
for gd in result.generation_detail do
  Add(genDetailJson, Concatenation("{\"m\":", String(gd.m), ",\"f_word\":", WordToJson(gd.f_word),
      ",\"pass\":", JB(gd.pass), ",\"stage\":\"", gd.stage, "\"}"));
od;

settledJson := [];;
for sd in settledDetail do
  if sd.settled then
    Add(settledJson, Concatenation("{\"m\":", String(sd.m), ",\"f_word\":", WordToJson(sd.f_word),
        ",\"settled\":true,\"automorphism_witness\":\"", MatToStr(sd.witness_mat), "\"}"));
  else
    Add(settledJson, Concatenation("{\"m\":", String(sd.m), ",\"f_word\":", WordToJson(sd.f_word),
        ",\"settled\":false,\"automorphism_witness\":null}"));
  fi;
od;

centGenJson := [];;
for gm in centW.generator_mats do Add(centGenJson, JStr(MatToStr(gm))); od;

hexFreeCert := Concatenation(
  "{\"candidate_total\":", String(result.candidate_total),
  ",\"h10_fail\":", String(result.h10_fail),
  ",\"h11_fail\":", String(result.h11_fail),
  ",\"generation_fail\":", String(result.generation_fail),
  ",\"shadow_total\":", String(result.shadow_total), "}");;

s := Concatenation(
  "{\"schema\":\"gtsh-cert/v2-psl\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/week3-psl-S1.g\",\"date\":\"2026-07-26\"},",
  "\"ambient_group\":\"PSL(2,7)\",\"case\":\"A_split_inner\",\"object_count\":1,\"aut_orbit_index\":1,",
  "\"element_encoding\":\"pgl2q_matrix/v1\",",
  "\"marking\":", markingJson, ",",
  "\"generation_checks\":{\"gen_ambient\":", String(ghatSize), ",\"gen_derived\":", String(gSize), "},",
  "\"universe\":{\"pb3_index\":", String(gSize), ",\"b3_points\":", String(b3Points),
  ",\"n_ord\":", String(nOrd), ",\"charming_set\":", JArr(List(charmingSet,String)),
  ",\"derived_order\":", String(derivedOrder), ",\"candidate_total\":", String(candidateTotalExpected), "},",
  "\"c_in_N\":true,\"evaluation_mode\":\"quotient_ok\",",
  "\"triangle_marking\":{\"applicable\":true,\"exact_order_binv_a\":", String(exactOrder), "},",
  "\"hexagon_free_certificate\":", hexFreeCert, ",",
  "\"generation_pass_count\":", String(result.shadow_total), ",",
  "\"generation_detail\":", JArr(genDetailJson), ",",
  "\"frobenius_zero\":", JArr(List(frobeniusZero,String)), ",",
  "\"m_missing\":", JArr(List(mMissing,String)), ",",
  "\"settled_detail\":", JArr(settledJson), ",",
  "\"settled_count\":", String(settledCount), ",",
  "\"centralizer_witness\":{\"order\":", String(centW.order), ",\"generator_mats\":", JArr(centGenJson), "},",
  "\"pu_f12_control\":{\"class_coefficient\":", String(cc), ",\"generation_pass_count\":0,\"note\":\"excluded window control, PSL(2,11) inner order-5 element\"},",
  "\"isolated\":\"UNKNOWN\",",
  "\"runtime\":{\"wall_seconds\":", String(Int(wallSeconds*1000)/1000.0), "}",
  "}");;

WriteFile("certificates/S1.v2.json", s);;
Print("wrote certificates/S1.v2.json\n");

fi; # haltStage

Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");
QUIT;
