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

import { runVerifierA, resolveRef } from '../ninfty-verifier-a.mjs';

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
    // 裁定139 item 3: searcher_native/checker_native's *_ref fields are now
    // {artifact_id, digest, object_id, inline} triples (see
    // ninfty-verifier-a.mjs resolveRef), not the raw {components:[...]}
    // object directly. This EP helper is not a lane file (it is a thin
    // receiving-side CLI wrapper around runVerifierA, same status as
    // search/certs/gen_full_cert_base.mjs), so it is updated here to
    // resolve the ref's inline content before handing the native blob to
    // runVerifierA -- runVerifierA itself has no way to know what "the
    // blob this caller actually read" was except what's passed in.
    function resolvedNativeBlob(nativeSide) {
      const ram = resolveRef(nativeSide.ramification_divisor_on_C_ref);
      const branch = resolveRef(nativeSide.branch_divisor_on_P1_ref);
      return {
        ramification_divisor_on_C_ref: ram.malformed ? undefined : ram.data,
        branch_divisor_on_P1_ref: branch.malformed ? undefined : branch.data,
      };
    }
    const searcherNativeBlob = resolvedNativeBlob(cert.searcher_native);
    const checkerNativeBlob = resolvedNativeBlob(cert.checker_native);
    const result = runVerifierA({ certificate: cert, searcherNativeBlob, checkerNativeBlob });
    process.stdout.write(JSON.stringify(result));
  } catch (e) {
    process.stdout.write(JSON.stringify({ error: 'runVerifierA-threw', message: String(e && e.message), stack: String(e && e.stack) }));
  }
});
