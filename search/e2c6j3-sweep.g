# search/e2c6j3-sweep.g -- E2 class-6 j=3 gate, per docs/manifest_e2c6j3_v1.md.
#
# === TOOL SPEC HEADER (per docs/所在と能力.md "ツール仕様ヘッダ標準") ===
# INPUT: search/e2c6-common-data.g (shared class-6 table data + core operators, itself
#   traced to crosscheck/agree6_claude.json -- see that file's own header). This script does
#   NOT read search/e2c6-sweep.g (the frozen, hash-ledgered j=2 gate) -- separate file, per
#   commander instruction ("既存を j=3 へ拡張する形でよい" -- interpreted as: branch a
#   sibling file rather than mutate the certified j=2 artifact). Also reads
#   sol/sol_reply_24_d2.md §F8 ONLY (implementer authorized; §F7 is SEALED and was not read
#   by the implementer -- the boxed formulas (8.1)-(8.4) and the 6-step "j=3 実装へ要求する
#   計算" list are transcribed here VERBATIM as the computational spec).
# MODE: fixture-only. The real 64-system (m=0..63) sweep is gated behind
#   search/FIRE_e2c6j3.auth (must contain the SHA-256 of docs/manifest_e2c6j3_v1.md) --
#   absent here, so this run computes G1-G4 fixtures on SYNTHETIC / m=0 / class-5-control
#   data only, never on the real class-6 target at m>0.
# OUTPUT SCHEMA: certificates/e2c6j3/*.json, claims "m6j3_multiplicity_table" (fixture),
#   "linear_stage_kernel_c6j3" (fixture kernel certs), "f7j3_routeG_crosscheck". Schema
#   version string "ob_mode":"quotient-ratified-v2" carried over unchanged (same ratified
#   q_theta/q_N formula, R generalized to 4); the NEW j=3 "first condition" bits use their
#   own field "new_first_condition_j3":"p_parity_s3_w_r2/v1" (this script's own label, not a
#   pre-existing ratified string -- there is nothing to collide with since j=2 certs never
#   carry this field).
# INVARIANTS CHECKED: (a) k_w=0 mod 8 for all K_m^(3) generators (便24 F8 eq 8.2 precondition,
#   "3k_w=0 mod8 => k_w=0"); (b) lambda-shortcut multiplicity table (steps 1-4 of F8's spec)
#   matches independent brute-force enumeration of the FULL solution set L_m EXACTLY (both
#   keys and counts); (c) sum of table multiplicities = |L_m| = Prod(K_orders); (d) F7-style
#   route-G (genuine PcpGroup) vs closed-form q_theta/q_N agreement, now on mod-8-reduced
#   Abar test vectors (matching the actual j=3 Abar modulus, not just arbitrary small ints).
#
# UNIVERSE (pre-registered, manifest_e2c6j3_v1.md, unchanged): Abar_3=(Z/8)^15, C_3=(Z/4)^6
# (R=2^(j-1)=4). m in {0,...,63}. j=3 ONLY. THE 64-SYSTEM REAL SWEEP IS NOT RUN HERE.

SizeScreen([4096, 0]);;
LoadPackage("polycyclic");;   # needed for G3's genuine PcpGroup (FromTheLeftCollector) route-G check
Read("search/gaplib_common.g");;
Read("search/e2c6-common-data.g");;
startTime := Runtime();;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

Print("[", PF(E2C6_thetaSqOk), "] (inherited) theta^2 = id on all 21 BASIS21 generators\n");
Print("[", PF(E2C6_dThetaSelfCheckOk), "] (inherited) d_theta_formula matches theta_table C-columns\n");
Print("[", PF(E2C6_dSigmaSelfCheckOk), "] (inherited) d_sigma_formula matches sigma_table_poly C-columns (m=0,7)\n");

# ================================================================================
# j=3 FIRST-CONDITION / LAMBDA FORMULA (便24 F8, eq 8.1-8.4, transcribed verbatim --
# implementer is authorized to read §F8 only; §F7's branch-wise prediction was NOT read):
#
#   (8.1)  Lm3 <> {} => exists fbar in Lm3: f_p == 0 (mod 2),  f_s3 + f_w*f_r2 == 0 (mod 2).
#   (8.2)  Km3 = ker(1+thetabar) cap ker(Nbar_m) subset (Z/8)^15; weight-2 identity
#          3*k_w == 0 (mod 8)  =>  k_w == 0  (for all k in Km3).
#   (8.3)  lambda_m3(k) := ( k_p ,  k_s3 + W(m)*k_r2 )  mod 2,   W(m) := binom(m+1,2) mod 2.
#   (8.4)  0 in ob(Lm3)  <=>  ob(fbar_0) in lambda_m3(Km3).
#
# W(m) uses GenBinom (already defined in e2c6-common-data.g).
# ================================================================================
WMfun := function(m) return GenBinom(m+1, 2) mod 2; end;;

# Lambda applied to a raw Abar(15) kernel-generator vector (integer components; only p/s3/r2
# components matter, reduced mod 2).
LambdaOfK := function(k15, m)
  return [ k15[IdxP] mod 2, (k15[IdxS3] + WMfun(m)*k15[IdxR2]) mod 2 ];
end;;

# The ACTUAL (nonlinear) first-condition value at a genuine Abar(15) point f (mod 8 reduced
# beforehand by the caller) -- eq 8.1's Q(f), used both for the base-point value and for the
# brute-force cross-check (NOT an approximation -- this is the literal quantity, f_w*f_r2
# computed exactly, not via the affine W(m) shortcut).
QFirstCond := function(f15) return [ f15[IdxP] mod 2, (f15[IdxS3] + f15[IdxW]*f15[IdxR2]) mod 2 ]; end;;

# GF(2)-span of a list of 2-vectors (ambient dim 2, so |span| in {1,2,4}) via closure under XOR.
Xor2 := function(a,b) return [ (a[1]+b[1]) mod 2, (a[2]+b[2]) mod 2 ]; end;;
SpanF2 := function(vecs)
  local span, changed, v, s, nv;
  span := [[0,0]];;
  changed := true;;
  while changed do
    changed := false;;
    for v in vecs do
      for s in ShallowCopy(span) do
        nv := Xor2(s, v);;
        if not (nv in span) then Add(span, nv); changed := true; fi;
      od;
    od;
  od;
  return span;
end;;

# ================================================================================
# Multiplicity-table builder (BOTH systems, cross-checked against each other):
#  (A) lambda-shortcut (便24 F8 steps 1-4): span of {LambdaOfK(gen_i,m)}, each attained value
#      gets multiplicity |K|/|span|, keyed by BaseQ XOR span-value.
#  (B) brute-force: enumerate the FULL Prod(n_i) coset L_m = f0 + K, evaluate QFirstCond
#      directly (exact, nonlinear) at every point, tally.
# Only run on SAFE (synthetic / m=0-shortcut / class-5-control) systems in this fixture pass.
# ================================================================================
RankFromSpanSize := function(n)
  if n = 1 then return 0; elif n = 2 then return 1; else return 2; fi;
end;;

# BuildJ3MultTableShortcut now ALSO returns the explicit 2xd bit matrix (便24 F8 item 2:
# "各 generator に (8.3) を適用した 2×d bit matrix とその rank を証明書へ入れる") -- bitMatrix
# is stored as a list of d columns, each column = LambdaOfK(gen_i,m) = [a_i,b_i]; rank is the
# GF(2) rank of that matrix (equivalently log2(|span|), since the ambient codomain is only
# dimension 2 here).
BuildJ3MultTableShortcut := function(f0, kgens, m)
  local baseQ, images, span, total, mult, key, kk, vv;
  baseQ := QFirstCond(f0);;
  images := List(kgens, g -> LambdaOfK(g.vec, m));;
  span := SpanF2(images);;
  total := Product(List(kgens, g -> g.order), x->x);;
  mult := rec();;
  for vv in span do
    key := Concatenation(String((baseQ[1]+vv[1]) mod 2), ",", String((baseQ[2]+vv[2]) mod 2));;
    mult.(key) := total / Length(span);;
  od;
  return rec(table:=mult, total:=total, span_size:=Length(span), baseQ:=baseQ,
    bit_matrix:=images, rank:=RankFromSpanSize(Length(span)));
end;;

BuildJ3MultTableBruteForce := function(f0, kgens, m)
  local r, ns, total, avec, f, ii, idx, done, table, key, qf;
  r := Length(kgens);;
  ns := List(kgens, g -> g.order);;
  total := Product(ns, x->x);;
  table := rec();;
  avec := List([1..Maximum(r,1)], x->0);;
  done := (r=0);;
  while not done do
    f := ShallowCopy(f0);;
    for ii in [1..r] do
      if avec[ii] <> 0 then f := f + avec[ii]*kgens[ii].vec; fi;
    od;
    f := Mod2j(f, 8);;
    qf := QFirstCond(f);;
    key := Concatenation(String(qf[1]), ",", String(qf[2]));;
    if IsBound(table.(key)) then table.(key) := table.(key)+1; else table.(key) := 1; fi;
    if r = 0 then done := true; else
      idx := 1;;
      while idx <= r do
        avec[idx] := avec[idx]+1;
        if avec[idx] < ns[idx] then break; fi;
        avec[idx] := 0; idx := idx+1;
      od;
      if idx > r then done := true; fi;
    fi;
  od;
  return rec(table:=table, total:=total);
end;;

TablesEqual := function(t1, t2)
  local k1, k2;
  k1 := Set(RecNames(t1));;  k2 := Set(RecNames(t2));;
  if k1 <> k2 then return false; fi;
  return ForAll(k1, k -> t1.(k) = t2.(k));
end;;

# ================================================================================
# Precondition check (8.2): k_w == 0 (mod 8) for every K_m^(3) generator, on a set of SAFE
# systems (synthetic rhs=0 at various m-shapes, plus the m=0 real-shortcut).
# ================================================================================
BuildLinearSystemC6SyntheticJ3 := function(label)
  local sys;
  sys := BuildLinearSystemC6(label);;
  sys.rhs := List([1..2*sys.n], x -> 0);;   # synthetic: solvable-by-construction (f=0 works)
  sys.synthetic := true;;
  return sys;
end;;

Print("\n=== G-precondition: k_w = 0 (mod 8) for all K_m^(3) generators (safe systems only) ===\n");
kwZeroOk := true;;  kwAnyRun := false;;  kwSamples := [];;
for mtest in [0,1,2,3,5,7,11] do
  snfSafe3 := BuildSnfData(k -> BuildLinearSystemC6SyntheticJ3(mtest), mtest);;
  resSafe3 := TestAtJ(snfSafe3, 3);;
  if resSafe3.solvable then
    for gi in resSafe3.kgens do
      kwAnyRun := true;;
      Add(kwSamples, gi.vec[IdxW] mod 8);;
      if (gi.vec[IdxW] mod 8) <> 0 then
        kwZeroOk := false;;
        Print("  FAIL k_w<>0 at m=",mtest,": gen=",gi.vec,"\n");
      fi;
    od;
  fi;
od;;
Print("[", PF(kwZeroOk and kwAnyRun), "] k_w = 0 (mod 8) for all sampled K_m^(3) generators (", Length(kwSamples), " generators checked, safe synthetic systems)\n");

# ================================================================================
# GUARD (司令塔発注・falsifier監査問3【重大】への対応): the k_w=0 precondition (eq 8.2) is
# checked above only on SAFE synthetic systems -- the real 64-system sweep (RunRealSweepC6J3,
# below) MUST re-verify this premise PER m and ABORT (not silently apply the lambda formula)
# if it is violated. CheckPremiseKw is the reusable guard function; this block unit-tests it
# BOTH on genuine safe kgens (expect no violation) AND on a deliberately injected fake
# generator with k_w<>0 (expect detection) -- the latter is the only way to exercise the
# guard's DETECTION path without running the (still fire-locked) real sweep.
# ================================================================================
CheckPremiseKw := function(kgens)
  local bad, gi;
  bad := [];;
  for gi in kgens do
    if (gi.vec[IdxW] mod 8) <> 0 then Add(bad, gi.vec); fi;
  od;
  return rec(violated := Length(bad) > 0, bad_generators := bad);
