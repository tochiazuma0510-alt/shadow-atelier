#!/usr/bin/env node
// crosscheck/check-k5e.mjs -- 【GAP-K5e】負較正の独立照合器 (node, 標準ライブラリのみ)
//
// 独立性の規律 (CLAUDE.md): search/k5e-negcal.g のコード・中間結果は一切 import しない。
// 入力は (1) search/k5e-negcal.g が書き出した certificates/k5e/K24.v1.json (+ summary.v1.json)
//        (2) 既存 C-4 証明書 certificates/K4.v1.json, K8.v1.json, K12.v1.json, K16.v1.json
// のみ。D_n/G_n の構成・積・hexagon/charming/surjective 判定はすべて本ファイルで自前導出する
// (docs/week4-K5橋_D1_opus_v1.md の定義そのものから; GAP スクリプトの実装は読んでいない)。
//
// 対象: n in {4,8,12,16,24} (事前登録どおり)
// 判定対象: (A) 位数式(4.1)  (B) gcd(e,M/e)>1 <=> 8|n  (C) 命題K5-2b(盲点定理)

'use strict';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const CERT_DIR = join(ROOT, 'certificates');
const K5E_DIR = join(CERT_DIR, 'k5e');

function mod(a, n) { return ((a % n) + n) % n; }
function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; }
function lcm(a, b) { return Math.abs(a * b) / gcd(a, b); }
function phiEuler(n) { let c = 0; for (let a = 1; a <= n; a++) if (gcd(a, n) === 1) c++; return c; }

// ---------- D_n: 自前導出 (r,s), 元 = [a,e] = r^a s^e, 積 (a,e)(b,f) = (a + (-1)^e b, e+f) mod (n,2) ----------
function makeDn(n) {
  const id = { a: 0, e: 0 };
  const mul = (g, h) => ({ a: mod(g.a + (g.e === 0 ? 1 : -1) * h.a, n), e: (g.e + h.e) % 2 });
  const inv = (g) => (g.e === 0 ? { a: mod(-g.a, n), e: 0 } : { a: mod(g.a, n), e: 1 });
  const key = (g) => `${mod(g.a, n)},${g.e}`;
  const eq = (g, h) => key(g) === key(h);
  const pow = (g, k) => {
    if (k === 0) return id;
    let base = k < 0 ? inv(g) : g, exponent = Math.abs(k), res = id;
    while (exponent > 0) { if (exponent % 2 === 1) res = mul(res, base); base = mul(base, base); exponent = Math.floor(exponent / 2); }
    return res;
  };
  return { n, id, mul, inv, key, eq, pow };
}

function makeProduct3(D) {
  const id = [D.id, D.id, D.id];
  const mul = (x, y) => [D.mul(x[0], y[0]), D.mul(x[1], y[1]), D.mul(x[2], y[2])];
  const inv = (x) => [D.inv(x[0]), D.inv(x[1]), D.inv(x[2])];
  const key = (x) => `${D.key(x[0])}|${D.key(x[1])}|${D.key(x[2])}`;
  const eq = (x, y) => key(x) === key(y);
  const pow = (x, k) => [D.pow(x[0], k), D.pow(x[1], k), D.pow(x[2], k)];
  return { id, mul, inv, key, eq, pow };
}

function subgroupClosure(G, gens) {
  const genList = [];
  for (const g of gens) { genList.push(g); genList.push(G.inv(g)); }
  const seen = new Map();
  seen.set(G.key(G.id), G.id);
  const frontier = [G.id];
  while (frontier.length) {
    const elem = frontier.pop();
    for (const g of genList) {
      const cand = G.mul(elem, g);
      const k = G.key(cand);
      if (!seen.has(k)) { seen.set(k, cand); frontier.push(cand); }
    }
  }
  return seen;
}

