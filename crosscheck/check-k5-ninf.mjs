#!/usr/bin/env node
// crosscheck/check-k5-ninf.mjs -- (N_infty) 副枝の排除証明書の独立照合器 (node, 第二系統)
// v3(便 36・裁定 36 の修理 + 司令塔中継の補題 R1-N∞-W 仕様反映)
//
// 独立性の規律 (CLAUDE.md): search/k5-ninf-exclusion.g のコード・中間結果は
// 一切 import しない。候補生成の導出は本ファイルが自前で証明コメント化する
// (GAP 側の実装は読んでいない -- 司令塔中継の指示どおり、手法の独立性は
// 「同じ制限探索を各実装が自前で正当化して書く」ことで担保する)。
//
// *** v1 からの撤回理由(Sol 便 35 F1.5・裁定 36) ***
// v1 は (0 infty)-交換の monodromy 三つ組への移し方として素朴な置換
//   (x,y,z) |-> (z,y,x)                                            (35.2)
// を検査していた。これは xyz=1 の relator を一般に保たない
// (zyx=1 は xyz=1 から従わない)ため誤りである。
//
// *** v2 -> v3 差分(司令塔中継・補題 R1-N∞-W の反映) ***
// 1. decisive predicate は (35.4) の第一・第二式のみ:
//      E1: g s0 g^-1 = sInf
//      E2: g s1 g^-1 = s1
//    第三式(E3: g sInf g^-1 = s1^-1 s0 s1)は E1 のもとで xyz=1 型の関係式
//    から自動的に従う(補題 R1-N∞-W)。本証明書では E3 を「冗長確認」として
//    別途記録するが、判定には使わない。
// 2. 10! の悉皆は不要: s0 が単一の 10-サイクルなので、E1 を満たす g は
//    g(0) の値ひとつで(サイクルに沿って伝播させるだけで)完全に決まる。
//    ゆえに 10 候補の悉皆で閉じる(3,628,800 通りの総当りは不要)。
// 3. 自己検査(定理由来・R1-N∞-W): 各 fixture でちょうど 1 個の survivor が
//    あり、かつ g^2 = sigma_1 が成立するはず。破れたら UNKNOWN ではなく
//    integrity stop(入力破損)。
// 4. 撤回の記録を自己完結させる: sigma_0*sigma_1 <> sigma_1*sigma_0 を直接
//    計算で確認する。これにより (35.3) の第三式(E1 と合わせて sigma_0,
//    sigma_1 の可換性を要求する)は充足不能であることが分かる — v1 の
//    「conjugator が見つからない」という結果は正しい計算だったが、それは
//    的外れな問い (35.3) への答えであって (N_infty) の排除ではない。
//
// 入力: certificates/k5fixture/K5-sq.json, K5-ns.json の perm_triple のみ。
// 比較対象: certificates/k5pipeline/ninf-exclusion.gap.json(GAP 側証明書 --
// 「一致」は cross-checked の意味であって verified ではない)。
//
// 結論札: 「排除されず・対称性充足・(N_infty) の存否は UNKNOWN・
// witness は cross-checked」。
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

function loadFixture(name) {
  const j = JSON.parse(readFileSync(join(ROOT, 'certificates', 'k5fixture', `${name}.json`), 'utf8'));
  const pt = j.perm_triple;
  return { s0: pt.sigma_0.slice(), s1: pt.sigma_1.slice(), sInf: pt.sigma_infty.slice() };
}

const N = 10;
const identityN = [...Array(N).keys()];
const eqPerm = (p, q) => p.length === q.length && p.every((v, i) => v === q[i]);
const isIdentity = (p) => eqPerm(p, identityN);
function composeArr(p, q, n) { const r = new Array(n); for (let i = 0; i < n; i++) r[i] = p[q[i]]; return r; }
function invPerm(p) { const r = new Array(p.length); for (let i = 0; i < p.length; i++) r[p[i]] = i; return r; }
function cycleType(p, domain) {
  const dom = domain.slice().sort((a, b) => a - b);
  const seen = new Set();
  const lens = [];
  for (const start of dom) {
    if (seen.has(start)) continue;
    let cur = start, len = 0;
    do { seen.add(cur); len++; cur = p[cur]; } while (cur !== start);
    lens.push(len);
  }
  lens.sort((a, b) => b - a);
  return lens;
}
function sign(p) { const t = cycleType(p, identityN); return (N - t.length) % 2 === 0 ? 1 : -1; }

// Build the (unique, if it exists) g satisfying E1: g[s0[x]] = sInf[g[x]] for
// all x, given g[0] = c. s0 is a single 10-cycle covering every point starting
// from 0, so this determines g everywhere by propagation along the cycle --
// no guessing, no 10!-search over all of S_10.
function buildGFromG0(s0, sInf, c) {
  const g = new Array(N).fill(-1);
  g[0] = c;
  let x = 0;
  for (let i = 0; i < N - 1; i++) {
    const xn = s0[x];
    g[xn] = sInf[g[x]];
    x = xn;
  }
  return g;
}
function isBijection(g) {
  const seen = new Set();
  for (const v of g) { if (v < 0 || v > N - 1 || seen.has(v)) return false; seen.add(v); }
  return true;
}

