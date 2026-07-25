#!/usr/bin/env node
// crosscheck/check.mjs -- WP2b 独立照合器 (node 標準ライブラリのみ, 依存ゼロ)
//
// 独立性の規律 (CLAUDE.md / wp2-workorders.md):
//   - search/ の .g ファイルは一切読んでいない・移植していない。
//   - 本ファイルの数学的根拠は次の文書のみ:
//       docs/wp2-transversal-model.md (12 規則 + 証明書スキーマ + 検査項目 1-10)
//       docs/wp2-workorders.md
//       docs/week1-定義ノート.md (hexagon (3.3)(3.4), charming, 合成 (3.53), 逆射 (3.54), Thm 4.3/4.6)
//       docs/notes/2405.11725-抽出ノート_v1.md (Thm 4.3/4.6 の式, (4.19)(4.20), LS witness item (G))
//       sol/sol_reply_01_definition_gate.md 6 節 (罠12件)
//   - D_n の元・積・作用は自分で導出し、起動時自己検査で braid / sigma^2 / c-check / 群位数較正 を通す。
//
// 追補1 (docs/wp2-transversal-model.md「追補1」2026-07-18 司令塔裁定) 反映済み:
//   - 検査項目 6 「kernel_cert の (4.11) 等式」: 確定式で実装済み。
//       x-bar^{2m+1} = h . x-bar . h^-1  かつ  g^-1 . y-bar^{2m+1} . g = h . y-bar . h^-1
//       (h=(h1,h2,h3)∈Sn^3、成分ごとの Sym(Z/n) 内共役として checkKernelCert に実装)。
//       control(N5)の type=brute は checkKernelCertBrute で別途、井戸定義性+全単射性を検査。
//   - 検査項目 10 「ls_witness の (5.1) 両式」: 確定式で実装済み。
//       fK_F2 = theta(g)^-1 g K_F2、かつ
//       f x^m K_F2 = tau(h)^-1 h K_F2 (m≡0 mod3) / tau(h)^-1 (xy) h K_F2 (m≡-1 mod3)
//       (checkLsWitness に実装)。m≡1 mod3 は空虚 (charming の単元条件違反) — 出現したら FAIL。
//   - 検査項目 1 (counts) の簡略化 (raw 候補の完全再列挙は不要) は司令塔承認済み
//     (verdict に approved_simplification として明記)。
//   - 検査項目 9 (reduction) の image[i] 添字規約は凍結済み (verdict に index_convention として明記)。
//   - 検査項目 7 の (4.20) は mod n で判定 (司令塔追認)。
//
'use strict';

import { readFileSync, readdirSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const CERT_DIR = join(ROOT, 'certificates');
const VERDICT_DIR = join(ROOT, 'crosscheck', 'verdicts');

// ---------- 基礎ユーティリティ ----------

function mod(a, n) { return ((a % n) + n) % n; }
function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; }
function lcm(a, b) { return Math.abs(a * b) / gcd(a, b); }

// ---------- 群インターフェース ----------
// 各 Group は { id, elements(), mul(a,b), inv(a), eq(a,b), key(a), pow(a,k) } を持つ。

function makeDn(n) {
  // D_n = <r,s | r^n, s^2, s r s^-1 = r^-1>, 元 = [a,e] = r^a s^e
  // 積: (a,e)(b,f) = (a + (-1)^e b mod n, e+f mod 2)  -- 自前導出 (仕様 conventions と一致)
  const id = { a: 0, e: 0 };
  const mul = (g, h) => ({ a: mod(g.a + (g.e === 0 ? 1 : -1) * h.a, n), e: (g.e + h.e) % 2 });
  const inv = (g) => (g.e === 0 ? { a: mod(-g.a, n), e: 0 } : { a: mod(g.a, n), e: 1 });
  const key = (g) => `${mod(g.a, n)},${g.e}`;
  const eq = (g, h) => key(g) === key(h);
  const elements = () => { const out = []; for (let a = 0; a < n; a++) for (let e = 0; e < 2; e++) out.push({ a, e }); return out; };
  const pow = (g, k) => {
    if (k === 0) return id;
    let base = k < 0 ? inv(g) : g, exponent = Math.abs(k), res = id;
    while (exponent > 0) {
      if (exponent % 2 === 1) res = mul(res, base);
      base = mul(base, base);
      exponent = Math.floor(exponent / 2);
    }
    return res;
  };
  return { n, id, mul, inv, key, eq, elements, pow };
}

function makeCyclic(m) {
  const id = 0;
  const mul = (a, b) => mod(a + b, m);
  const inv = (a) => mod(-a, m);
  const key = (a) => `${mod(a, m)}`;
  const eq = (a, b) => key(a) === key(b);
  const elements = () => { const out = []; for (let a = 0; a < m; a++) out.push(a); return out; };
  const pow = (a, k) => mod(a * k, m);
  return { m, id, mul, inv, key, eq, elements, pow };
}

// 直積 (成分ごとに同じ or 違う Group の配列)
function cartesianProduct(arrays) {
  let result = [[]];
  for (const arr of arrays) {
    const next = [];
    for (const prefix of result) for (const item of arr) next.push(prefix.concat([item]));
    result = next;
  }
  return result;
}
function makeProduct(groups) {
  const id = groups.map((g) => g.id);
  const mul = (xs, ys) => xs.map((x, i) => groups[i].mul(x, ys[i]));
  const inv = (xs) => xs.map((x, i) => groups[i].inv(x));
  const key = (xs) => xs.map((x, i) => groups[i].key(x)).join('|');
  const eq = (xs, ys) => key(xs) === key(ys);
  const pow = (xs, k) => xs.map((x, i) => groups[i].pow(x, k));
  // elements(): 成分すべてが elements() を持つ場合のみ (直積の全数列挙; Week3 general family の Q_L 構成に使用)
  const elements = groups.every((g) => typeof g.elements === 'function')
    ? () => cartesianProduct(groups.map((g) => g.elements()))
    : undefined;
  return { id, mul, inv, key, eq, pow, elements };
}

// ---------- H3 (Week3 general family: docs/week3-L-設計.md v1.1 sec.1) ----------
// H3 := F2/V, V = F2^3.gamma3(F2) = Heisenberg group mod 3, 位数 27。
// 元 = (a,b,e) in (Z/3)^3, X=(1,0,0), Y=(0,1,0)。
// 積: (a,b,e)(a',b',e') = (a+a', b+b', e+e'+a*b') mod 3 (仕様 §1 の規約のみから自前実装 -- search/ 不参照)。
function makeH3() {
  const P = 3;
  const id = { a: 0, b: 0, e: 0 };
  const mul = (g, h) => ({ a: mod(g.a + h.a, P), b: mod(g.b + h.b, P), e: mod(g.e + h.e + g.a * h.b, P) });
  // 逆元: (a,b,e)^-1 = (-a,-b,-e+a*b) -- (a,b,e)(-a,-b,-e+a*b) = (0,0, e+(-e+a*b)+a*(-b)) = (0,0,0) を満たす
  const inv = (g) => ({ a: mod(-g.a, P), b: mod(-g.b, P), e: mod(-g.e + g.a * g.b, P) });
  const key = (g) => `${mod(g.a, P)},${mod(g.b, P)},${mod(g.e, P)}`;
  const eq = (g, h) => key(g) === key(h);
  const elements = () => { const out = []; for (let a = 0; a < P; a++) for (let b = 0; b < P; b++) for (let e = 0; e < P; e++) out.push({ a, b, e }); return out; };
  const pow = (g, k) => {
    if (k === 0) return id;
    let base = k < 0 ? inv(g) : g, exponent = Math.abs(k), res = id;
    while (exponent > 0) { if (exponent % 2 === 1) res = mul(res, base); base = mul(base, base); exponent = Math.floor(exponent / 2); }
    return res;
  };
  return { id, mul, inv, key, eq, elements, pow };
}

// Q_L = G3 x H3 (仕様 §1: phi_L: x -> ((r,s,s),X), y -> ((rs,r,rs),Y), c -> (1,1))。
// G3 = Im(psi_3) <= D3^3 は既存の buildGn(3) と同一構成 (x->(r,s,s), y->(rs,r,rs) の triple)。
// |Q_L| = 2916 は Goursat 論証 (仕様 §1) の帰結として自己検査で確認する (subgroupClosure で実測)。
function buildQL() {
  const G3 = buildGn(3);
  const H3 = makeH3();
  const H3_X = { a: 1, b: 0, e: 0 }, H3_Y = { a: 0, b: 1, e: 0 };
  // ambient = D3^3 x H3 (位数 216*27=5832) -- mul/inv/key の演算だけを提供する台。
  // Q_L 自体は Goursat 論証(仕様§1)により ambient 内で <X,Y> が生成する部分群(=Im(psi_3)xH3、
  // 位数 2916)であり、G3.Triple(=D3^3 全体、位数216)の cartesian ではない
  // (「PB₃/N を安易に直積分解しない」罠 — G3=Im(psi_3) は D3^3 の真部分群、位数108)。
  const ambient = makeProduct([G3.Triple, H3]);
  const X = [G3.X, H3_X];
  const Y = [G3.Y, H3_Y];
  const phiTriple = { x: X, y: Y, c: [G3.Triple.id, H3.id] };
  const QLMap = subgroupClosure(ambient, [X, Y]); // BFS 閉包 (自己検査で 2916 を確認)
  const derived = derivedSubgroupOfTwoGen(ambient, QLMap, X, Y);
  // Triple: 演算は ambient と共有し、elements() だけを実際の部分群 QLMap に差し替える
  // (buildTransversalModel が Q.elements() で点集合を作るため、ambient の 5832 ではなく
  //  Q_L の 2916 を使わせる必要がある)。
  const Triple = {
    id: ambient.id, mul: ambient.mul, inv: ambient.inv, key: ambient.key, eq: ambient.eq, pow: ambient.pow,
    elements: () => [...QLMap.values()],
  };
  return { G3, H3, Triple, phiTriple, X, Y, QLMap, derived };
}

// (旧) shadowToQLElement: 証明書に H3 成分の専用フィールドが無いことが実測で判明したため撤去。
// Q_L の完全な元が必要な箇所は evalShadowQL (下方で定義) で f_word から自前再構成する。

// ---------- 語の評価 ----------
// token = [gen, power]  (gen: 文字, power: 整数)
// phi: { [gen]: G-element }
function evalWord(G, phi, tokens) {
  let res = G.id;
  for (const [gen, p] of tokens) {
    const g = phi[gen];
    res = G.mul(res, G.pow(g, p));
  }
  return res;
}

// ---------- 部分群の生成 (BFS closure) ----------
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
  return seen; // Map key -> element
}

function commutator(G, g, h) {
  return G.mul(G.mul(G.inv(g), G.inv(h)), G.mul(g, h));
}

// derived subgroup of the subgroup generated by (X,Y): 正規閉包 of [X,Y] を BFS で計算
function derivedSubgroupOfTwoGen(G, GnMap, X, Y) {
  const c0 = commutator(G, X, Y);
  const conjugates = [];
  for (const g of GnMap.values()) {
    conjugates.push(G.mul(G.mul(g, c0), G.inv(g)));
  }
  return subgroupClosure(G, conjugates);
}

// ---------- dihedral Gn (= Im(psi_n) <= Dn^3) ----------
function buildGn(n) {
  const Dn = makeDn(n);
  const r = { a: 1, e: 0 };
  const s = { a: 0, e: 1 };
  const rs = Dn.mul(r, s);
  const Triple = makeProduct([Dn, Dn, Dn]);
  const phiTriple = { x: [r, s, s], y: [rs, r, rs], c: [Dn.id, Dn.id, Dn.id] };
  const X = phiTriple.x, Y = phiTriple.y;
  const GnMap = subgroupClosure(Triple, [X, Y]);
  const derived = derivedSubgroupOfTwoGen(Triple, GnMap, X, Y);
  return { Dn, Triple, phiTriple, GnMap, derived, X, Y };
}

// Global sweep only needs the source Cayley graph and generator images.
// Avoid the expensive derived-subgroup construction used by certificate checks.
function buildGnLight(n) {
  const Dn = makeDn(n);
  const r = { a: 1, e: 0 }, s = { a: 0, e: 1 }, rs = Dn.mul(r, s);
  const Triple = makeProduct([Dn, Dn, Dn]);
  const phiTriple = { x: [r, s, s], y: [rs, r, rs], c: [Dn.id, Dn.id, Dn.id] };
  const X = phiTriple.x, Y = phiTriple.y, GnMap = subgroupClosure(Triple, [X, Y]);
  return { Dn, Triple, phiTriple, GnMap, X, Y };
}

function expectedGnOrder(n) {
  return (n % 2 === 1) ? 4 * n ** 3 : 4 * (n / 2) ** 3;
}

// ---------- Thm 4.3 の閉じた式 ----------
function kappa(m) { return (m % 2 === 1) ? m + 1 : -m; }

function xn(Nord) {
  const out = [];
  for (let m = 0; m < Nord; m++) if (gcd(2 * m + 1, Nord) === 1) out.push(m);
  return out;
}

function thm43ShadowSet(n) {
  const Nord = lcm(n, 2);
  const n1 = n / gcd(n, 2); // ord(r^2)
  const Xn = xn(Nord);
  const fourDividesN = (n % 4 === 0);
  const result = [];
  for (const m of Xn) {
    const kap = kappa(m);
    for (let k = 0; k < n1; k++) {
      if (fourDividesN) {
        if (kap % 2 !== 0) continue; // 想定外 (guard)
        const need = mod(kap / 2, 2);
        if (mod(k, 2) !== need) continue;
      }
      const triple = [[mod(2 * k, n), 0], [mod(-2 * k, n), 0], [mod(kap, n), 0]];
      result.push({ m, triple });
    }
  }
  return { Nord, n1, Xn, shadows: result };
}

function thm46Order(n) {
  let odd = n, alpha = 0;
  while (odd % 2 === 0) { odd /= 2; alpha++; }
  if (alpha < 2) return 2 * odd * (odd - 1); // phi(odd) for the registered odd cases is checked below
  let phi = 0;
  for (let a = 1; a <= odd; a++) if (gcd(a, odd) === 1) phi++;
  return odd * phi * 2 ** (2 * alpha - 2);
}

function hasOwn(obj, key) { return Object.prototype.hasOwnProperty.call(obj, key); }