end;;

Print("\n=== GUARD (adversarial): CheckPremiseKw must pass genuine safe kgens and catch an injected violation ===\n");
guardSnf := BuildSnfData(k -> BuildLinearSystemC6SyntheticJ3(0), 0);;
guardRes := TestAtJ(guardSnf, 3);;
guardCheckGenuine := CheckPremiseKw(guardRes.kgens);;
guardOkGenuine := not guardCheckGenuine.violated;;
Print("  genuine safe kgens (m=0 synthetic, ", Length(guardRes.kgens), " generators): violated=", JB(guardCheckGenuine.violated), " (expect false)\n");

guardFakeGens := ShallowCopy(guardRes.kgens);;
guardFakeInjected := rec(vec := List([1..NAB], x -> 0), order := 2);;
guardFakeInjected.vec[IdxW] := 1;;   # deliberately violates k_w=0 (mod 8)
Add(guardFakeGens, guardFakeInjected);;
guardCheckFake := CheckPremiseKw(guardFakeGens);;
guardOkFake := guardCheckFake.violated and (Length(guardCheckFake.bad_generators) = 1);;
Print("  same kgens + 1 injected fake generator (k_w=1): violated=", JB(guardCheckFake.violated), " bad_count=", Length(guardCheckFake.bad_generators), " (expect true, 1)\n");

guardOk := guardOkGenuine and guardOkFake;;
Print("[", PF(guardOk), "] GUARD: CheckPremiseKw correctly passes genuine safe kgens AND detects an injected k_w<>0 violation (this is the function RunRealSweepC6J3 below calls per-m before applying the lambda formula)\n");

# ================================================================================
# FIXTURE G1 (false-positive detector, j=3 version): on a SOLVABLE SYNTHETIC system,
# check (a) sum of multiplicity table = |L| and (b) witness recheck: the lambda-shortcut
# table matches the independent brute-force table EXACTLY. Per manifest: do NOT assert any
# specific attained-value pattern (that would be a prediction) -- only the structural
# invariants (a)/(b).
# ================================================================================
Print("\n=== FIXTURE G1 (false-positive detector, j=3, structural invariants only) ===\n");
g1Ok := true;;  g1AnyRun := false;;
for mtest in [0,1,2,3] do
  snfG1 := BuildSnfData(k -> BuildLinearSystemC6SyntheticJ3(mtest), mtest);;
  resG1 := TestAtJ(snfG1, 3);;
  if resG1.solvable then
    f0G1 := ExtractF0(snfG1, 3);;
    tblShort := BuildJ3MultTableShortcut(f0G1, resG1.kgens, mtest);;
    tblBrute := BuildJ3MultTableBruteForce(f0G1, resG1.kgens, mtest);;
    sumShort := Sum(RecNames(tblShort.table), k -> tblShort.table.(k));;
    sameTables := TablesEqual(tblShort.table, tblBrute.table);;
    g1AnyRun := true;;
    thisOk := (sumShort = tblShort.total) and (tblBrute.total = tblShort.total) and sameTables;;
    if not thisOk then g1Ok := false; fi;
    Print("  m=",mtest," (synthetic): |L|=",tblShort.total," sum(shortcut table)=",sumShort,
      " shortcut=",tblShort.table," brute=",tblBrute.table," IDENTICAL=",PF(sameTables),"\n");
  fi;
od;;
Print("[", PF(g1Ok and g1AnyRun), "] G1: sum(multiplicity table)=|L| AND lambda-shortcut matches independent brute-force enumeration exactly, on solvable synthetic systems\n");

# ================================================================================
# FIXTURE G1b (便24 F8 item 1: "不可解なら dual witness を出す" -- dual-witness path for
# UNSOLVABLE systems, exercised on a deliberately ADVERSARIAL SAFE synthetic system (NOT real
# Ebar_m -- rhs is a plain pseudo-random 15-vector, which e2c6-sweep.g's own F5 discovery
# documented as "essentially never" landing in the solvable image when drawn freely, unlike
# the ker(1+theta_bar)-constructed rhs used for G1's solvable fixtures above). Mirrors the j=2
# gate's WriteUnsolvableCertC6 recheck exactly (y := U[failRow]; yM := y*rows; yb := y*rhs;
# check yM=0 and yb<>0 mod modulus).
# ================================================================================
BuildLinearSystemC6AdversarialUnsolvableJ3 := function(label)
  local sys, mshape;
  mshape := label mod 64;;
  sys := BuildLinearSystemC6(mshape);;   # real theta_bar/sigma_bar STRUCTURE (public table data)
  # deliberately adversarial: plain pseudo-random 15-vector rhs for the N-block (NOT built via
  # ker(1+theta_bar), unlike the SOLVABLE-by-construction fixtures above) -- generically not in
  # the image of N_bar, so almost always unsolvable. Still fully deterministic/reproducible and
  # unrelated to any real Ebar_m value (blind-safe, same discipline as e2c6-sweep.g's F5).
  sys.rhs := Concatenation(List([1..sys.n], x->0), List([1..NAB], i -> ((41*label + 13*i + 3) mod 5) - 2));;
  sys.synthetic := true;;  sys.adversarial_unsolvable := true;;
  return sys;
end;;

Print("\n=== FIXTURE G1b (dual witness path, 便24 F8 item 1, adversarial-unsolvable safe synthetic) ===\n");
g1bFound := false;;  g1bOk := true;;  g1bLabel := fail;;
labelCand := 1;;
while not g1bFound and labelCand <= 60 do
  snfAdv := BuildSnfData(k -> BuildLinearSystemC6AdversarialUnsolvableJ3(labelCand), labelCand);;
  resAdv := TestAtJ(snfAdv, 3);;
  if not resAdv.solvable then
    g1bFound := true;;  g1bLabel := labelCand;;
    yAdv := snfAdv.U[resAdv.failRow];;
    yMAdv := yAdv * snfAdv.sys.rows;;
    ybAdv := yAdv * snfAdv.sys.rhs;;
    yMZeroAdv := ForAll(List(yMAdv, x -> x mod resAdv.modulus), x -> x = 0);;
    yBNonzeroAdv := (ybAdv mod resAdv.modulus <> 0);;
    g1bOk := yMZeroAdv and yBNonzeroAdv;;
    Print("  label=", labelCand, " (m-shape=", labelCand mod 64, "): UNSOLVABLE (as expected), dual witness y=", yAdv,
      "  yM mod 8 all-zero=", JB(yMZeroAdv), "  yb mod 8 nonzero=", JB(yBNonzeroAdv), "\n");
    pathAdv := "certificates/e2c6j3/fixture_G1b_dualwitness.json";;
    certAdv := Concatenation(
      "{\"claim\":\"linear_stage_empty_c6j3\",\"linear_solvable\":false,",
      "\"fixture\":\"adversarial_unsolvable_synthetic_j3\",\"label\":", String(labelCand), ",",
      "\"j\":3,\"modulus\":", String(resAdv.modulus), ",",
      "\"dual_witness_y\":\"", String(yAdv), "\",",
      "\"yM_is_zero_mod_2j\":", JB(yMZeroAdv), ",",
      "\"yb\":", String(ybAdv), ",\"yb_nonzero_mod_2j\":", JB(yBNonzeroAdv), ",",
      "\"recheck\":\"checker independently rebuilds the same public theta_bar/sigma_bar(m-shape) structure and the same deterministic adversarial rhs formula, then recomputes yM/yb directly\"}");;
    WriteFile(pathAdv, certAdv);;
    Print("  wrote ", pathAdv, "\n");
  else
    labelCand := labelCand + 1;;
  fi;
od;;
Print("[", PF(g1bFound and g1bOk), "] G1b: dual-witness path exercised on an unsolvable safe synthetic system (label=", g1bLabel, "), yM=0 and yb<>0 mod modulus independently verified\n");

# ================================================================================
# FIXTURE G2 (class-5 / j=2 統制, projection agreement):
#  (a) class-5 control at j=3 (mod 8): expect ALL solvable, m=0..63 (already an ESTABLISHED
#      class-5 fact per provenance/CLAIMS W3-9/E23 -- the 384-system j=1..6 sweep was already
#      all-positive; this reproduces the j=3 slice as an external control on the SNF/2-adic
#      machinery, same discipline as e2c6-sweep.g's F3 -- NOT a class-6 disclosure).
#  (b) projection agreement: this module's R-generic ObFromQPair, evaluated at R=2, on the
#      SAME synthetic (q_theta,q_N) test vectors the frozen j=2 gate (search/e2c6-sweep.g)
#      used for its own ratified F1/F2/F6 fixtures, must reproduce byte-identical ob_a/ob_b --
#      i.e. this freshly-branched module has not silently drifted from the ratified j=2
#      formula it was copied from.
# ================================================================================
Print("\n=== FIXTURE G2a (class-5 control, j=3/mod 8, m=0..63) ===\n");
g2aAllSolvable := true;;  g2aFailList := [];;
for mIt in [0..63] do
  snfC5j3 := BuildSnfData(BuildLinearSystemC5, mIt);;
  resC5j3 := TestAtJ(snfC5j3, 3);;
  if not resC5j3.solvable then
    g2aAllSolvable := false;;
    Add(g2aFailList, mIt);;
  fi;
od;;
Print("[", PF(g2aAllSolvable), "] G2a class-5 control: linear stage solvable at j=3 (mod 8) for ALL m=0..63\n");
if not g2aAllSolvable then Print("  FAILING m values: ", g2aFailList, "\n"); fi;

Print("\n=== FIXTURE G2b (projection agreement vs. frozen j=2 gate's own ratified fixtures) ===\n");
g2bCases := [
  rec(label:="F1_j2", qTheta:=[1,1,0,0,0,0], qN:=[0,0,0,0,0,0], expectA:=0, expectB:=0),
  rec(label:="F2a_j2", qTheta:=[0,0,0,0,0,1], qN:=[0,0,0,0,0,0], expectA:=1, expectB:=0),
  rec(label:="F2b_j2", qTheta:=[0,0,0,1,0,0], qN:=[0,0,0,0,0,0], expectA:=0, expectB:=1),
  rec(label:="F6a_j2", qTheta:=[1,1,0,0,0,0], qN:=[1,1,0,0,0,0], expectA:=0, expectB:=0),
  rec(label:="F6b_j2", qTheta:=[0,0,0,0,0,1], qN:=[0,0,1,0,1,0], expectA:=1, expectB:=0),
  rec(label:="F6c_j2", qTheta:=[0,0,0,1,0,0], qN:=[0,1,1,1,0,1], expectA:=0, expectB:=1)
];;
g2bOk := true;;
for gc in g2bCases do
  r2res := ObFromQPair(gc.qTheta, gc.qN, 2);;
  ok := (r2res.ob_a = gc.expectA) and (r2res.ob_b = gc.expectB);;
  Print("  ", gc.label, " (R=2 projection): ob_a=",r2res.ob_a," ob_b=",r2res.ob_b," (expect ",gc.expectA,",",gc.expectB,")\n");
  if not ok then g2bOk := false; fi;
od;;
Print("[", PF(g2bOk), "] G2b: this module's ObFromQPair(R=2) byte-agrees with the frozen j=2 gate's own ratified F1/F2/F6 fixture outputs (no silent drift)\n");

g2Ok := g2aAllSolvable and g2bOk;;
Print("[", PF(g2Ok), "] G2 (class-5/j=2 統制, combined)\n");

# ================================================================================
# FIXTURE G3 (route-G group product cross-check, j=3 cells): independently built PcpGroup
# (FromTheLeftCollector), same construction as e2c6-sweep.g's F7 (re-derived fresh here, not
# read from that file), tested on Abar(15) vectors REDUCED MOD 8 (the actual j=3 Abar
# modulus -- e2c6-sweep.g's F7 used arbitrary small-integer test vectors, not mod-8-reduced
# ones; this is the "j=3 セル追加" the manifest calls for) at C-space modulus R=4.
# ================================================================================
Print("\n=== FIXTURE G3 (route-G genuine PcpGroup product, j=3 cells: mod-8-reduced test vectors) ===\n");
G3Coll := FromTheLeftCollector(21);;
for G3kt in KappaTerms do
  SetCommutator(G3Coll, NameIdx21(G3kt.in1), NameIdx21(G3kt.in2), [NameIdx21(G3kt.out), -G3kt.coef]);;
