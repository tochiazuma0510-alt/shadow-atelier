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
// R-8(便 35 F5.2・便 36 F3.2 (4)/F6-3・**裁定 38/便 37 F3 修理**): 旧実装は
// 「大域枝 (M0 の三値 {W,N_aff,N_infty})」と「P0 の局所 Weierstrass 性」を
// 同じ `branchP0` field に混ぜていた(Sol 便 37 F3 の指摘)。ここを二軸に
// 分離する:
//   - `branch`  : 大域枝(P_infty の Weierstrass 性 + P0=iota(P_infty) 判定
//                 (2.-1)。Rule 1 SS2.2 M0)。このスキーマ(x0,y0 を持つ
//                 アフィン raw)では {W, N_aff} のいずれかでなければならない
//                 -- N_infty はここに来たら別スキーマ違反(I-m)。
//   - `P0_type` : 局所 P0 の Weierstrass 性({Weierstrass, nonWeierstrass})。
//                 B-i/B-ii(SS6.2)・Hensel/Newton 展開の分岐(SS6.1)の選択に
//                 使う量そのもの。
// 整合規則(Sol 便37 F3 / Rule 1 SS4.1 の帰結・S5-W 補題・R1-M0 3.):
//   - branch = 'W'      => P0_type は 'nonWeierstrass' でなければならない
//                          (枝 (W) では P0 は自動的に非 Weierstrass -- S5-W
//                          補題・SS4.1「(v1.2 の絞り込み)」)。
//   - branch = 'N_aff'  => P0_type は両値どちらでも良い(「P0 も Weierstrass」
//                          が発火しうるのは副枝 (N_aff) だけ -- SS4.1)。
//   - branch = 'N_infty' はこのスキーマでは不正(loadModelNinf を使うこと)。
// 未知ラベル・欠落ラベルを既定値(旧実装は無条件で 'Weierstrass' へ
// fallback していた -- バグ)へ丸めることは禁止する(fail-closed。
// Rule 1 SS2.2 M0 / SS9.2 I-m)。
const GLOBAL_BRANCH_ENUM = ['W', 'N_aff', 'N_infty'];
const P0_TYPE_ENUM = ['Weierstrass', 'nonWeierstrass'];
export function loadModel(raw) {
  const branch = raw.branch;
  const p0Type = raw.P0_type;
  if (!GLOBAL_BRANCH_ENUM.includes(branch)) {
    throw new Error(`loadModel (I-m): branch must be one of {${GLOBAL_BRANCH_ENUM.join(', ')}}, got '${branch}' -- no default fallback is permitted (Rule 1 SS2.2 M0 / SS9.2 I-m)`);
  }
  if (branch === 'N_infty') {
    throw new Error(`loadModel (I-m): branch='N_infty' models have no x0,y0 and must use loadModelNinf/extractPathB_Ninf, not loadModel/extractPathB (Rule 1 SS6.3-6)`);
  }
  if (!P0_TYPE_ENUM.includes(p0Type)) {
    throw new Error(`loadModel (I-m): P0_type must be one of {${P0_TYPE_ENUM.join(', ')}}, got '${p0Type}' -- no default fallback is permitted`);
  }
  if (branch === 'W' && p0Type !== 'nonWeierstrass') {
    throw new Error(`loadModel (I-m): branch='W' requires P0_type='nonWeierstrass' (Lemma S5-W / Rule 1 SS4.1 "v1.2 の絞り込み"), got P0_type='${p0Type}'`);
  }
  return {
    id: raw.fixture_id ?? raw.id,
    M: raw.M,
    branch,
    P0_type: p0Type,
    x0: Q.parse(raw.x0),
    y0: Q.parse(raw.y0),
    f: raw.f_coeffs_ascending.map(Q.parse),
    A: raw.A_coeffs_ascending.map(Q.parse),
    B: raw.B_coeffs_ascending.map(Q.parse),
  };
}

//////////////////// canonical model digest (便 34 P6-E2・便 37 F3 で branch/P0_type 分離) ////////////////////
// search/u-extract-pathA.g の PathA_CanonicalModelString と**同一のバイト列**
// を生成するよう独立に実装する(突合の前提)。ここでは実装を独立に書き下す
// ことで「両方が同じ仕様を独立に満たす」ことを保証する(共有関数の呼び出し
// ではない)。schema v3(便 37 F3 の branch/P0_type 分離で digest 対象文字列が
// 変わるため v2 から version up)。
export function canonicalModelString(model) {
  const rat = (x) => x.toString();
  const list = (xs) => xs.map(rat).join(',');
  return `id=${model.id};M=${model.M};branch=${model.branch};P0_type=${model.P0_type};` +
    `x0=${rat(model.x0)};y0=${rat(model.y0)};` +
    `f=[${list(model.f)}];A=[${list(model.A)}];B=[${list(model.B)}]`;
}
export function modelDigest(model) {
  return createHash('sha256').update(canonicalModelString(model), 'utf8').digest('hex');
}

