#!/usr/bin/env node
// crosscheck/u-compare-ninf.mjs -- R-5/R-7(便 36 F3.2/F6-1,2・**裁定 38/便 37
// F2 で bundle 束縛へ修理**)副枝 (N_infty) 経路 A∞/B-iii の第三 checker
// (production schema v2 対応)。
//
// docs/week4-K5_Rule1_v1.md v1.2 S6.3 (4)(5) と同じ設計思想: 二つの raw 出力
// JSON(*-pathA.json / *-pathB.json)だけでなく、**第三の入力として凍結
// bundle ファイル**(*-bundle.json・crosscheck/build-frozen-bundles.mjs が
// pathA/pathB のどちらのコードとも独立に生成)を読み、厳密等号
// u^(A) = u^(B) を判定する。加えて(便 36 F3.2 (3)/R-7・便 37 F2 修理):
//   (i)   二 raw の model_digest が相互に一致すること、かつこの checker
//         自身が raw の echo フィールドから canonical_model_string を
//         独立に再構成して sha256 を取り直し、embed 値と一致すること
//         (embed された digest を鵜呑みにしない -- u-compare.mjs と同じ規律)。
//   (ii)  bundle 自身の canonical_model_string から sha256 を取り直し、
//         bundle.expected_model_digest と一致すること(bundle の自己整合)。
//   (iii) **bundle.canonical_model_string が raw から再構成した canonical
//         string と逐語一致すること**(便 37 F2 の核心: 「二 driver が同じ
//         誤転記をすれば、raw 内の自己申告 expected_model_digest 同士が
//         一致するだけで ACCEPT してしまう」攻撃を、raw の外部にある
//         独立ファイルとの byte 一致で遮断する。raw 内の expected_model_digest
//         フィールドは参考情報として記録するが、判定の根拠には bundle 側の
//         値を使う)。
//   (iv)  production mode の bundle では上記がすべて揃わなければ必ず
//         INTEGRITY_STOP にする(expected 欠落を ACCEPT する fail-open を
//         禁止)。calibration mode も同じ拘束を受ける(便 37 F2 修理 1 --
//         「合成較正にも小さな synthetic frozen bundle を作る」)。
//
// 本ファイルは search/u-extract-pathA.g / crosscheck/u-extract-pathB-lib.mjs /
// crosscheck/build-frozen-bundles.mjs のいずれの関数・データ構造にも依存
// しない(u-compare.mjs / u-compare-ninf-toy.mjs(旧版・本ファイルが
// supersede)と同じ独立実装方針)。
//
// 身分: schema v2 は M=3 の unit test 較正にも M=10 の production 較正にも
// 同じ raw フィールド構成を使うため、本 checker は M の値に依らず動く
// (旧 crosscheck/u-compare-ninf-toy.mjs の M=3 専用版を supersede する)。
//
// *** SYNTHETIC のみ *** 本 checker が扱うのは Rule 1 S0.4-3 型の合成
// fixture(M=3 unit test または M=10 production 較正のいずれか)であり、
// K^(5) の実データではない。
//
// 使い方: node crosscheck/u-compare-ninf.mjs <pathA.json> <pathB.json> <bundle.json>

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

const [pathAFile, pathBFile, bundleFile] = process.argv.slice(2);
if (!pathAFile || !pathBFile || !bundleFile) {
  console.error('usage: node u-compare-ninf.mjs <ninf pathA.json> <pathB.json> <bundle.json>');
  console.error('(bundle.json is REQUIRED -- R-7/I-l: raw-only expected-digest self-comparison is not accepted, cf. Sol 便37 F2)');
  process.exit(2);
}

const A = JSON.parse(readFileSync(pathAFile, 'utf8'));
const B = JSON.parse(readFileSync(pathBFile, 'utf8'));
const bundle = JSON.parse(readFileSync(bundleFile, 'utf8'));

const report = { schema: 'u-compare-ninf/v3', pathAFile, pathBFile, bundleFile, idA: A.id, idB: B.id };

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