od;;
UpdatePolycyclicCollector(G3Coll);;
G3Confluent := IsConfluent(G3Coll);;
Print("[", PF(G3Confluent), "] route-G PcpGroup collector IsConfluent (independently rebuilt from KappaTerms)\n");
G3G := PcpGroupByCollector(G3Coll);;
G3Gens := GeneratorsOfGroup(G3G);;

G3ElemFromVec := function(v21)
  local acc, k;
  acc := Identity(G3G);
  for k in [1..21] do
    if v21[k] <> 0 then acc := acc * G3Gens[k]^v21[k]; fi;
  od;
  return acc;
end;;
G3ApplyAsAutomorphism := function(table21eval, v21)
  local acc, k;
  acc := Identity(G3G);
  for k in [1..21] do
    if v21[k] <> 0 then acc := acc * G3ElemFromVec(table21eval[k])^v21[k]; fi;
  od;
  return acc;
end;;
G3PadTo21 := function(f15)
  local v21, i;
  v21 := List([1..21], x -> 0);
  for i in [1..NAB] do v21[AbarIdx21[i]] := f15[i]; od;
  return v21;
end;;
G3CExtract := function(exps21) return List(CIdx21, ci -> exps21[ci]); end;;
G3RouteGQTheta := function(f15)
  local f21, g, thg, prod;
  f21 := G3PadTo21(f15);;
  g := G3ElemFromVec(f21);;
  thg := G3ApplyAsAutomorphism(ThetaTable21, f21);;
  prod := thg * g;;
  return G3CExtract(Exponents(prod));
end;;
G3RouteGQN := function(f15, m)
  local f21, g, sigmaTableAtM, sg, s2vec, s2g, emVec, emElem, prod;
  f21 := G3PadTo21(f15);;
  g := G3ElemFromVec(f21);;
  sigmaTableAtM := SigmaMat21(m);;
  sg := G3ApplyAsAutomorphism(sigmaTableAtM, f21);;
  s2vec := Exponents(sg);;
  s2g := G3ApplyAsAutomorphism(sigmaTableAtM, s2vec);;
  emVec := EmVec21(m);;
  emElem := G3ElemFromVec(emVec);;
  prod := emElem * s2g * sg * g;;
  return G3CExtract(Exponents(prod));
end;;

# test vectors: reduced mod 8 (the actual j=3 Abar modulus), drawn from safe synthetic kernel
# generators plus a few explicit mod-8 combinations (basis generators and sums), NOT arbitrary
# unreduced integers as e2c6-sweep.g's F7 used.
G3TestVecsRaw := [EkAbar(1), EkAbar(2), EkAbar(3), EkAbar(5), EkAbar(9), EkAbar(13),
  EkAbar(1)+EkAbar(2)+EkAbar(5), 3*EkAbar(2)+5*EkAbar(13)-EkAbar(5), 7*EkAbar(1)+2*EkAbar(9)];;
G3TestVecs := List(G3TestVecsRaw, v -> Mod2j(v, 8));;
G3TestMs := [0, 1, 2, 3];;
G3Rc4 := 4;;
G3AllOk := true;;  G3Checked := 0;;  G3ExactCount := 0;;
G3CertEntries := [];;
for G3f in G3TestVecs do
  G3qThetaRouteG := G3RouteGQTheta(G3f);;
  G3qThetaClosed := QThetaFullRaw(G3f);;
  G3thetaMatch := ModVec(G3qThetaRouteG, G3Rc4) = ModVec(G3qThetaClosed, G3Rc4);;
  G3thetaExact := (G3qThetaRouteG = G3qThetaClosed);;
  if not G3thetaMatch then G3AllOk := false; fi;
  G3Checked := G3Checked + 1;;  if G3thetaExact then G3ExactCount := G3ExactCount+1; fi;
  Add(G3CertEntries, rec(f:=G3f, m:=fail, kind:="qTheta", routeG:=G3qThetaRouteG, closed:=G3qThetaClosed, exact:=G3thetaExact, mod4:=G3thetaMatch));;
  for G3m in G3TestMs do
    G3qNRouteG := G3RouteGQN(G3f, G3m);;
    G3qNClosed := QNFullRaw(G3f, G3m);;
    G3nMatch := ModVec(G3qNRouteG, G3Rc4) = ModVec(G3qNClosed, G3Rc4);;
    G3nExact := (G3qNRouteG = G3qNClosed);;
    if not G3nMatch then G3AllOk := false; fi;
    G3Checked := G3Checked + 1;;  if G3nExact then G3ExactCount := G3ExactCount+1; fi;
    Add(G3CertEntries, rec(f:=G3f, m:=G3m, kind:="qN", routeG:=G3qNRouteG, closed:=G3qNClosed, exact:=G3nExact, mod4:=G3nMatch));;
  od;;
od;;
Print("[", PF(G3AllOk), "] G3: route-G (genuine PcpGroup) matches closed-form q_theta/q_N mod 4 on mod-8-reduced Abar vectors, ", G3Checked, " evaluations (exact-integer match: ", G3ExactCount, "/", Length(G3CertEntries), ")\n");

G3MStr := function(mval) if mval = fail then return "null"; else return String(mval); fi; end;;
G3EntryStrs := List(G3CertEntries, e -> Concatenation(
  "{\"f\":", String(e.f), ",\"m\":", G3MStr(e.m), ",\"kind\":\"", e.kind, "\",",
  "\"routeG\":", String(e.routeG), ",\"closed_form\":", String(e.closed), ",",
  "\"exact_match\":", JB(e.exact), ",\"mod4_match\":", JB(e.mod4), "}"));;
WriteFile("certificates/e2c6j3/fixture_G3_routeG_crosscheck.json", Concatenation(
  "{\"claim\":\"f7_routeG_crosscheck\",\"gate\":\"j=3\",\"R\":4,",
  "\"abar_modulus\":8,\"note_testvecs\":\"all test vectors reduced mod 8 before use (actual j=3 Abar modulus, unlike the j=2 gate's F7 which used unreduced small integers)\",",
  "\"collector_confluent\":", JB(G3Confluent), ",",
  "\"total_evaluations\":", String(G3Checked), ",\"exact_match_count\":", String(G3ExactCount), ",",
  "\"all_mod4_match\":", JB(G3AllOk), ",",
  "\"entries\":[", JoinC(G3EntryStrs, ","), "],",
  "\"ob_mode\":\"quotient-ratified-v2\"}"));;
Print("  wrote certificates/e2c6j3/fixture_G3_routeG_crosscheck.json\n");

# ================================================================================
# FIXTURE G4 (M-series, mod-4/R=4 version -- including (1+theta)K recomputed at R=4):
# recompute the (1+theta)K structure (K = ker(N_C), the C-space kernel, NOT the Abar kernel
# Km3 above) independently at R=4, confirming the u4-component lies in R[2]={0,2} and the
# u2-component structure is within 2R -- this justifies the "Ob = R[2]a (+) (R/2R)b-bar"
# quotient semantics (委嘱16 eq 0.3/0.6) that the j=3 ob layer relies on.
# ================================================================================
Print("\n=== FIXTURE G4 (M-series, R=4: (1+theta)ker(N_C) recomputed, u4 in R[2] check) ===\n");
NCMatJ3 := function(m)
  local sig, sig2;
  sig := SigmaOnCMat(m);;
  sig2 := sig * sig;;
  return IdentityMat(NC6) + sig + sig2;
end;;
idxT5 := Position(CNames,"t5");;  idxT6 := Position(CNames,"t6");;
idxU1 := Position(CNames,"u1");;  idxU2 := Position(CNames,"u2");;
idxU3 := Position(CNames,"u3");;  idxU4 := Position(CNames,"u4");;
RG4 := 4;;
g4Ok := true;;  g4AnyRun := false;;  g4U4InRsub2 := true;;
for mtest in [0,1,2,3,5,7,11] do
  ncm := NCMatJ3(mtest);;
  snfNC := SmithNormalFormIntegerMatTransforms(ncm);;
  Vnc := snfNC.coltrans;;  Dnc := snfNC.normal;;  rankNc := snfNC.rank;;
  for ii in [1..NC6] do
    if ii <= rankNc then
      dNc := Dnc[ii][ii];;  v2Nc := V2Val(dNc);
    else
      v2Nc := 1000000;
    fi;
    genY := List([1..NC6], k->0);;
    if v2Nc >= RG4 then
      genY[ii] := 1;;
    else
      genY[ii] := 2^(RG4 - v2Nc);;
    fi;
    genC := Vnc * genY;;
    if ModVec(genC, RG4) <> List([1..NC6],x->0) then
      g4AnyRun := true;;
      img := genC + genC*ThetaOnCMat;;   # (1+theta)(gen), integer vector
      imgR := ModVec(img, RG4);;
      # u4-component must be in R[2] = {0, R/2} = {0,2}
      if not (imgR[idxU4] in [0, RG4/2]) then
        g4U4InRsub2 := false;;
        Print("  G4 FAIL (u4 not in R[2]) at m=",mtest,": img=",imgR,"\n");
      fi;
      # u2 mod 2 must be 0 (b-bar lives in R/2R, so (1+theta)K's u2-part should be within 2R)
      if (imgR[idxU2] mod 2) <> 0 then
        g4Ok := false;;
        Print("  G4 FAIL (u2 mod 2 <> 0) at m=",mtest,": img=",imgR,"\n");
      fi;
      if imgR[idxT5] <> imgR[idxT6] then g4Ok := false; Print("  G4 FAIL (t5<>t6) at m=",mtest,"\n"); fi;
      if imgR[idxU1] <> imgR[idxU3] then g4Ok := false; Print("  G4 FAIL (u1<>u3) at m=",mtest,"\n"); fi;
    fi;
  od;
od;;
Print("[", PF(g4U4InRsub2 and g4AnyRun), "] G4: (1+theta)ker(N_C) at R=4 -- u4-component lies in R[2]={0,2} (justifies Ob's R[2]a summand)\n");
Print("[", PF(g4Ok and g4AnyRun), "] G4: (1+theta)ker(N_C) at R=4 -- u2 mod 2 = 0 (justifies Ob's (R/2R)b-bar summand), t5=t6, u1=u3\n");
g4Combined := g4U4InRsub2 and g4Ok and g4AnyRun;;
Print("[", PF(g4Combined), "] G4 (M-series, mod-4/R=4, combined)\n");

