// mb-naff-branch-search.mjs — 委嘱2(Model-Builder)探索器・副枝 (N_aff) 専用。
// 探索器(GAP と対にならぬ独立実装)。crosscheck/ の照合器とは非共有。
//
// ============================================================
// 数学的設計(S5 設計 v1.2 §3.3.4・Rule 1 v1.3 §2.2 M1/M2 に整合)
// ============================================================
//
// 正規形(3.3): a(x)^2 - c_N (x-x0)^5 = f6(x) p2(x)^2
//   N-0 前提: x0 = x(P0) は有限(副枝 (N_aff) の定義)。
//
// ゲージの使用(Rule 1 M1・S5 設計 §3.3.2/§3.3.4 と同型):
//   - x-平行移動: x0 = 0 に固定(Rule 1 M1 が (N_aff) について既にこれを課す
//     — "副枝(N_aff): 従来通り x-平行移動で x(P0)=0")。
//   - y-スケール(f6 を monic にする、Rule 1 M1 (N) 行): これは
//     deg(a)=5 を要求したうえで(a^2 の主要項からくる)f6cand の主係数が
//     a5^2 になることから、a5 = ±1 に固定することと同値である。
//   - mu-スケール(残る 1 自由度): c_N の平方類を変える作用であり、これを
//     使って c_N を特定値(例: -1)に固定することは sqfree(c_N) の計算を
//     要求する。sqfree(c_N) が (P1) を漏らすかどうかは S5 設計に明記が
//     ない(命題 S5-4/S5-4∞ は c および c_hat_mu についてのみ確立している)。
//     ★教材 3(S5 設計 §6.3)の教訓により、未確立の量は安全側に倒す:
//     本探索器は sqfree(c_N) を一度も計算せず、c_N を素朴な整数格子で
//     ブルートフォースする(ゲージで縮めない)。
//
// 判定アルゴリズム(厳密・浮動小数点不使用・2 段階):
//
// 段階 1(N-2/N-3/N-4 — 分解構造の必要条件):
//   h(x) := a(x)^2 - c_N x^5 (deg <=10, deg=10 は a5=+-1 だから恒真)
//   g := gcd(h, h')  を厳密 Euclid 互除法で計算。
//   deg(g) が厳密に 2 でなければ棄却(「動く二重根がちょうど 2 個」という
//   S5 設計の余次元 2 条件に対応)。
//   p2 := monic(g)。h を p2^2 で厳密除算し、余りが 0 でなければ棄却
//   (gcd の定義から通常 0 だが自己検算として実施)。
//   商 f6cand の次数が 6・monic でなければ棄却(N-4 の一部)。
//   f6cand が squarefree(gcd(f6cand,f6cand') が定数)でなければ棄却(N-2)。
//   gcd(f6cand,p2) が定数でなければ棄却(N-3)。
//
// 段階 2(mu の分岐型 (5,2^2 1,2^2 1,5) — S5-1/S5-2/S5-2a の必要十分条件):
//   mu のファイバー方程式(3.1 の恒等式を使って x^6..x^10 の項が落ちた後の
//   厳密な代数的帰結・枝 (W) の f(x;v) と同型):
//     g(x;v) := c_N x^5 - 2 v a(x) + v^2 = 0
//   ここで a の次数が 5 なので、g(x;v) の x^5 係数 (c_N - 2 v a5) は v に
//   依存する(枝 (W) では a の次数が <=2 だったので常に係数 1 で v 非依存
//   だった — この差異が本探索器の固有の技術的注意点)。同様に g'(x;v) の
//   x^4 係数 (5 c_N - 10 v a5) も v 依存。ゆえに resultant(g,g') を
//   「実際の次数を都度 trim する」実装(枝 (W) 用の関数をそのまま流用)は
//   誤り — 特殊な v(= c_N/(2 a5)、これは mu(infty_-) の値に一致する
//   幾何的に意味のある点)で次数が落ち、補間が破綻する。
//   本探索器は **固定次数(5,4)の Sylvester 行列**で resultant を計算し、
//   この破綻を回避する(下記 resultantFixedDeg)。
//
//   D(v) := resultantFixedDeg(g(x;v), g'(x;v)) を 21 点の厳密有理数
//   Lagrange 補間で再構成し(次数上界 13 の余裕をもって 16 に設定)、
//   追加点で自己検算する。v=0 での重複度 k を割り、R(v):=D(v)/v^k が
//   ちょうど A v^4+B v^2+C(奇数次係数 0)かつ B^2=4AC を満たせば候補とする。
//
// 禁止事項の遵守: 本探索器は c_N の平方類・平方因子・符号を一切「計算・
// 選択基準に使用」していない(ブルートフォースの格子点として扱うのみ)。
// lambda=c*mu^2 の c、c_hat_mu = a^2-f6*p2^2 のいずれも計算・出力していない
// (段階 1 で得る f6cand は曲線方程式そのものであり A1 whitelist 内)。

