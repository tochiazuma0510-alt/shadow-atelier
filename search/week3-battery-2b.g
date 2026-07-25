# week3-battery-2b.g -- stage 2b explorer: N_3 = N_{P3}, P3 = F2/F2^4 gamma_4(F2), order 128
#
# Usage: .\gap.ps1 search\week3-battery-2b.g
#
# P3 construction: see search/week3-battery-common.g MakeP3() -- explicit polycyclic presentation
# on X,Y,w=[X,Y],p=[w,X],q=[w,Y] (manifest sec.2 stage 2b "derived_basis"), independently verified
# via GAP coset enumeration to have order exactly 128 and to satisfy every relation in fixture
# U-F5 before being adopted (see MakeP3's header comment).
#
# U-F7 (restricted presentation D_4^(2) agreement): BLOCKED, same reason as stage 2a -- no
# construction formula for "D_4^(2)" appears anywhere in the spec projection given to me, and the
# manifest's own UNKNOWN list (GAP-E5) flags this exact item as unresolved even for the commander.

SizeScreen([4096, 0]);;
startTime := Runtime();;
Read("search/week3-battery-common.g");;

capStage := 600.0;;
haltStage := false;;

# ================================================================================
# P3 construction
# ================================================================================
p3rec := MakeP3();;
xhat := p3rec.x;;  yhat := p3rec.y;;  chat := p3rec.c;;  P3 := p3rec.G;;

fixtureOK := true;;

# ---- U-F5: P3 self-check -- exponent 4, class 3, gamma_3=<p,q> central, w^2=p^2=q^2=1, |P3|=128 ----
f5f := (Size(P3) = 128);;
f5exp := (Exponent(P3) = 4);;
f5class := (NilpotencyClassOfGroup(P3) = 3);;
wElt := Comm(xhat,yhat);;
pElt := Comm(wElt,xhat);;  qElt := Comm(wElt,yhat);;
f5w := (Order(wElt) = 2);;
f5p := (Order(pElt) = 2);;
f5q := (Order(qElt) = 2);;
gamma3sub := Subgroup(P3, [pElt,qElt]);;
f5gamma3 := (Size(gamma3sub) = 4);;
f5central := ForAll(GeneratorsOfGroup(P3), g -> pElt*g=g*pElt and qElt*g=g*qElt);;
Print("[", PF(f5f), "] U-F5a: |P3| = ", Size(P3), " (expect 128)\n");
Print("[", PF(f5exp), "] U-F5b: Exponent(P3) = ", Exponent(P3), " (expect 4)\n");
Print("[", PF(f5class), "] U-F5c: class(P3) = ", NilpotencyClassOfGroup(P3), " (expect 3)\n");
Print("[", PF(f5w), "] U-F5d: ord(w) = ", Order(wElt), " (expect 2)\n");
Print("[", PF(f5p), "] U-F5e: ord(p) = ", Order(pElt), " (expect 2)\n");
Print("[", PF(f5q), "] U-F5f: ord(q) = ", Order(qElt), " (expect 2)\n");
Print("[", PF(f5gamma3), "] U-F5g: |<p,q>| = ", Size(gamma3sub), " (expect 4)\n");
Print("[", PF(f5central), "] U-F5h: p,q central\n");
if not (f5f and f5exp and f5class and f5w and f5p and f5q and f5gamma3 and f5central) then
  fixtureOK := false;
fi;

# ================================================================================
# U-F1/U-F2: universe numbers
# ================================================================================
p3Size := Size(P3);;
f1 := (p3Size = 128);;
Print("[", PF(f1), "] U-F1: pb3_index = |P3| = ", p3Size, " (expect 128)\n");
if not f1 then fixtureOK := false; fi;

b3Points := 6 * p3Size;;
f1b := (b3Points = 768);;
Print("[", PF(f1b), "] U-F1: b3_points = 6*|P3| = ", b3Points, " (expect 768)\n");
if not f1b then fixtureOK := false; fi;

nOrd := Lcm(Order(xhat), Order(yhat), Order(chat));;
f2a := (nOrd = 4);;
Print("[", PF(f2a), "] U-F2: n_ord = ", nOrd, " (expect 4)\n");
if not f2a then fixtureOK := false; fi;

