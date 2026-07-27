#!/usr/bin/env node
// crosscheck/u-compare-ninf.mjs -- R-5/R-7(便 36 F3.2/F6-1,2・**裁定 38/便 37
// F2 で bundle 束縛へ修理・裁定 39/便 38 F2 で schema gate を fail-closed 化・
// 便 38 F1.2 対応で in-process 呼び出し用の純関数として export**)副枝
// (N_infty) 経路 A∞/B-iii の第三 checker(production schema 対応)。
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
//         string と逐語一致すること**(便 37 F2 の核心)。
//   (iv)  production mode の bundle では上記がすべて揃わなければ必ず
//         INTEGRITY_STOP にする(expected 欠落を ACCEPT する fail-open を
//         禁止)。calibration mode も同じ拘束を受ける。
//
// 便 38 F2(裁定 39 blocker 1)修理: 旧版は
//   - schema field が任意(`if (raw.schema && !ALLOWED...)`)で、pathA/pathB を
//     同一集合で検査したため方向交換を検出できなかった、
//   - P0_type field が任意(与えられなければ検査自体をスキップ)、
//   - x0/y0(N_infty raw には本来存在しない main-path 専用 field)の混入を
//     検査しない、
//   - a_M/b_Mm3 の**存在**と、係数列から独立に再抽出した値との一致を
//     検査しない(deg_A_equals_M 等の自己申告 boolean flag のみに依存)
// という 5 種の fail-open な穴があった(便38 F2.3 の悪意入力 5 件で実証)。
// 本版は次を必須化する:
//   1. schema field の存在必須化 + pathA='u-pathA-ninf/v2'・
//      pathB='u-pathB-ninf/v2' への方向付き exact equality。
//   2. P0_type field の存在必須化 + 'nonWeierstrass' との exact equality
//      (N_infty では常にこの値のみ許される -- 補題 R1-M0 3.)。
//   3. x0/y0 field が存在すれば INTEGRITY_STOP(N_infty raw に存在してはならない
//      main-path 専用 field の混入拒否)。
//   4. M, chat, a_M, b_Mm3 field の存在必須化 + a_M/b_Mm3 はこの checker が
//      係数列(A_coeffs_ascending[M]・B_coeffs_ascending[M-3])から独立に
//      再抽出した値と一致すること(自己申告の boolean flag を鵜呑みにしない)。
//
// 本ファイルは search/u-extract-pathA.g / crosscheck/u-extract-pathB-lib.mjs /
// crosscheck/build-frozen-bundles.mjs のいずれの関数・データ構造にも依存
// しない(u-compare.mjs / u-compare-ninf-toy.mjs(旧版・本ファイルが
// supersede)と同じ独立実装方針)。
//
// *** SYNTHETIC のみ *** 本 checker が扱うのは Rule 1 S0.4-3 型の合成
// fixture(M=3 unit test または M=10 production 較正のいずれか)であり、
// K^(5) の実データではない。
//
// 使い方(CLI): node crosscheck/u-compare-ninf.mjs <pathA.json> <pathB.json> <bundle.json>
// 使い方(import): import { compareNinf } from './u-compare-ninf.mjs'; compareNinf(A, B, bundle)
//   -- 純関数。ファイル I/O・console.log・process.exit を行わない。

import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';

