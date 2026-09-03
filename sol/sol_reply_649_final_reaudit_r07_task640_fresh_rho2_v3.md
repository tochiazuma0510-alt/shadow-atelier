# Sol(max) Task649: final bounded release re-audit of Task640 v3

## Verdict

`FAIL`

`SAFE_TO_DISPATCH_GHA=no`

F646-A and F646-B are closed, the `unpack` authority collision is repaired,
and the accepted R1/R3/R4/R5/R7 surface has not regressed.  F646-C is not yet
closed: three mutations explicitly named by Task648/649 can still be made to
production gates while both bundled selftests remain green.  No production
run, GHA dispatch, implementation edit, or git operation was performed.

`verified=false`

## Frozen inputs

No `INPUT_MISMATCH` occurred.

| file | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 27,474 | 304 | `060202458e8643acb1ed42d2ad94b9f192406c57b803dc7f3b07897c39115ef7` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 90,762 | 1,548 | `ff3ed7d2287baa807a3577c0f72ddc7f33bce00322d8a581a1d263c393eda774` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml` | 9,974 | 161 | `7f53ca31cac0d2c828a9e1ac57e87f324bd0787c98cbfffb7e9ce9875808858a` |
| `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md` | 2,972 | 58 | `1a2c3584f93e93152de1874cc7ca16d8d9820ed7ee4dedf4b75eab1c35df3243` |

The complete Task649 mail is 3,314 bytes / 58 lines / SHA-256
`6a61b073d1987940270a2b6ff72f66e86466161e5bb8725aebd06cb340f8e07d`.
I read the complete Task646 reply (10,783 bytes / 209 lines / SHA-256
`fe1a6fbec8a3b4518b2e12cae72f3dd46e29d910ed3ad5b5407264bda7183c41`),
the complete Task648 instruction (4,546 bytes / 92 lines / SHA-256
`dbaa3af98fcc3f884ed89f6a10869ab5bfb9d4816fb29b264c45de20385d4d54`),
and the updated Task648 reply in the frozen quartet.

## F646-A -- PASS

Producer constants at lines 19 and 22--23 are strings, so producer line 276
emits strings for `task601_run`, `task601_attempt`, `source_run`, and
`candidate_run`.  Checker line 452 now uses exactly the same four JSON string
types and values.  Production line 453 calls `exact_parent_gate`, whose line
366 comparison is strict dictionary equality with no coercion.

The same gate is exercised by selftest line 412.  It accepts the exact object,
rejects a string-to-integer mutation, and separately rejects an artifact
envelope/digest mutation.  The previous honest-producer contradiction is
gone.

## F646-B -- PASS

Checker line 19 fixes the seven exact key-to-filename pairs.  Production
lines 455--462 require the exact key set, receipt schema, and canonical
filename before reading each blob.  After independently reconstructing all
seven byte strings, production line 523 calls `exact_receipt_gate`; lines
399--401 compare the complete receipt dictionary with fixed filename,
recomputed length, and recomputed SHA-256.

Selftest lines 438--440 call that same production gate and reject filename,
size, and digest mutations.  Strict whole-dictionary equality also rejects a
filename alias, duplicate canonical name, missing key, or extra key.  A
bounded audit probe confirmed a duplicate-name alias is rejected with
`consumer_receipt_exact`.

## F646-C -- FAIL

Most of the repaired mutation path is now genuine.  The following helpers are
called by both production and selftest: manifest/claims (363--368,
413--417, 449--450), parent (365--366, 412, 453), roots (369--370,
418--419, 322), raw seeds (371--374, 420--421, 468), typed endpoints and
occurrence roster (375--380, 422--425, 472--475), signed relations
(381--383, 426--427, 1363/1404), signature extension/grouping
(384--394, 428--435, 492--499), direct/occurrence and block-product gates
(395--398, 436, 1345/1484), receipts (399--401, 438--440, 523), dense bytes
(402--405, 441--443, 510), and the live leaf parser (250--267, 531--535,
321).  Three mandatory cases nevertheless remain unexercised.

### F649-C1 -- occurrence-prefix mutation survives selftest

The actual suffix-prefix and signed occurrence-prefix construction remains
inline at checker lines 1337--1350.  No selftest invokes this code or a factored
equivalent.  The line-436 toy `block_product_gate` call checks only that an
already supplied value is identity, and the toy `direct_occurrence_gate` call
checks only two supplied dictionaries.  Neither constructs `p_j` or
`U_j`.

Concrete surviving mutation: change lines 1347--1350 so a positive occurrence
uses `prefix` instead of `prefix * base_factor`, or reverse the multiplication
there.  All 40 reported checker mutations and all producer tests still pass,
because `IndependentAllSeven.__init__` is never entered by `--selftest`.
This is exactly the mandatory prefix/order mutation, not additional
hardening.

Smallest repair: factor the two-line `U_j` construction into one helper used
at lines 1347--1350 and call it in selftest with a tiny noncommutative
multiplication callback.  Require the positive and negative sign cases and
reject the reversed/prefix-only result.  No real quotient is needed.

### F649-C2 -- packing-roundtrip mutation survives selftest

Production `dense_result_gate` reaches the trit roundtrip only at checker
line 405.  Every dense mutation at selftest lines 442--443 changes a blob
while leaving the independently supplied `target/lower/top/packed` values
unchanged, so it is rejected at lines 403--404 before line 405.  The successful
all-zero baseline at line 441 cannot distinguish a real roundtrip comparison
from a deleted one.

Concrete surviving mutation: delete line 405, or make its equality
unconditional.  The full `mutation_count=40` remains green.  This is the
explicit Task649 `roundtrip` case.

Smallest repair: add one tiny call in which the receipt blobs agree with the
supplied `top` and `packed`, but decoding that packed row differs from `top`;
require line 405 to reject it.  For example, use a top row with one trit 1 and
the packed all-zero row.  A bounded audit probe of the current live gate
already rejects this exact case with `rho2_packing`.

### F649-C3 -- ancestry-binding mutation survives selftest

The live parser correctly checks `binding.hex() != ancestry_digest` at checker
line 253 (and producer line 104).  But checker selftest lines 531--535 mutate
only truncation, trailing EOF, and the magic byte.  Producer lines 285--292 add
a record-payload mutation, but likewise never alter the ancestry binding.

Concrete surviving mutation: remove only the binding comparison from checker
line 253 or producer line 104.  All present leaf mutations still fail for
their independent reasons and both selftests remain green.  This is the
explicit live leaf/header ancestry-binding case retained by Task648.

Smallest repair: add one parser call using an otherwise valid tiny leaf stream
with a different expected ancestry digest (and do so on both executables, as
both own the live parser).  A bounded audit probe confirmed the current
checker gate rejects this case with `leaf_header`.

These three repairs are finite callbacks/byte fixtures.  They require no
production data, graph, ancestry DOM, dense production row, or redesign.

## `unpack` authority -- PASS

Dense trit decoding has the sole `unpack` definition at checker lines
718--722; `matrix` calls it at line 734 and `dense_result_gate` calls
`module.unpack` at line 405.  Endpoint element decoding is separately named
`unpack_element` at lines 1286--1288 and is called only at lines 491, 1299,
and 1417.  No endpoint call resolves to the trit decoder and no dense call
resolves to the endpoint decoder.  The bounded successful packing fixture
also reaches the trit implementation.

## Accepted-gate regression -- PASS

- **R1:** workflow lines 112--118 still fetch the exact Task595 v2 artifact.
- **R3:** producer lines 221--222 and checker lines 467--469 derive reached
  seeds from raw `prior + leaves` before exact-key cancellation; direct
  all-seven canaries remain before grouping.
- **R4:** checker lines 499--504 dense-replay only its independently rebuilt
  nonzero buckets; the exact-key canary remains at lines 496--498.
- **R5:** no shared semantic `exec`/load/import was introduced.  Local E3/E4
  construction and one actual local direct-versus-occurrence smoke passed
  with 11 contexts and equal sparse support 1,383.
- **R7:** parent receipts remain stream-hashed at producer lines 161--169 and
  checker lines 307--316; only roots/leaves are retained.  Record,
  path-length, path, trie, and state caps remain attached to live counters.
  No ancestry DOM load was introduced.
- All manifest later claims remain exactly false/null, and checker line 450
  plus lines 513--522 retain their exact claim/schema gates.
- Workflow lines 39--42 remain inert under `false &&`.

## Bounded serial checks

- External-cache `py_compile` of both executables: `PASS`.
- Producer `--selftest`: exit 0, `leaf_live_mutations=4`.
- Checker `--selftest`: exit 0, `mutation_count=40`.
- PyYAML safe parse: `PASS`.
- Forbidden checker shared-exec/import scan: `PASS`.
- Immutable action scan: `PASS`; all seven `uses:` entries have 40-hex pins.
- Workflow producer/checker/reply pins match the frozen files: `PASS`.
- Bounded local q3/E3/E4 plus one direct/occurrence smoke: `PASS`.

The green selftests do not close F646-C because the three counterexamples
above do not reach their corresponding production branches.

## Claim boundary

This audit establishes no rho2 value, grade2 MEMBER/NONMEMBER result, A0,
order 54,432/full-Q0, COMMON word, cofinal lift, FAKE, IHARA, cross-check, or
Lean verification.  A future PASS would authorize only one fresh-rho2 GHA
consumer feeding v474.  The frozen quartet is not authorized for dispatch.
