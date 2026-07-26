#!/usr/bin/env node
// crosscheck/check-k5-blocks.mjs -- S5-1/S5-2/S5-3 の独立照合器 (node, 第二系統)
//
// 独立性の規律 (CLAUDE.md): search/k5-blocks-check.g のコード・中間結果は
// 一切 import しない。ブロック探索・部分群列挙・D5 判定はすべて本ファイルで
// 自前実装する(GAP の AllBlocks / ConjugacyClassesSubgroups / RestrictedPerm
// の実装は読んでいない)。
//
// 入力: (1) certificates/k5fixture/K5-sq.json, K5-ns.json の perm_triple
//          フィールドのみ(= 凍結済み有限 fixture の生データ)。
//       (2) 比較対象として certificates/k5blocks/k5-blocks-check.gap.json
//          (GAP 側が書き出した証明書 — 「一致」は cross-checked の意味で
//          あって verified ではない)。GAP の .g ソースは読まない。
//
// 接触禁止: 曲線・λ・u・数値近似・database には一切触れない。
//
// 対象命題(docs/week4-K5_S5設計_opus_v1.md §2.4):
//  S5-1: 10 点作用(K5-sq/K5-ns)の非自明ブロック系はちょうど一つ、
//        2 ブロック x サイズ 5。
//  S5-2: そのブロック(5 点)上で sigma_0^2, sigma_1, sigma_infty^2 が生成する
//        群は位数 10・非可換(⇒ 群論の分類により D_5)。型は (5, 2.2.1, 5)。
//  S5-3: Mon = <sigma_0,sigma_1>(位数 100)内で、点 0 の安定化群 Hbar
//        (位数 10)を含む中間部分群は |K|=20 が 0 個・|K|=50 がちょうど 1 個。
//
// 実行: node crosscheck/check-k5-blocks.mjs

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

// ---------------------------------------------------------------- fixture
// certificates/k5fixture/{K5-sq,K5-ns}.json の perm_triple フィールドを
// 生データとして読む(H_generators や passport 等の他フィールドは見ない —
// 本照合はブロック構造のみを対象とする)。
function loadFixture(name) {
  const j = JSON.parse(readFileSync(join(ROOT, 'certificates', 'k5fixture', `${name}.json`), 'utf8'));
  const pt = j.perm_triple;
  return { s0: pt.sigma_0.slice(), s1: pt.sigma_1.slice(), sInf: pt.sigma_infty.slice() };
}

// ---------------------------------------------------------------- permutations
// 規約: perm は長さ 10 の配列、perm[i] = 点 i (0-indexed) の像。
// 合成規約(fixture の "convention" フィールドと同一): (p o q)(i) = p(q(i))。
const N = 10;
const identity10 = [...Array(N).keys()];
const applyPerm = (p, i) => p[i];
const composeApply = (p, q, i) => applyPerm(p, applyPerm(q, i)); // (p o q)(i)
const eqPerm = (p, q) => p.length === q.length && p.every((v, i) => v === q[i]);
const isIdentity = (p) => eqPerm(p, identity10.slice(0, p.length));
const permKey = (p) => p.join(',');

