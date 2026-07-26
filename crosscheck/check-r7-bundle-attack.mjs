#!/usr/bin/env node
// crosscheck/check-r7-bundle-attack.mjs -- R-7 の bundle 束縛 adversarial 較正
// (裁定 38/便 37 F2 blocker 1・**便 38 F1.2/裁定 39 対応で in-process 化**)。
//
// 目的: Sol 便 37 F2 が明記した攻撃そのものを実行して確認する:
//   「両 driver が同じ誤ったモデル M' を転記し、同時に
//    expected_model_digest = digest(M') を入れれば ACCEPT する」
// 旧 u-compare-ninf.mjs / u-compare.mjs は raw 二本の自己申告
// expected_model_digest 同士を比較するだけだったので、この攻撃は通ってしまう
// (便37 F2 の指摘)。修理後の checker は第三の独立 bundle ファイルを必須
// 引数とし、raw から再構成した canonical string を bundle の
// canonical_model_string と逐語照合するので、この攻撃は落ちるはずである。
//
// 便 38 F1.2 の指摘: 旧版は nested `execFileSync('node', ...)` で子 process を
// 起動して再現していたが、この管理下 Windows セッションでは子 process の
// stdout 捕捉が `EPERM` で拒まれ、5/5 のうち 2 件が harness の問題で失敗した
// (checker 自体の判定は正しかった -- 便38 F1.2)。本版は
// `crosscheck/u-compare-ninf.mjs` が export する純関数 `compareNinf` を
// **in-process で直接呼ぶ**ことで nested process capture への依存を除去する。
//
// 本テストは実際に:
//   1. toy-ninf-M3 の正しい raw 二本を、係数を一箇所だけ変えた「同じ誤り」
//      (pathA/pathB 両方に同じ誤転記)に書き換える。
//   2. 両者の model_digest / expected_model_digest を、その誤ったモデルから
//      再計算した(内部無矛盾な)値に揃える(=「二 raw は相互に整合して
//      見える」状態を作る -- これが旧 checker では ACCEPT してしまう状態)。
//   3. 本物の(正しい)bundle オブジェクト(toy-ninf-M3-bundle.json)に対して
//      compareNinf() を呼び、INTEGRITY_STOP になることを確認する(bundle と
//      raw の canonical string が食い違うため)。
//
// 実行: node crosscheck/check-r7-bundle-attack.mjs

import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { compareNinf } from './u-compare-ninf.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

let pass = 0, fail = 0;
function report(name, ok, extra = '') {
  if (ok) { pass++; console.log(`[PASS] ${name}${extra ? '  ' + extra : ''}`); }
  else { fail++; console.log(`[FAIL] ${name}${extra ? '  ' + extra : ''}`); }
}

const rawA = JSON.parse(readFileSync(join(ROOT, 'certificates/k5pipeline/toy-ninf-M3-pathA.json'), 'utf8'));
const rawB = JSON.parse(readFileSync(join(ROOT, 'certificates/k5pipeline/toy-ninf-M3-pathB.json'), 'utf8'));
const goodBundle = JSON.parse(readFileSync(join(ROOT, 'certificates/k5pipeline/toy-ninf-M3-bundle.json'), 'utf8'));

// ---- attack: both drivers mistranscribe the same coefficient the same
// way (A_coeffs_ascending[1]: '1' -> '2'), and both embed a
// self-consistent (but WRONG) expected_model_digest computed from the
// corrupted model itself. ----
function canonicalNinf(raw) {
  const list = (xs) => xs.join(',');
  return `id=${raw.id};branch=N_infty;M=${raw.M};f=[${list(raw.f_coeffs_ascending)}];A=[${list(raw.A_coeffs_ascending)}];B=[${list(raw.B_coeffs_ascending)}]`;
}
function digestOf(s) { return createHash('sha256').update(s, 'utf8').digest('hex'); }

const badA = { ...rawA, A_coeffs_ascending: ['1', '2', '0', '1'] }; // same corruption in both
const badB = { ...rawB, A_coeffs_ascending: ['1', '2', '0', '1'] };
const corruptedDigest = digestOf(canonicalNinf(badA));
badA.model_digest = corruptedDigest;
badA.expected_model_digest = corruptedDigest;
badB.model_digest = corruptedDigest;
badB.expected_model_digest = corruptedDigest;
// a_M was corrupted too (A_coeffs_ascending[1] changed, not A_coeffs_ascending[M],
// so a_M/b_Mm3 independent-recompute check in u-compare-ninf.mjs still holds
// for this attack -- the corruption is at a non-boundary coefficient index).

// sanity: the two corrupted raws DO agree with each other (mutual
// model_digest match, mutual expected_model_digest match) -- this is
// exactly the state that a raw-only checker would ACCEPT.
report('sanity: both corrupted raws mutually agree (model_digest)', badA.model_digest === badB.model_digest);
report('sanity: both corrupted raws mutually agree (expected_model_digest)', badA.expected_model_digest === badB.expected_model_digest);
report('sanity: corrupted model_digest differs from the true frozen bundle digest', corruptedDigest !== goodBundle.expected_model_digest);

// ---- run the actual checker (in-process) against the REAL bundle ----
const realBundleResult = compareNinf(badA, badB, goodBundle);
report(
  'R-7 (便37 F2): checker rejects two mutually-consistent-but-wrong raws when checked against the REAL frozen bundle',
  realBundleResult.result === 'INTEGRITY_STOP',
  `result=${realBundleResult.result} reason=${realBundleResult.reason}`
);

// ---- control: same corrupted raws against a bundle regenerated FROM the
// corrupted model (i.e. if the "bundle" were also compromised, this
// demonstrates the mechanism's logic is otherwise sound -- not a required
// adversarial case, just confirms the corrupted-raw plumbing is coherent) ----
const matchingBundle = {
  schema: 'k5pipeline/frozen-bundle/v1',
  mode: 'calibration',
  id: 'toy-ninf-M3',
  branch: 'N_infty',
  canonical_model_string: canonicalNinf(badA),
  expected_model_digest: corruptedDigest,
};
const matchingBundleResult = compareNinf(badA, badB, matchingBundle);
report(
  'control: checker ACCEPTs when the (also-corrupted) bundle matches the corrupted raws exactly -- confirms the mechanism checks bundle-vs-raw bytes, not "is the model correct"',
  matchingBundleResult.result === 'ACCEPT'
);

console.log(`\n=== ${pass}/${pass + fail} PASS ===`);
if (fail > 0) process.exitCode = 1;
