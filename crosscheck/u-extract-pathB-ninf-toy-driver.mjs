#!/usr/bin/env node
// crosscheck/u-extract-pathB-ninf-toy-driver.mjs -- R-5 (N_infty) 経路 B-iii 玩具較正・driver
// 委嘱: 便 36(裁定 36_ben35)。crosscheck/u-extract-pathB-lib.mjs の
// extractPathB_Ninf を、Rule 1 S0.4-3 の M=n=3 玩具族で較正する
// (search/u-extract-pathA-ninf-toy-driver.g と同一の玩具モデル -- 二経路
// 比較のため意図的に同じ数値を使うが、計算方式・実装は完全に独立: 級数を
// 一切使わない多項式演算のみ)。
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

const raw = {
  id: 'toy-ninf-M3',
  n: 3,
  f_coeffs_ascending: ['-1', '2', '1', '2', '2', '0', '1'],
  A_coeffs_ascending: ['1', '1', '0', '1'],
  B_coeffs_ascending: ['1'],
};

const model = loadModelNinf(raw);
const report = extractPathB_Ninf(model);

console.log('=== u-extract-pathB-ninf toy calibration (M=n=3, synthetic) ===');
console.log(JSON.stringify(report, null, 2));

writeFileSync(join(ROOT, 'certificates', 'k5pipeline', 'toy-ninf-M3-pathB.json'), JSON.stringify(report, null, 2) + '\n');
console.log('\nwrote certificates/k5pipeline/toy-ninf-M3-pathB.json');
