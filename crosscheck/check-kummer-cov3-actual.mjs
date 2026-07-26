#!/usr/bin/env node
// crosscheck/check-kummer-cov3-actual.mjs -- 第三 covariance の独立照合器(node・第二系統)v1
// 委嘱: 便 36(裁定 36_ben35)。search/kummer-cov3-actual.g のコード・中間結果
// は一切 import しない(独立実装)。fixture データは同一の出所
// (certificates/k5fixture/K3-regression.json .tau_rho0_j_orientation ブロック)
// から本ファイルが自前で転記・再構成する。
//
// *** 射程の限定(GAP 側と同じ・重複表示) ***
// 本証明書が検査するのは rho_0/tau/j の実値データに基づく生成元取り替え
// covariance のみ。b_i(実測の局所モノドロミー生成元・intertwiner c_i)と
// formal a(K5 sq/ns 比較指数)は本 campaign の証明書に実測値が無いため
// UNKNOWN として扱う(勝手に b:=1・a:=1 を「較正結果」と称して弱めない --
// 定義上そうなる、というだけであり独立測定ではない、と明記する)。
//
// 実行: node crosscheck/check-kummer-cov3-actual.mjs

'use strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

let pass = 0, fail = 0;
const ck = (name, ok, extra = '') => {
  if (ok) { pass++; console.log(`[PASS] ${name}${extra ? '  ' + extra : ''}`); }
  else { fail++; console.log(`[FAIL] ${name}${extra ? '  ' + extra : ''}`); }
};

// ---------------------------------------------------------------- fixture (self-transcribed, not shared with GAP script)
// 出所: certificates/k5fixture/K3-regression.json .tau_rho0_j_orientation
const N = 6;
const rho0 = {
  k0: [0, 1, 2, 3, 4, 5],
  k1: [1, 2, 0, 4, 5, 3],
  k2: [2, 0, 1, 5, 3, 4],
};
const tau2Fixture = [2, 0, 1, 5, 3, 4];
const e = 3, M = 6;

function compose(p, q) { // (p o q)(i) = p(q(i))
  return q.map((x) => p[x]);
}
function eqPerm(p, q) { return p.length === q.length && p.every((v, i) => v === q[i]); }
function power(p, k) {
  let r = [...Array(N).keys()]; // identity
  for (let i = 0; i < k; i++) r = compose(p, r);
  return r;
}

// -- sanity
ck('SANITY tau_2 (fixture) = rho0(Phi_{0,2})', eqPerm(tau2Fixture, rho0.k2));

// -- derive tau_0, tau_4 purely from the homomorphism property (tau is a hom
// mu_6 -> Sym(Lambda)) + the cited tau_2. No shared code with GAP script.
const tau0 = [...Array(N).keys()];
const tau2 = tau2Fixture;
const tau4 = compose(tau2, tau2);

ck('DERIVE tau_0 = id', eqPerm(tau0, rho0.k0));
ck('DERIVE tau_4 = tau_2^2 = rho0(Phi_{0,1})', eqPerm(tau4, rho0.k1), `tau_4=${JSON.stringify(tau4)}`);

// -- baseline j-table, independently recomputed (not copied from fixture j_table)
const baseTauByT = [tau0, tau2, tau4]; // t=0,1,2 -> tau_{2t mod 6}
const rho0ByK = [rho0.k0, rho0.k1, rho0.k2];
function findK(target) {
  for (let k = 0; k < 3; k++) if (eqPerm(rho0ByK[k], target)) return k;
  return null;
}
const baseJTable = [0, 1, 2].map((t) => findK(baseTauByT[t]));
console.log('baseJTable (t -> k) =', baseJTable);
ck('baseJTable matches fixture j_table (tt0:0, tt1:2, tt2:1)', JSON.stringify(baseJTable) === JSON.stringify([0, 2, 1]),
   `got ${JSON.stringify(baseJTable)}`);