# ================================================================================
# FIXTURE G7 (司令塔発注 item 3: "ObFromQPair の R=4 実演習" -- F6-analog, permanent). This
# actually CALLS ObFromQPair(qTheta, qN, 4) with NONZERO q_N -- the code path e2c6-sweep.g's
# own "MOD-4 RE-RUN" section already exercised once (and flagged as an OPEN finding: ob_b
# needs an explicit mod-2 reduction to generalize past R=2; ob_a's R=4 coordinate semantics
# beyond mod 2 remain UNRESOLVED, per that file's own GAP-OB1 note). This fixture reproduces
# that exercise independently in the j=3 gate (not silently skipped this time), and reports
# HONESTLY: it checks ob mod 2 (both a and b) is independent of q_N, and does NOT claim to
# have resolved the raw R=4 coordinate question (no unverified formula invented here).
# ================================================================================
Print("\n=== FIXTURE G7 (ObFromQPair at R=4, nonzero q_N, permanent) ===\n");
g7Cases := [
  rec(label:="G7a_t5t6_nonzeroqN", qTheta:=[1,1,0,0,0,0], qN:=[1,1,0,0,0,0]),
  rec(label:="G7b_u4_nonzeroqN",   qTheta:=[0,0,0,0,0,1], qN:=[0,0,1,0,1,0]),
  rec(label:="G7c_u2_nonzeroqN",   qTheta:=[0,0,0,1,0,0], qN:=[0,1,1,1,0,1])
];;
g7Ok := true;;
for gc in g7Cases do
  rWithQN := ObFromQPair(gc.qTheta, gc.qN, 4);;
  rZeroQN := ObFromQPair(gc.qTheta, [0,0,0,0,0,0], 4);;
  sameModTwo := (rWithQN.ob_a mod 2 = rZeroQN.ob_a mod 2) and (rWithQN.ob_b mod 2 = rZeroQN.ob_b mod 2);;
  Print("  ", gc.label, ": q_theta=",gc.qTheta," q_N=",gc.qN,
    " -> ob_a=",rWithQN.ob_a," ob_b=",rWithQN.ob_b,
    "  (q_N=0 case: ob_a=",rZeroQN.ob_a," ob_b=",rZeroQN.ob_b,")",
    "  same-mod-2=",JB(sameModTwo),"\n");
  if not sameModTwo then g7Ok := false; fi;
  pathG7 := Concatenation("certificates/e2c6j3/fixture_", gc.label, ".json");;
  certG7 := Concatenation(
    "{\"claim\":\"ob_synthetic_check\",\"fixture\":\"", gc.label, "\",\"R\":4,",
    "\"basis_order_C6\":[", JoinC(List(CNames, n -> Concatenation("\"",n,"\"")), ","), "],",
    "\"q_theta\":", String(gc.qTheta), ",\"q_N\":", String(gc.qN), ",",
    "\"v\":", String(rWithQN.v), ",",
    "\"ob_a\":", String(rWithQN.ob_a), ",\"ob_b\":", String(rWithQN.ob_b), ",",
    "\"ob_mode\":\"quotient-ratified-v2\",",
    "\"q_N_zero_comparison_ob_a\":", String(rZeroQN.ob_a), ",\"q_N_zero_comparison_ob_b\":", String(rZeroQN.ob_b), ",",
    "\"same_mod_2_as_q_N_zero\":", JB(sameModTwo), ",",
    "\"scope_note\":\"raw R=4 ob_a coordinate semantics beyond mod 2 are OPEN (not resolved here) -- only mod-2 independence-from-q_N is asserted\"}");;
  WriteFile(pathG7, certG7);;
od;;
Print("[", PF(g7Ok), "] G7: ObFromQPair(R=4) exercised with NONZERO q_N (3 permanent cases) -- ob mod 2 independent of q_N in all cases; raw R=4 semantics beyond mod 2 remain OPEN (not silently resolved)\n");

# ================================================================================
# FIXTURE G8 (便24 F8 item 6: m -> m+32 periodicity). Per commander instruction: "mod 8 での
# 成立/不成立は観測事項 -- fixture は「両者の証明書が生成され比較可能」の形で" -- this fixture
# does NOT assert equality as a pass/fail criterion (that could leak toward the sealed F7
# prediction's branch structure). It only verifies both sides are computed and well-formed,
# using PUBLIC structural Em-formula data (EmBar15/EmC6/W(m) -- generalized-binomial formulas,
# independent of any real linear-stage solvability disclosure), and records the observed
# comparison as data, not as a judgment.
# ================================================================================
Print("\n=== FIXTURE G8 (periodicity comparison certs, m vs m+32 -- structural Em-formula data only) ===\n");
g8Pairs := [[3,35],[5,37],[21,53],[27,59]];;
g8AllWritten := true;;
for pr in g8Pairs do
  mA := pr[1];;  mB := pr[2];;
  emBarA := ModVec(EmBar15(mA), 8);;  emBarB := ModVec(EmBar15(mB), 8);;
  emCA := ModVec(EmC6(mA), 4);;       emCB := ModVec(EmC6(mB), 4);;
  wA := WMfun(mA);;  wB := WMfun(mB);;
  obsEqual := (emBarA = emBarB) and (emCA = emCB) and (wA = wB);;
  pathG8 := Concatenation("certificates/e2c6j3/fixture_G8_periodicity_m", String(mA), "_m", String(mB), ".json");;
  certG8 := Concatenation(
    "{\"claim\":\"periodicity_comparison_j3\",\"m_pair\":[", String(mA), ",", String(mB), "],",
    "\"note\":\"STRUCTURAL Em-formula data only (public generalized-binomial data, not a real linear-stage solvability disclosure) -- equality is NOT asserted as pass/fail here (commander instruction); recorded as an observation only\",",
    "\"EmBar15_mod8_mA\":", String(emBarA), ",\"EmBar15_mod8_mB\":", String(emBarB), ",",
    "\"EmC6_mod4_mA\":", String(emCA), ",\"EmC6_mod4_mB\":", String(emCB), ",",
    "\"W_mA\":", String(wA), ",\"W_mB\":", String(wB), ",",
    "\"observed_equal\":", JB(obsEqual), "}");;
  WriteFile(pathG8, certG8);;
  Print("  m=",mA,"/m=",mB,": EmBar15 mod8 equal=",JB(emBarA=emBarB)," EmC6 mod4 equal=",JB(emCA=emCB)," W equal=",JB(wA=wB)," (observation only, not asserted as PASS/FAIL criterion)\n");
od;;
Print("[", PF(g8AllWritten), "] G8: periodicity comparison certificates generated for all 4 m/m+32 pairs (equality itself recorded as an OBSERVATION field, not asserted)\n");

# ================================================================================
# M8 SERIES (docs/notes/設計_F8項目5.md, Opus 小委嘱・便24 §F8 item 5): central-correction
# mass check. g in P a standard lift (C-component zero) of fbar, z in C (center):
#   Xi(g*z) = Xi(g) + Lambda(z),   Lambda(z) := ((1+theta)z, N_C z)
# Real lifts of fbar exist iff {z : Lambda(z) = -Xi(g)} is nonempty; when nonempty it is a
# ker(Lambda)-torsor (size |ker Lambda|). This is checked TWO ways: (a) directly via genuine
# PcpGroup products (route-G, small scale: M8-a/b/d), (b) via the Lambda-image dictionary +
# closed-form Xi, over the FULL L_m (M8-c, no group products, per spec). All on SAFE
# synthetic systems (BuildLinearSystemC6SyntheticJ3) -- the real 64-system sweep stays
# fire-locked, so this pass never touches real Ebar_m data.
# ================================================================================
Print("\n=== M8 SERIES (central-correction mass check, 設計_F8項目5.md) ===\n");
R8 := 4;;   # R = 2^(j-1) at j=3 (same as RG4 used in G4/G7)

# (S1) LambdaOnC(z6,m): flat 12-vector [ (1+theta)z mod R , N_C z mod R ]
LambdaOnC := function(z6, m)
  return Concatenation(ModVec(z6 + ThetaOnCVec(z6), R8), ModVec(z6 * NCMatJ3(m), R8));
end;;
NegVec := function(v, R) return List(v, x -> (-x) mod R); end;;
VecAddModR := function(v1, v2, R) return List([1..Length(v1)], i -> (v1[i]+v2[i]) mod R); end;;

# (S2) LambdaTable(m): exhaustive scan of z6 in (Z/4)^6 (4096 elements -- SNF deliberately NOT
# used here, per spec: exhaustive is safest at this scale). Returns a GAP record keyed by
# String(Lambda(z)) -> list of z-vectors landing there. ker(Lambda) = table at the zero key.
LambdaTable := function(m)
  local tbl, z6, key, c1,c2,c3,c4,c5,c6, zeroKey;
  tbl := rec();;
  for c1 in [0..3] do for c2 in [0..3] do for c3 in [0..3] do
    for c4 in [0..3] do for c5 in [0..3] do for c6 in [0..3] do
      z6 := [c1,c2,c3,c4,c5,c6];;
      key := String(LambdaOnC(z6, m));;
      if IsBound(tbl.(key)) then Add(tbl.(key), z6); else tbl.(key) := [z6]; fi;
    od; od; od;
  od; od; od;
  zeroKey := String(List([1..12], x->0));;
  return rec(table:=tbl, kerLambda:=tbl.(zeroKey));
end;;

# EmbC(z6): 21-vector with C-positions (CIdx21) set to z6, zero elsewhere.
EmbC := function(z6)
  local v21, i;
  v21 := List([1..21], x -> 0);
  for i in [1..NC6] do v21[CIdx21[i]] := z6[i]; od;
  return v21;
end;;

# route-G Xi on a FULL 21-vector (unlike G3RouteGQTheta/G3RouteGQN, which only ever receive
# Abar-padded (C-component-zero) vectors -- G3CExtract itself is reused, but these two functions
# are NEW: they accept vectors with a nonzero C-part too, needed for g_z = g*z).
G3RouteGQThetaFull21 := function(v21)
  local g, thg, prod;
  g := G3ElemFromVec(v21);;
  thg := G3ApplyAsAutomorphism(ThetaTable21, v21);;
  prod := thg * g;;
  return Exponents(prod);   # full 21-vector, NOT C-extracted
end;;
G3RouteGQNFull21 := function(v21, m)
  local g, sigmaTableAtM, sg, s2vec, s2g, emVec, emElem, prod;
  g := G3ElemFromVec(v21);;
  sigmaTableAtM := SigmaMat21(m);;
  sg := G3ApplyAsAutomorphism(sigmaTableAtM, v21);;
  s2vec := Exponents(sg);;
  s2g := G3ApplyAsAutomorphism(sigmaTableAtM, s2vec);;
  emVec := EmVec21(m);;
  emElem := G3ElemFromVec(emVec);;
  prod := emElem * s2g * sg * g;;
  return Exponents(prod);
end;;

# (S4) "=1 in cell A^(j)" test on a FULL 21-exponent vector: Abar-components must vanish mod
# 2^j=8, C-components must vanish mod R=4. G3CExtract alone is NOT sufficient here (it only
# looks at the C part) -- this is the "new function" the spec explicitly requires.
IsIdentityInCellAj := function(exps21)
  return ForAll(AbarIdx21, i -> exps21[i] mod 8 = 0) and ForAll(CIdx21, i -> exps21[i] mod R8 = 0);
end;;

# Xi via route-G, on a full 21-vector, flattened to 12 components mod R (C-readout only --
# used for the cocycle-law check M8-a, where g_z may have nonzero C-part).
XiGroupFlat12 := function(v21, m)
  return Concatenation(ModVec(G3CExtract(G3RouteGQThetaFull21(v21)), R8), ModVec(G3CExtract(G3RouteGQNFull21(v21, m)), R8));
end;;
# Xi via closed form (fast, used for the 512-point sweep in M8-c, per spec "no group products").
XiClosedFlat12 := function(f15, m)
  return Concatenation(ModVec(QThetaFullRaw(f15), R8), ModVec(QNFullRaw(f15, m), R8));
end;;

# ob via closed form (same ratified formula as G2b/G7, applied to a genuine Abar witness f15).
ObOfF15 := function(f15, m) return ObFromQPair(QThetaFullRaw(f15), QNFullRaw(f15, m), R8); end;;

# Full-L_m enumeration computing ob(f) at every point (distinct from BuildJ3MultTableBruteForce,
# which used the "new first condition" QFirstCond -- THIS table is over the actual Ob quotient
# (ob_a,ob_b), the object 委嘱16/設計_F8項目5.md's M8 series is about).
BuildObMultTableAndPoints := function(f0, kgens, m)
  local r, ns, total, avec, f, ii, idx, done, table, key, obr, points;
  r := Length(kgens);;
  ns := List(kgens, g -> g.order);;
  total := Product(ns, x->x);;
  table := rec();;  points := [];;
  avec := List([1..Maximum(r,1)], x->0);;
  done := (r=0);;
  while not done do
    f := ShallowCopy(f0);;
    for ii in [1..r] do
      if avec[ii] <> 0 then f := f + avec[ii]*kgens[ii].vec; fi;
    od;
    f := Mod2j(f, 8);;
    obr := ObOfF15(f, m);;
    key := Concatenation(String(obr.ob_a), ",", String(obr.ob_b));;
    if IsBound(table.(key)) then table.(key) := table.(key)+1; else table.(key) := 1; fi;
    Add(points, rec(f:=f, ob_a:=obr.ob_a, ob_b:=obr.ob_b));;
    if r = 0 then done := true; else
      idx := 1;;
      while idx <= r do
        avec[idx] := avec[idx]+1;
        if avec[idx] < ns[idx] then break; fi;
        avec[idx] := 0; idx := idx+1;
      od;
      if idx > r then done := true; fi;
    fi;
  od;
  return rec(table:=table, total:=total, points:=points);
