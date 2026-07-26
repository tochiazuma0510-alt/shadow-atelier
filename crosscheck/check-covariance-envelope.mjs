#!/usr/bin/env node
// crosscheck/check-covariance-envelope.mjs -- sealed covariance calibration
// envelope (便 36 F4.2 の 3 点構成・裁定_37_ben36 最小条件 5・**裁定 38/便 37
// F5 で seal を実配線へ修理**)。
//
// 便 36 F4.2 が橋段(atomic Freeze 2)へ送ってはならないと指摘した 3 点を、
// 実 b_i の値を待たずに**共通の d-規約**で一つの sealed checker に束ねる:
//
//   (1) K3 の actual rho_0/tau/j 再パラメータ化 artifact(既存 PASS -- ここでは
//       再導出せず、既に独立照合済みの
//       certificates/k5pipeline/K3-regression-kummer-cov3-actual.json を
//       そのまま第一構成要素として取り込む。中身の再計算はしない)。
//       **便37 F5.2 (2) 修理**: conclusion/cross_check の抜粋だけでなく、
//       ファイル全体の SHA-256 を計算して envelope に束縛する(source の
//       他部分が変わっても同じ envelope digest になり得るという指摘への
//       修理)。
//   (2) b/k(Kummer character の離散指数)の型レベル covariance:
//       b/k -> d^{-1}(b/k)(mod e) と tau' = tau o [d] の同時変換で
//       tau'(kappa') = tau(kappa) となることの exact な型検査。実 K5 では
//       e=10((Z/10)^x)。tau は abstract(実 local monodromy データが
//       橋段前には存在しないため、tau(kappa) := kappa という恒等ラベル関数を
//       使う -- 群構造だけを検査する「型」チェックであって、特定の
//       local monodromy 値の較正ではない)。(Z/10)^x の 4 元 x kappa in Z/10
//       の 10 元 = 40 通りを**悉皆**する。
//   (3) K5 finite layer の formal invariant a(Rule 1 SS7.2・永久不変)と、
//       a_eff = [b_ns]^{-1} a [b_sq] の d-reparametrization 前後比較。
//       **便37 F5.2 (1) 修理**: formal a はハードコードせず、
//       certificates/k5fixture/K5-sq.json / K5-ns.json の
//       `rho0_and_j.a_sealed` を実読取りし、両 fixture で値が一致すること
//       を検査した上で使う。両 fixture の**ファイル全体**の SHA-256 も
//       envelope に束縛する。
//       (Z/10)^x の 4 元 x 4 元 x 4 元(d, b_sq, b_ns)= 64 通りを**悉皆**し、
//       a_eff が d の取り方に依らない不変量であること、および
//       b_sq=b_ns ⇒ a_eff=a(SS7.3 の受理条件)を exact 整数演算で確認する。
//       実 b_sq, b_ns の値は本チェッカーには代入しない -- 橋段
//       (crosscheck/covariance-bridge-in.mjs)が同じ crosscheck/
//       covariance-lib.mjs の computeAEff を呼ぶ(便37 F5.2 (3) 修理:
//       「橋段で使う同一 checker への配線」の実体化)。
//
// 独立性: 本ファイルは search/kummer-cov3-actual.g のコード・中間結果を
// import しない(K3 artifact は JSON 出力だけを読む)。(2)(3) の演算自体は
// crosscheck/covariance-lib.mjs(本ファイルと橋段 driver の両方が import する
// 共有インフラ -- Rule 1 の型レベル規約そのものであり、K5 の実データを
// ハードコードしない)。
//
// 実行: node crosscheck/check-covariance-envelope.mjs

import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { gcd, unitsMod, invMod, mulMod, restrict10to5, computeAEff } from './covariance-lib.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

let pass = 0, fail = 0;
const ck = (name, ok, extra = '') => {
  if (ok) { pass++; console.log(`[PASS] ${name}${extra ? '  ' + extra : ''}`); }
  else { fail++; console.log(`[FAIL] ${name}${extra ? '  ' + extra : ''}`); }
};

function sha256OfFile(path) {
  return createHash('sha256').update(readFileSync(path)).digest('hex');
}

