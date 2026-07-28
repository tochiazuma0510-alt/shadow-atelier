// search/certs/ep-lanea-verify-cert.mjs
//
// EP receiving-side helper: run lane A's own runVerifierA() over an
// ARBITRARY certificate object supplied on stdin as JSON (used for the
// reverse-direction cross-check: lane B cert fixtures, converted to lane
// A's schema by search/ninfty-ep-runner.py, run through verifier A).
// Read-only w.r.t. lane A's source; does not import lane B (python).
//
// input: { certificate: <lane-A-shaped cert with embedded searcher_native/
//          checker_native>, native_a?: <root doc for json_pointer resolution
//          on the searcher side>, native_b?: <... checker side> }
// The searcherNativeBlob/checkerNativeBlob passed to runVerifierA are
// resolved from the certificate's own embedded searcher_native/checker_native
// _ref triples (P-3.3 is expected to fail in this reverse-direction use
// since those are STAND-IN values, not real digests -- this script does not
// paper over that).
//
// v5 (裁定142 symmetric-gap closure): resolveRef(ref, rootDoc) now takes a
// SECOND argument to resolve a `json_pointer`-style _ref against -- EP v4's
// run supplied none, so every json_pointer ref (lane B's chosen form, per
// interpretation v3 条項3's "json_pointer または object_id") came back
// 'json-pointer-unresolvable'. This EP helper (receiving-side tooling, not a
// lane file) is updated to pass payload.native_a/native_b through as the
// resolution root -- the natural root document for a pointer like
// "/ramification_divisor_on_C_ref" is exactly the fixture's own top-level
// native_a/native_b object (confirmed against search/fixtures/ninfty/
// cert_pos_01.json's json_pointer values).

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
    const rootA = payload.native_a; // resolution root for searcher-side json_pointer refs
    const rootB = payload.native_b; // resolution root for checker-side json_pointer refs
    // 裁定139 item 3: searcher_native/checker_native's *_ref fields are
    // {artifact_id, digest, json_pointer|object_id, inline?} triples (see
    // ninfty-verifier-a.mjs resolveRef), not the raw {components:[...]}
    // object directly. This EP helper is not a lane file (it is a thin
    // receiving-side CLI wrapper around runVerifierA, same status as
    // search/certs/gen_full_cert_base.mjs), so it resolves the ref before
    // handing the native blob to runVerifierA -- runVerifierA itself has no
    // way to know what "the blob this caller actually read" was except what
    // is passed in.
    function resolvedNativeBlob(nativeSide, rootDoc) {
      const ram = resolveRef(nativeSide.ramification_divisor_on_C_ref, rootDoc);
      const branch = resolveRef(nativeSide.branch_divisor_on_P1_ref, rootDoc);
      return {
        ramification_divisor_on_C_ref: ram.malformed ? undefined : ram.data,
        branch_divisor_on_P1_ref: branch.malformed ? undefined : branch.data,
        _resolution: { ram, branch }, // kept for EP diagnostics, not consumed by runVerifierA
      };
    }
    const searcherResolved = resolvedNativeBlob(cert.searcher_native, rootA);
    const checkerResolved = resolvedNativeBlob(cert.checker_native, rootB);
    const result = runVerifierA({ certificate: cert, searcherNativeBlob: searcherResolved, checkerNativeBlob: checkerResolved });
    result._ep_ref_resolution = {
      searcher: { ramification_malformed: searcherResolved._resolution.ram.malformed, branch_malformed: searcherResolved._resolution.branch.malformed },
      checker: { ramification_malformed: checkerResolved._resolution.ram.malformed, branch_malformed: checkerResolved._resolution.branch.malformed },
    };
    process.stdout.write(JSON.stringify(result));
  } catch (e) {
    process.stdout.write(JSON.stringify({ error: 'runVerifierA-threw', message: String(e && e.message), stack: String(e && e.stack) }));
  }
});