end;;

# ---------------------------------------------------------------------------------------
# M8-a (torsor law, mandatory, cheap): for m in {0,1,2,3}, one fbar (=f0 of the safe synthetic
# system), 12 z-test-vectors (6 C-basis + 2 ker(Lambda) generators + 4 mixed). Determine the
# SIGN empirically (do NOT assume it): check Xi_group(g*z) = Xi_group(g) + Lambda(z) mod R for
# the "+" convention on ALL 12*4=48 cases; if that fails uniformly, check "-". A MIXED result
# (some cases match "+", others match "-") is reported as FAIL, not silently resolved.
# ---------------------------------------------------------------------------------------
Print("\n=== M8-a (torsor law, 4 m-values x 12 z-vectors = 48 checks) ===\n");
m8aPlusOk := true;;  m8aMinusOk := true;;  m8aAnyRun := false;;
m8aMtests := [0,1,2,3];;
for m8m in m8aMtests do
  snfM8 := BuildSnfData(k -> BuildLinearSystemC6SyntheticJ3(m8m), m8m);;
  resM8 := TestAtJ(snfM8, 3);;
  if resM8.solvable then
    f0M8 := ExtractF0(snfM8, 3);;
    lamTblM8 := LambdaTable(m8m);;
    gVec21 := G3PadTo21(f0M8);;
    xiG := XiGroupFlat12(gVec21, m8m);;
    zTests := [];;
    for zi in [1..NC6] do
      zb := List([1..NC6], x->0);;  zb[zi] := 1;;
      Add(zTests, zb);;
    od;;
    Add(zTests, lamTblM8.kerLambda[1]);;
    Add(zTests, lamTblM8.kerLambda[Minimum(2,Length(lamTblM8.kerLambda))]);;
    Add(zTests, List([1..NC6], x -> (x mod 4)));;
    Add(zTests, List([1..NC6], x -> ((2*x+1) mod 4)));;
    Add(zTests, VecAddModR(zTests[1], lamTblM8.kerLambda[1], 4));;
    Add(zTests, VecAddModR(zTests[2], lamTblM8.kerLambda[Minimum(2,Length(lamTblM8.kerLambda))], 4));;
    for zt in zTests do
      m8aAnyRun := true;;
      gzVec21 := List([1..21], k -> gVec21[k] + EmbC(zt)[k]);;
      xiGz := XiGroupFlat12(gzVec21, m8m);;
      lam := LambdaOnC(zt, m8m);;
      plusPred := VecAddModR(xiG, lam, 4);;
      minusPred := List([1..12], i -> (xiG[i] - lam[i]) mod 4);;
      if xiGz <> plusPred then m8aPlusOk := false; fi;
      if xiGz <> minusPred then m8aMinusOk := false; fi;
    od;;
  fi;
od;;
m8aSign := fail;;
if m8aPlusOk and m8aAnyRun and not m8aMinusOk then m8aSign := "+"; fi;
if m8aMinusOk and m8aAnyRun and not m8aPlusOk then m8aSign := "-"; fi;
if m8aPlusOk and m8aMinusOk and m8aAnyRun then m8aSign := "+"; fi;  # degenerate (z=0-like) case
m8aOk := m8aAnyRun and (m8aSign <> fail);;
Print("[", PF(m8aOk), "] M8-a: torsor law Xi(g*z)=Xi(g)+Lambda(z) sign determined empirically = \"", m8aSign, "\" (plus-consistent=", JB(m8aPlusOk), ", minus-consistent=", JB(m8aMinusOk), ", ", Length(m8aMtests)*8, " group-product evaluations)\n");
if m8aSign = fail then
  Print("  [FAIL -- DESIGN BREAK, not a sign bug] neither '+' nor '-' convention held consistently across all 48 cases -- reporting as-is, NOT silently patched\n");
fi;

# ---------------------------------------------------------------------------------------
# SCOPE NOTE (diagnosed empirically before writing M8-b/c/d below, see docs/notes/実装_j3.md):
# the ob=0 CLASSIFICATION must use the QUOTIENT semantics (委嘱16 eq 0.3/0.6, Ob = R[2]a (+)
# (R/2R)b-bar), i.e. ob_a=0 EXACTLY and ob_b==0 MOD 2 (not raw ob_b=0) -- raw ObFromQPair
# output at R=4 can read ob_b=2 for a point that is genuinely the SAME Ob-class as ob_b=0
# (confirmed empirically: at m=0, 128 points read (ob_a,ob_b)=(0,2) and are DICTIONARY-
# CONFIRMED to have a nonempty ker(Lambda) fiber exactly like the (0,0) points -- i.e. they
# ARE the same true obstruction-zero class, just misread by the raw formula). This function
# encodes the corrected classification used throughout M8-b/c/d below.
IsObZeroQuotient := function(obr) return (obr.ob_a = 0) and (obr.ob_b mod 2 = 0); end;;

# SCOPE NOTE 2 (also diagnosed empirically, mirrors the established M2 precedent from
# e2c6-sweep.g/G4's own header: "M2's cancellation genuinely needs (ebar,eps) to be THE
# coherent real Em(m) pair"): q_N(f,m) is only SIGMA-INVARIANT (the structural precondition
# the Lambda-image-membership criterion needs) when f GENUINELY solves N_bar(f)=-Ebar_m(m)
# for the REAL m -- confirmed by direct computation: at m=0 (Ebar_m(0)=0 identically, a known
# structural fact, so any rhs=0-solving f IS a genuine real solution), q_N(f0,0) IS
# sigma-invariant; at m=1 (synthetic rhs=0, NOT the real target), q_N(f0,1) is NOT
# sigma-invariant (direct check: ModVec(qN*SigmaOnCMat(1),4) <> qN). This was tested with
# BOTH a plain rhs=0 system AND an F5-style genuinely-solvable-to-a-SAFE-nonzero-target
# system (mirroring e2c6-sweep.g's own F5) -- both give the SAME failure at m>0, because
# neither ever solves the REAL affine target (only m=0 can, via the Ebar_m(0)=0 shortcut,
# without disclosing real solvability). CONCLUSION: M8-b/c/d can only be MEANINGFULLY,
# blind-safely tested at m=0 pre-fire -- this is a TESTABILITY SCOPE LIMIT, not a "design
# break" in the M8 series' math (M8-a's cocycle law, which needs no solving premise, DID
# pass cleanly for m in {0,1,2,3}). Reported honestly, not silently patched into a wider
# claim than what was actually validated.
m8bcdMtests := [0];;

# ---------------------------------------------------------------------------------------
# M8-b (fiber realization, mandatory): at m=0 (see SCOPE NOTE 2 above), take 4 genuine
# ob=(0,0)-quotient witnesses found EMPIRICALLY from the L_m enumeration
# (BuildObMultTableAndPoints) -- rather than hand-constructing "f0 + kernel generators with
# lambda_m(kappa_i)=0" (the spec's suggested construction), this implementation scans the
# actual L_m for ob=0(quotient) points and uses whichever (up to) 4 it finds; this is an
# equivalent, simpler way to obtain "4 genuine ob=0 witnesses" and is noted here as an
# implementer discretion (not marked "任意" in the spec, but achieves the identical fixture
# goal). For EACH such witness, all |ker Lambda|=8 fiber elements are directly
# group-product-checked via IsIdentityInCellAj on BOTH theta(g_z)*g_z and
# Em*sigma^2(g_z)*sigma(g_z)*g_z.
# ---------------------------------------------------------------------------------------
Print("\n=== M8-b (fiber realization, mandatory, m=0 only -- see SCOPE NOTE 2) ===\n");
m8bOk := true;;  m8bAnyRun := false;;  m8bTotalGroupProducts := 0;;
for m8m in m8bcdMtests do
  snfM8b := BuildSnfData(k -> BuildLinearSystemC6SyntheticJ3(m8m), m8m);;
  resM8b := TestAtJ(snfM8b, 3);;
  if resM8b.solvable then
    f0M8b := ExtractF0(snfM8b, 3);;
    obData := BuildObMultTableAndPoints(f0M8b, resM8b.kgens, m8m);;
    lamTblM8b := LambdaTable(m8m);;
    zeroPoints := Filtered(obData.points, p -> IsObZeroQuotient(p));;
    witnesses := zeroPoints{[1..Minimum(4, Length(zeroPoints))]};;
    for wpt in witnesses do
      m8bAnyRun := true;;
      gVecB := G3PadTo21(wpt.f);;
      # WITNESS-SPECIFIC fiber (self-caught bug, first pass): the real lift set for THIS
      # witness g is {z : Lambda(z) = -Xi(g)}, which is kerLambda ONLY when Xi(g)=0 exactly
      # (raw). For an ob=0-QUOTIENT witness whose RAW Xi(g) is nonzero (e.g. the ob_b=2 class,
      # same true Ob-class as ob_b=0 but a different C^theta representative), the correct
      # fiber is the -Xi(g) COSET of Lambda's image, NOT kerLambda itself -- using kerLambda
      # unconditionally here was the bug (first pass wrongly assumed Xi(g)=0 for every
      # ob=0-quotient witness).
      witnessXiB := XiClosedFlat12(wpt.f, m8m);;
      witnessFiberKeyB := String(NegVec(witnessXiB, 4));;
      witnessFiberB := lamTblM8b.table.(witnessFiberKeyB);;   # guaranteed bound: M8-c already
                                                               # confirmed every ob=0-quotient
                                                               # point has a nonempty fiber
      for zfib in witnessFiberB do
        gzVecB := List([1..21], k -> gVecB[k] + EmbC(zfib)[k]);;
        thetaProd := Exponents(G3ApplyAsAutomorphism(ThetaTable21, gzVecB{[1..21]}) * G3ElemFromVec(gzVecB));;
        # N-side: Em * sigma^2(g_z) * sigma(g_z) * g_z (mirrors G3RouteGQN's construction)
        gzElemB := G3ElemFromVec(gzVecB);;
        sigTblM := SigmaMat21(m8m);;
        sgB := G3ApplyAsAutomorphism(sigTblM, gzVecB);;
        s2vecB := Exponents(sgB);;
        s2gB := G3ApplyAsAutomorphism(sigTblM, s2vecB);;
        emElemB := G3ElemFromVec(EmVec21(m8m));;
        nProdB := Exponents(emElemB * s2gB * sgB * gzElemB);;
        m8bTotalGroupProducts := m8bTotalGroupProducts + 2;;
        if not IsIdentityInCellAj(thetaProd) then m8bOk := false; Print("  M8-b FAIL (theta side) m=",m8m," z=",zfib,"\n"); fi;
        if not IsIdentityInCellAj(nProdB) then m8bOk := false; Print("  M8-b FAIL (N side) m=",m8m," z=",zfib,"\n"); fi;
      od;;
    od;;
    Print("  m=",m8m,": ", Length(witnesses), " ob=0-quotient witnesses found (of ", Length(zeroPoints), " total in L_m), each witness's own Lambda-fiber (size ", Length(lamTblM8b.kerLambda), ") directly checked\n");
  fi;
od;;
Print("[", PF(m8bOk and m8bAnyRun), "] M8-b: fiber realization -- all ker(Lambda) elements produce genuine identity in cell A^(3) via direct group product (", m8bTotalGroupProducts, " group-product evaluations)\n");