// ================= (2) b/k type-level covariance (e=10, abstract tau) =================
const E10 = 10;
const unitsE10 = unitsMod(E10); // {1,3,7,9}
const covKType = [];
for (const d of unitsE10) {
  const dInv = invMod(d, E10);
  for (let kappa = 0; kappa < E10; kappa++) {
    const kappaPrime = mulMod(dInv, kappa, E10);
    const tau = (k) => k % E10;              // abstract tau(k) := k
    const tauPrime = (k) => tau(mulMod(d, k, E10)); // tau' := tau o [d]
    const lhs = tauPrime(kappaPrime);
    const rhs = tau(kappa);
    const ok = lhs === rhs;
    covKType.push({ d, kappa, kappaPrime, lhs, rhs, ok });
    if (!ok) ck(`COV-K type d=${d} kappa=${kappa}: tau'(kappa')=tau(kappa)`, ok, `lhs=${lhs} rhs=${rhs}`);
  }
}
const covKTypeAllOk = covKType.every((r) => r.ok);
ck(`COV-K type-level exhaustive check (e=10): all ${covKType.length} (d,kappa) combinations satisfy tau'(kappa')=tau(kappa)`, covKTypeAllOk);
const EXPECTED_COVK_COUNT = unitsE10.length * E10; // 4 * 10 = 40

// ================= (3) formal a (read from K5 fixtures, not re-derived) + a_eff invariance =================
// Rule 1 SS7.2: a := j_ns^{-1} j_sq = 1, permanent invariant. **便37 F5.2 (1)
// 修理**: ハードコードせず、K5 finite fixture の rho0_and_j.a_sealed を実読取り
// する(両 fixture が一致することを fail-closed に検査してから使う)。
const K5_SQ_PATH = join(ROOT, 'certificates', 'k5fixture', 'K5-sq.json');
const K5_NS_PATH = join(ROOT, 'certificates', 'k5fixture', 'K5-ns.json');
let k5Sq = null, k5Ns = null, k5SqDigest = null, k5NsDigest = null;
try {
  k5Sq = JSON.parse(readFileSync(K5_SQ_PATH, 'utf8'));
  k5SqDigest = sha256OfFile(K5_SQ_PATH);
} catch (e) {
  console.log(`[FAIL] could not read K5-sq fixture: ${e}`);
  fail++;
}
try {
  k5Ns = JSON.parse(readFileSync(K5_NS_PATH, 'utf8'));
  k5NsDigest = sha256OfFile(K5_NS_PATH);
} catch (e) {
  console.log(`[FAIL] could not read K5-ns fixture: ${e}`);
  fail++;
}
const aSealedSq = k5Sq?.rho0_and_j?.a_sealed;
const aSealedNs = k5Ns?.rho0_and_j?.a_sealed;
ck('K5-sq/K5-ns fixtures: rho0_and_j.a_sealed is present on both', aSealedSq !== undefined && aSealedNs !== undefined,
   `a_sealed(sq)=${aSealedSq} a_sealed(ns)=${aSealedNs}`);
ck('K5-sq/K5-ns fixtures: rho0_and_j.a_sealed agrees between the two fixtures (Rule 1 SS7.2 (1.11): a is a single invariant)', aSealedSq === aSealedNs);

const FORMAL_A = aSealedSq; // read-only, from fixture; NOT re-derived here.
if (typeof FORMAL_A !== 'number') {
  console.log('[FAIL] FORMAL_A could not be read from the K5-sq fixture -- aborting envelope construction');
  process.exitCode = 1;
  process.exit(1);
}

const aEffResults = [];
for (const d of unitsE10) {
  for (const bSq of unitsE10) {
    for (const bNs of unitsE10) {
      const aEff = computeAEff(bSq, bNs, FORMAL_A);
      const bSqPrime = mulMod(invMod(d, E10), bSq, E10);
      const bNsPrime = mulMod(invMod(d, E10), bNs, E10);
      const aEffPrime = computeAEff(bSqPrime, bNsPrime, FORMAL_A);
      const invariant = aEff === aEffPrime;
      aEffResults.push({ d, bSq, bNs, aEff, bSqPrime, bNsPrime, aEffPrime, invariant });
      if (!invariant) ck(`COV-A d=${d} bSq=${bSq} bNs=${bNs}: a_eff invariant under d-reparametrization`, invariant, `aEff=${aEff} aEffPrime=${aEffPrime}`);
    }
  }
}
const aEffAllInvariant = aEffResults.every((r) => r.invariant);
ck(`COV-A a_eff d-reparametrization invariance, exhaustive (e=10, 4x4x4=${aEffResults.length} combinations)`, aEffAllInvariant);
const EXPECTED_AEFF_COUNT = unitsE10.length ** 3; // 4^3 = 64

