#!/usr/bin/env node
// crosscheck/build-frozen-bundles.mjs -- R-7 修理(裁定 38/便 37 F2 blocker 1)。
//
// 目的: 副枝 (N_infty) の M=3 unit test / M=10 production 較正それぞれについて、
// pathA(GAP・search/u-extract-pathA-ninf-*-driver.g)にも pathB(node・
// crosscheck/u-extract-pathB-ninf-*-driver.mjs)にも属さない**第三の独立実装**
// で canonical_model_string + expected_model_digest を計算し、
// certificates/k5pipeline/<id>-bundle.json として保存する。
//
// 便 37 F2 が指摘した攻撃: 「二 driver が同じ誤転記をすれば、raw の
// echo field から自己生成した expected_model_digest 同士が一致するだけで
// ACCEPT してしまう」。この bundle は pathA/pathB のどちらのコードとも
// 独立に(有理数クラス・多項式演算を本ファイル内で再実装して)同じ
// 数学的定義(a, p, f, A, B の式そのもの)から出発するので、pathA/pathB
// 両方に**共通の**コードバグがあってもこの bundle には伝播しない。
// 第三 checker (crosscheck/u-compare-ninf.mjs) はこの bundle をファイル
// として読み、raw 二本の recomputed canonical string と逐語一致するかを
// 検査する(§6.3-5 (5)・I-l)。
//
// 独立性: 本ファイルは search/u-extract-pathA.g のコードも
// crosscheck/u-extract-pathB-lib.mjs のコードも import/参照しない。
// 有理数・多項式演算は本ファイル内で完結する(node crypto の createHash
// のみ共有 -- アルゴリズム本体ではない)。
//
// 実行: node crosscheck/build-frozen-bundles.mjs
// (この bundle は一度生成したら凍結物として扱う -- 較正の度に再生成して
//  上書きしない。値を変える場合は新しい id/version を切ること。)

import { writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

function gcdBig(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { [a, b] = [b, a % b]; } return a; }
class R {
  constructor(n, d = 1n) {
    if (typeof n === 'number') n = BigInt(n);
    if (typeof d === 'number') d = BigInt(d);
    if (d === 0n) throw new Error('R: zero denominator');
    if (d < 0n) { n = -n; d = -d; }
    const g = gcdBig(n, d) || 1n;
    this.n = n / g; this.d = d / g;
  }
  add(o) { return new R(this.n * o.d + o.n * this.d, this.d * o.d); }
  sub(o) { return new R(this.n * o.d - o.n * this.d, this.d * o.d); }
  mul(o) { return new R(this.n * o.n, this.d * o.d); }
  eq(o) { return this.n * o.d === o.n * this.d; }
  isZero() { return this.n === 0n; }
  toString() { return this.d === 1n ? `${this.n}` : `${this.n}/${this.d}`; }
}
const R0 = new R(0n);
const R1 = new R(1n);
function toR(intList) { return intList.map((x) => new R(BigInt(x))); }
function trim(a) { const r = a.slice(); while (r.length > 1 && r[r.length - 1].isZero()) r.pop(); return r; }
function padd(a, b) { const n = Math.max(a.length, b.length); const r = []; for (let i = 0; i < n; i++) r.push((a[i] ?? R0).add(b[i] ?? R0)); return trim(r); }
function psub(a, b) { const n = Math.max(a.length, b.length); const r = []; for (let i = 0; i < n; i++) r.push((a[i] ?? R0).sub(b[i] ?? R0)); return trim(r); }
function pmul(a, b) { const r = Array.from({ length: a.length + b.length - 1 }, () => R0); for (let i = 0; i < a.length; i++) for (let j = 0; j < b.length; j++) r[i + j] = r[i + j].add(a[i].mul(b[j])); return trim(r); }
function pscale(a, c) { return a.map((x) => x.mul(c)); }

function canonicalNinf(id, M, f, A, B) {
  const s = (x) => x.toString();
  const list = (xs) => xs.map(s).join(',');
  return `id=${id};branch=N_infty;M=${M};f=[${list(f)}];A=[${list(A)}];B=[${list(B)}]`;
}
function digestOf(str) { return createHash('sha256').update(str, 'utf8').digest('hex'); }

function buildNinfBundle(id, M, f, A, B, mode) {
  const canonical_model_string = canonicalNinf(id, M, f, A, B);
  const expected_model_digest = digestOf(canonical_model_string);
  return {
    schema: 'k5pipeline/frozen-bundle/v1',
    mode,
    id,
    branch: 'N_infty',
    canonical_model_string,
    expected_model_digest,
    note: '本 bundle は search/u-extract-pathA-ninf-*-driver.g / crosscheck/u-extract-pathB-ninf-*-driver.mjs のどちらのコードとも独立な第三実装(本ファイル build-frozen-bundles.mjs)で計算した。第三 checker (crosscheck/u-compare-ninf.mjs) はこのファイルを第三引数として読み、二 raw の recomputed canonical string がこの canonical_model_string と逐語一致するかを検査する(便37 F2/I-l)。',
  };
}

// ---- toy M=3 (unit test): A(x) = x^3+x+1, B(x) = 1, f(x) = A(x)^2 - 1 ----
{
  const A = toR([1, 1, 0, 1]);
  const B = toR([1]);
  const f = trim(psub(pmul(A, A), [R1]));
  const bundle = buildNinfBundle('toy-ninf-M3', 3, f, A, B, 'calibration');
  writeFileSync('certificates/k5pipeline/toy-ninf-M3-bundle.json', JSON.stringify(bundle, null, 2) + '\n');
  console.log('wrote certificates/k5pipeline/toy-ninf-M3-bundle.json  expected_model_digest =', bundle.expected_model_digest);
}

// ---- production M=10: p := 1+x^2, a := 1+x(x^2+1)^2, f := 2x+x^2 p^2,
//      A := 2a^2-1, B := 2ap (lambda = mu^2, mu = a+p*y) ----
{
  const p = toR([1, 0, 1]);
  const xpoly = toR([0, 1]);
  const a = toR([1, 1, 0, 2, 0, 1]);
  const f = trim(padd(pscale(xpoly, new R(2n)), pmul(pmul(xpoly, xpoly), pmul(p, p))));
  const chatMu = trim(psub(pmul(a, a), pmul(f, pmul(p, p))));
  if (chatMu.length !== 1 || !chatMu[0].eq(R1)) {
    throw new Error(`build-frozen-bundles: a^2-f*p^2 must be the constant 1 (mu-side norm), got [${chatMu.map(String).join(',')}]`);
  }
  const A = trim(psub(pscale(pmul(a, a), new R(2n)), [R1]));
  const B = trim(pscale(pmul(a, p), new R(2n)));
  const bundle = buildNinfBundle('prod-ninf-M10', 10, f, A, B, 'production');
  writeFileSync('certificates/k5pipeline/prod-ninf-M10-bundle.json', JSON.stringify(bundle, null, 2) + '\n');
  console.log('wrote certificates/k5pipeline/prod-ninf-M10-bundle.json  expected_model_digest =', bundle.expected_model_digest);
}
