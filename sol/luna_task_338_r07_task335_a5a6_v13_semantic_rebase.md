# Luna task 338 - task335 A5/A6-v13 semantic rebase

Role: Luna, bounded implementation only.  Read this FULL mail and every
numbered section first to last.  Do not run Python, Node, GAP, GHA, workflows,
network, or git.  Preserve every v7--v12 file, fixture, proof, authority, and
v220.  Edit only the five new v13 outputs in Section 2.

## 1. Binding inputs and repair boundary

Read in full:

- task324/reply324, task329/reply329, task334/reply334, task335/reply335;
- `sol/proof_r07_actual_a5_three_input_slice_compiler_v242.md` and v231;
- all complete v11 and v12 producer/checker/driver/fixture files; and
- the literal source fixture pinned by v12, including all five cases, all
  thirty base/binding pairs, six stored actions, and twelve trailing-zero
  repairs.

Task335 is the binding defect ledger.  V13 is a semantic rebase on immutable
v11, not a patch of v12's shaped transcript.  Retain only v11 code paths whose
actual invariant you can restate and replay.  V12 constants, copied seed
records, zero eta placeholders, hard-coded POPS/ranks/terminals, detached
tableau digests, forced mutations, and trusted Booleans are forbidden.

## 2. Sole permitted outputs

Create only:

- `search/d972_r07_joint_slice_kernel_general_v13.py`;
- `crosscheck/check_d972_r07_joint_slice_kernel_general_v13.py`;
- `search/d972_r07_joint_slice_kernel_general_gha_driver_v13.g`;
- `search/certs/d972_r07_joint_slice_kernel_general_selftest_v13_20260829.json`;
- `sol/luna_reply_338_r07_task335_a5a6_v13_semantic_rebase.md`.

Return `IMPLEMENTED / UNEXECUTED` only if the five literal cases reach their
arithmetic terminals by static trace and every certificate/mutation/driver
gate below is present.  Otherwise return `BLOCKED / UNEXECUTED` with the first
exact missing owner/API.  No execution is authorized.

## 3. Strict frozen input validation

The v13 wrapper must bind the immutable v11 source fixture by exact resolved
path, bytes, SHA and schema.  Producer and checker load that source explicitly;
neither may validate the v13 wrapper as though it were the v11 fixture.
Authenticate every literal field, all 30 base/binding pairs with exact
equality, the five expected tuples, all matrix shapes, action rosters/orders,
and the twelve accepted zero repairs.

Before any arithmetic, recursively require exact Python integers excluding
bool, canonical representatives in `{0,1,2}`, rectangular matrices, and every
dimension needed by multiplication.  Never silently coerce floats, strings,
None, booleans, or out-of-range values with `%3`.

## 4. One live mathematical closure owner

Rebase on v11's actual matrix arithmetic.  For each case construct every seed
from its literal theta and the actual frozen D/O maps, so the live occurrence
row is the commissioned 13-coordinate joint image `(z,eta)`; theta remains
coefficient ancestry and is not appended to the pivot universe.  For each
dequeued rank-raising row, apply each stored action matrix in the exact frozen
order to the actual theta/z/eta data.  Do not copy a modulo-index seed or emit
an action label without applying its matrix.

Maintain one queue containing exactly accepted rank raises.  Stop only at
queue exhaustion.  For every seed and action candidate, before reduction,
append a chronological record containing literal parent/action, immutable raw
candidate, pre-rank, reduction coefficients, decision, normalization scalar,
normalized row/ancestry, post-rank, and queue effect.  Derive all fields from
the live owner; no independent POPS/rank table may influence control flow.

Use one explicit retained-basis invariant and enforce it after every
operation.  Pad every existing transform with zero whenever the raw roster
grows.  State signs so that replay of returned direct raw coefficients equals
the original candidate.  Apply every row operation and scale to coefficients,
retain zero-relation coefficients for dependencies, and replay both accepted
and dependent candidates exactly.  Normalize only after complete reduction.

## 5. Post-closure kernel, Hd1, and exact terminals

Only after the joint closure exhausts, apply the literal C map at its defined
owner boundary.  Compute, rather than declare:

1. the closure basis and its coefficient ancestry;
2. the left-kernel/nullspace needed by v242;
3. the reconstructed kernel rows in the raw theta ancestry;
4. `Hd1`, its retained transforms, rank, and two-way relation to the closure;
5. the literal target reduction against `Hd1`; and
6. exactly one terminal certificate.

MEMBER returns an explicit raw ancestry whose replay is the target.  The
checker need not reproduce the same noncanonical coefficient vector, but must
prove the supplied one and its own solution.  NONMEMBER returns a dual in the
authenticated coordinate universe, proves annihilation of every `Hd1` row,
and proves nonzero target pairing.  No artificial key, copied expected
terminal, post-hoc C application to the wrong span, or Boolean span claim is
allowed.

