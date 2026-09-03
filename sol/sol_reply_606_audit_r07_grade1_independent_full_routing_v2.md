# Task 606 - audit of grade-one independent full-routing v2

## Verdict

`PASS`

The launched v2 snapshot contains all five Task602 Section 6 repairs and no
change to the registered routing mathematics.  The byte adapter now compares
two one-dimensional `uint8[6048]` arrays; the old-lower companion test is real;
all four block states must advertise exhaustion; the hot reducer finds the
same first nonzero packed byte without constructing an array of every nonzero
index; and resource guards cover both post-route work and verdict emission.

The checker marker and workflow namespace are v2.  Source/candidate identities,
digests, row order, aggregation, GF(3) tables, pivot normalization, target
coefficients, reconstruction, and claim flags remain unchanged.  There is no
load-bearing repair.

I did not run the 8,059-row route and did not query or wait for GHA run
`33710955262`.  This is a static verdict for launched commit
`13529ad947b82062bfa12e83107cb19ef303de6b`; a successful run still needs its
immutable receipt inspected.

## 1. Inputs and launched identity

| file read in full | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_606_audit_r07_grade1_independent_full_routing_v2.md` | 1,676 | 30 | `c20e23d3799222ddc5d215a82db50484adc82f703832740b5fb80ac008cfe965` |
| `sol/sol_reply_602_audit_r07_grade1_independent_full_routing_v1.md` | 16,570 | 312 | `4c124a138f81a16917afb68ec04c2d85e302eddfab77a518c95dccdf8258930d` |
| `sol/luna_task_604_r07_grade1_independent_full_routing_v2.md` | 1,653 | 30 | `c31893f424528a709d9d2b033b74ff5b3447f36047ec1bedeb98d2720a58558f` |
| `crosscheck/check_d972_r07_a0_first_rung_grade1_full_routing_v1.py` | 26,358 | 380 | `8e159cc262fd35d61018da4b30db45017534546f7bbe89ebd001b3dbff6286d8` |
| `crosscheck/check_d972_r07_a0_first_rung_grade1_full_routing_v2.py` | 27,778 | 399 | `a0504ae6a2562aab3b9af5ba7ed672bcc87bbd1cfdf5cc9fd3489240e51008e3` |
| `.github/workflows/d972-r07-a0-grade1-independent-routing-v2.yml` | 5,511 | 119 | `ead3da7f3c214526e54fe021dfefd0e0f3adbd6981baae61a5a5fca8b765169a` |
| `sol/luna_reply_604_r07_grade1_independent_full_routing_v2.md` | 1,436 | 29 | `3e1961bda5bfc07bf59e3a424079fdad7e4e0f400f5b6696185c39ece8de6c03` |

The commissioned checker digest matches exactly.  The workflow pins that
checker digest and the exact Luna-reply digest above before downloading any
large artifact.

## 2. Exact v1-to-v2 delta

A linewise comparison of the complete v1 and v2 checkers finds only:

1. `R07_GRADE1_FULL_ROUTING_REPLAY_V1_PASS` becomes the required v2 marker;
2. the reducer's first-nonzero search is replaced by boolean `any` plus
   first-`argmax`;
3. the old-lower and remainder-adapter fixtures are added;
4. `queue_exhausted is True` is added to the block semantic gate;
5. one `guard(started)` is added after complete route-count acceptance;
6. authenticated candidate remainder bytes are decoded to a copied
   `uint8` array before terminal comparison; and
7. one `guard(started)` is added immediately before verdict writing.

There is no other checker delta.  In particular, constants and expected
digests, group/affine/Fourier functions, physical aggregation, source loading
apart from exhaustion, lower-first loops, old/block order, owner AXPY and
normalization, target reduction, coefficient comparison, reconstruction, and
verdict fields are byte-for-byte inherited from v1.

The workflow delta is likewise only the v2 workflow/trigger/checker/reply
names and hashes plus the `task604` temporary and artifact namespaces.  Its
source and candidate run identities, action pins, environment, resource
bounds, commands, success conditions, and upload policy are unchanged.

## 3. The five Task602 repairs

### 3.1 Terminal byte adapter and shape

`candidate_files` first authenticates the remainder receipt as one row of
width 24,192, requires exactly 6,048 bytes, checks its filename/digest, reads
exactly that many bytes, and rechecks both size and the registered SHA-256

`564cbfafc869a8c6eb761a392caa5e792b546bf577af7fe808177b2fdf13cbb0`.

V2 then executes

```python
candidate_remainder = np.frombuffer(
    candidate_remainder, dtype=np.uint8
).copy()
```

Default `frombuffer` shape is one-dimensional; the prior exact-length gate
therefore makes this canonically `uint8[6048]`.  `grade.reduce(target)` already
returns the same shape and dtype.  `np.array_equal` now compares packed bytes
as intended, rather than comparing an array with a scalar `bytes` object.
The independent `np.any(remainder)` zero test and the exact coefficient-list
comparison remain in the same fail-closed gate.

The later SHA calls remain sound after conversion: a copied contiguous NumPy
`uint8` array exports precisely the same byte buffer.  A bounded check gave
the registered zero digest above for both the array and `.tobytes()`.

### 3.2 Truthful lower-companion fixture

The new fixture inserts a lower row whose actual lead coefficient is two,
observes normalization scale two, and doubles its grade companion.  It then
reduces a second copy of that lower row, requires the exact reduction
`[[0,2]]`, applies coefficient `-2` to the stored normalized companion, and
requires both zero lower remainder and the exact zero grade companion offered
by the lower-first branch.  Thus `old_lower:"PASS"` now exercises the missing
paired path, including coefficient two, rather than merely reporting a label.

### 3.3 Exhausted blocks

Every sealed `block-0` through `block-3` body must now satisfy
`queue_exhausted is True` in addition to the existing phase, character,
parent-digest and registered-rank gates.  Python identity comparison also
rejects integer `1` and truthy substitutes.  No source closure is rerun or
silently enlarged.

### 3.4 First-index hot search

For the packed `uint8` tail, v1 used

```python
nz = np.flatnonzero(tail)
bi = cursor + int(nz[0])
```

V2 uses a nonempty `np.any(tail)` gate followed by
`np.argmax(tail != 0)`.  On a nonempty boolean mask, `argmax` is the first
true position, so the chosen packed byte, trit lead, pivot lookup, coefficient,
AXPY update and cursor are identical.  It avoids an `int64` index array
containing every nonzero position.

As a bounded independent check, 160 deterministic width-40 insertions and 160
subsequent reductions agreed exactly between v1 and v2 in acceptance records,
reduction lists, normalized rows, leads and final rank 40.

### 3.5 Final resource guards

The first new guard runs after all 8,059 rows and the exact
`8059/6398/5044` route gate, before matrix copying, basis/leads comparison and
target work.  The second runs after reconstruction and hash checks,
immediately before `out.write_bytes`.  Thus no v2 PASS artifact can be emitted
without a final check of the 2,400-second and 7-GiB internal limits.  The
45-minute process timeout, 8-GiB virtual-memory limit and 60-minute job limit
remain independent outer bounds.

## 4. Bounded tests and unchanged decision semantics

The official bounded selftest completed with exit zero:

```text
canonical_zero=PASS
coefficient_2=PASS
fixture=PASS
mutated_remainder_rejection=PASS
nonzero_remainder_rejection=PASS
old_lower=PASS
packed_echelon=PASS
```

The canonical-zero fixture constructs the exact `uint8[6048]` zero row; its
two mutations are unequal to that row.  In production, a nonzero independently
computed remainder is rejected by `np.any`, while a mutated candidate
remainder is rejected by exact equality (and earlier by its pinned digest).

The load-bearing MEMBER chain is unchanged:

- all 2,014 old rows are processed first, with the same lower reductions
  applied to their grade companions;
- only then are all 6,045 block rows processed in character order;
- terminal counts remain lower `2014/1661`, grade `6398/5044`, cursor `8059`;
- the independently routed matrix and 5,044 insertion leads must equal the
  authenticated candidate and basis digest
  `b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d`;
- reducing the authenticated residual must give an identically zero packed
  remainder, the exact candidate remainder, and the candidate's ordered 3,317
  coefficient pairs; and
- starting from zero, `PACKED_AXPY[(3-c)%3]` adds `c` times each normalized
  insertion row and must reconstruct the residual exactly.

The terminal adapter changes representation only.  It changes neither a
coefficient nor the MEMBER predicate.

## 5. Workflow and authentication

The v2 workflow has read-only `contents`/`actions` permissions, checks out the
exact event SHA, installs Python 3.13 and pinned NumPy 2.5.1, and authenticates
the v2 checker/reply before downloads.  It downloads:

- prepare and four block artifacts from source run/attempt `33677346616/1`
  under the same exact attempt-qualified names; and
- the Task595 candidate from `33707397894/1` under its exact
  attempt-qualified name.

It runs only on manual dispatch or the v2 fire marker on the registered
working branch.  `set -euo pipefail` propagates checker, timeout and `tee`
failures.  A nonempty verdict with
`R07_GRADE1_FULL_ROUTING_REPLAY_V2_PASS` is required before the success-only
verdict upload; logs upload under `always()`.

As in Task602, the workflow's comparison of `CANDIDATE_COMMIT` to the same
literal is not an API authentication of the old run's head SHA.  The retained
Task597 immutable receipt supplies the needed binding of candidate
`33707397894/1` to
`93f746ad1b649796e1bc28e00ff34993498929ee` and its exact content.  Root must
also bind run `33710955262` itself to launched head
`13529ad947b82062bfa12e83107cb19ef303de6b`.  This is receipt inspection, not a
new v2 repair.

## 6. Consequence of a successful authenticated v2 receipt

**Yes.**  If run `33710955262` finishes successfully and root authenticates
its immutable run/attempt/job, head SHA, logs and verdict artifact against
this exact snapshot, then a canonical v2 verdict with:

- marker `R07_GRADE1_FULL_ROUTING_REPLAY_V2_PASS`;
- cursor 8,059 and ranks/counts `2014/1661`, `6398/5044`;
- registered prepare, four-block, residual, basis, remainder, lead and
  coefficient digests;
- exactly 3,317 ordered coefficients and zero 6,048-byte remainder;
- elapsed time at most 2,400 seconds; and
- `cross_checked:false`, `verified:false`

permits promotion of exactly the first v220 rung from `0/6` to
`1/6 cross-checked`.  The false body flag prevents self-promotion; root's
authenticated comparison supplies the cross-check.

That statement is only that the registered grade-one residual is MEMBER of
the registered 8,059-row lower-first routed span.  It is not Lean-verified,
does not decide any of the other five grades, and implies no A0, COMMON,
cofinal/compatible lift, fake, or Ihara conclusion.

```text
TASK606_STATIC: PASS
LAUNCHED_COMMIT: 13529ad947b82062bfa12e83107cb19ef303de6b
LIVE_RUN_33710955262: NOT_QUERIED
SUCCESSFUL_AUTHENTICATED_V2_RECEIPT: PROMOTE_EXACTLY_TO_1_OF_6_CROSS_CHECKED
LEAN_VERIFIED: NO
COFINAL_FAKE_IHARA: NOT_DECLARED
```
