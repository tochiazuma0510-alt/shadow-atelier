# Luna reply 358 — zero-base A5/A6 compiler v1

## Scope and status

The requested four files were created.  No Python, Node, GAP, SELFTEST,
fixture generation, GHA, retry, workflow, or git command was run.  The
compiler is production-only and fail-closed: absent or malformed upstream
owners produce a sealed typed `UNKNOWN_INPUT`; no provisional MEMBER or
NONMEMBER is manufactured.

The implementation incorporates v348 and v349.  It maintains the complete
pre-`C` action closure, streams both the A5 column `(a,Cb)` and (when the
authenticated exact endpoint coordinate is present) the augmented column
`(a,Cb,U(P))`, records an early A5 hit without stopping, and prefers an
augmented MEMBER.  A finite canonical augmented no-hit is never emitted as
an A7 negative.

## Created files

```text
search/d972_r07_zero_base_a5_a6_compiler_v1.py
  504 lines, SHA-256 abd44b7182a13bb53595f562df3310b0d96fb61e5ed54391446e1bf265df4173
crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v1.py
  369 lines, SHA-256 06055c2e9ea599d666711327b7ba75a9f02e6dae90bfe4c3cee3560f95651b72
search/d972_r07_zero_base_a5_a6_compiler_gha_driver_v1.g
   43 lines, SHA-256 59fb372eb56abbe8025535a6c6d564a750492228c95ff3f218eef81ee112a64e
```

Before freezing the candidate, the parent added exact producer/checker
byte/SHA pins to the driver and corrected its GAP `Exec` call to use one
concatenated shell command.  No mathematical code or execution was changed.

The only additional file is this reply; no fixture was created because the
commission forbids SELFTEST/fixture work.

## Input and owner boundary

The manifest schema is

```text
d972-r07-zero-base-a5-a6-compiler/v1/actual-input-manifest
```

It requires physical repository-relative descriptors for `a3_zero`,
`task198`, `a4`, `a0`, and `task193_actual`, plus a checker/verdict
descriptor for each and nonempty `common_identity`.  Each descriptor is read,
byte-count checked, SHA-256 checked, parsed, and self-seal checked when
present.  Absolute paths, traversal, links, and containment failures stop as
`UNKNOWN_INPUT`.

The producer derives the zero base by replaying the A3 terminal and requiring
empty target, lambda, and kappa0.  It accepts only the A4 `kernel.K_roster`
word-bearing items and their derived seed coordinates; no anchor, adapted
basis, or local A3 base-pair field is read.  It binds the A0 literal
`correction_word` to task193's literal binding and derives
`e1=-beta1_vector`.  The task198 runtime must expose the authenticated
zero-base `d1`, occurrence vector `w`, printed `C`, and marked actions.

The exact augmented coordinate is intentionally optional at this boundary:
if task193 `eta_c`, every seed `exact` coordinate, and every marked-action
`exact` map are present, the v349 augmented echelon is active.  If they are
absent, A5/A6 can still be compiled, but the receipt says
`A5_ONLY_AUGMENTED_NOT_BOUND`; it does not claim A7.

## Streaming algorithm

For every original A4 word-bearing seed the producer constructs the supplied
derived zero-base pair `(z,eta)` and factored seed ancestry
`(coefficient=1, prefix=[], original_A4_kernel_word_index)`.  It inserts the
pair into `E_pre`; only a rank-raising row enters the action queue.  For every
accepted row it inserts `(z,C eta)` into `E_joint`, and, where available,
`(z,C eta,exact)` into `E_aug`.  The target reductions are respectively

```text
E_joint: (e1, 0)
E_aug:   (e1, 0, eta_c)
```

The pre-`C` action decision always precedes `C`, as required by v348/v349.
The first zero remainder in `E_aug` returns an augmented MEMBER with the
finite coefficient transform and its complete selected ancestry.  An
`E_joint` zero is recorded but does not stop the closure.  After queue
exhaustion, an A5 hit returns MEMBER with an explicit augmented status; a
nonzero A5 remainder returns NONMEMBER only at exhaustion.  A5 member plus
augmented no-hit remains a canonical finite-state result, not an A7 negative.

For MEMBER, the receipt emits only the factored A6 records

```text
(coefficient, prefix_DAG_node, original_A4_kernel_word_index)
```

and the row/action/parent ancestry used to derive them.  No standalone
Boolean controls acceptance.  Equal factored records are collected modulo 3
only after ancestry has been retained.

The checker is separately written.  It independently reads the physical
manifest and upstream bytes, uses a reverse pivot direction, rebuilds the
pre-`C`, A5, and augmented streams, and requires the producer terminal to
equal its own replay terminal.  It does not import producer code, pivots,
caches, transcript, or A6 records as mathematical authority.

## A7 boundary

The exact endpoint coordinate is accepted only as an authenticated upstream
owner and is carried as a third streaming coordinate.  This v1 does not
implement the full literal PB3/PB4 universal endpoint evaluator or
constructive relator decomposition itself.  Therefore it deliberately
exports the complete literal A6 pair ancestry needed by the v281/v349 A7
consumer and labels an unavailable or non-hit augmented route without
promoting it to A7 NONZERO.  No compatible cofinal lift, fake, or Ihara
witness is asserted.

## Static status

```text
ZERO-BASE A3 / anchor removal:                 implemented in adapter
FULL PRE-C ACTION CLOSURE:                     implemented, execution pending
STREAMING E_joint A5 TEST:                     implemented, execution pending
STREAMING E_aug A5/A7 FUSION:                  implemented when exact owner is present
A6 FACTORED ANCESTRY:                          implemented, execution pending
INDEPENDENT CHECKER:                           implemented, execution pending
ACCEPTED ACTUAL A4/A0/task193 INPUT:           not present in inspected workspace
ACTUAL A5 MEMBER/NONMEMBER:                    not computed
ACTUAL A6 / EXACT PB ZERO / LIFT / FAKE/IHARA:  not established
```

IMPLEMENTATION:                  IMPLEMENTED
SELFTEST / PRODUCTION:           UNEXECUTED
ACTUAL A5 / ACTUAL A6:           0/3 / 0/3
LIFT / FAKE / IHARA:             NONE

`R07_ZERO_BASE_A5_A6_COMPILER_V1_IMPLEMENTED_UNEXECUTED`