import { Frac, F0, F1, polyTrim, polyDeg, polyEval, detFrac, lagrangeInterpolate } from './mb-frac.mjs';
import { polyAdd, polySub, polyMul, polyScale, polyDerivative, polyDivMod, polyGCD, polyMonic, polyIsZero, polyToString } from './mb-polyops.mjs';

function fr(x) { return Frac.from(x); }

// --- 段階 1: h(x)=a(x)^2-c_N x^5 の分解構造検査 ---

function xPow(n) {
  const arr = new Array(n + 1).fill(F0);
  arr[n] = F1;
  return arr;
}

export function factorCheck(aCoeffs /* [a0..a5] Frac */, cN /* Frac */) {
  const a = aCoeffs;
  const h = polySub(polyMul(a, a), polyScale(xPow(5), cN));
  const dH = polyDeg(h);
  if (dH !== 10) return { ok: false, reason: `deg(h)=${dH}, expected 10` };
  const hp = polyDerivative(h);
  const g = polyGCD(h, hp);
  const dg = polyDeg(g);
  if (dg !== 2) return { ok: false, reason: `deg(gcd(h,h'))=${dg}, expected 2` };
  const p2 = polyMonic(g);
  const p2sq = polyMul(p2, p2);
  const { quot: f6cand, rem } = polyDivMod(h, p2sq);
  if (!polyIsZero(rem)) return { ok: false, reason: 'h not exactly divisible by p2^2 (internal inconsistency)', internal_error: true };
  const df6 = polyDeg(f6cand);
  if (df6 !== 6) return { ok: false, reason: `deg(f6cand)=${df6}, expected 6` };
  if (!f6cand[6].eq(F1)) return { ok: false, reason: `f6cand not monic (lc=${f6cand[6]})` };
  // squarefree check
  const f6p = polyDerivative(f6cand);
  const sf = polyGCD(f6cand, f6p);
  if (polyDeg(sf) > 0) return { ok: false, reason: `f6cand not squarefree (deg gcd(f6,f6')=${polyDeg(sf)})` };
  // coprimality N-3
  const cop = polyGCD(f6cand, p2);
  if (polyDeg(cop) > 0) return { ok: false, reason: `gcd(f6cand,p2) has degree ${polyDeg(cop)} (N-3 fails)` };
  return { ok: true, p2, f6cand };
}

// --- 段階 2: mu の分岐型判定(固定次数 resultant) ---

// g(x;v) の係数(低次->高次、長さ6固定, x^0..x^5)。a5 = leading coeff of a.
function gPolyAtV(a, cN, v) {
  const [a0, a1, a2, a3, a4, a5] = a;
  const c0 = v.mul(v).sub(v.mul(fr(2)).mul(a0));
  const c1 = v.mul(fr(-2)).mul(a1);
  const c2 = v.mul(fr(-2)).mul(a2);
  const c3 = v.mul(fr(-2)).mul(a3);
  const c4 = v.mul(fr(-2)).mul(a4);
  const c5 = cN.sub(v.mul(fr(2)).mul(a5));
  return [c0, c1, c2, c3, c4, c5];
}
// g'(x;v) の係数(低次->高次、長さ5固定, x^0..x^4)。
function gPrimePolyAtV(a, cN, v) {
  const [a0, a1, a2, a3, a4, a5] = a;
  const c0 = v.mul(fr(-2)).mul(a1);
  const c1 = v.mul(fr(-4)).mul(a2);
  const c2 = v.mul(fr(-6)).mul(a3);
  const c3 = v.mul(fr(-8)).mul(a4);
  const c4 = cN.mul(fr(5)).sub(v.mul(fr(10)).mul(a5));
  return [c0, c1, c2, c3, c4];
}

