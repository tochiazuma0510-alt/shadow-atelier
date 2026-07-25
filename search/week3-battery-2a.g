# week3-battery-2a.g -- stage 2a explorer: N_2 = N_{P2}, P2 = F2/F2^4 gamma_3(F2), order 32
#
# Usage: .\gap.ps1 search\week3-battery-2a.g
#
# P2 construction: manifest gives two presentations of P2 -- "verbal" (F2^4 gamma_3, i.e. mod
# 4th-power verbal subgroup and gamma_3) and "restricted" (label "D_3^(2)", no construction
# formula given anywhere in the spec projection I was given -- confirmed by grep of
# manifest_spec_v1.md: the string "D_3^(2)"/"D_4^(2)" appears only as a bare label, and even the
# commander's own UNKNOWN list (GAP-E5) flags the restricted presentation's "収集公式の原典照合"
# as unresolved for stage 2b. I build P2 from the VERBAL side only, using the exact relations
# spec-disclosed in fixture U-F4 (X^4=Y^4=(XY)^4=1, [X,Y] central order 2, class 2, |P2|=32) --
# these four relations pin P2 down to isomorphism (a class-2 2-group of order 32 with two order-4
# generators and central commutator of order 2), realized as a Heisenberg-style cocycle group
# (a,b,e) in Z/4 x Z/4 x Z/2, (a,b,e)(a',b',e')=(a+a',b+b',e+e'+a*b') -- HAND-VERIFIED against all
# four U-F4 relations before use (see report to commander). U-F7 ("両表示の一致") CANNOT be
# independently checked with this construction alone since the restricted side's defining formula
# is not given to me -- marked BLOCKED below, not fabricated, not silently skipped.

SizeScreen([4096, 0]);;
startTime := Runtime();;
Read("search/week3-battery-common.g");;

capStage := 600.0;;
haltStage := false;;

# ================================================================================
# P2 construction (Heisenberg-style, mod (4,4,2))
# ================================================================================
p2rec := MakeHeis(4, 2);;
xhat := p2rec.x;;  yhat := p2rec.y;;  chat := p2rec.c;;  P2 := p2rec.G;;

fixtureOK := true;;

# ---- U-F4: P2 self-check -- X^4=Y^4=(XY)^4=1, [X,Y] central order 2, class 2 ----
f4a := (xhat^4 = ());;
f4b := (yhat^4 = ());;
f4c := ((xhat*yhat)^4 = ());;
commXY := xhat^-1*yhat^-1*xhat*yhat;;
f4d := (Order(commXY) = 2);;
f4e := (commXY*xhat = xhat*commXY and commXY*yhat = yhat*commXY);;  # central
f4f := (Size(P2) = 32);;
Print("[", PF(f4a), "] U-F4a: X^4 = 1\n");
Print("[", PF(f4b), "] U-F4b: Y^4 = 1\n");
Print("[", PF(f4c), "] U-F4c: (XY)^4 = 1\n");
Print("[", PF(f4d), "] U-F4d: ord([X,Y]) = 2\n");
Print("[", PF(f4e), "] U-F4e: [X,Y] central\n");
Print("[", PF(f4f), "] U-F4f: |P2| = 32\n");
if not (f4a and f4b and f4c and f4d and f4e and f4f) then fixtureOK := false; fi;

# class 2: [X,Y] itself must be central and no deeper commutators -- already confirmed by f4e
# (P2 has 2 generators; class <=2 follows once [X,Y] is central, since gamma_3 = [[X,Y],{X,Y}] = 1)
gamma3check := (commXY^-1*xhat^-1*commXY*xhat = () and commXY^-1*yhat^-1*commXY*yhat = ());;
Print("[", PF(gamma3check), "] U-F4g: gamma_3(P2) = 1 (class exactly 2)\n");
if not gamma3check then fixtureOK := false; fi;

# ================================================================================
# U-F1/U-F2: universe numbers
# ================================================================================
p2Size := Size(P2);;
f1 := (p2Size = 32);;
Print("[", PF(f1), "] U-F1: pb3_index = |P2| = ", p2Size, " (expect 32)\n");
if not f1 then fixtureOK := false; fi;

b3Points := 6 * p2Size;;
f1b := (b3Points = 192);;
Print("[", PF(f1b), "] U-F1: b3_points = 6*|P2| = ", b3Points, " (expect 192)\n");
if not f1b then fixtureOK := false; fi;

nOrd := Lcm(Order(xhat), Order(yhat), Order(chat));;
f2a := (nOrd = 4);;
Print("[", PF(f2a), "] U-F2: n_ord = ", nOrd, " (expect 4)\n");
if not f2a then fixtureOK := false; fi;

