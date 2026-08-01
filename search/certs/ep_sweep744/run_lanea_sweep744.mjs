// search/certs/ep_sweep744/run_lanea_sweep744.mjs
//
// Lane A batch runner for the P5 悉皆スウィープ: calls the SAME
// evaluateDecisionLane() that search/certs/ep-lanea-eval-candidate.mjs
// calls (identical import, identical function), once per candidate, looping
// in-process instead of spawning 744 separate node processes (pure
// performance choice -- the decision-lane call itself is unchanged and
// stateless per candidate, so batching does not alter what is computed).
//
// Usage: node search/certs/ep_sweep744/run_lanea_sweep744.mjs
// Reads: search/certs/ep_sweep744/candidates_744.json
// Writes: search/certs/ep_sweep744/lanea_results_744.json

import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { evaluateDecisionLane } from '../../ninfty-searcher-v2.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..', '..', '..');

function main() {
  const candFile = join(HERE, 'candidates_744.json');
  const candRaw = readFileSync(candFile);
  const candDigest = createHash('sha256').update(candRaw).digest('hex');
  const candData = JSON.parse(candRaw.toString('utf-8'));

  const searcherPath = join(ROOT, 'search', 'ninfty-searcher-v2.mjs');
  const searcherDigest = createHash('sha256').update(readFileSync(searcherPath)).digest('hex');

  const results = candData.candidates.map((entry) => {
    let out;
    try {
      const r = evaluateDecisionLane(entry.candidate);
      out = { verdict: r.verdict, primary_reason_code: r.primary_reason_code, all_reason_codes: r.all_reason_codes };
    } catch (e) {
      out = { error: 'evaluate-threw', message: String(e && e.message) };
    }
    return { global_index: entry.global_index, lane_A: out };
  });

  const finalOut = {
    role_note: 'Lane A (node, ninfty-searcher-v2.mjs evaluateDecisionLane) batch results for the 744-candidate P5 sweep.',
    entry_point: 'search/ninfty-searcher-v2.mjs :: evaluateDecisionLane (same function search/certs/ep-lanea-eval-candidate.mjs calls)',
    entry_point_sha256: searcherDigest,
    input_candidates_file: 'search/certs/ep_sweep744/candidates_744.json',
    input_candidates_sha256: candDigest,
    total: results.length,
    results,
  };
  writeFileSync(join(HERE, 'lanea_results_744.json'), JSON.stringify(finalOut, null, 2) + '\n');
  process.stdout.write(JSON.stringify({ total: results.length, entry_point_sha256: searcherDigest, input_candidates_sha256: candDigest }, null, 2) + '\n');
}

main();
