// crosscheck/cyclo-ring-lib.mjs
// 便 34 P6-K1/C3 のための共有インフラ(BigInt 有理数係数の多項式環演算・
// 円分多項式の独立計算)。GAP の search/kummer-decide.g のコード・中間結果は
// import しない(この module は Q[T] 上の純粋な多項式演算だけを行い、GAP の
// AlgebraicExtension/Factors には一切依存しない)。
// crosscheck/check-kummer.mjs と crosscheck/check-kummer-cov3.mjs の両方が
// この module を使うが、これは「u 抽出アルゴリズムの非共有」規律(SS6.3)の
// 対象ではない(u_pathA/u_pathB のような被検証アルゴリズム本体ではなく、
// 円分体の環演算という共通の数学インフラ)。

function gcdBig(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { [a, b] = [b, a % b]; } return a; }
// --- 司令塔独自攻撃(裁定41続報)修理: Q.parse は旧版で `str.split('/')` の
// 先頭 2 要素だけを黙って読んでいた("1/2/3" が黙って 1/2 として parse
// され、" 1/2" のような空白混入 trim も通した)。u-compare 系/check-kummer 系
// と同じ全文一致 grammar(符号付き整数 or 分子/分母一組だけ・空白混入拒否)
// へ硬化する。denominator 0 は既存の Q コンストラクタが引き続き拒否する
// (実測確認済み・変更不要)。 ---
export class RationalFormatError extends Error {}
const RATIONAL_LITERAL_RE = /^([+-]?\d+)(?:\/([+-]?\d+))?$/;
export class Q {
  constructor(n, d = 1n) {
    if (typeof n === 'number') n = BigInt(n);
    if (typeof d === 'number') d = BigInt(d);
    if (d === 0n) throw new Error('Q: zero denominator');
    if (d < 0n) { n = -n; d = -d; }
    const g = gcdBig(n, d) || 1n;
    this.n = n / g; this.d = d / g;
  }
  static parse(s) {
    if (typeof s === 'number') return Q.fromNumber(s);
    const str = String(s);
    const m = RATIONAL_LITERAL_RE.exec(str);
    if (!m) {
      throw new RationalFormatError(
        `malformed rational literal ${JSON.stringify(s)}: must match ^[+-]?\\d+(/[+-]?\\d+)?$ ` +
        `(signed integer, or exactly one numerator/denominator pair -- whitespace, empty ` +
        `numerator/denominator, and a second '/' are all rejected)`
      );
    }
    const nRaw = BigInt(m[1]);
    const dRaw = m[2] !== undefined ? BigInt(m[2]) : 1n;
    return new Q(nRaw, dRaw);
  }
  static fromNumber(x) { return new Q(BigInt(x)); }
  add(o) { return new Q(this.n * o.d + o.n * this.d, this.d * o.d); }
  sub(o) { return new Q(this.n * o.d - o.n * this.d, this.d * o.d); }
  mul(o) { return new Q(this.n * o.n, this.d * o.d); }
  div(o) { return new Q(this.n * o.d, this.d * o.n); }
  neg() { return new Q(-this.n, this.d); }
  isZero() { return this.n === 0n; }
  eq(o) { return this.n * o.d === o.n * this.d; }
  toString() { return this.d === 1n ? `${this.n}` : `${this.n}/${this.d}`; }
}
export const Q0 = new Q(0n);
export const Q1 = new Q(1n);

