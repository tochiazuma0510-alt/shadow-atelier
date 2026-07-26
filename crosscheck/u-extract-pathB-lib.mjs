// crosscheck/u-extract-pathB-lib.mjs
// Rule 1 (docs/week4-K5_Rule1_v1.md) SS6.2 経路 B (Vieta / ノルム・級数不使用)
// 委嘱: 便 32 P6 後半 + 便 34 blocker 2 (Sol 便 34 P6-E1)。
//
// 身分: 本ファイルは library である(関数定義のみ・入力パラメトリック・
// トップレベル実行なし)。K3 較正の実行は
// crosscheck/u-extract-pathB-k3-driver.mjs(薄い driver)が担う。将来の K5
// driver はこの library を import して extractPathB(model) を呼ぶだけで
// よい(model literal・ファイル書き出しは driver 側)。
//
// 独立性 (SS6.3): べき級数を一切使わない。使う演算は
//   (a) 多項式の掛け算・引き算 (係数ベクトル演算)
//   (b) 多項式の一点評価
//   (c) 多項式の Taylor 係数 (= 高階微分/階乗。B-ii のみ)
// search/u-extract-pathA.g とは関数・データ構造を一切共有しない
// (BigInt 有理数クラス Q はこのファイル内で独立に再実装する)。
//
// 便 34 P6-E2 (blocker 3 前半): extractPathB の出力に「入力モデルの
// canonical digest」を埋め込む(model_digest フィールド)。canonical
// 化・sha256 の算出は search/u-extract-pathA.g 側と**独立に**実装する
// (node crypto の createHash のみを共有インフラとして使う -- これは
// アルゴリズム本体ではないので SS6.3 の非共有 helper 要件には抵触しない)。

import { createHash } from 'node:crypto';

//////////////////// BigInt 有理数 (pathA.g とは独立実装) ////////////////////
function gcdBig(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { [a, b] = [b, a % b]; } return a; }
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
    const str = String(s).trim();
    if (str.includes('/')) { const [a, b] = str.split('/'); return new Q(BigInt(a), BigInt(b)); }
    return new Q(BigInt(str));
  }
  static fromNumber(x) { return new Q(BigInt(x)); }
  add(o) { return new Q(this.n * o.d + o.n * this.d, this.d * o.d); }
  sub(o) { return new Q(this.n * o.d - o.n * this.d, this.d * o.d); }
  mul(o) { return new Q(this.n * o.n, this.d * o.d); }
  div(o) { return new Q(this.n * o.d, this.d * o.n); }
  neg() { return new Q(-this.n, this.d); }
  pow(k) {
    if (k === 0) return new Q(1n);
    if (k > 0) { let r = new Q(1n); for (let i = 0; i < k; i++) r = r.mul(this); return r; }
    return new Q(1n).div(this.pow(-k));
  }
  isZero() { return this.n === 0n; }
  eq(o) { return this.n * o.d === o.n * this.d; }
  toString() { return this.d === 1n ? `${this.n}` : `${this.n}/${this.d}`; }
}
const Q0 = new Q(0n);