function bfsWords(G, gens) {
  // gens: [{sym:['x',1], elt}, ...]
  const wordOf = new Map();
  wordOf.set(G.key(G.id), []);
  const elements = [G.id];
  let qi = 0;
  while (qi < elements.length) {
    const cur = elements[qi]; qi++;
    const curWord = wordOf.get(G.key(cur));
    for (const g of gens) {
      const nv = G.mul(cur, g.elt); // right mult -- word reconstruction via naive 左から右 evaluation
      const k = G.key(nv);
      if (!wordOf.has(k)) { wordOf.set(k, curWord.concat([g.sym])); elements.push(nv); }
    }
  }
  return { wordOf, elements };
}

function commutator(G, g, h) { return G.mul(G.mul(G.inv(g), G.inv(h)), G.mul(g, h)); }

function derivedSubgroupOfTwoGen(G, GnMap, X, Y) {
  const c0 = commutator(G, X, Y);
  const conjugates = [];
  for (const g of GnMap.values()) conjugates.push(G.mul(G.mul(g, c0), G.inv(g)));
  return subgroupClosure(G, conjugates);
}

function buildGn(n) {
  const Dn = makeDn(n);
  const r = { a: 1, e: 0 }, s = { a: 0, e: 1 };
  const rs = Dn.mul(r, s);
  const Triple = makeProduct3(Dn);
  const X = [r, s, s];
  const Y = [rs, r, rs];
  const GnMap = subgroupClosure(Triple, [X, Y]);
  const derived = derivedSubgroupOfTwoGen(Triple, GnMap, X, Y);
  return { Dn, Triple, X, Y, GnMap, derived, r, s };
}

function expectedGnOrder(n) { return (n % 2 === 1) ? 4 * n ** 3 : 4 * (n / 2) ** 3; }

function thm46Order(n) {
  let odd = n, alpha = 0;
  while (odd % 2 === 0) { odd /= 2; alpha++; }
  if (alpha < 2) return 2 * odd * phiEuler(odd);
  return odd * phiEuler(odd) * 2 ** (2 * alpha - 2);
}

// abstract product "f1 f2 ... fk" (paper 記法, 左から順) -> Triple 演算。
// week1-定義ノート/D1 の hexagon (3.10)(3.11) 等で使われる抽象積は「最後の語から順に右へ掛ける」
// 反転規約になる (自前導出: G_n の元としての作用が右から左へ合成される定義に整合させるため、
// val := list[last]; val := val*list[last-1]; ... ; val := val*list[first] という順で畳み込む)。
function abstractProd(Triple, list) {
  let val = Triple.id;
  for (let i = list.length - 1; i >= 0; i--) val = Triple.mul(val, list[i]);
  return val;
}

function evalWord(Triple, phi, tokens) {
  let res = Triple.id;
  for (const [gen, p] of tokens) res = Triple.mul(res, Triple.pow(phi[gen], p));
  return res;
}

function kappa(m) { return (m % 2 === 1) ? m + 1 : -m; }