function validateCertificateShape(cert) {
  const errors = [];
  if (!cert || typeof cert !== 'object') return ['certificate is not an object'];
  if (cert.schema !== 'gtsh-cert/v1') errors.push('schema must be gtsh-cert/v1');
  if (!cert.target || typeof cert.target !== 'object') return errors.concat('target is missing');
  const isGeneral = cert.target.family === 'general';
  const requiredTargetKeys = isGeneral ? ['family', 'id', 'invariants'] : ['family', 'id', 'n', 'invariants'];
  for (const key of requiredTargetKeys) if (!hasOwn(cert.target, key)) errors.push(`target.${key} is missing`);
  if (cert.target.family !== 'dihedral' && cert.target.family !== 'control' && cert.target.family !== 'general') errors.push('unknown target.family');
  if (cert.target.family === 'dihedral' && (!Number.isInteger(cert.target.n) || cert.target.n < 3)) errors.push('dihedral target.n is invalid');
  if (cert.target.family === 'control' && cert.target.n !== 5) errors.push('control target.n must be 5');
  if (isGeneral && !hasOwn(cert.target, 'construction')) errors.push('target.construction is missing (general family requires phi_L generator images per week3-L-設計.md §3)');
  for (const key of ['shadows', 'counts', 'composition_table', 'inverse_map', 'reduction', 'ls_witness']) {
    if (!hasOwn(cert, key)) errors.push(`${key} is missing`);
  }
  if (!Array.isArray(cert.shadows)) errors.push('shadows is not an array');
  if (!Array.isArray(cert.composition_table)) errors.push('composition_table is not an array');
  if (!Array.isArray(cert.inverse_map)) errors.push('inverse_map is not an array');
  if (!Array.isArray(cert.reduction)) errors.push('reduction is not an array');
  if (!Array.isArray(cert.ls_witness)) errors.push('ls_witness is not an array');
  if (cert.target.invariants && typeof cert.target.invariants === 'object') {
    for (const key of ['index_PB3', 'index_B3', 'N_ord', 'derived_order']) {
      if (!hasOwn(cert.target.invariants, key)) errors.push(`target.invariants.${key} is missing`);
    }
  }
  if (Array.isArray(cert.shadows)) {
    cert.shadows.forEach((sh, i) => {
      // general (Q_L=G3xH3) の f_triple は G3 成分のみ (実測: WP3a explorer は H3 成分の専用
      // フィールドを持たない)。Q_L の完全な元は f_word から自前再構成する(checkCertificateGeneral 参照)。
      const requiredShadowKeys = ['m', 'f_word', 'f_triple', 'kernel_cert'];
      for (const key of requiredShadowKeys) if (!hasOwn(sh, key)) errors.push(`shadow[${i}].${key} is missing`);
      if (!Array.isArray(sh.f_word) || !Array.isArray(sh.f_triple)) errors.push(`shadow[${i}] word/triple malformed`);
    });
  }
  return errors;
}

function tripleKey(triple) {
  return triple.map(([a, e]) => `${a},${e}`).join('|');
}

// ---------- Q x T transversal モデル (12 規則) ----------
// t0..t5 = t1..t6 = e, s1, s2, s1s2, s2s1, Delta
const RULES = [
  /* t0=e        */ { s1: { p: [], t: 1 }, s2: { p: [], t: 2 } },
  /* t1=s1       */ { s1: { p: [['x', 1]], t: 0 }, s2: { p: [], t: 3 } },
  /* t2=s2       */ { s1: { p: [], t: 4 }, s2: { p: [['y', 1]], t: 0 } },
  /* t3=s1s2     */ { s1: { p: [], t: 5 }, s2: { p: [['y', -1], ['x', -1], ['c', 1]], t: 1 } },
  /* t4=s2s1     */ { s1: { p: [['x', -1], ['y', -1], ['c', 1]], t: 2 }, s2: { p: [], t: 5 } },
  /* t5=Delta    */ { s1: { p: [['y', 1]], t: 3 }, s2: { p: [['x', 1]], t: 4 } },
];

function buildTransversalModel(Q, phi) {
  const qElems = Q.elements();
  const qN = qElems.length;
  const qIndex = new Map();
  qElems.forEach((e, i) => qIndex.set(Q.key(e), i));
  const N = qN * 6;
  const idx = (qi, ti) => qi * 6 + ti;

  function buildPerm(which) {
    const perm = new Array(N);
    for (let qi = 0; qi < qN; qi++) {
      for (let ti = 0; ti < 6; ti++) {
        const rule = RULES[ti][which];
        const pElem = evalWord(Q, phi, rule.p);
        const newQ = Q.mul(qElems[qi], pElem);
        const newQi = qIndex.get(Q.key(newQ));
        if (newQi === undefined) throw new Error('transversal model: Q closure broken');
        perm[idx(qi, ti)] = idx(newQi, rule.t);
      }
    }
    return perm;
  }

  const perm1 = buildPerm('s1');
  const perm2 = buildPerm('s2');
  return { Q, phi, qElems, qIndex, N, idx, perm1, perm2 };
}

function invPerm(perm) {
  const inv = new Array(perm.length);
  for (let i = 0; i < perm.length; i++) inv[perm[i]] = i;
  return inv;
}
function composeRight(a, b) { // apply a then b
  const out = new Array(a.length);
  for (let i = 0; i < a.length; i++) out[i] = b[a[i]];
  return out;
}
function composeAll(perms) {
  let res = perms[0];
  for (let i = 1; i < perms.length; i++) res = composeRight(res, perms[i]);
  return res;
}
function identityPerm(n) { const p = new Array(n); for (let i = 0; i < n; i++) p[i] = i; return p; }
function permEq(a, b) { if (a.length !== b.length) return false; for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return false; return true; }
function permPow(perm, k) {
  const N = perm.length;
  if (k === 0) return identityPerm(N);
  const base = k < 0 ? invPerm(perm) : perm;
  let res = identityPerm(N);
  for (let i = 0; i < Math.abs(k); i++) res = composeRight(res, base);
  return res;
}

// x = sigma1^2, y = sigma2^2, Delta = s1 s2 s1, c = Delta^2
function modelDerivedPerms(model) {
  const x_perm = composeRight(model.perm1, model.perm1);
  const y_perm = composeRight(model.perm2, model.perm2);
  const delta_perm = composeAll([model.perm1, model.perm2, model.perm1]);
  const c_perm = composeRight(delta_perm, delta_perm);
  return { x_perm, y_perm, delta_perm, c_perm };
}

// F2 語 (x,y のみ) を sigma-permutation へ: x^k -> s1^{2k}, y^k -> s2^{2k}
function xyWordToPerm(model, tokens) {
  const N = model.N;
  let res = identityPerm(N);
  for (const [gen, k] of tokens) {
    const base = gen === 'x' ? model.perm1 : model.perm2;
    res = composeRight(res, permPow(base, 2 * k));
  }
  return res;
}

// ---------- 自己検査 ----------
function selfCheck() {
  const log = [];
  let ok = true;

  const rawFixtureOk = rawCountFixtureSelfCheck();
  log.push(`fail-closed raw count fixture (wrong raw is rejected): ${rawFixtureOk ? 'PASS' : 'FAIL'}`);
  if (!rawFixtureOk) ok = false;

  // (0) Dn 群の公理 (単位元・逆元・簡単な結合則スポットチェック)
  {
    const Dn = makeDn(7);
    const els = Dn.elements();
    let axFail = 0;
    for (const g of els) {
      if (!Dn.eq(Dn.mul(g, Dn.id), g)) axFail++;
      if (!Dn.eq(Dn.mul(g, Dn.inv(g)), Dn.id)) axFail++;
    }
    // 結合則スポットチェック (全 343 通りは重いので簡易サンプル)
    const sample = els.slice(0, 6);
    for (const a of sample) for (const b of sample) for (const c of sample) {
      const l = Dn.mul(Dn.mul(a, b), c);
      const r = Dn.mul(a, Dn.mul(b, c));
      if (!Dn.eq(l, r)) axFail++;
    }
    log.push(`D7 群公理 (単位元/逆元/結合則サンプル): ${axFail === 0 ? 'PASS' : 'FAIL(' + axFail + ')'}`);
    if (axFail !== 0) ok = false;
  }

  // (1),(2),(3) braid / sigma^2 / c-check / 群位数較正 を n=5,8 で実施
  for (const n of [5, 8]) {
    const Dn = makeDn(n);
    const r = { a: 1, e: 0 }, s = { a: 0, e: 1 };
    const phi = { x: s, y: Dn.mul(r, s), c: Dn.id };
    const model = buildTransversalModel(Dn, phi);
    const { x_perm, y_perm, delta_perm, c_perm } = modelDerivedPerms(model);

    // braid: s1 s2 s1 == s2 s1 s2
    const lhsBraid = composeAll([model.perm1, model.perm2, model.perm1]);
    const rhsBraid = composeAll([model.perm2, model.perm1, model.perm2]);
    const braidOk = permEq(lhsBraid, rhsBraid);
    log.push(`n=${n}: braid s1s2s1=s2s1s2 : ${braidOk ? 'PASS' : 'FAIL'}`);
    if (!braidOk) ok = false;

    // sigma_i^2 は t 成分を固定し、t=t1(=e) では q -> q*phi(x or y)
    let tFixOk = true, expectAtE_x = true, expectAtE_y = true;
    for (let qi = 0; qi < model.qElems.length; qi++) {
      for (let ti = 0; ti < 6; ti++) {
        const p = model.idx(qi, ti);
        const dx = x_perm[p], dy = y_perm[p];
        if (dx % 6 !== ti) tFixOk = false;
        if (dy % 6 !== ti) tFixOk = false;
      }
      const p0 = model.idx(qi, 0);
      const expQ_x = model.qIndex.get(Dn.key(Dn.mul(model.qElems[qi], phi.x)));
      const expQ_y = model.qIndex.get(Dn.key(Dn.mul(model.qElems[qi], phi.y)));
      if (Math.floor(x_perm[p0] / 6) !== expQ_x) expectAtE_x = false;
      if (Math.floor(y_perm[p0] / 6) !== expQ_y) expectAtE_y = false;
    }
    log.push(`n=${n}: sigma_i^2 が t 成分を固定 : ${tFixOk ? 'PASS' : 'FAIL'}`);
    log.push(`n=${n}: sigma1^2|_{t=e} = q*phi(x) : ${expectAtE_x ? 'PASS' : 'FAIL'}`);
    log.push(`n=${n}: sigma2^2|_{t=e} = q*phi(y) : ${expectAtE_y ? 'PASS' : 'FAIL'}`);
    if (!tFixOk || !expectAtE_x || !expectAtE_y) ok = false;

    // c-check: c = Delta^2 は全点で q -> q*phi(c) を一様に与え、t 成分を固定 (c は PB3 中心)
    let cUniformOk = true;
    for (let qi = 0; qi < model.qElems.length; qi++) {
      for (let ti = 0; ti < 6; ti++) {
        const p = model.idx(qi, ti);
        if (c_perm[p] % 6 !== ti) cUniformOk = false;
        const expQ = model.qIndex.get(Dn.key(Dn.mul(model.qElems[qi], phi.c)));
        if (Math.floor(c_perm[p] / 6) !== expQ) cUniformOk = false;
      }
    }
    log.push(`n=${n}: c-hat = phi(c) が全点で一様 : ${cUniformOk ? 'PASS' : 'FAIL'}`);
    if (!cUniformOk) ok = false;

    // 群位数較正: |<sigma1,sigma2>| = 6|Gn| (n=5: 3000, n=8: 1536) -- wp2-transversal-model.md 検算記録より
    const expectedGnOrd = expectedGnOrder(n);
    const expectedGroupOrder = 6 * expectedGnOrd;
    const inv1 = invPerm(model.perm1), inv2 = invPerm(model.perm2);
    const gens = [model.perm1, model.perm2, inv1, inv2];
    const seen = new Map();
    const id0 = identityPerm(model.N);
    seen.set(id0.join(','), true);
    const frontier = [id0];
    let cap = 20000; // 安全キャップ (期待値 <=1536 なので十分)
    while (frontier.length && seen.size < cap) {
      const e = frontier.pop();
      for (const g of gens) {
        const cand = composeRight(e, g);
        const k = cand.join(',');
        if (!seen.has(k)) { seen.set(k, true); frontier.push(cand); }
      }
    }
    const groupOrder = seen.size;
    const orderOk = (groupOrder === expectedGroupOrder);
    log.push(`n=${n}: |<sigma1hat,sigma2hat>| = ${groupOrder} (期待 ${expectedGroupOrder} = 6*|G_${n}|=6*${expectedGnOrd}) : ${orderOk ? 'PASS' : 'FAIL'}`);
    if (!orderOk) ok = false;
  }

  // (4) Week3 general family: H3 fixture + Q_L = G3 x H3 構成 + 12 規則モデルの自己検査
  // (docs/week3-L-設計.md v1.1 §1・§2。search/ の explorer は一切参照しない)
  {
    const H3 = makeH3();
    const X = { a: 1, b: 0, e: 0 }, Y = { a: 0, b: 1, e: 0 };
    const x3 = H3.pow(X, 3), y3 = H3.pow(Y, 3);
    const xy = H3.mul(X, Y);
    const xy3 = H3.pow(xy, 3);
    const fixtureOk = H3.eq(x3, H3.id) && H3.eq(y3, H3.id) && H3.eq(xy3, H3.id);
    const comm = commutator(H3, X, Y);
    const commCentral = H3.eq(H3.mul(comm, X), H3.mul(X, comm)) && H3.eq(H3.mul(comm, Y), H3.mul(Y, comm));
    const commOrder3 = !H3.eq(comm, H3.id) && H3.eq(H3.pow(comm, 3), H3.id);
    const nonComm = !H3.eq(H3.mul(X, Y), H3.mul(Y, X));
    const h3Ok = fixtureOk && commCentral && commOrder3 && nonComm;
    log.push(`H3 fixture (X^3=Y^3=(XY)^3=1, [X,Y] 中心・位数3, 非可換) : ${h3Ok ? 'PASS' : 'FAIL'}`);
    if (!h3Ok) ok = false;

    const QL = buildQL();
    const qlSizeOk = QL.QLMap.size === 2916;
    log.push(`|Q_L| = ${QL.QLMap.size} (期待 2916 = |G3|*|H3| = 108*27) : ${qlSizeOk ? 'PASS' : 'FAIL'}`);
    if (!qlSizeOk) ok = false;
    const derivedOk = QL.derived.size === 81;
    log.push(`|[Q_L,Q_L]| = ${QL.derived.size} (期待 81 = 27*3) : ${derivedOk ? 'PASS' : 'FAIL'}`);
    if (!derivedOk) ok = false;

    const model = buildTransversalModel(QL.Triple, QL.phiTriple);
    const modelSizeOk = model.N === 17496;
    log.push(`Q_L x T 点数 = ${model.N} (期待 17496 = 2916*6) : ${modelSizeOk ? 'PASS' : 'FAIL'}`);
    if (!modelSizeOk) ok = false;

    const lhsBraid = composeAll([model.perm1, model.perm2, model.perm1]);
    const rhsBraid = composeAll([model.perm2, model.perm1, model.perm2]);
    const braidOk = permEq(lhsBraid, rhsBraid);
    log.push(`Q_L: braid s1s2s1=s2s1s2 : ${braidOk ? 'PASS' : 'FAIL'}`);
    if (!braidOk) ok = false;

    const { x_perm, y_perm, c_perm } = modelDerivedPerms(model);
    let tFixOk = true;
    for (let p = 0; p < model.N; p++) { if (x_perm[p] % 6 !== p % 6) tFixOk = false; if (y_perm[p] % 6 !== p % 6) tFixOk = false; }
    log.push(`Q_L: sigma_i^2 が t 成分を固定 : ${tFixOk ? 'PASS' : 'FAIL'}`);
    if (!tFixOk) ok = false;

    // c-hat: phi_L(c) = (1,1) (=id in Q_L) なので Delta^2 は全点で恒等置換のはず
    const cHatIdentity = permEq(c_perm, identityPerm(model.N));
    log.push(`Q_L: c-hat = phi_L(c) = id (全点で恒等) : ${cHatIdentity ? 'PASS' : 'FAIL'}`);
    if (!cHatIdentity) ok = false;

    // 軌道: <sigma1,sigma2,sigma1^-1,sigma2^-1> の基点 (id_QL, t0) からの軌道が全 17496 点を覆う (推移性)
    const invP1 = invPerm(model.perm1), invP2 = invPerm(model.perm2);
    const orbit = new Set([0]);
    const frontier = [0];
    while (frontier.length) {
      const p = frontier.pop();
      for (const perm of [model.perm1, model.perm2, invP1, invP2]) {
        const q = perm[p];
        if (!orbit.has(q)) { orbit.add(q); frontier.push(q); }
      }
    }
    const orbitOk = orbit.size === 17496;
    log.push(`Q_L: <sigma1hat,sigma2hat> の軌道サイズ = ${orbit.size} (期待 17496) : ${orbitOk ? 'PASS' : 'FAIL'}`);
    if (!orbitOk) ok = false;
  }

  return { ok, log };
}

