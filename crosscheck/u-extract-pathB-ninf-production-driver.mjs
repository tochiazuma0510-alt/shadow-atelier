#!/usr/bin/env node
// crosscheck/u-extract-pathB-ninf-production-driver.mjs -- R-5 production 較正(M=10, synthetic)
// 委嘱: 便 36 F3.2/F6-1(裁定_37_ben36 の最小条件 1)。Sol 提供の exact synthetic
// fixture で extractPathB_Ninf(crosscheck/u-extract-pathB-lib.mjs・schema v2)
// を production-degree で叩く。search/u-extract-pathA-ninf-production-
// driver.g とは独立実装(級数を一切使わない多項式演算のみ・BigInt 有理数
// クラスも別実装)。
//
// *** SYNTHETIC(合成の較正例)であることを明記(便 36 F3.2 の言明) ***
// p := x^2+1、a := 1+x(x^2+1)^2、f := 2x+x^2(x^2+1)^2 = x^6+2x^4+x^2+2x。
// a^2-f p^2 = 1(mu の norm 定数)、gcd(f,f') = 1。y^2=f、mu=a+p y、
// lambda=mu^2=A+B y with A=2a^2-1, B=2ap: deg A=10, deg B=7, b_7=a_10=2,
// A^2-B^2 f = 1 (= chat)。以下は K^(5) の Belyi 候補・係数・数値近似では
// **ない**(封印前の合成 unit fixture)。
//
// A, B はこの driver が a, p, f から Q クラスの多項式演算でその場で導出する
// (GAP 側 production driver と同じ定義式から独立に再計算 -- 手転記による
// 誤記の余地を減らす)。
//
// 実行: node crosscheck/u-extract-pathB-ninf-production-driver.mjs

import { writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Q, loadModelNinf, extractPathB_Ninf } from './u-extract-pathB-lib.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

// ---- local (independent) plain-polynomial helpers over Q (ascending coeff arrays) ----
const Q0 = new Q(0n);
function ptrim(c) { const r = c.slice(); while (r.length > 1 && r[r.length - 1].isZero()) r.pop(); return r; }
function padd(a, b) { const n = Math.max(a.length, b.length); const r = []; for (let i = 0; i < n; i++) r.push((a[i] ?? Q0).add(b[i] ?? Q0)); return ptrim(r); }
function psub(a, b) { const n = Math.max(a.length, b.length); const r = []; for (let i = 0; i < n; i++) r.push((a[i] ?? Q0).sub(b[i] ?? Q0)); return ptrim(r); }
function pmul(a, b) { const r = Array.from({ length: a.length + b.length - 1 }, () => Q0); for (let i = 0; i < a.length; i++) for (let j = 0; j < b.length; j++) r[i + j] = r[i + j].add(a[i].mul(b[j])); return ptrim(r); }
function pscale(a, c) { return a.map((x) => x.mul(c)); }
function toQList(intList) { return intList.map((n) => new Q(BigInt(n))); }

const p = toQList([1, 0, 1]);            // p(x) = 1 + x^2
const a = toQList([1, 1, 0, 2, 0, 1]);   // a(x) = 1 + x(x^2+1)^2 = 1 + x + 2x^3 + x^5
const xpoly = toQList([0, 1]);           // x

// f := 2x + x^2 * p^2
const f = ptrim(padd(pscale(xpoly, new Q(2n)), pmul(pmul(xpoly, xpoly), pmul(p, p))));

// sanity: a^2 - f*p^2 = 1 (mu-side norm constant)
const chatMu = ptrim(psub(pmul(a, a), pmul(f, pmul(p, p))));
if (chatMu.length !== 1 || !chatMu[0].eq(new Q(1n))) {
  throw new Error(`production driver: a^2-f*p^2 must be the constant 1, got [${chatMu.map(String).join(',')}]`);
}
console.log('sanity check a^2-f*p^2 =', chatMu.map(String), '(expect ["1"])');

// lambda = mu^2 = (a^2+p^2 f) + 2ap y =: A + B y
const A = ptrim(psub(pscale(pmul(a, a), new Q(2n)), [new Q(1n)]));   // 2a^2-1
const B = ptrim(pscale(pmul(a, p), new Q(2n)));                       // 2ap

console.log('derived A =', A.map(String), 'deg =', A.length - 1);
console.log('derived B =', B.map(String), 'deg =', B.length - 1);
console.log('f =', f.map(String), 'deg =', f.length - 1);

const raw = {
  id: 'prod-ninf-M10',
  branch: 'N_infty',
  M: 10,
  f_coeffs_ascending: f.map(String),
  A_coeffs_ascending: A.map(String),
  B_coeffs_ascending: B.map(String),
  series_length: 30,
  expected_model_digest: 'a8e58ee991e93895383e8bbf346565620b3e3406f3f38e518b9d7bb3d026ffe3',
};

const model = loadModelNinf(raw);
const report = extractPathB_Ninf(model);

console.log('\n=== u-extract-pathB-ninf PRODUCTION calibration (M=10, synthetic, schema v2) ===');
console.log(JSON.stringify(report, null, 2));

writeFileSync(join(ROOT, 'certificates', 'k5pipeline', 'prod-ninf-M10-pathB.json'), JSON.stringify(report, null, 2) + '\n');
console.log('\nwrote certificates/k5pipeline/prod-ninf-M10-pathB.json');