// ---------- hexagon (3.3)(3.4) 相当 + charming + surjective: 独立な GT(K^(n)) 探索 ----------
function processDihedral(n) {
  const Gn = buildGn(n);
  const { Triple, X, Y, GnMap, derived } = Gn;
  const ordX = groupElementOrder(Triple, X), ordY = groupElementOrder(Triple, Y);
  const Nord = lcm(ordX, ordY);
  const zTok = Triple.inv(abstractProd(Triple, [X, Y])); // z = (xy)^-1, paper 積 (反転規約)
  const gens = [{ sym: ['x', 1], elt: X }, { sym: ['x', -1], elt: Triple.inv(X) },
                { sym: ['y', 1], elt: Y }, { sym: ['y', -1], elt: Triple.inv(Y) }];
  const bfs = bfsWords(Triple, gens);
  if (bfs.elements.length !== GnMap.size) throw new Error(`BFS did not cover G_${n}: ${bfs.elements.length} vs ${GnMap.size}`);

  // theta: x->y, y->x ; tau: x->y, y->z  (Ehom via generator substitution on words)
  function applyHom(elt, images) {
    const word = bfs.wordOf.get(Triple.key(elt));
    let res = Triple.id;
    for (const [gen, p] of word) res = Triple.mul(res, Triple.pow(images[gen], p));
    return res;
  }
  const thetaImages = { x: Y, y: X };
  const tauImages = { x: Y, y: zTok };

  const Dwords = [];
  for (const elt of bfs.elements) if (derived.has(Triple.key(elt))) Dwords.push({ elt, word: bfs.wordOf.get(Triple.key(elt)) });

  const Xn = [];
  for (let m = 0; m < Nord; m++) if (gcd(2 * m + 1, Nord) === 1) Xn.push(m);

  let rawCount = 0, hexPass = 0, surjPass = 0;
  const shadows = [];
  for (const cand of Dwords) {
    const f = cand.elt;
    for (const m of Xn) {
      rawCount++;
      const u = 2 * m + 1;
      const thetaf = applyHom(f, thetaImages);
      const hex310 = Triple.eq(abstractProd(Triple, [f, thetaf]), Triple.id);
      const ymf = abstractProd(Triple, [Triple.pow(Y, m), f]);
      const tauymf = applyHom(ymf, tauImages);
      const tau2ymf = applyHom(tauymf, tauImages);
      const hex311 = Triple.eq(abstractProd(Triple, [tau2ymf, tauymf, ymf]), Triple.id);
      if (hex310 && hex311) {
        hexPass++;
        const genA = Triple.pow(X, u);
        const genB = abstractProd(Triple, [Triple.inv(f), Triple.pow(Y, u), f]);
        const genGroup = subgroupClosure(Triple, [genA, genB]);
        if (genGroup.size === GnMap.size) {
          surjPass++;
          shadows.push({ m, f, word: cand.word });
        }
      }
    }
  }
  return { Gn, Nord, shadows, Xn, rawCount, hexPass, surjPass };
}

function groupElementOrder(G, g) {
  let cur = g, k = 1;
  while (!G.eq(cur, G.id)) { cur = G.mul(cur, g); k++; if (k > 100000) throw new Error('order search runaway'); }
  return k;
}

// ---------- (C) K5-2b: X^{-2k0} 中心性 + Phi_{0,k0}=id ----------
function checkK52b(n) {
  const Gn = buildGn(n);
  const { Triple, X, Y } = Gn;
  const k0 = n / 4;
  const z = Triple.pow(X, -2 * k0);
  const zOrder = groupElementOrder(Triple, z);
  const central = Triple.eq(Triple.mul(z, X), Triple.mul(X, z)) && Triple.eq(Triple.mul(z, Y), Triple.mul(Y, z));
  const zinv = Triple.inv(z);
  const phiXtrivial = Triple.eq(Triple.mul(Triple.mul(zinv, X), z), X);
  const phiYtrivial = Triple.eq(Triple.mul(Triple.mul(zinv, Y), z), Y);
  return { n, k0, zOrder, central, phiTrivial: phiXtrivial && phiYtrivial };
}

function checkFaithfulF0(n) {
  const Gn = buildGn(n);
  const { Triple, X, Y } = Gn;
  const half = n / 2;
  const kset = []; for (let k = 0; k < half; k++) if (k % 2 === 0) kset.push(k);
  const trivialKs = [];
  for (const k of kset) {
    const z = Triple.pow(X, -2 * k);
    const zinv = Triple.inv(z);
    const phiXtrivial = Triple.eq(Triple.mul(Triple.mul(zinv, X), z), X);
    const phiYtrivial = Triple.eq(Triple.mul(Triple.mul(zinv, Y), z), Y);
    if (phiXtrivial && phiYtrivial) trivialKs.push(k);
  }
  return { n, kset, trivialKs, faithful: trivialKs.length === 1 && trivialKs[0] === 0 };
}

// ==================== メイン ====================
const universe = [4, 8, 12, 16, 24];
let allOk = true;
const log = [];
function P(ok) { if (!ok) allOk = false; return ok ? 'PASS' : 'FAIL'; }

console.log('========================================================');
console.log('【crosscheck-K5e】独立照合 (node, search/k5e-negcal.g とヘルパー非共有)');
console.log('========================================================\n');

console.log('---- Step 1: |G_n| 突合(C-1) ----');
for (const n of universe) {
  const t0 = Date.now();
  const Gn = buildGn(n);
  const ok = Gn.GnMap.size === expectedGnOrder(n);
  console.log(`[${P(ok)}] n=${n}  |G_n|=${Gn.GnMap.size}  expected(C-1)=${expectedGnOrder(n)}  time_ms=${Date.now() - t0}`);
}
console.log('');

