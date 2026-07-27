#!/usr/bin/env node
// crosscheck/check-qparse-fail-closed.mjs -- 司令塔独自攻撃(裁定41続報)
// 対応の adversarial 較正。
//
// 対象: crosscheck/u-extract-pathB-lib.mjs の `Q.parse`(探索器側・path B
// 抽出 library が使う BigInt 有理数 parser)と
// crosscheck/cyclo-ring-lib.mjs の `Q.parse`(check-kummer 系が import する
// 円分体環演算 library の同名 parser)。両者は独立実装(u-extract-pathB-lib
// は search/u-extract-pathA.g と関数・データ構造を共有しない既存方針を保つ
// ため、RationalFormatError も独立に再定義している)。
//
// 司令塔の実測: 旧版はどちらも `str.split('/')` の先頭 2 要素だけを黙って
// 読み("1/2/3" が黙って 1/2 として parse された)、`.trim()` により
// " 1/2" のような空白混入も通した(denominator 0 は Q コンストラクタが
// 元々拒否済み)。本版は両 Q.parse を u-compare 系と同じ全文一致 grammar
// (`^[+-]?\d+(?:\/[+-]?\d+)?$`・空白拒否)へ硬化した。
//
// 実行: node crosscheck/check-qparse-fail-closed.mjs

import { pathToFileURL } from 'node:url';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const imp = (f) => import(pathToFileURL(join(ROOT, f)).href);

const { Q: QPathB, RationalFormatError: ErrPathB } = await imp('crosscheck/u-extract-pathB-lib.mjs');
const { Q: QCyclo, RationalFormatError: ErrCyclo } = await imp('crosscheck/cyclo-ring-lib.mjs');

let pass = 0, fail = 0;
function expectThrow(name, fn, ErrClass) {
  try {
    fn();
    console.log(`[FAIL] ${name}: expected a throw, but call succeeded`);
    fail++;
  } catch (e) {
    if (e instanceof ErrClass) {
      console.log(`[PASS] ${name}: rejected as expected -- ${e.message}`);
      pass++;
    } else {
      console.log(`[FAIL] ${name}: threw the wrong error type -- ${e.constructor.name}: ${e.message}`);
      fail++;
    }
  }
}
function expectValue(name, fn, expected) {
  try {
    const v = fn();
    const s = v.toString();
    if (s === expected) {
      console.log(`[PASS] ${name}: ${s}`);
      pass++;
    } else {
      console.log(`[FAIL] ${name}: got ${s}, expected ${expected}`);
      fail++;
    }
  } catch (e) {
    console.log(`[FAIL] ${name}: expected success (${expected}), but threw -- ${e.message}`);
    fail++;
  }
}

for (const [label, Q, Err] of [
  ['crosscheck/u-extract-pathB-lib.mjs Q', QPathB, ErrPathB],
  ['crosscheck/cyclo-ring-lib.mjs Q', QCyclo, ErrCyclo],
]) {
  // ---- attacks: must reject ----
  expectThrow(`${label}.parse("1/2/3") (two or more '/') rejected`, () => Q.parse('1/2/3'), Err);
  expectThrow(`${label}.parse(" 1") (leading space) rejected`, () => Q.parse(' 1'), Err);
  expectThrow(`${label}.parse("1 ") (trailing space) rejected`, () => Q.parse('1 '), Err);
  expectThrow(`${label}.parse(" 1/2") (leading space, fraction) rejected`, () => Q.parse(' 1/2'), Err);
  expectThrow(`${label}.parse("1/ 2") (space after slash) rejected`, () => Q.parse('1/ 2'), Err);
  expectThrow(`${label}.parse("") (empty string) rejected`, () => Q.parse(''), Err);
  expectThrow(`${label}.parse("1/") (empty denominator) rejected`, () => Q.parse('1/'), Err);
  expectThrow(`${label}.parse("/1") (empty numerator) rejected`, () => Q.parse('/1'), Err);
  // denominator 0 was already rejected pre-existing (Q constructor) -- confirm still true
  expectThrow(`${label}.parse("0/0") (denominator zero) rejected (pre-existing Q constructor behavior)`, () => Q.parse('0/0'), Error);
  expectThrow(`${label}.parse("1/0") (denominator zero) rejected (pre-existing Q constructor behavior)`, () => Q.parse('1/0'), Error);

  // ---- must still accept (per 司令塔 confirmation: within-spec, keep as-is) ----
  expectValue(`${label}.parse("1/2") accepted`, () => Q.parse('1/2'), '1/2');
  expectValue(`${label}.parse("-4") accepted`, () => Q.parse('-4'), '-4');
  expectValue(`${label}.parse("+1") accepted (leading '+' is in-spec)`, () => Q.parse('+1'), '1');
  expectValue(`${label}.parse("2/1") accepted (non-reduced input reduces correctly)`, () => Q.parse('2/1'), '2');
  expectValue(`${label}.parse("1/-2") accepted (sign on denominator, normalizes to -1/2)`, () => Q.parse('1/-2'), '-1/2');
}

console.log(`\n=== ${pass}/${pass + fail} PASS ===`);
if (fail > 0) process.exitCode = 1;