function gcdBig(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { [a, b] = [b, a % b]; } return a; }
// --- 裁定41/便40 F1.2: strict rational literal grammar(全文一致・単一の
// regex で符号付き整数 or 分子/分母一組だけを許す)。空の分子・分母・二本
// 以上の '/'・分母 0 はすべて RationalFormatError として拒否する(交差積
// 等値判定 ratEq に「0/0 は何にでも等しい」「1/0 同士は等しい」という穴を
// 開けない -- Sol 便40 F1.2 の指摘)。malformed rational は純関数 API
// (compareNinf)でも structured INTEGRITY_STOP になるよう、下の catch で
// この Error クラスを捕捉して report へ変換する。
// **司令塔独自攻撃(裁定41続報)修理**: trim を廃止し、入力文字列そのままが
// 正規表現に一致することを要求する(先頭/末尾空白混入は拒否)。 ---
class RationalFormatError extends Error {}
const RATIONAL_LITERAL_RE = /^([+-]?\d+)(?:\/([+-]?\d+))?$/;
function parseRat(s) {
  const str = String(s);
  const m = RATIONAL_LITERAL_RE.exec(str);
  if (!m) {
    throw new RationalFormatError(
      `malformed rational literal ${JSON.stringify(s)}: must match ^[+-]?\\d+(/[+-]?\\d+)?$ ` +
      `(signed integer, or exactly one numerator/denominator pair -- empty numerator/denominator, ` +
      `a second '/', and non-digit content are all rejected)`
    );
  }
  let n = BigInt(m[1]);
  let d = m[2] !== undefined ? BigInt(m[2]) : 1n;
  if (d === 0n) {
    throw new RationalFormatError(`malformed rational literal ${JSON.stringify(s)}: denominator is zero`);
  }
  if (d < 0n) { n = -n; d = -d; }
  const g = gcdBig(n, d) || 1n;
  const rn = n / g, rd = d / g;
  if (rd <= 0n) {
    throw new RationalFormatError(`internal invariant violated: reduced denominator is not positive for ${JSON.stringify(s)} (rn=${rn}, rd=${rd})`);
  }
  return { n: rn, d: rd };
}
function ratEq(a, b) { return a.n * b.d === b.n * a.d; }
function ratStr(a) { return a.d === 1n ? `${a.n}` : `${a.n}/${a.d}`; }
function ratListEq(as, bs) {
  if (as.length !== bs.length) return false;
  for (let i = 0; i < as.length; i++) if (!ratEq(parseRat(as[i]), parseRat(bs[i]))) return false;
  return true;
}
const RAT_ONE = { n: 1n, d: 1n };
const RAT_ZERO = { n: 0n, d: 1n };

