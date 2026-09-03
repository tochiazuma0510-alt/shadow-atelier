# Task 602 - audit of independent grade-one full-routing replay v1

## Verdict

`PASS_AFTER_REPAIR`

The launched checker has the correct independent routing mathematics.  It
authenticates the frozen source and candidate byte images, reconstructs the
group/affine/Fourier routing without importing a producer or validator, routes
all old rows before every block row, and compares only after independently
building the final grade owner.  Its GF(3) reduction, coefficient-2
normalization, target reduction, and coefficient reconstruction arithmetic are
correct.  However, its terminal adapter compares the NumPy remainder directly
with candidate `bytes`, so even equal zero bytes fail the gate.

Five narrow package defects remain: that terminal type mismatch; the advertised
`old_lower` selftest does not exercise old-lower companion routing at all;
block exhaustion is not explicitly required when block bodies are interpreted;
the hottest lead search materializes every nonzero index although only the
first is used; and no final resource check prevents a PASS written after the
nominal 2,400-second internal cap.  These require no mathematical or workflow
redesign.

I did not query, wait for, or alter the live replay.  Root subsequently supplied
its terminal status: run `33709557095` rebuilt all 8,059 rows, obtained ranks
1,661/5,044, and passed the exact basis/leads comparison before failing
`target_reduction`.  That is precisely the deterministic adapter failure above,
not a routing disagreement.  The failed run has no PASS verdict and cannot by
itself promote v220.  A later successful receipt from the one-line repaired
adapter can be used under the authentication conditions in section 8.

## 1. Frozen audit identity

The commissioned checker hash matches the launched pin exactly.

| file read in full | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_602_audit_r07_grade1_independent_full_routing_v1.md` | 2,199 | 42 | `332b5111f882c4aa5d58d039f5b528b7eefdbd93d1aca4e20899e2b62f57cb49` |
| `sol/luna_task_599_r07_grade1_independent_full_routing_v1.md` | 5,233 | 105 | `bc8b89c76b4639065b3a92dd9430b942400239a77567a144ce96b53d9582b07f` |
| `crosscheck/check_d972_r07_a0_first_rung_grade1_full_routing_v1.py` | 26,358 | 380 | `8e159cc262fd35d61018da4b30db45017534546f7bbe89ebd001b3dbff6286d8` |
| `.github/workflows/d972-r07-a0-grade1-independent-routing-v1.yml` | 5,508 | 119 | `45229fc41839d4a9246cbdfea08db0f4f744f46141c0c98a846f335c4f4c7b52` |
| `sol/luna_reply_599_r07_grade1_independent_full_routing_v1.md` | 1,587 | 34 | `5823311daa5f5cbfd9ea6dfa186a850cef784058f8dcdcbd44984f8b9da45d15` |
| `sol/sol_reply_597_audit_r07_grade1_decision_probe_v2.md` | 14,635 | 286 | `53900086c43549a06ff073716cfbe1086d16386f2297c22f8a1065921791afaf` |
| `crosscheck/check_d972_r07_a0_first_rung_grade1_decision_result_v1.mjs` | 13,729 | 270 | `020daede47b0bcd894723fc4562154b79426a729098ce83b7bdc7a41a26183ea` |

This audit is bound to launched commit
`5440d66d44f9ca937bc7f8a4958a54ad9f5eba4f`.  The two raw mathematical
definition inputs also match the checker's pins:

```text
scratchpad/a0_paper_words_v1.json
  90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893
scratchpad/fuda1_a0_rmax_data.g
  625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba
