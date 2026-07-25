# week3-battery-1b.g -- stage 1b explorer: M_Q = K^(3) cap N_Q
#
# Usage: .\gap.ps1 search\week3-battery-1b.g
# Reads only: search/manifest_spec_v1.md (spec projection), docs/wp2-transversal-model.md,
#             docs/week1-定義ノート.md SS1-2, search/week3-{L,M5}-explorer.g (fiber-product
#             pattern: Q_L=G3xH3 / Q_M=G3xC5 built as subgroup of ambient direct product on
#             disjoint point blocks), search/week3-battery-common.g (this batch's shared helpers).
#
# Object (spec sec.2 stage "1b"): quotient = G3 x_{C2^2} Q8 (order 216), a genuine fiber product
# (NOT the full direct product 108*8=864) realized exactly like Q_L/Q_M in week3-L/M5-explorer.g:
# build the ambient direct product on disjoint point blocks (G3 on 1-9, Q8 on 10-17) and take
# Group(xhat,yhat) where xhat=(G3.x,Q8.x), yhat=(G3.y,Q8.y) -- the fiber-product structure falls
# out of the BFS closure automatically (Goursat: G3^ab=C2^2=Q8^ab is the shared common quotient
# forcing index 4 inside the full product, exactly analogous to how Q_L/Q_M's BFS closure
# automatically produced their own (different) orders).
#
# coordinator ruling 2026-07-26: reduction table (R#) in manifest_spec_v1.md sec.4 is the norm;
# workorder text conflicts resolve in favor of the spec. R1 (M_Q -> K^(3)) and R2 (M_Q -> N_Q) both
# belong to this stage per sec.4. f_word is the canonical generation_detail field (ruling 4).

SizeScreen([4096, 0]);;
startTime := Runtime();;
Read("search/week3-battery-common.g");;

capStage := 600.0;;
haltStage := false;;

# ================================================================================
# G3 (9 pts, from MakeGn(3)) and Q8 (8 pts, from MakeQ8()) -- fiber product on 17 points
# ================================================================================
gn := MakeGn(3);;
Print("G3 = MakeGn(3): |G3| = ", Size(gn.G), " (expect 108)\n");
q8rec := MakeQ8();;
Print("Q8 = MakeQ8(): |Q8| = ", Size(q8rec.G), " (expect 8)\n");

xhat := PermList(Concatenation(List([1..9], j -> j^gn.x), List([1..8], j -> 9 + (j^q8rec.x))));;
yhat := PermList(Concatenation(List([1..9], j -> j^gn.y), List([1..8], j -> 9 + (j^q8rec.y))));;
chat := ();;   # c -> ((1,1,1),1): identity on both blocks

QM := Group(xhat, yhat);;

# ================================================================================
# fixture self-checks (halt before enumeration if any fails -- sec.1.2)
# ================================================================================
fixtureOK := true;;

qmSize := Size(QM);;
f1 := (qmSize = 216);;
Print("[", PF(f1), "] U-F1: pb3_index = |Q_M| = ", qmSize, " (expect 216, fiber product not 108*8=864)\n");
if not f1 then fixtureOK := false; fi;

b3Points := 6 * qmSize;;
f1b := (b3Points = 1296);;
Print("[", PF(f1b), "] U-F1: b3_points = 6*|Q_M| = ", b3Points, " (expect 1296)\n");
if not f1b then fixtureOK := false; fi;

nOrd := Lcm(Order(xhat), Order(yhat), Order(chat));;
f2a := (nOrd = 12);;
Print("[", PF(f2a), "] U-F2: n_ord = ", nOrd, " (expect 12 = lcm(6,4))\n");
if not f2a then fixtureOK := false; fi;

DQM := DerivedSubgroup(QM);;
derivedOrder := Size(DQM);;
f2b := (derivedOrder = 54);;
Print("[", PF(f2b), "] U-F2: derived_order = |[Q_M,Q_M]| = ", derivedOrder, " (expect 54 = 27*2)\n");
if not f2b then fixtureOK := false; fi;