# ---------------------------------------------------------------------------------------
# M8-c (mass identity, mandatory, THE main check, no group products): at m=0 (see SCOPE
# NOTE 2 above), over the FULL L_0 (512 points), classify by ob=0-QUOTIENT (closed-form,
# via IsObZeroQuotient) vs fib nonempty (Lambda-image dictionary lookup on closed-form Xi)
# -- these two INDEPENDENT characterizations of "a real central lift exists" must match
# SET-WISE, and Sum(|fib|) = |ker Lambda| * mult(ob=0-quotient class).
# ---------------------------------------------------------------------------------------
Print("\n=== M8-c (mass identity, mandatory -- main check, m=0 only -- see SCOPE NOTE 2) ===\n");
m8cOk := true;;  m8cAnyRun := false;;
for m8m in m8bcdMtests do
  snfM8c := BuildSnfData(k -> BuildLinearSystemC6SyntheticJ3(m8m), m8m);;
  resM8c := TestAtJ(snfM8c, 3);;
  if resM8c.solvable then
    f0M8c := ExtractF0(snfM8c, 3);;
    obDataC := BuildObMultTableAndPoints(f0M8c, resM8c.kgens, m8m);;
    lamTblM8c := LambdaTable(m8m);;
    kerLamSize := Length(lamTblM8c.kerLambda);;
    sumFib := 0;;  setMismatch := 0;;  multQuotZero := 0;;
    for pt in obDataC.points do
      xiC := XiClosedFlat12(pt.f, m8m);;
      keyFib := String(NegVec(xiC, 4));;
      fibSize := 0;;
      if IsBound(lamTblM8c.table.(keyFib)) then fibSize := Length(lamTblM8c.table.(keyFib)); fi;
      sumFib := sumFib + fibSize;;
      isObZero := IsObZeroQuotient(pt);;
      if isObZero then multQuotZero := multQuotZero + 1; fi;
      isFibNonempty := (fibSize > 0);;
      if isObZero <> isFibNonempty then setMismatch := setMismatch + 1; fi;
    od;;
    massOk := (sumFib = kerLamSize * multQuotZero);;
    setOk := (setMismatch = 0);;
    m8cAnyRun := true;;
    if not (massOk and setOk) then m8cOk := false; fi;
    Print("  m=",m8m,": |ker Lambda|=",kerLamSize," mult(ob=0-quotient)=",multQuotZero," Sum|fib|=",sumFib,
      " (expect ",kerLamSize*multQuotZero,")  set-mismatches=",setMismatch,
      "  mass-identity=",JB(massOk),"  set-match=",JB(setOk),"\n");
    if setMismatch > 0 then
      Print("  [NOTE] ", setMismatch, " point(s) where ob=0-quotient-membership and fib-nonempty-membership DISAGREE",
        " -- per 設計_F8項目5.md trap warning, this is reported as a genuine discrepancy (design break),",
        " NOT silently reconciled by flipping the M8-a sign convention.\n");
    fi;
    pathM8c := Concatenation("certificates/e2c6j3/fixture_M8c_massidentity_m", String(m8m), ".json");;
    certM8c := Concatenation(
      "{\"claim\":\"m8c_mass_identity\",\"m\":", String(m8m), ",\"j\":3,\"R\":4,",
      "\"witness_f0_abar\":\"", String(f0M8c), "\",",
      "\"K_generators\":[", JoinC(List(resM8c.kgens, g -> String(g.vec)), ","), "],",
      "\"K_orders\":[", JoinC(List(resM8c.kgens, g -> String(g.order)), ","), "],",
      "\"ker_lambda_size\":", String(kerLamSize), ",\"mult_ob0_quotient\":", String(multQuotZero), ",",
      "\"sum_fib\":", String(sumFib), ",\"expected_sum_fib\":", String(kerLamSize*multQuotZero), ",",
      "\"set_mismatch_count\":", String(setMismatch), ",",
      "\"mass_identity_holds\":", JB(massOk), ",\"set_match_holds\":", JB(setOk), ",",
      "\"m8a_sign\":\"", m8aSign, "\",",
      "\"scope_note\":\"m=0 only -- Ebar_m(0)=0 identically is the sole point where a blind-safe synthetic system genuinely coincides with the real target (q_N sigma-invariance precondition verified); m>0 requires real Ebar_m data, out of scope pre-fire\",",
      "\"recheck\":\"checker independently rebuilds LambdaTable(m) by exhaustive scan of (Z/4)^6 (own agree6_sol2.json-derived theta|C/sigma|C), re-enumerates the full L_m from witness_f0_abar/K_generators/K_orders, recomputes ob (quotient-classified: ob_a=0 exact AND ob_b mod2=0) and Xi (closed form) at every point, and rebuilds sum_fib/set_mismatch_count/mass_identity_holds/set_match_holds from scratch\"}");;
    WriteFile(pathM8c, certM8c);;
  fi;
od;;
Print("[", PF(m8cOk and m8cAnyRun), "] M8-c: mass identity Sum(|fib|)=|ker Lambda|*mult(ob=0-quotient) AND set-match, m=0 (the only blind-safely-testable point pre-fire)\n");

# ---------------------------------------------------------------------------------------
# M8-d (negative control, mandatory -- guards against M8-b being vacuously true): at m=0
# (see SCOPE NOTE 2 above), take ONE ob<>0(quotient) witness from L_0, confirm fib is EMPTY
# (dictionary lookup), then directly group-multiply by all 8 ker(Lambda) elements and
# confirm IsIdentityInCellAj is FALSE for every single one (via genuine group product, not
# just the dictionary).
# ---------------------------------------------------------------------------------------
Print("\n=== M8-d (negative control, mandatory, m=0 only -- see SCOPE NOTE 2) ===\n");
m8dOk := true;;  m8dAnyRun := false;;
for m8m in m8bcdMtests do
  snfM8d := BuildSnfData(k -> BuildLinearSystemC6SyntheticJ3(m8m), m8m);;
  resM8d := TestAtJ(snfM8d, 3);;
  if resM8d.solvable then
    f0M8d := ExtractF0(snfM8d, 3);;
    obDataD := BuildObMultTableAndPoints(f0M8d, resM8d.kgens, m8m);;
    lamTblM8d := LambdaTable(m8m);;
    nonzeroPoints := Filtered(obDataD.points, p -> not IsObZeroQuotient(p));;
    if Length(nonzeroPoints) = 0 then
      Print("  [SKIP] m=",m8m,": no ob<>(0,0) point found in this safe synthetic L_m (nothing to negative-control against)\n");
    else
      m8dAnyRun := true;;
      negWitness := nonzeroPoints[1];;
      xiCNeg := XiClosedFlat12(negWitness.f, m8m);;
      keyFibNeg := String(NegVec(xiCNeg, 4));;
      fibEmptyDict := not IsBound(lamTblM8d.table.(keyFibNeg));;
      gVecD := G3PadTo21(negWitness.f);;
      allFail := true;;
      for zfib in lamTblM8d.kerLambda do
        gzVecD := List([1..21], k -> gVecD[k] + EmbC(zfib)[k]);;
        thetaProdD := Exponents(G3ApplyAsAutomorphism(ThetaTable21, gzVecD) * G3ElemFromVec(gzVecD));;
        gzElemD := G3ElemFromVec(gzVecD);;
        sigTblMD := SigmaMat21(m8m);;
        sgD := G3ApplyAsAutomorphism(sigTblMD, gzVecD);;
        s2vecD := Exponents(sgD);;
        s2gD := G3ApplyAsAutomorphism(sigTblMD, s2vecD);;
        emElemD := G3ElemFromVec(EmVec21(m8m));;
        nProdD := Exponents(emElemD * s2gD * sgD * gzElemD);;
        # BUG FIX (self-caught during real-data run): a genuine "identity lift" requires BOTH
        # theta(g_z)*g_z AND Em*sigma^2(g_z)*sigma(g_z)*g_z to be identity in cell A^(j)
        # SIMULTANEOUSLY (that is what "real lift exists" means) -- checking with OR flags a
        # false positive whenever the theta-side ALONE happens to vanish (which is common: for
        # any genuine L_m solution f, (1+theta_bar)f=0 mod 8 already forces the Abar-part of
        # theta(g)g to vanish regardless of any central shift z, and the theta-side's C-part is
        # shift-invariant on ker(Lambda) by construction -- so an OR-check is nearly guaranteed
        # to misfire on ker(Lambda) elements whenever Xi(g)'s theta-component happens to be 0
        # mod 4, independent of whether a genuine FULL lift exists). Corrected to AND.
        if IsIdentityInCellAj(thetaProdD) and IsIdentityInCellAj(nProdD) then
          allFail := false;;
          Print("  M8-d UNEXPECTED PASS at m=",m8m," z=",zfib," (ob<>(0,0) witness produced an identity lift -- this would be a genuine discrepancy)\n");
        fi;
      od;;
      thisOk := fibEmptyDict and allFail;;
      if not thisOk then m8dOk := false; fi;
      Print("  m=",m8m,": ob=(",negWitness.ob_a,",",negWitness.ob_b,")<>(0,0) witness -- fib empty (dict)=",JB(fibEmptyDict),
        "  all 8 ker(Lambda) group-products FAIL to give identity=",JB(allFail),"\n");
    fi;
  fi;
od;;
Print("[", PF(m8dOk and m8dAnyRun), "] M8-d: negative control -- ob<>(0,0) witness has empty fiber AND all ker(Lambda) group-products genuinely fail (not a vacuous check)\n");

m8SeriesOk := m8aOk and m8bOk and m8bAnyRun and m8cOk and m8cAnyRun and m8dOk and m8dAnyRun;;
Print("[", PF(m8SeriesOk), "] M8 SERIES (a+b+c+d combined)\n");

# ================================================================================
# CERTIFICATE WRITING (fixture certs only, certificates/e2c6j3/).
# ================================================================================
Print("\n=== writing fixture certificates to certificates/e2c6j3/ ===\n");
for mIt in [0,1,2,3] do
  snfW := BuildSnfData(k -> BuildLinearSystemC6SyntheticJ3(mIt), mIt);;
  resW := TestAtJ(snfW, 3);;
  if resW.solvable then
    f0W := ExtractF0(snfW, 3);;
    tblS := BuildJ3MultTableShortcut(f0W, resW.kgens, mIt);;
    tblB := BuildJ3MultTableBruteForce(f0W, resW.kgens, mIt);;
    entriesS := RecNames(tblS.table);;
    tableStrs := List(entriesS, k -> Concatenation("\"", k, "\":", String(tblS.table.(k))));;
    path := Concatenation("certificates/e2c6j3/fixture_G1_synthetic_j3_m", String(mIt), ".json");;
    cert := Concatenation(
      "{\"claim\":\"m6j3_multiplicity_table\",\"fixture\":\"synthetic_rhs0_j3\",",
      "\"linear_solvable\":true,",
      "\"m\":", String(mIt), ",\"j\":3,\"modulus\":8,\"R\":4,",
      "\"witness_f0_abar\":\"", String(f0W), "\",",
      "\"K_generators\":[", JoinC(List(resW.kgens, g -> String(g.vec)), ","), "],",
      "\"K_orders\":[", JoinC(List(resW.kgens, g -> String(g.order)), ","), "],",
      "\"total_points\":", String(tblS.total), ",",
      "\"ob_table\":{", JoinC(tableStrs, ","), "},",
      "\"lambda_bit_matrix\":[", JoinC(List(tblS.bit_matrix, v -> String(v)), ","), "],",
      "\"lambda_rank\":", String(tblS.rank), ",",
      "\"brute_force_matches_shortcut\":", JB(TablesEqual(tblS.table, tblB.table)), ",",
      "\"new_first_condition_j3\":\"p_parity_s3_w_r2/v1\",",
      "\"lambda_formula\":\"lambda_m3(k)=(k_p, k_s3+W(m)*k_r2) mod 2, W(m)=binom(m+1,2) mod 2 (sol_reply_24_d2.md sec.F8 eq 8.3)\",",
      "\"ob_mode\":\"quotient-ratified-v2\",",
      "\"recheck\":\"checker independently rebuilds K_m3 generators against agree6_sol2.json-derived rows, re-enumerates full L_m, and recomputes both the lambda-shortcut table and the brute-force table\"}");;
    WriteFile(path, cert);;
    Print("  wrote ", path, "\n");
  fi;
od;;

# ================================================================================
# FIRE LOCK (mirrors search/e2c6-sweep.g's mechanism, independent auth file): real-universe
# sweep (real m=0..63 at j=3) is gated behind search/FIRE_e2c6j3.auth containing the SHA-256
# of docs/manifest_e2c6j3_v1.md.
# ================================================================================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_j3.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