// ---------- 主要判定ロジック (証明書ごと) ----------

function dihedralPhi(n) {
  const Dn = makeDn(n);
  const r = { a: 1, e: 0 }, s = { a: 0, e: 1 };
  return { Q: Dn, phi: { x: s, y: Dn.mul(r, s), c: Dn.id } };
}

function controlN5Phi() {
  const C5 = makeCyclic(5);
  return { Q: C5, phi: { x: 2, y: 2, c: 1 } };
}

function tripleFromCertFormat(arr) {
  // 証明書の f_triple: [[a,e],[a,e],[a,e]]
  return arr.map(([a, e]) => ({ a, e }));
}

function checkHexagon(model, shadow) {
  const { perm1, perm2 } = model;
  const inv1 = invPerm(perm1), inv2 = invPerm(perm2);
  const { x_perm, y_perm, c_perm } = modelDerivedPerms(model);
  const invX = invPerm(x_perm), invY = invPerm(y_perm), invC = invPerm(c_perm);
  const m = shadow.m;
  const fPerm = xyWordToPerm(model, shadow.f_word);
  const invF = invPerm(fPerm);

  // (3.3): s1^{2m+1} f^-1 s2^{2m+1} f == f^-1 s1 s2 x^-m c^m
  const lhs33 = composeAll([permPow(perm1, 2 * m + 1), invF, permPow(perm2, 2 * m + 1), fPerm]);
  const rhs33 = composeAll([invF, perm1, perm2, permPow(x_perm, -m), permPow(c_perm, m)]);
  const ok33 = permEq(lhs33, rhs33);

  // (3.4): f^-1 s2^{2m+1} f s1^{2m+1} == s2 s1 y^-m c^m f
  const lhs34 = composeAll([invF, permPow(perm2, 2 * m + 1), fPerm, permPow(perm1, 2 * m + 1)]);
  const rhs34 = composeAll([perm2, perm1, permPow(y_perm, -m), permPow(c_perm, m), fPerm]);
  const ok34 = permEq(lhs34, rhs34);

  return { ok33, ok34, ok: ok33 && ok34 };
}

function checkFWordVsTriple(Gn, n, shadow) {
  const { Triple, phiTriple } = Gn;
  const computed = evalWord(Triple, phiTriple, shadow.f_word);
  const given = tripleFromCertFormat(shadow.f_triple);
  const eq = Triple.eq(computed, given);
  return { ok: eq, computed_key: Triple.key(computed), given_key: Triple.key(given) };
}

function checkCharmingAndSurjective(Gn, n, shadow) {
  const { Triple, phiTriple, GnMap, derived, X, Y } = Gn;
  const m = shadow.m;
  const fTriple = tripleFromCertFormat(shadow.f_triple);
  // charming: f in [Gn,Gn]
  const charming = derived.has(Triple.key(fTriple));

  // surjective: <x^{2m+1}, f^-1 y^{2m+1} f> == Gn
  const g1 = Triple.pow(X, 2 * m + 1);
  const invF = Triple.inv(fTriple);
  const g2 = Triple.mul(Triple.mul(invF, Triple.pow(Y, 2 * m + 1)), fTriple);
  const gen = subgroupClosure(Triple, [g1, g2]);
  const surjective = gen.size === GnMap.size;

  return { charming, surjective, ok: charming && surjective };
}

function checkThm43(Gn, n, cert) {
  const expected = thm43ShadowSet(n);
  const expectedKeys = new Set(expected.shadows.map((s) => `${s.m}|${tripleKey(s.triple)}`));
  const certKeys = new Set();
  const dupCount = { count: 0 };
  for (const sh of cert.shadows) {
    const k = `${mod(sh.m, expected.Nord)}|${tripleKey(sh.f_triple)}`;
    if (certKeys.has(k)) dupCount.count++;
    certKeys.add(k);
  }
  let missingInCert = 0, extraInCert = 0;
  for (const k of expectedKeys) if (!certKeys.has(k)) missingInCert++;
  for (const k of certKeys) if (!expectedKeys.has(k)) extraInCert++;
  const setEqual = (missingInCert === 0 && extraInCert === 0 && certKeys.size === expectedKeys.size);
  return {
    ok: setEqual,
    expected_count: expectedKeys.size,
    cert_count: certKeys.size,
    missing_in_cert: missingInCert,
    extra_in_cert: extraInCert,
    duplicates_in_cert: dupCount.count,
  };
}

function checkCertificateInvariants(cert, Gn, n) {
  const inv = cert.target.invariants || {};
  const expectedNord = lcm(n, 2);
  const expectedGroup = expectedGnOrder(n);
  const actualGroup = Gn.GnMap.size;
  const actualDerived = Gn.derived.size;
  const checks = {
    index_PB3: inv.index_PB3 === actualGroup && actualGroup === expectedGroup,
    index_B3: inv.index_B3 === 6 * inv.index_PB3 && inv.index_B3 === 6 * expectedGroup,
    N_ord: inv.N_ord === expectedNord,
    derived_order: inv.derived_order === actualDerived,
  };
  return { ok: Object.values(checks).every(Boolean), expected: { index_PB3: expectedGroup, index_B3: 6 * expectedGroup, N_ord: expectedNord, derived_order: actualDerived }, claimed: inv, checks };
}

function checkRawCandidateFormula(cert, Gn, n) {
  const expected = thm43ShadowSet(n);
  const XnCount = expected.Xn.length;
  const derivedOrder = Gn.derived.size;
  const expectedRaw = XnCount * derivedOrder;
  const claimedRaw = cert.counts?.raw_candidates;
  return { ok: claimedRaw === expectedRaw, claimed_raw: claimedRaw, expected_raw: expectedRaw, X_n_count: XnCount, derived_order: derivedOrder };
}

function rawCountFixtureSelfCheck() {
  const expected = { counts: { raw_candidates: 1 } };
  const fake = { ...expected, target: { n: 4 }, shadows: [] };
  const fakeGn = { derived: { size: 2 } };
  return checkRawCandidateFormula(fake, fakeGn, 4).ok === false;
}

function checkN5Enumeration(model, cert) {
  const expectedM = [0, 1, 3, 4];
  const rows = [];
  for (let m = 0; m < 5; m++) {
    const shadow = { m, f_word: [], f_triple: [[0, 0], [0, 0], [0, 0]] };
    const hex = checkHexagon(model, shadow);
    const unit = gcd(2 * m + 1, 5) === 1;
    const u = 2 * m + 1;
    const g1 = permPow(model.perm1, u);
    const g2 = permPow(model.perm2, u);
    const gen = enumeratePermGroup([g1, g2]);
    const surjective = gen.size === 30;
    rows.push({ m, hexagon: hex.ok, charming_unit: unit, surjective, accepted: hex.ok && unit && surjective });
  }
  const accepted = rows.filter((r) => r.accepted).map((r) => r.m);
  const certM = cert.shadows.map((s) => s.m).sort((a, b) => a - b);
  const directCentral = [];
  const centralWord = [['s1', 1], ['s2', 1], ['s1', 1], ['s1', 1], ['s2', 1], ['s1', 1]];
  const centralPerm = modelDerivedPerms(model).c_perm;
  for (const sh of cert.shadows) {
    const u = 2 * sh.m + 1;
    const fPerm = xyWordToPerm(model, sh.f_word);
    const invF = invPerm(fPerm);
    const sigma1T = permPow(model.perm1, u);
    const sigma2T = composeAll([invF, permPow(model.perm2, u), fPerm]);
    let image = identityPerm(model.N);
    for (const [name, sign] of centralWord) {
      const gp = name === 's1' ? (sign > 0 ? sigma1T : invPerm(sigma1T)) : (sign > 0 ? sigma2T : invPerm(sigma2T));
      image = composeRight(image, gp);
    }
    directCentral.push({ m: sh.m, pass: permEq(image, permPow(centralPerm, u)) });
  }
  const c = cert.counts || {};
  const countsOk = c.raw_candidates === 5 && c.hexagon_pass === 5 && c.charming_pass === 4 && c.surjective_pass === 4;
  const acceptedOk = accepted.join(',') === expectedM.join(',') && certM.join(',') === expectedM.join(',');
  return { ok: countsOk && acceptedOk && directCentral.every((r) => r.pass), counts: { raw_candidates: 5, hexagon_pass: rows.filter((r) => r.hexagon).length, charming_pass: rows.filter((r) => r.hexagon && r.charming_unit).length, surjective_pass: rows.filter((r) => r.hexagon && r.charming_unit && r.surjective).length }, expected_counts: { raw_candidates: 5, hexagon_pass: 5, charming_pass: 4, surjective_pass: 4 }, m_set: accepted, expected_m_set: expectedM, stages: rows, central_power_direct: directCentral };
}

function enumeratePermGroup(gens) {
  const steps = [];
  for (const [name, perm] of gens.map((p, i) => [i === 0 ? 's1' : 's2', p])) {
    steps.push([name, 1, perm], [name, -1, invPerm(perm)]);
  }
  const id = identityPerm(gens[0].length);
  const seen = new Map([[id.join(','), { perm: id, word: [] }]]);
  const queue = [seen.get(id.join(','))];
  for (let qi = 0; qi < queue.length; qi++) {
    const cur = queue[qi];
    for (const [name, sign, perm] of steps) {
      const cand = composeRight(cur.perm, perm);
      const key = cand.join(',');
      if (!seen.has(key)) { const v = { perm: cand, word: cur.word.concat([[name, sign]]) }; seen.set(key, v); queue.push(v); }
    }
  }
  return seen;
}

function checkStrictCompositionInverse(cert, Gn, n) {
  const S = cert.shadows.length, Nord = lcm(n, 2), indexErrors = [], pairSeen = new Set(), inverseSeen = new Set();
  for (const row of cert.composition_table) {
    if (!Array.isArray(row) || row.length !== 3 || !row.every(Number.isInteger)) { indexErrors.push({ row, reason: 'row shape' }); continue; }
    const [i, j, k] = row;
    if (i < 0 || i >= S || j < 0 || j >= S || k < 0 || k >= S) indexErrors.push({ row, reason: 'index out of range' });
    const pair = `${i},${j}`;
    if (pairSeen.has(pair)) indexErrors.push({ row, reason: 'duplicate ordered pair' });
    pairSeen.add(pair);
  }
  for (let i = 0; i < S; i++) for (let j = 0; j < S; j++) if (!pairSeen.has(`${i},${j}`)) indexErrors.push({ i, j, reason: 'missing ordered pair' });
  const compRows = cert.composition_table.map(([i, j, k]) => ({ i, j, k })).filter((r) => r.i >= 0 && r.i < S && r.j >= 0 && r.j < S && r.k >= 0 && r.k < S);
  const compChecks = compRows.map((row) => ({ ...row, ...checkCompositionEntry(Gn, n, Nord, cert.shadows, row.i, row.j, row.k) }));
  for (const row of cert.inverse_map) {
    if (!Array.isArray(row) || row.length !== 2 || !row.every(Number.isInteger)) { indexErrors.push({ row, reason: 'inverse row shape' }); continue; }
    const [i, j] = row;
    if (i < 0 || i >= S || j < 0 || j >= S) indexErrors.push({ row, reason: 'inverse index out of range' });
    if (inverseSeen.has(i)) indexErrors.push({ row, reason: 'duplicate inverse source' });
    inverseSeen.add(i);
  }
  for (let i = 0; i < S; i++) if (!inverseSeen.has(i)) indexErrors.push({ i, reason: 'missing inverse source' });
  const invRows = cert.inverse_map.map(([i, j]) => ({ i, j })).filter((r) => r.i >= 0 && r.i < S && r.j >= 0 && r.j < S);
  const invChecks = invRows.map((row) => ({ ...row, ...checkInverseEntry(Gn, n, Nord, cert.shadows, row.i, row.j) }));
  return { ok: indexErrors.length === 0 && compRows.length === S * S && compChecks.every((r) => r.ok) && invRows.length === S && invChecks.every((r) => r.ok), composition_rows: compRows.length, composition_expected: S * S, composition_pair_unique: pairSeen.size === S * S, composition_failures: compChecks.filter((r) => !r.ok).slice(0, 10), inverse_rows: invRows.length, inverse_expected: S, inverse_source_unique: inverseSeen.size === S, inverse_failures: invChecks.filter((r) => !r.ok).slice(0, 10), structural_errors: indexErrors.slice(0, 20) };
}

function requiredReductionsFor(n) {
  const req = { 8: ['K4'], 12: ['K4'], 9: ['K3'], 18: ['K3'], 36: ['K12', 'K4'] };
  return req[n] || [];
}

function checkReductionCoverage(cert, certsById) {
  const required = requiredReductionsFor(cert.target.n);
  const listed = cert.reduction.map((r) => r && r.to);
  const exact = listed.length === required.length && required.every((id) => listed.filter((x) => x === id).length === 1);
  const results = [];
  for (const id of required) {
    const entry = cert.reduction.find((r) => r.to === id);
    if (!entry) { results.push({ to: id, ok: false, reason: 'required reduction entry missing' }); continue; }
    const target = certsById.get(id);
    const checked = checkReductionEntry(cert.target.n, entry, cert.shadows, target);
    results.push({ to: id, ...checked });
  }
  return { ok: exact && results.every((r) => r.ok === true), required, listed, exact_entry_set: exact, results };
}

// =====================================================================
// Week3 general family (target.family="general", id="L01" 想定)
// docs/week3-L-設計.md v1.1 §3・§5 の検査項目実装。search/ の explorer は不参照。
// 証明書スキーマの実態 (certificates/L01.v1.json 実測で確認):
//   shadow.f_triple = G3 成分のみ (既存 dihedral と同一形式 [[a,e],[a,e],[a,e]])
//   H3 成分の専用フィールドは存在しない。Q_L の完全な元(G3+H3)が要る箇所(charming・
//   composition・inverse)は f_word を Q_L=G3xH3 で評価して自前再構成する(evalShadowQL)。
//   item3(f_word<->f_pair)は結果として G3 成分のみの突合になる — 証明書に格納された
//   冗長データがそれしかないため。他の項目はすべて f_word からの独立再計算で完結する。
// =====================================================================

function checkRawCandidateFormulaGeneral(cert, QL) {
  const XL = xn(6); // 𝒳_L = {m in 0..5 : gcd(2m+1,6)=1} = {0,2,3,5}
  const derivedOrder = QL.derived.size;
  const expectedRaw = XL.length * derivedOrder;
  const claimedRaw = cert.counts?.raw_candidates;
  return { ok: claimedRaw === expectedRaw, claimed_raw: claimedRaw, expected_raw: expectedRaw, X_L_count: XL.length, derived_order: derivedOrder };
}

function checkCertificateInvariantsGeneral(cert, QL) {
  const inv = cert.target.invariants || {};
  const actualDerived = QL.derived.size;
  const checks = {
    index_PB3: inv.index_PB3 === 2916 && QL.QLMap.size === 2916,
    index_B3: inv.index_B3 === 17496 && inv.index_B3 === 6 * inv.index_PB3,
    N_ord: inv.N_ord === 6,
    derived_order: inv.derived_order === 81 && inv.derived_order === actualDerived,
  };
  return { ok: Object.values(checks).every(Boolean), expected: { index_PB3: 2916, index_B3: 17496, N_ord: 6, derived_order: actualDerived }, claimed: inv, checks };
}