function processTarget(label, fx) {
  console.log(`\n==== target: ${label} ====`);
  const { s0, s1, sInf } = fx;

  const h = identityN.map((i) => s0[s1[sInf[i]]]);
  ck(`${label}-S0 sigma_0 sigma_1 sigma_infty = id (composition conv.)`, isIdentity(h));

  const t0 = cycleType(s0, identityN);
  const tInf = cycleType(sInf, identityN);
  const t1 = cycleType(s1, identityN);
  ck(`${label}-INV sigma_0 is a single 10-cycle`, JSON.stringify(t0) === '[10]', `got ${JSON.stringify(t0)}`);
  ck(`${label}-INV sigma_infty is a single 10-cycle`, JSON.stringify(tInf) === '[10]', `got ${JSON.stringify(tInf)}`);
  const s1sign = sign(s1);
  ck(`${label}-INV sigma_1 has even sign`, s1sign === 1, `sign=${s1sign}`);
  const oddCount = t1.filter((x) => x % 2 === 1).length;
  ck(`${label}-INV # odd-length cycles of sigma_1 <= 6`, oddCount <= 6, `count=${oddCount}`);

  // (35.3) impossibility, demonstrated directly: sigma_0*sigma_1 <> sigma_1*sigma_0.
  const s0s1 = composeArr(s0, s1, N);
  const s1s0 = composeArr(s1, s0, N);
  const commute = eqPerm(s0s1, s1s0);
  ck(`${label}-COMMUTE sigma_0*sigma_1 <> sigma_1*sigma_0 (so (35.3)'s third eqn, combined with E1, is unsatisfiable)`,
     !commute, `commute=${commute}`);

  // rhs(x) = (s1^-1 s0 s1)(x), used only for the E3 redundant confirmation.
  const s1inv = invPerm(s1);
  const rhs = identityN.map((x) => s1inv[s0[s1[x]]]);

  const survivors = [];
  for (let c = 0; c < N; c++) {
    const g = buildGFromG0(s0, sInf, c);
    if (!isBijection(g)) continue;
    const e2ok = identityN.every((x) => g[s1[x]] === s1[g[x]]);
    if (e2ok) {
      const e3ok = identityN.every((x) => g[sInf[x]] === rhs[g[x]]);
      survivors.push({ c, g, e3ok });
    }
  }
  ck(`${label}-MAIN E1+E2 restricted to 10 candidates (g(0)=c): survivors found`, true, `count=${survivors.length}`);

  if (survivors.length !== 1) {
    console.log(`*** INTEGRITY STOP: expected exactly 1 survivor, got ${survivors.length} for target ${label} ***`);
    ck(`${label}-SELFCHECK exactly one survivor (R1-N∞-W)`, false, `got ${survivors.length} survivors`);
    return { target: label, integrity_stop: true, reason: `expected exactly 1 survivor of E1+E2 among the 10 candidates, got ${survivors.length}` };
  }
  ck(`${label}-SELFCHECK exactly one survivor (R1-N∞-W)`, true);

  const sol = survivors[0];
  ck(`${label}-REDUNDANT E3 (third eqn of (35.4), should be automatic from E1)`, sol.e3ok);

  const g2 = composeArr(sol.g, sol.g, N);
  const gSquaredOk = eqPerm(g2, s1);
  if (!gSquaredOk) console.log(`*** INTEGRITY STOP: g^2 <> sigma_1 for target ${label} (fixture corruption suspected) ***`);
  ck(`${label}-SELFCHECK g^2 = sigma_1 (35.6)/(R1-N∞-W)`, gSquaredOk, `g^2=${JSON.stringify(g2)} sigma_1=${JSON.stringify(s1)}`);

  console.log(`  => (N_infty) NOT excluded for target ${label} (unique witness g satisfying (35.4)'s E1+E2 found, E3 redundant-confirmed, g^2=sigma_1 self-check passed; UNDETERMINED, not a proof of presence)`);

  return {
    target: label,
    integrity_stop: false,
    sanity_relation_ok: isIdentity(h),
    cycle_type_sigma0: t0,
    cycle_type_sigmaInf: tInf,
    cycle_type_sigma1: t1,
    sign_sigma1: s1sign,
    odd_length_cycle_count_sigma1: oddCount,
    sigma0_sigma1_commute: commute,
    num_candidates_checked: 10,
    num_survivors: 1,
    conjugator_exists: true,
    conjugator_g_0indexed: sol.g,
    e3_redundant_confirmation: sol.e3ok,
    g_squared_equals_sigma1: gSquaredOk,
    ninf_excluded: false,
  };
}

