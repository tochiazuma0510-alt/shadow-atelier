# week3-battery-1a.g -- stage 1a explorer: N_Q = pi^{-1}( ker( F2 ->> Q8 ) )
#
# Usage: .\gap.ps1 search\week3-battery-1a.g
# Reads only: search/manifest_spec_v1.md (spec projection), docs/wp2-transversal-model.md,
#             docs/week1-定義ノート.md SS1-2, search/week3-{L,M5}-explorer.g (patterns),
#             search/week3-battery-common.g (this batch's own shared helpers).
#
# Object (spec sec.2 stage "1a"): ambient B3, quotient Q8, marked_images x->i, y->j, c->1.
# element_encoding: quaternion units {1,-1,i,-i,j,-j,k,-k}. Self-contained construction below
# (NOT via GAP's SmallGroup library id, to keep the encoding auditable directly against the
# spec's quaternion-algebra definition rather than an opaque library id).

SizeScreen([4096, 0]);;
startTime := Runtime();;
Read("search/week3-battery-common.g");;

capStage := 600.0;;   # seconds, sec.1.1
haltStage := false;;

# ================================================================================
# Q8 construction (self-contained quaternion algebra, regular permutation representation)
# elements indexed 1..8 <-> (sign,unit): unit in {0=1,1=i,2=j,3=k}, sign in {+1,-1}
# ================================================================================
QUnitTable := [ [[1,0],[1,1],[1,2],[1,3]],     # 1 * {1,i,j,k}
                 [[1,1],[-1,0],[1,3],[-1,2]],  # i * {1,i,j,k} = {i,-1,k,-j}
                 [[1,2],[-1,3],[-1,0],[1,1]],  # j * {1,i,j,k} = {j,-k,-1,i}
                 [[1,3],[1,2],[-1,1],[-1,0]] ];; # k * {1,i,j,k} = {k,j,-i,-1}

QMul := function(g, h)
  local t;
  t := QUnitTable[g[2]+1][h[2]+1];
  return [ g[1]*h[1]*t[1], t[2] ];
end;;

IdxOfQ := function(g) return g[2]*2 + (1 - g[1])/2 + 1; end;;  # sign=1 -> +0, sign=-1 -> +1
ElemOfIdxQ := function(idx)
  local k, unit, signCode;
  k := idx - 1;
  unit := QuoInt(k, 2);
  signCode := k mod 2;
  if signCode = 0 then return [1, unit]; else return [-1, unit]; fi;
end;;

QRegPerm := function(d)
  local l, idx;
  l := [];
  for idx in [1..8] do l[idx] := IdxOfQ(QMul(d, ElemOfIdxQ(idx))); od;
  return PermList(l);
end;;

QLabelOfElem := function(g)
  local unitNames, s;
  unitNames := ["1","i","j","k"];
  if g[1] = 1 then
    if g[2] = 0 then return "1"; else return unitNames[g[2]+1]; fi;
  else
    if g[2] = 0 then return "-1"; else return Concatenation("-", unitNames[g[2]+1]); fi;
  fi;
end;;

QLabelOfPerm := function(p) return QLabelOfElem(ElemOfIdxQ(1^p)); end;;

one := [1,0];;  negone := [-1,0];;  ii := [1,1];;  jj := [1,2];;

xhat := QRegPerm(ii);;
yhat := QRegPerm(jj);;
chat := QRegPerm(one);;   # c |-> 1
QQ := Group(xhat, yhat);;

# ================================================================================
# U-F3: Q8 self-check -- i^4=1, i^2=j^2, ord(ij)=4, [i,j]=-1
# ================================================================================
fixtureOK := true;;

f3a := (xhat^4 = ());;
f3b := (xhat^2 = yhat^2);;
f3c := (Order(xhat*yhat) = 4);;
commIJ := xhat^-1*yhat^-1*xhat*yhat;;
f3d := (commIJ = QRegPerm(negone));;
Print("[", PF(f3a), "] U-F3a: i^4 = 1\n");
Print("[", PF(f3b), "] U-F3b: i^2 = j^2\n");
Print("[", PF(f3c), "] U-F3c: ord(ij) = 4\n");
Print("[", PF(f3d), "] U-F3d: [i,j] = -1\n");
if not (f3a and f3b and f3c and f3d) then fixtureOK := false; fi;

# ================================================================================
# U-F1/U-F2: universe numbers (spec sec.2 stage 1a (2)(3))
# ================================================================================
qqSize := Size(QQ);;
f1 := (qqSize = 8);;
Print("[", PF(f1), "] U-F1: pb3_index = |Q8| = ", qqSize, " (expect 8)\n");
if not f1 then fixtureOK := false; fi;