// --- I-m (便 37 F3/R-8): schema 名と枝ラベルの突合 + P0_type 整合(N_infty
// では常に nonWeierstrass -- 補題 R1-M0 3.)。schema field が無い raw は
// 旧世代のもので、ここに来る前に上の branch チェックで弾かれているはずだが、
// schema 文字列自体も明示的に検査する。
const ALLOWED_NINF_SCHEMAS = new Set(['u-pathA-ninf/v2', 'u-pathB-ninf/v2']);
for (const [raw, label] of [[A, 'pathA'], [B, 'pathB']]) {
  if (raw.schema && !ALLOWED_NINF_SCHEMAS.has(raw.schema)) {
    stop(`(I-m) ${label}.schema='${raw.schema}' is not an allowed N_infty schema (${[...ALLOWED_NINF_SCHEMAS].join(', ')})`);
  }
  if (raw.P0_type !== undefined && raw.P0_type !== null && raw.P0_type !== 'nonWeierstrass') {
    stop(`(I-m) ${label}.P0_type must be 'nonWeierstrass' for branch='N_infty' (Lemma R1-M0 3.), got '${raw.P0_type}'`);
  }
}

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

// --- R-7 / I-l(便 37 F2 修理): expected digest 束縛は raw の自己申告ではなく
// 第三の bundle ファイルに対して行う。raw の expected_model_digest は参考
// 情報として記録するが、ACCEPT/STOP の根拠にはしない(それ単独では「二 raw
// が同じ誤転記をした」攻撃を防げないため -- 便 37 F2 の指摘そのもの)。
if (!bundle.schema || bundle.schema !== 'k5pipeline/frozen-bundle/v1') {
  stop(`bundle.schema must be 'k5pipeline/frozen-bundle/v1', got '${bundle.schema}'`);
}
if (bundle.mode !== 'production' && bundle.mode !== 'calibration') {
  stop(`bundle.mode must be 'production' or 'calibration' for the N_infty checker, got '${bundle.mode}'`);
}
if (bundle.branch !== 'N_infty') stop(`bundle.branch must be 'N_infty', got '${bundle.branch}'`);
if (bundle.id !== A.id) stop(`bundle.id (${bundle.id}) does not match raw id (${A.id})`);
if (!bundle.canonical_model_string) stop('bundle.canonical_model_string is missing');
if (!bundle.expected_model_digest) {
  // production/calibration いずれのモードでも expected 欠落は fail-closed
  // (便 37 F2 修理 4: production では必ず STOP。calibration も同じ拘束を
  // 受ける -- 「較正だから緩める」という暗黙の例外を作らない)。
  stop(`bundle.expected_model_digest is missing (mode=${bundle.mode}) -- R-7 requires this to be present and bound, not silently skipped`);
}
// bundle 自己整合: bundle 自身の canonical_model_string から sha256 を
// 独立に取り直し、bundle が宣言する expected_model_digest と一致するか。
const bundleRecomputedDigest = createHash('sha256').update(bundle.canonical_model_string, 'utf8').digest('hex');
if (bundleRecomputedDigest !== bundle.expected_model_digest) {
  stop(`bundle self-consistency failure: sha256(bundle.canonical_model_string)=${bundleRecomputedDigest} != bundle.expected_model_digest=${bundle.expected_model_digest}`);
}
// 核心の防御(便37 F2): raw から再構成した canonical string が、独立な
// bundle ファイルの canonical_model_string と逐語一致すること。
if (bundle.canonical_model_string !== recomputeCanonicalModelStringNinf(A)) {
  stop(`(I-l) bundle.canonical_model_string does not match the string reconstructed from pathA raw fields -- pathA does not match the frozen bundle (independent of pathA's own self-reported expected_model_digest)`);
}
if (bundle.canonical_model_string !== recomputeCanonicalModelStringNinf(B)) {
  stop(`(I-l) bundle.canonical_model_string does not match the string reconstructed from pathB raw fields -- pathB does not match the frozen bundle`);
}
report.bundle_mode = bundle.mode;
report.bundle_expected_model_digest = bundle.expected_model_digest;
report.expected_digest_check = 'BOUND (bundle-external, R-7/I-l closed per 裁定38/便37 F2)';
// raw 側の自己申告 expected_model_digest は参考情報としてのみ記録する。
if (A.expected_model_digest || B.expected_model_digest) {
  report.raw_self_reported_expected_model_digest = { pathA: A.expected_model_digest, pathB: B.expected_model_digest };
}

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