// -- covariance: for d' in (Z/e)^x, rebuild j'-table from the NEW generator's
// powers independently, and check against the transformation law
// t' = d'^{-1} t (mod e) applied to the OLD table.
function gcd(a, b) { while (b) { [a, b] = [b, a % b]; } return a; }
const unitsModE = [];
for (let x = 1; x < e; x++) if (gcd(x, e) === 1) unitsModE.push(x);

const covarianceResults = [];
for (const dprime of unitsModE) {
  const tIdx = ((2 * dprime) % 6) / 2; // exponent 2*dprime mod 6, divided by 2 -> t-index in baseTauByT
  const newGen = baseTauByT[tIdx];
  const newTauByT = [0, 1, 2].map((tp) => power(newGen, tp));
  const newJTable = [0, 1, 2].map((tp) => findK(newTauByT[tp]));
  let dprimeInv = null;
  for (let x = 1; x <= e; x++) if ((x * dprime) % e === 1) { dprimeInv = x; break; }
  const predictedFromOld = [0, 1, 2].map((tp) => baseJTable[(dprime * tp) % e]);
  const match = JSON.stringify(newJTable) === JSON.stringify(predictedFromOld);
  covarianceResults.push({ dprime, dprimeInv, newJTable, predictedFromOld, match });
  ck(`COV d'=${dprime}: independently rebuilt j'-table = predicted-from-old via t'=d'^{-1}t(mod e)`,
     match, `newJTable=${JSON.stringify(newJTable)} predictedFromOld=${JSON.stringify(predictedFromOld)}`);
}
const allCovarianceMatch = covarianceResults.every((r) => r.match);
console.log('\nallCovarianceMatch =', allCovarianceMatch);

// -- b (formal/definitional -- NOT independently measured; see header note)
const bFormal = 1;
const bPrimeByDprime = unitsModE.map((dp) => {
  let dpInv = null;
  for (let x = 1; x <= e; x++) if ((x * dp) % e === 1) { dpInv = x; break; }
  return { dprime: dp, bPrime: (dpInv * bFormal) % e };
});
console.log('b (formal/definitional) =', bFormal);
console.log("b' = d'^{-1} * b (mod e):", bPrimeByDprime);

console.log(`\n=== node self-check: ${pass}/${pass + fail} PASS ===`);

// ---------------------------------------------------------------- cross-check vs GAP certificate
console.log('\n==== cross-check vs GAP certificate ====');
let gapCert = null;
try {
  gapCert = JSON.parse(readFileSync(join(ROOT, 'certificates', 'k5pipeline', 'K3-regression-kummer-cov3-actual.gap.json'), 'utf8'));
} catch (e) {
  console.log(`[FAIL] could not read GAP certificate: ${e}`);
}
let xpass = 0, xfail = 0;
const xck = (name, ok, extra = '') => {
  if (ok) { xpass++; console.log(`[PASS] ${name}${extra ? '  ' + extra : ''}`); }
  else { xfail++; console.log(`[FAIL] ${name}${extra ? '  ' + extra : ''}`); }
};
if (gapCert) {
  xck('GAP cert reports 0 fail', gapCert.fail === 0, `gap fail=${gapCert.fail}`);
  xck('baseJTable node==gap', JSON.stringify(baseJTable) === JSON.stringify(gapCert.baseJTable.map(Number)),
      `${JSON.stringify(baseJTable)} vs ${JSON.stringify(gapCert.baseJTable)}`);
  xck('allCovarianceMatch node==gap', allCovarianceMatch === gapCert.all_covariance_match,
      `${allCovarianceMatch} vs ${gapCert.all_covariance_match}`);
  for (const r of covarianceResults) {
    const gr = gapCert.covariance_results.find((g) => Number(g.dprime) === r.dprime);
    xck(`d'=${r.dprime}: newJTable node==gap`, gr && JSON.stringify(r.newJTable) === JSON.stringify(gr.newJTable.map(Number)),
        `${JSON.stringify(r.newJTable)} vs ${gr ? JSON.stringify(gr.newJTable) : 'MISSING'}`);
  }
}
console.log(`\n=== cross-check: ${xpass}/${xpass + xfail} PASS ===`);
console.log(`\n=== GRAND TOTAL (self ${pass}/${pass + fail} + cross ${xpass}/${xpass + xfail}) ===`);

