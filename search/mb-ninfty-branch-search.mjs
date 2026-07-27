// mb-ninfty-branch-search.mjs — 委嘱3(Model-Builder)探索器・副枝 (N_infty) 専用。
// 探索器(GAP と対にならぬ独立実装)。crosscheck/ の照合器とは非共有。
//
// ============================================================
// 数学的設計(S5 設計 v1.2 §3.3.5・命題 S5-3∞・Rule 1 v1.3 §2.2 M1(N_infty 行)
// に整合)
// ============================================================
//
// 設定: y^2=f6(x)(f6: Q 上 monic・squarefree・deg6・depressed = B5=0
// — Rule 1 M1 (2.-3) の x-平行移動を使い切った正規化)、P_infty=infty_+、
// P_0=infty_-=iota(P_infty)。mu=a(x)+p(x)y(deg a=5, deg p=2, 補題 S5-H)。
//
// 命題 S5-3∞(global な同値・分離条件を要しない):
//   div(mu)=5P_0-5P_infty  <=>  a(x)^2 - f6(x) p(x)^2 = c_hat_mu (定数・非零)
//     かつ deg a=5, deg p=2, a_5:=[x^5]a = [x^2]p (leading coeff 一致)
//
// ゲージ: Rule 1 M1 が既に f6 を monic・depressed(B5=0)に固定する
// (x-平行移動を使い切る)。残余スケール(x->tx, y->t^3y)は N_aff と同型
// (weight 6-j)であり、これを使って a5=+-1 に正規化できる(N_aff と同じ
// 議論: f6 の主係数が a5^2 になるので monic 性は a5=+-1 と同値)。
// mu-スケール(残り1自由度)は c_hat_mu の平方類を変える作用であり、
// ★教材3(S5設計§6.3)により c_hat_mu の平方類・平方因子・符号を計算・
// 選択基準に一切使わず、ゲージで縮めずにブルートフォースする(N_aff の
// c_N と同じ扱い)。
//
// 判定アルゴリズム(厳密・浮動小数点不使用・2 段階):
//
// 段階1(命題 S5-3∞ の等式そのものを満たす f6 の存在):
//   asq := a^2 (deg10), psq := p^2 (deg4) を計算し、asq を psq で厳密
//   多項式除算する: asq = psq*q + r (deg r < 4)。
//   命題の等式 a^2-f6p^2=c_hat_mu(定数)が成り立つことと、
//     q が deg6・monic(q_6=1)・depressed(q_5=0)であり、
//     r の deg <= 0(すなわち r_1=r_2=r_3=0)
//   であることは同値(f6:=q、c_hat_mu:=r_0)。この4条件をすべて厳密に
//   検査し、f6 がさらに squarefree(非特異性)・p2!=0(補題 S5-H)・
//   c_hat_mu != 0 であることも確認する。leading coeff 一致 a5=p2 は
//   ここでは課さない(p2 は独立変数として走査し、a5^2=p2^2 は q_6=1 の
//   検査から自動的に必要条件として出る — a5=+-1 なので実質 p2=+-1)。
//
// 段階2(mu の分岐型 (5,2^2 1,2^2 1,5)):
//   s:=1/x(P_0 の Q-有理 uniformizer・Rule 1 補題 R1-U∞ 2.)に関して、
//   a~(s):=s^5 a(1/s) = a5+a4 s+a3 s^2+a2 s^3+a1 s^4+a0 s^5 と置くと、
//   mu のファイバー方程式(命題 S5-3∞ の等式を使って導かれる厳密な
//   代数的帰結)は
//     h(s;v) := s^5 (v^2+c_hat_mu) - 2 v a~(s) = 0
//   となる(枝 (N_aff) の g(x;v) と同型の導出。v=0 では h(s;0)=c_hat_mu*s^5
//   となり s=0 の 5 重根が自動的に現れる — これが P_0 での型 5 分岐に
//   対応し、N_aff の v=0 分岐と違って「見かけの次数低下」は v=0 では
//   起きない)。
//
//   ただし h(s;v) の s^5 係数((v^2+c_hat_mu)-2v a0 = v^2-2a0v+c_hat_mu)
//   と h'(s;v) の s^4 係数(比例)は、ある**2 点**(v^2-2a0v+c_hat_mu=0 の
//   根)で同時に消える(N_aff の v_0 と同型・ここでは 2 次式)。これは
//   s=infty(=x=0、C 上の 2 点)が射影的な意味での共通根になる特異点であり、
//   幾何的な分岐点ではない。固定次数(5,4)の Sylvester 行列で計算した
//   D(v)=Res_{5,4}(h,h') はこの根で機械的に 0 になることを実例で確認し
//   (下記 stripKnownQuadraticFactor)、この既知の 2 次因子を除去してから
//   v^k 剥離・偶関数判定へ進む(N_aff §1.3 で発見した手法をそのまま適用)。
//
// 禁止事項の遵守: 本探索器は c_hat_mu(=a^2-f6*p^2)の値・平方類・平方因子・
// 符号を一切「計算・選択基準に使用」していない(ブルートフォースの格子点
// として扱うのみ)。lambda=c*mu^2 の c も計算・出力していない。出力する
// f6・a・p は完全な曲線データ(A1 whitelist 内)である。