// 固定次数の resultant(次数を都度 trim しない — v に応じた主係数の消滅を
// 正しく扱う。fFixedLen/gFixedLen はそれぞれ配列長(= 次数+1)。
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

// D(v) を 21 点の厳密補間で再構成(次数上界: n*d_f+m*d_g = 4*2+5*1=13 の
// 余裕をもって 16 とする)。追加 1 点で自己検算。
export function computeDiscriminantPolyNaff(a, cN) {
  const DEG_BOUND = 16;
  const numPts = DEG_BOUND + 1;
  const xs = [];
  for (let i = 0; i <= DEG_BOUND; i++) {
    const k = Math.ceil(i / 2);
    xs.push(i === 0 ? 0n : (i % 2 === 1 ? BigInt(k) : -BigInt(k)));
  }
  const ys = xs.map(v => {
    const vF = fr(v);
    const f = gPolyAtV(a, cN, vF);
    const g = gPrimePolyAtV(a, cN, vF);
    return resultantFixedDeg(f, 6, g, 5);
  });
  const poly = lagrangeInterpolate(xs.map(x => fr(x)), ys);
  const checkX = BigInt(DEG_BOUND + 5);
  const vF = fr(checkX);
  const f = gPolyAtV(a, cN, vF);
  const g = gPrimePolyAtV(a, cN, vF);
  const actual = resultantFixedDeg(f, 6, g, 5);
  const predicted = polyEval(poly, checkX);
  const consistent = actual.eq(predicted);
  return { poly, consistent };
}

