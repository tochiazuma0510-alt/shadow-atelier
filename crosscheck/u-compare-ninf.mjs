#!/usr/bin/env node
// crosscheck/u-compare-ninf.mjs -- R-5/R-7(便 36 F3.2/F6-1,2)副枝 (N_infty)
// 経路 A∞/B-iii の第三 checker(production schema v2 対応)。
//
// docs/week4-K5_Rule1_v1.md v1.2 S6.3 (4)(5) と同じ設計思想: 二つの raw 出力
// JSON(*-pathA.json / *-pathB.json)だけを読み、厳密等号 u^(A) = u^(B) を
// 判定する。それ以外の計算はしない。加えて(便 36 F3.2 (3)/R-7):
//   (i)  二 raw の model_digest が相互に一致すること、かつこの checker
//        自身が raw の echo フィールドから canonical_model_string を
//        独立に再構成して sha256 を取り直し、embed 値と一致すること
//        (embed された digest を鵜呑みにしない -- u-compare.mjs と同じ規律)。
//   (ii) 二 raw の expected_model_digest が相互に一致し、かつ (i) で
//        再計算した digest とも一致すること(I-l -- 「凍結 bundle の期待
//        digest への束縛」。較正では driver が転記した synthetic な期待値、
//        実 K5 では Freeze 2 が注入する値のスタンドイン)。
//
// 本ファイルは search/u-extract-pathA.g / crosscheck/u-extract-pathB-lib.mjs の
// どちらの関数・データ構造にも依存しない(u-compare.mjs / u-compare-ninf-
// toy.mjs(旧版・本ファイルが supersede)と同じ独立実装方針)。
//
// 身分: schema v2 は M=3 の unit test 較正にも M=10 の production 較正にも
// 同じ raw フィールド構成を使うため、本 checker は M の値に依らず動く
// (旧 crosscheck/u-compare-ninf-toy.mjs の M=3 専用版を supersede する)。
//
// *** SYNTHETIC のみ *** 本 checker が扱うのは Rule 1 S0.4-3 型の合成
// fixture(M=3 unit test または M=10 production 較正のいずれか)であり、
// K^(5) の実データではない。
//
// 使い方: node crosscheck/u-compare-ninf.mjs <pathA.json> <pathB.json>

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
// この checker 自身による canonical digest 再構成(GAP/node どちらの実装
// コードも import せず、raw JSON の echo フィールドから独立に組み立てる)。
function recomputeCanonicalModelStringNinf(raw) {
  const rat = (s) => ratStr(parseRat(s));
  const list = (xs) => xs.map(rat).join(',');
  return `id=${raw.id};branch=N_infty;M=${raw.M};` +
    `f=[${list(raw.f_coeffs_ascending)}];A=[${list(raw.A_coeffs_ascending)}];B=[${list(raw.B_coeffs_ascending)}]`;
}
function recomputeModelDigestNinf(raw) {
  return createHash('sha256').update(recomputeCanonicalModelStringNinf(raw), 'utf8').digest('hex');
}

const [pathAFile, pathBFile] = process.argv.slice(2);
if (!pathAFile || !pathBFile) {
  console.error('usage: node u-compare-ninf.mjs <ninf pathA.json> <pathB.json>');
  process.exit(2);
}

const A = JSON.parse(readFileSync(pathAFile, 'utf8'));
const B = JSON.parse(readFileSync(pathBFile, 'utf8'));

const report = { schema: 'u-compare-ninf/v2', pathAFile, pathBFile, idA: A.id, idB: B.id };

function stop(reason) {
  report.result = 'INTEGRITY_STOP';
  report.reason = reason;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}

if (A.id !== B.id) stop(`id mismatch: pathA.id=${A.id} pathB.id=${B.id}`);
if (A.branch !== 'N_infty' || B.branch !== 'N_infty') {
  stop(`branch label mismatch (I-m): pathA.branch=${A.branch} pathB.branch=${B.branch} (both must be 'N_infty')`);
}
if (A.M !== B.M) stop(`M mismatch: pathA.M=${A.M} pathB.M=${B.M}`);

