// search/certs/ep-lanea-verify-cert.mjs
//
// EP receiving-side helper: run lane A's own runVerifierA() over an
// ARBITRARY certificate object supplied on stdin as JSON (used for the
// reverse-direction cross-check: lane B cert fixtures, converted to lane
// A's schema by search/ninfty-ep-runner.py, run through verifier A).
// Read-only w.r.t. lane A's source; does not import lane B (python).
//
// input: { certificate: <lane-A-shaped cert with embedded searcher_native/
//          checker_native> }
// The searcherNativeBlob/checkerNativeBlob passed to runVerifierA are taken
// directly from the certificate's own embedded searcher_native/checker_native
// (P-3.3 is expected to fail in this reverse-direction use since those are
// STAND-IN values, not real digests -- this script does not paper over that).

import { runVerifierA } from '../ninfty-verifier-a.mjs';

let raw = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => { raw += chunk; });
process.stdin.on('end', () => {
  let payload;
  try {
    payload = JSON.parse(raw);
  } catch (e) {
    process.stdout.write(JSON.stringify({ error: 'json-parse-failed', message: String(e) }));
    process.exit(0);
  }
  try {
    const cert = payload.certificate;
    const searcherNativeBlob = {
      ramification_divisor_on_C_ref: cert.searcher_native.ramification_divisor_on_C_ref,
      branch_divisor_on_P1_ref: cert.searcher_native.branch_divisor_on_P1_ref,
    };
    const checkerNativeBlob = {
      ramification_divisor_on_C_ref: cert.checker_native.ramification_divisor_on_C_ref,
      branch_divisor_on_P1_ref: cert.checker_native.branch_divisor_on_P1_ref,
    };
    const result = runVerifierA({ certificate: cert, searcherNativeBlob, checkerNativeBlob });
    process.stdout.write(JSON.stringify(result));
  } catch (e) {
    process.stdout.write(JSON.stringify({ error: 'runVerifierA-threw', message: String(e && e.message), stack: String(e && e.stack) }));
  }
});