//////////////////// 経路 B 本体 (SS6.2 (6.1)(6.2)) ////////////////////
export function extractPathB(model) {
  const { M, branch, P0_type, x0, y0, f, A, B } = model;
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
  if (P0_type === 'nonWeierstrass') {
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
    schema: 'u-pathB/v3',
    id: model.id,
    M,
    branch,
    P0_type,
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

//////////////////// R-5(便 36・裁定 37): 副枝 (N_infty) 経路 B-iii(production 化) ////////////////////
// docs/week4-K5_Rule1_v1.md v1.2 S6.2 B-iii (6.3) / 補題 R1-B∞ + 便 36 F3.2/F6-1
// (Sol 提供の M=10, chat=1 exact synthetic fixture)。級数を使わない: N(lambda)
// = A^2 - B^2 f (多項式のみ) が定数 chat=1 であることを直接検算し、
// u^{(B)} = chat / (2 a_M) (a_M := [x^M] A) を計算する。
//
// schema v3(便 36 F3.2 (3) の修理・裁定40/便39 F2 で v2→v3 へ破壊的
// version bump -- 必須 field P0_type/a_M/b_Mm3 を持たない旧 v2 raw は
// retracted/ へ退避): 三値 branch label(model.branch は必ず
// "N_infty")・model.M(旧 model.n を置換)・model_digest・
// expected_model_digest を持つ。x0, y0 は存在しない(§6.3-6)。同じライブラリ
// コードを M=3 の unit test(crosscheck/u-extract-pathB-ninf-toy-driver.mjs)
// と M=10 の production 較正(crosscheck/u-extract-pathB-ninf-production-
// driver.mjs)の両方が使う -- いずれも K^(5) の実 fixture ではない。
//
// (N∞-1)-(N∞-4) の構造検査(すべて exact 多項式演算・fail-closed。§6.2):
//   (N∞-1) deg A = M かつ deg B = M-3
//   (N∞-2) b_{M-3} = a_M かつ a_M <> 0
//   (N∞-3) A^2-B^2 f が定数 chat <> 0
//   (N∞-4) chat = 1(補題 R1-N∞-S)
// いずれかが破れたら throw で即停止する(§9.2 I-j)。加えて gcd(f,f') が単元
// (f の平方非因子性・多項式 Euclid の互除法で実装。search/u-extract-pathA.g
// の PolyGcdIsUnit とは独立実装)・model_digest = expectedModelDigest
// (§9.2 I-l)も fail-closed に検査する(便 36 F3.2 (2)(3)(5))。
export function loadModelNinf(raw) {
  if (raw.branch !== 'N_infty') {
    throw new Error(`loadModelNinf (I-m): raw.branch must be the literal string 'N_infty', got '${raw.branch}'`);
  }
  if (raw.M === undefined || raw.M === null) {
    throw new Error("loadModelNinf: raw.M is required (Rule 1 M naming; the old raw.n field name is retired)");
  }
  // 便 37 F3 (R-8): P0_type は副枝 (N_infty) では常に 'nonWeierstrass'
  // (補題 R1-M0 3.: iota(P_infty) は iota の不動点でないので P0 は非
  // Weierstrass)。field が与えられていれば fail-closed に検査する
  // (未提供でも許す -- N_infty raw の必須 field ではないが、あれば逐語一致
  // を要求する)。
  if (raw.P0_type !== undefined && raw.P0_type !== null && raw.P0_type !== 'nonWeierstrass') {
    throw new Error(`loadModelNinf (I-m): P0_type must be 'nonWeierstrass' for branch='N_infty' (Lemma R1-M0 3.), got '${raw.P0_type}'`);
  }
  return {
    id: raw.id,
    branch: raw.branch,
    P0_type: 'nonWeierstrass',
    M: raw.M,
    f: raw.f_coeffs_ascending.map(Q.parse),
    A: raw.A_coeffs_ascending.map(Q.parse),
    B: raw.B_coeffs_ascending.map(Q.parse),
    seriesLen: raw.series_length,
    expectedModelDigest: raw.expected_model_digest,
  };
}

//////////////////// exact 多項式 gcd(有理数係数・pathA.g とは独立実装) ////////////////////
function polyDivMod(a, b) {
  const bdeg = b.length - 1;
  const blead = b[bdeg];
  let rem = a.slice();
  const quot = [];
  while (rem.length - 1 >= bdeg && !(rem.length === 1 && rem[0].isZero())) {
    const rdeg = rem.length - 1;
    const coeff = rem[rdeg].div(blead);
    const shift = rdeg - bdeg;
    const term = Array(shift).fill(Q0).concat([coeff]);
    rem = polySub(rem, polyMul(term, b));
    quot[shift] = coeff;
  }
  for (let i = 0; i < quot.length; i++) if (quot[i] === undefined) quot[i] = Q0;
  return { quot: polyTrim(quot.length ? quot : [Q0]), rem };
}
function polyGcd(a, b) {
  let A = a.slice(), B = b.slice();
  while (!(B.length === 1 && B[0].isZero())) {
    const { rem } = polyDivMod(A, B);
    A = B;
    B = rem;
  }
  return A;
}
function polyGcdIsUnit(f) {
  const fp = polyDeriv(f);
  if (fp.length === 1 && fp[0].isZero()) return false; // f' = 0 degenerate
  const g = polyGcd(f, fp);
  return g.length === 1 && !g[0].isZero();
}

//////////////////// canonical model digest (N_infty schema, pathA.g の Ninf 版と同一仕様) ////////////////////
export function canonicalModelStringNinf(model) {
  const rat = (x) => x.toString();
  const list = (xs) => xs.map(rat).join(',');
  return `id=${model.id};branch=N_infty;M=${model.M};` +
    `f=[${list(model.f)}];A=[${list(model.A)}];B=[${list(model.B)}]`;
}
export function modelDigestNinf(model) {
  return createHash('sha256').update(canonicalModelStringNinf(model), 'utf8').digest('hex');
}

export function extractPathB_Ninf(model) {
  const { M, f, A, B } = model;
  if (f.length !== 7) throw new Error('extractPathB_Ninf: f must have degree 6');
  if (!f[6].eq(new Q(1n))) throw new Error('extractPathB_Ninf: f must be monic');

  // -- (N∞-1) --
  const degA = A.length - 1;
  const degB = B.length - 1;
  if (degA !== M) throw new Error(`extractPathB_Ninf (N∞-1): deg A must equal M=${M}, got ${degA}`);
  if (degB !== M - 3) throw new Error(`extractPathB_Ninf (N∞-1): deg B must equal M-3=${M - 3}, got ${degB}`);

  // -- (N∞-2) --
  const a_M = A[M];
  const b_Mm3 = B[M - 3];
  if (!a_M.eq(b_Mm3)) throw new Error(`extractPathB_Ninf (N∞-2): b_{M-3} (${b_Mm3}) must equal a_M (${a_M})`);
  if (a_M.isZero()) throw new Error('extractPathB_Ninf (N∞-2): a_M must be nonzero');

  // -- gcd(f,f') must be a unit (f squarefree) --
  if (!polyGcdIsUnit(f)) throw new Error('extractPathB_Ninf: gcd(f,f\') is not a unit -- f is not squarefree (fixture corruption)');

  // -- required series length, if declared (便 36 F3.2 (2)) --
  if (model.seriesLen !== undefined && model.seriesLen !== null && model.seriesLen < 2 * M + 4) {
    throw new Error(`extractPathB_Ninf: seriesLen (${model.seriesLen}) must be >= 2M+4 = ${2 * M + 4}`);
  }

  const A2 = polyMul(A, A);
  const B2 = polyMul(B, B);
  const B2f = polyMul(B2, f);
  const Nlambda = polySub(A2, B2f);

  // -- (N∞-3) N(lambda) must be a nonzero constant polynomial. --
  const isConstant = Nlambda.length === 1;
  if (!isConstant) throw new Error(`extractPathB_Ninf (N∞-3): N(lambda) is not constant, degree ${Nlambda.length - 1}`);
  const chat = Nlambda[0];
  if (chat.isZero()) throw new Error('extractPathB_Ninf (N∞-3): N(lambda) is the zero constant');

  // -- (N∞-4) --
  if (!chat.eq(new Q(1n))) throw new Error(`extractPathB_Ninf (N∞-4): chat must equal 1 (Lemma R1-N∞-S; sigma_1<>id is automatic in this campaign), got ${chat}`);

  const u_pathB_ninf = chat.div(a_M.mul(new Q(2n)));

  const modelDigest = modelDigestNinf(model);
  if (model.expectedModelDigest !== undefined && model.expectedModelDigest !== null) {
    if (modelDigest !== model.expectedModelDigest) {
      throw new Error(`extractPathB_Ninf (I-l): model_digest (${modelDigest}) does not match expectedModelDigest (${model.expectedModelDigest})`);
    }
  }

  return {
    schema: 'u-pathB-ninf/v3',
    id: model.id,
    branch: 'N_infty',
    P0_type: 'nonWeierstrass',
    M,
    f_coeffs_ascending: f.map(String),
    A_coeffs_ascending: A.map(String),
    B_coeffs_ascending: B.map(String),
    deg_A_equals_M: degA === M,
    deg_B_equals_Mminus3: degB === M - 3,
    b_Mm3_equals_a_M: a_M.eq(b_Mm3),
    gcd_f_fprime_is_unit: true,
    N_lambda_coeffs_ascending: Nlambda.map(String),
    N_lambda_is_nonzero_constant: isConstant && !chat.isZero(),
    chat: chat.toString(),
    chat_equals_1: chat.eq(new Q(1n)),
    a_M: a_M.toString(),
    b_Mm3: b_Mm3.toString(),
    u_pathB_ninf: u_pathB_ninf.toString(),
    model_digest: modelDigest,
    model_digest_algo: 'sha256(canonical_model_string_ninf)',
    expected_model_digest: model.expectedModelDigest,
    canonical_model_string: canonicalModelStringNinf(model),
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
    branch: model.branch,
    P0_type: model.P0_type,
    x0: model.x0, // k^2 * x0 = 0 when x0 = 0
    y0: kQ.pow(5).mul(model.y0),
    f: f2, A: A2, B: B2,
  };
}