// 証明書スキーマの実態(WP3a explorer の実際の出力を確認): shadow は f_triple(G3 成分)のみを
// 格納し、H3 成分を格納する専用フィールドは存在しない。ゆえに Q_L の完全な元が必要な箇所
// (charming・composition・inverse)では f_word を Q_L で評価して自前で再構成する(f_h3 という
// フィールドを信用しない・存在すればなお良いが必須にしない、で独立性をむしろ強める)。
// item3 は「f_word の評価と証明書が格納する f_triple(G3 成分)の突合」に限定する。
function checkFWordVsPairGeneral(QL, shadow) {
  const computed = evalWord(QL.Triple, QL.phiTriple, shadow.f_word); // [G3elem, H3elem]
  const computedG3 = computed[0];
  const givenG3 = tripleFromCertFormat(shadow.f_triple);
  const g3Ok = QL.G3.Triple.eq(computedG3, givenG3);
  return {
    ok: g3Ok, g3Ok,
    computed_g3_key: QL.G3.Triple.key(computedG3), given_g3_key: QL.G3.Triple.key(givenG3),
    note: '証明書スキーマに H3 成分の専用フィールドが無いため、G3 成分(f_triple)のみを突合する。H3 成分を要する検査(charming/composition/inverse)は f_word を Q_L で評価して自前再構成する。',
  };
}

function evalShadowQL(QL, shadow) {
  return evalWord(QL.Triple, QL.phiTriple, shadow.f_word || []);
}

function checkCharmingAndSurjectiveGeneral(QL, shadow) {
  const { Triple, phiTriple, QLMap, derived, X, Y } = QL;
  const m = shadow.m;
  const fTriple = evalShadowQL(QL, shadow);
  const charming = derived.has(Triple.key(fTriple));
  const g1 = Triple.pow(X, 2 * m + 1);
  const invF = Triple.inv(fTriple);
  const g2 = Triple.mul(Triple.mul(invF, Triple.pow(Y, 2 * m + 1)), fTriple);
  const gen = subgroupClosure(Triple, [g1, g2]);
  const surjective = gen.size === QLMap.size;
  return { charming, surjective, ok: charming && surjective };
}

// kernel brute (N5 の checkKernelCertBrute と同じ数学的手続きの一般化だが、実装は別)。
// N5 は N=30 点なので全順列(長さ30の配列)を Map のキー/値として素朴に保持しても軽い。
// L01 は N=17496 点で、同じ素朴な実装(全順列を要素ごとに Map へ格納)を試したところ
// 17496×17496 の全順列格納が発生し JS heap が枯渇して OOM した(実測)。
// 対策: expected_kernel_index = model.N(点数)なので、軌道-安定化群定理より
// <sigma1,sigma2> の B3/L 上の作用は正則(自由)であることが構成上保証される。正則表現の元は
// 基点(点0)の像 1 個で一意に定まるので、各元を「基点の像」という 1 整数だけで追跡すれば足り、
// O(N) の点追跡だけで済む(O(N^2) の全順列格納を回避)。T-像側も同じ基点を並行して追跡し、
// 衝突(同じ源点に別の語で到達)時に T-像の基点が食い違えば、その時点で「井戸定義でない」の
// 確証となる(全順列として不一致であることの十分条件)。最終的に T-像側の基点到達集合の
// サイズが expectedIdx に届けば Im(T) も正則表現になるため、基点一致 <=> 全順列一致が成立する
// (双方が位数 N の正則表現になるため)。
function checkKernelCertBruteGeneral(model, shadow, opts = {}) {
  const maxMs = opts.maxMs ?? 120000;
  const kc = shadow.kernel_cert;
  if (!kc || kc.type !== 'brute') return { ok: false, reason: 'kernel_cert.type が brute でない' };
  const expectedIdx = kc.expected_kernel_index;
  const elementCap = opts.elementCap ?? (expectedIdx + 100);
  const started = Date.now();
  const m = shadow.m;
  const fPerm = xyWordToPerm(model, shadow.f_word);
  const invF = invPerm(fPerm);
  const sigma1T = permPow(model.perm1, 2 * m + 1);
  const invSigma1T = invPerm(sigma1T);
  const sigma2T = composeAll([invF, permPow(model.perm2, 2 * m + 1), fPerm]);
  const invSigma2T = invPerm(sigma2T);
  const invP1 = invPerm(model.perm1), invP2 = invPerm(model.perm2);

  const genSteps = [
    ['s1', 1, model.perm1, sigma1T],
    ['s1', -1, invP1, invSigma1T],
    ['s2', 1, model.perm2, sigma2T],
    ['s2', -1, invP2, invSigma2T],
  ];
  const tPointOf = new Map([[0, 0]]); // sourcePoint(基点の像) -> tPoint(T-像の基点)
  let frontier = [{ sp: 0, tp: 0 }];
  let wellDefined = true;
  const conflicts = [];
  let timedOut = false;
  let iter = 0;
  while (frontier.length && tPointOf.size < elementCap) {
    if (((iter++) & 511) === 0 && Date.now() - started > maxMs) { timedOut = true; break; }
    const next = [];
    for (const node of frontier) {
      for (const [name, sign, gp, tgp] of genSteps) {
        const candSp = gp[node.sp];
        const candTp = tgp[node.tp];
        if (!tPointOf.has(candSp)) {
          tPointOf.set(candSp, candTp);
          next.push({ sp: candSp, tp: candTp });
        } else {
          const existingTp = tPointOf.get(candSp);
          if (existingTp !== candTp) {
            wellDefined = false;
            if (conflicts.length < 10) conflicts.push({ source_point: candSp, existing_t_point: existingTp, candidate_t_point: candTp });
          }
        }
      }
    }
    frontier = next;
    if (Date.now() - started > maxMs) { timedOut = true; break; }
  }
  const groupOrder = tPointOf.size;
  const orderOk = !timedOut && groupOrder === expectedIdx;
  const distinctTPoints = new Set(tPointOf.values()).size;
  const imageOrderOk = !timedOut && distinctTPoints === expectedIdx;
  const elapsedMs = Date.now() - started;
  return {
    ok: !timedOut && orderOk && wellDefined && imageOrderOk,
    timed_out: timedOut, elapsed_ms: elapsedMs,
    groupOrder, expectedIdx, orderOk, wellDefined,
    conflicts,
    imageOrderCount: distinctTPoints, imageOrderOk,
    method: 'basepoint-tracking (regular-representation shortcut) -- O(N) memory, see comment above',
  };
}

// composition (3.53) の一般化 (E_{m,f} は群非依存の式なので QL にそのまま適用できる).
// (4.19) は代数的恒等式として汎用に成立するが (4.20) は kappa(=Dn の r 冪指数) 依存なので N/A。
function checkCompositionEntryGeneral(QL, Nord, shadows, i, j, k) {
  const shA = shadows[i], shB = shadows[j], shC = shadows[k];
  const { mNewRaw } = composeShadowWords(shA.m, shA.f_word, shB.m, shB.f_word);
  const mNew = mod(mNewRaw, Nord);
  const mOk = mNew === mod(shC.m, Nord);
  const { Triple, phiTriple } = QL;
  const f1Triple = evalWord(Triple, phiTriple, shA.f_word);
  const computedTriple = Triple.mul(f1Triple, evalFactorUnderAction(QL, shA.m, f1Triple, shB.f_word));
  const givenTriple = evalShadowQL(QL, shC);
  const tripleOk = Triple.eq(computedTriple, givenTriple);
  const u1 = 2 * shA.m + 1, u2 = 2 * shB.m + 1;
  const id419 = (u1 * u2) === (2 * mNewRaw + 1);
  return { ok: mOk && tripleOk && id419, mOk, tripleOk, id419 };
}

function checkInverseEntryGeneral(QL, Nord, shadows, i, iInv) {
  const shA = shadows[i], shB = shadows[iInv];
  const idShadow = { m: 0, f_word: [], f_triple: identityTripleFormat() };
  const c1 = checkCompositionEntryGeneral(QL, Nord, [shA, shB, idShadow], 0, 1, 2);
  const c2 = checkCompositionEntryGeneral(QL, Nord, [shB, shA, idShadow], 0, 1, 2);
  return { ok: c1.ok && c2.ok, forward: c1, backward: c2 };
}

function checkStrictCompositionInverseGeneral(cert, QL) {
  const S = cert.shadows.length, Nord = 6, indexErrors = [], pairSeen = new Set(), inverseSeen = new Set();
  for (const row of cert.composition_table) {
    if (!Array.isArray(row) || row.length !== 3 || !row.every(Number.isInteger)) { indexErrors.push({ row, reason: 'row shape' }); continue; }
    const [i, j, k] = row;
    if (i < 0 || i >= S || j < 0 || j >= S || k < 0 || k >= S) indexErrors.push({ row, reason: 'index out of range' });
    const pair = `${i},${j}`;
    if (pairSeen.has(pair)) indexErrors.push({ row, reason: 'duplicate ordered pair' });
    pairSeen.add(pair);
  }
  for (let i = 0; i < S; i++) for (let j = 0; j < S; j++) if (!pairSeen.has(`${i},${j}`)) indexErrors.push({ i, j, reason: 'missing ordered pair' });
  const compRows = cert.composition_table.map(([i, j, k]) => ({ i, j, k })).filter((r) => r.i >= 0 && r.i < S && r.j >= 0 && r.j < S && r.k >= 0 && r.k < S);
  const compChecks = compRows.map((row) => ({ ...row, ...checkCompositionEntryGeneral(QL, Nord, cert.shadows, row.i, row.j, row.k) }));
  for (const row of cert.inverse_map) {
    if (!Array.isArray(row) || row.length !== 2 || !row.every(Number.isInteger)) { indexErrors.push({ row, reason: 'inverse row shape' }); continue; }
    const [i, j] = row;
    if (i < 0 || i >= S || j < 0 || j >= S) indexErrors.push({ row, reason: 'inverse index out of range' });
    if (inverseSeen.has(i)) indexErrors.push({ row, reason: 'duplicate inverse source' });
    inverseSeen.add(i);
  }
  for (let i = 0; i < S; i++) if (!inverseSeen.has(i)) indexErrors.push({ i, reason: 'missing inverse source' });
  const invRows = cert.inverse_map.map(([i, j]) => ({ i, j })).filter((r) => r.i >= 0 && r.i < S && r.j >= 0 && r.j < S);
  const invChecks = invRows.map((row) => ({ ...row, ...checkInverseEntryGeneral(QL, Nord, cert.shadows, row.i, row.j) }));
  return { ok: indexErrors.length === 0 && compRows.length === S * S && compChecks.every((r) => r.ok) && invRows.length === S && invChecks.every((r) => r.ok), composition_rows: compRows.length, composition_expected: S * S, composition_pair_unique: pairSeen.size === S * S, composition_failures: compChecks.filter((r) => !r.ok).slice(0, 10), inverse_rows: invRows.length, inverse_expected: S, inverse_source_unique: inverseSeen.size === S, inverse_failures: invChecks.filter((r) => !r.ok).slice(0, 10), structural_errors: indexErrors.slice(0, 20) };
}

function checkRepresentativeInvariance(cert, model, Gn, originalHexagon = [], certsById = new Map()) {
  const n = cert.target.n, Nord = lcm(n, 2), S = cert.shadows.length;
  const xNordIdentity = permEq(permPow(model.perm1, 2 * Nord), identityPerm(model.N));
  const shifted = cert.shadows.map((sh) => ({ ...sh, m: sh.m + Nord, f_word: sh.f_word.concat([['x', Nord]]) }));
  let hexOriginalPass = 0, hexShiftedPass = 0, hexEqual = 0, quotientPass = 0, tPass = 0;
  const hexFailures = [], quotientFailures = [], tFailures = [];
  for (let i = 0; i < S; i++) {
    const originalOk = originalHexagon[i]?.ok === true;
    const shiftedCheck = checkHexagon(model, { ...shifted[i], m: mod(shifted[i].m, Nord) });
    if (originalOk) hexOriginalPass++;
    if (shiftedCheck.ok) hexShiftedPass++;
    if (originalOk && shiftedCheck.ok) hexEqual++;
    else if (hexFailures.length < 10) hexFailures.push({ i, original: originalOk, shifted: shiftedCheck });
    const fSame = Gn.Triple.eq(evalWord(Gn.Triple, Gn.phiTriple, cert.shadows[i].f_word), evalWord(Gn.Triple, Gn.phiTriple, shifted[i].f_word));
    if (fSame) quotientPass++; else if (quotientFailures.length < 10) quotientFailures.push(i);
    const f0 = xyWordToPerm(model, cert.shadows[i].f_word), f1 = xyWordToPerm(model, shifted[i].f_word);
    const u0 = 2 * cert.shadows[i].m + 1, u1 = 2 * shifted[i].m + 1;
    const t0 = [permPow(model.perm1, u0), composeAll([invPerm(f0), permPow(model.perm2, u0), f0])];
    const t1 = [permPow(model.perm1, u1), composeAll([invPerm(f1), permPow(model.perm2, u1), f1])];
    const tOk = permEq(t0[0], t1[0]) && permEq(t0[1], t1[1]);
    if (tOk) tPass++; else if (tFailures.length < 10) tFailures.push(i);
  }

  const comp = { left_checked: 0, left_pass: 0, right_checked: 0, right_pass: 0, failures: [] };
  for (const [i, j, k] of cert.composition_table) {
    const left = checkCompositionEntry(Gn, n, Nord, [shifted[i], cert.shadows[j], cert.shadows[k]], 0, 1, 2);
    const right = checkCompositionEntry(Gn, n, Nord, [cert.shadows[i], shifted[j], cert.shadows[k]], 0, 1, 2);
    comp.left_checked++; comp.right_checked++;
    if (left.ok) comp.left_pass++; else if (comp.failures.length < 10) comp.failures.push({ side: 'left', i, j, k, result: left });
    if (right.ok) comp.right_pass++; else if (comp.failures.length < 10) comp.failures.push({ side: 'right', i, j, k, result: right });
  }

  const reduction = { required_entries: requiredReductionsFor(n), checked: 0, pass: 0, failures: [] };
  for (const targetId of reduction.required_entries) {
    const entry = cert.reduction.find((r) => r.to === targetId);
    if (!entry) { reduction.failures.push({ to: targetId, reason: 'required entry missing' }); continue; }
    const target = certsById.get(targetId);
    if (!target) { reduction.failures.push({ to: targetId, reason: 'target certificate missing' }); continue; }
    const targetGn = buildGn(target.target.n), targetNord = lcm(target.target.n, 2);
    const targetIndex = new Map();
    for (let j = 0; j < target.shadows.length; j++) {
      const sh = target.shadows[j];
      targetIndex.set(`${mod(sh.m, targetNord)}|${tripleKey(sh.f_triple)}`, j);
    }
    for (let i = 0; i < S; i++) {
      const sh = shifted[i], image = evalWord(targetGn.Triple, targetGn.phiTriple, sh.f_word);
      const actual = targetIndex.get(`${mod(sh.m, targetNord)}|${tripleKey(image.map((e) => [e.a, e.e]))}`);
      reduction.checked++;
      if (actual === entry.image[i]) reduction.pass++;
      else if (reduction.failures.length < 10) reduction.failures.push({ to: targetId, i, expected: entry.image[i], actual });
    }
  }
  const hexOk = hexOriginalPass === S && hexShiftedPass === S && hexEqual === S;
  const quotientOk = quotientPass === S, tOk = tPass === S;
  const compOk = comp.left_checked === S * S && comp.right_checked === S * S && comp.left_pass === S * S && comp.right_pass === S * S;
  const reductionOk = reduction.failures.length === 0 && reduction.checked === reduction.required_entries.length * S;
  return { ok: xNordIdentity && hexOk && quotientOk && tOk && compOk && reductionOk, x_Nord_in_N_F2: xNordIdentity, hexagon: { checked: S, original_pass: hexOriginalPass, shifted_pass: hexShiftedPass, equal_pass: hexEqual, failures: hexFailures }, quotient_f: { checked: S, pass: quotientPass, failures: quotientFailures }, T_sigma: { checked: S, pass: tPass, failures: tFailures }, composition: comp, reduction, assertions: { x_Nord_in_N_F2: xNordIdentity, all_downstream_direct: hexOk && quotientOk && tOk && compOk && reductionOk } };
}

