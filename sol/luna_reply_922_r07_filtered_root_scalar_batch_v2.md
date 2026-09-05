# Luna reply 922 -- filtered actual root-scalar batch v2

## Delivery

Implemented the v541 repair in the two new v2 programs; both v1 programs are
retained unchanged.

| file | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_actual_grade2_root_scalar_batch_v2.py` | 118315 | 2106 | `3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856` |
| `search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py` | 119619 | 1968 | `e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6` |

The schema prefix is
`d972.r07.actual-grade2.root-scalar-batch.v2`; launch, Task554-parent and
separator-parent suffixes remain versioned `.v1` envelopes under that prefix.

## Implemented repair

- The affine--Fox context is constructed once on the actual path.  Each of
  the 44 seed direct values is paired with the ordinary character slice of
  the full **raw** degree-two seed evaluation.  Production never calls the
  old projected direct-seed routine or checks its registered row hashes.
- Formula v541 (4.1) is evaluated directly over six tags, both Fox
  components, four source characters, four parities, the coupled monomials
  and 504 PSL coordinates.  It produces four 96,776-trit lower adjoints;
  their eight auxiliary entries are zero.  Each pure-top restriction must
  equal the accepted Task712 homogeneous adjoint.
- The eight old lower/grade blobs and four new grade blobs are selected only
  after authenticating their fixed Task554 bodies.  Descriptor equality,
  shape, exact byte count, SHA-256, base-3 byte range and zero padding are
  checked while a fixed 81-by-81 packed-dot table streams them.  The exact
  total is 67,011,332 bytes; no dense 8,059-by-96,776 matrix or DAG replay is
  constructed.
- Lower contractions are added to the four homogeneous child arrays before
  the unchanged Task554 relation subtraction.  Receipts keep separate hashes
  for homogeneous values, lower contractions and their complete direct sums.
- The active character saves `seed-scalars-a0.bin` (44 corrected uint8
  trits) and `actor-lower-a0-t0.bin` through `t3.bin` (8,059 uint8 trits
  each).  Raw seed rows/values, lower covectors, all 12 blob reads, saved
  arrays and complete direct arrays are transitively sealed into the
  character and result objects.
- Both `Violation` and `ScalarEOF` bind all five independently recomputed P1
  value-vector hashes plus the filtered-direct receipt.  Thus an early
  violation also binds the root/homogeneous values, lower values and repaired
  direct arrays.
- The fixed total family is labelled
  `global_relation_declared_count=32280`.  A violation's `origin_id` and
  prefix digest state the actually checked prefix; `ScalarEOF` records
  `origins=next_origin=32280`.  The later 504-row orbit is only a declared
  bound and explicitly records zero executed rows.

The actual seed-2 gate fixes
`SeedRed(2)=((2,2),(505,2),(1008,2),(1511,2))` and requires the corrected
scalar to be zero.  A later nonzero scalar remains only a materializer input;
no physical insertion, Grade2 decision or A0 claim is made here.

## Focused gates

The v2 selftests cover:

1. the pinned seed-2 raw/projected difference and a genuine synthetic
   reconstruction whose copied `d0/d1/aux` components cancel in the complete
   defect; the correct raw-minus-reconstruction pairing agrees with the
   projected lower-zero defect while the one-sided projected-seed expression
   fails;
2. lower-only and mixed direct full-actor equality with a known nonzero
   lower-to-top contribution, plus the pure-top Task712 equality;
3. tiny streamed old/new packed rows against dense dot products, including a
   forced nonzero cross-character grade companion;
4. the retained sparse/vectorized P1, exact-envelope, blockwise-fold,
   violation/EOF and output-reconstruction controls; and
5. an optional `--actual-canary-launch` which reads only the selected actual
   seed-2 P1 slices (not the full 8,059-row production scan), checks raw pair
   0, projected pair 1, difference pair 2 and corrected scalar 0, and checks
   the four Task712 pure-top actor adjoints.

No local Python test was started: an unknown pre-existing Python process
(PID 10104, start time 2026-09-05 00:56:16 JST) occupied the sole coordinated
slot and was neither interrupted nor overlapped.  Static producer checks
found balanced delimiters, no leading tabs/trailing whitespace/CRLF, exact
dimension identities `96776`, `32280` and `67011332`, both violation/EOF
five-vector bindings, and no production text reference to
`direct_seed_rows` or `SEED_REGISTERED_ROW_SHA`.  The bounded selftests and
the actual 32,280-origin run are therefore pending the serial Task923 GHA
workflow.

## Independence and boundary

The producer reuses the pinned legacy producer-v15 affine--Fox primitives
(`76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632`);
the checker reuses the separately pinned checker-v15 implementation
(`8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662`).
Their raw-seed, actor-adjoint, packed-stream and reconstruction code paths are
separate, but they intentionally share the legacy v15 seed-arithmetic design
and underlying marking data.  This is independent implementation
cross-checking, not a claim of independent mathematical provenance or Lean
verification.

Current boundary remains:

```text
CORRECTED ACTUAL ROOT SCAN:  PENDING SERIAL GHA
GRADE2 MEMBER/NONMEMBER:    NOT DECIDED
A0/COMMON/COFINAL/FAKE/IHARA: NOT DECLARED
verified=false
```
