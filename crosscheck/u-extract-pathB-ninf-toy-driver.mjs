#!/usr/bin/env node
// crosscheck/u-extract-pathB-ninf-toy-driver.mjs -- R-5 ライブラリ unit test(M=3, synthetic)
// 委嘱: 便 36(裁定_36_ben35 起草・裁定_37_ben36 で production 化を要求・便 36 F3.2)。
// crosscheck/u-extract-pathB-lib.mjs の extractPathB_Ninf(schema v2)を、
// search/u-extract-pathA-ninf-toy-driver.g と同一の玩具モデルで叩く(二経路
// 比較のため意図的に同じ数値を使うが、計算方式・実装は完全に独立: 級数を
// 一切使わない多項式演算のみ)。
//
// *** 位置づけ(便 36 F3.2 の裁定を反映・重要) ***
// 本ファイルは **R-5 の production 較正ではない**。extractPathB_Ninf ライブラリ
// 関数(schema v2 の配線・(N∞-1)-(N∞-4) の fail-closed 検査・gcd(f,f')=1・
// model digest 束縛)の unit test である。R-5 の production 較正(M=10)は
// crosscheck/u-extract-pathB-ninf-production-driver.mjs が別途行う。
//
// *** SYNTHETIC のみ *** K^(5) の実 fixture には (N_infty) が無い。
//
// 実行: node crosscheck/u-extract-pathB-ninf-toy-driver.mjs

import { writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadModelNinf, extractPathB_Ninf } from './u-extract-pathB-lib.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

// search/u-extract-pathA-ninf-toy-driver.g と同一の値(f の定数項を -1 -> 0
// に変えて chat=2 -> chat=1 へ修理した版 -- 便 36 F3.2 の (N∞-4) 要求)。
const raw = {
  id: 'toy-ninf-M3',
  branch: 'N_infty',
  M: 3,
  f_coeffs_ascending: ['0', '2', '1', '2', '2', '0', '1'],
  A_coeffs_ascending: ['1', '1', '0', '1'],
  B_coeffs_ascending: ['1'],
  series_length: 20,
  expected_model_digest: '9e5563726c0fbd544ad13e569ed368baaac1ade58d1be1617548e6570cacfe1d',
};

const model = loadModelNinf(raw);
const report = extractPathB_Ninf(model);

console.log('=== u-extract-pathB-ninf unit test (M=3, synthetic, schema v2) ===');
console.log(JSON.stringify(report, null, 2));

writeFileSync(join(ROOT, 'certificates', 'k5pipeline', 'toy-ninf-M3-pathB.json'), JSON.stringify(report, null, 2) + '\n');
console.log('\nwrote certificates/k5pipeline/toy-ninf-M3-pathB.json');
