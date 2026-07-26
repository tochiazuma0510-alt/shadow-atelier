#!/usr/bin/env node
// crosscheck/check-covariance-envelope.mjs -- sealed covariance calibration
// envelope (便 36 F4.2 の 3 点構成・裁定_37_ben36 最小条件 5)。
//
// 便 36 F4.2 が橋段(atomic Freeze 2)へ送ってはならないと指摘した 3 点を、
// 実 b_i の値を待たずに**共通の d-規約**で一つの sealed checker に束ねる:
//
//   (1) K3 の actual rho_0/tau/j 再パラメータ化 artifact(既存 PASS -- ここでは
//       再導出せず、既に独立照合済みの
//       certificates/k5pipeline/K3-regression-kummer-cov3-actual.json を
//       そのまま第一構成要素として取り込む。中身の再計算はしない)。
//   (2) b/k(Kummer character の離散指数)の型レベル covariance:
//       b/k -> d^{-1}(b/k)(mod e) と tau' = tau o [d] の同時変換で
//       tau'(kappa') = tau(kappa) となることの exact な型検査。実 K5 では
//       e=10((Z/10)^x)。tau は abstract(実 local monodromy データが
//       橋段前には存在しないため、tau(kappa) := kappa という恒等ラベル関数を
//       使う -- 群構造だけを検査する「型」チェックであって、特定の
//       local monodromy 値の較正ではない)。(Z/10)^x の 4 元 x kappa in Z/10
//       の 10 元 = 40 通りを**悉皆**する。
//   (3) K5 finite layer の formal invariant a=1(Rule 1 SS7.2・永久不変 --
//       このチェッカーは a を**再導出しない**、定義値として読むだけ)と、
//       a_eff = [b_ns]^{-1} a [b_sq] の d-reparametrization 前後比較。
//       (Z/10)^x の 4 元 x 4 元 x 4 元(d, b_sq, b_ns)= 64 通りを**悉皆**し、
//       a_eff が d の取り方に依らない不変量であること、および
//       b_sq=b_ns ⇒ a_eff=a=1(SS7.3 の受理条件)を exact 整数演算で確認する。
//       実 b_sq, b_ns の値は本チェッカーには代入しない(橋段で同じ関数
//       computeAEff/checkCovariantInvariance へ実値を渡す設計 -- synthetic
//       な全域悉皆でスキーマだけを較正する)。
//
// 独立性: 本ファイルは search/kummer-cov3-actual.g のコード・中間結果を
// import しない(K3 artifact は JSON 出力だけを読む)。(2)(3) は本ファイルの
// 自己完結した exact 整数演算(BigInt 不要 -- 群の位数が小さいので Number で
// 十分。ただし演算はすべて mod 演算の厳密整数比較で浮動小数点を使わない)。
//
// 実行: node crosscheck/check-covariance-envelope.mjs

import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

let pass = 0, fail = 0;
const ck = (name, ok, extra = '') => {
  if (ok) { pass++; console.log(`[PASS] ${name}${extra ? '  ' + extra : ''}`); }
  else { fail++; console.log(`[FAIL] ${name}${extra ? '  ' + extra : ''}`); }
};

function gcd(a, b) { while (b) { [a, b] = [b, a % b]; } return a; }
function unitsMod(n) {
  const r = [];
  for (let x = 1; x < n; x++) if (gcd(x, n) === 1) r.push(x);
  return r;
}
function invMod(x, n) {
  for (let y = 1; y < n; y++) if ((x * y) % n === 1) return y;
  throw new Error(`invMod: ${x} has no inverse mod ${n}`);
}
function mulMod(x, y, n) { return ((x * y) % n + n) % n; }

// -- restriction map [.]: (Z/10)^x -> (Z/5)^x, per Rule 1 SS7.2 ("(Z/10)^x ->
// (Z/5)^x は全単射ゆえ lift の曖昧さはない"): reduce mod 5.
function restrict10to5(b) { return ((b % 5) + 5) % 5; }

// ================= (2) b/k type-level covariance (e=10, abstract tau) =================
// tau: Z/10 -> {label}. Since no actual local-monodromy target group exists
// pre-bridge, tau is the identity label function tau(k) := k -- this checks
// the GROUP-THEORETIC schema (kappa' = d^{-1} kappa (mod e) combined with
// tau' := tau o [d] recovers tau(kappa)), not a specific numeric calibration.
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

// ================= (3) formal a=1 + a_eff invariance (e=10 -> restrict to Z/5) =================
// Rule 1 SS7.2: a := j_ns^{-1} j_sq = 1, permanent invariant. NOT re-derived
// here -- read as a defined constant.
const FORMAL_A = 1; // Rule 1 SS7.2 (1.11) -- formal invariant, read-only, never updated.

