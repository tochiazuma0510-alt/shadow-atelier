# Luna task 234 - task227 second static repair v1

Date: 2026-08-28

Role: bounded mechanical implementation.  Parent Sol owns the mathematics,
acceptance, git, and GHA.  Read Sections 1--10 in full.  Do not run Python,
Node, GAP, git, GHA, or network.

## 1. Verdict, dependency, and authorized scope

The task230 revision is **REJECTED BEFORE EXECUTION**.  None of its member,
dual, mutation, 486/729, or checker claims is evidence.  Repair only:

```text
search/d972_r07_typed_single_seed_endpoint_consumer_v2.py
crosscheck/check_d972_r07_typed_single_seed_endpoint_consumer_v2.py
search/d972_r07_typed_single_seed_endpoint_consumer_gha_driver_v2.g
search/certs/d972_r07_typed_single_seed_endpoint_consumer_selftest_v2_20260828.json
sol/luna_reply_227_r07_typed_single_seed_consumer_v2.md
```

Do not edit task226, task233, proofs, predecessors, or workflows.  Target the
ABI contract in task233 Section 6.  If exact spelling cannot be finalized
without reading the repaired task226 file in the shared tree, wait until that
file appears, then adapt only these five files.

## 2. Exact defects found by parent Sol

1. `add_echelon` combines ancestry with `{**anc,**basis_anc}`.  On a shared
   actor key this discards the old ancestry coefficient.  Use the union of
   keys and `anc.get(k,0)-s*basis_anc.get(k,0)`.
2. The block echelon stores ancestry in occurrence-row IDs, but member
   recovery takes only `next(iter(...))`.  It therefore loses every other
   coefficient in a combined basis row.  Compose the complete ancestry map.
3. `kappa_from_lambda` emits `lambda-lambda*z0`; v216 requires
   `kappa=lambda*(z0-1)=lambda*z0-lambda`.
4. A positive branch never replays `kappa odot w`; it only replays
   `lambda odot u0`.  All three equalities in task230 Section 6 are mandatory.
5. The checker's alleged 486 roster contains `t` and `t(z0-1)`, while its
   acted degree-two row is `t*z0^2-t`.  The canonical basis is
   `t(z0-1)` and `t(z0-1)^2=t*z0^2+t*z0+t` over F3.
6. `compare_sparse_spans` does not normalize pivot rows and is never called.
7. The producer result omits `specialization_v216_abi`, although the checker
   expects it.  The checker does not decode or compare the producer occurrence
   basis, block basis, lambda/kappa, member replay, or dual.
8. SELFTEST has only a zero target member, a coordinate-shortcut nonmember,
   no zero-seed nonmember, no production-shaped tags, and no genuine mutation
   execution.  Most mutations merely set `modulus=8`.
9. Empty serialized `u0` skips comparison.  Predecessor authentication trusts
   arbitrary `accepted=true` dictionaries and requires invented task226
   member/manifest files which task226 does not produce.
10. RSS/elapsed use is not measured, and production UNKNOWN terminals are
    written as independently accepted verdicts.

## 3. Correct producer closure and ancestry

Retain the repaired Q3/Q4 arithmetic, actor normal form
`x^a y^b h^r`, marked action `p_o q_o(g) p_o^-1`, and complete seed
`u0=(z0-1) odot w`.  Parse task233's exact eleven-row, zero-safe `u0` format
and compare every row even when all are empty.

Every occurrence echelon entry is `(normalized_row,lambda)`, where `lambda`
is a sparse map on all 729 actor triples.  Row subtraction, pivot scaling,
and generator translation must apply the identical operation to every
coefficient of `lambda`.  For each retained row require direct replay

```text
row == lambda odot u0.
```

Close under all four marked generators until the queue is empty.  A 487th
independent row is `UNKNOWN_INPUT` with a typed arithmetic/rank reason, not a
valid nonmember or generic resource stop.

## 4. Exact block solve and positive certificate

Apply `C` only after occurrence closure.  A block-echelon row must retain a
sparse ancestry map on *all* occurrence-basis row IDs.  Reduction of the
target returns the full original-row coefficient vector `(c_i)`, not pivot
IDs or one arbitrary ancestor.

On zero remainder form

```text
lambda = sum_i c_i lambda_i
kappa  = lambda*(z0-1) = lambda*z0-lambda.
```

Implement a generic action of a group-ring coefficient on either `u0` or
`w`, and directly require and serialize:

```text
sum_i c_i row_i             == lambda odot u0
lambda odot u0              == kappa odot w
C(kappa odot w)             == bar_epsilon_1
kappa mod F3[D1/R0]         == 0.
```

The positive certificate carries `(c_i)`, every used occurrence ancestry,
`lambda`, `kappa`, all three replay rows, and their digests.  Do not return the
whole seed-basis ancestry as the target certificate.

## 5. Exact negative dual

For a nonzero target remainder, solve the full annihilator system on the
union coordinate roster.  Normalize `phi(target)=1`.  Directly require and
serialize:

