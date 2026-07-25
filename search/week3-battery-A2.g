# week3-battery-A2.g -- stage A2 explorer: M_A5 = N_A cap N_5, N_5 = ker(beta_5: B3 -> S3 x C5)
#
# Usage: .\gap.ps1 search\week3-battery-A2.g
#
# c_in_N = false (c-bar = (1,zeta) has order 5) -> evaluation_mode = word_level_required.
# REVISED 2026-07-26 (coordinator reversed the earlier "natural" ruling on evidence): uses PREPEND
# word evaluation (search/week3-battery-common.g's EnumerateWordLevelHexagonPrepend), matching
# week3-M5-explorer.g's EvalWordInQ exactly -- the manifest's original pre-registered instruction.
# A first attempt with NATURAL evaluation gave shadow_total=12, disagreeing with N_A's (A1's)
# trusted shadow_total=20 via R6 (which Lemma A2A1 predicts should set-biject); a ground-truth
# check using genuine GAP FreeGroup automorphisms (theta,tau on F2 directly, no custom
# word-substitution code) confirmed PREPEND is correct: the "paper's word AB = GAP's B*A" reversal
# (established via 1a's S3-marking and A1's A5-marking fixtures) applies generally to this whole
# project's convention, and for A5 (a NATURAL, non-left-regular permutation representation) only
# ONE such reversal applies, which prepend accumulation already embeds. quotient-shortcut computed
# in parallel purely as a DIAGNOSTIC (A-F4), never used for the pass/fail judgement itself.

SizeScreen([4096, 0]);;
startTime := Runtime();;
Read("search/week3-battery-common.g");;

capStage := 600.0;;
haltStage := false;;

# ================================================================================
# A5 (on points 1-5) x C5 (on points 6-10) -- full direct product (Goursat: A5 simple, no
# nontrivial proper quotient shared with C5) -- generator zeta, marked images use zeta^2
# ================================================================================
Xhat5 := (1,3,2,4,5);;
Yhat5 := (1,3,4,5,2);;
zeta := (6,7,8,9,10);;   # C5 generator on points 6-10
zeta2 := zeta^2;;

xhat := Xhat5 * zeta2;;
yhat := Yhat5 * zeta2;;
chat := zeta;;            # c -> (1, zeta)

QM := Group(xhat, yhat);;

fixtureOK := true;;

# ---- A-F6 style + U-F1/U-F2 universe checks ----
qmSize := Size(QM);;
f1 := (qmSize = 300);;
Print("[", PF(f1), "] U-F1: pb3_index = |A5 x C5| = ", qmSize, " (expect 300, full direct product)\n");
if not f1 then fixtureOK := false; fi;

b3Points := 6 * qmSize;;
f1b := (b3Points = 1800);;
Print("[", PF(f1b), "] U-F1: b3_points = 6*|Q| = ", b3Points, " (expect 1800)\n");
if not f1b then fixtureOK := false; fi;

nOrd := Lcm(Order(xhat), Order(yhat), Order(chat));;
f2a := (nOrd = 5);;
Print("[", PF(f2a), "] U-F2: n_ord = ", nOrd, " (expect 5)\n");
if not f2a then fixtureOK := false; fi;

DQM := DerivedSubgroup(QM);;
derivedOrder := Size(DQM);;
f2b := (derivedOrder = 60);;
Print("[", PF(f2b), "] U-F2: derived_order = ", derivedOrder, " (expect 60, = A5 x 1)\n");
if not f2b then fixtureOK := false; fi;

# A-F6: projection A5x1 -> A5 is an isomorphism (derived subgroup structure check)
projA5 := function(g) return PermList(List([1..5], j -> j^g)); end;;
projC5 := function(g) return PermList(List([1..5], j -> (j+5)^g - 5)); end;;
derivedElts := List(DQM, projA5);;
f6a := (Set(derivedElts) = Elements(Group(Xhat5,Yhat5)));;
f6b := ForAll(DQM, g -> projC5(g) = ());;
Print("[", PF(f6a), "] A-F6a: G3-component(here A5-component) of [Q,Q] covers all of A5\n");
Print("[", PF(f6b), "] A-F6b: C5-component of every [Q,Q] element is trivial (derived subgroup = A5 x 1)\n");
if not (f6a and f6b) then fixtureOK := false; fi;

