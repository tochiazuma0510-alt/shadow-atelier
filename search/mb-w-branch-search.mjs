// mb-w-branch-search.mjs — 委嘱1(Model-Builder)探索器・枝 (W) 専用。
// 探索器(GAP と対にならぬ独立実装)。 crosscheck/ の照合器とは非共有。
//
// 正規形(Rule 1 v1.3 (3.2') / S5 設計 v1.2 §3.3.2、Rule 1 に依存しない M-A のみを使用):
//   C: y^2 = a(x)^2 + x^5,  a(x) = a0 + a1 x + a2 x^2 (deg a <= 2)
//   mu = a(x) + y  (deg 5 map to P^1_mu, S5-2/S5-2a: monodromy D5)
//
// mu のファイバー: mu = v <=> y = v - a(x) かつ y^2 = a(x)^2+x^5
//   => (v-a(x))^2 = a(x)^2 + x^5
//   => v^2 - 2v a(x) = x^5
//   => f(x;v) := x^5 + 2v a(x) - v^2 = 0   (v ごとに次数 5 の quintic — mu の
//      ファイバーそのもの)
//
// mu の分岐点(v の値)は f(x;v) の判別式(x に関する)D(v) の根である。
// v=0 は ord_{P0}(mu)=5 に対応する既知の分岐点(x^5=0 の 5 重根)。
// S5-2a(命題)は「mu の分岐は {0,s,-s,infty}、局所型 (5,2^2 1,2^2 1,5)」と
// 主張する。これが成り立つための **exact 判定可能な必要十分条件**(この
// 正規形の中で)は:
//   D(v) / v^k  が v の**偶関数**であり、かつ厳密に
//     D(v)/v^k = c * (v^2 - h)^2   (c,h は有理数、h は h!=0)
//   という形にちょうど一致すること(他の根が一切無いこと)。
// これは Riemann-Hurwitz(枝(W)の mu: 2g-2 = -10 + ram, g=2 => ram=12,
// 0/infty で 4+4=8, 残り 4 は 2 点 x 各 ram=2(型 2^2,1)でちょうど埋まる)
// から従う exact な言明であり、S5 設計にも Rule 1 にも新たな依存を追加しない
// (独立に導出可能な判別式の代数的事実)。
//
// 禁止事項の遵守: 本探索器は c(lambda=c*mu^2 の定数)・その平方類・平方因子・
// 符号を一切計算・出力・選択基準に用いない。出力するのは a(x) の係数と
// D(v) の構造検査結果のみ。

import { Frac, F0, F1, polyTrim, polyDeg, polyEval, detFrac, lagrangeInterpolate } from './mb-frac.mjs';

function fr(x) { return Frac.from(x); }

// f(x;v) の係数(x の低次->高次, Frac[])を、a=(a0,a1,a2) と数値 v(Frac) から作る。
function fCoeffsAtV(a, v) {
  const [a0, a1, a2] = a;
  // f = x^5 + 2v*a2 x^2 + 2v*a1 x + (2v*a0 - v^2)
  const c0 = v.mul(2).mul(a0).sub(v.mul(v));
  const c1 = v.mul(2).mul(a1);
  const c2 = v.mul(2).mul(a2);
  return [c0, c1, c2, F0, F1]; // x^0..x^4=0 except c2 at x^2, x^5 coeff separate below? wait need length 6
}

// 上のヘルパーは長さ6 (x^0..x^5) で返すべき。修正:
function fPolyAtV(a, v) {
  const [a0, a1, a2] = a;
  const c0 = v.mul(fr(2)).mul(a0).sub(v.mul(v));
  const c1 = v.mul(fr(2)).mul(a1);
  const c2 = v.mul(fr(2)).mul(a2);
  return [c0, c1, c2, F0, F0, F1]; // x^0,x^1,...,x^5
}
function fPrimePolyAtV(a, v) {
  // f' = 5x^4 + 4v a2 x + 2v a1
  const [a0, a1, a2] = a;
  const c0 = v.mul(fr(2)).mul(a1);
  const c1 = v.mul(fr(4)).mul(a2);
  return [c0, c1, F0, F0, fr(5)]; // x^0..x^4
}