function computeAEff(bSq, bNs, a) {
  const bSq5 = restrict10to5(bSq);
  const bNs5 = restrict10to5(bNs);
  const bNs5Inv = invMod(bNs5, 5);
  return mulMod(mulMod(bNs5Inv, a, 5), bSq5, 5);
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

// SS7.3 acceptance rule: b_sq = b_ns => a_eff = a = 1.
const acceptRuleResults = unitsE10.map((b) => ({ b, aEff: computeAEff(b, b, FORMAL_A) }));
const acceptRuleOk = acceptRuleResults.every((r) => r.aEff === FORMAL_A);
ck('SS7.3 acceptance rule: b_sq=b_ns => a_eff=a=1, for all b in (Z/10)^x', acceptRuleOk,
   JSON.stringify(acceptRuleResults));

console.log(`\n=== envelope self-check: ${pass}/${pass + fail} PASS ===`);

// ================= (1) K3 actual rho0/tau/j artifact (imported, not recomputed) =================
let k3Actual = null;
try {
  k3Actual = JSON.parse(readFileSync(join(ROOT, 'certificates', 'k5pipeline', 'K3-regression-kummer-cov3-actual.json'), 'utf8'));
} catch (e) {
  console.log(`[FAIL] could not read K3 actual covariance certificate: ${e}`);
  fail++;
}
const k3ActualOk = !!(k3Actual && k3Actual.conclusion && k3Actual.conclusion.rho0_tau_j_reparametrization_covariance === true
  && k3Actual.cross_check && k3Actual.cross_check.fail === 0);
ck('component (1): K3 actual rho0/tau/j reparametrization artifact reports covariance=true, cross_check.fail=0', k3ActualOk);

// ================= envelope assembly + digest =================
const envelope = {
  schema: 'k5pipeline/covariance-sealed-envelope/v1',
  source_doc: 'sol/sol_reply_36_freeze1r5.md F4.2; sol/裁定_37_ben36.md 条件5',
  d_convention: 'For a Kummer character with exponent kappa in Z/e represented via tau(kappa) (tau injective on <zeta_e>), reparametrizing the primitive root zeta_e -> zeta_e^d (d in (Z/e)^x) transforms the exponent as kappa -> kappa\' = d^{-1} kappa (mod e) and the labeling map as tau -> tau\' := tau o [d], jointly satisfying tau\'(kappa\') = tau(kappa). The restriction map [.]: (Z/10)^x -> (Z/5)^x used in SS7.2 is reduction mod 5 (bijective on these two 4-element groups).',
  components: {
    k3_actual_rho0_tau_j: {
      note: 'imported verbatim from certificates/k5pipeline/K3-regression-kummer-cov3-actual.json (not recomputed here -- that artifact is its own independent GAP/node cross-check)',
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
      formal_a_source: 'Rule 1 SS7.2 (1.11): a := j_ns^{-1} j_sq = 1, permanent invariant -- read here, NOT re-derived',
      restriction_map: '(Z/10)^x -> (Z/5)^x, reduce mod 5',
      all_combinations_checked: aEffResults.length,
      a_eff_invariant_under_reparametrization: aEffAllInvariant,
      acceptance_rule_b_sq_eq_b_ns_implies_a_eff_eq_1: acceptRuleOk,
      note: 'real b_sq, b_ns are supplied at the bridge stage to the SAME computeAEff/covariance functions; this envelope calibrates the schema exhaustively over synthetic (Z/10)^x values, not any individual K5 model',
    },
  },
  self_check: { pass, fail },
  conclusion: {
    sealed: pass > 0 && fail === 0 && k3ActualOk && covKTypeAllOk && aEffAllInvariant && acceptRuleOk,
    note: '一致は cross-checked であって Lean の verified ではない(CLAUDE.md 語彙規律)。実 b_i の代入は橋段(atomic Freeze 2 受理後)へ送る -- 便 36 F4.1/F4.2。',
  },
};

const canonicalForDigest = JSON.stringify({
  schema: envelope.schema,
  d_convention: envelope.d_convention,
  components: envelope.components,
  self_check: envelope.self_check,
  conclusion: envelope.conclusion,
});
envelope.envelope_digest = createHash('sha256').update(canonicalForDigest, 'utf8').digest('hex');

writeFileSync(join(ROOT, 'certificates', 'k5pipeline', 'covariance-sealed-envelope.json'), JSON.stringify(envelope, null, 2) + '\n');
console.log('\nwrote certificates/k5pipeline/covariance-sealed-envelope.json');
console.log('envelope_digest =', envelope.envelope_digest);
console.log('sealed =', envelope.conclusion.sealed);

if (fail > 0 || !envelope.conclusion.sealed) process.exitCode = 1;