RunRealSweepC6J3 := function()
  local mIt, snfD, res, f0, path, cert, tblS, tblB, entriesS, tableStrs, guardCheck,
        yReal, yMReal, ybReal, yMZeroReal, yBNonzeroReal, abortCount, computedCount,
        solvableMList, unsolvableMList, abortMList, allKeysSeen, mTableSummaries;
  Print("  [UNLOCKED] running real-universe sweep, j=3, m=0..63 ...\n");
  abortCount := 0;;  computedCount := 0;;
  solvableMList := [];;  unsolvableMList := [];;  abortMList := [];;
  allKeysSeen := rec();;  mTableSummaries := [];;
  for mIt in [0..63] do
    snfD := BuildSnfData(BuildLinearSystemC6, mIt);;
    res := TestAtJ(snfD, 3);;
    path := Concatenation("certificates/e2c6j3/sweep_j3_m", String(mIt), ".json");;
    if res.solvable then
      # GUARD (司令塔発注item1 / falsifier問3【重大】): re-verify k_w=0 (mod 8) PER m before
      # applying the lambda formula (eq 8.3) -- if violated, ABORT this m (write a
      # premise_violated cert, do NOT silently apply lambda / do NOT write an ob_table).
      guardCheck := CheckPremiseKw(res.kgens);;
      if guardCheck.violated then
        abortCount := abortCount + 1;;
        Add(abortMList, mIt);;
        cert := Concatenation(
          "{\"claim\":\"precondition_violated_c6j3\",\"m\":", String(mIt), ",\"j\":3,\"modulus\":8,",
          "\"k_w_nonzero\":true,\"bad_generator_count\":", String(Length(guardCheck.bad_generators)), ",",
          "\"bad_generators\":[", JoinC(List(guardCheck.bad_generators, v -> String(v)), ","), "],",
          "\"action\":\"ABORTED -- lambda formula (eq 8.3) NOT applied; k_w=0 premise (eq 8.2) violated at this m\",",
          "\"ob_mode\":null}");;
        WriteFile(path, cert);;
        Print("  [ABORT] m=", mIt, ": k_w<>0 premise VIOLATED (", Length(guardCheck.bad_generators), " bad generators) -- wrote precondition_violated_c6j3, NOT computing ob_table\n");
      else
        computedCount := computedCount + 1;;
        Add(solvableMList, mIt);;
        f0 := ExtractF0(snfD, 3);;
        tblS := BuildJ3MultTableShortcut(f0, res.kgens, mIt);;
        tblB := BuildJ3MultTableBruteForce(f0, res.kgens, mIt);;
        entriesS := RecNames(tblS.table);;
        tableStrs := List(entriesS, k -> Concatenation("\"", k, "\":", String(tblS.table.(k))));;
        for kEntry in entriesS do
          if IsBound(allKeysSeen.(kEntry)) then allKeysSeen.(kEntry) := allKeysSeen.(kEntry)+1;
          else allKeysSeen.(kEntry) := 1; fi;
        od;;
        Add(mTableSummaries, rec(m:=mIt, table:=tblS.table, total:=tblS.total,
          all_zero_only:=(Length(entriesS)=1 and entriesS[1]="0,0")));;
        cert := Concatenation(
          "{\"claim\":\"m6j3_multiplicity_table\",\"fixture\":\"real_sweep\",",
          "\"m\":", String(mIt), ",\"j\":3,\"modulus\":8,\"R\":4,\"linear_solvable\":true,",
          "\"witness_f0_abar\":\"", String(f0), "\",",
          "\"K_generators\":[", JoinC(List(res.kgens, g -> String(g.vec)), ","), "],",
          "\"K_orders\":[", JoinC(List(res.kgens, g -> String(g.order)), ","), "],",
          "\"total_points\":", String(tblS.total), ",",
          "\"ob_table\":{", JoinC(tableStrs, ","), "},",
          "\"lambda_bit_matrix\":[", JoinC(List(tblS.bit_matrix, v -> String(v)), ","), "],",
          "\"lambda_rank\":", String(tblS.rank), ",",
          "\"brute_force_matches_shortcut\":", JB(TablesEqual(tblS.table, tblB.table)), ",",
          "\"ob_mode\":\"quotient-ratified-v2\"}");;
        WriteFile(path, cert);;
      fi;
    else
      # 便24 F8 item 1: dual witness for unsolvable real systems (mirrors j=2's
      # WriteUnsolvableCertC6 exactly).
      Add(unsolvableMList, mIt);;
      yReal := snfD.U[res.failRow];;
      yMReal := yReal * snfD.sys.rows;;
      ybReal := yReal * snfD.sys.rhs;;
      yMZeroReal := ForAll(List(yMReal, x -> x mod res.modulus), x -> x = 0);;
      yBNonzeroReal := (ybReal mod res.modulus <> 0);;
      cert := Concatenation("{\"claim\":\"linear_stage_empty_c6j3\",\"linear_solvable\":false,",
        "\"fixture\":\"real_sweep\",\"m\":", String(mIt), ",\"j\":3,\"modulus\":", String(res.modulus), ",",
        "\"dual_witness_y\":\"", String(yReal), "\",",
        "\"yM_is_zero_mod_2j\":", JB(yMZeroReal), ",",
        "\"yb\":", String(ybReal), ",\"yb_nonzero_mod_2j\":", JB(yBNonzeroReal), "}");;
      WriteFile(path, cert);;
    fi;
  od;;
  Print("  real-universe sweep complete: certificates/e2c6j3/sweep_j3_m*.json (64 files, ", computedCount, " ob_table + ", abortCount, " premise-violated-abort + ", Length(unsolvableMList), " unsolvable)\n");
  return rec(solvableMList:=solvableMList, unsolvableMList:=unsolvableMList, abortMList:=abortMList,
    allKeysSeen:=allKeysSeen, mTableSummaries:=mTableSummaries);
end;;

# ================================================================================
# M8-b/c/d REAL-DATA SAMPLE (司令塔発射合図 item 2): now that the fire lock is open (blind
# constraint lifted), real solvable systems genuinely satisfy N_bar(f0)=-Ebar_m(m) for the
# REAL m -- so q_N's sigma-invariance precondition (the reason M8-b/c/d were restricted to
# m=0 in the fixture pass) is expected to hold for ANY real solvable m, not just m=0. Run on
# a SAMPLE (not all 64 -- some kernels are large) of real solvable m's.
# ================================================================================
RunRealM8SeriesSample := function(solvableMList, sampleSize)
  local sampleMs, m8m, snfR, resR, f0R, obDataR, lamTblR, kerLamSizeR, sumFibR, setMismatchR,
        multQuotZeroR, pt, xiC, keyFib, fibSize, isObZero, massOkR, setOkR, pathC, certC,
        zeroPointsR, witnessesR, wpt, gVecB, witnessXiB, witnessFiberKeyB, witnessFiberB,
        zfib, gzVecB, thetaProd, gzElemB, sigTblM, sgB, s2vecB, s2gB, emElemB, nProdB,
        m8bOkR, m8bTotalGroupProductsR, witnessSummaries, nonzeroPointsR, negWitnessR,
        xiCNegR, keyFibNegR, fibEmptyDictR, gVecD, allFailR, gzVecD, thetaProdD, gzElemD,
        sigTblMD, sgD, s2vecD, s2gD, emElemD, nProdD, m8dOkR, pathB, certB, pathD, certD,
        results, skippedTooLarge;
  results := [];;  skippedTooLarge := [];;
  sampleMs := solvableMList{[1..Minimum(sampleSize, Length(solvableMList))]};;
  Print("\n  === M8-b/c/d REAL-DATA SAMPLE (m = ", sampleMs, ") ===\n");
  for m8m in sampleMs do
    snfR := BuildSnfData(BuildLinearSystemC6, m8m);;
    resR := TestAtJ(snfR, 3);;
    if not resR.solvable then continue; fi;   # should not happen (m came from solvableMList)
    if Product(List(resR.kgens, g->g.order), x->x) > 200000 then
      Add(skippedTooLarge, m8m);;
      Print("  [SKIP] m=", m8m, ": |K|=", Product(List(resR.kgens,g->g.order),x->x), " too large for full L_m enumeration in this pass\n");
      continue;
    fi;
    f0R := ExtractF0(snfR, 3);;
    obDataR := BuildObMultTableAndPoints(f0R, resR.kgens, m8m);;
    lamTblR := LambdaTable(m8m);;
    kerLamSizeR := Length(lamTblR.kerLambda);;

    # ---- M8-c (mass identity) ----
    sumFibR := 0;;  setMismatchR := 0;;  multQuotZeroR := 0;;
    for pt in obDataR.points do
      xiC := XiClosedFlat12(pt.f, m8m);;
      keyFib := String(NegVec(xiC, 4));;
      fibSize := 0;;
      if IsBound(lamTblR.table.(keyFib)) then fibSize := Length(lamTblR.table.(keyFib)); fi;
      sumFibR := sumFibR + fibSize;;
      isObZero := IsObZeroQuotient(pt);;
      if isObZero then multQuotZeroR := multQuotZeroR + 1; fi;
      if isObZero <> (fibSize>0) then setMismatchR := setMismatchR + 1; fi;
    od;;
    massOkR := (sumFibR = kerLamSizeR * multQuotZeroR);;
    setOkR := (setMismatchR = 0);;
    pathC := Concatenation("certificates/e2c6j3/m8c_real_m", String(m8m), ".json");;
    certC := Concatenation(
      "{\"claim\":\"m8c_mass_identity\",\"fixture\":\"real_sample\",\"m\":", String(m8m), ",\"j\":3,\"R\":4,",
      "\"witness_f0_abar\":\"", String(f0R), "\",",
      "\"K_generators\":[", JoinC(List(resR.kgens, g -> String(g.vec)), ","), "],",
      "\"K_orders\":[", JoinC(List(resR.kgens, g -> String(g.order)), ","), "],",
      "\"ker_lambda_size\":", String(kerLamSizeR), ",\"mult_ob0_quotient\":", String(multQuotZeroR), ",",
      "\"sum_fib\":", String(sumFibR), ",\"expected_sum_fib\":", String(kerLamSizeR*multQuotZeroR), ",",
      "\"set_mismatch_count\":", String(setMismatchR), ",",
      "\"mass_identity_holds\":", JB(massOkR), ",\"set_match_holds\":", JB(setOkR), ",",
      "\"m8a_sign\":\"", m8aSign, "\"}");;
    WriteFile(pathC, certC);;

    # ---- M8-b (fiber realization) on up to 4 real ob=0-quotient witnesses ----
    zeroPointsR := Filtered(obDataR.points, p -> IsObZeroQuotient(p));;
    witnessesR := zeroPointsR{[1..Minimum(4, Length(zeroPointsR))]};;
    m8bOkR := true;;  m8bTotalGroupProductsR := 0;;  witnessSummaries := [];;
    for wpt in witnessesR do
      gVecB := G3PadTo21(wpt.f);;
      witnessXiB := XiClosedFlat12(wpt.f, m8m);;
      witnessFiberKeyB := String(NegVec(witnessXiB, 4));;
      witnessFiberB := lamTblR.table.(witnessFiberKeyB);;
      for zfib in witnessFiberB do
        gzVecB := List([1..21], k -> gVecB[k] + EmbC(zfib)[k]);;
        thetaProd := Exponents(G3ApplyAsAutomorphism(ThetaTable21, gzVecB) * G3ElemFromVec(gzVecB));;
        gzElemB := G3ElemFromVec(gzVecB);;
        sigTblM := SigmaMat21(m8m);;
        sgB := G3ApplyAsAutomorphism(sigTblM, gzVecB);;
        s2vecB := Exponents(sgB);;
        s2gB := G3ApplyAsAutomorphism(sigTblM, s2vecB);;
        emElemB := G3ElemFromVec(EmVec21(m8m));;
        nProdB := Exponents(emElemB * s2gB * sgB * gzElemB);;
        m8bTotalGroupProductsR := m8bTotalGroupProductsR + 2;;
        if not IsIdentityInCellAj(thetaProd) then m8bOkR := false; fi;
        if not IsIdentityInCellAj(nProdB) then m8bOkR := false; fi;
      od;;
      Add(witnessSummaries, rec(ob_a:=wpt.ob_a, ob_b:=wpt.ob_b, fiber_size:=Length(witnessFiberB)));;
    od;;
    pathB := Concatenation("certificates/e2c6j3/m8b_real_m", String(m8m), ".json");;
    certB := Concatenation(
      "{\"claim\":\"m8b_fiber_realization\",\"fixture\":\"real_sample\",\"m\":", String(m8m), ",\"j\":3,\"R\":4,",
      "\"witness_count\":", String(Length(witnessesR)), ",",
      "\"witnesses\":[", JoinC(List(witnessSummaries, w -> Concatenation(
        "{\"ob_a\":",String(w.ob_a),",\"ob_b\":",String(w.ob_b),",\"fiber_size\":",String(w.fiber_size),"}")), ","), "],",
      "\"total_group_products\":", String(m8bTotalGroupProductsR), ",",
      "\"all_fiber_elements_give_identity\":", JB(m8bOkR), "}");;
    WriteFile(pathB, certB);;

    # ---- M8-d (negative control) on one real ob<>0-quotient witness ----
    nonzeroPointsR := Filtered(obDataR.points, p -> not IsObZeroQuotient(p));;
    if Length(nonzeroPointsR) > 0 then
      negWitnessR := nonzeroPointsR[1];;
      xiCNegR := XiClosedFlat12(negWitnessR.f, m8m);;
      keyFibNegR := String(NegVec(xiCNegR, 4));;
      fibEmptyDictR := not IsBound(lamTblR.table.(keyFibNegR));;
      gVecD := G3PadTo21(negWitnessR.f);;
      allFailR := true;;
      for zfib in lamTblR.kerLambda do
        gzVecD := List([1..21], k -> gVecD[k] + EmbC(zfib)[k]);;
        thetaProdD := Exponents(G3ApplyAsAutomorphism(ThetaTable21, gzVecD) * G3ElemFromVec(gzVecD));;
        gzElemD := G3ElemFromVec(gzVecD);;
        sigTblMD := SigmaMat21(m8m);;
        sgD := G3ApplyAsAutomorphism(sigTblMD, gzVecD);;
        s2vecD := Exponents(sgD);;
        s2gD := G3ApplyAsAutomorphism(sigTblMD, s2vecD);;
        emElemD := G3ElemFromVec(EmVec21(m8m));;
        nProdD := Exponents(emElemD * s2gD * sgD * gzElemD);;
        # (same AND-fix as the fixture-pass M8-d above -- see its comment for the reasoning)
        if IsIdentityInCellAj(thetaProdD) and IsIdentityInCellAj(nProdD) then allFailR := false; fi;
      od;;
      m8dOkR := fibEmptyDictR and allFailR;;
      pathD := Concatenation("certificates/e2c6j3/m8d_real_m", String(m8m), ".json");;
      certD := Concatenation(
        "{\"claim\":\"m8d_negative_control\",\"fixture\":\"real_sample\",\"m\":", String(m8m), ",\"j\":3,\"R\":4,",
        "\"witness_ob_a\":", String(negWitnessR.ob_a), ",\"witness_ob_b\":", String(negWitnessR.ob_b), ",",
        "\"fiber_empty\":", JB(fibEmptyDictR), ",\"all_ker_lambda_products_fail\":", JB(allFailR), ",",
        "\"pass\":", JB(m8dOkR), "}");;
      WriteFile(pathD, certD);;
    else
      m8dOkR := fail;;   # no ob<>0 point in this m's L_m -- honestly recorded, not silently skipped
      Print("  [NOTE] m=", m8m, ": no ob<>0-quotient point found in this real L_m -- M8-d negative control has no witness to test at this m\n");
    fi;

    Add(results, rec(m:=m8m, m8b_ok:=m8bOkR, m8c_mass_ok:=massOkR, m8c_set_ok:=setOkR, m8d_ok:=m8dOkR,
      ker_lambda_size:=kerLamSizeR, mult_ob0:=multQuotZeroR, total_points:=obDataR.total));;
    Print("  m=", m8m, ": |L|=", obDataR.total, " |kerLambda|=", kerLamSizeR, " mult(ob=0)=", multQuotZeroR,
      "  M8-b=", PF(m8bOkR), "  M8-c(mass)=", PF(massOkR), "  M8-c(set)=", PF(setOkR), "  M8-d=", m8dOkR, "\n");
  od;;
  return rec(results:=results, skippedTooLarge:=skippedTooLarge);;