// SS7.3 acceptance rule: b_sq = b_ns => a_eff = a.
const acceptRuleResults = unitsE10.map((b) => ({ b, aEff: computeAEff(b, b, FORMAL_A) }));
const acceptRuleOk = acceptRuleResults.every((r) => r.aEff === FORMAL_A);
ck('SS7.3 acceptance rule: b_sq=b_ns => a_eff=a, for all b in (Z/10)^x', acceptRuleOk,
   JSON.stringify(acceptRuleResults));

console.log(`\n=== envelope self-check: ${pass}/${pass + fail} PASS ===`);

// ================= (1) K3 actual rho0/tau/j artifact (imported, not recomputed) =================
const K3_ACTUAL_PATH = join(ROOT, 'certificates', 'k5pipeline', 'K3-regression-kummer-cov3-actual.json');
let k3Actual = null;
let k3ActualFileDigest = null;
try {
  k3Actual = JSON.parse(readFileSync(K3_ACTUAL_PATH, 'utf8'));
  k3ActualFileDigest = sha256OfFile(K3_ACTUAL_PATH); // 便37 F5.2 (2): full-file digest, not just an excerpt.
} catch (e) {
  console.log(`[FAIL] could not read K3 actual covariance certificate: ${e}`);
  fail++;
}
const k3ActualOk = !!(k3Actual && k3Actual.conclusion && k3Actual.conclusion.rho0_tau_j_reparametrization_covariance === true
  && k3Actual.cross_check && k3Actual.cross_check.fail === 0);
ck('component (1): K3 actual rho0/tau/j reparametrization artifact reports covariance=true, cross_check.fail=0', k3ActualOk);

// ================= explicit component/check-count assertions (便37 F5.2 (5)) =================
// 「sealed 条件が pass > 0」では封印としては弱い(便37 F5.2 の指摘)。
// 期待される component 数・検査件数そのものを明示的に固定して assert する。
const EXPECTED_COMPONENTS = 3; // (1) K3 actual, (2) COV-K type-level, (3) formal a + a_eff
const actualComponentsPresent = [k3ActualOk, covKTypeAllOk, aEffAllInvariant && acceptRuleOk].filter(Boolean).length;
ck(`sealed requires exactly ${EXPECTED_COMPONENTS} components present and passing (not merely pass>0)`, actualComponentsPresent === EXPECTED_COMPONENTS,
   `present=${actualComponentsPresent}`);
ck(`sealed requires COV-K exhaustive count == ${EXPECTED_COVK_COUNT}`, covKType.length === EXPECTED_COVK_COUNT, `actual=${covKType.length}`);
ck(`sealed requires COV-A exhaustive count == ${EXPECTED_AEFF_COUNT}`, aEffResults.length === EXPECTED_AEFF_COUNT, `actual=${aEffResults.length}`);

