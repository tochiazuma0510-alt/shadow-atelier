# week3-battery-A1.g -- stage A1 explorer: N_A = pi^{-1}( ker( F2 ->> A5 ) )
#
# Usage: .\gap.ps1 search\week3-battery-A1.g
#
# All generators (t,a,X,Y,Z,s) are taken VERBATIM from the spec-disclosed marking (manifest sec.2
# stage A1 "marking" block) -- these are spec, not sealed, so using the given cycle notation
# directly (rather than re-deriving X:=a t^-1 etc. myself) is legitimate and reduces derivation
# risk. Independently verified below (A-F1/A-F2/A-F3) before use.
#
# layer_id (P75, Prop E6): BLOCKED, same reasoning as the U-F7 blocker before its resolution --
# "Prop E6" is not in the spec projection given to me (docs/命題_* is explicitly off-limits), and
# no formula for the 3-layer S3 classification appears anywhere in manifest_spec_v1.md. Reporting
# BLOCKED rather than guessing which of the 3 layers corresponds to this Delta_bar.

SizeScreen([4096, 0]);;
startTime := Runtime();;
Read("search/week3-battery-common.g");;

capStage := 600.0;;
haltStage := false;;

# ================================================================================
# A5 construction: generators exactly as given in the spec marking block
# ================================================================================
tPerm := (1,2,3);;
aPerm := (1,4,5);;
Xhat := (1,3,2,4,5);;
Yhat := (1,3,4,5,2);;
Zhat := (1,4,5,3,2);;
sPerm := (1,4)(3,5);;
chat := ();;

fixtureOK := true;;

# ---- A-F1: A5 self-check ----
# NOTE (reversal convention, established for this codebase in stage 1a's U-F11 debugging and
# consistently used by AbstractProd elsewhere): paper's product "AB" (left to right) corresponds
# to GAP's "B*A" (empirically re-verified here for XYZ=1, tXt^-1=Y, X=at^-1 -- all three only hold
# under the reversed order; sXs^-1=Y is convention-independent since s=s^-1).
f1a := (Order(Xhat)=5 and Order(Yhat)=5 and Order(Zhat)=5);;
f1b := (Zhat*Yhat*Xhat = ());;                              # paper XYZ=1 -> GAP Z*Y*X=1
f1c := (Order(sPerm)=2);;
f1d := (sPerm*Xhat*sPerm^-1 = Yhat);;                        # s=s^-1, reversal-independent
f1e := (Order(tPerm)=3);;
f1f := (tPerm^-1*Xhat*tPerm = Yhat and tPerm^-1*Yhat*tPerm = Zhat and tPerm^-1*Zhat*tPerm = Xhat);;
f1g := (tPerm^-1*aPerm = Xhat);;   # marking says X = a t^{-1} -> GAP t^-1*a
Print("[", PF(f1a), "] A-F1a: ord(X)=ord(Y)=ord(Z)=5\n");
Print("[", PF(f1b), "] A-F1b: XYZ=1\n");
Print("[", PF(f1c), "] A-F1c: ord(s)=2\n");
Print("[", PF(f1d), "] A-F1d: sXs^-1=Y\n");
Print("[", PF(f1e), "] A-F1e: ord(t)=3\n");
Print("[", PF(f1f), "] A-F1f: tau: X->Y->Z->X (Ad(t))\n");
Print("[", PF(f1g), "] A-F1g: X = a t^-1 (marking consistency)\n");
if not (f1a and f1b and f1c and f1d and f1e and f1f and f1g) then fixtureOK := false; fi;

# ---- A-F2: <X,Y> = <X,t> = <s,t> = A5 (order 60) ----
gXY := Size(Group(Xhat,Yhat));;
gXt := Size(Group(Xhat,tPerm));;
gst := Size(Group(sPerm,tPerm));;
f2 := (gXY=60 and gXt=60 and gst=60);;
Print("[", PF(f2), "] A-F2: |<X,Y>|=", gXY, " |<X,t>|=", gXt, " |<s,t>|=", gst, " (expect 60,60,60)\n");
if not f2 then fixtureOK := false; fi;

A5 := Group(Xhat,Yhat);;

# ================================================================================
# U-F1/U-F2: universe numbers
# ================================================================================
a5Size := Size(A5);;
f1u := (a5Size = 60);;
Print("[", PF(f1u), "] U-F1: pb3_index = |A5| = ", a5Size, " (expect 60)\n");
if not f1u then fixtureOK := false; fi;

b3Points := 6 * a5Size;;
f1bu := (b3Points = 360);;
Print("[", PF(f1bu), "] U-F1: b3_points = 6*|A5| = ", b3Points, " (expect 360)\n");
if not f1bu then fixtureOK := false; fi;

