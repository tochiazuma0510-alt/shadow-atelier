#!/usr/bin/env node
// crosscheck/covariance-bridge-in.mjs -- covariance BRIDGE-IN 配線の実体化
// (裁定 38/便 37 F5.2 (3) 修理: 「橋段で使う同一 checker への配線」)。
//
// 身分: これは atomic Freeze 2 の実配線**そのもの**ではない。K5 の実
// b_sq/b_ns はまだ measured/frozen ではないため(sealed automation schema の
// 事前登録・BRIDGE-IN の受理条件がまだ閉じていない)、本ファイルはコマンド
// ライン引数として b_sq, b_ns を受け取り、crosscheck/covariance-lib.mjs の
// computeAEff を crosscheck/check-covariance-envelope.mjs と**まったく同じ
// import**で呼ぶ、という「配線の形」だけを実演する driver である。
//
// 実 K5 データには接触しない(manifest v1.4 I-b∞: ĉ_μ・μ/Pell の値・平方類・
// 平方因子・符号は凍結 2 前に人間へ見せない -- 本ファイルは b_sq/b_ns を
// 引数として要求するだけで、どの値がそれかを知らない・推測しない)。
//
// 実行: node crosscheck/covariance-bridge-in.mjs <b_sq> <b_ns>
//   (b_sq, b_ns in (Z/10)^x = {1,3,7,9}. 引数を渡さなければ「未配線」を
//    正直に報告して終了する -- BRIDGE-UNKNOWN のまま、fail-open しない。)

import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { computeAEff, unitsMod } from './covariance-lib.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

const [bSqArg, bNsArg] = process.argv.slice(2);

const K5_SQ_PATH = join(ROOT, 'certificates', 'k5fixture', 'K5-sq.json');
const K5_NS_PATH = join(ROOT, 'certificates', 'k5fixture', 'K5-ns.json');
const k5Sq = JSON.parse(readFileSync(K5_SQ_PATH, 'utf8'));
const k5Ns = JSON.parse(readFileSync(K5_NS_PATH, 'utf8'));
const aSealedSq = k5Sq.rho0_and_j.a_sealed;
const aSealedNs = k5Ns.rho0_and_j.a_sealed;
if (aSealedSq !== aSealedNs) {
  console.error(`INTEGRITY_STOP: K5-sq/K5-ns a_sealed disagree (${aSealedSq} vs ${aSealedNs})`);
  process.exit(1);
}
const FORMAL_A = aSealedSq;

if (bSqArg === undefined || bNsArg === undefined) {
  console.log(JSON.stringify({
    schema: 'k5pipeline/covariance-bridge-in/v1',
    status: 'BRIDGE-UNKNOWN (not wired to a real value)',
    note: '実 b_sq/b_ns はコマンドライン引数として与えられていない。atomic Freeze 2 が b_sq=b_ns を受理条件として確定するまで、この driver は正直に UNKNOWN を報告する(fail-open しない)。使い方: node crosscheck/covariance-bridge-in.mjs <b_sq> <b_ns> (b_sq,b_ns in (Z/10)^x = {1,3,7,9}).',
    formal_a_from_fixture: FORMAL_A,
  }, null, 2));
  process.exit(2);
}

const bSq = Number(bSqArg);
const bNs = Number(bNsArg);
const unitsE10 = unitsMod(10);
if (!unitsE10.includes(bSq) || !unitsE10.includes(bNs)) {
  console.error(`INTEGRITY_STOP: b_sq, b_ns must be in (Z/10)^x = {${unitsE10.join(',')}}, got b_sq=${bSqArg} b_ns=${bNsArg}`);
  process.exit(1);
}

// 便37 F5.2 (4) の文言訂正: b_sq=b_ns は BRIDGE-IN / atomic Freeze 2 の
// **受理条件**そのものであり、「受理後に代入する」ものではない。したがって
// この driver は受理判定の一部としてこの等式を評価する(受理前・u 開示前)。
const aEff = computeAEff(bSq, bNs, FORMAL_A);
const acceptanceConditionMet = bSq === bNs;

console.log(JSON.stringify({
  schema: 'k5pipeline/covariance-bridge-in/v1',
  status: 'WIRED (same crosscheck/covariance-lib.mjs computeAEff as check-covariance-envelope.mjs)',
  formal_a_from_fixture: FORMAL_A,
  b_sq: bSq,
  b_ns: bNs,
  a_eff: aEff,
  acceptance_rule_b_sq_eq_b_ns: acceptanceConditionMet,
  note: acceptanceConditionMet
    ? 'b_sq=b_ns holds: SS7.3 acceptance condition for atomic Freeze 2 / BRIDGE-IN is met at this stage (before acceptance, before u disclosure).'
    : 'b_sq != b_ns: SS7.3 acceptance condition is NOT met -- this would be an INTEGRITY_STOP at the actual bridge stage, not an accepted BRIDGE-IN.',
}, null, 2));
if (!acceptanceConditionMet) process.exitCode = 1;
