// crosscheck/u-compare.mjs
// Rule 1 SS6.3 (4) 第三の checker。
// 二つの raw 出力 JSON (u_pathA / u_pathB) **だけ**を読み、K 内の厳密等号
// u^(A) = u^(B) を判定する。それ以外の計算はしない(SS6.3 の要件)。
//
// 本ファイルは search/u-extract-pathA.g / crosscheck/u-extract-pathB.mjs の
// どちらの関数・データ構造にも依存しない(有理数の parse/eq のみ独立実装)。
//
// 使い方: node crosscheck/u-compare.mjs <pathA.json> <pathB.json>

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

const [pathAFile, pathBFile] = process.argv.slice(2);
if (!pathAFile || !pathBFile) {
  console.error('usage: node u-compare.mjs <u_pathA.json> <u_pathB.json>');
  process.exit(2);
}

const A = JSON.parse(readFileSync(pathAFile, 'utf8'));
const B = JSON.parse(readFileSync(pathBFile, 'utf8'));

const report = { schema: 'u-compare/v1', pathAFile, pathBFile, idA: A.id, idB: B.id };

if (A.id !== B.id) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `id mismatch: pathA.id=${A.id} pathB.id=${B.id}`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}

if (A.M !== B.M) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `M mismatch: pathA.M=${A.M} pathB.M=${B.M}`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}

if (!A.lower_order_vanish || !B.lower_order_vanish) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `lower-order vanish check failed: pathA=${A.lower_order_vanish} pathB=${B.lower_order_vanish}`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}

const uA = parseRat(A.u_pathA);
const uB = parseRat(B.u_pathB);
const equal = ratEq(uA, uB);

report.u_pathA = ratStr(uA);
report.u_pathB = ratStr(uB);
report.result = equal ? 'ACCEPT' : 'INTEGRITY_STOP';
if (!equal) report.reason = 'u^(A) != u^(B) (SS6.4 不一致 -> integrity stop / BRIDGE-UNKNOWN)';

console.log(JSON.stringify(report, null, 2));
if (!equal) process.exit(1);
