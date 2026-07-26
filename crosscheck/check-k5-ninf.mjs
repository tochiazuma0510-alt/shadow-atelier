#!/usr/bin/env node
// crosscheck/check-k5-ninf.mjs -- (N_infty) 副枝の排除証明書の独立照合器 (node, 第二系統)
//
// 独立性の規律 (CLAUDE.md): search/k5-ninf-exclusion.g のコード・中間結果は
// 一切 import しない。simultaneous conjugator の探索はここで自前実装する
// (GAP の RepresentativeAction / OnTuples の実装は読んでいない)。GAP 側は
// 群論の代数的アルゴリズム(backtrack)、こちら側は S_10 全体の総当り
// (brute force, 3,628,800 通り)で同じ存在問題を解く -- 手法自体を独立にする。
//
// 入力: (1) certificates/k5fixture/K5-sq.json, K5-ns.json の perm_triple
//          フィールドのみ(= 凍結済み有限 fixture の生データ)。
//       (2) 比較対象として certificates/k5pipeline/ninf-exclusion.gap.json
//          (GAP 側が書き出した証明書 -- 「一致」は cross-checked の意味で
//          あって verified ではない)。GAP の .g ソースは読まない。
//
// 接触禁止: 曲線・lambda・u・数値近似・database には一切触れない。モデル・
// lambda・u には一切触れない(perm_triple のみが入力)。
//
// 委嘱: docs/week4-K5_Rule1_v1.md v1.2 S11 論点 7 / 補題 R1-N∞-S。
// 補題 3.: (N_infty) が生じるなら ordered dessin は (0 infty)-交換
// (Mobius 対合 lambda -> 1/lambda) で不変でなければならない。この交換は
// monodromy 三つ組レベルでは、simultaneous conjugation で
//   sigma_0 -> sigma_infty, sigma_1 -> sigma_1, sigma_infty -> sigma_0
// を実現する g in S_10 の存在として現れる(委嘱書の指定通り、向き規約に
// 依存しない保守形)。この g が存在しなければ (0 infty)-交換不変性が破れる
// ので、対偶により (N_infty) はこの dessin について発火し得ない(排除)。
// g が存在すれば判定不能(排除できない、というだけで発火を意味しない)。
//
// 期待("対称性なし ⇒ 発火しない")は判定に使わない。結果は結果として記録する。
//
// 実行: node crosscheck/check-k5-ninf.mjs

'use strict';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

let pass = 0, fail = 0;
const ck = (name, ok, extra = '') => {
  if (ok) { pass++; console.log(`[PASS] ${name}${extra ? '  ' + extra : ''}`); }
  else { fail++; console.log(`[FAIL] ${name}${extra ? '  ' + extra : ''}`); }
};

// ---------------------------------------------------------------- fixture
// certificates/k5fixture/{K5-sq,K5-ns}.json の perm_triple フィールドを
// 生データとして読む(他フィールドは見ない -- 本照合は置換三つ組のみ対象)。
function loadFixture(name) {
  const j = JSON.parse(readFileSync(join(ROOT, 'certificates', 'k5fixture', `${name}.json`), 'utf8'));
  const pt = j.perm_triple;
  return { s0: pt.sigma_0.slice(), s1: pt.sigma_1.slice(), sInf: pt.sigma_infty.slice() };
}

// ---------------------------------------------------------------- permutations
// 規約(fixture の "convention" フィールドと同一): perm は長さ 10 の配列、
// perm[i] = 点 i (0-indexed) の像。合成規約: (p o q)(i) = p(q(i))。
const N = 10;
const identityN = [...Array(N).keys()];
const eqPerm = (p, q) => p.length === q.length && p.every((v, i) => v === q[i]);
const isIdentity = (p) => eqPerm(p, identityN);

function composeArr(p, q, n) {
  const r = new Array(n);
  for (let i = 0; i < n; i++) r[i] = p[q[i]];
  return r;
}
function cycleType(p, domain) {
  const dom = domain.slice().sort((a, b) => a - b);
  const inDom = new Set(dom);
  const seen = new Set();
  const lens = [];
  for (const start of dom) {
    if (seen.has(start)) continue;
    let cur = start, len = 0;
    do {
      seen.add(cur);
      len++;
      cur = p[cur];
      if (!inDom.has(cur)) throw new Error('domain not invariant under p');
    } while (cur !== start);
    lens.push(len);
  }
  lens.sort((a, b) => b - a);
  return lens;
}
function sign(p) {
  // parity from cycle type: sign = (-1)^(n - #cycles)
  const t = cycleType(p, identityN);
  return (N - t.length) % 2 === 0 ? 1 : -1;
}

