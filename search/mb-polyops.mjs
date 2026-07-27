// mb-polyops.mjs — 委嘱2(Model-Builder)探索器・多項式演算の追加分。
// mb-frac.mjs(委嘱1・凍結せず継続利用)の Frac 上に、枝 (N_aff) の探索に
// 必要な多項式演算(加減乗・微分・除算・GCD)を追加する。
// 探索器専用。crosscheck/ の照合器とは非共有(独立実装の原則)。
// 浮動小数点は一切使わない(すべて BigInt 分数)。

import { Frac, F0, F1, polyTrim, polyDeg } from './mb-frac.mjs';

function fr(x) { return Frac.from(x); }

export function polyIsZero(p) { return polyDeg(p) < 0; }

export function polyAdd(p, q) {
  const n = Math.max(p.length, q.length);
  const r = new Array(n).fill(F0);
  for (let i = 0; i < n; i++) {
    const a = i < p.length ? p[i] : F0;
    const b = i < q.length ? q[i] : F0;
    r[i] = a.add(b);
  }
  return polyTrim(r);
}

export function polySub(p, q) {
  const n = Math.max(p.length, q.length);
  const r = new Array(n).fill(F0);
  for (let i = 0; i < n; i++) {
    const a = i < p.length ? p[i] : F0;
    const b = i < q.length ? q[i] : F0;
    r[i] = a.sub(b);
  }
  return polyTrim(r);
}

export function polyScale(p, s) {
  s = fr(s);
  return polyTrim(p.map(c => c.mul(s)));
}

export function polyMul(p, q) {
  const dp = polyDeg(p), dq = polyDeg(q);
  if (dp < 0 || dq < 0) return [];
  const r = new Array(dp + dq + 1).fill(F0);
  for (let i = 0; i <= dp; i++) {
    if (p[i].isZero()) continue;
    for (let j = 0; j <= dq; j++) {
      if (q[j].isZero()) continue;
      r[i + j] = r[i + j].add(p[i].mul(q[j]));
    }
  }
  return polyTrim(r);
}

export function polyDerivative(p) {
  const d = polyDeg(p);
  if (d <= 0) return [];
  const r = new Array(d).fill(F0);
  for (let i = 1; i <= d; i++) r[i - 1] = p[i].mul(fr(i));
  return polyTrim(r);
}

// 厳密多項式除算(Frac 係数の Q[x] における商・余り)。q は非零多項式。
export function polyDivMod(p, q) {
  const dq = polyDeg(q);
  if (dq < 0) throw new Error('polyDivMod: division by zero polynomial');
  let rem = p.slice();
  const dp0 = polyDeg(rem);
  const quotDeg = dp0 - dq;
  const quot = new Array(quotDeg >= 0 ? quotDeg + 1 : 0).fill(F0);
  const lcQ = q[dq];
  while (true) {
    const dr = polyDeg(rem);
    if (dr < dq) break;
    const factor = rem[dr].div(lcQ);
    const shift = dr - dq;
    quot[shift] = factor;
    const sub = new Array(dr + 1).fill(F0);
    for (let i = 0; i <= dq; i++) sub[i + shift] = q[i].mul(factor);
    rem = polySub(rem, sub);
  }
  return { quot: polyTrim(quot), rem: polyTrim(rem) };
}

// 厳密多項式 GCD(Euclid の互除法・Frac 係数)。結果はスカラー倍の不定性を持つ
// (呼び出し側で monic 正規化すること)。両方零多項式なら空配列を返す。
export function polyGCD(p, q) {
  let a = polyTrim(p), b = polyTrim(q);
  if (polyIsZero(a)) return b;
  if (polyIsZero(b)) return a;
  while (!polyIsZero(b)) {
    const { rem } = polyDivMod(a, b);
    a = b;
    b = rem;
  }
  return a;
}

// monic 正規化(先頭係数で全体を割る)。零多項式はそのまま返す。
export function polyMonic(p) {
  const d = polyDeg(p);
  if (d < 0) return p;
  return polyScale(p, F1.div(p[d]));
}

export function polyEqual(p, q) {
  const pt = polyTrim(p), qt = polyTrim(q);
  if (pt.length !== qt.length) return false;
  for (let i = 0; i < pt.length; i++) if (!pt[i].eq(qt[i])) return false;
  return true;
}

export function polyToString(p) {
  const d = polyDeg(p);
  if (d < 0) return '0';
  const terms = [];
  for (let i = d; i >= 0; i--) {
    if (p[i].isZero()) continue;
    terms.push(`${p[i].toString()}${i > 0 ? `*x^${i}` : ''}`);
  }
  return terms.join(' + ');
}