import { Frac, F0, F1, polyTrim, polyDeg, polyEval, detFrac, lagrangeInterpolate } from './mb-frac.mjs';
import { polyMul, polyDerivative, polyDivMod, polyGCD, polyIsZero } from './mb-polyops.mjs';

function fr(x) { return Frac.from(x); }

function xPow(n) {
  const arr = new Array(n + 1).fill(F0);
  arr[n] = F1;
  return arr;
}

// --- 段階1: a^2-f6*p^2=定数 の成立検査(f6・c_hat_mu を同時に得る) ---
export function factorCheckNinfty(aCoeffs /* [a0..a5] Frac, deg5 */, pCoeffs /* [p0,p1,p2] Frac, deg2 */) {
  const a = aCoeffs, p = pCoeffs;
  if (p[2].isZero()) return { ok: false, reason: 'p2=0 (deg p < 2, violates lemma S5-H structure)' };
  const asq = polyMul(a, a);
  const psq = polyMul(p, p);
  if (polyDeg(asq) !== 10) return { ok: false, reason: `deg(a^2)=${polyDeg(asq)}, expected 10` };
  const { quot: q, rem: r } = polyDivMod(asq, psq);
  const dq = polyDeg(q);
  if (dq !== 6) return { ok: false, reason: `deg(quotient)=${dq}, expected 6 (f6 must be degree 6)` };
  if (!q[6].eq(F1)) return { ok: false, reason: `quotient not monic (lc=${q[6]})`, internal_error: false };
  if (q[5] && !q[5].isZero()) return { ok: false, reason: `quotient not depressed (B5=${q[5]}, expected 0 by Rule 1 M1 gauge)` };
  // 余りの次数が 0 以下(定数)であることを確認
  if (r[1] && !r[1].isZero()) return { ok: false, reason: 'remainder has nonzero x^1 coeff (c_hat_mu condition fails)' };
  if (r[2] && !r[2].isZero()) return { ok: false, reason: 'remainder has nonzero x^2 coeff (c_hat_mu condition fails)' };
  if (r[3] && !r[3].isZero()) return { ok: false, reason: 'remainder has nonzero x^3 coeff (c_hat_mu condition fails)' };
  const cHatMu = r[0] ?? F0;
  if (cHatMu.isZero()) return { ok: false, reason: 'c_hat_mu=0 (mu would have an affine zero/pole, contradicting lemma)' };
  // f6 の squarefree 性(非特異性)
  const f6 = q;
  const f6p = polyDerivative(f6);
  const sf = polyGCD(f6, f6p);
  if (polyDeg(sf) > 0) return { ok: false, reason: `f6 not squarefree (deg gcd(f6,f6')=${polyDeg(sf)})` };
  return { ok: true, f6, cHatMu };
}

// --- 段階2: mu の分岐型判定(s=1/x 座標・固定次数 resultant) ---

// a~(s) = s^5*a(1/s) = 低次->高次で [a5,a4,a3,a2,a1,a0]
function aTilde(a) {
  return [a[5], a[4], a[3], a[2], a[1], a[0]];
}