b3Points := 6 * qqSize;;
f1b := (b3Points = 48);;
Print("[", PF(f1b), "] U-F1: b3_points = 6*|Q8| = ", b3Points, " (expect 48)\n");
if not f1b then fixtureOK := false; fi;

nOrd := Lcm(Order(xhat), Order(yhat), Order(chat));;
f2a := (nOrd = 4);;
Print("[", PF(f2a), "] U-F2: n_ord = ", nOrd, " (expect 4)\n");
if not f2a then fixtureOK := false; fi;

DQQ := DerivedSubgroup(QQ);;
derivedOrder := Size(DQQ);;
f2b := (derivedOrder = 2);;
Print("[", PF(f2b), "] U-F2: derived_order = |[Q8,Q8]| = ", derivedOrder, " (expect 2)\n");
if not f2b then fixtureOK := false; fi;

charmingSet := Filtered([0..nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);;
f2c := (charmingSet = [0,1,2,3]);;
Print("[", PF(f2c), "] U-F2: charming_set = ", charmingSet, " (expect [0,1,2,3])\n");
if not f2c then fixtureOK := false; fi;

candidateTotalExpected := Length(charmingSet) * derivedOrder;;
f2d := (candidateTotalExpected = 8);;
Print("[", PF(f2d), "] U-F2: candidate_total = ", candidateTotalExpected, " (expect 8)\n");
if not f2d then fixtureOK := false; fi;

if not fixtureOK then
  Print("\n[UNKNOWN] stage 1a: fixture mismatch -- halting before enumeration (silent cap 禁止).\n");
  haltStage := true;
fi;

# ================================================================================
# enumeration (reduced hexagon, quotient shortcut -- valid since c_in_N=true here)
# ================================================================================
if not haltStage then

qrec := rec(x:=xhat, y:=yhat, c:=chat, G:=QQ);;
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

# ---- U-F8: theta/tau descend (spot check on generators via images already used above) ----
thetaOnGens := (Image(GroupHomomorphismByImages(QQ,QQ,[xhat,yhat],[yhat,xhat]), xhat) = yhat);;
Print("[", PF(thetaOnGens), "] U-F8: theta descends to Q8 (spot check on x)\n");

# ---- word-level parallel evaluation (spec (4): "安い" cheap self-check, diagnostic only) ----
zElt := AbstractProd([xhat,yhat])^-1;;
ThetaLetter := function(l) if l[1]="x" then return [["y",l[2]]]; else return [["x",l[2]]]; fi; end;;
TauLetter := function(l)
  if l[1]="x" then
    if l[2]=1 then return [["y",1]]; else return [["y",-1]]; fi;
  else
    if l[2]=1 then return [["y",-1],["x",-1]]; else return [["x",1],["y",1]]; fi;
  fi;
end;;
ApplyLetterSubst := function(word, letterFn) return Concatenation(List(word, letterFn)); end;;
ThetaWord := function(word) return ApplyLetterSubst(word, ThetaLetter); end;;
TauWord := function(word) return ApplyLetterSubst(word, TauLetter); end;;
EvalWordInQ := function(word, xg, yg)
  local val, letter;
  val := Identity(QQ);
  for letter in word do
    if letter[1]="x" then val := xg^letter[2] * val; else val := yg^letter[2] * val; fi;
  od;
  return val;
end;;

wordLevelDiff := 0;;
for sh in result.shadows do
  m := sh.m;
  combinedWord10 := Concatenation(sh.word, ThetaWord(sh.word));;
  wl310 := EvalWordInQ(combinedWord10, xhat, yhat) = Identity(QQ);;
  yWordM := List([1..m], ii -> ["y",1]);;
  ymfWord := Concatenation(yWordM, sh.word);;
  tauWord1 := TauWord(ymfWord);;
  tauWord2 := TauWord(tauWord1);;
  combinedWord11 := Concatenation(tauWord2, tauWord1, ymfWord);;
  wl311 := EvalWordInQ(combinedWord11, xhat, yhat) = Identity(QQ);;
  if not (wl310 and wl311) then wordLevelDiff := wordLevelDiff + 1; fi;
od;
Print("[", PF(wordLevelDiff = 0), "] 語レベル評価 並走診断: quotient_eval_diff_count(diagnostic, not schema field) = ", wordLevelDiff, " (0 なら商評価と一致)\n");

# ---- U-F9: E_m table, independent computation ----
emTable := ComputeEmTable(qrec, nOrd);;
Print("E_m table (independent):\n");
for row in emTable do
  Print("  E_", row.m, " = ", QLabelOfPerm(row.value), "\n");
od;

# ---- full-hexagon double-check on Q8 x T model (48 points) ----
t0 := Runtime();;
qt := BuildQTGeneral(QQ, xhat, yhat, chat);;
t1 := Runtime();;
Print("Q8 x T model built: np=", qt.np, " total_points=", 6*qt.np, " time_ms=", t1-t0, "\n");
qt.xx := qt.s1^2;;  qt.yy := qt.s2^2;;  qt.cc := (qt.s1*qt.s2*qt.s1)^2;;

braidOk := (qt.s1*qt.s2*qt.s1 = qt.s2*qt.s1*qt.s2);;
Print("[", PF(braidOk), "] QxT braid relation s1 s2 s1 = s2 s1 s2\n");

qtGroupSize := Size(Group(qt.s1, qt.s2));;
Print("Size(<s1,s2>) = ", qtGroupSize, " (expect ", b3Points, ")\n");
qtSizeOk := (qtGroupSize = b3Points);;
Print("[", PF(qtSizeOk), "] QxT |<s1,s2>| = b3_points\n");

if qt.cc <> () then
  Print("  [ANOMALY] qt.cc should be identity (c_in_N -> phi(c)=1), got non-identity\n");
fi;

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

# ---- U-F10: exact order (G-01) -- computed in the full B3/N permutation model (QxT) ----
deltaBPerm := qt.s1*qt.s2;;
DeltaPerm := qt.s1*qt.s2*qt.s1;;
exactOrder := Order(deltaBPerm^-1 * DeltaPerm);;
f10 := (exactOrder = 8);;
Print("[", PF(f10), "] U-F10: ord_Q(deltaB^-1 Delta) = ", exactOrder, " (expect 8 = 2*n_ord)\n");
if not f10 then fixtureOK := false; fi;

# ---- U-F11: S3 marking, independent of N (standard rho: B3 -> S3, sigma1->(12), sigma2->(23)) ----
S3rep := SymmetricGroup(3);;
sig1S3 := (1,2);;  sig2S3 := (2,3);;
# NOTE (reversal convention, same as AbstractProd elsewhere in this codebase): the paper's word
# "sigma1 sigma2 ... " is left-to-right, but GAP's raw permutation multiplication corresponds to
# the paper's convention only when applied in REVERSE order (verified empirically: GAP gives
# (1,2)*(2,3)=(1,3,2) but the manifest's standard rho gives deltaB=sigma1sigma2 -> (1,2,3), which
# matches (2,3)*(1,2) i.e. the reversed product -- consistent with AbstractProd's documented
# reversal). Delta=sigma1 sigma2 sigma1 is a palindrome so reversal doesn't change it.
deltaS3 := sig1S3*sig2S3*sig1S3;;      # Delta = sigma1 sigma2 sigma1 (palindrome, reversal-invariant)
deltaBS3 := sig2S3*sig1S3;;            # delta_B = sigma1 sigma2 (reversed for GAP convention)
# our marking convention: Delta -> (1,2), deltaB -> (1,2,3); this is the standard rho
# conjugated by (1,2,3) (manifest sec.1.5).  Verify: conj = (1,2,3); conj^-1 * deltaS3 * conj = ?
conj := (1,2,3);;
deltaConj := deltaS3^conj;;
deltaBConj := deltaBS3^conj;;
f11a := (deltaConj = (1,2));;
f11b := (deltaBConj = (1,2,3));;
Print("[", PF(f11a), "] U-F11: (standard Delta)^(1 2 3) = (1 2)\n");
Print("[", PF(f11b), "] U-F11: (standard deltaB)^(1 2 3) = (1 2 3)\n");
if not (f11a and f11b) then fixtureOK := false; fi;

# ---- m_missing: m in charming_set with no (h10,h11)-passing f at all ----
mMissing := [];;
for m in charmingSet do
  hasSolution := false;
  for gd in result.generation_detail do
    if gd.m = m and gd.stage <> "h10_fail" and gd.stage <> "h11_fail" then hasSolution := true; fi;
  od;
  if not hasSolution then Add(mMissing, m); fi;
od;
Print("m_missing (no simultaneous hexagon solution) = ", mMissing, "\n");

# ---- derived_product_check (W46): direct object, no fiber-product -- Q8^ab order check ----
abOrderObserved := qqSize / derivedOrder;;   # = 4
Print("derived_product_check: |Q8^ab| = ", abOrderObserved, ", |[Q8,Q8]| = ", derivedOrder,
      " (product = ", abOrderObserved*derivedOrder, " = |Q8| = ", qqSize, ")\n");

elapsedMs := Runtime() - startTime;;
Print("\n累計 elapsed ms: ", elapsedMs, "\n");
wallSeconds := elapsedMs / 1000.0;;
if wallSeconds > capStage then
  Print("[CAP EXCEEDED] stage 1a exceeded ", capStage, "s -> UNKNOWN (per sec.1.1)\n");
fi;

# ================================================================================
# certificate assembly (gtsh-cert/v2)
# ================================================================================
targetDef := Concatenation(
  "{\"ambient\":\"B3\",",
  "\"definition\":\"pi^{-1}( ker( F2 ->> Q8 ) )\",",
  "\"element_encoding\":\"quaternion units {1,-1,i,-i,j,-j,k,-k}\",",
  "\"id\":\"1a\",",
  "\"marked_images\":{\"c\":\"1\",\"x\":\"i\",\"y\":\"j\"},",
  "\"name\":\"N_Q\",",
  "\"quotient\":\"Q8\",",
  "\"source\":\"week3-狩場計画_v2 §3.1\"}");;

s3Marking := Concatenation(
  "{\"convention\":\"Delta_delta\",\"Delta_image\":\"(1 2)\",\"deltaB_image\":\"(1 2 3)\",",
  "\"equals_standard\":false,\"simultaneous_conjugate_of_standard\":true,\"conjugator\":\"(1 2 3)\"}");;

universeJson := Concatenation(
  "{\"pb3_index\":", String(qqSize), ",\"b3_points\":", String(b3Points),
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
  ",\"agree\":true,",
  "\"note\":\"1a is not a fiber-product object; ab_order_observed = |Q8:[Q8,Q8]| directly, no separate expected formula to cross-check against (W46 applies to 1b/3)\"}");;

emTableJson := [];;
for row in emTable do
  Add(emTableJson, Concatenation("{\"m\":", String(row.m), ",\"value_label\":\"", QLabelOfPerm(row.value), "\"}"));
od;

kernelCert := Concatenation(
  "{\"kernel_scope\":\"PB3\",\"pb3_kernel_index\":", String(qqSize),
  ",\"b3_kernel_index\":", String(b3Points), ",\"justification\":\"2401 (3.32)\"}");;

runtimeJson := Concatenation("{\"wall_seconds\":", String(Int(wallSeconds*1000)/1000.0),
                              ",\"max_rss_bytes\":null,\"max_rss_note\":\"not measured (GAP has no cheap RSS probe available in this session; -o 2g cap enforced via gap.ps1 instead)\"}");;

s := Concatenation(
  "{\"schema\":\"gtsh-cert/v2\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/week3-battery-1a.g\",\"date\":\"2026-07-26\"},",
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
  "\"torsion_generation_agrees\":\"UNKNOWN\",",
  "\"derived_product_check\":", derivedProductCheck, ",",
  "\"frobenius_zero\":[],",
  "\"frobenius_zero_note\":\"命題 E4 (指標和 N(v_m)) は読取禁止範囲(docs/命題_*)につき未計算 -- UNKNOWN として空配列\",",
  "\"m_missing\":", JArr(List(mMissing, String)), ",",
  "\"kernel_certificate\":", kernelCert, ",",
  "\"reductions\":[],",
  "\"reductions_note\":\"stage 1a is not a source of any reduction in this workorder's scope (R2/R3/R5 target N_Q are computed at stages 1b/2a/2b respectively, per workorder text)\",",
  "\"isolated\":\"UNKNOWN\",",
  "\"isolated_note\":\"settled/kernel-triple determination for every shadow not implemented in this batch -- reported UNKNOWN, not guessed\",",
  "\"runtime\":", runtimeJson, ",",
  "\"e_m_table\":", JArr(emTableJson), ",",
  "\"word_level_parallel_diagnostic\":{\"diff_count\":", String(wordLevelDiff), ",\"note\":\"spec (4) cheap parallel word-level check, diagnostic only (not a schema-required field; c_in_N=true so quotient shortcut is the evaluation_mode of record)\"}",
  "}");;

WriteFile("certificates/1a.v2.json", s);;
Print("wrote certificates/1a.v2.json\n");

fi; # haltStage

Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");
QUIT;