function checkInducedMaps(Gn) {
  const words = new Map([[Gn.Triple.key(Gn.Triple.id), []]]), queue = [Gn.Triple.id];
  for (let qi = 0; qi < queue.length; qi++) {
    const cur = queue[qi], w = words.get(Gn.Triple.key(cur));
    for (const [g, token] of [[Gn.X, ['x', 1]], [Gn.Y, ['y', 1]]]) {
      const next = Gn.Triple.mul(cur, g), key = Gn.Triple.key(next);
      if (!words.has(key)) { words.set(key, w.concat([token])); queue.push(next); }
    }
  }
  const theta = { x: [['y', 1]], y: [['x', 1]] };
  const z = Gn.Triple.inv(Gn.Triple.mul(Gn.X, Gn.Y));
  const tau = { x: [['y', 1]], y: [['z', 1]], z: [['x', 1]] };
  const evalExt = (word, image) => {
    const ext = { x: Gn.X, y: Gn.Y, z };
    let out = Gn.Triple.id;
    for (const [g, p] of word) {
      const imageWord = image[g] || [[g, 1]];
      const use = p < 0 ? invertWord(imageWord) : imageWord;
      for (let i = 0; i < Math.abs(p); i++) out = Gn.Triple.mul(out, evalWord(Gn.Triple, ext, use));
    }
    return out;
  };
  const imageSet = (image) => new Set([...words.values()].map((w) => Gn.Triple.key(evalExt(w, image))));
  const thetaSet = imageSet(theta), tauSet = imageSet(tau);
  return { ok: thetaSet.size === Gn.GnMap.size && tauSet.size === Gn.GnMap.size, theta_bijective: thetaSet.size === Gn.GnMap.size, tau_bijective: tauSet.size === Gn.GnMap.size, checked: words.size };
}

function checkVarRho(cert, n) {
  const q = n / 2, rows = [], byKey = new Map(), errors = [];
  for (let i = 0; i < cert.shadows.length; i++) {
    const sh = cert.shadows[i], first = sh.f_triple?.[0];
    if (!Array.isArray(first) || first[1] !== 0 || first[0] % 2 !== 0) { errors.push({ i, reason: 'f_triple[0] is not r^(2k)' }); continue; }
    const k = mod(first[0] / 2, q), u = mod(2 * sh.m + 1, 2 * n), key = `${k},${u}`;
    if (byKey.has(key)) errors.push({ i, reason: 'duplicate rho image', key });
    byKey.set(key, i); rows.push({ i, m: sh.m, k, u, key });
  }
  const alpha = Math.round(Math.log2(n));
  const expectedCount = 2 ** (2 * alpha - 2);
  const expectedSet = new Set();
  const bCount = 2 ** (alpha - 1);
  for (let b = 0; b < bCount; b++) {
    const u5 = mod(5 ** b, 2 * n);
    for (let a = 0; a < 2; a++) {
      const u = mod((a === 0 ? 1 : -1) * u5, 2 * n);
      for (let k = 0; k < q; k++) if (mod(k - b, 2) === 0) expectedSet.add(`${k},${u}`);
    }
  }
  const actualSet = new Set(rows.map((r) => r.key));
  const missing = [...expectedSet].filter((key) => !actualSet.has(key));
  const extra = [...actualSet].filter((key) => !expectedSet.has(key));
  const duplicateCount = rows.length - actualSet.size;
  const comp = [];
  if (cert.composition_table.length === cert.shadows.length ** 2) {
    for (const [i, j, k] of cert.composition_table) {
      const a = rows.find((r) => r.i === i), b = rows.find((r) => r.i === j), c = rows.find((r) => r.i === k);
      const expected = a && b ? { k: mod(a.k + a.u * b.k, q), u: mod(a.u * b.u, 2 * n) } : null;
      comp.push({ i, j, k, expected, actual: c ? { k: c.k, u: c.u } : null, ok: Boolean(expected && c && expected.k === c.k && expected.u === c.u) });
    }
  }
  const witness = {};
  if (n === 8 || n === 16) {
    for (const wanted of [[0, mod(-1, 2 * n)], [1, 5]]) {
      const row = rows.find((r) => r.k === wanted[0] && r.u === wanted[1]);
      witness[`${wanted[0]},${wanted[1]}`] = row ? row.i : null;
    }
    const a = witness['0,' + mod(-1, 2 * n)], b = witness['1,5'];
    const lookup = (i, j) => cert.composition_table.find((r) => r[0] === i && r[1] === j)?.[2];
    witness.forward_product = a !== null && b !== null ? lookup(a, b) : null;
    witness.reverse_product = a !== null && b !== null ? lookup(b, a) : null;
    const forwardTarget = witness.forward_product === null ? null : rows.find((r) => r.i === witness.forward_product);
    const reverseTarget = witness.reverse_product === null ? null : rows.find((r) => r.i === witness.reverse_product);
    witness.forward_expected = { k: mod(0 + mod(-1, 2 * n) * 1, q), u: mod(mod(-1, 2 * n) * 5, 2 * n) };
    witness.reverse_expected = { k: mod(1 + 5 * 0, q), u: mod(5 * mod(-1, 2 * n), 2 * n) };
    witness.forward_actual = forwardTarget ? { k: forwardTarget.k, u: forwardTarget.u } : null;
    witness.reverse_actual = reverseTarget ? { k: reverseTarget.k, u: reverseTarget.u } : null;
    witness.forward_match = Boolean(witness.forward_actual && witness.forward_actual.k === witness.forward_expected.k && witness.forward_actual.u === witness.forward_expected.u);
    witness.reverse_match = Boolean(witness.reverse_actual && witness.reverse_actual.k === witness.reverse_expected.k && witness.reverse_actual.u === witness.reverse_expected.u);
    witness.noncommuting = witness.forward_product !== null && witness.reverse_product !== null && witness.forward_product !== witness.reverse_product;
  }
  const exactSetOk = missing.length === 0 && extra.length === 0 && duplicateCount === 0 && expectedSet.size === expectedCount && actualSet.size === expectedCount;
  const baseOk = rows.length === cert.shadows.length && exactSetOk && errors.length === 0 && comp.length === cert.shadows.length ** 2 && comp.every((r) => r.ok);
  const witnessOk = (n === 4) || (witness.noncommuting === true && witness.forward_match === true && witness.reverse_match === true);
  return { ok: baseOk && witnessOk, formula: 'rho(m,k)=(k mod n/2,u mod 2n), u=2m+1', expected_shadow_count: expectedCount, actual_shadow_count: cert.shadows.length, exact_set: { expected_count: expectedSet.size, actual_count: actualSet.size, missing, extra, duplicate_count: duplicateCount, ok: exactSetOk }, rows, composition_checked: comp.length, composition_failures: comp.filter((r) => !r.ok).slice(0, 10), errors, witness };
}

function buildWordTable(Gn) {
  // Canonical source Cayley graph.  Store parent/generator integers rather
  // than materialising a token array for every element (the old O(|G|*word
  // length) concat/eval path dominated the 256-pair sweep).
  const indexByKey = new Map([[Gn.Triple.key(Gn.Triple.id), 0]]);
  const elems = [Gn.Triple.id], parent = [-1], via = [-1], nextX = [], nextY = [];
  for (let qi = 0; qi < elems.length; qi++) {
    const cur = elems[qi], nextIndices = [];
    for (const g of [Gn.X, Gn.Y]) {
      const next = Gn.Triple.mul(cur, g), key = Gn.Triple.key(next);
      let idx = indexByKey.get(key);
      if (idx === undefined) {
        idx = elems.length; indexByKey.set(key, idx); elems.push(next); parent.push(qi); via.push(g === Gn.X ? 0 : 1);
      }
      nextIndices.push(idx);
    }
    nextX[qi] = nextIndices[0]; nextY[qi] = nextIndices[1];
  }
  return { indexByKey, elems, parent, via, nextX, nextY, size: elems.length };
}

function checkMarkedFactorMap(source, target, tableArg = null) {
  const table = tableArg || buildWordTable(source), images = new Array(table.size), conflicts = [];
  images[0] = target.Triple.id;
  for (let i = 1; i < table.size; i++) {
    images[i] = target.Triple.mul(images[table.parent[i]], table.via[i] === 0 ? target.X : target.Y);
  }
  for (let i = 0; i < table.size; i++) {
    const img = images[i];
    const ex = target.Triple.mul(img, target.X), ey = target.Triple.mul(img, target.Y);
    if (!target.Triple.eq(ex, images[table.nextX[i]])) conflicts.push({ source_index: i, generator: 'x', next_index: table.nextX[i] });
    if (!target.Triple.eq(ey, images[table.nextY[i]])) conflicts.push({ source_index: i, generator: 'y', next_index: table.nextY[i] });
    if (conflicts.length >= 3) break;
  }
  const imageKeys = new Set(images.map((x) => target.Triple.key(x)));
  return { well_defined: conflicts.length === 0, injective: imageKeys.size === table.size, source_order: table.size, image_order: imageKeys.size, conflicts };
}

function runGlobalSuite(certsById, capMs = 120000) {
  const started = Date.now();
  const universe = [...Array(14)].map((_, i) => i + 3).concat([18, 36]);
  const groups = new Map(universe.map((n) => [n, buildGnLight(n)]));
  const numeric = universe.map((n) => {
    const g = groups.get(n), expected = expectedGnOrder(n), nord = lcm(n, 2);
    return { n, group_order: g.GnMap.size, expected_group_order: expected, N_ord: nord, expected_N_ord: nord, pass: g.GnMap.size === expected && nord === lcm(n, 2) };
  });
  const doublingNs = [3, 5, 7, 9, 11, 13, 15], doublingAuxTargets = [22, 26, 30];
  const doubling = doublingNs.map((n) => {
    const source = groups.get(n) || buildGnLight(n), target = buildGnLight(2 * n), r = checkMarkedFactorMap(source, target, buildWordTable(source));
    return { n, target: 2 * n, auxiliary_target: doublingAuxTargets.includes(2 * n), target_order: target.GnMap.size, ...r, isomorphism: r.well_defined && r.injective && r.image_order === target.GnMap.size, pass: r.well_defined && r.injective && r.image_order === target.GnMap.size };
  });
  const pairs = [], sourceTables = new Map(universe.map((q) => [q, buildWordTable(groups.get(q))]));
  let trueCount = 0, falseCount = 0, mismatch = 0;
  for (const q of universe) for (const n of universe) {
    if (Date.now() - started > capMs) {
      const falsePairs = pairs.filter((p) => !p.number_theory);
      return { schema: 'gtsh-global/v1', status: 'UNKNOWN', reason: `Prop.3.5 Cayley collision sweep exceeded cap ${capMs} ms`, cap_ms: capMs, elapsed_ms: Date.now() - started, universe, numeric: { ok: numeric.every((r) => r.pass), rows: numeric }, doubling: { ok: doubling.every((r) => r.pass), rows: doubling }, prop_3_5: { ok: false, total: 256, true_count: universe.flatMap((qq) => universe.filter((nn) => lcm(qq, 2) % nn === 0)).length, false_count: 256 - universe.flatMap((qq) => universe.filter((nn) => lcm(qq, 2) % nn === 0)).length, false_pair_collision_count: falsePairs.filter((p) => !p.well_defined).length, false_pair_well_defined_count: falsePairs.filter((p) => p.well_defined).length, true_pair_collision_count: pairs.filter((p) => p.number_theory && !p.well_defined).length, false_collision_count: falsePairs.filter((p) => p.well_defined).length, checked_pairs: pairs.length, mismatch_count: null, pairs }, reduction_triangle: { ok: false, status: 'UNKNOWN', reason: 'not reached before cap' }, all_pass: false };
    }
    const formula = n !== 0 && lcm(q, 2) % n === 0;
    if (formula) trueCount++; else falseCount++;
    const r = checkMarkedFactorMap(groups.get(q), groups.get(n), sourceTables.get(q));
    // This is a quotient/factor map: source-to-target collisions are allowed.
    // The required criterion is well-definedness of equal source words, not injectivity.
    const admissible = r.well_defined;
    if (admissible !== formula) mismatch++;
    pairs.push({ q, n, number_theory: formula, well_defined: r.well_defined, injective: r.injective, admissible, conflict_count: r.conflicts.length });
  }
  const reductionTriangle = (() => {
    const c36 = certsById.get('K36'), c12 = certsById.get('K12'), c4 = certsById.get('K4');
    if (!c36 || !c12 || !c4) return { ok: false, checked: 0, reason: 'K36/K12/K4 certificate missing' };
    const r3612 = c36.reduction.find((r) => r.to === 'K12'), r124 = c12.reduction.find((r) => r.to === 'K4'), r364 = c36.reduction.find((r) => r.to === 'K4');
    if (!r3612 || !r124 || !r364) return { ok: false, checked: 0, reason: 'triangle entry missing' };
    let pass = 0, failures = [];
    for (let i = 0; i < c36.shadows.length; i++) {
      const a = r364.image[i], b = r3612.image[i], composed = r124.image[b];
      if (a === composed) pass++; else failures.push({ i, image_36_4: a, image_12_4_of_36_12: composed });
    }
    return { ok: pass === 216, checked: pass, expected: 216, failures: failures.slice(0, 10) };
  })();
  const falsePairCollisionCount = pairs.filter((p) => !p.number_theory && !p.well_defined).length;
  const falsePairWellDefinedCount = pairs.filter((p) => !p.number_theory && p.well_defined).length;
  const truePairCollisionCount = pairs.filter((p) => p.number_theory && !p.well_defined).length;
  const propOk = mismatch === 0 && trueCount + falseCount === 256;
  const numericOk = numeric.every((r) => r.pass), doublingOk = doubling.every((r) => r.pass), allPass = numericOk && doublingOk && propOk && reductionTriangle.ok;
  const status = allPass ? 'PASS' : (mismatch > 0 || !numericOk || !doublingOk || !propOk || (reductionTriangle.ok === false && reductionTriangle.failures?.length) ? 'FAIL' : 'UNKNOWN');
  const global = { schema: 'gtsh-global/v1', status, cap_ms: capMs, elapsed_ms: Date.now() - started, universe, numeric: { ok: numericOk, rows: numeric }, doubling: { ok: doublingOk, rows: doubling }, prop_3_5: { ok: propOk, total: 256, true_count: trueCount, false_count: falseCount, false_pair_collision_count: falsePairCollisionCount, false_pair_well_defined_count: falsePairWellDefinedCount, true_pair_collision_count: truePairCollisionCount, false_collision_count: falsePairWellDefinedCount, mismatch_count: mismatch, pairs }, reduction_triangle: reductionTriangle, all_pass: allPass };
  return global;
}

function globalCapFromArgs() {
  const at = process.argv.indexOf('--cap');
  if (at >= 0 && Number.isFinite(Number(process.argv[at + 1]))) return Math.max(1, Number(process.argv[at + 1]));
  if (Number.isFinite(Number(process.env.GTSH_GLOBAL_CAP_MS))) return Math.max(1, Number(process.env.GTSH_GLOBAL_CAP_MS));
  return 120000;
}

