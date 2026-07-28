// search/certs/ep-lanea-eval-candidate.mjs
//
// EP receiving-side helper: run lane A's own evaluateDecisionLane() over a
// SINGLE candidate supplied on stdin as JSON, print the native result as JSON.
// Used by search/ninfty-ep-runner.py to cross-feed lane B's checker fixtures
// (converted candidate schema) into lane A's decision-lane native, for the
// cross-fixture native-verdict comparison (task item 2). Read-only w.r.t.
// lane A's source; does not import anything from lane B (python).

import { evaluateDecisionLane } from '../ninfty-searcher-v2.mjs';

let raw = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => { raw += chunk; });
process.stdin.on('end', () => {
  let candidate;
  try {
    candidate = JSON.parse(raw);
  } catch (e) {
    process.stdout.write(JSON.stringify({ error: 'json-parse-failed', message: String(e) }));
    process.exit(0);
  }
  try {
    const result = evaluateDecisionLane(candidate);
    process.stdout.write(JSON.stringify({
      verdict: result.verdict,
      primary_reason_code: result.primary_reason_code,
      all_reason_codes: result.all_reason_codes,
    }));
  } catch (e) {
    process.stdout.write(JSON.stringify({ error: 'evaluate-threw', message: String(e && e.message) }));
  }
});