nOrd := Lcm(Order(Xhat), Order(Yhat), Order(chat));;
f2au := (nOrd = 5);;
Print("[", PF(f2au), "] U-F2: n_ord = ", nOrd, " (expect 5)\n");
if not f2au then fixtureOK := false; fi;

DA5 := DerivedSubgroup(A5);;
derivedOrder := Size(DA5);;
f2bu := (derivedOrder = 60);;
Print("[", PF(f2bu), "] U-F2: derived_order = ", derivedOrder, " (expect 60, A5 perfect)\n");
if not f2bu then fixtureOK := false; fi;

charmingSet := Filtered([0..nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);;
f2cu := (charmingSet = [0,1,3,4]);;
Print("[", PF(f2cu), "] U-F2: charming_set = ", charmingSet, " (expect [0,1,3,4])\n");
if not f2cu then fixtureOK := false; fi;

candidateTotalExpected := Length(charmingSet) * derivedOrder;;
f2du := (candidateTotalExpected = 240);;
Print("[", PF(f2du), "] U-F2: candidate_total = ", candidateTotalExpected, " (expect 240)\n");
if not f2du then fixtureOK := false; fi;

Print("[BLOCKED] layer_id (P75, Prop E6): 命題 E4/E6 系の式は読取禁止範囲(docs/命題_*)につき\n");
Print("  未計算。3層のうちどれが指定 Delta_bar に対応するか判定不能 -- 司令塔確認要\n");

if not fixtureOK then
  Print("\n[UNKNOWN] stage A1: fixture mismatch -- halting.\n");
  haltStage := true;
fi;

# ================================================================================
# enumeration (reduced hexagon, quotient shortcut -- c_in_N=true for A1)
# ================================================================================
if not haltStage then

qrec := rec(x:=Xhat, y:=Yhat, c:=chat, G:=A5);;
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

# ================================================================================
# A-F3 + full-hexagon double-check on A5 x T model (B3/N_A ~= A5 x S3, order 360)
# ================================================================================
t0 := Runtime();;
qt := BuildQTGeneral(A5, Xhat, Yhat, chat);;
t1 := Runtime();;
Print("A5 x T model built: np=", qt.np, " total_points=", 6*qt.np, " time_ms=", t1-t0, "\n");
qt.xx := qt.s1^2;;  qt.yy := qt.s2^2;;  qt.cc := (qt.s1*qt.s2*qt.s1)^2;;

braidOk := (qt.s1*qt.s2*qt.s1 = qt.s2*qt.s1*qt.s2);;
Print("[", PF(braidOk), "] A-F3a: QxT braid relation\n");

qtGroupSize := Size(Group(qt.s1, qt.s2));;
qtSizeOk := (qtGroupSize = b3Points);;
Print("[", PF(qtSizeOk), "] A-F3b: |<s1,s2>| = ", qtGroupSize, " (expect ", b3Points, ")\n");
if not qtSizeOk then fixtureOK := false; fi;

deltaPermA := qt.s1*qt.s2*qt.s1;;
deltaBPermA := qt.s1*qt.s2;;
f3delta2 := (deltaPermA^2 = ());;
f3deltaB3 := (deltaBPermA^3 = ());;
Print("[", PF(f3delta2), "] A-F3c: Delta_bar^2 = 1 (c_in_N)\n");
Print("[", PF(f3deltaB3), "] A-F3d: deltaB_bar^3 = 1\n");
if not (f3delta2 and f3deltaB3) then fixtureOK := false; fi;

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
f10 := (exactOrder = 10);;
Print("[", PF(f10), "] U-F10: ord_Q(deltaB^-1 Delta) = ", exactOrder, " (expect 10)\n");
if not f10 then fixtureOK := false; fi;

# ---- U-F11 (independent of N, same standard block as other stages) ----
sig1S3 := (1,2);;  sig2S3 := (2,3);;
deltaS3 := sig1S3*sig2S3*sig1S3;;
deltaBS3 := sig2S3*sig1S3;;
conj := (1,2,3);;
f11a := (deltaS3^conj = (1,2));;
f11b := (deltaBS3^conj = (1,2,3));;
Print("[", PF(f11a), "] U-F11a\n");
Print("[", PF(f11b), "] U-F11b\n");
if not (f11a and f11b) then fixtureOK := false; fi;

mMissing := [];;
for m in charmingSet do
  hasSolution := false;
  for gd in result.generation_detail do
    if gd.m = m and gd.stage <> "h10_fail" and gd.stage <> "h11_fail" then hasSolution := true; fi;
  od;
  if not hasSolution then Add(mMissing, m); fi;
od;
Print("m_missing = ", mMissing, "\n");

abOrderObserved := a5Size / derivedOrder;;
Print("derived_product_check: |A5^ab| = ", abOrderObserved, ", |[A5,A5]| = ", derivedOrder,
      " (A5 perfect, ab trivial)\n");

elapsedMs := Runtime() - startTime;;
Print("\n累計 elapsed ms: ", elapsedMs, "\n");
wallSeconds := elapsedMs / 1000.0;;
if wallSeconds > capStage then Print("[CAP EXCEEDED] stage A1\n"); fi;

# ================================================================================
# certificate assembly (gtsh-cert/v2)
# ================================================================================
targetDef := Concatenation(
  "{\"B3_quotient\":\"Q = B3/N_A = A5 x S3 (order 360), Delta_bar=(s,(1 2)), deltaB_bar=(t,(1 2 3))\",",
  "\"definition\":\"pi^{-1}( ker( q: F2 ->> A5, x|->X, y|->Y ) )\",",
  "\"element_encoding\":\"permutations of {1..5}, 1-indexed cycle strings\",",
  "\"id\":\"A1\",",
  "\"marked_images\":{\"c\":\"1\",\"x\":\"X\",\"y\":\"Y\"},",
  "\"marking\":{\"X\":\"a t^{-1} = (1 3 2 4 5)\",\"Y\":\"t X t^{-1} = (1 3 4 5 2)\",",
  "\"Z\":\"t^2 X t^{-2} = (1 4 5 3 2)\",\"a\":\"(1 4 5)\",\"s\":\"t X^3 = (1 4)(3 5)\",",
  "\"tau_P\":\"Ad(t)\",\"theta_P\":\"Ad(s)\",\"t\":\"(1 2 3)\"},",
  "\"name\":\"N_A\",\"quotient\":\"A5\"}");;

s3Marking := Concatenation(
  "{\"convention\":\"Delta_delta\",\"Delta_image\":\"(1 2)\",\"deltaB_image\":\"(1 2 3)\",",
  "\"equals_standard\":false,\"simultaneous_conjugate_of_standard\":true,\"conjugator\":\"(1 2 3)\"}");;

universeJson := Concatenation(
  "{\"pb3_index\":", String(a5Size), ",\"b3_points\":", String(b3Points),
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

gtShadowsObservedJson := [];;
for sh in result.shadows do
  Add(gtShadowsObservedJson, Concatenation("{\"m\":", String(sh.m), ",\"f_word\":", WordToJson(sh.word), "}"));
od;

derivedProductCheck := Concatenation(
  "{\"ab_order_observed\":", String(abOrderObserved),
  ",\"product_expected\":", String(abOrderObserved),
  ",\"agree\":true,\"note\":\"A5 perfect: [A5,A5]=A5, ab trivial\"}");;

kernelCert := Concatenation(
  "{\"kernel_scope\":\"PB3\",\"pb3_kernel_index\":", String(a5Size),
  ",\"b3_kernel_index\":", String(b3Points), ",\"justification\":\"2401 (3.32)\"}");;

runtimeJson := Concatenation("{\"wall_seconds\":", String(Int(wallSeconds*1000)/1000.0),
                              ",\"max_rss_bytes\":null,\"max_rss_note\":\"not measured (see stage 1a note)\"}");;

s := Concatenation(
  "{\"schema\":\"gtsh-cert/v2\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/week3-battery-A1.g\",\"date\":\"2026-07-26\"},",
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
  "\"reductions\":[],",
  "\"reductions_note\":\"A1 is not a source of any reduction in the spec table (R6's source is A2's M_A5, computed at stage A2)\",",
  "\"isolated\":\"UNKNOWN\",",
  "\"isolated_note\":\"settled 判定未実装(司令塔裁定③)\",",
  "\"layer_id\":\"BLOCKED\",",
  "\"layer_id_note\":\"P75/Prop E6 の3層分類式が spec 射影内に見当たらない(docs/命題_* は読取禁止)。どの層が指定 Delta_bar に対応するか判定不能 -- 司令塔確認要\",",
  "\"runtime\":", runtimeJson, ",",
  "\"gt_shadows_observed\":", JArr(gtShadowsObservedJson), ",",
  "\"gt_shadows_observed_note\":\"G-06形式の要請への対応: sealed の known_solutions とは別名で観測 shadow 一覧をそのまま出力(比較や整形は行っていない)\"",
  "}");;

WriteFile("certificates/A1.v2.json", s);;
Print("wrote certificates/A1.v2.json\n");

fi; # haltStage

Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");
QUIT;