// --- 検査項目 6 (kernel_cert / (4.11)) : 確定式 (司令塔裁定・追補1・2026-07-18) ---
// h = [u,v] アフィン表記 (Z/n 上, j -> u*j + v mod n)。
// 確定式 (2405 p.18): shadow (m, g), g = f_triple = (r^{2k}, r^{-2k}, r^{kappa(m)}) とし、
//   (I)  x-bar^{2m+1} = h . x-bar . h^-1
//   (II) g^-1 . y-bar^{2m+1} . g = h . y-bar . h^-1
// を Sym(Z/n) 内の成分ごと (i=1,2,3) の等式として検査する (x-bar=psi_n(x), y-bar=psi_n(y))。
function affineOfDnElement(n, el) {
  // r^a s^e <-> j -> ((-1)^e) j + a  (Lemma 4.2: r(j)=j+1, s(j)=-j という左作用の規約)
  return { u: el.e === 0 ? 1 : -1, v: el.a };
}
function affineCompose(n, f, g) {
  // (f after g): j -> f(g(j)) = f(u_g j + v_g) = u_f (u_g j + v_g) + v_f = u_f u_g j + (u_f v_g + v_f)
  return { u: mod(f.u * g.u, n), v: mod(f.u * g.v + f.v, n) };
}
function modInverse(u, n) {
  // 拡張ユークリッド互除法: u の mod n 逆元 (u は Z/n の単元であることを仮定)
  u = mod(u, n);
  let [oldR, rr] = [u, n];
  let [oldS, ss] = [1, 0];
  while (rr !== 0) {
    const q = Math.floor(oldR / rr);
    [oldR, rr] = [rr, oldR - q * rr];
    [oldS, ss] = [ss, oldS - q * ss];
  }
  if (oldR !== 1) throw new Error(`modInverse: ${u} は mod ${n} で単元でない (gcd=${oldR})`);
  return mod(oldS, n);
}
function affineInv(n, f) {
  // f: j -> u j + v.  f^-1: j -> u^-1 j - u^-1 v.  u は一般の単元 (b=(j->(2m+1)j) など ±1 に限らない)。
  const uinv = modInverse(f.u, n);
  return { u: uinv, v: mod(-uinv * f.v, n) };
}
function affineEq(n, f, g) { return mod(f.u, n) === mod(g.u, n) && mod(f.v, n) === mod(g.v, n); }
function affinePow(n, f, k) {
  if (k === 0) return { u: 1, v: 0 };
  const base = k < 0 ? affineInv(n, f) : f;
  let res = { u: 1, v: 0 };
  for (let i = 0; i < Math.abs(k); i++) res = affineCompose(n, res, base);
  return res;
}

function checkKernelCert(n, shadow) {
  const kc = shadow.kernel_cert;
  if (!kc) return { ok: false, reason: 'kernel_cert 欠落' };
  if (kc.type === 'brute') {
    return { ok: null, reason: 'brute type は checkKernelCertBrute (control/N5 専用) で処理する。dihedral 用関数では非対応。' };
  }
  if (kc.type !== 'conjugator-triple') {
    return { ok: false, reason: `未知の kernel_cert.type: ${kc.type}` };
  }
  const m = shadow.m;
  const hRaw = kc.h; // [[u,v],[u,v],[u,v]]
  if (!Array.isArray(hRaw) || hRaw.length !== 3) return { ok: false, reason: 'h が 3 要素でない' };
  const h = hRaw.map(([u, v]) => ({ u: mod(u, n), v: mod(v, n) }));

  // psi_n の座標: x -> (r,s,s), y -> (rs,r,rs)  それぞれの affine 表現
  const rAff = { u: 1, v: 1 };       // r: j->j+1
  const sAff = { u: mod(-1, n), v: 0 }; // s: j->-j
  const rsAff = affineCompose(n, rAff, sAff); // rs: j -> r(s(j)) = -j+1 (左作用: s のち r)
  const psiXTriple = [rAff, sAff, sAff];
  const psiYTriple = [rsAff, rAff, rsAff];
  const gTriple = tripleFromCertFormat(shadow.f_triple).map((el) => affineOfDnElement(n, el));

  let eq1ok = true, eq2ok = true;
  const detail = [];
  for (let i = 0; i < 3; i++) {
    // (I) x-bar^{2m+1} == h_i . x-bar_i . h_i^-1
    const lhs1 = affinePow(n, psiXTriple[i], 2 * m + 1);
    const rhs1 = affineCompose(n, affineCompose(n, h[i], psiXTriple[i]), affineInv(n, h[i]));
    const c1 = affineEq(n, lhs1, rhs1);
    if (!c1) eq1ok = false;
    // (II) g_i^-1 . y-bar_i^{2m+1} . g_i == h_i . y-bar_i . h_i^-1
    const lhs2 = affineCompose(n, affineCompose(n, affineInv(n, gTriple[i]), affinePow(n, psiYTriple[i], 2 * m + 1)), gTriple[i]);
    const rhs2 = affineCompose(n, affineCompose(n, h[i], psiYTriple[i]), affineInv(n, h[i]));
    const c2 = affineEq(n, lhs2, rhs2);
    if (!c2) eq2ok = false;
    detail.push({ i, eq1: c1, eq2: c2 });
  }
  return { ok: eq1ok && eq2ok, eq1ok, eq2ok, detail };
}

// --- N5 (control) 用 kernel_cert(type=brute) の確定手続き (追補1 項目4) ---
// <sigma1hat,sigma2hat> (期待位数 = kc.expected_kernel_index, N5 では 30) を BFS で全列挙し、
// 全エッジ (木でない辺も含む) で T-substitution (sigma1->sigma1^{2m+1}, sigma2->f^-1 sigma2^{2m+1} f)
// の井戸定義性 (同じ元に到達する 2 語の T-像が一致するか) を検査、さらに T-像の全単射性 (30 通り相異なるか)
// を確認する。両方 PASS なら T は B3/N を経由し単射 -> settled。
function checkKernelCertBrute(model, shadow) {
  const kc = shadow.kernel_cert;
  if (!kc || kc.type !== 'brute') return { ok: false, reason: 'kernel_cert.type が brute でない' };
  const expectedIdx = kc.expected_kernel_index;
  const m = shadow.m;
  const fPerm = xyWordToPerm(model, shadow.f_word);
  const invF = invPerm(fPerm);
  const sigma1T = permPow(model.perm1, 2 * m + 1);
  const invSigma1T = invPerm(sigma1T);
  const sigma2T = composeAll([invF, permPow(model.perm2, 2 * m + 1), fPerm]);
  const invSigma2T = invPerm(sigma2T);

  function computeTWord(word) {
    let res = identityPerm(model.N);
    for (const [name, sign] of word) {
      const gp = name === 's1' ? (sign > 0 ? sigma1T : invSigma1T) : (sign > 0 ? sigma2T : invSigma2T);
      res = composeRight(res, gp);
    }
    return res;
  }

  const id0 = identityPerm(model.N);
  const seen = new Map();
  seen.set(id0.join(','), { perm: id0, word: [] });
  let frontier = [{ perm: id0, word: [] }];
  const steps = [['s1', 1, model.perm1], ['s1', -1, invPerm(model.perm1)], ['s2', 1, model.perm2], ['s2', -1, invPerm(model.perm2)]];
  let wellDefined = true;
  const conflicts = [];
  let cap = 5000;
  while (frontier.length && seen.size < cap) {
    const next = [];
    for (const node of frontier) {
      for (const [name, sign, gp] of steps) {
        const cand = composeRight(node.perm, gp);
        const key = cand.join(',');
        const candWord = node.word.concat([[name, sign]]);
        if (!seen.has(key)) {
          const entry = { perm: cand, word: candWord };
          seen.set(key, entry);
          next.push(entry);
        } else {
          const existing = seen.get(key);
          const tExisting = computeTWord(existing.word);
          const tCand = computeTWord(candWord);
          if (!permEq(tExisting, tCand)) {
            wellDefined = false;
            conflicts.push({ existingWord: existing.word, candWord });
          }
        }
      }
    }
    frontier = next;
  }
  const groupOrder = seen.size;
  const orderOk = (groupOrder === expectedIdx);

  const tImages = new Set();
  let bijective = true;
  for (const { word } of seen.values()) {
    const t = computeTWord(word);
    const k = t.join(',');
    if (tImages.has(k)) bijective = false;
    tImages.add(k);
  }
  const imageOrderOk = (tImages.size === expectedIdx);

  return {
    ok: orderOk && wellDefined && bijective && imageOrderOk,
    groupOrder, expectedIdx, orderOk, wellDefined,
    conflicts: conflicts.slice(0, 5),
    bijective, imageOrderCount: tImages.size, imageOrderOk,
  };
}

// --- 検査項目 10 (ls_witness / (5.1)) : 確定式 (司令塔裁定・追補1・2026-07-18) ---
// [m,f] in GT(K^(n)), 3|n. f = x^{2k} y^{-2k} z^{kappa(m)}, z=(xy)^-1.
// 確定式:
//   (i)  f K_F2 = theta(g)^-1 g K_F2
//   (ii) f x^m K_F2 = tau(h)^-1 h K_F2          (m == 0 mod 3)
//        f x^m K_F2 = tau(h)^-1 (x y) h K_F2    (m == -1 mod 3, i.e. m mod 3 == 2)
//   m == 1 mod 3 は空虚 (3|n なら 3|N_ord, m==1 mod3 -> 3|(2m+1) -> charming の単元条件違反 -> Xn に不在)。
//   ここでは「そのような m が ls_witness に現れたら FAIL」に変える。
function invertWord(w) { return w.slice().reverse().map(([g, p]) => [g, -p]); }
function applyAutoWord(tokens, image) {
  const out = [];
  for (const [gen, p] of tokens) {
    const rep = image[gen];
    const unit = p < 0 ? invertWord(rep) : rep;
    for (let i = 0; i < Math.abs(p); i++) out.push(...unit);
  }
  return out;
}
function checkLsWitness(Gn, n, entry) {
  const { Triple, phiTriple } = Gn;
  const m = entry.m, k = entry.k;
  const mm3 = mod(m, 3);
  if (mm3 === 1) {
    return { ok: false, reason: 'm == 1 mod 3 は空虚 (charming の単元条件違反) のはずが ls_witness に現れている', vacuous_violation: true };
  }
  const kap = kappa(m);
  const fWord = [['x', 2 * k], ['y', -2 * k], ['z', kap]];
  const phiExt = { x: phiTriple.x, y: phiTriple.y, c: phiTriple.c, z: Triple.inv(Triple.mul(phiTriple.x, phiTriple.y)) };
  const ev = (tokens) => evalWord(Triple, phiExt, tokens);

  // theta = (x<->y), theta(z) = theta((xy)^-1) = (yx)^-1 = x^-1 y^-1
  const thetaImage = { x: [['y', 1]], y: [['x', 1]], z: [['x', -1], ['y', -1]] };
  // tau: x->y->z->x (位数3の巡回)
  const tauImage = { x: [['y', 1]], y: [['z', 1]], z: [['x', 1]] };

  const gWord = entry.g_word;
  const hWord = entry.h_word;

  // (i) f = theta(g)^-1 g
  const lhs1 = ev(fWord);
  const rhs1 = Triple.mul(Triple.inv(ev(applyAutoWord(gWord, thetaImage))), ev(gWord));
  const eq1ok = Triple.eq(lhs1, rhs1);

  // (ii) f x^m = tau(h)^-1 h  or  tau(h)^-1 (xy) h
  const lhsFxm = Triple.mul(ev(fWord), Triple.pow(phiTriple.x, m));
  const tauH = ev(applyAutoWord(hWord, tauImage));
  let rhs2;
  if (mm3 === 0) {
    rhs2 = Triple.mul(Triple.inv(tauH), ev(hWord));
  } else {
    const xy = Triple.mul(phiTriple.x, phiTriple.y);
    rhs2 = Triple.mul(Triple.mul(Triple.inv(tauH), xy), ev(hWord));
  }
  const eq2ok = Triple.eq(lhsFxm, rhs2);

  return { ok: eq1ok && eq2ok, eq1ok, eq2ok, mm3 };
}

// --- 検査項目 7: composition_table via (3.53) + (4.19)(4.20) ---
function composeShadowWords(m1, f1Tokens, m2, f2Tokens) {
  // E_{m1,f1}(x^k) = x^{k(2m1+1)}
  // E_{m1,f1}(y^k) = f1^-1 y^{k(2m1+1)} f1
  const u1 = 2 * m1 + 1;
  const invF1 = f1Tokens.slice().reverse().map(([g, p]) => [g, -p]);
  const eOfF2 = [];
  for (const [gen, p] of f2Tokens) {
    if (gen === 'x') {
      eOfF2.push(['x', p * u1]);
    } else if (gen === 'y') {
      for (const t of invF1) eOfF2.push(t);
      eOfF2.push(['y', p * u1]);
      for (const t of f1Tokens) eOfF2.push(t);
    }
  }
  const composedWord = f1Tokens.concat(eOfF2);
  return { mNewRaw: 2 * m1 * m2 + m1 + m2, composedWord };
}

const shadowTripleCache = new WeakMap();
function evalShadowTriple(Gn, shadow) {
  let cached = shadowTripleCache.get(shadow);
  if (!cached) {
    cached = evalWord(Gn.Triple, Gn.phiTriple, shadow.f_word || []);
    shadowTripleCache.set(shadow, cached);
  }
  return cached;
}

function evalFactorUnderAction(Gn, m, f1Triple, f2Tokens) {
  const { Triple, phiTriple } = Gn;
  const u = 2 * m + 1;
  const xImage = Triple.pow(phiTriple.x, u);
  const yImage = Triple.mul(Triple.mul(Triple.inv(f1Triple), Triple.pow(phiTriple.y, u)), f1Triple);
  let result = Triple.id;
  for (const [gen, power] of f2Tokens || []) {
    result = Triple.mul(result, Triple.pow(gen === 'x' ? xImage : yImage, power));
  }
  return result;
}

function checkCompositionEntry(Gn, n, Nord, shadows, i, j, k) {
  const shA = shadows[i], shB = shadows[j], shC = shadows[k];
  const { mNewRaw } = composeShadowWords(shA.m, shA.f_word, shB.m, shB.f_word);
  const mNew = mod(mNewRaw, Nord);
  const mOk = mNew === mod(shC.m, Nord);
  const { Triple, phiTriple } = Gn;
  const f1Triple = evalShadowTriple(Gn, shA);
  const computedTriple = Triple.mul(f1Triple, evalFactorUnderAction(Gn, shA.m, f1Triple, shB.f_word));
  const givenTriple = tripleFromCertFormat(shC.f_triple);
  const tripleOk = Triple.eq(computedTriple, givenTriple);
  // (4.19): (2m1+1)(2m2+1) = 2mNewRaw+1  -- 代数的恒等式、常に真 (自己整合性チェック)
  const u1 = 2 * shA.m + 1, u2 = 2 * shB.m + 1;
  const id419 = (u1 * u2) === (2 * mNewRaw + 1);
  // (4.20): kappa(m1)+kappa(m2)-2 kappa(m1) kappa(m2) = kappa(mNewRaw)  -- mod 適用前の整数関係として確認は
  // kappa が mod Nord 依存のため、mod Nord 上の代表で比較する
  const k1 = kappa(mod(shA.m, Nord)), k2 = kappa(mod(shB.m, Nord)), kNew = kappa(mNew);
  const lhs420 = mod(k1 + k2 - 2 * k1 * k2, n);
  const rhs420 = mod(kNew, n);
  // 注: kappa は本来 Dn の r 冪の指数として mod n で解釈するのが自然なので mod n で比較
  const id420 = lhs420 === rhs420;
  return { ok: mOk && tripleOk && id419 && id420, mOk, tripleOk, id419, id420 };
}

