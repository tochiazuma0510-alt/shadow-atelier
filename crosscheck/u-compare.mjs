// crosscheck/u-compare.mjs
// Rule 1 SS6.3 (4) 第三の checker(**裁定 38/便 37 F2/F3 で bundle 束縛 +
// branch/P0_type 分離へ修理**)。
// 二つの raw 出力 JSON (u_pathA / u_pathB) に加えて**第三の入力として凍結
// bundle ファイル**(K3 較正では model-spec ファイル自身 -- certificates/
// k5fixture/K3-regression-model.json。実 K5 では Freeze 2 が渡す canonical
// model JSON)を読み、K 内の厳密等号 u^(A) = u^(B) を判定する。それ以外の
// 計算はしない(SS6.3 の要件)。
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
  return `id=${raw.id};M=${raw.M};branch=${raw.branch};P0_type=${raw.P0_type};` +
    `x0=${rat(raw.x0)};y0=${rat(raw.y0)};` +
    `f=[${list(raw.f_coeffs_ascending)}];A=[${list(raw.A_coeffs_ascending)}];B=[${list(raw.B_coeffs_ascending)}]`;
}
// model-spec ファイル(certificates/k5fixture/*-model.json)は raw 出力とは
// 別の field 名(f_coeffs_ascending 等でなく f_coeffs_ascending は同名だが
// x0/y0/branch/P0_type は model-spec でも同名 -- 便 37 で model-spec 側の
// field 名も branch/P0_type に統一したため、raw 用の関数をそのまま使える)。
function recomputeModelDigest(raw) {
  return createHash('sha256').update(recomputeCanonicalModelString(raw), 'utf8').digest('hex');
}

const [pathAFile, pathBFile, bundleFile] = process.argv.slice(2);
if (!pathAFile || !pathBFile || !bundleFile) {
  console.error('usage: node u-compare.mjs <u_pathA.json> <u_pathB.json> <bundle-or-model-spec.json>');
  console.error('(bundle is REQUIRED -- R-7/I-l: raw-only expected-digest self-comparison is not accepted, cf. 裁定38/便37 F2)');
  process.exit(2);
}

const A = JSON.parse(readFileSync(pathAFile, 'utf8'));
const B = JSON.parse(readFileSync(pathBFile, 'utf8'));
const bundle = JSON.parse(readFileSync(bundleFile, 'utf8'));

const report = { schema: 'u-compare/v3', pathAFile, pathBFile, bundleFile, idA: A.id, idB: B.id };

// bundle は二形態を許す(便 37 F2 修理 4):
//  - schema='model-spec/v1' かつ bridge_mode='calibration_pre_bridge'
//    (K3 較正: Freeze 2 以前・expected_model_digest の事前登録なし。
//    certificates/k5fixture/*-model.json をそのまま渡す。id は fixture_id)。
//  - schema='k5pipeline/frozen-bundle/v1' かつ mode in {production,calibration}
//    (Freeze 2 が注入する canonical model JSON、または合成較正用の凍結 bundle。
//    expected_model_digest の束縛を必須とする)。
const bundleId = bundle.id ?? bundle.fixture_id;
const bundleIsPreBridge = bundle.schema === 'model-spec/v1' && bundle.bridge_mode === 'calibration_pre_bridge';
const bundleIsFrozen = bundle.schema === 'k5pipeline/frozen-bundle/v1';
if (!bundleIsPreBridge && !bundleIsFrozen) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `bundle.schema must be 'model-spec/v1' (with bridge_mode='calibration_pre_bridge') or 'k5pipeline/frozen-bundle/v1', got '${bundle.schema}'`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}

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
  ['branch', A.branch === B.branch],
  ['P0_type', A.P0_type === B.P0_type],
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

// --- I-m(便 37 F3/R-8): 大域枝 enum・schema 名の突合・branch=W の整合規則 ---
const GLOBAL_BRANCH_ENUM = ['W', 'N_aff'];
const ALLOWED_MAIN_SCHEMAS = new Set(['u-pathA/v3', 'u-pathB/v3']);
for (const [raw, label] of [[A, 'pathA'], [B, 'pathB']]) {
  if (!GLOBAL_BRANCH_ENUM.includes(raw.branch)) {
    report.result = 'INTEGRITY_STOP';
    report.reason = `(I-m) ${label}.branch must be one of {${GLOBAL_BRANCH_ENUM.join(', ')}}, got '${raw.branch}' (N_infty must use u-compare-ninf.mjs, not this checker)`;
    console.log(JSON.stringify(report, null, 2));
    process.exit(1);
  }
  if (raw.schema && !ALLOWED_MAIN_SCHEMAS.has(raw.schema)) {
    report.result = 'INTEGRITY_STOP';
    report.reason = `(I-m) ${label}.schema='${raw.schema}' is not an allowed main-path schema (${[...ALLOWED_MAIN_SCHEMAS].join(', ')})`;
    console.log(JSON.stringify(report, null, 2));
    process.exit(1);
  }
  if (raw.branch === 'W' && raw.P0_type !== 'nonWeierstrass') {
    report.result = 'INTEGRITY_STOP';
    report.reason = `(I-m) ${label}: branch='W' requires P0_type='nonWeierstrass' (Lemma S5-W / Rule 1 SS4.1 "v1.2 の絞り込み"), got P0_type='${raw.P0_type}'`;
    console.log(JSON.stringify(report, null, 2));
    process.exit(1);
  }
}
if (bundleId !== A.id) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `bundle id (${bundleId}) does not match raw id (${A.id})`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}
if (bundle.branch !== undefined && bundle.branch !== A.branch) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `bundle.branch (${bundle.branch}) does not match raw branch (${A.branch})`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
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