//////////////////// 多項式(昇冪係数配列の Q[]) ////////////////////
function polyTrim(c) { const r = c.slice(); while (r.length > 1 && r[r.length - 1].isZero()) r.pop(); return r; }
function polyAdd(a, b) {
  const n = Math.max(a.length, b.length);
  const r = [];
  for (let i = 0; i < n; i++) r.push((a[i] ?? Q0).add(b[i] ?? Q0));
  return polyTrim(r);
}
function polySub(a, b) {
  const n = Math.max(a.length, b.length);
  const r = [];
  for (let i = 0; i < n; i++) r.push((a[i] ?? Q0).sub(b[i] ?? Q0));
  return polyTrim(r);
}
function polyMul(a, b) {
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
function polyEval(a, x) {
  let r = Q0;
  for (let i = a.length - 1; i >= 0; i--) r = r.mul(x).add(a[i]);
  return r;
}
// Taylor シフト: f(x0 + t) の t 昇冪係数 (有限・厳密)
function polyShift(a, x0) {
  const deg = a.length - 1;
  // ホーナー法で (x - (-x0)) による合成を反復適用しても良いが、
  // ここでは二項展開で直接: coeff of t^k = sum_{i=k}^{deg} a[i] * C(i,k) * x0^{i-k}
  const binom = (n, k) => { let r = 1n; for (let i = 0; i < k; i++) r = r * BigInt(n - i) / BigInt(i + 1); return r; };
  const out = [];
  for (let k = 0; k <= deg; k++) {
    let s = Q0;
    for (let i = k; i <= deg; i++) {
      const c = new Q(binom(i, k));
      s = s.add(a[i].mul(c).mul(x0.pow(i - k)));
    }
    out.push(s);
  }
  return polyTrim(out);
}
function polyDeriv(a) {
  if (a.length <= 1) return [Q0];
  const out = [];
  for (let i = 1; i < a.length; i++) out.push(a[i].mul(new Q(BigInt(i))));
  return polyTrim(out);
}
// 高階微分: f^{(k)} の係数配列(k 回 polyDeriv を適用)
function polyDerivN(a, k) { let r = a; for (let i = 0; i < k; i++) r = polyDeriv(r); return r; }
function factorialQ(k) { let r = 1n; for (let i = 2; i <= k; i++) r = r * BigInt(i); return new Q(r); }

//////////////////// モデル読み込み ////////////////////
export function loadModel(raw) {
  return {
    id: raw.fixture_id ?? raw.id,
    M: raw.M,
    branchP0: raw.branch_P0 === 'nonWeierstrass' || raw.branchP0 === 'nonWeierstrass' ? 'nonWeierstrass' : 'Weierstrass',
    x0: Q.parse(raw.x0),
    y0: Q.parse(raw.y0),
    f: raw.f_coeffs_ascending.map(Q.parse),
    A: raw.A_coeffs_ascending.map(Q.parse),
    B: raw.B_coeffs_ascending.map(Q.parse),
  };
}

//////////////////// canonical model digest (便 34 P6-E2) ////////////////////
// search/u-extract-pathA.g の PathA_CanonicalModelString と**同一のバイト列**
// を生成するよう独立に実装する(突合の前提)。ここでは実装を独立に書き下す
// ことで「両方が同じ仕様を独立に満たす」ことを保証する(共有関数の呼び出し
// ではない)。
export function canonicalModelString(model) {
  const rat = (x) => x.toString();
  const list = (xs) => xs.map(rat).join(',');
  return `id=${model.id};M=${model.M};branchP0=${model.branchP0};` +
    `x0=${rat(model.x0)};y0=${rat(model.y0)};` +
    `f=[${list(model.f)}];A=[${list(model.A)}];B=[${list(model.B)}]`;
}
export function modelDigest(model) {
  return createHash('sha256').update(canonicalModelString(model), 'utf8').digest('hex');
}

//////////////////// 経路 B 本体 (SS6.2 (6.1)(6.2)) ////////////////////
export function extractPathB(model) {
  const { M, branchP0, x0, y0, f, A, B } = model;
  // lambda^iota = A - B y なので N(lambda) = A^2 - B^2 f
  const A2 = polyMul(A, A);
  const B2 = polyMul(B, B);
  const B2f = polyMul(B2, f);
  const Nlambda = polySub(A2, B2f); // in x, degree <= max(2degA, 2degB+degf)

  // 検算: ord_{x0}(N(lambda)) = M であること (x0 におけるテイラー展開の
  // 下位 M 項が消えること) -- shift して確認
  const NlambdaShift = polyShift(Nlambda, x0); // 係数 = t^k の係数 (t = x - x0)
  let lowerVanish = true;
  for (let k = 0; k < M; k++) {
    if (!(NlambdaShift[k] ?? Q0).isZero()) lowerVanish = false;
  }
  const chat = NlambdaShift[M] ?? Q0; // ĉ

  let u_pathB, formula, extra = {};
  if (branchP0 === 'nonWeierstrass') {
    // (6.1): u = chat / (A(x0) - B(x0) y0)
    const Ax0 = polyEval(A, x0);
    const Bx0 = polyEval(B, x0);
    const denom = Ax0.sub(Bx0.mul(y0));
    if (denom.isZero()) throw new Error('pathB B-i: lambda^iota(P0) = 0, formula degenerates');
    u_pathB = chat.div(denom);
    formula = 'B-i (6.1)';
    extra = { chat: chat.toString(), lambda_iota_P0: denom.toString() };
  } else {
    // (6.2): alpha = [(x-x0)^{M/2}] A(x) = A^{(M/2)}(x0) / (M/2)!
    if (M % 2 !== 0) throw new Error('pathB B-ii requires even M');
    const half = M / 2;
    const Ahalf = polyDerivN(A, half);
    const alpha = polyEval(Ahalf, x0).div(factorialQ(half));
    const fprime = polyDeriv(f);
    const fpx0 = polyEval(fprime, x0);
    if (fpx0.isZero()) throw new Error('pathB B-ii: f\'(x0) = 0, P0 not a simple Weierstrass root');
    u_pathB = alpha.div(fpx0.pow(half));
    formula = 'B-ii (6.2)';
    extra = { alpha: alpha.toString(), fprime_x0: fpx0.toString() };
  }

  return {
    schema: 'u-pathB/v2',
    id: model.id,
    M,
    branchP0,
    x0: x0.toString(),
    y0: y0.toString(),
    f_coeffs_ascending: f.map(String),
    A_coeffs_ascending: A.map(String),
    B_coeffs_ascending: B.map(String),
    formula,
    lower_order_vanish: lowerVanish,
    N_lambda_coeffs_ascending: Nlambda.map(String),
    u_pathB: u_pathB.toString(),
    ...extra,
    model_digest: modelDigest(model),
    model_digest_algo: 'sha256(canonical_model_string)',
    canonical_model_string: canonicalModelString(model),
  };
}

//////////////////// R-5(便 36・裁定 36): 副枝 (N_infty) 経路 B-iii ////////////////////
// docs/week4-K5_Rule1_v1.md v1.2 S6.2 B-iii (6.3) / 補題 R1-B∞。級数を使わない:
// N(lambda) = A^2 - B^2 f (多項式のみ) が定数 chat であることを直接検算し、
// u^{(B)} = chat / (2 a_n) (a_n := [x^n] A) を計算する。
// SYNTHETIC のみ: K^(5) の実 fixture には (N_infty) が無いため、較正は
// crosscheck/u-extract-pathB-ninf-toy-driver.mjs が明示する玩具モデルでのみ
// 行う。
export function loadModelNinf(raw) {
  return {
    id: raw.id,
    n: raw.n,
    f: raw.f_coeffs_ascending.map(Q.parse),
    A: raw.A_coeffs_ascending.map(Q.parse),
    B: raw.B_coeffs_ascending.map(Q.parse),
  };
}

export function extractPathB_Ninf(model) {
  const { n, f, A, B } = model;
  if (f.length !== 7) throw new Error('extractPathB_Ninf: f must have degree 6');
  if (!f[6].eq(new Q(1n))) throw new Error('extractPathB_Ninf: f must be monic');

  const degA = A.length - 1;
  const degB = B.length - 1;
  if (degA !== n) throw new Error(`extractPathB_Ninf (N∞-1): deg A must equal n=${n}, got ${degA}`);
  if (degB !== n - 3) throw new Error(`extractPathB_Ninf (N∞-1): deg B must equal n-3=${n - 3}, got ${degB}`);
  const a_n = A[n];
  const b_nm3 = B[n - 3];
  if (!a_n.eq(b_nm3)) throw new Error(`extractPathB_Ninf (N∞-2): b_{n-3} (${b_nm3}) must equal a_n (${a_n})`);
  if (a_n.isZero()) throw new Error('extractPathB_Ninf (N∞-2): a_n must be nonzero');

  const A2 = polyMul(A, A);
  const B2 = polyMul(B, B);
  const B2f = polyMul(B2, f);
  const Nlambda = polySub(A2, B2f);

  // (N∞-3) N(lambda) must be a nonzero constant polynomial.
  const isConstant = Nlambda.length === 1;
  if (!isConstant) throw new Error(`extractPathB_Ninf (N∞-3): N(lambda) is not constant, degree ${Nlambda.length - 1}`);
  const chat = Nlambda[0];
  if (chat.isZero()) throw new Error('extractPathB_Ninf (N∞-3): N(lambda) is the zero constant');

  const u_pathB_ninf = chat.div(a_n.mul(new Q(2n)));

  return {
    schema: 'u-pathB-ninf-toy/v1',
    synthetic_note: 'R-5 toy calibration (Rule 1 S0.4-3 M=n=3 toy family) -- NOT a K^(5) individual model/coefficient/numeric approximation',
    id: model.id,
    n,
    f_coeffs_ascending: f.map(String),
    A_coeffs_ascending: A.map(String),
    B_coeffs_ascending: B.map(String),
    deg_A_equals_n: degA === n,
    b_nm3_equals_a_n: a_n.eq(b_nm3),
    N_lambda_coeffs_ascending: Nlambda.map(String),
    N_lambda_is_nonzero_constant: isConstant && !chat.isZero(),
    chat: chat.toString(),
    a_n: a_n.toString(),
    u_pathB_ninf: u_pathB_ninf.toString(),
  };
}

//////////////////// COV-1 (s -> cs) 派生モデル (pathA.g と独立に再構成) ////////////////////
export function cov1Model(model, k) {
  const kQ = Q.parse(k);
  const f2 = model.f.map((c, i) => c.mul(kQ.pow(10 - 2 * i)));
  const A2 = model.A.map((c, i) => c.div(kQ.pow(2 * i)));
  const B2 = model.B.map((c, i) => c.div(kQ.pow(2 * i + 5)));
  return {
    id: model.id + '-cov1-k' + k,
    M: model.M,
    branchP0: model.branchP0,
    x0: model.x0, // k^2 * x0 = 0 when x0 = 0
    y0: kQ.pow(5).mul(model.y0),
    f: f2, A: A2, B: B2,
  };
}