// --- 裁定40/便39 F1.2: この checker 自身による厳密有理数多項式演算
// (independent of crosscheck/u-extract-pathB-lib.mjs / search/u-extract-pathA.g --
// 係数配列は raw の echo フィールドから読むのみで、両実装の polyMul/polySub
// 関数そのものは import しない)。A^2-B^2*f を再計算し、chat の自己申告
// boolean flag だけに頼らず、厳密に定数 1 であることを直接検算する。 ---
function ratMul2(a, b) { const n = a.n * b.n, d = a.d * b.d; const g = gcdBig(n, d) || 1n; return { n: n / g, d: d / g }; }
function ratSub2(a, b) { const n = a.n * b.d - b.n * a.d, d = a.d * b.d; const g = gcdBig(n, d) || 1n; return { n: n / g, d: d / g }; }
function ratAdd2(a, b) { const n = a.n * b.d + b.n * a.d, d = a.d * b.d; const g = gcdBig(n, d) || 1n; return { n: n / g, d: d / g }; }
function polyTrimRat(cs) { const r = cs.slice(); while (r.length > 1 && r[r.length - 1].n === 0n) r.pop(); return r; }
function polyMulRat(a, b) {
  const r = Array.from({ length: a.length + b.length - 1 }, () => RAT_ZERO);
  for (let i = 0; i < a.length; i++) for (let j = 0; j < b.length; j++) r[i + j] = ratAdd2(r[i + j], ratMul2(a[i], b[j]));
  return polyTrimRat(r);
}
function polySubRat(a, b) {
  const n = Math.max(a.length, b.length);
  const r = [];
  for (let i = 0; i < n; i++) r.push(ratSub2(a[i] ?? RAT_ZERO, b[i] ?? RAT_ZERO));
  return polyTrimRat(r);
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

// --- 便 38 F2/裁定 39 blocker 1: 方向付き exact equality(集合所属ではない)。
// 裁定40/便39 F2: v2 raw は P0_type/a_M/b_Mm3 を欠いていたため、同じ schema
// 名の下で受理言語を破壊的に変更するのではなく v3 へ version bump した
// (旧 v2 raw/compare は certificates/k5pipeline/retracted/ へ理由付きで退避)。 ---
const EXPECTED_NINF_SCHEMA = { pathA: 'u-pathA-ninf/v3', pathB: 'u-pathB-ninf/v3' };

class IntegrityStopSignal { constructor(report) { this.report = report; } }

// --- 純関数本体 ---
export function compareNinf(A, B, bundle, meta = {}) {
  const report = { schema: 'u-compare-ninf/v3', ...meta, idA: A.id, idB: B.id };
  function stop(reason) {
    report.result = 'INTEGRITY_STOP';
    report.reason = reason;
    throw new IntegrityStopSignal(report);
  }

  try {
    if (A.id !== B.id) stop(`id mismatch: pathA.id=${A.id} pathB.id=${B.id}`);
    if (A.branch !== 'N_infty' || B.branch !== 'N_infty') {
      stop(`branch label mismatch (I-m): pathA.branch=${A.branch} pathB.branch=${B.branch} (both must be 'N_infty')`);
    }
    if (A.M === undefined || A.M === null || B.M === undefined || B.M === null) {
      stop(`(裁定39 F2) M field is missing on pathA and/or pathB raw (required field)`);
    }
    if (A.M !== B.M) stop(`M mismatch: pathA.M=${A.M} pathB.M=${B.M}`);

    // --- I-m (便 37 F3/R-8・裁定39/便38 F2): schema 名(方向付き exact
    // equality・欠落は STOP)と枝ラベルの突合 + P0_type 整合(N_infty では
    // 常に nonWeierstrass -- 補題 R1-M0 3.。欠落も STOP、旧版は任意 field
    // だった)。x0/y0(main-path 専用 field)の混入も拒否する。 ---
    for (const [raw, label, pathKey] of [[A, 'pathA', 'pathA'], [B, 'pathB', 'pathB']]) {
      if (raw.schema === undefined || raw.schema === null) {
        stop(`(I-m/裁定39 F2) ${label}.schema is missing -- schema field is required (must equal '${EXPECTED_NINF_SCHEMA[pathKey]}')`);
      }
      if (raw.schema !== EXPECTED_NINF_SCHEMA[pathKey]) {
        stop(`(I-m/裁定39 F2) ${label}.schema='${raw.schema}' does not match the required directional schema '${EXPECTED_NINF_SCHEMA[pathKey]}' (schema names are not interchangeable between pathA/pathB -- swap attack rejected)`);
      }
      if (raw.P0_type === undefined || raw.P0_type === null) {
        stop(`(I-m/裁定39 F2) ${label}.P0_type is missing -- must be present and equal 'nonWeierstrass' for branch='N_infty' (Lemma R1-M0 3.)`);
      }
      if (raw.P0_type !== 'nonWeierstrass') {
        stop(`(I-m) ${label}.P0_type must be 'nonWeierstrass' for branch='N_infty' (Lemma R1-M0 3.), got '${raw.P0_type}'`);
      }
      if (raw.x0 !== undefined || raw.y0 !== undefined) {
        stop(`(裁定39 F2) ${label} carries forbidden field(s) x0/y0 (main-path-only fields must not appear on an N_infty raw): x0=${raw.x0} y0=${raw.y0}`);
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

    // --- 裁定40/便39 F1.2: chat の実値検査(自己申告 boolean flag だけに
    // 依存しない)。旧版は chat_equals_1===true という自己申告を信じるのみで、
    // raw.chat 自体の値・pathA/pathB 相互一致・pathB.N_lambda_coeffs_ascending
    // の値を一度も検査していなかった(Sol 便39 F1.2 の矛盾 raw 攻撃: chat="2"
    // かつ N_lambda=["2"] にしても chat_equals_1=true を保てば旧版は ACCEPT
    // した)。本版は次の三点を独立に exact rational として検査する: ---
    if (A.chat === undefined || A.chat === null) stop('(裁定40 F1.2) pathA.chat is missing (required field)');
    if (B.chat === undefined || B.chat === null) stop('(裁定40 F1.2) pathB.chat is missing (required field)');
    const chatA = parseRat(A.chat);
    const chatB = parseRat(B.chat);
    if (!ratEq(chatA, RAT_ONE)) stop(`(裁定40 F1.2) pathA.chat='${A.chat}' is not exactly the rational 1 (N∞-4 requires chat=1, not just the self-reported chat_equals_1 flag)`);
    if (!ratEq(chatB, RAT_ONE)) stop(`(裁定40 F1.2) pathB.chat='${B.chat}' is not exactly the rational 1 (N∞-4 requires chat=1, not just the self-reported chat_equals_1 flag)`);
    if (!ratEq(chatA, chatB)) stop(`(裁定40 F1.2) pathA.chat='${A.chat}' and pathB.chat='${B.chat}' disagree (mutual exact-value check)`);

    // 2. pathB.N_lambda_coeffs_ascending は宣言済みの定数多項式であり、
    //    厳密に [1] (trailing zeros を除いて長さ 1・値 1) と一致すること。
    if (!Array.isArray(B.N_lambda_coeffs_ascending) || B.N_lambda_coeffs_ascending.length === 0) {
      stop('(裁定40 F1.2) pathB.N_lambda_coeffs_ascending is missing or empty (required field)');
    }
    const nLambdaDeclared = polyTrimRat(B.N_lambda_coeffs_ascending.map(parseRat));
    if (nLambdaDeclared.length !== 1 || !ratEq(nLambdaDeclared[0], RAT_ONE)) {
      stop(`(裁定40 F1.2) pathB.N_lambda_coeffs_ascending does not equal the constant polynomial [1]: [${B.N_lambda_coeffs_ascending.join(',')}]`);
    }

    // 3. checker 自身が A_coeffs_ascending/B_coeffs_ascending/f_coeffs_ascending
    //    から A^2-B^2*f を独立に再計算し、厳密に定数多項式 1 であることを
    //    確認する(自己申告の chat 値・N_lambda_coeffs_ascending 値を一切
    //    信頼せず、model field として既に検査済みの A/B/f のみから導出する)。
    const AcoeffsRat = A.A_coeffs_ascending.map(parseRat);
    const BcoeffsRat = A.B_coeffs_ascending.map(parseRat); // A/B間で既に等しいと fieldChecks で確認済み
    const fcoeffsRat = A.f_coeffs_ascending.map(parseRat);
    const A2rat = polyMulRat(AcoeffsRat, AcoeffsRat);
    const B2rat = polyMulRat(BcoeffsRat, BcoeffsRat);
    const B2frat = polyMulRat(B2rat, fcoeffsRat);
    const NlambdaRecomputed = polySubRat(A2rat, B2frat);
    report.recomputed_N_lambda_coeffs_ascending = NlambdaRecomputed.map(ratStr);
    if (NlambdaRecomputed.length !== 1 || !ratEq(NlambdaRecomputed[0], RAT_ONE)) {
      stop(`(裁定40 F1.2) checker が A_coeffs_ascending/B_coeffs_ascending/f_coeffs_ascending から独立に再計算した A^2-B^2*f が定数 1 ではない: [${NlambdaRecomputed.map(ratStr).join(',')}] (declared chat=${A.chat}/${B.chat} does not match the independently recomputed value)`);
    }
    report.chat = ratStr(chatA);

    // --- 裁定39 F2(必須 field a_M/b_Mm3/chat): 存在必須化 + 係数列から
    // 独立に再抽出した値との一致(自己申告 boolean flag だけに依存しない)。
    // deg_A_equals_M/deg_B_equals_Mminus3 が true である前提のもとで、
    // a_M = A_coeffs_ascending[M]、b_{M-3} = B_coeffs_ascending[M-3]。---
    for (const [raw, label] of [[A, 'pathA'], [B, 'pathB']]) {
      if (raw.chat === undefined || raw.chat === null) stop(`(裁定39 F2) ${label}.chat is missing (required field)`);
      if (raw.a_M === undefined || raw.a_M === null) stop(`(裁定39 F2) ${label}.a_M is missing (required field)`);
      if (raw.b_Mm3 === undefined || raw.b_Mm3 === null) stop(`(裁定39 F2) ${label}.b_Mm3 is missing (required field)`);
      const extractedAM = raw.A_coeffs_ascending[raw.M];
      const extractedBMm3 = raw.B_coeffs_ascending[raw.M - 3];
      if (extractedAM === undefined || !ratEq(parseRat(raw.a_M), parseRat(extractedAM))) {
        stop(`(裁定39 F2) ${label}.a_M='${raw.a_M}' does not match the value independently re-extracted from A_coeffs_ascending[M]='${extractedAM}'`);
      }
      if (extractedBMm3 === undefined || !ratEq(parseRat(raw.b_Mm3), parseRat(extractedBMm3))) {
        stop(`(裁定39 F2) ${label}.b_Mm3='${raw.b_Mm3}' does not match the value independently re-extracted from B_coeffs_ascending[M-3]='${extractedBMm3}'`);
      }
    }

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
    // 第三の bundle ファイルに対して行う。---
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
      stop(`bundle.expected_model_digest is missing (mode=${bundle.mode}) -- R-7 requires this to be present and bound, not silently skipped`);
    }
    const bundleRecomputedDigest = createHash('sha256').update(bundle.canonical_model_string, 'utf8').digest('hex');
    if (bundleRecomputedDigest !== bundle.expected_model_digest) {
      stop(`bundle self-consistency failure: sha256(bundle.canonical_model_string)=${bundleRecomputedDigest} != bundle.expected_model_digest=${bundle.expected_model_digest}`);
    }
    if (bundle.canonical_model_string !== recomputeCanonicalModelStringNinf(A)) {
      stop(`(I-l) bundle.canonical_model_string does not match the string reconstructed from pathA raw fields -- pathA does not match the frozen bundle (independent of pathA's own self-reported expected_model_digest)`);
    }
    if (bundle.canonical_model_string !== recomputeCanonicalModelStringNinf(B)) {
      stop(`(I-l) bundle.canonical_model_string does not match the string reconstructed from pathB raw fields -- pathB does not match the frozen bundle`);
    }
    report.bundle_mode = bundle.mode;
    report.bundle_expected_model_digest = bundle.expected_model_digest;
    report.expected_digest_check = 'BOUND (bundle-external, R-7/I-l closed per 裁定38/便37 F2)';
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
    return report;
  } catch (e) {
    if (e instanceof IntegrityStopSignal) return e.report;
    // 裁定41/便40 F1.2 要求 4: malformed rational は純関数 API でも
    // structured INTEGRITY_STOP にする(呼び出し元に生の例外を投げない)。
    if (e instanceof RationalFormatError) {
      report.result = 'INTEGRITY_STOP';
      report.reason = `(strict rational parser) ${e.message}`;
      return report;
    }
    throw e;
  }
}

// --- CLI wrapper: 直接実行された場合のみ発火(import 時は発火しない)。
// 裁定40/便39 F1.3 修理: 旧版は「direct-run 判定」と「runCli() 本体の
// JSON.parse/BigInt/I-O/型例外」を同じ最外 catch で握り潰し、非 JSON 入力を
// 与えても無出力・exit 0 になっていた(Sol 便39 実測)。本版は
// runCliGuarded() 内の try/catch を runCli() 本体の例外だけに限定し、
// 予期しない例外は stderr に INTEGRITY_STOP メッセージを出して非零 exit
// する(direct-run 判定自体は try で囲まない -- pathToFileURL/import.meta.url
// の比較は通常例外を投げない静的 import なので、握りつぶす catch は不要)。 ---
function runCli() {
  const [pathAFile, pathBFile, bundleFile] = process.argv.slice(2);
  if (!pathAFile || !pathBFile || !bundleFile) {
    console.error('usage: node u-compare-ninf.mjs <ninf pathA.json> <pathB.json> <bundle.json>');
    console.error('(bundle.json is REQUIRED -- R-7/I-l: raw-only expected-digest self-comparison is not accepted, cf. Sol 便37 F2)');
    process.exit(2);
  }
  const A = JSON.parse(readFileSync(pathAFile, 'utf8'));
  const B = JSON.parse(readFileSync(pathBFile, 'utf8'));
  const bundle = JSON.parse(readFileSync(bundleFile, 'utf8'));
  const report = compareNinf(A, B, bundle, { pathAFile, pathBFile, bundleFile });
  console.log(JSON.stringify(report, null, 2));
  if (report.result !== 'ACCEPT') process.exit(1);
}
function runCliGuarded() {
  try {
    runCli();
  } catch (e) {
    process.stderr.write(`INTEGRITY_STOP: unhandled exception in u-compare-ninf.mjs CLI wrapper -- ${e && e.stack ? e.stack : e}\n`);
    process.exit(1);
  }
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  runCliGuarded();
}