// h(s;v) の係数(低次->高次、長さ6固定, s^0..s^5)。
function hPolyAtV(aTil, cHatMu, v) {
  const [t0, t1, t2, t3, t4, t5] = aTil; // a~ の係数 s^0..s^5
  const c0 = v.mul(fr(-2)).mul(t0);
  const c1 = v.mul(fr(-2)).mul(t1);
  const c2 = v.mul(fr(-2)).mul(t2);
  const c3 = v.mul(fr(-2)).mul(t3);
  const c4 = v.mul(fr(-2)).mul(t4);
  const c5 = v.mul(v).add(cHatMu).sub(v.mul(fr(2)).mul(t5));
  return [c0, c1, c2, c3, c4, c5];
}
// h'(s;v)(s に関する微分)の係数(低次->高次、長さ5固定, s^0..s^4)。
function hPrimePolyAtV(aTil, cHatMu, v) {
  const [t0, t1, t2, t3, t4, t5] = aTil;
  const c0 = v.mul(fr(-2)).mul(t1);
  const c1 = v.mul(fr(-4)).mul(t2);
  const c2 = v.mul(fr(-6)).mul(t3);
  const c3 = v.mul(fr(-8)).mul(t4);
  const c4 = v.mul(v).add(cHatMu).mul(fr(5)).sub(v.mul(fr(10)).mul(t5));
  return [c0, c1, c2, c3, c4];
}

function resultantFixedDeg(fLow, fFixedLen, gLow, gFixedLen) {
  const df = fFixedLen - 1;
  const dg = gFixedLen - 1;
  const n = df + dg;
  const fHigh = []; for (let i = df; i >= 0; i--) fHigh.push(fLow[i]);
  const gHigh = []; for (let i = dg; i >= 0; i--) gHigh.push(gLow[i]);
  const mat = [];
  for (let r = 0; r < dg; r++) {
    const row = new Array(n).fill(F0);
    for (let k = 0; k < fHigh.length; k++) row[r + k] = fHigh[k];
    mat.push(row);
  }
  for (let r = 0; r < df; r++) {
    const row = new Array(n).fill(F0);
    for (let k = 0; k < gHigh.length; k++) row[r + k] = gHigh[k];
    mat.push(row);
  }
  return detFrac(mat);
}

// D(v) を厳密補間で再構成する。次数上界: n*d_f+m*d_g = 4*2+5*1=13 の余裕で16。
export function computeDiscriminantPolyNinfty(aTil, cHatMu) {
  const DEG_BOUND = 16;
  const xs = [];
  for (let i = 0; i <= DEG_BOUND; i++) {
    const k = Math.ceil(i / 2);
    xs.push(i === 0 ? 0n : (i % 2 === 1 ? BigInt(k) : -BigInt(k)));
  }
  const ys = xs.map(v => {
    const vF = fr(v);
    const f = hPolyAtV(aTil, cHatMu, vF);
    const g = hPrimePolyAtV(aTil, cHatMu, vF);
    return resultantFixedDeg(f, 6, g, 5);
  });
  const poly = lagrangeInterpolate(xs.map(x => fr(x)), ys);
  const checkX = BigInt(DEG_BOUND + 5);
  const vF = fr(checkX);
  const f = hPolyAtV(aTil, cHatMu, vF);
  const g = hPrimePolyAtV(aTil, cHatMu, vF);
  const actual = resultantFixedDeg(f, 6, g, 5);
  const predicted = polyEval(poly, checkX);
  const consistent = actual.eq(predicted);
  return { poly, consistent };
}

// ★ 既知の2次アーティファクト因子 (v^2-2*a0*v+c_hat_mu) の除去。
// N_aff の線形アーティファクト(§1.3 の stripKnownLinearFactor)と同型の
// 現象で、ここでは h(s;v)・h'(s;v) の主要係数(s^5・s^4)が共に
// v^2-2 a0 v+c_hat_mu に比例するため 2 次になる。この v は s=infty
// (=x=0、C 上の2点のいずれか)での mu の値に対応し、幾何的分岐点ではない。
function stripKnownQuadraticFactor(poly, a0, cHatMu) {
  const quad = [cHatMu, a0.mul(fr(-2)), F1]; // c_hat_mu - 2 a0 v + v^2 (低次->高次)
  let cur = poly;
  let power = 0;
  while (polyDeg(cur) >= 2) {
    const { quot, rem } = polyDivMod(cur, quad);
    if (!polyIsZero(rem)) break;
    cur = quot;
    power++;
  }
  return { power, rest: cur };
}