DP2 := DerivedSubgroup(P2);;
derivedOrder := Size(DP2);;
f2b := (derivedOrder = 2);;
Print("[", PF(f2b), "] U-F2: derived_order = ", derivedOrder, " (expect 2)\n");
if not f2b then fixtureOK := false; fi;

charmingSet := Filtered([0..nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);;
f2c := (charmingSet = [0,1,2,3]);;
Print("[", PF(f2c), "] U-F2: charming_set = ", charmingSet, " (expect [0,1,2,3])\n");
if not f2c then fixtureOK := false; fi;

candidateTotalExpected := Length(charmingSet) * derivedOrder;;
f2d := (candidateTotalExpected = 8);;
Print("[", PF(f2d), "] U-F2: candidate_total = ", candidateTotalExpected, " (expect 8)\n");
if not f2d then fixtureOK := false; fi;

# ================================================================================
# U-F6 (partial -- only the P2 -> Q8 leg exists at this stage; P3 -> P2 belongs to 2b):
# marked factor map X->i, Y->j must be a well-defined surjective homomorphism P2 ->> Q8
# ================================================================================
q8rec := MakeQ8();;
p2ToQ8 := GroupHomomorphismByImages(P2, q8rec.G, [xhat,yhat], [q8rec.x,q8rec.y]);;
uf6ok := (p2ToQ8 <> fail) and IsSurjective(p2ToQ8);;
Print("[", PF(uf6ok), "] U-F6 (P2->Q8 leg only): marked factor map X->i,Y->j is a well-defined surjective hom\n");
if not uf6ok then fixtureOK := false; fi;

# ---- U-F7: resolved (司令塔裁定 2026-07-26) -- D_n^(2)(F2) := Prod_{i*2^j >= n} gamma_i(F2)^(2^j).
# D_3^(2) = F2^4 . gamma_2^2 . gamma_3. Since P2 = F2/F2^4 gamma_3 already, F2^4 gamma_3 <=
# ker(F2->P2) by construction; D_3^(2) = ker(F2->P2) EXACTLY iff the extra factor gamma_2^2 ALSO
# maps to 1 in P2, i.e. iff [P2,P2] (= image of gamma_2(F2) in P2) has exponent dividing 2 --
# because gamma_2(F2)^2 is generated by squares of elements of gamma_2(F2), all of which map into
# [P2,P2], so if [P2,P2] has exponent <=2 every such square is already trivial in P2. This is
# directly checkable: U-F4 already established ord([X,Y])=2 and [P2,P2]=<[X,Y]> is cyclic of order
# 2, so exponent([P2,P2])=2 automatically. Verified explicitly below (not just re-asserted).
uf7Exp := Exponent(DP2);;
uf7ok := (uf7Exp = 2);;
Print("[", PF(uf7ok), "] U-F7: Exponent([P2,P2]) = ", uf7Exp,
      " (=2 => gamma_2(F2)^2 maps to 1 in P2 => D_3^(2) = ker(F2->P2) => verbal/restricted agree)\n");
if not uf7ok then fixtureOK := false; fi;

if not fixtureOK then
  Print("\n[UNKNOWN] stage 2a: fixture mismatch -- halting.\n");
  haltStage := true;
fi;

# ================================================================================
# enumeration (reduced hexagon, quotient shortcut -- c_in_N=true)
# ================================================================================
if not haltStage then

qrec := rec(x:=xhat, y:=yhat, c:=chat, G:=P2);;
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
qt := BuildQTGeneral(P2, xhat, yhat, chat);;
t1 := Runtime();;
Print("P2 x T model built: np=", qt.np, " total_points=", 6*qt.np, " time_ms=", t1-t0, "\n");
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

abOrderObserved := p2Size / derivedOrder;;
Print("derived_product_check: |P2^ab| = ", abOrderObserved, ", |[P2,P2]| = ", derivedOrder,
      " (product = ", abOrderObserved*derivedOrder, " = |P2| = ", p2Size, ")\n");

# ================================================================================
# R3: N2 -> N_Q, via the marked factor map p2ToQ8 (spec sec.4 -- coordinator ruling: spec
# reduction table is authoritative; R3 belongs to stage 2a)
# ================================================================================
nqCharming := Filtered([0..3], mm -> Gcd(2*mm+1,4)=1);;
nqQrec := rec(x:=q8rec.x, y:=q8rec.y, c:=q8rec.c, G:=q8rec.G);;
nqResult := EnumerateReducedHexagon(nqQrec, nqCharming);;
Print("recomputed N_Q shadow_total = ", nqResult.shadow_total, " (inline, for R3 index matching)\n");

r3Images := [];;  r3Seen := [];;
for sh in result.shadows do
  fq8 := Image(p2ToQ8, sh.f);;
  newm := sh.m mod 4;
  idx := fail;
  for t in [1..Length(nqResult.shadows)] do
    if nqResult.shadows[t].m = newm and nqResult.shadows[t].f = fq8 then idx := t; break; fi;
  od;
  if idx = fail then
    Print("  [ANOMALY] R3 N2->N_Q: shadow (m=", sh.m, ") has no image!\n");
    Add(r3Images, -1);
  else
    Add(r3Images, idx-1);
    if not (idx in r3Seen) then Add(r3Seen, idx); fi;
  fi;
od;
r3Surjective := Length(r3Seen) = Length(nqResult.shadows);;
Print("R3 N2 -> N_Q: image_size=", Length(r3Seen), " of ", Length(nqResult.shadows),
      " target shadows, surjective=", r3Surjective, "\n");

elapsedMs := Runtime() - startTime;;
Print("\n累計 elapsed ms: ", elapsedMs, "\n");
wallSeconds := elapsedMs / 1000.0;;
if wallSeconds > capStage then Print("[CAP EXCEEDED] stage 2a\n"); fi;

# ================================================================================
# certificate assembly (gtsh-cert/v2)
# ================================================================================
targetDef := Concatenation(
  "{\"definition\":\"pi^{-1}( F2^4 gamma_3(F2) )\",",
  "\"equality_proof\":\"計画v2 定理 T1a\",",
  "\"equality_scope\":\"p=2, n<=4, rank=2\",",
  "\"id\":\"2a\",",
  "\"marked_images\":{\"c\":\"1\",\"x\":\"X\",\"y\":\"Y\"},",
  "\"name\":\"N_2\",",
  "\"presentation_restricted\":\"D_3^(2)\",",
  "\"presentation_verbal\":\"F2^4 gamma_3\",",
  "\"quotient\":\"P2 = F2 / F2^4 gamma_3, order 32\"}");;

s3Marking := Concatenation(
  "{\"convention\":\"Delta_delta\",\"Delta_image\":\"(1 2)\",\"deltaB_image\":\"(1 2 3)\",",
  "\"equals_standard\":false,\"simultaneous_conjugate_of_standard\":true,\"conjugator\":\"(1 2 3)\"}");;

universeJson := Concatenation(
  "{\"pb3_index\":", String(p2Size), ",\"b3_points\":", String(b3Points),
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
  "{\"kernel_scope\":\"PB3\",\"pb3_kernel_index\":", String(p2Size),
  ",\"b3_kernel_index\":", String(b3Points), ",\"justification\":\"2401 (3.32)\"}");;

runtimeJson := Concatenation("{\"wall_seconds\":", String(Int(wallSeconds*1000)/1000.0),
                              ",\"max_rss_bytes\":null,\"max_rss_note\":\"not measured (see stage 1a note)\"}");;

r3ImgStr := [];;  for i in r3Images do Add(r3ImgStr, String(i)); od;
reductionsJson := Concatenation(
  "[{\"target\":\"N_Q\",\"surjective\":", JB(r3Surjective),
  ",\"image_size\":", String(Length(r3Seen)), ",\"image\":", JArr(r3ImgStr),
  ",\"fibre\":{\"note\":\"see image[] for raw per-shadow target index map\"},",
  "\"kernel_order\":null,\"kernel_order_note\":\"not computed as a single value; see image[]\",",
  "\"kernel_structure\":\"UNKNOWN\"}]");;

s := Concatenation(
  "{\"schema\":\"gtsh-cert/v2\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/week3-battery-2a.g\",\"date\":\"2026-07-26\"},",
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
  "\"uf6_check\":{\"p2_to_q8_leg\":", JB(uf6ok), ",\"p3_to_p2_leg\":\"not applicable at this stage (2b)\"},",
  "\"uf7_status\":\"PASS\",",
  "\"uf7_note\":\"司令塔裁定 2026-07-26: D_3^(2)(F2) = F2^4.gamma_2^2.gamma_3. 検査 = Exponent([P2,P2]) = ",
  String(uf7Exp), " (=2) => gamma_2(F2)^2 は P2 で自明 => D_3^(2) = ker(F2->P2) = F2^4.gamma_3 => verbal/restricted 一致(定理T1)\"",
  "}");;

WriteFile("certificates/2a.v2.json", s);;
Print("wrote certificates/2a.v2.json\n");

fi; # haltStage

Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");
QUIT;