// ================= envelope assembly + digest =================
const envelope = {
  schema: 'k5pipeline/covariance-sealed-envelope/v2',
  source_doc: 'sol/sol_reply_36_freeze1r5.md F4.2; sol/裁定_37_ben36.md 条件5; sol/sol_reply_37_freeze1r6.md F5; sol/裁定_38_ben37.md 条件3',
  d_convention: 'For a Kummer character with exponent kappa in Z/e represented via tau(kappa) (tau injective on <zeta_e>), reparametrizing the primitive root zeta_e -> zeta_e^d (d in (Z/e)^x) transforms the exponent as kappa -> kappa\' = d^{-1} kappa (mod e) and the labeling map as tau -> tau\' := tau o [d], jointly satisfying tau\'(kappa\') = tau(kappa). The restriction map [.]: (Z/10)^x -> (Z/5)^x used in SS7.2 is reduction mod 5 (bijective on these two 4-element groups).',
  components: {
    k3_actual_rho0_tau_j: {
      note: 'imported verbatim from certificates/k5pipeline/K3-regression-kummer-cov3-actual.json (not recomputed here -- that artifact is its own independent GAP/node cross-check)',
      source_file: 'certificates/k5pipeline/K3-regression-kummer-cov3-actual.json',
      source_file_sha256: k3ActualFileDigest,
      conclusion: k3Actual ? k3Actual.conclusion : null,
      cross_check: k3Actual ? k3Actual.cross_check : null,
      envelope_check_pass: k3ActualOk,
    },
    b_over_k_type_level_covariance: {
      e: E10,
      units_mod_e: unitsE10,
      tau_model: 'abstract tau(k) := k (mod e) -- schema-only check, not an actual local-monodromy calibration',
      all_combinations_checked: covKType.length,
      all_ok: covKTypeAllOk,
    },
    formal_a_and_a_eff: {
      formal_a: FORMAL_A,
      formal_a_source: {
        note: 'Rule 1 SS7.2 (1.11): a := j_ns^{-1} j_sq, permanent invariant. Read here from the K5 finite fixtures rho0_and_j.a_sealed field (NOT hardcoded, NOT re-derived) -- 便37 F5.2 (1) 修理.',
        k5_sq_source_file: 'certificates/k5fixture/K5-sq.json',
        k5_sq_source_file_sha256: k5SqDigest,
        k5_ns_source_file: 'certificates/k5fixture/K5-ns.json',
        k5_ns_source_file_sha256: k5NsDigest,
        a_sealed_sq: aSealedSq,
        a_sealed_ns: aSealedNs,
        agrees_between_fixtures: aSealedSq === aSealedNs,
      },
      restriction_map: '(Z/10)^x -> (Z/5)^x, reduce mod 5',
      all_combinations_checked: aEffResults.length,
      a_eff_invariant_under_reparametrization: aEffAllInvariant,
      acceptance_rule_b_sq_eq_b_ns_implies_a_eff_eq_a: acceptRuleOk,
      note: 'real b_sq, b_ns are supplied to the SAME crosscheck/covariance-lib.mjs computeAEff function by crosscheck/covariance-bridge-in.mjs (便37 F5.2 (3) 修理: actual bridge imports this shared library). This envelope calibrates the schema exhaustively over synthetic (Z/10)^x values, not any individual K5 model. 実 b_i の代入は atomic Freeze 2 の組立て中・受理前・u 開示前に行う(便37 F5.2 (4) の文言訂正: 「受理後」ではなく「受理前」が正しい -- b_sq=b_ns はFreeze 2/BRIDGE-IN の受理条件そのものである)。',
    },
  },
  self_check: { pass, fail },
  expected_counts: {
    components: EXPECTED_COMPONENTS,
    components_present: actualComponentsPresent,
    covk_combinations: EXPECTED_COVK_COUNT,
    covk_combinations_actual: covKType.length,
    aeff_combinations: EXPECTED_AEFF_COUNT,
    aeff_combinations_actual: aEffResults.length,
  },
  conclusion: {
    sealed: pass > 0 && fail === 0 && k3ActualOk && covKTypeAllOk && aEffAllInvariant && acceptRuleOk
      && actualComponentsPresent === EXPECTED_COMPONENTS
      && covKType.length === EXPECTED_COVK_COUNT
      && aEffResults.length === EXPECTED_AEFF_COUNT
      && aSealedSq === aSealedNs,
    note: '一致は cross-checked であって Lean の verified ではない(CLAUDE.md 語彙規律)。実 b_i の代入は atomic Freeze 2 の組立て中・受理前・u 開示前に crosscheck/covariance-bridge-in.mjs 経由で同じ computeAEff へ渡す(便37 F5.2 (3)(4))。',
  },
};

const canonicalForDigest = JSON.stringify({
  schema: envelope.schema,
  d_convention: envelope.d_convention,
  components: envelope.components,
  self_check: envelope.self_check,
  expected_counts: envelope.expected_counts,
  conclusion: envelope.conclusion,
});
envelope.envelope_digest = createHash('sha256').update(canonicalForDigest, 'utf8').digest('hex');

writeFileSync(join(ROOT, 'certificates', 'k5pipeline', 'covariance-sealed-envelope.json'), JSON.stringify(envelope, null, 2) + '\n');
console.log('\nwrote certificates/k5pipeline/covariance-sealed-envelope.json');
console.log('envelope_digest =', envelope.envelope_digest);
console.log('sealed =', envelope.conclusion.sealed);

if (fail > 0 || !envelope.conclusion.sealed) process.exitCode = 1;