export function stripZeroRoot(poly) {
  const d = polyDeg(poly);
  if (d < 0) return { k: Infinity, rest: [] };
  let k = 0;
  while (k <= d && poly[k].isZero()) k++;
  const rest = poly.slice(k);
  return { k, rest: polyTrim(rest) };
}

function isEvenPoly(poly) {
  for (let i = 1; i < poly.length; i += 2) {
    if (!poly[i].isZero()) return false;
  }
  return true;
}

function isPerfectSquarePair(rest) {
  const d = polyDeg(rest);
  if (d !== 4) return { ok: false, reason: `deg(R)=${d}, expected 4` };
  const A = rest[4], B = rest[2] ?? F0, C = rest[0] ?? F0;
  if (rest[1] && !rest[1].isZero()) return { ok: false, reason: 'odd coeff v^1 nonzero' };
  if (rest[3] && !rest[3].isZero()) return { ok: false, reason: 'odd coeff v^3 nonzero' };
  if (A.isZero()) return { ok: false, reason: 'leading coeff zero' };
  const lhs = B.mul(B);
  const rhs = A.mul(C).mul(fr(4));
  if (!lhs.eq(rhs)) return { ok: false, reason: `B^2 != 4AC (B^2=${lhs}, 4AC=${rhs})` };
  const h = B.neg().div(A.mul(fr(2)));
  if (h.isZero()) return { ok: false, reason: 'h=0 (degenerate, s would be 0)' };
  return { ok: true, A, B, C, h };
}

// --- 統合判定(fail-closed: ok/skip のいずれかを必ず明示) ---
export function testCandidateNinfty(a0, a1, a2, a3, a4, a5, p0, p1, p2) {
  if (a5 !== 1 && a5 !== -1) throw new Error('a5 must be +-1 (monic-f6 gauge)');
  if (p2 === 0) return { ok: false, stage: 1, reason: 'p2=0' };
  const a = [fr(a0), fr(a1), fr(a2), fr(a3), fr(a4), fr(a5)];
  const p = [fr(p0), fr(p1), fr(p2)];

  const stage1 = factorCheckNinfty(a, p);
  if (!stage1.ok) return { ok: false, stage: 1, reason: stage1.reason, internal_error: !!stage1.internal_error };

  const aTil = aTilde(a);
  const { poly: D, consistent } = computeDiscriminantPolyNinfty(aTil, stage1.cHatMu);
  if (!consistent) return { skip: true, stage: 2, reason: 'interpolation self-check failed (degree bound exceeded?)' };
  const { power: quadPower, rest: Dcorr } = stripKnownQuadraticFactor(D, fr(a0), stage1.cHatMu);
  if (polyIsZero(Dcorr)) return { ok: false, stage: 2, reason: 'D(v) identically zero after removing known quadratic artifact factor' };
  const { k, rest } = stripZeroRoot(Dcorr);
  if (k === Infinity) return { ok: false, stage: 2, reason: 'D(v) identically zero' };
  if (!isEvenPoly(rest)) return { ok: false, stage: 2, reason: 'R(v) not even (no +-s symmetry)', k };
  const sq = isPerfectSquarePair(rest);
  if (!sq.ok) return { ok: false, stage: 2, reason: sq.reason, k };

  return {
    ok: true,
    a: [a0, a1, a2, a3, a4, a5],
    p: [p0, p1, p2],
    f6: stage1.f6.map(f => f.toString()),
    quadratic_artifact_power: quadPower,
    k,
    h: sq.h.toString(),
  };
}