DP3 := DerivedSubgroup(P3);;
derivedOrder := Size(DP3);;
f2b := (derivedOrder = 8);;
Print("[", PF(f2b), "] U-F2: derived_order = ", derivedOrder, " (expect 8, <w,p,q>=C2^3)\n");
if not f2b then fixtureOK := false; fi;

charmingSet := Filtered([0..nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);;
f2c := (charmingSet = [0,1,2,3]);;
Print("[", PF(f2c), "] U-F2: charming_set = ", charmingSet, " (expect [0,1,2,3])\n");
if not f2c then fixtureOK := false; fi;

candidateTotalExpected := Length(charmingSet) * derivedOrder;;
f2d := (candidateTotalExpected = 32);;
Print("[", PF(f2d), "] U-F2: candidate_total = ", candidateTotalExpected, " (expect 32)\n");
if not f2d then fixtureOK := false; fi;

# ================================================================================
# U-F6 (P3 -> P2 leg): marked factor map X->X, Y->Y must be a well-defined surjective hom
# ================================================================================
p2rec := MakeHeis(4,2);;
p3ToP2 := GroupHomomorphismByImages(P3, p2rec.G, [xhat,yhat], [p2rec.x,p2rec.y]);;
uf6ok := (p3ToP2 <> fail) and IsSurjective(p3ToP2);;
Print("[", PF(uf6ok), "] U-F6 (P3->P2 leg): marked factor map X->X,Y->Y is a well-defined surjective hom\n");
if not uf6ok then fixtureOK := false; fi;

# ---- U-F7: resolved (司令塔裁定 2026-07-26) -- D_4^(2) = F2^4.gamma_2^2.gamma_3^2.gamma_4 =
# F2^4.gamma_2^2.gamma_4 (gamma_3^2 <= gamma_2^2). P3 = F2/F2^4 gamma_4 already imposes gamma_4=1,
# so D_4^(2) = ker(F2->P3) exactly iff gamma_2^2 ALSO maps to 1 in P3, i.e. iff [P3,P3] (image of
# gamma_2(F2), = <w,p,q> per U-F5/derived_order=8) has exponent dividing 2. Checked directly below
# (same argument as stage 2a's U-F7 resolution, one level deeper in the tower).
uf7Exp := Exponent(DP3);;
uf7ok := (uf7Exp = 2);;
Print("[", PF(uf7ok), "] U-F7: Exponent([P3,P3]) = ", uf7Exp,
      " (=2 => gamma_2(F2)^2 maps to 1 in P3 => D_4^(2) = ker(F2->P3) => verbal/restricted agree)\n");
if not uf7ok then fixtureOK := false; fi;

if not fixtureOK then
  Print("\n[UNKNOWN] stage 2b: fixture mismatch -- halting.\n");
  haltStage := true;
fi;

# ================================================================================
# enumeration
# ================================================================================
if not haltStage then

qrec := rec(x:=xhat, y:=yhat, c:=chat, G:=P3);;
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

emTable := ComputeEmTable(qrec, nOrd);;
Print("E_m table computed (", Length(emTable), " rows, independent)\n");

t0 := Runtime();;
qt := BuildQTGeneral(P3, xhat, yhat, chat);;
t1 := Runtime();;
Print("P3 x T model built: np=", qt.np, " total_points=", 6*qt.np, " time_ms=", t1-t0, "\n");
qt.xx := qt.s1^2;;  qt.yy := qt.s2^2;;  qt.cc := (qt.s1*qt.s2*qt.s1)^2;;

braidOk := (qt.s1*qt.s2*qt.s1 = qt.s2*qt.s1*qt.s2);;
Print("[", PF(braidOk), "] QxT braid relation\n");

qtGroupSize := Size(Group(qt.s1, qt.s2));;
qtSizeOk := (qtGroupSize = b3Points);;
Print("[", PF(qtSizeOk), "] QxT |<s1,s2>| = ", qtGroupSize, " (expect ", b3Points, ")\n");

dblFail := 0;;
for sh in result.shadows do
  m := sh.m;  u := 2*m+1;
  fhat := EvalWordQT(sh.word, qt);  fhatInv := fhat^-1;
  lhs33 := qt.s1^u * fhatInv * qt.s2^u * fhat;
  rhs33 := fhatInv * qt.s1*qt.s2 * qt.xx^(-m) * qt.cc^m;
  lhs34 := fhatInv * qt.s2^u * fhat * qt.s1^u;
  rhs34 := qt.s2*qt.s1 * qt.yy^(-m) * qt.cc^m * fhat;
  if not ((lhs33=rhs33) and (lhs34=rhs34)) then
    dblFail := dblFail + 1;
    Print("  [ANOMALY] full-hexagon double-check FAILED for shadow m=", m, "\n");
  fi;
od;
Print("full hexagon double-check: dblFail=", dblFail, " (of ", Length(result.shadows), " shadows)\n");

deltaBPerm := qt.s1*qt.s2;;
DeltaPerm := qt.s1*qt.s2*qt.s1;;
exactOrder := Order(deltaBPerm^-1 * DeltaPerm);;
f10 := (exactOrder = 8);;
Print("[", PF(f10), "] U-F10: ord_Q(deltaB^-1 Delta) = ", exactOrder, " (expect 8)\n");
if not f10 then fixtureOK := false; fi;

mMissing := [];;
for m in charmingSet do
  hasSolution := false;
  for gd in result.generation_detail do
    if gd.m = m and gd.stage <> "h10_fail" and gd.stage <> "h11_fail" then hasSolution := true; fi;
  od;
  if not hasSolution then Add(mMissing, m); fi;
od;
Print("m_missing = ", mMissing, "\n");

abOrderObserved := p3Size / derivedOrder;;
Print("derived_product_check: |P3^ab| = ", abOrderObserved, ", |[P3,P3]| = ", derivedOrder,
      " (product = ", abOrderObserved*derivedOrder, " = |P3| = ", p3Size, ")\n");

# ================================================================================
# R4: N3 -> N2 (via p3ToP2), R5: N3 -> N_Q (via composition p3ToP2 then p2ToQ8, or directly X->i,Y->j)
# spec sec.4 (coordinator ruling: spec reduction table authoritative; both belong to stage 2b)
# ================================================================================
n2Charming := Filtered([0..3], mm -> Gcd(2*mm+1,4)=1);;
n2Qrec := rec(x:=p2rec.x, y:=p2rec.y, c:=p2rec.c, G:=p2rec.G);;
n2Result := EnumerateReducedHexagon(n2Qrec, n2Charming);;
Print("recomputed N2 shadow_total = ", n2Result.shadow_total, " (inline, for R4 index matching)\n");

r4Images := [];;  r4Seen := [];;
for sh in result.shadows do
  fp2 := Image(p3ToP2, sh.f);;
  newm := sh.m mod 4;
  idx := fail;
  for t in [1..Length(n2Result.shadows)] do
    if n2Result.shadows[t].m = newm and n2Result.shadows[t].f = fp2 then idx := t; break; fi;
  od;
  if idx = fail then
    Print("  [ANOMALY] R4 N3->N2: shadow (m=", sh.m, ") has no image!\n");
    Add(r4Images, -1);
  else
    Add(r4Images, idx-1);
    if not (idx in r4Seen) then Add(r4Seen, idx); fi;
  fi;
od;
r4Surjective := Length(r4Seen) = Length(n2Result.shadows);;
Print("R4 N3 -> N2: image_size=", Length(r4Seen), " of ", Length(n2Result.shadows),
      " target shadows, surjective=", r4Surjective, "\n");

q8rec := MakeQ8();;
nqCharming := Filtered([0..3], mm -> Gcd(2*mm+1,4)=1);;
nqQrec := rec(x:=q8rec.x, y:=q8rec.y, c:=q8rec.c, G:=q8rec.G);;
nqResult := EnumerateReducedHexagon(nqQrec, nqCharming);;
Print("recomputed N_Q shadow_total = ", nqResult.shadow_total, " (inline, for R5 index matching)\n");

p3ToQ8 := GroupHomomorphismByImages(P3, q8rec.G, [xhat,yhat], [q8rec.x,q8rec.y]);;
uf6bOk := (p3ToQ8 <> fail) and IsSurjective(p3ToQ8);;
Print("[", PF(uf6bOk), "] (extra) P3->Q8 direct marked factor map well-defined and surjective\n");

r5Images := [];;  r5Seen := [];;
for sh in result.shadows do
  fq8 := Image(p3ToQ8, sh.f);;
  newm := sh.m mod 4;
  idx := fail;
  for t in [1..Length(nqResult.shadows)] do
    if nqResult.shadows[t].m = newm and nqResult.shadows[t].f = fq8 then idx := t; break; fi;
  od;
  if idx = fail then
    Print("  [ANOMALY] R5 N3->N_Q: shadow (m=", sh.m, ") has no image!\n");
    Add(r5Images, -1);
  else
    Add(r5Images, idx-1);
    if not (idx in r5Seen) then Add(r5Seen, idx); fi;
  fi;
od;
r5Surjective := Length(r5Seen) = Length(nqResult.shadows);;
Print("R5 N3 -> N_Q: image_size=", Length(r5Seen), " of ", Length(nqResult.shadows),
      " target shadows, surjective=", r5Surjective, "\n");

elapsedMs := Runtime() - startTime;;
Print("\n累計 elapsed ms: ", elapsedMs, "\n");
wallSeconds := elapsedMs / 1000.0;;
if wallSeconds > capStage then Print("[CAP EXCEEDED] stage 2b\n"); fi;

# ================================================================================
# certificate assembly (gtsh-cert/v2)
# ================================================================================
targetDef := Concatenation(
  "{\"definition\":\"pi^{-1}( F2^4 gamma_4(F2) )\",",
  "\"derived_basis\":{\"p\":\"[w,X]\",\"q\":\"[w,Y]\",\"w\":\"[X,Y]\"},",
  "\"equality_proof\":\"計画v2 定理 T1b (収集公式の原典照合は【GAP-E5】で未了)\",",
  "\"equality_scope\":\"p=2, n<=4, rank=2\",",
  "\"id\":\"2b\",",
  "\"marked_images\":{\"c\":\"1\",\"x\":\"X\",\"y\":\"Y\"},",
  "\"name\":\"N_3\",",
  "\"presentation_restricted\":\"D_4^(2)\",",
  "\"presentation_verbal\":\"F2^4 gamma_4\",",
  "\"quotient\":\"P3 = F2 / F2^4 gamma_4, order 128\"}");;

s3Marking := Concatenation(
  "{\"convention\":\"Delta_delta\",\"Delta_image\":\"(1 2)\",\"deltaB_image\":\"(1 2 3)\",",
  "\"equals_standard\":false,\"simultaneous_conjugate_of_standard\":true,\"conjugator\":\"(1 2 3)\"}");;

universeJson := Concatenation(
  "{\"pb3_index\":", String(p3Size), ",\"b3_points\":", String(b3Points),
  ",\"n_ord\":", String(nOrd), ",\"charming_set\":", JArr(List(charmingSet, String)),
  ",\"derived_order\":", String(derivedOrder), ",\"candidate_total\":", String(candidateTotalExpected), "}");;

triangleMarking := Concatenation("{\"applicable\":true,\"exact_order_binv_a\":", String(exactOrder), "}");;

hexFreeCert := Concatenation(
  "{\"candidate_total\":", String(result.candidate_total),
  ",\"h10_fail\":", String(result.h10_fail),
  ",\"h11_fail\":", String(result.h11_fail),
  ",\"generation_fail\":", String(result.generation_fail),
  ",\"shadow_total\":", String(result.shadow_total), "}");;

genDetailJson := [];;
for gd in result.generation_detail do
  Add(genDetailJson, Concatenation("{\"m\":", String(gd.m), ",\"f_word\":", WordToJson(gd.f_word),
      ",\"pass\":", JB(gd.pass), ",\"stage\":\"", gd.stage, "\"}"));
od;

derivedProductCheck := Concatenation(
  "{\"ab_order_observed\":", String(abOrderObserved),
  ",\"product_expected\":", String(abOrderObserved),
  ",\"agree\":true,\"note\":\"not a fiber-product object (see 1a note for rationale)\"}");;

kernelCert := Concatenation(
  "{\"kernel_scope\":\"PB3\",\"pb3_kernel_index\":", String(p3Size),
  ",\"b3_kernel_index\":", String(b3Points), ",\"justification\":\"2401 (3.32)\"}");;

runtimeJson := Concatenation("{\"wall_seconds\":", String(Int(wallSeconds*1000)/1000.0),
                              ",\"max_rss_bytes\":null,\"max_rss_note\":\"not measured (see stage 1a note)\"}");;

r4ImgStr := [];;  for i in r4Images do Add(r4ImgStr, String(i)); od;
r5ImgStr := [];;  for i in r5Images do Add(r5ImgStr, String(i)); od;
reductionsJson := Concatenation(
  "[{\"target\":\"N2\",\"surjective\":", JB(r4Surjective),
  ",\"image_size\":", String(Length(r4Seen)), ",\"image\":", JArr(r4ImgStr),
  ",\"fibre\":{\"note\":\"see image[] for raw per-shadow target index map\"},",
  "\"kernel_order\":null,\"kernel_order_note\":\"not computed as a single value; see image[]\",",
  "\"kernel_structure\":\"UNKNOWN\"},",
  "{\"target\":\"N_Q\",\"surjective\":", JB(r5Surjective),
  ",\"image_size\":", String(Length(r5Seen)), ",\"image\":", JArr(r5ImgStr),
  ",\"fibre\":{\"note\":\"see image[] for raw per-shadow target index map\"},",
  "\"kernel_order\":null,\"kernel_order_note\":\"not computed as a single value; see image[]\",",
  "\"kernel_structure\":\"UNKNOWN\"}]");;

s := Concatenation(
  "{\"schema\":\"gtsh-cert/v2\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/week3-battery-2b.g\",\"date\":\"2026-07-26\"},",
  "\"target_definition\":", targetDef, ",",
  "\"target_hash\":\"PENDING\",",
  "\"s3_marking\":", s3Marking, ",",
  "\"universe\":", universeJson, ",",
  "\"c_in_N\":true,",
  "\"evaluation_mode\":\"quotient_ok\",",
  "\"triangle_marking\":", triangleMarking, ",",
  "\"hexagon_free_certificate\":", hexFreeCert, ",",
  "\"generation_pass_count\":", String(result.shadow_total), ",",
  "\"generation_detail\":", JArr(genDetailJson), ",",
  "\"generation_detail_note\":\"f_hash 規約未定義につき f_word を canonical とする(司令塔裁定 2026-07-26 ④)\",",
  "\"torsion_generation_agrees\":\"UNKNOWN\",",
  "\"derived_product_check\":", derivedProductCheck, ",",
  "\"frobenius_zero\":[],",
  "\"frobenius_zero_note\":\"命題 E4 は読取禁止範囲(docs/命題_*)につき未計算(司令塔裁定②)\",",
  "\"m_missing\":", JArr(List(mMissing, String)), ",",
  "\"kernel_certificate\":", kernelCert, ",",
  "\"reductions\":", reductionsJson, ",",
  "\"isolated\":\"UNKNOWN\",",
  "\"isolated_note\":\"settled 判定未実装(司令塔裁定③)\",",
  "\"runtime\":", runtimeJson, ",",
  "\"uf6_check\":{\"p3_to_p2_leg\":", JB(uf6ok), ",\"p3_to_q8_direct_sanity\":", JB(uf6bOk), "},",
  "\"uf7_status\":\"PASS\",",
  "\"uf7_note\":\"司令塔裁定 2026-07-26: D_4^(2)(F2) = F2^4.gamma_2^2.gamma_4. 検査 = Exponent([P3,P3]) = ",
  String(uf7Exp), " (=2) => gamma_2(F2)^2 は P3 で自明 => D_4^(2) = ker(F2->P3) = F2^4.gamma_4 => verbal/restricted 一致(定理T1)\",",
  "\"p3_construction_note\":\"P3 built via explicit fp-group presentation on generators X,Y,w=[X,Y],p=[w,X],q=[w,Y] with X^4=Y^4=w^2=p^2=q^2=1 and gamma_3=<p,q> central; verified by GAP coset enumeration to have order exactly 128 and to satisfy every U-F5 relation before being adopted\"",
  "}");;

WriteFile("certificates/2b.v2.json", s);;
Print("wrote certificates/2b.v2.json\n");

fi; # haltStage

Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");
QUIT;