Every one of the five frozen cases must recover its expected
`(closure_rank,kernel_dimension,nonzero_kernel_count,Hd1_rank,terminal)` from
actual arithmetic.  A mismatch is `UNKNOWN_INPUT`, not a passing selftest.

## 6. Independent polynomial checker

The checker may share only immutable literal input bytes, never producer code,
echelon helpers, transcripts, mutation oracle, ranks, pivots, ancestry, or
Booleans.  Implement a genuinely separate bottom-pivot or dense tableau,
ordinary polynomial-time nullspace and solve, and a different pivot/order
convention.  Exponential coefficient enumeration such as `3^r` is forbidden.

Independently reconstruct all seeds/actions, the chronological candidate
sequence, closure, kernel, `Hd1`, target terminal, and producer certificate.
Verify semantic two-way span containment at every basis boundary.  Compare
canonical subspaces/terminals and replay supplied certificates; do not demand
equality of nonunique MEMBER witnesses or trust a digest merely because it is
a string.

## 7. Real owner mutations

Keep one identical registered roster of at least 34 producer and 34 checker
mutations covering every owner named in task335.  Each mutant must modify the
actual production-shaped fixture, raw candidate, transcript, receipt, or
verdict, be correctly resealed when applicable, run through the normal
semantic validator, and be rejected with its registered narrow stage/code/
reason.  At minimum cover field/type/shape, each seed/action/D/O/C owner,
action order, premature C, target, parent/action/decision/normalization/rank/
coefficients, accepted and dependent replay, left kernel, `Hd1`, MEMBER
ancestry, NONMEMBER dual, queue counts/bounds, production input, envelope,
seal, terminal, duplicate terminal, stale output, and resource cap.

An explicit `raise` chosen from the mutation name, a generic toy object,
`canonical_before != canonical_after`, or a producer `rejected=true` flag is
not a mutation test.  The independent checker regenerates and routes every
mutant itself.

## 8. Resource and performance contract

Meter actual JSON reads/parses, candidate construction, queue pops, action
applications, field operations, pivot reductions, coefficient updates,
nullspace/solve work, ancestry replay, mutation work, canonicalization,
serialization, RSS, and output write.  Counters are per case plus explicit
totals; never compare a cumulative total with a per-case expected count.

Give polynomial bounds in number of candidates N, joint width 13, closure
rank r, kernel dimension d, and `Hd1` rank h.  Remove repeated known-basis
rebuilds, duplicate closure computation, unnecessary dense augmented
tableaus, repeated whole-object canonicalization, recursive ancestry
expansion, and all sleep/poll/retry/lock/thread/pool/subprocess paths.  Do not
claim speed by omitting kernel, `Hd1`, certificate, mutation, or checker work.

Seal the exact final resource snapshot after charging canonicalization and
write.  Cap exhaustion is only `UNKNOWN_RESOURCE`; malformed input is only
`UNKNOWN_INPUT`.  Broad exception conversion to a PASS-prefixed line is
forbidden.

## 9. Driver and final report

The ASCII GAP driver must support explicit SELFTEST and PRODUCTION modes,
pin the current producer/checker/fixture bytes and SHA, stale-reject the real
owned receipt/verdict/log/terminal/shell/sentinel paths for v7--v13, and
actually execute one producer followed by one checker under timeout.  Validate
both canonical internal seals, nonempty files, exact-one equal full terminal
payloads, terminal-specific sidecars, and write the sole sentinel as the
literal final successful operation.  GAP must execute any emitted shell and
propagate its status.

Production may remain `STATIC_BLOCKED` only at the exact absent actual typed
matrix input owner; the driver still needs a real production route and must
not trust a producer terminal string as arithmetic evidence.

The reply must list exact bytes/SHA for the quartet, complete import graph,
five actual static arithmetic traces and observed ranks, retained-basis sign
invariant, checker algorithm/independence, all 34+34 mutation owner routes,
polynomial counts/bounds, driver process flow, and every remaining blocker.
End with:

```text
IMPLEMENTATION:                  IMPLEMENTED or BLOCKED
SELFTEST / PRODUCTION:           UNEXECUTED
FIVE FROZEN CASES:               STATICALLY REACHABLE or BLOCKED
ACTUAL A5 / ACTUAL A6:           0/3 / 0/3
LIFT / FAKE / IHARA:             NONE
```

Any future execution requires a new Sol(max) code-and-performance PASS.

`TASK338_R07_TASK335_A5A6_V13_SEMANTIC_REBASE`