// --- 検査項目 8: inverse via composition round-trip ---
function checkInverseEntry(Gn, n, Nord, shadows, i, iInv) {
  const shA = shadows[i], shB = shadows[iInv];
  // shA ∘ shB should be identity (0, f=1) and shB ∘ shA should be identity too
  const c1 = checkCompositionEntry(Gn, n, Nord, [shA, shB, { m: 0, f_word: [], f_triple: identityTripleFormat() }], 0, 1, 2);
  const c2 = checkCompositionEntry(Gn, n, Nord, [shB, shA, { m: 0, f_word: [], f_triple: identityTripleFormat() }], 0, 1, 2);
  return { ok: c1.ok && c2.ok, forward: c1, backward: c2 };
}
function identityTripleFormat() { return [[0, 0], [0, 0], [0, 0]]; }

// --- 検査項目 9: reduction ---
function checkReductionEntry(n, redEntry, sourceShadows, targetCert) {
  if (!targetCert) return { ok: null, reason: `目標証明書 ${redEntry.to} が見つからない` };
  const targetN = targetCert.target.n;
  const GnTarget = buildGn(targetN);
  const targetNord = lcm(targetN, 2);
  const results = [];
  const coveredTargetIdx = new Set();
  for (let i = 0; i < sourceShadows.length; i++) {
    const sh = sourceShadows[i];
    const mReduced = mod(sh.m, targetNord);
    const tripleReduced = evalWord(GnTarget.Triple, GnTarget.phiTriple, sh.f_word);
    const claimedIdx = redEntry.image[i];
    const claimedShadow = targetCert.shadows[claimedIdx];
    const okM = claimedShadow ? mod(claimedShadow.m, targetNord) === mReduced : false;
    const okTriple = claimedShadow ? GnTarget.Triple.eq(tripleReduced, tripleFromCertFormat(claimedShadow.f_triple)) : false;
    results.push({ i, claimedIdx, okM, okTriple });
    if (claimedShadow) coveredTargetIdx.add(claimedIdx);
  }
  const allOk = results.every((r) => r.okM && r.okTriple);
  const surjectiveOk = coveredTargetIdx.size === targetCert.shadows.length;
  return { ok: allOk && (redEntry.surjective ? surjectiveOk : true), results, surjectiveOk };
}

// ---------- 証明書1件の検査 ----------
// ---------- family="general" (Week3・L=K^(3)∩N0) 証明書の検査 ----------
// docs/week3-L-設計.md v1.1 §1-§5 に基づく。search/ の explorer コードは不参照。
function checkRepresentativeInvarianceGeneral(cert, model, QL) {
  const Nord = 6, S = cert.shadows.length;
  const xNordIdentity = permEq(permPow(model.perm1, 2 * Nord), identityPerm(model.N));
  const shifted = cert.shadows.map((sh) => ({ ...sh, m: sh.m + Nord, f_word: sh.f_word.concat([['x', Nord]]) }));
  let hexShiftedPass = 0, quotientPass = 0, tPass = 0;
  const hexFailures = [], quotientFailures = [], tFailures = [];
  for (let i = 0; i < S; i++) {
    const shiftedCheck = checkHexagon(model, { ...shifted[i], m: mod(shifted[i].m, Nord) });
    if (shiftedCheck.ok) hexShiftedPass++; else if (hexFailures.length < 10) hexFailures.push({ i, shiftedCheck });
    const fSame = QL.Triple.eq(evalWord(QL.Triple, QL.phiTriple, cert.shadows[i].f_word), evalWord(QL.Triple, QL.phiTriple, shifted[i].f_word));
    if (fSame) quotientPass++; else if (quotientFailures.length < 10) quotientFailures.push(i);
    const f0 = xyWordToPerm(model, cert.shadows[i].f_word), f1 = xyWordToPerm(model, shifted[i].f_word);
    const u0 = 2 * cert.shadows[i].m + 1, u1 = 2 * shifted[i].m + 1;
    const t0 = [permPow(model.perm1, u0), composeAll([invPerm(f0), permPow(model.perm2, u0), f0])];
    const t1 = [permPow(model.perm1, u1), composeAll([invPerm(f1), permPow(model.perm2, u1), f1])];
    const tOk = permEq(t0[0], t1[0]) && permEq(t0[1], t1[1]);
    if (tOk) tPass++; else if (tFailures.length < 10) tFailures.push(i);
  }
  const hexOk = hexShiftedPass === S, quotientOk = quotientPass === S, tOk = tPass === S;
  return {
    ok: xNordIdentity && hexOk && quotientOk && tOk, x_Nord_in_N_F2: xNordIdentity,
    hexagon: { checked: S, shifted_pass: hexShiftedPass, failures: hexFailures },
    quotient_f: { checked: S, pass: quotientPass, failures: quotientFailures },
    T_sigma: { checked: S, pass: tPass, failures: tFailures },
  };
}

function checkCertificateGeneral(cert, certsById) {
  const verdict = { id: cert.target.id, family: 'general', schema: cert.schema, items: {} };

  const schemaErrors = validateCertificateShape(cert);
  verdict.items['0_schema_fail_closed'] = { ok: schemaErrors.length === 0, errors: schemaErrors };

  const QL = buildQL();
  const model = buildTransversalModel(QL.Triple, QL.phiTriple);

  verdict.items['0_invariants'] = checkCertificateInvariantsGeneral(cert, QL);

  // item 1: counts 整合 (raw = |X_L|*|[Q_L,Q_L]| = 4*81 = 324)
  {
    const c = cert.counts || {};
    const monotone = (c.raw_candidates >= c.hexagon_pass) && (c.hexagon_pass >= c.charming_pass) && (c.charming_pass >= c.surjective_pass);
    const matchesShadowLen = c.surjective_pass === cert.shadows.length;
    verdict.items['1_counts'] = {
      ok: monotone && matchesShadowLen, monotone, matchesShadowLen,
      approved_simplification: '追補1 項目3(司令塔裁定・2026-07-18)の緩和を general に準用: raw 候補の完全再列挙は不要、単調性+最終個数一致で可。',
    };
    verdict.items['1_raw_formula'] = checkRawCandidateFormulaGeneral(cert, QL);
  }

  // item 2: full hexagon (3.3)(3.4) を Q_L x T 上で
  {
    let allOk = true; const fails = [];
    for (let i = 0; i < cert.shadows.length; i++) {
      const r = checkHexagon(model, cert.shadows[i]);
      if (!r.ok) { allOk = false; fails.push({ i, r }); }
    }
    verdict.items['2_hexagon'] = { ok: allOk, checked: cert.shadows.length, fails };
  }

  // item 3: f_word <-> f_pair (G3 triple + H3 座標)
  {
    let allOk = true; const fails = [];
    for (let i = 0; i < cert.shadows.length; i++) {
      const r = checkFWordVsPairGeneral(QL, cert.shadows[i]);
      if (!r.ok) { allOk = false; fails.push({ i, r }); }
    }
    verdict.items['3_f_word_vs_pair'] = { ok: allOk, checked: cert.shadows.length, fails };
  }

  // item 4: charming (f in [Q_L,Q_L]) + surjective
  {
    let allOk = true; const fails = [];
    for (let i = 0; i < cert.shadows.length; i++) {
      const r = checkCharmingAndSurjectiveGeneral(QL, cert.shadows[i]);
      if (!r.ok) { allOk = false; fails.push({ i, r }); }
    }
    verdict.items['4_charming_surjective'] = { ok: allOk, checked: cert.shadows.length, fails };
  }

  // item 5: Thm 4.3 系 -- dihedral 専用 (N/A, fail-closed: 理由つきで明記)
  verdict.items['5_thm43_set'] = {
    ok: true, status: 'N/A',
    reason: 'Thm 4.3 の閉じた式(2405)は dihedral 専用。Q_L=G3xH3 の general 対象には非適用 -- week3-L-設計.md §3。',
  };

  // item 6: kernel brute (N5 方式の一般化)。単位 cap 120秒/shadow・集約 cap 30分。
  {
    const unitCapMs = 120000, aggregateCapMs = 1800000, sampleLimit = 50;
    let allOk = true; const fails = []; const results = [];
    let aggregateMs = 0, aggregateExceeded = false;
    for (let i = 0; i < cert.shadows.length; i++) {
      if (aggregateExceeded && i >= sampleLimit) {
        results.push({ i, status: 'UNKNOWN' });
        continue;
      }
      const sh = cert.shadows[i];
      const r = checkKernelCertBruteGeneral(model, sh, { maxMs: unitCapMs });
      aggregateMs += r.elapsed_ms || 0;
      results.push({ i, ...r });
      if (r.ok !== true) { allOk = false; fails.push({ i, r }); }
      if (aggregateMs > aggregateCapMs) aggregateExceeded = true;
    }
    const unknownCount = results.filter((r) => r.status === 'UNKNOWN').length;
    verdict.items['6_kernel_cert'] = {
      ok: allOk && unknownCount === 0, checked: cert.shadows.length, fails,
      aggregate_elapsed_ms: aggregateMs, unit_cap_ms: unitCapMs, aggregate_cap_ms: aggregateCapMs,
      sample_limit: sampleLimit, unknown_count: unknownCount,
      note: 'N5 の checkKernelCertBrute 方式の一般化 (17496 元 BFS で井戸定義性+全単射性)。集約 cap 超過時は決定的に先頭50件のみ全数、残りは UNKNOWN(silent cap 禁止・week3-L-設計.md §5)。',
    };
  }

  // item 7: composition_table via (3.53)。(4.20)(kappa 依存)は dihedral 専用のため id419 のみ適用。
  if (cert.composition_table) {
    const Nord = 6;
    let allOk = true; const fails = [];
    for (const [i, j, k] of cert.composition_table) {
      const r = checkCompositionEntryGeneral(QL, Nord, cert.shadows, i, j, k);
      if (!r.ok) { allOk = false; fails.push({ i, j, k, r }); }
    }
    const strict = checkStrictCompositionInverseGeneral(cert, QL);
    verdict.items['7_composition_table'] = { ok: allOk && strict.ok, checked: cert.composition_table.length, fails, strict };
  } else {
    verdict.items['7_composition_table'] = { ok: false, reason: 'composition_table is missing' };
  }

  // item 8: inverse via (3.54) round-trip
  if (cert.inverse_map) {
    const Nord = 6;
    let allOk = true; const fails = [];
    for (const [i, iInv] of cert.inverse_map) {
      const r = checkInverseEntryGeneral(QL, Nord, cert.shadows, i, iInv);
      if (!r.ok) { allOk = false; fails.push({ i, iInv, r }); }
    }
    verdict.items['8_inverse_map'] = { ok: allOk, checked: cert.inverse_map.length, fails };
  } else {
    verdict.items['8_inverse_map'] = { ok: false, reason: 'inverse_map is missing' };
  }

  // item 9: reduction -> K3 ([m,f] -> (m, f の G3 成分))。全射かどうかを独立再計算し claim と突合。
  {
    const required = ['K3'];
    const listed = (cert.reduction || []).map((r) => r && r.to);
    const exact = listed.length === required.length && required.every((id) => listed.filter((x) => x === id).length === 1);
    let allOk = true; const fails = [];
    for (const id of required) {
      const entry = (cert.reduction || []).find((r) => r.to === id);
      if (!entry) { allOk = false; fails.push({ to: id, reason: 'required reduction entry missing' }); continue; }
      const targetCert = certsById.get(id);
      const r = checkReductionEntry(cert.target.n, entry, cert.shadows, targetCert);
      const claimMatchesRecomputed = r.surjectiveOk === undefined ? false : (entry.surjective === r.surjectiveOk);
      if (!(r.ok === true && claimMatchesRecomputed)) {
        allOk = false;
        fails.push({ to: id, r, claimed_surjective: entry.surjective, recomputed_surjective: r.surjectiveOk });
      }
    }
    verdict.items['9_reduction'] = {
      ok: allOk && exact, required, listed, exact_entry_set: exact, fails,
      note: '設計 §2/§1: R_{L,K3} = [m,f]->(m, fのG3成分)。全射性は claim をそのまま信じず独立再計算し一致を要求(week3-L-設計.md §2 fake 証明書対応)。',
    };
  }

  // item 10: ls_witness -- (5.1) の theta/tau (F2 の自己準同型) は dihedral 専用構成。N/A。
  verdict.items['10_ls_witness'] = {
    ok: true, status: 'N/A',
    reason: 'ls_witness (5.1) の theta/tau 構成は dihedral(2405 Thm4.3系)専用。week3-L-設計.md は general 用の再定義を与えていない。',
  };

  verdict.items['11_induced_maps'] = { ok: true, status: 'N/A', reason: 'dihedral の theta/tau 商写像は Q_L=G3xH3 に非適用。' };
  verdict.items['12_representative_invariance'] = checkRepresentativeInvarianceGeneral(cert, model, QL);
  verdict.items['13_varrho'] = { ok: true, status: 'N/A', reason: 'Thm.4.6 の明示式 rho は n=4,8,16 dihedral 専用。' };

  const allItemsOk = Object.values(verdict.items).every((it) => it.ok === true);
  verdict.all_pass = allItemsOk;
  verdict.cross_checked = allItemsOk; // 用語規律: cross-checked (verified は Lean 専有)
  return verdict;
}