charmingSet := Filtered([0..nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);;
f2c := (charmingSet = [0,1,3,4]);;
Print("[", PF(f2c), "] U-F2: charming_set = ", charmingSet, " (expect [0,1,3,4])\n");
if not f2c then fixtureOK := false; fi;

candidateTotalExpected := Length(charmingSet) * derivedOrder;;
f2d := (candidateTotalExpected = 240);;
Print("[", PF(f2d), "] U-F2: candidate_total = ", candidateTotalExpected, " (expect 240)\n");
if not f2d then fixtureOK := false; fi;

# c_in_N = false check: c-bar = chat = zeta has order 5, not identity
cInNActual := (Order(chat) = 1);;
Print("[", PF(not cInNActual), "] c_in_N check: ord(c-bar) = ", Order(chat), " (expect 5, i.e. c_in_N=false)\n");
if cInNActual then fixtureOK := false; fi;

if not fixtureOK then
  Print("\n[UNKNOWN] stage A2: fixture mismatch -- halting.\n");
  haltStage := true;
fi;

# ================================================================================
# word-level enumeration (A-F4: mandatory; quotient shortcut diagnostic only)
# ================================================================================
if not haltStage then

qrec := rec(x:=xhat, y:=yhat, c:=chat, G:=QM);;
t0 := Runtime();;
result := EnumerateWordLevelHexagonPrepend(qrec, charmingSet);;
t1 := Runtime();;
Print("\nword-level hexagon enumeration: time_ms=", t1-t0, "\n");
Print("candidate_total=", result.candidate_total, " h10_fail=", result.h10_fail,
      " h11_fail=", result.h11_fail, " generation_fail=", result.generation_fail,
      " shadow_total=", result.shadow_total, "\n");
Print("quotient_shortcut_available=", result.quotient_shortcut_available,
      " quotient_eval_diff_count=", result.quotient_eval_diff_count, "\n");
shadowSumCheck := (result.candidate_total - result.h10_fail - result.h11_fail - result.generation_fail
                    = result.shadow_total);;
Print("[", PF(shadowSumCheck), "] shadow_total 引き算整合性チェック\n");
Print("[", PF(true), "] A-F4: judged by word-level evaluation only; quotient-shortcut recorded as diagnostic (see quotient_eval_diff_count)\n");
if result.quotient_eval_diff_count = 0 then
  Print("  [REPORT] quotient_eval_diff_count = 0 observed (spec sec.3: report to commander, not a fixture fail)\n");
fi;

# ---- A-F5: E_m via word level (C5 component hexagon holds for all m in charmingSet) ----
emTable := ComputeEmTable(qrec, nOrd);;
Print("E_m table computed (", Length(emTable), " rows, independent, note: reflects quotient eval of E_m itself, not the hex predicate)\n");

# ================================================================================
# full-hexagon double-check on QxT model (c genuinely alive, order 5)
# ================================================================================
t0 := Runtime();;
qt := BuildQTGeneral(QM, xhat, yhat, chat);;
t1 := Runtime();;
Print("Q x T model built: np=", qt.np, " total_points=", 6*qt.np, " time_ms=", t1-t0, "\n");
qt.xx := qt.s1^2;;  qt.yy := qt.s2^2;;  qt.cc := (qt.s1*qt.s2*qt.s1)^2;;

braidOk := (qt.s1*qt.s2*qt.s1 = qt.s2*qt.s1*qt.s2);;
Print("[", PF(braidOk), "] QxT braid relation\n");

qtGroupSize := Size(Group(qt.s1, qt.s2));;
qtSizeOk := (qtGroupSize = b3Points);;
Print("[", PF(qtSizeOk), "] QxT |<s1,s2>| = ", qtGroupSize, " (expect ", b3Points, ")\n");
if not qtSizeOk then fixtureOK := false; fi;

Print("Order(qt.cc) = ", Order(qt.cc), " (expect 5, c alive)\n");

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
Print("full hexagon double-check (words now prepend-convention, matches EvalWordQT): dblFail=",
      dblFail, " (of ", Length(result.shadows), " shadows)\n");

mMissing := [];;
for m in charmingSet do
  hasSolution := false;
  for gd in result.generation_detail do
    if gd.m = m and gd.stage <> "h10_fail" and gd.stage <> "h11_fail" then hasSolution := true; fi;
  od;
  if not hasSolution then Add(mMissing, m); fi;
od;
Print("m_missing = ", mMissing, "\n");

# ================================================================================
# R6: M_A5 -> N_A (集合全単射, W57 -- "群同型" と呼ばない). spec sec.4.
# ================================================================================
a5Charming := Filtered([0..4], mm -> Gcd(2*mm+1,5)=1);;
a5Qrec := rec(x:=Xhat5, y:=Yhat5, c:=(), G:=Group(Xhat5,Yhat5));;
a5Result := EnumerateReducedHexagon(a5Qrec, a5Charming);;
Print("recomputed N_A shadow_total = ", a5Result.shadow_total, " (inline, for R6 index matching, N_A c_in_N=true so shortcut valid there)\n");

r6Images := [];;  r6Seen := [];;
for sh in result.shadows do
  fa5 := projA5(sh.f);;
  newm := sh.m mod 5;
  idx := fail;
  for t in [1..Length(a5Result.shadows)] do
    if a5Result.shadows[t].m = newm and a5Result.shadows[t].f = fa5 then idx := t; break; fi;
  od;
  if idx = fail then
    Print("  [ANOMALY] R6 M_A5->N_A: shadow (m=", sh.m, ") has no image!\n");
    Add(r6Images, -1);
  else
    Add(r6Images, idx-1);
    if not (idx in r6Seen) then Add(r6Seen, idx); fi;
  fi;
od;
r6Surjective := Length(r6Seen) = Length(a5Result.shadows);;
r6Bijective := r6Surjective and (Length(Set(r6Images)) = Length(result.shadows));;
Print("R6 M_A5 -> N_A: image_size=", Length(r6Seen), " of ", Length(a5Result.shadows),
      " target shadows, surjective=", r6Surjective, ", |M_A5 shadows|=", Length(result.shadows),
      ", set-bijective(集合全単射,W57)=", r6Bijective, "\n");

elapsedMs := Runtime() - startTime;;
Print("\n累計 elapsed ms: ", elapsedMs, "\n");
wallSeconds := elapsedMs / 1000.0;;
if wallSeconds > capStage then Print("[CAP EXCEEDED] stage A2\n"); fi;

# ================================================================================
# certificate assembly (gtsh-cert/v2)
# ================================================================================
targetDef := Concatenation(
  "{\"C5_generator\":\"zeta\",",
  "\"definition\":\"N_A cap N_5,  N_5 = ker( beta_5: B3 -> S3 x C5 )\",",
  "\"id\":\"A2\",",
  "\"marked_images\":{\"c\":\"(1, zeta)\",\"x\":\"(X, zeta^2)\",\"y\":\"(Y, zeta^2)\"},",
  "\"name\":\"M_A5\",",
  "\"quotient\":\"A5 x C5 (order 300)\",",
  "\"symbol_note\":\"C5 の生成元は zeta (v3 の t は A5 の (1 2 3) と衝突するため改名)\"}");;

s3Marking := Concatenation(
  "{\"convention\":\"Delta_delta\",\"Delta_image\":\"(1 2)\",\"deltaB_image\":\"(1 2 3)\",",
  "\"equals_standard\":false,\"simultaneous_conjugate_of_standard\":true,\"conjugator\":\"(1 2 3)\"}");;

universeJson := Concatenation(
  "{\"pb3_index\":", String(qmSize), ",\"b3_points\":", String(b3Points),
  ",\"n_ord\":", String(nOrd), ",\"charming_set\":", JArr(List(charmingSet, String)),
  ",\"derived_order\":", String(derivedOrder), ",\"candidate_total\":", String(candidateTotalExpected), "}");;

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

kernelCert := Concatenation(
  "{\"kernel_scope\":\"PB3\",\"pb3_kernel_index\":", String(qmSize),
  ",\"b3_kernel_index\":", String(b3Points), ",\"justification\":\"2401 (3.32)\"}");;

runtimeJson := Concatenation("{\"wall_seconds\":", String(Int(wallSeconds*1000)/1000.0),
                              ",\"max_rss_bytes\":null,\"max_rss_note\":\"not measured (see stage 1a note)\"}");;

r6ImgStr := [];;  for i in r6Images do Add(r6ImgStr, String(i)); od;
reductionsJson := Concatenation(
  "[{\"target\":\"N_A\",\"surjective\":", JB(r6Surjective),
  ",\"image_size\":", String(Length(r6Seen)), ",\"image\":", JArr(r6ImgStr),
  ",\"set_bijective_W57\":", JB(r6Bijective),
  ",\"fibre\":{\"note\":\"see image[] for raw per-shadow target index map; W57: set bijection only, NOT called a group isomorphism (isolated status UNKNOWN both sides)\"},",
  "\"kernel_order\":null,\"kernel_order_note\":\"not computed as a single value; see image[]\",",
  "\"kernel_structure\":\"UNKNOWN\"}]");;

s := Concatenation(
  "{\"schema\":\"gtsh-cert/v2\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/week3-battery-A2.g\",\"date\":\"2026-07-26\"},",
  "\"target_definition\":", targetDef, ",",
  "\"target_hash\":\"PENDING\",",
  "\"s3_marking\":", s3Marking, ",",
  "\"universe\":", universeJson, ",",
  "\"c_in_N\":false,",
  "\"evaluation_mode\":\"word_level_required\",",
  "\"evaluation_convention_note\":\"prepend 規約(week3-M5-explorer.g の EvalWordInQ と同一、manifest 事前登録どおり)-- 実装は search/week3-battery-common.g の EnumerateWordLevelHexagonPrepend。natural 規約での初回試行(shadow_total=12)は R6(->N_A)で補題A2A1(集合全単射)と矛盾し、FreeGroup 準同型による地の計算で prepend が正しいと確認(司令塔裁定 2026-07-26、先の natural 裁定を撤回)\",",
  "\"triangle_marking\":\"not_applicable\",",
  "\"hexagon_free_certificate\":", hexFreeCert, ",",
  "\"generation_pass_count\":", String(result.shadow_total), ",",
  "\"generation_detail\":", JArr(genDetailJson), ",",
  "\"generation_detail_note\":\"f_hash 規約未定義につき f_word を canonical とする(司令塔裁定 2026-07-26 ④)\",",
  "\"torsion_generation_agrees\":\"UNKNOWN\",",
  "\"quotient_eval_diff_count\":", String(result.quotient_eval_diff_count), ",",
  "\"quotient_eval_diff_count_note\":\"診断並走のみ(A-F4)。0 が観測された場合は事実として報告するのみ -- 罠が無害と断定しない(spec sec.3)\",",
  "\"derived_product_check\":{\"ab_order_observed\":null,\"product_expected\":null,\"agree\":\"not_applicable\",\"note\":\"A5 perfect x C5 abelian, [Q,Q]=A5x1 exactly (not a fiber-product-vs-verbal comparison case)\"},",
  "\"frobenius_zero\":[],",
  "\"frobenius_zero_note\":\"命題 E4 は読取禁止範囲(docs/命題_*)につき未計算(司令塔裁定②)\",",
  "\"m_missing\":", JArr(List(mMissing, String)), ",",
  "\"kernel_certificate\":", kernelCert, ",",
  "\"reductions\":", reductionsJson, ",",
  "\"isolated\":\"UNKNOWN\",",
  "\"isolated_note\":\"settled 判定未実装(司令塔裁定③)。W57: 両者の isolated が UNKNOWN の間、R6 の集合全単射を「群同型」と呼ばない\",",
  "\"runtime\":", runtimeJson,
  "}");;

WriteFile("certificates/A2.v2.json", s);;
Print("wrote certificates/A2.v2.json\n");

fi; # haltStage

Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");
QUIT;