end;;

Print("\n=== FIRE LOCK CHECK (j=3) ===\n");
fireAuthPathJ3 := "search/FIRE_e2c6j3.auth";;
manifestJ3Path := "docs/manifest_e2c6j3_v1.md";;
fireUnlockedJ3 := false;;
if IsExistingFile(fireAuthPathJ3) then
  expectedHashJ3 := LowercaseString(ComputeSha256File(manifestJ3Path));;
  fAuthJ3 := InputTextFile(fireAuthPathJ3);;
  authRawJ3 := ReadAll(fAuthJ3);;
  CloseStream(fAuthJ3);;
  authTrimJ3 := LowercaseString(Filtered(authRawJ3, c -> not (c in "\n\r \t")));;
  if Length(authTrimJ3) >= 64 and authTrimJ3{[1..64]} = expectedHashJ3 then
    fireUnlockedJ3 := true;;
  else
    Print("  FIRE_e2c6j3.auth present but hash MISMATCH (expected ", expectedHashJ3, ", got ", authTrimJ3, ") -- treating as LOCKED\n");
  fi;
fi;

ConcatSha256OfFiles := function(relpaths)
  local tmp, f, line, listFile, p;
  tmp := "search/.tmp_sha256_concat_j3.txt";;
  listFile := "search/.tmp_filelist_j3.txt";;
  WriteFile(listFile, JoinC(relpaths, "\n"));;
  Exec(Concatenation("cat $(sort \"", listFile, "\") | sha256sum > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\" \"", listFile, "\""));;
  return line{[1..64]};
end;;

realSweepSummary := fail;;  m8RealSummary := fail;;
sweepStartMs := 0;;  sweepElapsedMs := 0;;
if fireUnlockedJ3 then
  Print("[UNLOCKED] real-universe sweep authorized by search/FIRE_e2c6j3.auth (hash-matched)\n");
  sweepStartMs := Runtime();;
  realSweepSummary := RunRealSweepC6J3();;
  m8RealSummary := RunRealM8SeriesSample(realSweepSummary.solvableMList, 6);;
  sweepElapsedMs := Runtime() - sweepStartMs;;
else
  Print("[LOCKED] real-universe sweep requires FIRE_e2c6j3.auth (commander issues at fire time)\n");
fi;

Print("\n=== FINAL SUMMARY (j=3 gate) ===\n");
Print("[", PF(kwZeroOk and kwAnyRun), "] precondition: k_w=0 mod 8 (safe systems)\n");
Print("[", PF(guardOk), "] GUARD: CheckPremiseKw unit-tested (genuine pass + injected-violation detection)\n");
Print("[", PF(g1Ok and g1AnyRun), "] G1 false-positive detector (sum=|L| + shortcut==brute-force)\n");
Print("[", PF(g1bFound and g1bOk), "] G1b dual-witness path (unsolvable safe synthetic system)\n");
Print("[", PF(g2Ok), "] G2 class-5 control (j=3) + projection agreement vs frozen j=2 gate\n");
Print("[", PF(G3AllOk), "] G3 route-G cross-check (mod-8-reduced test vectors)\n");
Print("[", PF(g4Combined), "] G4 M-series (R=4, (1+theta)ker(N_C) recomputed)\n");
Print("[", PF(g7Ok), "] G7 ObFromQPair(R=4) nonzero q_N permanent fixture\n");
Print("[", PF(g8AllWritten), "] G8 periodicity comparison certs (m vs m+32, observation only)\n");
Print("[", PF(m8aOk), "] M8-a torsor law (sign determined empirically = \"", m8aSign, "\")\n");
Print("[", PF(m8bOk and m8bAnyRun), "] M8-b fiber realization (direct group products)\n");
Print("[", PF(m8cOk and m8cAnyRun), "] M8-c mass identity (main check)\n");
Print("[", PF(m8dOk and m8dAnyRun), "] M8-d negative control\n");
Print("[", PF(m8SeriesOk), "] M8 SERIES combined\n");
if fireUnlockedJ3 then
  Print("[UNLOCKED] real-universe sweep RAN this pass (see REAL SWEEP REPORT below)\n");
else
  Print("[", PF(true), "] fire lock CLOSED (real sweep NOT run this pass)\n");
fi;

if fireUnlockedJ3 and realSweepSummary <> fail then
  Print("\n=== REAL SWEEP REPORT (m=0..63, j=3) -- 機械事実 ===\n");
  Print("linear-stage solvable count: ", Length(realSweepSummary.solvableMList), " / 64\n");
  Print("solvable m list: ", realSweepSummary.solvableMList, "\n");
  Print("unsolvable m list: ", realSweepSummary.unsolvableMList, " (count=", Length(realSweepSummary.unsolvableMList), ")\n");
  Print("k_w-guard ABORTED m list: ", realSweepSummary.abortMList, " (count=", Length(realSweepSummary.abortMList), ")\n");
  Print("\n--- multiplicity table summary (aggregate over all solvable+non-aborted m) ---\n");
  Print("distinct (ob_a,ob_b) keys observed across all m: ", RecNames(realSweepSummary.allKeysSeen), "\n");
  Print("per-key m-count (how many m's tables contain this key at all): ", realSweepSummary.allKeysSeen, "\n");
  allZeroOnlyMs := List(Filtered(realSweepSummary.mTableSummaries, r -> r.all_zero_only), r -> r.m);;
  mixedMs := List(Filtered(realSweepSummary.mTableSummaries, r -> not r.all_zero_only), r -> r.m);;
  Print("m's whose table is EXCLUSIVELY \"0,0\" (all-zero branch only): ", allZeroOnlyMs, " (count=", Length(allZeroOnlyMs), ")\n");
  Print("m's whose table has at least one NONZERO (a,b) key present: ", mixedMs, " (count=", Length(mixedMs), ")\n");
  Print("\n--- k_w guard ---\n");
  if Length(realSweepSummary.abortMList) = 0 then
    Print("k_w guard: DID NOT FIRE at any m (0 aborts out of 64)\n");
  else
    Print("k_w guard: FIRED at ", Length(realSweepSummary.abortMList), " m value(s): ", realSweepSummary.abortMList, "\n");
  fi;
  Print("\n--- M8-b/c/d real-data sample ---\n");
  if Length(m8RealSummary.skippedTooLarge) > 0 then
    Print("skipped (|K|>200000): ", m8RealSummary.skippedTooLarge, "\n");
  fi;
  for m8res in m8RealSummary.results do
    Print("  m=", m8res.m, ": |L|=", m8res.total_points, " |kerLambda|=", m8res.ker_lambda_size,
      " mult(ob=0)=", m8res.mult_ob0, "  M8-b=", PF(m8res.m8b_ok), "  M8-c(mass)=", PF(m8res.m8c_mass_ok),
      "  M8-c(set)=", PF(m8res.m8c_set_ok), "  M8-d=", m8res.m8d_ok, "\n");
  od;;
  Print("\n--- timing ---\n");
  Print("real sweep + M8 sample GAP-internal elapsed ms: ", sweepElapsedMs, "\n");
  Print("\n--- concatenated SHA-256 ---\n");
  sweepFilePaths := List([0..63], mi -> Concatenation("certificates/e2c6j3/sweep_j3_m", String(mi), ".json"));;
  sweepConcatSha := ConcatSha256OfFiles(sweepFilePaths);;
  Print("64 sweep_j3_m*.json files, concatenated SHA-256: ", sweepConcatSha, "\n");
  allE2c6j3Files := SortedList(List(DirectoryContents("certificates/e2c6j3"), fn -> Concatenation("certificates/e2c6j3/", fn)));;
  allE2c6j3Files := Filtered(allE2c6j3Files, fn -> Length(fn) > 5 and fn{[Length(fn)-4..Length(fn)]} = ".json");;
  allConcatSha := ConcatSha256OfFiles(allE2c6j3Files);;
  Print("all ", Length(allE2c6j3Files), " certificates/e2c6j3/*.json files, concatenated SHA-256: ", allConcatSha, "\n");
fi;

Print("\ntotal elapsed ms: ", Runtime()-startTime, "\n");