```

The locally present v2 and frozen-v3 producer hashes equal the body pins, but
neither file is imported by the new checker:

```text
v2  5a445cf9a263c1968c004f04227d9f5bd5349e433f4dfd8776af80b1d53d9748
v3  bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff
```

## 2. Source and candidate authentication

The exact-input chain is adequate for this frozen replay.

- The workflow downloads source run `33677346616`, attempt `1`, using the
  attempt-qualified prepare name and four-block pattern.  It downloads the
  candidate from run `33707397894`, attempt `1`, under its exact
  attempt-qualified artifact name.
- Source HEADs must be canonical and have exactly schema, stem, body digest,
  and expected parent.  Each body filename and byte content is bound by its
  SHA-256; each consumed residual, lower-basis, lifted-grade, and block-basis
  blob has exact receipt shape, filename suffix, byte length, and digest.
- The prepare body is pinned to
  `1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865`.
  The four block body digests are read from the exact candidate body and then
  matched, in order, to the four independently authenticated source bodies.
- The candidate directory must have exactly four files.  Its canonical HEAD is
  pinned to `07de7a817e8c5ae2e7346402a290c32631d05b0cc621d03702faa6cb43a948c0`
  and its canonical body to
  `62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d`.
  Basis and remainder receipts and blobs are then checked for exact shape,
  size, name, and digest.

The workflow's comparison of `CANDIDATE_COMMIT` with the same literal at line
56 is not, by itself, a query of the candidate run's head SHA.  For this one
launch the missing link is already supplied by the immutable Task597 receipt:
run `33707397894` / attempt `1` / job `100499387350` is bound to commit
`93f746ad1b649796e1bc28e00ff34993498929ee` and to the same four exact content
hashes.  Promotion must retain that receipt and separately bind the live run's
head SHA to `5440d66d...`; the tautological environment comparison should not
be cited as that evidence.

## 3. Genuine implementation independence

The checker imports only the standard library and NumPy.  It does not import
Task595 v2, frozen v3, either validator, or the JavaScript result checker.  In
particular:

- it parses the pinned permutation marking and word data itself, enumerates
  the 504 PSL elements, and implements its own permutation, free-word,
  character, affine semidirect-product, and transport operations;
- it derives the six affine shifts and four Fourier-label transports locally;
- `aggregate_pair` and `aggregate_pure` construct physical lower/grade rows
  from these data without consulting candidate rows or leads;
- `IndependentOwner` has its own insertion-ordered row list and direct
  lead-to-pivot map.  It neither calls nor imports `PackedEchelon`; and
- the candidate basis, leads, and coefficient list are used only in terminal
  equality gates, never to steer routing or elimination.

Task599 expressly allowed the already independent v3 checker as a mathematical
reference.  In a bounded read-only comparison, the new formulas agreed with
that reference on four independently generated sparse old-row aggregations
and four sparse pure-block aggregations; PSL order was 504.  This is not the
real campaign and does not replace its terminal byte comparison.

## 4. Exact lower-first route

`load_source` fixes old characters in order `0,1,2,3` and checks ranks
`[505,503,503,503]`.  Lines 332--349 traverse every packed pivot of each old
basis before the block loop can begin.  For each row the checker:

1. independently aggregates its 6,056-trit lower row and 72,576-trit lifted
   grade row;
2. reduces the 8,068-trit physical lower part exactly once;
3. applies the same ordered `(pivot,coefficient)` reductions to the dense grade
   companion;
4. normalizes that companion with a newly accepted lower pivot, or offers it
   to the grade owner only when the lower remainder is zero.

The boundary gate requires exactly 2,014 logical rows and lower rank 1,661.
Only then do lines 350--355 traverse block bases `0,1,2,3` with ranks
`[1509,1512,1512,1512]`, totaling 6,045.  The terminal gates give

```text
logical cursor = 2,014 + 6,045 = 8,059
lower offers/rank = 2,014 / 1,661
grade offers = (2,014 - 1,661) + 6,045 = 6,398
grade rank = 5,044.
```

There is no candidate-derived early stop, row reorder, or second lower
reduction.

## 5. GF(3), canonical basis, and MEMBER reconstruction

`PACKED_AXPY[c,a,b]` is `a-cb` digitwise over four base-3 trits.
`PACKED_SCALE2` and `PACKED_FIRST` have the corresponding exact meanings.
The owner carries a monotone packed-byte cursor, cancels by the actual lead
coefficient, normalizes a new coefficient-2 pivot by multiplication by two,
and preserves insertion pivot IDs.

I independently exhausted all `3*81*81` packed AXPY entries and all 81 scale
entries against direct digit arithmetic.  I also compared 500 deterministic
width-12 insertions with a separately written dense reducer; reductions,
acceptance, leads, scales, normalized rows, and final rank 12 all agreed.

The full route requires the newly constructed matrix bytes to equal both the
candidate bytes and
`b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d`.
Its insertion leads must equal the 5,044-entry list in the exact candidate
body.  Source block rows are checked for distinct in-range actual leads and
coefficient-one normalization; the newly routed owner is normalized by
construction.

The authenticated residual is then reduced by that independent owner.  A PASS
requires all of the following simultaneously:

- packed remainder identically zero and byte-equal to the candidate remainder;
- zero-blob SHA-256
  `564cbfafc869a8c6eb761a392caa5e792b546bf577af7fe808177b2fdf13cbb0`;
- exact equality with the candidate's 3,317 ordered coefficient pairs; and
- reconstruction of the packed residual by adding precisely those normalized
  insertion rows, followed by agreement with both registered residual hashes.

Line 361 uses `PACKED_AXPY[3-c]` starting from zero, which is addition by `c`;
the reconstruction sign is correct.

The failure at line 359 is outside this algebra.  `candidate_files` returns
the candidate remainder as a Python `bytes` object, whereas `grade.reduce`
returns a one-dimensional NumPy `uint8` array.  The expression

```python
np.array_equal(remainder, candidate_remainder)
```

does not compare the byte sequences as intended: NumPy coerces the `bytes`
operand as a scalar byte string, so the shapes/dtypes disagree.  For the exact
6,048 zero bytes the comparison is false.  This explains why run
`33709557095` passed the much stronger routed basis/leads gate and then rejected
at `target_reduction`.  Root's separate local reduction of those exact emitted
basis/residual bytes returned zero and the exact 3,317 body coefficients,
which is consistent with the audited arithmetic, but it does not turn the
failed workflow run into a PASS receipt.

## 6. Exact load-bearing repairs

Freeze this launched v1.  A later version needs only these changes.

1. **Repair the terminal byte adapter.**  Convert `candidate_remainder` once
   with `np.frombuffer(candidate_remainder,dtype=np.uint8)` and require the
   expected one-dimensional 6,048-byte shape before `np.array_equal`, or compare
   `remainder.tobytes()` directly with `candidate_remainder`.  Retain the
   independent zero test and coefficient-list equality in the same gate.  No
   reduction or reconstruction formula changes.
2. **Make `old_lower` selftest truthful.**  `selftest` lines 251--258 tests a
   coefficient-2 pivot normalization and an ordinary packed dependence, then
   returns `"old_lower":"PASS"` without creating a grade companion or running
   the lower-first branch.  Add one tiny paired fixture which (a) accepts a
   lower pivot with leading coefficient two and doubles its companion and (b)
   reduces a later lower row with coefficient two to zero and checks the exact
   companion offered to the grade owner.  Do not merely retain the marker.
3. **Require the advertised exhausted block inputs.**  `load_source` line 314
   checks phase, character, parent, and rank but not
   `queue_exhausted is True`.  Add that single semantic gate for every one of
   the four authenticated block bodies.  Do not re-run or reconstruct their
   source closures.
4. **Do not materialize every nonzero index in the hottest loop.**  Reduction
   line 213 calls `np.flatnonzero(work[cursor:])` for every pivot cancellation
   and consumes only element zero.  At production width this repeatedly
   allocates an index array for all nonzero packed bytes.  Replace only this
   call with a vectorized boolean `any`/first-`argmax` search (or equivalent
   first-index primitive).  Keep packed AXPY, cursor, row order, and all
   arithmetic unchanged.  The once-per-row validation searches need no
   redesign.
5. **Enforce the internal cap before PASS.**  `guard` is called only when the
   logical cursor is a multiple of 256; the last call is at 7,936.  Rows
   7,937--8,059, target reduction, matrix comparison, and verdict writing have
   no later internal time/RSS gate.  Call `guard(started)` after route
   exhaustion and again immediately before writing the verdict.  The existing
   45-minute outer and 60-minute job caps remain unchanged.

These are evidence/performance/resource repairs.  They do not alter any source
digest, aggregation formula, owner algebra, candidate comparison, or decision
predicate.

## 7. Workflow and artifact policy

Apart from the terminal internal-cap gap above, the workflow implements the
commissioned finite run:

- event-SHA checkout, Python 3.13, NumPy 2.5.1, read-only permissions, and
  commit-pinned checkout/setup/download/upload actions;
- checker and Luna-reply hashes checked before any large artifact download;
- exact source/candidate run IDs and attempt-qualified artifact names;
- 7-GiB internal RSS, 8-GiB virtual memory, 2,400-second internal time,
  45-minute outer timeout, and 60-minute job timeout;
- `set -euo pipefail`, a required nonempty PASS verdict, and no success upload
  after a failing replay; and
- only the small verdict uploaded on success, with logs under `always()`.

The hot path retains packed source matrices and expands only the current row
for physical aggregation.  Live bases occupy about 30.5 MB for grade rows and
3.4 MB for lower rows; the 1,661 dense grade companions occupy about 40.2 MB.
There is no offer-sized ordering structure, dense closure, ancestry, dual,
per-offer basis copy, or unbounded queue.  The terminal 30.5-MB matrix copy and
the current-row aggregation scratch are bounded and required by the exact byte
comparison.  I reject broader optimization requests.

## 8. Consequence of a successful authenticated receipt

**Yes, after the terminal adapter repair and a successful rerun.**  A successful
authenticated receipt justifies promoting exactly the first v220 rung from
`0/6` to `1/6 cross-checked`, provided root binds all of the following before
promotion:

1. the live run's immutable head SHA is
   `5440d66d44f9ca937bc7f8a4958a54ad9f5eba4f` and the executed checker SHA-256
   is `8e159cc262fd35d61018da4b30db45017534546f7bbe89ebd001b3dbff6286d8`;
2. source `33677346616/1` and candidate `33707397894/1` artifact identities,
   plus the Task597 binding of that candidate run to commit
   `93f746ad1b649796e1bc28e00ff34993498929ee`, are retained;
3. the canonical verdict has marker
   `R07_GRADE1_FULL_ROUTING_REPLAY_V1_PASS`, `cursor=8059`, counts
   `2014/1661` and `6398/5044`, the expected prepare/block/basis/residual/
   remainder/lead/coefficient digests, coefficient count 3,317, and
   `verified:false`, `cross_checked:false`;
4. the workflow job and replay step succeeded, the verdict artifact and logs
   authenticate, no rejection/resource terminal occurred, and reported
   elapsed time is at most 2,400 seconds (the explicit receipt-side check is
   necessary because repair 5 is not in the launched v1).

Run `33709557095` does **not** meet item 4: it failed before verdict emission.
Its independently reconstructed 8,059-row basis/leads equality is strong
candidate evidence for the routing half and sharply localizes the failure, but
neither that partial log nor root's separate terminal reduction may be relabeled
as this checker's successful full-routing receipt.  Keep v220 at `0/6` until
the repaired rerun passes and its immutable receipt is inspected.

The false `cross_checked` field is intentional: it prevents the candidate
checker from promoting itself.  Root's inspection supplies the promotion.
The promoted statement is only:

```text
the registered grade-one residual is MEMBER of the registered 8,059-row
lower-first routed span - 1/6 cross-checked.
```

It is not Lean-verified.  It proves no A0, COMMON/cofinality, compatible lift,
fake, or Ihara conclusion.  `verified=false`.

```text
TASK602_STATIC: PASS_AFTER_REPAIR
RUN_33709557095: ROUTING_MATCH_THEN_TERMINAL_ADAPTER_REJECTED
CURRENT_V220_RUNG: KEEP_0_OF_6
REPAIRED_SUCCESSFUL_RECEIPT: PROMOTE_V220_FIRST_RUNG_TO_1_OF_6_CROSS_CHECKED
LEAN_VERIFIED: NO
COFINAL_FAKE_IHARA: NOT_DECLARED
```
