// crosscheck/u-extract-pathB-k3-driver.mjs
// 経路 B・K3 較正用の薄い driver。
// 委嘱: 便 34 blocker 2 (Sol 便 34 P6-E1)。
//
// 身分: 本ファイルは driver である。アルゴリズム本体(extractPathB 等)は
// crosscheck/u-extract-pathB-lib.mjs(library・凍結対象)から import するだけ
// で、model 読み込み・実行・ファイル書き出しはここに置く。将来の K5 driver
// は同じ形の新しい driver ファイルを追加すればよく、library 側は変更しない。
//
// 入力: certificates/k5fixture/<id>-model.json (model-spec/v1)
// 出力: certificates/k5pipeline/<id>-u-pathB.json

import { readFileSync, writeFileSync } from 'node:fs';
import { loadModel, extractPathB, cov1Model, Q } from './u-extract-pathB-lib.mjs';

const args = process.argv.slice(2);
const modelPath = args[0] ?? 'certificates/k5fixture/K3-regression-model.json';
const raw = JSON.parse(readFileSync(modelPath, 'utf8'));
const model = loadModel(raw);

const rBase = extractPathB(model);
console.log(`== ${rBase.id} == u_pathB = ${rBase.u_pathB}  lowerOrderVanish=${rBase.lower_order_vanish}  (${rBase.formula})  model_digest=${rBase.model_digest}`);
writeFileSync(`certificates/k5pipeline/${rBase.id}-u-pathB.json`, JSON.stringify(rBase, null, 2));

const cov1 = cov1Model(model, 2);
const rCov1 = extractPathB(cov1);
console.log(`== ${rCov1.id} == u_pathB = ${rCov1.u_pathB}  lowerOrderVanish=${rCov1.lower_order_vanish}  (${rCov1.formula})  model_digest=${rCov1.model_digest}`);
writeFileSync(`certificates/k5pipeline/${rCov1.id}-u-pathB.json`, JSON.stringify(rCov1, null, 2));

// 較正のみの参考出力(パイプラインの入力には使わない): u_pathB と cov1 の比 = k^{-2M} を厳密に検算
{
  const uBase = Q.parse(rBase.u_pathB);
  const uCov1 = Q.parse(rCov1.u_pathB);
  const kQ = Q.parse(2);
  const expectedRatio = kQ.pow(-2 * model.M);
  const actualRatio = uCov1.div(uBase);
  console.log(`COV-1 check (reference only): u_cov1/u_base = ${actualRatio}  expected k^(-2M) = ${expectedRatio}  match=${actualRatio.eq(expectedRatio)}`);
}
