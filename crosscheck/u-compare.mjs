// crosscheck/u-compare.mjs
// Rule 1 SS6.3 (4) 第三の checker(**裁定 38/便 37 F2/F3 で bundle 束縛へ修理・
// 裁定 39/便 38 F2 で schema gate を fail-closed 化・便 38 F1.2 対応で in-process
// 呼び出し用の純関数として export**)。
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
//   1. branch, P0_type, x0, y0, f, A, B の全フィールドが両 raw で一致すること。
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
// 便 38 F2(裁定 39 blocker 1): 旧版は `raw.schema && !ALLOWED_MAIN_SCHEMAS.has(...)`
// という fail-open な検査だった(schema 欠落時は無条件通過・pathA/pathB を
// 同一集合で検査するため方向を交換しても通った)。本版は
//   (a) schema field の**存在を必須化**(欠落は INTEGRITY_STOP)、
//   (b) pathA は 'u-pathA/v3'、pathB は 'u-pathB/v3' への**方向付き exact
//       equality**(集合所属ではない -- 交換すれば falsify する)
// に修理する。
//
// 使い方(CLI): node crosscheck/u-compare.mjs <pathA.json> <pathB.json> <bundle.json>
// 使い方(import): import { compareMain } from './u-compare.mjs'; compareMain(A, B, bundle)
//   -- 純関数。ファイル I/O・console.log・process.exit を行わない。report
//   オブジェクト(result: 'ACCEPT' | 'INTEGRITY_STOP' を含む)を返すのみ。

import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';

function gcdBig(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { [a, b] = [b, a % b]; } return a; }
// --- 裁定41/便40 F1.2: strict rational literal grammar(全文一致・単一の
// regex で符号付き整数 or 分子/分母一組だけを許す)。空の分子・分母・二本
// 以上の '/'・分母 0 はすべて RationalFormatError として拒否する(交差積
// 等値判定 ratEq に「0/0 は何にでも等しい」「1/0 同士は等しい」という穴を
// 開けない -- Sol 便40 F1.2 の指摘)。malformed rational は純関数 API
// (compareMain)でも structured INTEGRITY_STOP になるよう、下の catch で
// この Error クラスを捕捉して report へ変換する。
// **司令塔独自攻撃(裁定41続報)修理**: 旧版は正規表現の前に
// `String(s).trim()` を呼んでおり、"chat=\" 1\"" のような先頭/末尾空白が
// 黙って正規化されて ACCEPT されていた(「全文 grammar」の趣旨に反する)。
// trim を廃止し、**入力文字列そのまま**が正規表現に一致することを要求する
// (空白混入は拒否)。 ---
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

// --- 便 38 F2/裁定 39 blocker 1: pathA/pathB は方向付き exact equality
// (集合所属ではない -- 交換攻撃を弾くため)。---
const EXPECTED_MAIN_SCHEMA = { pathA: 'u-pathA/v3', pathB: 'u-pathB/v3' };

class IntegrityStopSignal { constructor(report) { this.report = report; } }