console.log('---- Step 2: GT(K^(n)) shadow enumeration (二系統の node 側) ----');
const resTable = [];
const procResults = {};
for (const n of universe) {
  const t0 = Date.now();
  const r = processDihedral(n);
  procResults[n] = r;
  const m0count = r.shadows.filter((s) => s.m === 0).length;
  const e = m0count, M = r.Nord, MoverE = M / e, g = gcd(e, MoverE);
  const expect = thm46Order(n);
  const orderOk = r.shadows.length === expect;
  resTable.push({ n, M, e, MoverE, gcdEM: g, numShadows: r.shadows.length, expect, orderOk });
  console.log(`[${P(orderOk)}] n=${n}  |GT(K^(n))|=${r.shadows.length}  Thm4.6 expect=${expect}  M=${M} e=${e} M/e=${MoverE} gcd(e,M/e)=${g}  8|n=${n % 8 === 0}  time_ms=${Date.now() - t0}`);
}
console.log('');

console.log('---- 表: (A)(B) 判定 ----');
console.log('n | M | e | M/e | gcd(e,M/e) | 8|n | repeated-primary(gcd>1) | 一致');
for (const row of resTable) {
  const match = (row.gcdEM > 1) === (row.n % 8 === 0);
  console.log(`${row.n} | ${row.M} | ${row.e} | ${row.MoverE} | ${row.gcdEM} | ${row.n % 8 === 0} | ${row.gcdEM > 1} | ${P(match)}`);
}
console.log('');

console.log('---- Step 3: 命題 K5-2b 直接確認 ----');
for (const n of [8, 16]) {
  const res = checkK52b(n);
  const ok = res.central && res.phiTrivial && res.zOrder === 2;
  console.log(`[${P(ok)}] n=${n}  k0=n/4=${res.k0}  ord(X^{-2k0})=${res.zOrder}  X^{-2k0} central=${res.central}  Phi_{0,k0}=id=${res.phiTrivial}`);
}
console.log('');

console.log('---- 対照: n=12 (8∤12) -- 期待 ker(Phi|F0)=1 ----');
{
  const resF0 = checkFaithfulF0(12);
  console.log(`[${P(resF0.faithful)}] n=12  F0 index set k in [${resF0.kset.join(',')}]  {k:Phi_{0,k}=id} = [${resF0.trivialKs.join(',')}] (期待 [0] のみ)`);
}
console.log('');

// ---- Step 4: n=4,8,12,16 を既存 C-4 証明書と突合 ----
console.log('---- Step 4: n=4,8,12,16 の既存 C-4 証明書 (certificates/K{n}.v1.json) との突合 ----');
for (const n of [4, 8, 12, 16]) {
  const certPath = join(CERT_DIR, `K${n}.v1.json`);
  const cert = JSON.parse(readFileSync(certPath, 'utf8'));
  const inv = cert.target.invariants;
  const r = procResults[n];
  const Gn = buildGn(n);
  const orderMatch = inv.index_PB3 === Gn.GnMap.size;
  const derivedMatch = inv.derived_order === Gn.derived.size;
  const nordMatch = inv.N_ord === r.Nord;
  const shadowCountMatch = cert.shadows.length === r.shadows.length;
  const thm46Match = cert.counts.thm46_expected_order === thm46Order(n);
  const m0certCount = cert.shadows.filter((s) => s.m === 0).length;
  const m0nodeCount = r.shadows.filter((s) => s.m === 0).length;
  const eMatch = m0certCount === m0nodeCount;
  const ok = orderMatch && derivedMatch && nordMatch && shadowCountMatch && thm46Match && eMatch;
  console.log(`[${P(ok)}] K${n}.v1.json: index_PB3(${inv.index_PB3})=|G_n|(node,${Gn.GnMap.size}):${orderMatch}  derived_order(${inv.derived_order})=(node,${Gn.derived.size}):${derivedMatch}  N_ord match:${nordMatch}  |shadows| cert=${cert.shadows.length} node=${r.shadows.length}:${shadowCountMatch}  thm46 match:${thm46Match}  e(m0count) cert=${m0certCount} node=${m0nodeCount}:${eMatch}`);
}
console.log('');