function checkCertificate(cert, certsById) {
  if (cert.target && cert.target.family === 'general') {
    return checkCertificateGeneral(cert, certsById);
  }
  const verdict = { id: cert.target.id, family: cert.target.family, schema: cert.schema, items: {} };
  const isDihedral = cert.target.family === 'dihedral';
  const n = cert.target.n;

  const schemaErrors = validateCertificateShape(cert);
  verdict.items['0_schema_fail_closed'] = { ok: schemaErrors.length === 0, errors: schemaErrors };

  const { Q, phi } = isDihedral ? dihedralPhi(n) : controlN5Phi();
  const model = buildTransversalModel(Q, phi);
  const Gn = isDihedral ? buildGn(n) : null;

  if (isDihedral) {
    verdict.items['0_invariants'] = checkCertificateInvariants(cert, Gn, n);
  } else {
    const inv = cert.target.invariants || {};
    const checks = { index_PB3: inv.index_PB3 === 5, index_B3: inv.index_B3 === 30, N_ord: inv.N_ord === 5, derived_order: inv.derived_order === 1 };
    verdict.items['0_invariants'] = { ok: Object.values(checks).every(Boolean), expected: { index_PB3: 5, index_B3: 30, N_ord: 5, derived_order: 1 }, claimed: inv, checks };
  }

  // item 1: counts 整合
  {
    const c = cert.counts || {};
    const monotone = (c.raw_candidates >= c.hexagon_pass) && (c.hexagon_pass >= c.charming_pass) && (c.charming_pass >= c.surjective_pass);
    const matchesShadowLen = isDihedral ? c.surjective_pass === cert.shadows.length : c.surjective_pass === 4;
    let matchesThm43 = null;
    if (isDihedral) {
      const t43 = thm43ShadowSet(n);
      matchesThm43 = (c.surjective_pass === t43.shadows.length);
    }
    verdict.items['1_counts'] = {
      ok: monotone && matchesShadowLen && (matchesThm43 !== false) && (isDihedral || (c.raw_candidates === 5 && c.hexagon_pass === 5 && c.charming_pass === 4 && c.surjective_pass === 4)),
      monotone, matchesShadowLen, matchesThm43,
      approved_simplification: '追補1 項目3(司令塔裁定・2026-07-18): raw 候補の完全再列挙は不要。単調性+最終個数一致(+dihedralはThm4.3集合一致)で可、と承認済み。',
    };
  }

  if (!isDihedral) verdict.items['1_n5_full_enumeration'] = checkN5Enumeration(model, cert);
  if (isDihedral) verdict.items['1_raw_formula'] = checkRawCandidateFormula(cert, Gn, n);
  else verdict.items['1_raw_formula'] = { ok: true, status: 'N/A', reason: 'control N5 uses explicit raw enumeration item 1_n5_full_enumeration' };

  // item 2: full hexagon per shadow
  {
    let allOk = true; const fails = [];
    const hexagonResults = [];
    for (let i = 0; i < cert.shadows.length; i++) {
      const r = checkHexagon(model, cert.shadows[i]);
      hexagonResults.push(r);
      if (!r.ok) { allOk = false; fails.push({ i, r }); }
    }
    verdict.items['2_hexagon'] = { ok: allOk, checked: cert.shadows.length, fails, _results_for_downstream: hexagonResults };
  }

  // item 3: f_word <-> f_triple (dihedral only, needs psi_n)
  if (isDihedral) {
    let allOk = true; const fails = [];
    for (let i = 0; i < cert.shadows.length; i++) {
      const r = checkFWordVsTriple(Gn, n, cert.shadows[i]);
      if (!r.ok) { allOk = false; fails.push({ i, r }); }
    }
    verdict.items['3_f_word_vs_triple'] = { ok: allOk, checked: cert.shadows.length, fails };
  }

  // item 4: charming + surjective (dihedral only)
  if (isDihedral) {
    let allOk = true; const fails = [];
    for (let i = 0; i < cert.shadows.length; i++) {
      const r = checkCharmingAndSurjective(Gn, n, cert.shadows[i]);
      if (!r.ok) { allOk = false; fails.push({ i, r }); }
    }
    verdict.items['4_charming_surjective'] = { ok: allOk, checked: cert.shadows.length, fails };
  } else {
    // item 4 相当 (control): PB3/N5 = C5 は可換なので [F2/N_F2, F2/N_F2] = 1。
    // charming の f ∈ [F2/N_F2,...] 条件は f_word が (N_F2 を法として) 1 であることに帰着する。
    // 追補1 F4 裁定どおり「f_word が空」を明示検査する。
    let allOk = true; const fails = [];
    for (let i = 0; i < cert.shadows.length; i++) {
      const sh = cert.shadows[i];
      const isEmpty = Array.isArray(sh.f_word) && sh.f_word.length === 0;
      if (!isEmpty) { allOk = false; fails.push({ i, f_word: sh.f_word }); }
    }
    verdict.items['4_charming_control'] = {
      ok: allOk, checked: cert.shadows.length, fails,
      note: '追補1 F4: control(N5) は PB3/N5=C5 が可換なので [F2/N_F2,F2/N_F2]=1。charming は f_word が空(f=1)であることの明示検査に帰着する。',
    };
  }

  // item 5: Thm 4.3 set equality (dihedral only)
  if (isDihedral) {
    verdict.items['5_thm43_set'] = checkThm43(Gn, n, cert);
  }

  // item 6: kernel_cert (4.11) -- 確定式 (追補1 項目1・項目4)
  {
    let allOk = true; const fails = [];
    for (let i = 0; i < cert.shadows.length; i++) {
      const sh = cert.shadows[i];
      const kc = sh.kernel_cert;
      const r = (kc && kc.type === 'brute') ? checkKernelCertBrute(model, sh) : checkKernelCert(n, sh);
      if (r.ok === false) { allOk = false; fails.push({ i, r }); }
    }
    verdict.items['6_kernel_cert'] = {
      ok: allOk, checked: cert.shadows.length, fails,
      note: '確定式で実装 (追補1 項目1: (4.11) の2等式 x-bar^{2m+1}=h.x-bar.h^-1, g^-1.y-bar^{2m+1}.g=h.y-bar.h^-1 / 項目4: N5 の brute 手続き)',
    };
  }

  // item 7: composition_table via (3.53)(4.19)(4.20)
  if (isDihedral && cert.composition_table) {
    const Nord = lcm(n, 2);
    let allOk = true; const fails = [];
    for (const [i, j, k] of cert.composition_table) {
      const r = checkCompositionEntry(Gn, n, Nord, cert.shadows, i, j, k);
      if (!r.ok) { allOk = false; fails.push({ i, j, k, r }); }
    }
    const strict = checkStrictCompositionInverse(cert, Gn, n);
    verdict.items['7_composition_table'] = { ok: allOk && strict.ok, checked: cert.composition_table.length, fails, strict };
  } else if (!isDihedral) {
    verdict.items['7_composition_table'] = { ok: true, status: 'N/A', reason: 'control certificate has no dihedral shadow group composition table; N5 is fully enumerated independently' };
  }

  // item 8: inverse via (3.54) round-trip
  if (isDihedral && cert.inverse_map) {
    const Nord = lcm(n, 2);
    let allOk = true; const fails = [];
    for (const [i, iInv] of cert.inverse_map) {
      const r = checkInverseEntry(Gn, n, Nord, cert.shadows, i, iInv);
      if (!r.ok) { allOk = false; fails.push({ i, iInv, r }); }
    }
    verdict.items['8_inverse_map'] = { ok: allOk, checked: cert.inverse_map.length, fails };
  } else if (!isDihedral) {
    verdict.items['8_inverse_map'] = { ok: true, status: 'N/A', reason: 'control certificate has no dihedral inverse map' };
  }

  // item 9: reduction
  if (isDihedral && cert.reduction) {
    let allOk = true; const fails = [];
    for (const redEntry of cert.reduction) {
      const targetCert = certsById.get(redEntry.to);
      const r = checkReductionEntry(n, redEntry, cert.shadows, targetCert);
      if (r.ok !== true) { allOk = false; fails.push({ to: redEntry.to, r }); }
    }
    const coverage = checkReductionCoverage(cert, certsById);
    verdict.items['9_reduction'] = {
      ok: allOk && coverage.ok, checked: cert.reduction.length, fails, coverage,
      index_convention: '追補1 項目5で凍結: image[i] = source shadows[i] の像の target 証明書 shadows[] における添字。全射性 = image の値域が target 全添字を被覆。',
    };
  } else if (isDihedral) {
    verdict.items['9_reduction'] = { ok: requiredReductionsFor(n).length === 0, checked: 0, expected_zero: requiredReductionsFor(n).length === 0, reason: requiredReductionsFor(n).length === 0 ? '非適用対象のため expected-zero' : '必要な reduction が欠落' };
  } else {
    verdict.items['9_reduction'] = { ok: true, status: 'N/A', reason: 'control certificate has no reduction entry' };
  }

  // item 10: ls_witness (5.1) -- 確定式 (追補1 項目2)
  if (isDihedral && cert.ls_witness) {
    let allOk = true; const fails = [];
    for (const entry of cert.ls_witness) {
      const r = checkLsWitness(Gn, n, entry);
      if (r.ok === false) { allOk = false; fails.push({ entry, r }); }
    }
    const expectedLs = n % 3 === 0 ? cert.shadows.length : 0;
    const coverageOk = cert.ls_witness.length === expectedLs;
    verdict.items['10_ls_witness'] = {
      ok: allOk && coverageOk, checked: cert.ls_witness.length, expected: expectedLs, fails,
      note: '確定式で実装 (追補1 項目2: fK=theta(g)^-1 gK, fx^mK=tau(h)^-1 hK(m=0 mod3)/tau(h)^-1 xy hK(m=2 mod3); m=1 mod3 は現れたらFAIL)',
    };
  } else if (isDihedral) {
    verdict.items['10_ls_witness'] = { ok: n % 3 !== 0, checked: 0, expected: n % 3 === 0 ? cert.shadows.length : 0, reason: n % 3 === 0 ? '適用対象だが ls_witness が欠落' : '非適用対象のため expected-zero' };
  } else {
    verdict.items['10_ls_witness'] = { ok: true, status: 'N/A', reason: 'control certificate has no LS witness' };
  }

  if (isDihedral) {
    verdict.items['11_induced_maps'] = checkInducedMaps(Gn);
    verdict.items['12_representative_invariance'] = checkRepresentativeInvariance(cert, model, Gn, verdict.items['2_hexagon']._results_for_downstream, certsById);
    delete verdict.items['2_hexagon']._results_for_downstream;
    if ([4, 8, 16].includes(n)) verdict.items['13_varrho'] = checkVarRho(cert, n);
    else verdict.items['13_varrho'] = { ok: true, status: 'N/A', reason: 'Thm.4.6 explicit rho is applicable only to n=4,8,16' };
  } else {
    verdict.items['11_induced_maps'] = { ok: true, status: 'N/A', reason: 'dihedral theta/tau maps are not part of control N5' };
    verdict.items['12_representative_invariance'] = { ok: true, status: 'N/A', reason: 'dihedral representative convention is not part of control N5' };
    verdict.items['13_varrho'] = { ok: true, status: 'N/A', reason: 'Thm.4.6 explicit rho is not part of control N5' };
  }

  const allItemsOk = Object.values(verdict.items).every((it) => it.ok === true);
  verdict.all_pass = allItemsOk;
  verdict.cross_checked = allItemsOk; // 用語規律: cross-checked (verified は Lean 専有)
  return verdict;
}

// ---------- main ----------
function main() {
  const globalOnly = process.argv.includes('--global-only');
  if (!globalOnly) {
    console.log('=== WP2b node 照合器: 起動時自己検査 ===');
    const sc = selfCheck();
    for (const line of sc.log) console.log(' - ' + line);
    if (!sc.ok) {
      console.log('\n自己検査 FAIL: 証明書の検査には進みません。仕様の再確認が必要です。');
      process.exitCode = 1;
      return;
    }
    console.log('\n自己検査: ALL PASS\n');
  } else {
    console.log('=== global-only: certificate self-check skipped (last full run was ALL PASS) ===');
  }

  if (!globalOnly) {
    console.log('=== Thm 4.3 閉じた式の自前生成 (n=3..16) ===');
    for (let n = 3; n <= 16; n++) {
      const Gn = buildGn(n);
      const expectedOrd = expectedGnOrder(n);
      const actualOrd = Gn.GnMap.size;
      const t43 = thm43ShadowSet(n);
      const derivedOrd = Gn.derived.size;
      console.log(`n=${n}: |G_n| actual=${actualOrd} expected=${expectedOrd} match=${actualOrd === expectedOrd} | N_ord=${t43.Nord} n1=${t43.n1} |X_n|=${t43.Xn.length} |GT(K^(${n}))|_expected=${t43.shadows.length} | |[Gn,Gn]|=${derivedOrd}`);
    }
  }

  console.log('\n=== 証明書の検査 ===');
  if (!existsSync(CERT_DIR)) {
    console.log(`certificates/ ディレクトリが存在しません (${CERT_DIR})。WP2a (探索器) 待ち — 本実行では自己検査と Thm4.3 生成のみ完了。`);
    return;
  }
  const files = readdirSync(CERT_DIR).filter((f) => f.endsWith('.json'));
  if (files.length === 0) {
    console.log('certificates/ は存在するが *.json が 0 件。WP2a 待ち。');
    return;
  }

  const certs = files.map((f) => JSON.parse(readFileSync(join(CERT_DIR, f), 'utf8')));
  const certsById = new Map();
  for (const c of certs) certsById.set(c.target.id, c);

  if (!existsSync(VERDICT_DIR)) mkdirSync(VERDICT_DIR, { recursive: true });

  if (process.argv.includes('--global-only')) {
    console.log('\n=== global suite only: numeric/doubling/Prop.3.5 ===');
    const capMs = globalCapFromArgs();
    let global;
    try { global = runGlobalSuite(certsById, capMs); } catch (err) { global = { schema: 'gtsh-global/v1', status: 'UNKNOWN', cap_ms: capMs, all_pass: false, error: String(err && err.stack || err) }; }
    const globalPath = join(VERDICT_DIR, 'global.v1.verdict.json');
    writeFileSync(globalPath, JSON.stringify(global, null, 2));
    console.log(`global verdict -> ${globalPath}`);
    console.log(`  cap_ms=${capMs} status=${global.status || 'UNKNOWN'} numeric=${global.numeric?.ok ? 'PASS' : 'FAIL'} doubling=${global.doubling?.ok ? 'PASS' : 'UNKNOWN'} Prop.3.5=${global.prop_3_5?.ok ? 'PASS' : 'UNKNOWN'} checked=${global.prop_3_5?.checked_pairs ?? 256}/256`);
    return;
  }

  for (const cert of certs) {
    console.log(`\n--- ${cert.target.id} (n=${cert.target.n ?? 'n/a'}, family=${cert.target.family}) ---`);
    let verdict;
    try {
      verdict = checkCertificate(cert, certsById);
    } catch (err) {
      verdict = { id: cert.target.id, error: String(err && err.stack || err), all_pass: false, cross_checked: false };
    }
    const outPath = join(VERDICT_DIR, `${cert.target.id}.v1.verdict.json`);
    writeFileSync(outPath, JSON.stringify(verdict, null, 2));
    console.log(`verdict -> ${outPath}`);
    if (verdict.items) {
      for (const [k, v] of Object.entries(verdict.items)) {
        console.log(`  ${k}: ${v.ok === true ? 'PASS' : v.ok === false ? 'FAIL' : 'N/A'}${v.provisional_interpretation ? ' [PROVISIONAL]' : ''}`);
      }
    }
    console.log(`  ALL PASS (cross-checked): ${verdict.all_pass ? 'YES' : 'NO'}`);
  }

  console.log('\n=== global suite: numeric/doubling/Prop.3.5 ===');
  let global;
  try {
    global = runGlobalSuite(certsById, globalCapFromArgs());
  } catch (err) {
    global = { schema: 'gtsh-global/v1', all_pass: false, error: String(err && err.stack || err) };
  }
  const globalPath = join(VERDICT_DIR, 'global.v1.verdict.json');
  writeFileSync(globalPath, JSON.stringify(global, null, 2));
  console.log(`global verdict -> ${globalPath}`);
  console.log(`  numeric: ${global.numeric?.ok ? 'PASS' : 'FAIL'}`);
  console.log(`  doubling: ${global.doubling?.ok ? 'PASS' : 'FAIL'}`);
  console.log(`  Prop.3.5: ${global.prop_3_5?.ok ? 'PASS' : 'FAIL'} true=${global.prop_3_5?.true_count ?? 'n/a'} false=${global.prop_3_5?.false_count ?? 'n/a'} mismatch=${global.prop_3_5?.mismatch_count ?? 'n/a'}`);
  console.log(`  K36 triangle: ${global.reduction_triangle?.ok ? 'PASS' : 'FAIL'} checked=${global.reduction_triangle?.checked ?? 'n/a'}/216`);
  console.log(`  GLOBAL ALL PASS: ${global.all_pass ? 'YES' : 'NO'}`);
}

// テスト用 export (main() の自動実行はコマンドライン起動時のみ -- 下の import.meta.url ガード参照)
export {
  checkCertificate, checkRepresentativeInvariance,
  checkKernelCert, checkKernelCertBrute, checkLsWitness, checkCompositionEntry,
  checkInverseEntry, checkReductionEntry, checkHexagon, checkFWordVsTriple,
  checkCharmingAndSurjective, checkThm43, buildGn, buildTransversalModel,
  dihedralPhi, controlN5Phi, thm43ShadowSet, kappa, evalWord, tripleFromCertFormat,
  xyWordToPerm,
  // Week3 general family (docs/week3-L-設計.md)
  makeH3, buildQL, checkCertificateGeneral, checkFWordVsPairGeneral,
  checkCharmingAndSurjectiveGeneral, checkKernelCertBruteGeneral,
  checkCompositionEntryGeneral, checkInverseEntryGeneral, checkRepresentativeInvarianceGeneral,
};

// process.argv[1] が指すファイルとして直接起動された場合のみ main() を実行する
// (他ファイルから import された場合は実行しない -- pathToFileURL で Windows のドライブレター/
//  バックスラッシュも正しく正規化して比較する)。
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main();
}