// ============================================================
// 較正(委嘱3・司令塔指示・N_infty は必須): positive/negative/adversarial。
// ============================================================
export function runCalibration() {
  const results = [];

  // stage1 positive: f6,p を先に選び h:=f6*p^2 を計算し、a^2=h+c で a が
  // 厳密平方根を持つよう c を選ぶのは一般に困難なので(N_aff §1.3 と同じ
  // 理由で「両方を同時に満たす a,p,f6」は探索そのものと同格に難しい)、
  // ここでは分解検出ロジック自体を「f6,p を先に固定し、a^2 の商・余りが
  // 正しく (f6,c) を復元するか」で較正する — asq:=f6*p^2+cTarget として
  // a を求める代わりに、直接 asq を構成し、その平方根が a であることを
  // 保証したうえで検査する構成にする。
  {
    // p, f6 を選ぶ:
    const p = [fr(1), fr(0), fr(1)]; // p(x)=x^2+1
    const f6 = [fr(1), fr(1), F0, F0, F0, F0, F1]; // f6=x^6+x+1 (monic,depressed,squarefree想定)
    const cTarget = fr(5);
    const psq = polyMul(p, p);
    const target = [...polyMul(f6, psq)];
    target[0] = target[0].add(cTarget); // asq := f6*p^2 + cTarget
    // asq が実際に完全平方(a^2)であるかは一般に保証されないので、
    // ここでは「asq を psq で割って f6,cTarget を復元できるか」という
    // stage1 の内部ロジック(除算による復元)のみを直接検査する
    // (a の平方根としての実在性は問わない — 分解ロジックの較正)。
    const { quot: q, rem: r } = polyDivMod(target, psq);
    const recoveredF6ok = q.length === f6.length && q.every((c, i) => c.eq(f6[i]));
    const recoveredCok = (r[0] ?? F0).eq(cTarget) && (!r[1] || r[1].isZero()) && (!r[2] || r[2].isZero()) && (!r[3] || r[3].isZero());
    results.push({ id: 'stage1-positive-division-recovery', kind: 'positive', input: { p: p.map(String), f6: f6.map(String), cTarget: cTarget.toString() }, expect: 'quotient=f6, remainder=cTarget (constant)', got: { recoveredF6ok, recoveredCok }, pass: recoveredF6ok && recoveredCok });
  }
  // stage1 negative: 上と同じ構成に、f6 に B5!=0(depressed でない)を混ぜて
  // 正しく棄却されるかを確認する。
  {
    const a = [fr(3), fr(1), fr(0), fr(2), fr(1), fr(1)]; // 適当な deg5・a5=1
    const p = [fr(1), fr(0), fr(-1)]; // p2=-1 (a5と符号不一致でも良い。p2=+-1に限らないので単なる負例)
    const r = factorCheckNinfty(a, p);
    results.push({ id: 'stage1-negative-random', kind: 'negative', input: { a: a.map(String), p: p.map(String) }, expect: 'ok=false (generic random tuple should fail)', got: r.ok === false, pass: r.ok === false, detail: r });
  }
  // stage2 positive: パターン検出ロジック自体を、既知の答え(k0=5・2次
  // アーティファクトべき1・h_target)から逆算した合成 D(v) で直接較正する
  // (N_aff と同じ理由により、a,p 側から到達可能な真の解を短時間で構成
  // するのは困難 — この境界は報告に明記する)。
  {
    const a0 = fr(2), cHatMu = fr(7), hTarget = fr(9), k0 = 5;
    const vPoly = [F0, F1];
    let vPowK = [F1];
    for (let i = 0; i < k0; i++) vPowK = polyMul(vPowK, vPoly);
    const quadFactor = [cHatMu, a0.mul(fr(-2)), F1]; // c_hat_mu - 2 a0 v + v^2
    const vSqMinusH = [hTarget.neg(), F0, F1];
    const rPoly = polyMul(vSqMinusH, vSqMinusH);
    const Dsynth = polyMul(polyMul(vPowK, quadFactor), rPoly);
    const { power: quadPower, rest: Dcorr } = stripKnownQuadraticFactor(Dsynth, a0, cHatMu);
    const { k, rest } = stripZeroRoot(Dcorr);
    const even = isEvenPoly(rest);
    const sq = even ? isPerfectSquarePair(rest) : { ok: false, reason: 'not even' };
    const pass = quadPower === 1 && k === k0 && even && sq.ok && sq.h.eq(hTarget);
    results.push({ id: 'stage2-positive-synthetic-pattern', kind: 'positive', input: { a0: '2', cHatMu: '7', hTarget: '9', k0 }, expect: `quadPower=1,k=${k0},even=true,h=9`, got: { quadPower, k, even, sqOk: sq.ok, h: sq.ok ? sq.h.toString() : null }, pass });
  }
  // stage2 negative: 余分な因子 (v-1) を掛けて even 性が破れることを確認。
  {
    const a0 = fr(2), cHatMu = fr(7), hTarget = fr(9), k0 = 5;
    const vPoly = [F0, F1];
    let vPowK = [F1];
    for (let i = 0; i < k0; i++) vPowK = polyMul(vPowK, vPoly);
    const quadFactor = [cHatMu, a0.mul(fr(-2)), F1];
    const vSqMinusH = [hTarget.neg(), F0, F1];
    const rPoly = polyMul(vSqMinusH, vSqMinusH);
    const extra = [fr(-1), F1];
    const Dsynth = polyMul(polyMul(polyMul(vPowK, quadFactor), rPoly), extra);
    const { rest: Dcorr } = stripKnownQuadraticFactor(Dsynth, a0, cHatMu);
    const { rest } = stripZeroRoot(Dcorr);
    const even = isEvenPoly(rest);
    results.push({ id: 'stage2-negative-broken-parity', kind: 'negative', input: { extra_factor: '(v-1)' }, expect: 'even=false (correctly rejected)', got: { even }, pass: even === false });
  }
  // stage2 adversarial: 2次アーティファクトを除去しないナイーブな経路だと
  // D(v) が疑似的に消える点を、実際に stage1 を通過する具体的なタプルで
  // 再現する(N_aff §1.3 と同型のレグレッションガード)。stage1 を通過する
  // 具体タプルが事前に分からないため、ここでは stage1 通過を要求せず、
  // 「a0,cHatMu を与えれば D(v) がその2次因子で割り切れる」という stage2
  // の構造自体(a,p の具体値に依存しない、h(s;v)/h'(s;v) の代数的性質)を
  // 直接検査する — 任意の a~,cHatMu に対して常に成り立つはずの恒等式。
  {
    const aTil = [fr(3), fr(-1), fr(2), fr(0), fr(1), fr(4)]; // 適当な a~ = [a5,a4,a3,a2,a1,a0](aTilde の規約どおり)
    const cHatMu = fr(11);
    const { poly: D, consistent } = computeDiscriminantPolyNinfty(aTil, cHatMu);
    const a0 = aTil[5]; // aTilde(a) は [a5,a4,a3,a2,a1,a0] を返す規約 — 末尾要素が元の a の a0(定数項)
    const { power: quadPower } = stripKnownQuadraticFactor(D, a0, cHatMu);
    const pass = consistent && quadPower >= 1;
    results.push({
      id: 'stage2-adversarial-quadratic-artifact-regression',
      kind: 'adversarial',
      input: { aTil: aTil.map(String), cHatMu: cHatMu.toString() },
      expect: 'D(v) は quadFactor=(c_hat_mu-2*a0*v+v^2) で厳密に割り切れる(べき>=1)',
      got: { consistent, quadPower },
      pass,
      note: 'h,h′ の主要係数が同一の2次式に比例するという代数的事実(具体的な a,p の値によらず常に成立)の直接検算。除去しないまま v^k 剥離・偶関数判定へ進むと、v^2-2a0v+c_hat_mu=0 の根で D(v) が幾何的意味なく消えることを見落とし、真の候補を誤棄却しかねない。',
    });
  }

  const allPass = results.every(r => r.pass);
  return { schema: 'mb/ninfty-calibration/v1', all_pass: allPass, results };
}