//////////////////// 多項式(昇冪係数配列の Q[]、通常の多項式演算) ////////////////////
export function polyTrim(c) { const r = c.slice(); while (r.length > 1 && r[r.length - 1].isZero()) r.pop(); return r; }
export function polyAdd(a, b) {
  const n = Math.max(a.length, b.length);
  const r = [];
  for (let i = 0; i < n; i++) r.push((a[i] ?? Q0).add(b[i] ?? Q0));
  return polyTrim(r);
}
export function polySub(a, b) {
  const n = Math.max(a.length, b.length);
  const r = [];
  for (let i = 0; i < n; i++) r.push((a[i] ?? Q0).sub(b[i] ?? Q0));
  return polyTrim(r);
}
export function polyMul(a, b) {
  const r = Array.from({ length: a.length + b.length - 1 }, () => Q0);
  for (let i = 0; i < a.length; i++) {
    if (a[i].isZero()) continue;
    for (let j = 0; j < b.length; j++) {
      if (b[j].isZero()) continue;
      r[i + j] = r[i + j].add(a[i].mul(b[j]));
    }
  }
  return polyTrim(r);
}
// 多項式の長除法(有理数係数)。a / b = (quotient, remainder)。b はゼロでない。
export function polyDivMod(a, b) {
  let rem = a.slice();
  const bDeg = b.length - 1;
  const bLead = b[bDeg];
  const quotient = [];
  while (rem.length - 1 >= bDeg && !(rem.length === 1 && rem[0].isZero())) {
    const remDeg = rem.length - 1;
    if (remDeg < bDeg) break;
    const coeff = rem[remDeg].div(bLead);
    const shift = remDeg - bDeg;
    quotient[shift] = coeff;
    const sub = Array.from({ length: remDeg + 1 }, () => Q0);
    for (let i = 0; i <= bDeg; i++) sub[i + shift] = coeff.mul(b[i]);
    rem = polyTrim(polySub(rem, sub));
    if (rem.length - 1 < bDeg) break;
  }
  for (let i = 0; i < quotient.length; i++) if (quotient[i] === undefined) quotient[i] = Q0;
  return { quotient: polyTrim(quotient.length ? quotient : [Q0]), remainder: rem };
}
// mod による reduce (modPoly は monic である必要はないが本 module では monic 前提)
export function polyMod(a, modPoly) { return polyDivMod(a, modPoly).remainder; }

export function polyMulMod(a, b, modPoly) { return polyMod(polyMul(a, b), modPoly); }
export function polyPowMod(base, exp, modPoly) {
  let result = [Q1];
  let b = polyMod(base, modPoly);
  let e = exp;
  while (e > 0) {
    if (e & 1) result = polyMulMod(result, b, modPoly);
    b = polyMulMod(b, b, modPoly);
    e >>= 1;
  }
  return result;
}
export function polyEqConst(a, c) {
  // a (mod 済み係数配列) が定数 c (BigInt or Q) に等しいか
  const cQ = c instanceof Q ? c : new Q(c);
  if (!(a[0] ?? Q0).eq(cQ)) return false;
  for (let i = 1; i < a.length; i++) if (!(a[i] ?? Q0).isZero()) return false;
  return true;
}

//////////////////// 円分多項式の独立計算(整数係数、Mobius 分解によらず
//////////////////// Phi_n(x) = (x^n-1) / prod_{d|n,d<n} Phi_d(x) の逐次除算) ////////////////////
const cyclotomicCache = new Map();
export function cyclotomicPolynomialAscending(n) {
  if (cyclotomicCache.has(n)) return cyclotomicCache.get(n);
  if (n === 1) { const r = [new Q(-1n), new Q(1n)]; cyclotomicCache.set(1, r); return r; }
  // x^n - 1
  let numerator = Array.from({ length: n + 1 }, () => Q0);
  numerator[0] = new Q(-1n);
  numerator[n] = new Q(1n);
  const divisors = [];
  for (let d = 1; d < n; d++) if (n % d === 0) divisors.push(d);
  let denom = [new Q(1n)];
  for (const d of divisors) denom = polyMul(denom, cyclotomicPolynomialAscending(d));
  const { quotient, remainder } = polyDivMod(numerator, denom);
  if (!(remainder.length === 1 && remainder[0].isZero())) {
    throw new Error(`cyclotomicPolynomialAscending(${n}): division did not come out exact (unexpected)`);
  }
  cyclotomicCache.set(n, quotient);
  return quotient;
}