// ---------------------------------------------------------------- brute-force
// simultaneous-conjugator search over ALL of S_10 (3,628,800 permutations),
// no structural assumption (single-cycle centralizer argument, etc.) used --
// exhaustive ("kaikai") as designated by the task as an acceptable method.
// Condition tested for candidate g (array, g[i] = image of point i):
//   E1: g[s0[x]]   == sInf[g[x]]  for all x   (g s0 g^-1 = sInf)
//   E2: g[sInf[x]] == s0[g[x]]    for all x   (g sInf g^-1 = s0)
//   E3: g[s1[x]]   == s1[g[x]]    for all x   (g s1 g^-1 = s1)
// All three simultaneously realize the (0,infty)-exchange conjugator.
//
// Heap's algorithm (iterative) generates all permutations of [0..N-1] without
// building an intermediate array copy at each step.
function findConjugators(s0, s1, sInf) {
  const found = [];
  const a = identityN.slice();
  const c = new Array(N).fill(0);

  const test = (g) => {
    for (let x = 0; x < N; x++) {
      if (g[s0[x]] !== sInf[g[x]]) return false;
    }
    for (let x = 0; x < N; x++) {
      if (g[sInf[x]] !== s0[g[x]]) return false;
    }
    for (let x = 0; x < N; x++) {
      if (g[s1[x]] !== s1[g[x]]) return false;
    }
    return true;
  };

  let count = 0;
  if (test(a)) found.push(a.slice());
  count++;

  let i = 0;
  while (i < N) {
    if (c[i] < i) {
      if (i % 2 === 0) {
        const tmp = a[0]; a[0] = a[i]; a[i] = tmp;
      } else {
        const tmp = a[c[i]]; a[c[i]] = a[i]; a[i] = tmp;
      }
      if (test(a)) found.push(a.slice());
      count++;
      c[i]++;
      i = 0;
    } else {
      c[i] = 0;
      i++;
    }
  }
  return { found, totalGenerated: count };
}

// ---------------------------------------------------------------- main per-target
function processTarget(label, fx) {
  console.log(`\n==== target: ${label} ====`);
  const { s0, s1, sInf } = fx;

  // S0: sigma_0 sigma_1 sigma_infty = id under (p o q)(i) = p(q(i)):
  // apply sigma_infty first, then sigma_1, then sigma_0: h(i) = s0(s1(sInf(i))).
  const h = identityN.map(i => s0[s1[sInf[i]]]);
  ck(`${label}-S0 sigma_0 sigma_1 sigma_infty = id (composition conv.)`, isIdentity(h), '');

  const t0 = cycleType(s0, identityN);
  const tInf = cycleType(sInf, identityN);
  const t1 = cycleType(s1, identityN);
  ck(`${label}-INV sigma_0 is a single 10-cycle`, JSON.stringify(t0) === '[10]', `got ${JSON.stringify(t0)}`);
  ck(`${label}-INV sigma_infty is a single 10-cycle`, JSON.stringify(tInf) === '[10]', `got ${JSON.stringify(tInf)}`);
  const s1sign = sign(s1);
  ck(`${label}-INV sigma_1 has even sign (product relation forces this)`, s1sign === 1, `sign=${s1sign}`);
  const oddCount = t1.filter(x => x % 2 === 1).length;
  ck(`${label}-INV # odd-length cycles of sigma_1 <= 6 (R1-N-infty-S pt.4 necessary cond.)`,
     oddCount <= 6, `count=${oddCount}`);

  const t0start = Date.now();
  const { found, totalGenerated } = findConjugators(s0, s1, sInf);
  const elapsedMs = Date.now() - t0start;
  const existsFlag = found.length > 0;
  ck(`${label}-MAIN (0,infty)-exchange conjugator g in S_10: exists? (brute force, ${totalGenerated} perms checked, ${elapsedMs}ms)`,
     true, `exists=${existsFlag} count=${found.length}`);
  const exclusion = !existsFlag;
  if (exclusion) {
    console.log(`  => (N_infty) EXCLUDED for target ${label} (no such g; contrapositive of R1-N-infty-S 3.)`);
  } else {
    console.log(`  => (N_infty) NOT excluded by this certificate for target ${label} (a conjugator g exists; UNDETERMINED, not a proof of presence)`);
  }

  return {
    target: label,
    sanity_relation_ok: isIdentity(h),
    cycle_type_sigma0: t0,
    cycle_type_sigmaInf: tInf,
    cycle_type_sigma1: t1,
    sign_sigma1: s1sign,
    odd_length_cycle_count_sigma1: oddCount,
    total_permutations_checked: totalGenerated,
    conjugator_exists: existsFlag,
    conjugator_count: found.length,
    conjugators_g_0indexed: found,
    ninf_excluded: exclusion,
    elapsed_ms: elapsedMs,
  };
}

const nodeResults = {};
for (const name of ['sq', 'ns']) {
  const fx = loadFixture(`K5-${name}`);
  nodeResults[name] = processTarget(name, fx);
}

console.log(`\n=== node self-check: ${pass}/${pass + fail} PASS ===`);