// --- R-7/I-l(便 36 F3.2/F6-2・**裁定38/便37 F2 で bundle 束縛へ修理**):
// raw の model_digest を、raw 自身の自己申告ではなく**第三の bundle
// ファイル**の expected digest へ束縛する(§6.3-5)。「二 raw が同じ誤転記を
// すれば自己申告 expected_model_digest 同士が一致するだけで ACCEPT する」
// 攻撃(便37 F2)を、raw の外部にある独立ファイルとの canonical string
// byte 一致で遮断する。
//
// bundleIsPreBridge(K3 較正・model-spec/v1・bridge_mode=calibration_pre_bridge):
// Freeze 2 以前で expected_model_digest の事前登録がまだ存在しない(「K3
// finite fixture の formal a=1 読取りは変更しない」規律と同じ精神で、
// 過去の較正例を遡って digest 登録しない)。この場合でも **canonical
// model string の byte 一致は必須**にする(digest は無いが、独立ファイルの
// 生データとの一致という保護は失わない)。
// bundleIsFrozen(k5pipeline/frozen-bundle/v1・production/calibration):
// expected_model_digest の完全な束縛を必須とし、欠落は fail-closed に stop
// する(便37 F2 修理 4: production/calibration どちらも緩めない)。
const bundleCanonicalString = (() => {
  const idField = bundle.id ?? bundle.fixture_id;
  if (bundleIsFrozen) return bundle.canonical_model_string;
  // model-spec/v1 (K3 pre-bridge): reconstruct from the same field names
  // (id/fixture_id, M, branch, P0_type, x0, y0, f/A/B coeffs).
  const rat = (s) => ratStr(parseRat(s));
  const list = (xs) => xs.map(rat).join(',');
  return `id=${idField};M=${bundle.M};branch=${bundle.branch};P0_type=${bundle.P0_type};` +
    `x0=${rat(bundle.x0)};y0=${rat(bundle.y0)};` +
    `f=[${list(bundle.f_coeffs_ascending)}];A=[${list(bundle.A_coeffs_ascending)}];B=[${list(bundle.B_coeffs_ascending)}]`;
})();

if (bundleCanonicalString !== recomputeCanonicalModelString(A)) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `(I-l) bundle canonical model string does not match the string reconstructed from pathA raw fields -- pathA does not match the frozen bundle/model-spec`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}
if (bundleCanonicalString !== recomputeCanonicalModelString(B)) {
  report.result = 'INTEGRITY_STOP';
  report.reason = `(I-l) bundle canonical model string does not match the string reconstructed from pathB raw fields -- pathB does not match the frozen bundle/model-spec`;
  console.log(JSON.stringify(report, null, 2));
  process.exit(1);
}

if (bundleIsFrozen) {
  if (!bundle.expected_model_digest) {
    report.result = 'INTEGRITY_STOP';
    report.reason = `bundle.expected_model_digest is missing (mode=${bundle.mode}) -- R-7 requires this to be present and bound, not silently skipped`;
    console.log(JSON.stringify(report, null, 2));
    process.exit(1);
  }
  const bundleRecomputedDigest = createHash('sha256').update(bundle.canonical_model_string, 'utf8').digest('hex');
  if (bundleRecomputedDigest !== bundle.expected_model_digest) {
    report.result = 'INTEGRITY_STOP';
    report.reason = `bundle self-consistency failure: sha256(bundle.canonical_model_string)=${bundleRecomputedDigest} != bundle.expected_model_digest=${bundle.expected_model_digest}`;
    console.log(JSON.stringify(report, null, 2));
    process.exit(1);
  }
  report.bundle_mode = bundle.mode;
  report.bundle_expected_model_digest = bundle.expected_model_digest;
  report.expected_digest_check = 'BOUND (bundle-external, R-7/I-l closed per 裁定38/便37 F2)';
} else {
  report.bundle_mode = 'calibration_pre_bridge';
  report.expected_digest_check = 'NOT_PROVIDED (calibration_pre_bridge, explicit -- K3 predates Freeze 2 digest injection; canonical-string byte match against the model-spec bundle is still enforced above)';
}
if (A.expected_model_digest || B.expected_model_digest) {
  report.raw_self_reported_expected_model_digest = { pathA: A.expected_model_digest, pathB: B.expected_model_digest };
}

const equal = ratEq(uA, uB);

report.u_pathA = ratStr(uA);
report.u_pathB = ratStr(uB);
report.result = equal ? 'ACCEPT' : 'INTEGRITY_STOP';
if (!equal) report.reason = 'u^(A) != u^(B) (SS6.4 不一致 -> integrity stop / BRIDGE-UNKNOWN)';

console.log(JSON.stringify(report, null, 2));
if (!equal) process.exit(1);