// resultant(f,g) with f,g given low-to-high Frac[] arrays (trimmed internally).
function resultant(fLow, gLow) {
  const f = polyTrim(fLow);
  const g = polyTrim(gLow);
  const df = polyDeg(f);
  const dg = polyDeg(g);
  if (df < 0 || dg < 0) throw new Error('resultant: zero polynomial input');
  // convert to high-to-low arrays for standard Sylvester construction
  const fHigh = []; for (let i = df; i >= 0; i--) fHigh.push(f[i]);
  const gHigh = []; for (let i = dg; i >= 0; i--) gHigh.push(g[i]);
  const n = df + dg;
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

// D(v) を厳密に補間で再構成する。次数上限を保守的に 16 とし、17 点で補間、
// 18 点目で自己検算(一致すれば信頼できる)。
export function computeDiscriminantPoly(a) {
  const DEG_BOUND = 16;
  const numPts = DEG_BOUND + 1;
  const xs = [];
  for (let i = 0; i <= DEG_BOUND; i++) {
    // 0, 1,-1,2,-2,... の順で使う(小さい整数優先)
    const k = Math.ceil(i / 2);
    xs.push(i === 0 ? 0n : (i % 2 === 1 ? BigInt(k) : -BigInt(k)));
  }
  const ys = xs.map(v => {
    const vF = fr(v);
    const f = fPolyAtV(a, vF);
    const g = fPrimePolyAtV(a, vF);
    return resultant(f, g);
  });
  const poly = lagrangeInterpolate(xs.map(x => fr(x)), ys);
  // 自己検算: 追加の 1 点で一致するか
  const checkX = BigInt(DEG_BOUND + 5);
  const vF = fr(checkX);
  const f = fPolyAtV(a, vF);
  const g = fPrimePolyAtV(a, vF);
  const actual = resultant(f, g);
  const predicted = polyEval(poly, checkX);
  const consistent = actual.eq(predicted);
  return { poly, consistent };
}

// D(v) の v=0 における根の重複度と、それを除いた R(v) を返す。
export function stripZeroRoot(poly) {
  const d = polyDeg(poly);
  if (d < 0) return { k: Infinity, rest: [] }; // D identically zero: 特異(除外)
  let k = 0;
  while (k <= d && poly[k].isZero()) k++;
  const rest = poly.slice(k);
  return { k, rest: polyTrim(rest) };
}

// R(v) が「奇数次係数がすべて 0」かどうか
function isEvenPoly(poly) {
  for (let i = 1; i < poly.length; i += 2) {
    if (!poly[i].isZero()) return false;
  }
  return true;
}

// 判定: R(v) が厳密に c*(v^2-h)^2 (次数ちょうど4、c!=0,h!=0) の形か。
// R(v) = C + B v^2 + A v^4 (奇数次はチェック済み前提)
function isPerfectSquarePair(rest) {
  const d = polyDeg(rest);
  if (d !== 4) return { ok: false, reason: `deg(R)=${d}, expected 4` };
  const A = rest[4], B = rest[2] ?? F0, C = rest[0] ?? F0;
  if (rest[1] && !rest[1].isZero()) return { ok: false, reason: 'odd coeff v^1 nonzero' };
  if (rest[3] && !rest[3].isZero()) return { ok: false, reason: 'odd coeff v^3 nonzero' };
  if (A.isZero()) return { ok: false, reason: 'leading coeff zero' };
  // perfect square in w=v^2: A w^2 + B w + C = A (w - h)^2  <=> B^2 = 4AC and h = -B/(2A)
  const lhs = B.mul(B);
  const rhs = A.mul(C).mul(fr(4));
  if (!lhs.eq(rhs)) return { ok: false, reason: `B^2 != 4AC (B^2=${lhs}, 4AC=${rhs})` };
  const h = B.neg().div(A.mul(fr(2)));
  if (h.isZero()) return { ok: false, reason: 'h=0 (degenerate, s would be 0)' };
  return { ok: true, A, B, C, h };
}

// 汎用版(a を Frac[3] で直接受ける — 委嘱2 の非整数有理数拡張が再利用する)。
export function testCandidateFrac(aFrac, label) {
  const [a0f, a1f, a2f] = aFrac;
  if (a0f.isZero() && a1f.isZero() && a2f.isZero()) return { skip: true, reason: 'a=0 identically' };
  const { poly: D, consistent } = computeDiscriminantPoly(aFrac);
  if (!consistent) return { skip: true, reason: 'interpolation self-check failed (degree bound exceeded?)' };
  const { k, rest } = stripZeroRoot(D);
  if (k === Infinity) return { skip: true, reason: 'D(v) identically zero (curve singular for all v?)' };
  if (!isEvenPoly(rest)) return { ok: false, reason: 'R(v) not even (no +-s symmetry)', k };
  const sq = isPerfectSquarePair(rest);
  if (!sq.ok) return { ok: false, reason: sq.reason, k };
  return { ok: true, k, h: sq.h.toString(), a0: a0f.toString(), a1: a1f.toString(), a2: a2f.toString(), label };
}

export function testCandidate(a0, a1, a2) {
  const a = [fr(a0), fr(a1), fr(a2)];
  if (a2 === 0 && a1 === 0 && a0 === 0) return { skip: true, reason: 'a=0 identically' };
  const { poly: D, consistent } = computeDiscriminantPoly(a);
  if (!consistent) return { skip: true, reason: 'interpolation self-check failed (degree bound exceeded?)' };
  const { k, rest } = stripZeroRoot(D);
  if (k === Infinity) return { skip: true, reason: 'D(v) identically zero (curve singular for all v?)' };
  if (!isEvenPoly(rest)) return { ok: false, reason: 'R(v) not even (no +-s symmetry)', k };
  const sq = isPerfectSquarePair(rest);
  if (!sq.ok) return { ok: false, reason: sq.reason, k };
  return { ok: true, k, h: sq.h.toString(), a0, a1, a2 };
}

// --- 探索本体 ---
// fail-closed 修理(委嘱3・検収指摘と同型の穴を W 側でも発見・是正):
// testCandidate の {skip:true} 経路が hits にも errors にも入らず証明書から
// 黙って消えていた。skip_count/skips と integrity_flag を追加する。
function main() {
  const BOUND = Number(process.env.MB_W_BOUND || 6); // 正の探索・非網羅: |a_i| <= BOUND の整数格子
  const hits = [];
  const errors = [];
  const skips = [];
  let tested = 0;
  const t0 = Date.now();
  for (let a2 = -BOUND; a2 <= BOUND; a2++) {
    for (let a1 = -BOUND; a1 <= BOUND; a1++) {
      for (let a0 = -BOUND; a0 <= BOUND; a0++) {
        if (a0 === 0 && a1 === 0 && a2 === 0) continue;
        tested++;
        try {
          const r = testCandidate(a0, a1, a2);
          if (r.ok) hits.push(r);
          else if (r.skip) skips.push({ a0, a1, a2, reason: r.reason });
        } catch (e) {
          errors.push({ a0, a1, a2, error: String(e && e.message || e) });
        }
      }
    }
  }
  const elapsedMs = Date.now() - t0;
  const integrityFlag = skips.length > 0 || errors.length > 0;
  const result = {
    schema: 'mb/w-branch-search/v2',
    branch: 'W',
    normal_form: 'y^2=a(x)^2+x^5, a=(a0,a1,a2), a2 x^2+a1 x+a0',
    search_bound: BOUND,
    tested,
    hits,
    skip_count: skips.length,
    skips,
    error_count: errors.length,
    errors: errors.slice(0, 20),
    integrity_flag: integrityFlag,
    elapsed_ms: elapsedMs,
    contact_discipline: '本探索器は c(lambda=c*mu^2 の定数)の値・平方類・平方因子・符号を一切計算していない。出力は a(x) の整数係数と D(v) の構造検査結果(k, h)のみ。',
  };
  console.log(JSON.stringify(result, null, 2));
  if (integrityFlag) process.exitCode = 2;
}

if (import.meta.url === `file://${process.argv[1]}` || import.meta.url.endsWith(process.argv[1]?.replace(/\\/g,'/'))) {
  main();
}

