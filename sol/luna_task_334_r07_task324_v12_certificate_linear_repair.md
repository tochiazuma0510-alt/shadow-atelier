# Luna task 334 - task324 A5/A6 v12 certificate and linear-time repair

Role: bounded implementation only.  Read every section first to last.  Do not
run Python, Node, GAP, GHA, workflows, git, or network.  Preserve v10/v11 and
all predecessors.  Create only:

- `search/d972_r07_joint_slice_kernel_general_v12.py`
- `crosscheck/check_d972_r07_joint_slice_kernel_general_v12.py`
- `search/d972_r07_joint_slice_kernel_general_gha_driver_v12.g`
- `search/certs/d972_r07_joint_slice_kernel_general_selftest_v12_20260829.json`
- `sol/luna_reply_334_r07_task324_v12_certificate_linear_repair.md`

## 1. Governing audit and frozen mathematics

Read task324/reply324, task329/reply329, the complete v10/v11 quartets, v242,
and every source pinned by v11.  Preserve byte-for-byte the v10/v11 five-case
mathematics: 30 base/binding pairs, six actions, case order, targets, expected
tuples, and production `STATIC_BLOCKED`.  This task computes no actual A5/A6.

## 2. Bind the complete closure transcript

For every case emit and seal the complete producer-order closure candidate
transcript: seed candidates followed by each popped accepted row's actions in
the registered action order.  Each record binds ordinal, parent, action,
raw theta/z/eta, accepted/dependent decision, normalization, canonical F3
reduction coefficients, and resulting rank.  Require

```text
closure_queue_pops == context.pops == number of popped accepted rows
closure_candidate_count == transcript length
closure_queue_bound == independently derived seed/action bound
```

and bind the top-level `production_input`.  The checker independently rebuilds
the candidates from raw fixture data and compares every transcript record; it
must not trust producer counts or accepted flags.  Add narrow mutations for
each formerly unbound scalar and for deletion/reordering of a dependent
record.

## 3. Canonical F3 and witness semantics

Before any modulo operation recursively type/range-check every receipt scalar,
vector, matrix, transform, reduction/direct/kernel/ancestry/dual coefficient:
exact Python `int`, never `bool`, and `0 <= value < 3`.  Shapes and dimensions
must be derived and checked.  Add a resealed `+3` coefficient mutation that
reaches the canonical-F3 owner on both producer and checker.

Do not require equality between independently selected MEMBER theta witnesses.
Replay the producer ancestry directly and independently prove that it maps to
the target and satisfies the endpoint-zero slice.  Compare only the resulting
mathematical row/span.  A NONMEMBER still requires a canonical dual annihilating
all Hd1 rows and pairing nontrivially with the target.

## 4. Remove exponential and duplicate work

No production-reachable `itertools.product(..., repeat=rank)` or enumeration
of all F3 coefficient vectors is permitted.  The checker must use its own
bottom-pivot incremental/dense tableau, ordinary nullspace, solve, and two-way
span routines with polynomial bounds.  A tiny exhaustive canary is allowed
only behind an exact SELFTEST-only rank-at-most-two guard and must not provide
the certificate.  Use `collections.deque`, not `pop(0)`.

Replay each retained owner export once.  Reuse the retained Hd1 owner instead
of re-enumerating it.  Remove duplicated kernel/Hd1/left-kernel containment
passes while retaining independent two-way span and coefficient replay.  Give
exact successful-fixture counts and symbolic polynomial bounds in closure
rank r, kernel dimension d, Hd1 rank h, ambient widths, and candidate count.

## 5. Seals, mutations, and driver

Keep the 19 old semantic mutations and add the new transcript/canonicality
owners.  Producer and checker must independently reach each narrow gate;
broad exceptions do not count.  Seal the full producer receipt and checker
verdict over canonical bytes.  After the checker exits, the ASCII driver must
use a separate bounded seal-only consumer/hash path to recompute the complete
verdict (and production receipt when applicable), not merely count a 64-hex
substring.  Retain exactly one producer and one checker process, exact-one
full-line terminals, stale v7--v12 rejection, terminal equality, and sole
sentinel last.

## 6. Reply contract

List exact final identities, dependency graph, transcript equations, canonical
F3 gates, distinct linear algorithms, removed work, mutation table, static
reachability, and resource accounting.  Return only `IMPLEMENTED / UNEXECUTED`
or the first exact `BLOCKED / UNEXECUTED` owner.  No local execution.  End with

```text
IMPLEMENTATION:          IMPLEMENTED or BLOCKED
SELFTEST / PRODUCTION:   UNEXECUTED
ACTUAL A5 / ACTUAL A6:   0/3 / 0/3
LIFT / FAKE / IHARA:     NONE
```

TASK334_R07_TASK324_V12_CERTIFICATE_LINEAR_REPAIR