// ---------------------------------------------------------------- final combined certificate
const finalCert = {
  schema: 'k5pipeline/kummer-cov3-actual/v1',
  retraction_note: 'Supersedes certificates/k5pipeline/retracted/K3-regression-kummer-cov3.v1.json + *-checkcov3.v1.json (search/kummer-decide.g KummerCovariance3Check + crosscheck/check-kummer-cov3.mjs, retracted per Sol 便35 F3 -- those applied Gal(K/Q) (GaloisCyc / cyclotomic ring substitution) to a witness e in K, which is NOT the required Kummer character kappa_w(gamma)=gamma(w^{1/M})/w^{1/M} for gamma in G_K, since e in K is fixed pointwise by G_K by definition.',
  scope_limitation_UNKNOWN: 'This certificate implements ONLY the rho_0/tau/j actual-value reparametrization covariance: the j-table (mu_M[e] generator -> F0 element) is independently rebuilt under a change of generator zeta_M[e] -> zeta_M[e]^{dprime} (dprime in (Z/e)^x) and checked against the transformation law tprime = dprime^{-1} t (mod e), using only certified fixture permutation data (no shared helper between GAP/node). It does NOT implement an independently measured b_i (Rule 1 §7.1: requires actual local monodromy generator ell_i and the FC-3 intertwiner c_i; not present as certified data for K3 -- K3\'s tau is defined directly via the local Kummer convention s^{1/M} -> zeta_M s^{1/M}, so b=1 reported here is definitional, not an independent measurement) and does NOT re-derive formal a=1 (Rule 1 (1.11), a K5 sq/ns comparison exponent with no meaning for a single K3 dessin). These two items are reported as UNKNOWN / explicitly out of scope, per instruction not to weaken the predicate to manufacture a false PASS.',
  e, M,
  systems: {
    gap: {
      method: 'derive tau_0/tau_4 from the tau homomorphism property + cited tau_2; rebuild j-table by raw permutation matching; rebuild j\'-table under generator change and compare to transformation law prediction',
      script: 'search/kummer-cov3-actual.g',
      certificate_file: 'certificates/k5pipeline/K3-regression-kummer-cov3-actual.gap.json',
      raw: gapCert,
    },
    node: {
      method: 'independent from-scratch reimplementation (no shared helper with the GAP script) of the same derivation, using self-transcribed fixture data',
      script: 'crosscheck/check-kummer-cov3-actual.mjs',
      self_pass: pass,
      self_fail: fail,
      baseJTable,
      covarianceResults,
      allCovarianceMatch,
      bFormal,
      bPrimeByDprime,
    },
  },
  cross_check: {
    pass: xpass,
    fail: xfail,
    note: '一致は cross-checked であって Lean の verified ではない(CLAUDE.md 語彙規律)',
  },
  conclusion: {
    rho0_tau_j_reparametrization_covariance: allCovarianceMatch,
    b_i_independently_measured: 'UNKNOWN -- not implementable from currently certified data (see scope_limitation_UNKNOWN)',
    formal_a_rederived: 'N/A -- K5 sq/ns-specific quantity, not applicable to a single K3 dessin',
  },
};
writeFileSync(join(ROOT, 'certificates', 'k5pipeline', 'K3-regression-kummer-cov3-actual.json'), JSON.stringify(finalCert, null, 2) + '\n');
console.log('\nwrote certificates/k5pipeline/K3-regression-kummer-cov3-actual.json');

if (fail > 0 || xfail > 0) process.exitCode = 1;