// ---------------------------------------------------------------- cross-check against GAP certificate
console.log('\n==== cross-check vs GAP certificate (certificates/k5pipeline/ninf-exclusion.gap.json) ====');
let gapCert = null;
try {
  gapCert = JSON.parse(readFileSync(join(ROOT, 'certificates', 'k5pipeline', 'ninf-exclusion.gap.json'), 'utf8'));
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
  for (const name of ['sq', 'ns']) {
    const nd = nodeResults[name];
    const gp = gapCert.targets[name];
    xck(`${name}: conjugator_exists node==gap`, nd.conjugator_exists === gp.conjugator_exists,
        `${nd.conjugator_exists} vs ${gp.conjugator_exists}`);
    xck(`${name}: ninf_excluded node==gap`, nd.ninf_excluded === gp.ninf_excluded,
        `${nd.ninf_excluded} vs ${gp.ninf_excluded}`);
    xck(`${name}: cycle_type_sigma0 node==gap`, JSON.stringify(nd.cycle_type_sigma0) === JSON.stringify(gp.cycle_type_sigma0.map(Number)),
        `${JSON.stringify(nd.cycle_type_sigma0)} vs ${JSON.stringify(gp.cycle_type_sigma0)}`);
    xck(`${name}: cycle_type_sigmaInf node==gap`, JSON.stringify(nd.cycle_type_sigmaInf) === JSON.stringify(gp.cycle_type_sigmaInf.map(Number)),
        `${JSON.stringify(nd.cycle_type_sigmaInf)} vs ${JSON.stringify(gp.cycle_type_sigmaInf)}`);
    xck(`${name}: odd_length_cycle_count_sigma1 node==gap`, nd.odd_length_cycle_count_sigma1 === gp.odd_length_cycle_count_sigma1,
        `${nd.odd_length_cycle_count_sigma1} vs ${gp.odd_length_cycle_count_sigma1}`);
  }
}

console.log(`\n=== cross-check: ${xpass}/${xpass + xfail} PASS ===`);
console.log(`\n=== GRAND TOTAL (self ${pass}/${pass + fail} + cross ${xpass}/${xpass + xfail}) ===`);

// ---------------------------------------------------------------- final combined certificate
// certificates/k5pipeline/ninf-exclusion.json -- 二系統の結果+判定根拠
// (委嘱書の指定するデリバラブル本体。GAP 側 .gap.json はその生成物として
// 埋め込む。)
mkdirSync(join(ROOT, 'certificates', 'k5pipeline'), { recursive: true });

const finalCert = {
  schema: 'k5pipeline/ninf-exclusion/v1',
  source_doc: 'docs/week4-K5_Rule1_v1.md v1.2 S11 論点7 / 補題 R1-N∞-S',
  question: 'sigma_0 <-> sigma_infty を交換し sigma_1 を保つ simultaneous conjugator g in S_10 は存在するか(存在しなければ、補題 R1-N∞-S 3. の対偶により (N_infty) はこの dessin について発火し得ない)',
  inputs: 'certificates/k5fixture/K5-sq.json, K5-ns.json の perm_triple のみ(model/lambda/u には一切接触なし)',
  expectation_not_used_in_judgement: '「対称性なし ⇒ (N_infty) は両 dessin で発火しない」という期待は判定に使っていない。以下は結果そのもの。',
  systems: {
    gap: {
      method: 'RepresentativeAction(SymmetricGroup(10), [s0,s1,sInf], [sInf,s1,s0], OnTuples) -- backtrack search (group-theoretic algebraic algorithm)',
      script: 'search/k5-ninf-exclusion.g',
      certificate_file: 'certificates/k5pipeline/ninf-exclusion.gap.json',
      raw: gapCert,
    },
    node: {
      method: 'brute force over all 3,628,800 permutations of S_10 (Heap\'s algorithm), testing g s0 g^-1 = sInf AND g sInf g^-1 = s0 AND g s1 g^-1 = s1 directly by permutation composition -- no shared code/helper with the GAP script, independent from-scratch implementation',
      script: 'crosscheck/check-k5-ninf.mjs',
      self_pass: pass,
      self_fail: fail,
      results: nodeResults,
    },
  },
  cross_check: {
    pass: xpass,
    fail: xfail,
    note: '一致は cross-checked であって Lean の verified ではない(CLAUDE.md 語彙規律)',
  },
  conclusion: {
    sq: {
      ninf_excluded_gap: gapCert ? gapCert.targets.sq.ninf_excluded : null,
      ninf_excluded_node: nodeResults.sq.ninf_excluded,
      agree: gapCert ? (gapCert.targets.sq.ninf_excluded === nodeResults.sq.ninf_excluded) : null,
    },
    ns: {
      ninf_excluded_gap: gapCert ? gapCert.targets.ns.ninf_excluded : null,
      ninf_excluded_node: nodeResults.ns.ninf_excluded,
      agree: gapCert ? (gapCert.targets.ns.ninf_excluded === nodeResults.ns.ninf_excluded) : null,
    },
  },
};

writeFileSync(join(ROOT, 'certificates', 'k5pipeline', 'ninf-exclusion.json'), JSON.stringify(finalCert, null, 2) + '\n');
console.log('\nwrote certificates/k5pipeline/ninf-exclusion.json');

if (fail > 0 || xfail > 0) process.exitCode = 1;
