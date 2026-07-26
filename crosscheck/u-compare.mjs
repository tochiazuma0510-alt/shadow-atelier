// crosscheck/u-compare.mjs
// Rule 1 SS6.3 (4) 第三の checker。
// 二つの raw 出力 JSON (u_pathA / u_pathB) **だけ**を読み、K 内の厳密等号
// u^(A) = u^(B) を判定する。それ以外の計算はしない(SS6.3 の要件)。
//
// 本ファイルは search/u-extract-pathA.g / crosscheck/u-extract-pathB-lib.mjs の
// どちらの関数・データ構造にも依存しない(有理数の parse/eq のみ独立実装)。
//
// 便 34 P6-E2 (Sol 便 34 blocker 3 前半 / F4.3): 従来は id/M/lower_order_vanish/
// u だけを突合しており、branchP0・x0・y0・f・A・B・model_digest・
// curve_residual_zero・u≠0 を検査しなかった(異なるモデルに同じ id を付けて
// 偶然同じ u が出れば ACCEPT し得た)。本版は次を fail-closed に追加する:
//   1. branchP0, x0, y0, f, A, B の全フィールドが両 raw で一致すること。
//   2. 両 raw が embed する model_digest が一致すること(かつ、この checker
//      自身が両 raw の echo フィールドから canonical_model_string を
//      **独立に再構成**して sha256 を取り直し、embed 値と一致するかも検査
//      する -- embed された digest を鵜呑みにしない)。
//   3. pathA の curve_residual_zero が true であること(pathB には対応する
//      検査がない -- pathB は級数を使わないので曲線方程式の残差という概念が
//      そもそも存在しない。8.6 系設計)。
//   4. u^(A), u^(B) がともに非零であること(分岐位数 > M で両側 0 のまま
//      ACCEPT してしまう罠の回避)。
//
// 使い方: node crosscheck/u-compare.mjs <pathA.json> <pathB.json>

import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

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
// 第三の(u-compare.mjs 自身による)canonical digest 再構成。search/u-extract-
// pathA.g / crosscheck/u-extract-pathB-lib.mjs のどちらの実装コードも import
// せず、raw JSON の echo フィールドから独立に文字列を組み立てて sha256 する。
function recomputeCanonicalModelString(raw) {
  const rat = (s) => ratStr(parseRat(s));
  const list = (xs) => xs.map(rat).join(',');
  return `id=${raw.id};M=${raw.M};branchP0=${raw.branchP0};` +
    `x0=${rat(raw.x0)};y0=${rat(raw.y0)};` +
    `f=[${list(raw.f_coeffs_ascending)}];A=[${list(raw.A_coeffs_ascending)}];B=[${list(raw.B_coeffs_ascending)}]`;
}
function recomputeModelDigest(raw) {
  return createHash('sha256').update(recomputeCanonicalModelString(raw), 'utf8').digest('hex');
}

const [pathAFile, pathBFile] = process.argv.slice(2);
if (!pathAFile || !pathBFile) {
  console.error('usage: node u-compare.mjs <u_pathA.json> <u_pathB.json>');
  process.exit(2);
}

const A = JSON.parse(readFileSync(pathAFile, 'utf8'));
const B = JSON.parse(readFileSync(pathBFile, 'utf8'));

const report = { schema: 'u-compare/v2', pathAFile, pathBFile, idA: A.id, idB: B.id };

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

// --- 便 34 P6-E2: モデル束縛の fail-closed 検査(id/M だけでは不十分) ---
const fieldChecks = [
  ['branchP0', A.branchP0 === B.branchP0],
  ['x0', ratEq(parseRat(A.x0), parseRat(B.x0))],
  ['y0', ratEq(parseRat(A.y0), parseRat(B.y0))],
  ['f_coeffs_ascending', ratListEq(A.f_coeffs_ascending, B.f_coeffs_ascending)],
  ['A_coeffs_ascending', ratListEq(A.A_coeffs_ascending, B.A_coeffs_ascending)],
  ['B_coeffs_ascending', ratListEq(A.B_coeffs_ascending, B.B_coeffs_ascending)],
];
for (const [field, ok] of fieldChecks) {
  if (!ok) {
    report.result = 'INTEGRITY_STOP';
    report.reason = `model field mismatch: ${field} differs between pathA and pathB raw (二 raw が同一モデル由来であることが検査できない)`;
    console.log(JSON.stringify(report, null, 2));
    process.exit(1);
  }
}