// ★ 必須の補正(自己検算で発見・§ 末尾の報告に記録): g(x;v) の x^5 係数
// (c_N-2*a5*v) と g'(x;v) の x^4 係数(5*(c_N-2*a5*v)、同じ線形式に比例)は
// 同一の v = c_N/(2 a5) で同時に消える。これは x=infty(具体的には infty_-)
// が「射影的な意味での共通根」になる特異点であり、その v は mu(infty_-) の
// 値(有限)に一致する — 幾何的には mu の分岐点では**ない**(infty_- は
// passport の 4 分岐点 {0,s,-s,infty} のいずれでもない一般の点)。
// ところが固定次数 Sylvester 行列で計算した D(v)=Res_{5,4}(g,g') は、この
// v で機械的に 0 になる(実際に計算して確認: 具体例で power=1 の
// (c_N-2 a5 v) 因子を持つ)。これを除かずに v^k 剥離・偶関数判定へ進むと、
// **正当な候補まで誤って棄却する**(false negative)ため、パターン判定の
// 前に、この既知の線形因子を割り切れる限り除去する。
function stripKnownLinearFactor(poly, cN, a5) {
  const lin = [cN, fr(-2).mul(a5)]; // c_N - 2*a5*v  (低次->高次)
  let cur = poly;
  let power = 0;
  while (polyDeg(cur) >= 1) {
    const { quot, rem } = polyDivMod(cur, lin);
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

// --- 統合判定 ---
export function testCandidateNaff(a0, a1, a2, a3, a4, a5, cN) {
  if (a5 !== 1 && a5 !== -1) throw new Error('a5 must be +-1 (monic-f6 gauge)');
  if (cN === 0) return { skip: true, reason: 'c_N=0 (norm would be trivial)' };
  const a = [fr(a0), fr(a1), fr(a2), fr(a3), fr(a4), fr(a5)];
  const cNf = fr(cN);

  // 段階1: 分解構造
  const stage1 = factorCheck(a, cNf);
  if (!stage1.ok) return { ok: false, stage: 1, reason: stage1.reason, internal_error: !!stage1.internal_error };

  // 段階2: mu の分岐型
  const { poly: D, consistent } = computeDiscriminantPolyNaff(a, cNf);
  if (!consistent) return { skip: true, reason: 'interpolation self-check failed (degree bound exceeded?)' };
  // 既知の線形因子 (c_N-2*a5*v)(= x=infty_- での射影的アーティファクト。
  // 幾何的分岐点ではない)を先に除去する。
  const { power: linPower, rest: Dcorr } = stripKnownLinearFactor(D, cNf, a[5]);
  if (polyIsZero(Dcorr)) return { ok: false, stage: 2, reason: 'D(v) identically zero after removing known linear artifact factor' };
  const { k, rest } = stripZeroRoot(Dcorr);
  if (k === Infinity) return { ok: false, stage: 2, reason: 'D(v) identically zero' };
  if (!isEvenPoly(rest)) return { ok: false, stage: 2, reason: 'R(v) not even (no +-s symmetry)', k };
  const sq = isPerfectSquarePair(rest);
  if (!sq.ok) return { ok: false, stage: 2, reason: sq.reason, k };

  return {
    ok: true,
    a: [a0, a1, a2, a3, a4, a5],
    c_N: cN,
    p2: stage1.p2.map(f => f.toString()),
    f6: stage1.f6cand.map(f => f.toString()),
    linear_artifact_power: linPower,
    k,
    h: sq.h.toString(),
  };
}

// --- 探索本体 ---
function main() {
  const BOUND = Number(process.env.MB_NAFF_BOUND || 2); // |a0..a4|,|c_N| <= BOUND
  const A5_VALUES = process.env.MB_NAFF_A5 ? [Number(process.env.MB_NAFF_A5)] : [1, -1];
  const CN_MIN = process.env.MB_NAFF_CN_MIN !== undefined ? Number(process.env.MB_NAFF_CN_MIN) : -BOUND;
  const CN_MAX = process.env.MB_NAFF_CN_MAX !== undefined ? Number(process.env.MB_NAFF_CN_MAX) : BOUND;
  const hits = [];
  const errors = [];
  const internalErrors = [];
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
              for (let cN = CN_MIN; cN <= CN_MAX; cN++) {
                if (cN === 0) continue;
                tested++;
                try {
                  // 段階1のみ先に軽く走らせて足切り(段階2は高コスト)
                  const a = [fr(a0), fr(a1), fr(a2), fr(a3), fr(a4), fr(a5)];
                  const stage1 = factorCheck(a, fr(cN));
                  if (!stage1.ok) {
                    stage1Rejects++;
                    if (stage1.internal_error) internalErrors.push({ a0, a1, a2, a3, a4, a5, cN, reason: stage1.reason });
                    continue;
                  }
                  stage1Passes++;
                  const r = testCandidateNaff(a0, a1, a2, a3, a4, a5, cN);
                  if (r.ok) hits.push(r);
                  else if (r.internal_error) internalErrors.push({ a0, a1, a2, a3, a4, a5, cN, reason: r.reason });
                } catch (e) {
                  errors.push({ a0, a1, a2, a3, a4, a5, cN, error: String(e && e.message || e) });
                }
              }
            }
          }
        }
      }
    }
  }
  const elapsedMs = Date.now() - t0;
  const result = {
    schema: 'mb/naff-branch-search/v1',
    branch: 'N_aff',
    normal_form: 'a(x)^2-c_N*x^5=f6(x)*p2(x)^2 (x0=0 by translation gauge, a5=+-1 by monic-f6 gauge, c_N NOT gauge-fixed)',
    search_bound: BOUND,
    a5_values: A5_VALUES,
    cn_range: [CN_MIN, CN_MAX],
    tested,
    stage1_passes: stage1Passes,
    stage1_rejects: stage1Rejects,
    hits,
    error_count: errors.length,
    errors: errors.slice(0, 20),
    internal_error_count: internalErrors.length,
    internal_errors: internalErrors.slice(0, 20),
    elapsed_ms: elapsedMs,
    contact_discipline: '本探索器は c_N の平方類・平方因子・符号、lambda=c*mu^2 の c、c_hat_mu=a^2-f6*p2^2 のいずれも計算・選択基準に使用していない。出力は a,c_N,p2,f6 の整数/有理係数(完全な曲線データ・A1 whitelist 内)と D(v) の構造検査結果(k,h)のみ。',
  };
  console.log(JSON.stringify(result, null, 2));
}

if (import.meta.url === `file://${process.argv[1]}` || import.meta.url.endsWith(process.argv[1]?.replace(/\\/g,'/'))) {
  main();
}