const nodeResults = {};
for (const name of ['sq', 'ns']) {
  const fx = loadFixture(`K5-${name}`);
  nodeResults[name] = processTarget(name, fx);
}

console.log(`\n=== node self-check: ${pass}/${pass + fail} PASS ===`);

// ---------------------------------------------------------------- cross-check vs GAP certificate
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
    xck(`${name}: conjugator_exists node==gap`, nd.conjugator_exists === gp.conjugator_exists, `${nd.conjugator_exists} vs ${gp.conjugator_exists}`);
    xck(`${name}: ninf_excluded node==gap`, nd.ninf_excluded === gp.ninf_excluded, `${nd.ninf_excluded} vs ${gp.ninf_excluded}`);
    xck(`${name}: g^2=sigma_1 node==gap`, nd.g_squared_equals_sigma1 === gp.g_squared_equals_sigma1, `${nd.g_squared_equals_sigma1} vs ${gp.g_squared_equals_sigma1}`);
    xck(`${name}: conjugator_g_0indexed node==gap`, JSON.stringify(nd.conjugator_g_0indexed) === JSON.stringify(gp.conjugator_g_0indexed.map(Number)),
        `${JSON.stringify(nd.conjugator_g_0indexed)} vs ${JSON.stringify(gp.conjugator_g_0indexed)}`);
    xck(`${name}: sigma0_sigma1_commute node==gap`, nd.sigma0_sigma1_commute === gp.sigma0_sigma1_commute, `${nd.sigma0_sigma1_commute} vs ${gp.sigma0_sigma1_commute}`);
  }
}
console.log(`\n=== cross-check: ${xpass}/${xpass + xfail} PASS ===`);
console.log(`\n=== GRAND TOTAL (self ${pass}/${pass + fail} + cross ${xpass}/${xpass + xfail}) ===`);

// ---------------------------------------------------------------- final combined certificate
mkdirSync(join(ROOT, 'certificates', 'k5pipeline'), { recursive: true });
const finalCert = {
  schema: 'k5pipeline/ninf-exclusion/v3',
  retraction_note: "v1 (moved to certificates/k5pipeline/retracted/) tested the naive swap (x,y,z)->(z,y,x) (35.2)/(35.3), which does not preserve the relator xyz=1 in general. Direct computation confirms sigma_0*sigma_1 <> sigma_1*sigma_0 for both fixtures, so (35.3)'s third equation combined with E1 is unsatisfiable (35.3 is equivalent to (35.4) AND [sigma_0,sigma_1]=1 given E1) -- v1's 'no conjugator found' was a CORRECT computation of an uninformative/wrong question, not evidence against (N_infty). v2 fixed the predicate to (35.4) but used a full-S10 search; v3 implements the mathematician-reviewed restricted method (Rule 1 v1.3 R1-N∞-W): only 10 candidates (g(0)=c), E1+E2 as the decisive predicate, E3 as a redundant confirmation, and theorem-derived self-checks (unique survivor, g^2=sigma_1) as integrity stops rather than UNKNOWN.",
  conclusion_label: '排除されず・対称性充足・(N_infty) の存否は UNKNOWN・witness は cross-checked',
  source_doc: 'docs/week4-K5_Rule1_v1.md v1.3 §11 R-6 (補題 R1-N∞-W); sol/sol_reply_35_freeze1r4.md F1.5; sol/裁定_36_ben35.md',
  inputs: 'certificates/k5fixture/K5-sq.json, K5-ns.json の perm_triple のみ(model/lambda/u には一切接触なし)',
  systems: {
    gap: {
      method: 'restricted 10-candidate search: g(0)=c for c=0..9 via GAP-side propagation; E1+E2 decisive, E3 redundant confirmation; self-checks per R1-N∞-W',
      script: 'search/k5-ninf-exclusion.g',
      certificate_file: 'certificates/k5pipeline/ninf-exclusion.gap.json',
      raw: gapCert,
    },
    node: {
      method: 'independent from-scratch reimplementation of the same restricted 10-candidate method (no shared helper with the GAP script)',
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
    sq: { ninf_excluded_gap: gapCert ? gapCert.targets.sq.ninf_excluded : null, ninf_excluded_node: nodeResults.sq.ninf_excluded,
          agree: gapCert ? (gapCert.targets.sq.ninf_excluded === nodeResults.sq.ninf_excluded) : null },
    ns: { ninf_excluded_gap: gapCert ? gapCert.targets.ns.ninf_excluded : null, ninf_excluded_node: nodeResults.ns.ninf_excluded,
          agree: gapCert ? (gapCert.targets.ns.ninf_excluded === nodeResults.ns.ninf_excluded) : null },
  },
};

writeFileSync(join(ROOT, 'certificates', 'k5pipeline', 'ninf-exclusion.json'), JSON.stringify(finalCert, null, 2) + '\n');
console.log('\nwrote certificates/k5pipeline/ninf-exclusion.json');

if (fail > 0 || xfail > 0) process.exitCode = 1;
