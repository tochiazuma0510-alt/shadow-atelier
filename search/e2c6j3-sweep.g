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
  return rec(table:=mult, total:=total, span_size:=Length(span), baseQ:=baseQ);
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
  local mIt, snfD, res, f0, path, cert, tblS, tblB, entriesS, tableStrs;
  Print("  [UNLOCKED] running real-universe sweep, j=3, m=0..63 ...\n");
  for mIt in [0..63] do
    snfD := BuildSnfData(BuildLinearSystemC6, mIt);;
    res := TestAtJ(snfD, 3);;
    path := Concatenation("certificates/e2c6j3/sweep_j3_m", String(mIt), ".json");;
    if res.solvable then
      f0 := ExtractF0(snfD, 3);;
      tblS := BuildJ3MultTableShortcut(f0, res.kgens, mIt);;
      tblB := BuildJ3MultTableBruteForce(f0, res.kgens, mIt);;
      entriesS := RecNames(tblS.table);;
      tableStrs := List(entriesS, k -> Concatenation("\"", k, "\":", String(tblS.table.(k))));;
      cert := Concatenation(
        "{\"claim\":\"m6j3_multiplicity_table\",\"fixture\":\"real_sweep\",",
        "\"m\":", String(mIt), ",\"j\":3,\"modulus\":8,\"R\":4,\"linear_solvable\":true,",
        "\"witness_f0_abar\":\"", String(f0), "\",",
        "\"K_generators\":[", JoinC(List(res.kgens, g -> String(g.vec)), ","), "],",
        "\"K_orders\":[", JoinC(List(res.kgens, g -> String(g.order)), ","), "],",
        "\"total_points\":", String(tblS.total), ",",
        "\"ob_table\":{", JoinC(tableStrs, ","), "},",
        "\"brute_force_matches_shortcut\":", JB(TablesEqual(tblS.table, tblB.table)), ",",
        "\"ob_mode\":\"quotient-ratified-v2\"}");;
      WriteFile(path, cert);;
    else
      cert := Concatenation("{\"claim\":\"linear_stage_empty_c6j3\",\"linear_solvable\":false,",
        "\"fixture\":\"real_sweep\",\"m\":", String(mIt), ",\"j\":3,\"modulus\":8}");;
      WriteFile(path, cert);;
    fi;
  od;;
  Print("  real-universe sweep complete: certificates/e2c6j3/sweep_j3_m*.json (64 files)\n");
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

if fireUnlockedJ3 then
  Print("[UNLOCKED] real-universe sweep authorized by search/FIRE_e2c6j3.auth (hash-matched)\n");
  RunRealSweepC6J3();;
else
  Print("[LOCKED] real-universe sweep requires FIRE_e2c6j3.auth (commander issues at fire time)\n");
fi;

Print("\n=== FINAL SUMMARY (j=3 gate) ===\n");
Print("[", PF(kwZeroOk and kwAnyRun), "] precondition: k_w=0 mod 8\n");
Print("[", PF(g1Ok and g1AnyRun), "] G1 false-positive detector (sum=|L| + shortcut==brute-force)\n");
Print("[", PF(g2Ok), "] G2 class-5 control (j=3) + projection agreement vs frozen j=2 gate\n");
Print("[", PF(G3AllOk), "] G3 route-G cross-check (mod-8-reduced test vectors)\n");
Print("[", PF(g4Combined), "] G4 M-series (R=4, (1+theta)ker(N_C) recomputed)\n");
Print("[", PF(fireUnlockedJ3 = false), "] fire lock CLOSED (real sweep NOT run this pass)\n");
Print("\ntotal elapsed ms: ", Runtime()-startTime, "\n");
