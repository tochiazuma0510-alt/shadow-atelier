# Luna task 324 - task320/v11 ancestry-preserving independent incremental repair

Role: Luna, bounded implementation only.  Read every section first to last.
Do not run Python, Node, GAP, GHA, workflows, git, or network.  Preserve every
v7--v10 file byte-for-byte.  Edit only the five versioned paths named below.

## 1. Inputs and sole outputs

Read in full:

- `sol/luna_task_307_r07_actual_joint_slice_kernel_general_v7.md`
- `sol/luna_reply_320_r07_task307_v10_action_shape_pin_echelon_repair.md`
- `sol/sol_task_322_r07_task320_v10_code_performance_audit.txt`
- `sol/sol_reply_322_r07_task320_v10_code_performance_audit_v1.md`
- the complete v10 producer, checker, driver, and fixture.

Create only:

- `search/d972_r07_joint_slice_kernel_general_v11.py`
- `crosscheck/check_d972_r07_joint_slice_kernel_general_v11.py`
- `search/d972_r07_joint_slice_kernel_general_gha_driver_v11.g`
- `search/certs/d972_r07_joint_slice_kernel_general_selftest_v11_20260828.json`
- `sol/luna_reply_324_r07_task320_v11_ancestry_independent_incremental_repair.md`

Return `IMPLEMENTED / UNEXECUTED` only if all gates below are present by
inspection.  Otherwise return `BLOCKED / UNEXECUTED` and do not weaken a
gate.  No execution is authorized by this commission.

## 2. Freeze the already repaired literal mathematics

Start from v10.  Apart from schema/version/source pins and mutation metadata,
the five literal cases, all 30 base/binding matrix pairs, all six stored
actions, action order, targets, and the five expected tuples must remain
exactly unchanged.  Preserve the twelve v10 trailing-zero action repairs and
the single-final-LF fixture normalization.  Run the complete action/base
shape and F3-scalar preflight in both programs before compilation/replay.

Production remains exactly fail-closed at
`STATIC_BLOCKED:actual typed matrices are not staged`.  SELFTEST, production,
actual A5/A6, lift, fake, and Ihara remain `UNEXECUTED`/false.

## 3. Producer coefficient-carrying echelon

Replace the v10 row-only echelon by one incremental owner which retains, for
every pivot row, both:

1. the fully normalized reduced mathematical row; and
2. its fully normalized coefficient vector in the insertion-order accepted
   raw-row roster.

Every scale/add operation must be applied to both halves.  Reduction of a new
row must return its remainder and a coefficient vector whose direct raw-row
linear combination reconstructs the original row.  An accepted row receives
one new identity coordinate before insertion.  A dependent row's returned
coefficients must replay it exactly.  Export explicit insertion order,
pivots, transforms, and direct reconstruction digests; replay them before
sealing.

Use this retained owner for closure, Hd1 membership/rank, two-way span tests,
and member ancestry.  Build each logically fixed basis at most once per case.
Do not recompute a full RREF merely to ask rank, containment, span equality,
or output a rank already owned by the retained basis.

## 4. Genuinely independent checker algorithm

Do not copy, rename, or lightly respell the producer's online reduction.  Use
a visibly different algorithm.  One acceptable design is a checker-owned
dense augmented Gauss--Jordan tableau built once from the full accepted-row
list, with an identity block carried through all row operations, followed by
batch coefficient solves against that canonical tableau.  Another genuinely
independent coefficient-preserving construction is acceptable if explained
line by line in the reply.

The checker must reconstruct closure and Hd1 from raw fixture data, recover
all transforms independently, and directly replay every producer-exported
coefficient map against the producer's raw rows.  Compare spans only by
two-way containment modulo independently built bases; never compare
coordinate dictionaries across the two bases.

Bind every receipt scalar/field that v10 left loose, including at minimum:

- `closure_rank`;
- `kernel_dim`;
- `full_nonzero_kernel_cardinality`;
- `target`;
- `slice_membership`;
- Hd1 rank/content;
- member theta ancestry or nonmember separating dual; and
- all change-of-basis/reconstruction transcripts.

## 5. Owner-specific mutation semantics

Keep the 19 registered mutation owner names, but repair both sides so that
each mutation changes the canonical bytes of its named owned object, reseals
where appropriate, reaches the intended independent semantic gate, and is
accepted as rejected only for one exact owner-specific stage/reason.

Do not catch broad `RuntimeError`, `ValueError`, `KeyError`, `TypeError`, or
`IndexError` classes as success.  Introduce a narrow semantic-rejection type
carrying a registered code, catch only that type at the mutation boundary,
and require equality with the mutation's expected code.  Any unrelated
exception is fatal.  In particular repair the v10 wrong-owner producer tests
for `seed_index`, `parent`, `row_theta`, `left_kernel`, `Hd1`,
`member_ancestry`, and `dual`: they must mutate and test the named produced
certificate object, not fail earlier through a fixture/control change.

The checker must not trust producer `{owner,rejected}` Booleans.  The receipt
must bind canonical-before/canonical-after digests, stage, and exact reason;
the checker independently proves the mutation changed, was resealed, and
fails at the registered owner gate.  No no-op, wrong seal, wrong owner,
earlier failure, or broad-catch result counts.

## 6. Performance contract

Enumerate all remaining RREF/echelon builds and give exact five-case upper
bounds.  Necessary fixed invertibility and nullspace calculations may remain.
For known closure/Hd1/span/ancestry bases:

- one retained construction per logically distinct basis per case;
- membership and rank queries reuse it;
- two-way span uses reductions against the retained owners;
- direct ancestry replay is sparse/dense linear combination, not a fresh
  rank build.

Remove the eight avoidable producer Hd1 rebuilds and at least the 58 exact
checker rebuilds identified by task322.  There must be no retry, sleep, poll,
lock, process pool, thread, subprocess beyond the driver-owned one producer
and one checker, or hidden repeated JSON parsing/serialization.  Report the
remaining maximum matrix dimensions, coefficient enumeration (`<=3^2`),
queue bounds, mutation counts, and why no avoidable known-basis rebuild
remains.

## 7. Driver, identities, and final accounting

The ASCII v11 driver must pin exact final byte counts and SHA-256 values for
producer/checker/fixture, stale-reject all v7--v11 owned outputs, invoke one
producer then one checker, require exact-one full-line PASS and terminal
markers, compare terminal payloads, require nonempty sealed outputs, and
write the sole sentinel last.  Do not embed a recursive driver self-hash.

In the reply provide exact bytes/SHA-256 for all four load-bearing files, a
v10-to-v11 change ledger, separate producer/checker algorithm descriptions,
all 19+19 mutation owners with expected codes, full performance counts, and:

```text
IMPLEMENTATION:             IMPLEMENTED or BLOCKED
EXECUTION:                  UNEXECUTED
SYNTHETIC SELFTEST:         UNEXECUTED
PRODUCTION:                 UNEXECUTED / STATIC_BLOCKED
ACTUAL A5 / ACTUAL A6:      0/3 / 0/3
LIFT / FAKE / IHARA:        NONE
```

`TASK324_R07_TASK320_V11_ANCESTRY_INDEPENDENT_INCREMENTAL_REPAIR`