function composeArr(p, q, n) {
  // returns permutation r with r[i] = p(q(i)), domain size n
  const r = new Array(n);
  for (let i = 0; i < n; i++) r[i] = p[q[i]];
  return r;
}
function invPerm(p) {
  const inv = new Array(p.length);
  for (let i = 0; i < p.length; i++) inv[p[i]] = i;
  return inv;
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

// ---------------------------------------------------------------- group closure (BFS, S_10-valued)
// 生成元集合から生成される群を BFS で全列挙する(位数は事前に既知の 100 程度で軽量)。
function closureGroup(gens, n) {
  const id = [...Array(n).keys()];
  const seen = new Map([[permKey(id), id]]);
  const queue = [id];
  while (queue.length) {
    const g = queue.shift();
    for (const h of gens) {
      const p = composeArr(g, h, n); // g then h : (h o g)? -- see note below
      const k = permKey(p);
      if (!seen.has(k)) { seen.set(k, p); queue.push(p); }
      const p2 = composeArr(h, g, n);
      const k2 = permKey(p2);
      if (!seen.has(k2)) { seen.set(k2, p2); queue.push(p2); }
    }
  }
  return [...seen.values()];
}

// ---------------------------------------------------------------- main per-target processing
function processTarget(label, fx) {
  console.log(`\n==== target: ${label} ====`);
  const { s0, s1, sInf } = fx;

  // S0: sigma_0 sigma_1 sigma_infty = id under (p o q)(i) = p(q(i)):
  // apply sigma_infty first, then sigma_1, then sigma_0: h(i) = s0(s1(sInf(i))).
  const h = identity10.map(i => s0[s1[sInf[i]]]);
  ck(`${label}-S0 sigma_0 sigma_1 sigma_infty = id (composition conv.)`, isIdentity(h), '');

  // Mon = <s0, s1>, brute BFS closure
  const Mon = closureGroup([s0, s1], N);
  ck(`${label}-S0b |Mon| = |<sigma_0,sigma_1>| = 100`, Mon.length === 100, `got ${Mon.length}`);

  // ------------------------------------------------ S5-1: block systems by brute force
  // Any block of a nontrivial block system for a transitive group on 10 points
  // has size dividing 10, size in {2,5} (excluding 1 and 10). Enumerate ALL
  // partitions of that shape and test G-invariance directly (no reliance on
  // any block-finding library routine).
  const isInvariantPartition = (blocks) => {
    // blocks: array of arrays (each sorted), partition of 0..9
    const blockOf = new Array(N);
    blocks.forEach((B, bi) => B.forEach(x => { blockOf[x] = bi; }));
    for (const g of Mon) {
      // for each block, g must map it entirely into a single block
      for (const B of blocks) {
        const target = blockOf[g[B[0]]];
        for (const x of B) if (blockOf[g[x]] !== target) return false;
      }
    }
    return true;
  };

  const combinations = (arr, k) => {
    const res = [];
    const rec = (start, chosen) => {
      if (chosen.length === k) { res.push(chosen.slice()); return; }
      for (let i = start; i < arr.length; i++) { chosen.push(arr[i]); rec(i + 1, chosen); chosen.pop(); }
    };
    rec(0, []);
    return res;
  };

  // size-5 block systems: block containing point 0, choose remaining 4 of {1..9}
  const rest = [1, 2, 3, 4, 5, 6, 7, 8, 9];
  const size5Systems = [];
  for (const combo of combinations(rest, 4)) {
    const B0 = [0, ...combo].sort((a, b) => a - b);
    const B1 = rest.filter(x => !combo.includes(x));
    const partition = [B0, B1];
    if (isInvariantPartition(partition)) size5Systems.push(partition);
  }

  // size-2 block systems: all perfect matchings of 0..9 into 5 pairs
  const size2Systems = [];
  const points = identity10.slice();
  const findMatchings = (remaining, current, out) => {
    if (remaining.length === 0) { out.push(current.map(p => p.slice())); return; }
    const a = remaining[0];
    const rest2 = remaining.slice(1);
    for (let i = 0; i < rest2.length; i++) {
      const b = rest2[i];
      const nextRemaining = rest2.slice(0, i).concat(rest2.slice(i + 1));
      current.push([a, b]);
      findMatchings(nextRemaining, current, out);
      current.pop();
    }
  };
  const allMatchings = [];
  findMatchings(points, [], allMatchings);
  for (const m of allMatchings) {
    if (isInvariantPartition(m)) size2Systems.push(m);
  }

  const totalNontrivialSystems = size5Systems.length + size2Systems.length;
  ck(`${label}-S5.1a exactly one nontrivial block system`, totalNontrivialSystems === 1,
     `size5=${size5Systems.length} size2=${size2Systems.length}`);

  let blockSizes = [];
  let B = null;
  if (size5Systems.length === 1 && size2Systems.length === 0) {
    B = size5Systems[0][0].includes(0) ? size5Systems[0][0] : size5Systems[0][1];
    blockSizes = size5Systems[0].map(x => x.length).sort((a, b) => a - b);
  }
  ck(`${label}-S5.1b block size = 5`, B !== null && B.length === 5, B ? `|B|=${B.length}` : 'no unique block found');
  ck(`${label}-S5.1c full block system = 2 blocks x size 5 (partition of 10 pts)`,
     blockSizes.length === 2 && blockSizes[0] === 5 && blockSizes[1] === 5, `blocks=${JSON.stringify(blockSizes)}`);

  // swap/preserve check on the 2-block quotient
  if (B) {
    const other = identity10.filter(x => !B.includes(x));
    const blockOf = new Array(N);
    B.forEach(x => { blockOf[x] = 0; });
    other.forEach(x => { blockOf[x] = 1; });
    const swaps = (g) => blockOf[g[B[0]]] !== blockOf[B[0]];
    ck(`${label}-S5.1d sigma_0 swaps the 2 blocks`, swaps(s0), '');
    ck(`${label}-S5.1e sigma_1 preserves the 2 blocks (fixes both)`, !swaps(s1), '');
    ck(`${label}-S5.1f sigma_infty swaps the 2 blocks`, swaps(sInf), '');
  }

  // ------------------------------------------------ S5-2: D5 on the block
  let d5order = 0, isD5 = false, types = [[], [], []];
  if (B) {
    const Bsorted = B.slice().sort((a, b) => a - b);
    const s0sq = composeArr(s0, s0, N);
    const sInfsq = composeArr(sInf, sInf, N);
    const preserves = (g) => Bsorted.every(x => Bsorted.includes(g[x]));
    const precondOk = preserves(s0sq) && preserves(s1) && preserves(sInfsq);
    ck(`${label}-S5.2 (precondition) sigma_0^2, sigma_1, sigma_infty^2 preserve B`, precondOk, '');
    if (precondOk) {
      types = [cycleType(s0sq, Bsorted), cycleType(s1, Bsorted), cycleType(sInfsq, Bsorted)];
      ck(`${label}-S5.2a cycle type sigma_0^2|B = (5)`, JSON.stringify(types[0]) === '[5]', `got ${JSON.stringify(types[0])}`);
      ck(`${label}-S5.2b cycle type sigma_1|B = (2,2,1)`, JSON.stringify(types[1]) === '[2,2,1]', `got ${JSON.stringify(types[1])}`);
      ck(`${label}-S5.2c cycle type sigma_infty^2|B = (5)`, JSON.stringify(types[2]) === '[5]', `got ${JSON.stringify(types[2])}`);

      // relabel block points to 0..4 in sorted order to build a genuine S_5 rep
      const pos = new Map(Bsorted.map((v, i) => [v, i]));
      const relabel = (g) => Bsorted.map(x => pos.get(g[x]));
      const gens5 = [relabel(s0sq), relabel(s1), relabel(sInfsq)];
      const D = closureGroup(gens5, 5);
      d5order = D.length;
      ck(`${label}-S5.2d |<sigma_0^2,sigma_1,sigma_infty^2>| on B = 10`, d5order === 10, `got ${d5order}`);
      // classification of order-10 groups: only C10 (abelian) or D5 (non-abelian).
      // check non-abelian via some pair of generators not commuting.
      const nonAbelian = gens5.some((a) => gens5.some((b) => {
        const ab = composeArr(a, b, 5), ba = composeArr(b, a, 5);
        return !eqPerm(ab, ba);
      }));
      isD5 = d5order === 10 && nonAbelian;
      ck(`${label}-S5.2e monodromy on B is isomorphic to D_5 (order 10, non-abelian ⇒ D_5 by classification)`, isD5, '');
    }
  }

  // ------------------------------------------------ S5-3: intermediate subgroups
  // Hbar := Stab_Mon(0). Enumerate K with Hbar <= K <= Mon by closure(Hbar U {g})
  // for all g in Mon, dedupe, filter by size.
  const stabilizerOf = (group, pt) => group.filter(g => g[pt] === pt);
  const Hbar = stabilizerOf(Mon, 0);
  ck(`${label}-S5.3a |Hbar| = |Stab_Mon(0)| = 10`, Hbar.length === 10, `got ${Hbar.length}`);

  const setKey = (elts) => elts.map(permKey).sort().join('|');
  const overgroupsMap = new Map();
  for (const g of Mon) {
    const K = closureGroup([...Hbar, g], N);
    const key = setKey(K);
    if (!overgroupsMap.has(key)) overgroupsMap.set(key, K);
  }
  const overgroups = [...overgroupsMap.values()];
  const overgroupSizes = overgroups.map(K => K.length).sort((a, b) => a - b);
  const k20 = overgroups.filter(K => K.length === 20);
  const k50 = overgroups.filter(K => K.length === 50);
  const k10 = overgroups.filter(K => K.length === 10);
  const k100 = overgroups.filter(K => K.length === 100);
  ck(`${label}-S5.3b intermediate |K|=20 with Hbar<=K<=Mon: count = 0`, k20.length === 0, `count = ${k20.length}`);
  ck(`${label}-S5.3c intermediate |K|=50 with Hbar<=K<=Mon: count = 1`, k50.length === 1, `count = ${k50.length}`);
  ck(`${label}-S5.3d overgroup lattice sane: includes Hbar(10) and Mon(100) exactly once each`,
     k10.length === 1 && k100.length === 1, `all sizes = ${JSON.stringify(overgroupSizes)}`);

  return {
    target: label,
    monOrder: Mon.length,
    nBlockSystems: totalNontrivialSystems,
    blockSizes,
    overgroupSizes,
    d5order,
    isD5,
  };
}

const nodeResults = {};
for (const name of ['sq', 'ns']) {
  const fx = loadFixture(`K5-${name}`);
  nodeResults[name] = processTarget(name, fx);
}

console.log(`\n=== node self-check: ${pass}/${pass + fail} PASS ===`);

// ---------------------------------------------------------------- cross-check against GAP certificate
// 「探索器と照合器の分離」— ここでは GAP の出力した証明書 JSON だけを入力にする
// (search/k5-blocks-check.g のソースは読まない)。一致は cross-checked であり
// verified (Lean) ではない。
console.log('\n==== cross-check vs GAP certificate (certificates/k5blocks/k5-blocks-check.gap.json) ====');
let gapCert = null;
try {
  gapCert = JSON.parse(readFileSync(join(ROOT, 'certificates', 'k5blocks', 'k5-blocks-check.gap.json'), 'utf8'));
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
    xck(`${name}: monOrder node==gap`, nd.monOrder === gp.monOrder, `${nd.monOrder} vs ${gp.monOrder}`);
    xck(`${name}: nBlockSystems node==gap`, nd.nBlockSystems === gp.nBlockSystems, `${nd.nBlockSystems} vs ${gp.nBlockSystems}`);
    xck(`${name}: blockSizes node==gap`, JSON.stringify(nd.blockSizes) === JSON.stringify(gp.blockSizes),
        `${JSON.stringify(nd.blockSizes)} vs ${JSON.stringify(gp.blockSizes)}`);
    xck(`${name}: overgroupSizes node==gap`, JSON.stringify(nd.overgroupSizes) === JSON.stringify(gp.overgroupSizes),
        `${JSON.stringify(nd.overgroupSizes)} vs ${JSON.stringify(gp.overgroupSizes)}`);
    xck(`${name}: d5order node==gap`, nd.d5order === gp.d5order, `${nd.d5order} vs ${gp.d5order}`);
    xck(`${name}: isD5 node==gap`, nd.isD5 === gp.isD5, `${nd.isD5} vs ${gp.isD5}`);
  }
}

console.log(`\n=== cross-check: ${xpass}/${xpass + xfail} PASS ===`);
console.log(`\n=== GRAND TOTAL (self ${pass}/${pass + fail} + cross ${xpass}/${xpass + xfail}) ===`);

// ---------------------------------------------------------------- node-side certificate
const nodeCert = {
  self_pass: pass,
  self_fail: fail,
  cross_pass: xpass,
  cross_fail: xfail,
  targets: nodeResults,
  gap_cert_read: gapCert !== null,
};
writeFileSync(join(ROOT, 'certificates', 'k5blocks', 'k5-blocks-check.node.json'), JSON.stringify(nodeCert) + '\n');
console.log('\nwrote certificates/k5blocks/k5-blocks-check.node.json');

if (fail > 0 || xfail > 0) process.exitCode = 1;