// --- 純関数本体: I/O・console.log・process.exit を行わない ---
export function compareMain(A, B, bundle, meta = {}) {
  const report = { schema: 'u-compare/v3', ...meta, idA: A.id, idB: B.id };
  function stop(reason) {
    report.result = 'INTEGRITY_STOP';
    report.reason = reason;
    throw new IntegrityStopSignal(report);
  }

  try {
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
      stop(`bundle.schema must be 'model-spec/v1' (with bridge_mode='calibration_pre_bridge') or 'k5pipeline/frozen-bundle/v1', got '${bundle.schema}'`);
    }

    if (A.id !== B.id) stop(`id mismatch: pathA.id=${A.id} pathB.id=${B.id}`);
    if (A.M !== B.M) stop(`M mismatch: pathA.M=${A.M} pathB.M=${B.M}`);

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
      if (!ok) stop(`model field mismatch: ${field} differs between pathA and pathB raw (二 raw が同一モデル由来であることが検査できない)`);
    }

    // --- I-m(便 37 F3/R-8): 大域枝 enum・schema 名の突合(裁定39/便38 F2:
    // 方向付き exact equality・欠落は STOP)・branch=W の整合規則 ---
    const GLOBAL_BRANCH_ENUM = ['W', 'N_aff'];
    for (const [raw, label, pathKey] of [[A, 'pathA', 'pathA'], [B, 'pathB', 'pathB']]) {
      if (!GLOBAL_BRANCH_ENUM.includes(raw.branch)) {
        stop(`(I-m) ${label}.branch must be one of {${GLOBAL_BRANCH_ENUM.join(', ')}}, got '${raw.branch}' (N_infty must use u-compare-ninf.mjs, not this checker)`);
      }
      if (raw.schema === undefined || raw.schema === null) {
        stop(`(I-m/裁定39 F2) ${label}.schema is missing -- schema field is required (must equal '${EXPECTED_MAIN_SCHEMA[pathKey]}')`);
      }
      if (raw.schema !== EXPECTED_MAIN_SCHEMA[pathKey]) {
        stop(`(I-m/裁定39 F2) ${label}.schema='${raw.schema}' does not match the required directional schema '${EXPECTED_MAIN_SCHEMA[pathKey]}' (schema names are not interchangeable between pathA/pathB -- swap attack rejected)`);
      }
      if (raw.branch === 'W' && raw.P0_type !== 'nonWeierstrass') {
        stop(`(I-m) ${label}: branch='W' requires P0_type='nonWeierstrass' (Lemma S5-W / Rule 1 SS4.1 "v1.2 の絞り込み"), got P0_type='${raw.P0_type}'`);
      }
    }
    if (bundleId !== A.id) stop(`bundle id (${bundleId}) does not match raw id (${A.id})`);
    if (bundle.branch !== undefined && bundle.branch !== A.branch) {
      stop(`bundle.branch (${bundle.branch}) does not match raw branch (${A.branch})`);
    }

    // --- model_digest 突合: embed 値の一致 + この checker 自身による独立再計算 ---
    if (!A.model_digest || !B.model_digest) stop('model_digest missing on pathA and/or pathB raw(便 34 以降の raw は model_digest を embed する必要がある)');
    if (A.model_digest !== B.model_digest) stop(`model_digest mismatch: pathA=${A.model_digest} pathB=${B.model_digest}`);
    const recomputedA = recomputeModelDigest(A);
    const recomputedB = recomputeModelDigest(B);
    report.recomputed_model_digest_pathA = recomputedA;
    report.recomputed_model_digest_pathB = recomputedB;
    if (recomputedA !== A.model_digest || recomputedB !== B.model_digest || recomputedA !== recomputedB) {
      stop(`independently recomputed model_digest does not match embedded value: recomputedA=${recomputedA} (embedded ${A.model_digest}), recomputedB=${recomputedB} (embedded ${B.model_digest})`);
    }
    report.model_digest = A.model_digest;

    // --- pathA 固有の curve_residual_zero(pathB には対応する検査概念がない) ---
    if (A.curve_residual_zero !== true) stop(`pathA.curve_residual_zero is not true (曲線方程式 y^2=f(x) の切断検算に失敗): ${A.curve_residual_zero}`);

    if (!A.lower_order_vanish || !B.lower_order_vanish) {
      stop(`lower-order vanish check failed: pathA=${A.lower_order_vanish} pathB=${B.lower_order_vanish}`);
    }

    const uA = parseRat(A.u_pathA);
    const uB = parseRat(B.u_pathB);

    // --- u != 0 (分岐位数 > M のまま両側 0 で ACCEPT してしまう罠の回避) ---
    if (uA.n === 0n || uB.n === 0n) {
      stop(`u must be nonzero (ord_{P0}(lambda) = M の前提が崩れている可能性): u_pathA=${ratStr(uA)} u_pathB=${ratStr(uB)}`);
    }

    // --- R-7/I-l(便 36 F3.2/F6-2・**裁定38/便37 F2 で bundle 束縛へ修理**):
    // raw の model_digest を、raw 自身の自己申告ではなく**第三の bundle
    // ファイル**の expected digest へ束縛する(§6.3-5)。
    const bundleCanonicalString = (() => {
      const idField = bundle.id ?? bundle.fixture_id;
      if (bundleIsFrozen) return bundle.canonical_model_string;
      const rat = (s) => ratStr(parseRat(s));
      const list = (xs) => xs.map(rat).join(',');
      return `id=${idField};M=${bundle.M};branch=${bundle.branch};P0_type=${bundle.P0_type};` +
        `x0=${rat(bundle.x0)};y0=${rat(bundle.y0)};` +
        `f=[${list(bundle.f_coeffs_ascending)}];A=[${list(bundle.A_coeffs_ascending)}];B=[${list(bundle.B_coeffs_ascending)}]`;
    })();

    if (bundleCanonicalString !== recomputeCanonicalModelString(A)) {
      stop(`(I-l) bundle canonical model string does not match the string reconstructed from pathA raw fields -- pathA does not match the frozen bundle/model-spec`);
    }
    if (bundleCanonicalString !== recomputeCanonicalModelString(B)) {
      stop(`(I-l) bundle canonical model string does not match the string reconstructed from pathB raw fields -- pathB does not match the frozen bundle/model-spec`);
    }

    if (bundleIsFrozen) {
      if (!bundle.expected_model_digest) {
        stop(`bundle.expected_model_digest is missing (mode=${bundle.mode}) -- R-7 requires this to be present and bound, not silently skipped`);
      }
      const bundleRecomputedDigest = createHash('sha256').update(bundle.canonical_model_string, 'utf8').digest('hex');
      if (bundleRecomputedDigest !== bundle.expected_model_digest) {
        stop(`bundle self-consistency failure: sha256(bundle.canonical_model_string)=${bundleRecomputedDigest} != bundle.expected_model_digest=${bundle.expected_model_digest}`);
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
// 裁定40/便39 F1.3 修理: u-compare-ninf.mjs と同じ修理 -- direct-run 判定と
// runCli() 本体の例外捕捉を分離し、予期しない例外は stderr へ
// INTEGRITY_STOP メッセージを出して非零 exit する(無出力・exit 0 の
// fail-open を禁止)。 ---
function runCli() {
  const [pathAFile, pathBFile, bundleFile] = process.argv.slice(2);
  if (!pathAFile || !pathBFile || !bundleFile) {
    console.error('usage: node u-compare.mjs <u_pathA.json> <u_pathB.json> <bundle-or-model-spec.json>');
    console.error('(bundle is REQUIRED -- R-7/I-l: raw-only expected-digest self-comparison is not accepted, cf. 裁定38/便37 F2)');
    process.exit(2);
  }
  const A = JSON.parse(readFileSync(pathAFile, 'utf8'));
  const B = JSON.parse(readFileSync(pathBFile, 'utf8'));
  const bundle = JSON.parse(readFileSync(bundleFile, 'utf8'));
  const report = compareMain(A, B, bundle, { pathAFile, pathBFile, bundleFile });
  console.log(JSON.stringify(report, null, 2));
  if (report.result !== 'ACCEPT') process.exit(1);
}
function runCliGuarded() {
  try {
    runCli();
  } catch (e) {
    process.stderr.write(`INTEGRITY_STOP: unhandled exception in u-compare.mjs CLI wrapper -- ${e && e.stack ? e.stack : e}\n`);
    process.exit(1);
  }
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  runCliGuarded();
}