// ---- Step 5: n=24 新証明書 (certificates/k5e/K24.v1.json, GAP 生成) との突合 ----
console.log('---- Step 5: n=24 (GAP 生成 certificates/k5e/K24.v1.json) との突合 ----');
{
  const certPath = join(K5E_DIR, 'K24.v1.json');
  const cert = JSON.parse(readFileSync(certPath, 'utf8'));
  const inv = cert.target.invariants;
  const r = procResults[24];
  const Gn = buildGn(24);
  const orderMatch = inv.index_PB3 === Gn.GnMap.size && Gn.GnMap.size === expectedGnOrder(24);
  const derivedMatch = inv.derived_order === Gn.derived.size;
  const nordMatch = inv.N_ord === r.Nord;
  const shadowCountMatch = cert.shadows.length === r.shadows.length;
  const thm46Match = cert.counts.thm46_expected_order === thm46Order(24);
  const m0certCount = cert.shadows.filter((s) => s.m === 0).length;
  const m0nodeCount = r.shadows.filter((s) => s.m === 0).length;
  const eMatch = m0certCount === m0nodeCount;

  // 各 shadow の f_word を node 側の D_n 演算で再評価し、cert の f_triple (r^a s^e 表記) と突合する
  const Dn = makeDn(24);
  const r24 = { a: 1, e: 0 }, s24 = { a: 0, e: 1 };
  const phi = { x: s24, y: Dn.mul(r24, s24) };
  let wordMismatch = 0;
  for (const sh of cert.shadows) {
    const computed = evalWordDn(Dn, phi, sh.f_word); // [D,D,D] as (a,e) triples reconstructed component-wise
    for (let i = 0; i < 3; i++) {
      const [a, e] = sh.f_triple[i];
      if (!(computed[i].a === a && computed[i].e === e)) wordMismatch++;
    }
  }
  const wordsOk = wordMismatch === 0;

  const ok = orderMatch && derivedMatch && nordMatch && shadowCountMatch && thm46Match && eMatch && wordsOk;
  console.log(`[${P(ok)}] K24.v1.json: |G_24| cert=${inv.index_PB3} node=${Gn.GnMap.size} expected(C-1)=${expectedGnOrder(24)}:${orderMatch}`);
  console.log(`       derived_order cert=${inv.derived_order} node=${Gn.derived.size}:${derivedMatch}  N_ord match:${nordMatch}`);
  console.log(`       |shadows| cert=${cert.shadows.length} node=${r.shadows.length}:${shadowCountMatch}  thm46 expect match:${thm46Match}`);
  console.log(`       e(m0count) cert=${m0certCount} node=${m0nodeCount}:${eMatch}  f_word re-evaluation mismatches=${wordMismatch}:${wordsOk}`);
}
console.log('');

console.log(`========================================================`);
console.log(`総合判定: ${P(allOk)}`);
console.log(`========================================================`);

function evalWordDn(Dn, phi, wordTokens) {
  // wordTokens: [["x",1],["y",-1],...] -- Triple の3成分それぞれに x->(r,s,s), y->(rs,r,rs) を適用
  const xTriple = [{ a: 1, e: 0 }, { a: 0, e: 1 }, { a: 0, e: 1 }]; // r,s,s
  const yTriple = [Dn.mul({ a: 1, e: 0 }, { a: 0, e: 1 }), { a: 1, e: 0 }, Dn.mul({ a: 1, e: 0 }, { a: 0, e: 1 })]; // rs,r,rs
  let res = [Dn.id, Dn.id, Dn.id];
  for (const [gen, p] of wordTokens) {
    const base = gen === 'x' ? xTriple : yTriple;
    for (let i = 0; i < 3; i++) res[i] = Dn.mul(res[i], Dn.pow(base[i], p));
  }
  return res;
}

process.exit(allOk ? 0 : 1);
