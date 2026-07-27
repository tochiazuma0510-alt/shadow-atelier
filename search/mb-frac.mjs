// mb-frac.mjs — 委嘱1(Model-Builder)専用の厳密有理数演算ライブラリ。
// BigInt 分数のみ・浮動小数点を一切使わない。
// 探索器(このファイル)は照合器(crosscheck/)とは共有しない — 独立実装の原則。

function gcdBig(a, b) {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b) { [a, b] = [b, a % b]; }
  return a;
}

export class Frac {
  constructor(n, d = 1n) {
    if (typeof n === 'number') n = BigInt(n);
    if (typeof d === 'number') d = BigInt(d);
    if (d === 0n) throw new Error('Frac: zero denominator');
    if (d < 0n) { n = -n; d = -d; }
    const g = gcdBig(n, d) || 1n;
    this.n = n / g;
    this.d = d / g;
  }
  static from(x) {
    if (x instanceof Frac) return x;
    return new Frac(BigInt(x), 1n);
  }
  add(o) { o = Frac.from(o); return new Frac(this.n * o.d + o.n * this.d, this.d * o.d); }
  sub(o) { o = Frac.from(o); return new Frac(this.n * o.d - o.n * this.d, this.d * o.d); }
  mul(o) { o = Frac.from(o); return new Frac(this.n * o.n, this.d * o.d); }
  div(o) { o = Frac.from(o); if (o.n === 0n) throw new Error('Frac: division by zero'); return new Frac(this.n * o.d, this.d * o.n); }
  neg() { return new Frac(-this.n, this.d); }
  isZero() { return this.n === 0n; }
  eq(o) { o = Frac.from(o); return this.n * o.d === o.n * this.d; }
  cmpAbs() { return this.n < 0n ? -this.n : this.n; }
  toString() {
    if (this.d === 1n) return this.n.toString();
    return `${this.n}/${this.d}`;
  }
  isInt() { return this.d === 1n; }
}

export const F0 = new Frac(0n);
export const F1 = new Frac(1n);

// 多項式は Frac[] (低次から高次)。
export function polyDeg(p) {
  for (let i = p.length - 1; i >= 0; i--) if (!p[i].isZero()) return i;
  return -1; // zero polynomial
}
export function polyTrim(p) {
  const d = polyDeg(p);
  return p.slice(0, d + 1);
}
export function polyEval(p, x) {
  x = Frac.from(x);
  let acc = F0;
  for (let i = p.length - 1; i >= 0; i--) acc = acc.mul(x).add(p[i]);
  return acc;
}

// Fraction 係数の n x n 行列の行列式(fraction Gaussian elimination・部分ピボット)。
export function detFrac(matIn) {
  const n = matIn.length;
  const mat = matIn.map(row => row.map(x => Frac.from(x)));
  let det = F1;
  for (let col = 0; col < n; col++) {
    let piv = -1;
    for (let r = col; r < n; r++) { if (!mat[r][col].isZero()) { piv = r; break; } }
    if (piv === -1) return F0;
    if (piv !== col) { [mat[piv], mat[col]] = [mat[col], mat[piv]]; det = det.neg(); }
    det = det.mul(mat[col][col]);
    const pivVal = mat[col][col];
    for (let r = col + 1; r < n; r++) {
      if (mat[r][col].isZero()) continue;
      const factor = mat[r][col].div(pivVal);
      for (let c = col; c < n; c++) {
        mat[r][c] = mat[r][c].sub(factor.mul(mat[col][c]));
      }
    }
  }
  return det;
}

// Lagrange 補間: 点 (xs[i], ys[i]) を通る次数 <= xs.length-1 の一意多項式の係数(低次から高次)。
export function lagrangeInterpolate(xs, ys) {
  const n = xs.length;
  // 結果多項式を Frac[] として構築
  let result = new Array(n).fill(F0);
  for (let i = 0; i < n; i++) {
    // basis_i(x) = prod_{j!=i} (x - xs[j]) / (xs[i]-xs[j])
    let basis = [F1]; // 多項式 1
    let denom = F1;
    for (let j = 0; j < n; j++) {
      if (j === i) continue;
      // multiply basis by (x - xs[j])
      const newBasis = new Array(basis.length + 1).fill(F0);
      for (let k = 0; k < basis.length; k++) {
        newBasis[k + 1] = newBasis[k + 1].add(basis[k]);
        newBasis[k] = newBasis[k].sub(basis[k].mul(Frac.from(xs[j])));
      }
      basis = newBasis;
      denom = denom.mul(Frac.from(xs[i]).sub(Frac.from(xs[j])));
    }
    const coef = ys[i].div(denom);
    for (let k = 0; k < basis.length; k++) {
      result[k] = result[k].add(basis[k].mul(coef));
    }
  }
  return polyTrim(result);
}