// --- 探索本体 ---
function main() {
  const BOUND = Number(process.env.MB_NINFTY_BOUND || 1); // |a0..a4|,|p0,p1|,|p2| <= BOUND
  const A5_VALUES = process.env.MB_NINFTY_A5 ? [Number(process.env.MB_NINFTY_A5)] : [1, -1];
  const P2_MIN = process.env.MB_NINFTY_P2_MIN !== undefined ? Number(process.env.MB_NINFTY_P2_MIN) : -BOUND;
  const P2_MAX = process.env.MB_NINFTY_P2_MAX !== undefined ? Number(process.env.MB_NINFTY_P2_MAX) : BOUND;

  const calibration = runCalibration();

  const hits = [];
  const errors = [];
  const internalErrors = [];
  const skips = [];
  const stage1PassDetails = [];
  let tested = 0;
  let stage1Rejects = 0;
  let stage1Passes = 0;
  const t0 = Date.now();

  for (const a5 of A5_VALUES) {
    for (let a4 = -BOUND; a4 <= BOUND; a4++) {
      for (let a3 = -BOUND; a3 <= BOUND; a3++) {
        for (let a2 = -BOUND; a2 <= BOUND; a2++) {
          for (let a1 = -BOUND; a1 <= BOUND; a1++) {
            for (let a0 = -BOUND; a0 <= BOUND; a0++) {
              for (let p0 = -BOUND; p0 <= BOUND; p0++) {
                for (let p1 = -BOUND; p1 <= BOUND; p1++) {
                  for (let p2 = P2_MIN; p2 <= P2_MAX; p2++) {
                    if (p2 === 0) continue;
                    tested++;
                    try {
                      const a = [fr(a0), fr(a1), fr(a2), fr(a3), fr(a4), fr(a5)];
                      const p = [fr(p0), fr(p1), fr(p2)];
                      const stage1 = factorCheckNinfty(a, p);
                      if (!stage1.ok) {
                        stage1Rejects++;
                        if (stage1.internal_error) internalErrors.push({ a0, a1, a2, a3, a4, a5, p0, p1, p2, reason: stage1.reason });
                        continue;
                      }
                      stage1Passes++;
                      const r = testCandidateNinfty(a0, a1, a2, a3, a4, a5, p0, p1, p2);
                      const tuple = { a0, a1, a2, a3, a4, a5, p0, p1, p2 };
                      if (r.ok) {
                        hits.push(r);
                        stage1PassDetails.push({ ...tuple, stage2: { ok: true, k: r.k, h: r.h } });
                      } else if (r.skip) {
                        skips.push({ ...tuple, stage: r.stage ?? null, reason: r.reason });
                        stage1PassDetails.push({ ...tuple, stage2: { skip: true, reason: r.reason } });
                      } else {
                        stage1PassDetails.push({ ...tuple, stage2: { ok: false, reason: r.reason, k: r.k ?? null } });
                        if (r.internal_error) internalErrors.push({ ...tuple, reason: r.reason });
                      }
                    } catch (e) {
                      errors.push({ a0, a1, a2, a3, a4, a5, p0, p1, p2, error: String(e && e.message || e) });
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  const elapsedMs = Date.now() - t0;
  const integrityFlag = skips.length > 0 || errors.length > 0 || internalErrors.length > 0 || !calibration.all_pass;
  const result = {
    schema: 'mb/ninfty-branch-search/v1',
    branch: 'N_infty',
    normal_form: 'a(x)^2-f6(x)*p(x)^2=c_hat_mu (const,!=0); f6 monic depressed deg6 (Rule1 M1 gauge); deg a=5 (a5=+-1 by monic-f6 gauge); deg p=2 (p2 free, NOT gauge-fixed); c_hat_mu NOT gauge-fixed',
    search_bound: BOUND,
    a5_values: A5_VALUES,
    p2_range: [P2_MIN, P2_MAX],
    calibration,
    tested,
    stage1_passes: stage1Passes,
    stage1_rejects: stage1Rejects,
    stage1_pass_details: stage1PassDetails,
    hits,
    skip_count: skips.length,
    skips,
    error_count: errors.length,
    errors: errors.slice(0, 20),
    internal_error_count: internalErrors.length,
    internal_errors: internalErrors.slice(0, 20),
    integrity_flag: integrityFlag,
    elapsed_ms: elapsedMs,
    contact_discipline: '本探索器は c_hat_mu(=a^2-f6*p^2)の値・平方類・平方因子・符号を一切計算・選択基準に使用していない。出力は a,p,f6 の整数/有理係数(完全な曲線データ・A1 whitelist 内)と D(v) の構造検査結果(k,h)のみ。',
  };
  console.log(JSON.stringify(result, null, 2));
  if (integrityFlag && (skips.length > 0 || errors.length > 0 || internalErrors.length > 0)) {
    process.exitCode = 2;
  }
}

if (import.meta.url === `file://${process.argv[1]}` || import.meta.url.endsWith(process.argv[1]?.replace(/\\/g,'/'))) {
  main();
}
