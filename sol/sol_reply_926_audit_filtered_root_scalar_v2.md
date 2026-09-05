# Task926 -- bounded release audit of filtered root-scalar batch v2

## Verdict

`VERDICT=PASS_STATIC_RELEASE`

`SAFE_TO_PUSH_TRIGGER_GHA=yes`

This authorizes the root broker to commit/push the frozen files and trigger the
serial GHA gate.  It is **not** a Python run, an actual scalar result, a
Grade2 decision, or verification.  I ran no local Python/GAP and made no
git/network/dispatch operation.

I independently reproduced the final byte counts and SHA-256 values with
read-only filesystem hashing:

| frozen file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_actual_grade2_root_scalar_batch_v2.py` | 118315 | `3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856` |
| `search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py` | 119619 | `e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6` |
| `.github/workflows/d972-r07-actual-grade2-root-scalar-batch-v2.yml` | 29421 | `326bc19f837a1c03a2613713747e0eed80d94ad466608a948209e52827abbe63` |

## F926-1 -- v541 arithmetic

PASS.

- `raw_seed_direct` evaluates each of the 44 full raw affine--Fox seeds and
  pairs `evaluated[2][character]` with the root covector.  The superseded
  one-sided full projector occurs only in negative-control/canary code, not
  in production.
- `actor_adjoint` is the literal transpose of v541 (4.1): all six tags, two
  Fox components, four parities, four source characters and coupled
  constant/degree-one to degree-two monomials are present.  Its factors are
  `chi_(tau_j(a))(e+eps_j)`, `chi_(tau_j(c))(e)`, and `E_e(k_j)`; indexing
  `q_rows[:,pmap]` samples `q[...,u_j*g]`, the required non-inverse
  translation.  The lower covector fills all four `d0/d1` character blocks,
  has zero auxiliary entries, and its degree-two restriction is required to
  equal the Task712 homogeneous adjoint byte-for-byte.
- The four lower contractions are added with a plus sign to the four plain
  homogeneous P1-cache value arrays **before** relation subtraction.  The
  retained relation fold subtracts the old and new coefficients with offsets
  `0,505,1008,1511,2014,3523,5035,6547`, then scans exactly the retained order
  `44 seeds`, followed by each `basis_i` and actor `(1,-1,2,-2)`.
- Character-zero seed 2 is required to be zero only after this complete
  relation fold.  The actual canary separately pins raw/projected/difference
  pairings `0/1/2`, the four selected P1 slices and
  `SeedRed(2)=((2,2),(505,2),(1008,2),(1511,2))`, giving corrected scalar zero.

I inspected the focused bodies, rather than relying on their labels.  The
producer seed test now uses a reconstruction with copied, nonzero
`d0/d1/aux`, so the complete defect really has zero lower part; it compares
the projected complete defect with raw-top minus reconstructed-top and makes
the one-sided projected-seed expression differ.  The producer actor tests
force a nonzero lower coordinate and check lower-only, mixed and pure-top
full actions.  The checker separately performs sixteen mixed full-action
comparisons, a forced nonzero lower term, pure-top/full-defect controls and
the one-sided-projector negative control.

## F926-2 -- Task554 joins, packing and boundedness

PASS.

The authenticated roster is exactly twelve blobs: for each of four old
owners, `6056 = 6048+8` trits plus the full four-character `72576 = 4*18144`
grade-one companion, and for each of four new blocks its owner `18144`-trit
grade-one slice.  The old/new ranks are respectively
`505,503,503,503` and `1509,1512,1512,1512`; descriptors, content-addressed
names, byte counts, hashes and body joins are checked, and the total is
`67011332` bytes.

Both lanes retain the plain top-cache values.  Their separately written
least-significant-trit-first `81 x 81` dot tables reject packed bytes above
80 and accumulate modulo 3.  Producer chunks are at most 256 rows under an
8 MiB target and checker chunks at most 193 rows under a 7 MiB target; the
widest per-slot lookup temporary is bounded (about 4.65 MiB in the producer).
The P1 cache is streamed once through a 256-row buffer (about 9.29 MiB), and
only the active character's five value arrays are populated.  No dense
`8059 x 96776` lower matrix, parent closure, canonical-lift rebuild or DAG
rebuild is introduced.

Concrete nonblocking costs, classified as optional optimization only:

- each large Task554 JSON body is read once for its digest and again for JSON
  decoding;
- authenticated relation expressions are walked during validation and again
  during the scalar fold, while the 349055442-byte P1 instruction file is
  hashed although this batch consumes only the cache;
- the same full 72576-trit old grade-one covector slices are copied/repacked
  once per old-owner blob.

These are finite retained/fail-closed passes, not release blockers, and do
not justify delaying the actual scan for a redesign.

## F926-3 -- checker and workflow join

PASS after the one narrow repair pass.

The checker imports no producer.  It independently implements the raw seed
slice, lower adjoint, packed dots, twelve-blob embedding, coefficient fold,
scalar prefix and exact output reconstruction.  It recomputes and compares
the corrected 44-byte seed payload and four 8059-byte lower-contraction
payloads, nested receipts, character records, terminal, result and manifest.
That reconstruction covers both an early `Violation` and `ScalarEOF`; an EOF
also reconstructs the normalized root state.  It intentionally retains the
checker-v15 arithmetic design and the same fixed marking data as the producer
lane, so this is implementation cross-checking, not independent mathematical
provenance or Lean verification.

During audit I found two real handoff blockers: the checker initially sealed
the old v1 relation-source recipe, and its parser initially lacked the
workflow's `--actual-canary-launch`.  Both are fixed in the frozen hash above.
Producer and checker now seal the same v2 recipe, including
`filtered-direct-blockwise-scalar-v2`, `V541_FORMULA_ID`,
`LOWER_BLOB_PIN_SHA256` and
`task554-v3-body-and-lower-blob-pins`; the optional canary argument is accepted
only with `--selftest`.

The count language is conservative: terminal/run scope says only
`global_relation_declared_count=32280` / `relation_origin_declared_count`.
On a violation, `origin_id` and the prefix digest bind the actually inspected
prefix (length `origin_id+1`); only EOF records `origins=next_origin=32280`.
No early stop is mislabeled as 32280 checked origins.

The workflow pins all three frozen files, retains the authenticated P1,
Task554, Task712 and separator parents (including Task554's deliberately
accepted failed parent run), stages the body-authenticated twelve-blob roster,
uses the corrected checker CLI, runs the two lanes serially, and publishes a
candidate only after both actual executions succeed.  Diagnostics remain
available on failure.

## F926-4 -- still-unexecuted release conditions

`SAFE_TO_PUSH_TRIGGER_GHA=yes` is conditional on one GHA execution satisfying
all of the following:

1. exact parent metadata/download/staging and the three frozen source pins
   above pass;
2. Python 3.13 `py_compile` passes for both v2 files;
3. the producer selftest **with actual-canary launch** passes the genuine
   complete-defect seed control, lower-only/mixed/pure-top actor controls,
   packed old/new controls, pinned actual seed-2 `0/1/2` comparison, corrected
   zero and four Task712 top matches;
4. the checker selftest **with its independent actual-canary launch** passes
   the corresponding v541, packed, relation-order, output-resealing and actual
   parent controls;
5. within its 40-minute cap, the producer authenticates the full P1/cache and
   twelve lower blobs, accumulates the full 32280-scalar family, then emits
   either the first ordered violation prefix or a genuine 32280-origin EOF;
6. within its separate 40-minute cap, the checker independently recomputes
   the same arithmetic and exactly matches every repaired payload and sealed
   output for that violation/EOF branch; and
7. the 90-minute job limit is respected and the final candidate artifact is
   emitted only because both actual steps succeeded.

Until those gates run, the exact boundary is:

```text
ACTUAL_CORRECTED_ROOT_SCAN=PENDING
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
```

`R07_FILTERED_ROOT_SCALAR_V2_STATIC_RELEASE_AUDIT_926_PASS`
