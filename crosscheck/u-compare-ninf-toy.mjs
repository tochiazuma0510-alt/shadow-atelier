// crosscheck/u-compare-ninf-toy.mjs
// R-5(便 36・裁定 36): 副枝 (N_infty) 経路 A∞/B-iii の第三 checker(玩具較正)。
// docs/week4-K5_Rule1_v1.md v1.2 S6.3 (4) と同じ設計思想: 二つの raw 出力
// JSON(toy-ninf-M3-pathA.json / toy-ninf-M3-pathB.json)だけを読み、厳密等号
// u^(A) = u^(B) を判定する。それ以外の計算はしない。
//
// 本ファイルは search/u-extract-pathA.g / crosscheck/u-extract-pathB-lib.mjs の
// どちらの関数・データ構造にも依存しない(u-compare.mjs と同じ独立実装方針)。
//
// *** SYNTHETIC のみ *** 本 checker が扱うのは Rule 1 S0.4-3 の M=n=3 玩具族
// のみであり、K^(5) の実データではない。
//
// 使い方: node crosscheck/u-compare-ninf-toy.mjs <pathA.json> <pathB.json>

import { readFileSync } from 'node:fs';

function gcdBig(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { [a, b] = [b, a % b]; } return a; }
function parseRat(s) {
  const str = String(s).trim();
  let n, d = 1n;
  if (str.includes('/')) { const [a, b] = str.split('/'); n = BigInt(a); d = BigInt(b); }
  else n = BigInt(str);
  if (d < 0n) { n = -n; d = -d; }
  const g = gcdBig(n, d) || 1n;
  return { n: n / g, d: d / g };
}
function ratEq(a, b) { return a.n * b.d === b.n * a.d; }
function ratStr(a) { return a.d === 1n ? `${a.n}` : `${a.n}/${a.d}`; }
function ratListEq(as, bs) {
  if (as.length !== bs.length) return false;
  for (let i = 0; i < as.length; i++) if (!ratEq(parseRat(as[i]), parseRat(bs[i]))) return false;
  return true;
}

const [pathAFile, pathBFile] = process.argv.slice(2);
if (!pathAFile || !pathBFile) {
  console.error('usage: node u-compare-ninf-toy.mjs <toy-ninf pathA.json> <pathB.json>');
  process.exit(2);
}

const A = JSON.parse(readFileSync(pathAFile, 'utf8'));
const B = JSON.parse(readFileSync(pathBFile, 'utf8'));

const report = { schema: 'u-compare-ninf-toy/v1', synthetic_note: 'Rule 1 S0.4-3 M=n=3 toy family -- NOT K^(5) real data', pathAFile, pathBFile, idA: A.id, idB: B.id };

if (A.id !== B.id) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `id mismatch: pathA.id=${A.id} pathB.id=${B.id}`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}
if (A.n !== B.n) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `n mismatch: pathA.n=${A.n} pathB.n=${B.n}`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}

const fieldChecks = [
  ['f_coeffs_ascending', ratListEq(A.f_coeffs_ascending, B.f_coeffs_ascending)],
  ['A_coeffs_ascending', ratListEq(A.A_coeffs_ascending, B.A_coeffs_ascending)],
  ['B_coeffs_ascending', ratListEq(A.B_coeffs_ascending, B.B_coeffs_ascending)],
];
for (const [field, ok] of fieldChecks) {
  if (!ok) {
    report.result = 'INTEGRITY_STOP';
    report.reason = `model field mismatch: ${field} differs between pathA and pathB raw`;
    console.log(JSON.stringify(report, null, 2));
    process.exit(1);
  }
}

// pathA-specific structural check
if (A.W_squared_equals_F !== true) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `pathA.W_squared_equals_F is not true: ${A.W_squared_equals_F}`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}
if (!A.lower_order_vanish) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `pathA.lower_order_vanish is not true: ${A.lower_order_vanish}`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}

// pathB-specific structural checks (N∞-1, N∞-2, N∞-3 analogs)
if (!B.deg_A_equals_n) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `pathB.deg_A_equals_n is not true (N∞-1 analog)`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}
if (!B.b_nm3_equals_a_n) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `pathB.b_nm3_equals_a_n is not true (N∞-2 analog)`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}
if (!B.N_lambda_is_nonzero_constant) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `pathB.N_lambda_is_nonzero_constant is not true (N∞-3 analog)`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}

const uA = parseRat(A.u_pathA_ninf);
const uB = parseRat(B.u_pathB_ninf);

if (uA.n === 0n || uB.n === 0n) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `u must be nonzero: u_pathA_ninf=${ratStr(uA)} u_pathB_ninf=${ratStr(uB)}`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}

const equal = ratEq(uA, uB);
report.u_pathA_ninf = ratStr(uA);
report.u_pathB_ninf = ratStr(uB);
report.result = equal ? 'ACCEPT' : 'INTEGRITY_STOP';
if (!equal) report.reason = 'u^(A) != u^(B) (S6.4 不一致 -> integrity stop / BRIDGE-UNKNOWN) [synthetic toy]';

console.log(JSON.stringify(report, null, 2));
if (!equal) process.exit(1);