```text
phi(C(row_i))=0 for every producer occurrence-basis row
phi(C(g odot u0))=0 for all 729 actors
phi(target)=1.
```

The target must be rejected if any coordinate, coefficient, or roster entry
is omitted.  A one-coordinate shortcut is not a general solver.

## 6. Independent checker: actual 486/729 equality

The checker independently authenticates and rebuilds task226's ABI, Q3/Q4,
`w`, `u0`, marked maps, and `C`.  It constructs the 243 transversal elements
`t=x^a y^b h^r`, `0<=r<3`, and exactly these 486 coefficients:

```text
t(z0-1)   = t*z0-t
t(z0-1)^2 = t*z0^2+t*z0+t.
```

Act every coefficient on `w`.  Build normalized sparse echelons and compare
the independent 486-row occurrence span to the decoded producer occurrence
span in both directions.  Repeat after applying `C`.  Separately construct
all 729 `g odot u0` rows.

For MEMBER, reconstruct the complete `(c_i)`, `lambda`, and `kappa` and replay
all Section 4 equalities independently.  For NONMEMBER, reconstruct `phi`,
annihilate both the producer basis and all 729 direct rows, and obtain target
pairing one.  Recompute the terminal; never accept a supplied terminal by
presence of `ancestry` or `dual`.

Normalize every pivot row before reduction.  Span comparison must call the
actual reducer on every row in both directions and compare ranks.  Advertised
counts and digests alone are insufficient.

## 7. Real task226 authentication

Remove the invented task226 member and manifest inputs.  Production consumes
exactly:

```text
ci/in/d972_r07_actual_two_word_endpoint_specializer_v2.json
ci/in/d972_r07_actual_two_word_endpoint_specializer_v2.verdict.json
ci/in/d972_r07_actual_two_word_endpoint_specializer_v2.binding.json
```

The receipt must have task226 schema and exact COMPLETE terminal.  The verdict
must be canonical, `accepted=true`, `independent=true`, and bind receipt
path/bytes/SHA plus ABI SHA exactly as task233 Section 6.  The binding schema
is exactly `d972-r07-task226-production-binding/v1` and binds receipt and
verdict path/bytes/SHA, run ID, immutable head SHA, artifact ID and ZIP SHA,
exact COMPLETE terminal, and checker acceptance.  Cross-compare every value.
Missing, SELFTEST, UNKNOWN, noncanonical, stale, or mismatched input is
`UNKNOWN_INPUT` before closure.

Embed the exact sealed ABI in the consumer result, together with its SHA, so
the checker has no hidden predecessor state.

## 8. Production-shaped SELFTEST and genuine mutations

Use all eleven immutable tags and the exact task233 ABI format.  Build four
cases:

1. nonzero seed with at least two rank increases and at least one dependent
   queued row;
2. a nonzero member target selected from a nontrivial retained coefficient,
   with nonzero lambda and complete positive replay;
3. a nonmember target sharing support coordinates with the block span and a
   genuinely multi-coordinate dual when possible; and
4. zero seed with both zero-target member and nonzero-target nonmember.

The independent checker must fully replay all four cases.  For each mutation
record `changed_field`, `expected_gate`, `observed_reason`, and rejection.
Each roster name changes the named datum and invokes its owning semantic
validator.  Add explicit controls for shared-key ancestry cancellation,
multirow block ancestry, reversed kappa sign, omitted `kappa odot w`, wrong
degree-two ideal row, unnormalized span pivot, skipped span call, empty-u0
mismatch, fabricated task226 files, shallow member, shallow dual, omitted
producer basis row, omitted 486 row, and omitted 729 translate.  It is
forbidden to reject unrelated names solely by changing modulus.

## 9. Resource, output, and driver

Measure actual input bytes, actor operations, sparse support, queue work,
rank increases, block work, dual work, checker work, mutation work,
serialized bytes, elapsed wall time, and peak RSS when available.  A cap stop
writes a fresh sealed `UNKNOWN_RESOURCE` receipt with phase/cap/value/limit;
bad input writes fresh sealed `UNKNOWN_INPUT`.  Refuse stale producer or
verdict outputs.

The checker verdict binds receipt bytes/SHA, recomputed terminal, predecessor
ABI SHA, occurrence/block ranks, and independent reconstruction digest.  It
may describe UNKNOWN but must set `accepted=false`; only MEMBER or NONMEMBER
after full replay has `accepted=true`.

Update the serial GAP driver for the three real task226 input files, final
source pins, anchored exact terminal equality, and fresh outputs.  UNKNOWN is
a typed run result, not A3 progress.

## 10. Reply and v220 boundary

Report every repair, exact file identities, unexecuted status, and dependency
on task233.  State:

```text
A3 actual package:       0/1 until accepted actual task226 input
A3 orbit closure:        0/1 until complete actual queue/486 equality
A3 membership-or-dual:   0/1 until accepted actual terminal
SELFTEST infrastructure: does not increment A3
A4 and later:            untouched
```

No pointed multiplier, exact PB endpoint zero, compatible lift, fake, or
Ihara witness is constructed by this task.