const fieldChecks = [
  ['f_coeffs_ascending', ratListEq(A.f_coeffs_ascending, B.f_coeffs_ascending)],
  ['A_coeffs_ascending', ratListEq(A.A_coeffs_ascending, B.A_coeffs_ascending)],
  ['B_coeffs_ascending', ratListEq(A.B_coeffs_ascending, B.B_coeffs_ascending)],
];
for (const [field, ok] of fieldChecks) {
  if (!ok) stop(`model field mismatch: ${field} differs between pathA and pathB raw`);
}

// --- pathA-specific structural checks ---
if (A.W_squared_equals_F !== true) stop(`pathA.W_squared_equals_F is not true: ${A.W_squared_equals_F}`);
if (!A.lower_order_vanish) stop(`pathA.lower_order_vanish is not true: ${A.lower_order_vanish}`);

// --- (N∞-1)-(N∞-4) analogs, checked on whichever raw carries them (both should) ---
for (const [raw, label] of [[A, 'pathA'], [B, 'pathB']]) {
  if (raw.deg_A_equals_M !== true) stop(`${label}.deg_A_equals_M is not true (N∞-1)`);
  if (raw.deg_B_equals_Mminus3 !== true) stop(`${label}.deg_B_equals_Mminus3 is not true (N∞-1)`);
  if (raw.b_Mm3_equals_a_M !== true) stop(`${label}.b_Mm3_equals_a_M is not true (N∞-2)`);
  if (raw.gcd_f_fprime_is_unit !== true) stop(`${label}.gcd_f_fprime_is_unit is not true (f not squarefree)`);
}
if (B.N_lambda_is_nonzero_constant !== true) stop('pathB.N_lambda_is_nonzero_constant is not true (N∞-3)');
if (A.chat_equals_1 !== true) stop('pathA.chat_equals_1 is not true (N∞-4)');
if (B.chat_equals_1 !== true) stop('pathB.chat_equals_1 is not true (N∞-4)');

// --- model_digest: mutual match + independent recomputation (not trusting embedded value) ---
if (!A.model_digest || !B.model_digest) stop('model_digest missing on pathA and/or pathB raw');
if (A.model_digest !== B.model_digest) stop(`model_digest mismatch: pathA=${A.model_digest} pathB=${B.model_digest}`);
const recomputedA = recomputeModelDigestNinf(A);
const recomputedB = recomputeModelDigestNinf(B);
report.recomputed_model_digest_pathA = recomputedA;
report.recomputed_model_digest_pathB = recomputedB;
if (recomputedA !== A.model_digest || recomputedB !== B.model_digest || recomputedA !== recomputedB) {
  stop(`independently recomputed model_digest does not match embedded value: recomputedA=${recomputedA} (embedded ${A.model_digest}), recomputedB=${recomputedB} (embedded ${B.model_digest})`);
}
report.model_digest = A.model_digest;

// --- R-7 / I-l: expected_model_digest binding to the (synthetic-stand-in) frozen bundle ---
if (!A.expected_model_digest || !B.expected_model_digest) {
  stop('expected_model_digest missing on pathA and/or pathB raw (R-7 requires binding to a frozen-bundle expected digest)');
}
if (A.expected_model_digest !== B.expected_model_digest) {
  stop(`expected_model_digest mismatch between pathA and pathB raw: pathA=${A.expected_model_digest} pathB=${B.expected_model_digest}`);
}
if (A.expected_model_digest !== recomputedA) {
  stop(`(I-l) expected_model_digest (${A.expected_model_digest}) does not match the independently recomputed model_digest (${recomputedA})`);
}
report.expected_model_digest = A.expected_model_digest;

const uA = parseRat(A.u_pathA_ninf);
const uB = parseRat(B.u_pathB_ninf);

if (uA.n === 0n || uB.n === 0n) {
  stop(`u must be nonzero: u_pathA_ninf=${ratStr(uA)} u_pathB_ninf=${ratStr(uB)}`);
}

const equal = ratEq(uA, uB);
report.u_pathA_ninf = ratStr(uA);
report.u_pathB_ninf = ratStr(uB);
report.result = equal ? 'ACCEPT' : 'INTEGRITY_STOP';
if (!equal) report.reason = 'u^(A) != u^(B) (S6.4 不一致 -> integrity stop / BRIDGE-UNKNOWN)';

console.log(JSON.stringify(report, null, 2));
if (!equal) process.exit(1);