// --- model_digest 突合: embed 値の一致 + この checker 自身による独立再計算 ---
if (!A.model_digest || !B.model_digest) {
  report.result = 'INTEGRITY_STOP';
  report.reason = 'model_digest missing on pathA and/or pathB raw (便 34 以降の raw は model_digest を embed する必要がある)';
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}
if (A.model_digest !== B.model_digest) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `model_digest mismatch: pathA=${A.model_digest} pathB=${B.model_digest}`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}
const recomputedA = recomputeModelDigest(A);
const recomputedB = recomputeModelDigest(B);
report.recomputed_model_digest_pathA = recomputedA;
report.recomputed_model_digest_pathB = recomputedB;
if (recomputedA !== A.model_digest || recomputedB !== B.model_digest || recomputedA !== recomputedB) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `independently recomputed model_digest does not match embedded value: ` +
    `recomputedA=${recomputedA} (embedded ${A.model_digest}), recomputedB=${recomputedB} (embedded ${B.model_digest})`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}
report.model_digest = A.model_digest;

// --- pathA 固有の curve_residual_zero(pathB には対応する検査概念がない) ---
if (A.curve_residual_zero !== true) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `pathA.curve_residual_zero is not true (曲線方程式 y^2=f(x) の切断検算に失敗): ${A.curve_residual_zero}`;
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

// --- u != 0 (分岐位数 > M のまま両側 0 で ACCEPT してしまう罠の回避) ---
if (uA.n === 0n || uB.n === 0n) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `u must be nonzero (ord_{P0}(lambda) = M の前提が崩れている可能性): u_pathA=${ratStr(uA)} u_pathB=${ratStr(uB)}`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}

// --- R-7/I-l(便 36 F3.2/F6-2): raw の model_digest を凍結 bundle の expected
// digest へ束縛する(§6.3-5)。この機構は expected_model_digest フィールドが
// raw に埋め込まれて初めて働く。K3 較正の凍結済み raw(certificates/
// k5pipeline/K3-regression-u-pathA.json 等)は本便で新設される前の schema で
// あり、このフィールドを持たない -- それらを遡って改変しない(「K3 finite
// fixture の formal a=1 読取りは変更しない」の規律)ので、両 raw に
// expected_model_digest が無い場合は「機構は配線済みだが Freeze 2 未到達」と
// 正直に記録し、ACCEPT/INTEGRITY_STOP の判定には使わない。一方が有って
// 他方が無い、または値が食い違う場合は fail-closed に stop する。
if (A.expected_model_digest || B.expected_model_digest) {
  if (!A.expected_model_digest || !B.expected_model_digest) {
    report.result = 'INTEGRITY_STOP';
    report.reason = `expected_model_digest present on only one of pathA/pathB (pathA=${A.expected_model_digest} pathB=${B.expected_model_digest})`;
    console.log(JSON.stringify(report, null, 2));
    process.exit(1);
  }
  if (A.expected_model_digest !== B.expected_model_digest) {
    report.result = 'INTEGRITY_STOP';
    report.reason = `expected_model_digest mismatch: pathA=${A.expected_model_digest} pathB=${B.expected_model_digest}`;
    console.log(JSON.stringify(report, null, 2));
    process.exit(1);
  }
  if (A.expected_model_digest !== recomputedA) {
    report.result = 'INTEGRITY_STOP';
    report.reason = `(I-l) expected_model_digest (${A.expected_model_digest}) does not match the independently recomputed model_digest (${recomputedA})`;
    console.log(JSON.stringify(report, null, 2));
    process.exit(1);
  }
  report.expected_model_digest = A.expected_model_digest;
  report.expected_digest_check = 'BOUND';
} else {
  report.expected_digest_check = 'NOT_PROVIDED (pre-bridge; R-7 mechanism wired but Freeze 2 has not injected a value into this raw schema yet)';
}

const equal = ratEq(uA, uB);

report.u_pathA = ratStr(uA);
report.u_pathB = ratStr(uB);
report.result = equal ? 'ACCEPT' : 'INTEGRITY_STOP';
if (!equal) report.reason = 'u^(A) != u^(B) (SS6.4 不一致 -> integrity stop / BRIDGE-UNKNOWN)';

console.log(JSON.stringify(report, null, 2));
if (!equal) process.exit(1);