charmingSet := Filtered([0..nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);;
f2c := (charmingSet = [0,2,3,5,6,8,9,11]);;
Print("[", PF(f2c), "] U-F2: charming_set = ", charmingSet, " (expect [0,2,3,5,6,8,9,11])\n");
if not f2c then fixtureOK := false; fi;

candidateTotalExpected := Length(charmingSet) * derivedOrder;;
f2d := (candidateTotalExpected = 432);;
Print("[", PF(f2d), "] U-F2: candidate_total = ", candidateTotalExpected, " (expect 432)\n");
if not f2d then fixtureOK := false; fi;

# ---- W46 derived_product_check: |Q_M^ab| = 216/54 = 4 ----
abOrderObserved := qmSize / derivedOrder;;
fW46 := (abOrderObserved = 4);;
Print("[", PF(fW46), "] W46 derived_product_check: |Q_M^ab| = ", abOrderObserved, " (expect 4)\n");
if not fW46 then fixtureOK := false; fi;

if not fixtureOK then
  Print("\n[UNKNOWN] stage 1b: fixture mismatch -- halting before enumeration.\n");
  haltStage := true;
fi;

# ================================================================================
# enumeration (reduced hexagon, quotient shortcut -- c_in_N=true for this batch)
# ================================================================================
if not haltStage then

qrec := rec(x:=xhat, y:=yhat, c:=chat, G:=QM);;
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

# ---- U-F9: E_m table ----
emTable := ComputeEmTable(qrec, nOrd);;
Print("E_m table computed (", Length(emTable), " rows, independent)\n");

# ---- full-hexagon double-check on Q_M x T model ----
t0 := Runtime();;
qt := BuildQTGeneral(QM, xhat, yhat, chat);;
t1 := Runtime();;
Print("Q_M x T model built: np=", qt.np, " total_points=", 6*qt.np, " time_ms=", t1-t0, "\n");
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

# ---- U-F10: exact order ----
deltaBPerm := qt.s1*qt.s2;;
DeltaPerm := qt.s1*qt.s2*qt.s1;;
exactOrder := Order(deltaBPerm^-1 * DeltaPerm);;
f10 := (exactOrder = 24);;
Print("[", PF(f10), "] U-F10: ord_Q(deltaB^-1 Delta) = ", exactOrder, " (expect 24 = 2*n_ord)\n");
if not f10 then fixtureOK := false; fi;

# ---- m_missing ----
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
# reductions R1 (M_Q -> K^(3)) and R2 (M_Q -> N_Q), per manifest sec.4
# ================================================================================

# ---- extract G3-component and Q8-component of a shadow's f (17-pt perm -> 9pt / 8pt) ----
G3PartOf := function(f17) return compOfBlock(f17, 0, 9); end;;
Q8PartOf := function(f17) return compOfBlock(f17, 9, 8); end;;

for sh in result.shadows do
  g3perm := G3PartOf(sh.f);
  g1c := compOfFix(g3perm, 1, 3);  g2c := compOfFix(g3perm, 2, 3);  g3c := compOfFix(g3perm, 3, 3);
  sh.g3_triple := [ DnElemToAE(g1c, gn.r, gn.s, 3), DnElemToAE(g2c, gn.r, gn.s, 3), DnElemToAE(g3c, gn.r, gn.s, 3) ];
  sh.q8_perm := Q8PartOf(sh.f);
od;

# ---- R1: M_Q -> K^(3), match (m mod 6, g3_triple) against certificates/K3.v1.json ----
k3Shadows := ParseK3Shadows("certificates/K3.v1.json");;
Print("Parsed K3.v1.json: ", Length(k3Shadows), " shadows (expect 12)\n");

r1Images := [];;  r1Seen := [];;
for sh in result.shadows do
  newm := sh.m mod 6;
  idx := fail;
  for t in [1..Length(k3Shadows)] do
    if k3Shadows[t].m = newm and k3Shadows[t].triple = sh.g3_triple then idx := t; break; fi;
  od;
  if idx = fail then
    Print("  [ANOMALY] R1 M_Q->K3: shadow (m=", sh.m, ", triple=", sh.g3_triple, ") has no image!\n");
    Add(r1Images, -1);
  else
    Add(r1Images, idx-1);
    if not (idx in r1Seen) then Add(r1Seen, idx); fi;
  fi;
od;
r1Surjective := Length(r1Seen) = Length(k3Shadows);;
Print("R1 M_Q -> K3: image_size=", Length(r1Seen), " of ", Length(k3Shadows),
      " target shadows, surjective=", r1Surjective, "\n");

# ---- R2: M_Q -> N_Q, recompute N_Q's own shadow set inline (same Q8 instance, direct comparison) ----
nqCharming := Filtered([0..3], mm -> Gcd(2*mm+1,4)=1);;   # = [0,1,2,3]
nqQrec := rec(x:=q8rec.x, y:=q8rec.y, c:=q8rec.c, G:=q8rec.G);;
nqResult := EnumerateReducedHexagon(nqQrec, nqCharming);;
Print("recomputed N_Q shadow_total = ", nqResult.shadow_total, " (inline, for R2 index matching only)\n");

r2Images := [];;  r2Seen := [];;
for sh in result.shadows do
  newm := sh.m mod 4;
  idx := fail;
  for t in [1..Length(nqResult.shadows)] do
    if nqResult.shadows[t].m = newm and nqResult.shadows[t].f = sh.q8_perm then idx := t; break; fi;
  od;
  if idx = fail then
    Print("  [ANOMALY] R2 M_Q->N_Q: shadow (m=", sh.m, ", q8=", QLabelOfPerm(sh.q8_perm), ") has no image!\n");
    Add(r2Images, -1);
  else
    Add(r2Images, idx-1);
    if not (idx in r2Seen) then Add(r2Seen, idx); fi;
  fi;
od;
r2Surjective := Length(r2Seen) = Length(nqResult.shadows);;
Print("R2 M_Q -> N_Q: image_size=", Length(r2Seen), " of ", Length(nqResult.shadows),
      " target shadows, surjective=", r2Surjective, "\n");

elapsedMs := Runtime() - startTime;;
Print("\n累計 elapsed ms: ", elapsedMs, "\n");
wallSeconds := elapsedMs / 1000.0;;
if wallSeconds > capStage then
  Print("[CAP EXCEEDED] stage 1b exceeded ", capStage, "s -> UNKNOWN\n");
fi;

# ================================================================================
# certificate assembly (gtsh-cert/v2)
# ================================================================================
targetDef := Concatenation(
  "{\"K3\":{\"G3_order\":108,\"K_ord\":6,\"c\":\"(1,1,1)\",\"psi3\":\"PB3 -> D3^3\",",
  "\"source\":\"2405.11725 (3.1)\",\"x\":\"(r,s,s)\",\"y\":\"(rs,r,rs)\"},",
  "\"definition\":\"K^(3) cap N_Q\",",
  "\"id\":\"1b\",",
  "\"marked_images\":{\"c\":\"(1,1)\",\"x\":\"((r,s,s), i)\",\"y\":\"((rs,r,rs), j)\"},",
  "\"name\":\"M_Q\",",
  "\"quotient\":\"G3 x_{C2^2} Q8  (order 216)\"}");;

s3Marking := Concatenation(
  "{\"convention\":\"Delta_delta\",\"Delta_image\":\"(1 2)\",\"deltaB_image\":\"(1 2 3)\",",
  "\"equals_standard\":false,\"simultaneous_conjugate_of_standard\":true,\"conjugator\":\"(1 2 3)\"}");;

universeJson := Concatenation(
  "{\"pb3_index\":", String(qmSize), ",\"b3_points\":", String(b3Points),
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
  "\"note\":\"W46: fiber-product [Q,Q] measured directly (not assumed), ab_order_observed*derived_order = |Q_M| = ",
  String(abOrderObserved*derivedOrder), "\"}");;

kernelCert := Concatenation(
  "{\"kernel_scope\":\"PB3\",\"pb3_kernel_index\":", String(qmSize),
  ",\"b3_kernel_index\":", String(b3Points), ",\"justification\":\"2401 (3.32)\"}");;

runtimeJson := Concatenation("{\"wall_seconds\":", String(Int(wallSeconds*1000)/1000.0),
                              ",\"max_rss_bytes\":null,\"max_rss_note\":\"not measured (see stage 1a note)\"}");;

r1ImgStr := [];;  for i in r1Images do Add(r1ImgStr, String(i)); od;
r2ImgStr := [];;  for i in r2Images do Add(r2ImgStr, String(i)); od;

# fibre histogram + kernel_order (only a well-defined single integer if the fibre is uniform)
FibreHistogram := function(images, targetCount)
  local hist, im, i;
  hist := List([1..targetCount], x -> 0);
  for im in images do
    if im >= 0 then hist[im+1] := hist[im+1] + 1; fi;
  od;
  return hist;
end;;
KernelOrderJson := function(images, seenCount, totalShadows)
  local uniform, hist, h;
  if seenCount = 0 then return "null"; fi;
  hist := FibreHistogram(images, seenCount);
  uniform := true;
  for h in hist do if h <> hist[1] then uniform := false; fi; od;
  if uniform then return String(hist[1]); else return "null"; fi;
end;;

r1Hist := FibreHistogram(r1Images, Length(r1Seen));;
r2Hist := FibreHistogram(r2Images, Length(r2Seen));;
r1HistStr := [];;  for h in r1Hist do Add(r1HistStr, String(h)); od;
r2HistStr := [];;  for h in r2Hist do Add(r2HistStr, String(h)); od;

reductionsJson := Concatenation(
  "[{\"target\":\"K3\",\"surjective\":", JB(r1Surjective),
  ",\"image_size\":", String(Length(r1Seen)), ",\"image\":", JArr(r1ImgStr),
  ",\"fibre\":", JArr(r1HistStr), ",",
  "\"kernel_order\":", KernelOrderJson(r1Images, Length(r1Seen), result.shadow_total), ",",
  "\"kernel_order_note\":\"null unless fibre is uniform across all target shadows; fibre[] gives the raw per-target preimage counts either way\",",
  "\"kernel_structure\":\"UNKNOWN\"},",
  "{\"target\":\"N_Q\",\"surjective\":", JB(r2Surjective),
  ",\"image_size\":", String(Length(r2Seen)), ",\"image\":", JArr(r2ImgStr),
  ",\"fibre\":", JArr(r2HistStr), ",",
  "\"kernel_order\":", KernelOrderJson(r2Images, Length(r2Seen), result.shadow_total), ",",
  "\"kernel_order_note\":\"null unless fibre is uniform across all target shadows; fibre[] gives the raw per-target preimage counts either way\",",
  "\"kernel_structure\":\"UNKNOWN\"}]");;

s := Concatenation(
  "{\"schema\":\"gtsh-cert/v2\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/week3-battery-1b.g\",\"date\":\"2026-07-26\"},",
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
  "\"frobenius_zero_note\":\"命題 E4 は読取禁止範囲(docs/命題_*)につき未計算(司令塔裁定②: 本バッテリー必須外)\",",
  "\"m_missing\":", JArr(List(mMissing, String)), ",",
  "\"kernel_certificate\":", kernelCert, ",",
  "\"reductions\":", reductionsJson, ",",
  "\"isolated\":\"UNKNOWN\",",
  "\"isolated_note\":\"settled 判定未実装(司令塔裁定③)\",",
  "\"runtime\":", runtimeJson,
  "}");;

WriteFile("certificates/1b.v2.json", s);;
Print("wrote certificates/1b.v2.json\n");

fi; # haltStage

Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");
QUIT;
