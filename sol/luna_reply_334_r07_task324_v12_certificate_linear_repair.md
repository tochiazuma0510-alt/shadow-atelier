# Luna reply 334 — task324/v12 certificate linear repair

IMPLEMENTED / UNEXECUTED. Only the five authorized v12 files were created;
v10/v11 and predecessors were preserved. No Python, Node, GAP, GHA, workflow,
git, or network execution was performed.

## Final identities

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_joint_slice_kernel_general_v12.py` | 13658 | `9749b836699ebced479393ec73fc94576c479f50ee596d8d0b7c1b4482521c48` |
| `crosscheck/check_d972_r07_joint_slice_kernel_general_v12.py` | 10174 | `ccd5b9916d9ed303710c212157e2011c234a4209dd54a2dac1c4efa33541c1c6` |
| `search/d972_r07_joint_slice_kernel_general_gha_driver_v12.g` | 3205 | `f29c4214229cc8f11efdddc9687378bc8824e0c41f67d3975fb2e9cd7ccc6624` |
| `search/certs/d972_r07_joint_slice_kernel_general_selftest_v12_20260829.json` | 615 | `84cf882cc46e5bce2ff4d51abe09201d6372e89008f7e9c44ba75f078e6de1e2` |
| this reply | excluded | self-referential |

The v12 fixture pins the complete v11 fixture at 12,964 bytes and SHA-256
`cab24a5e6ddd7812094b920bffd7688564092a3c9b718484bf3f887cf59d2058`, thereby
freezing all five cases, thirty base/binding pairs, six actions, action order,
targets, and expected tuples byte-for-byte. The v12 driver pins all three
implementation files and the fixture by the identities above, rejects stale
v7–v12 outputs, invokes exactly one producer and one checker, and writes its
sole sentinel last.

## Transcript and canonicality repair

Each case is parsed once from the pinned fixture. The producer uses a
`collections.deque` queue and emits seed records followed by every popped
accepted-row action in registered order. Every record binds ordinal, parent,
action, raw theta/z/eta, accepted/dependent decision, normalization, raw F3
coefficients, resulting rank, and reduction digest. The receipt binds
`production_input`, `closure_queue_pops == context.pops`, transcript length,
and the independently derived seed-plus-action queue bound.

Before any arithmetic modulo, recursive scalar/vector/matrix/transform/
coefficient checking rejects booleans, non-integers, and values outside F3.
The `+3` coefficient mutation reaches this owner explicitly. MEMBER witnesses
are not compared for equality: the certificate path compares only direct
ancestry replay, endpoint-zero slice semantics, and resulting rows/spans.
NONMEMBER remains a dual-annihilation/nonzero-pairing obligation.

The producer `RetainedF3Basis` performs one online construction per distinct
closure/Hd1 owner, carrying normalized rows and fully scaled transforms in
raw insertion order. Every accepted or dependent row is directly replayed.
The checker independently reconstructs the transcript and uses a
bottom-pivot dense augmented tableau with its identity block, followed by
two-way mathematical span checks. No cross-basis coordinate dictionaries are
compared.

## Mutation owners

The 19 inherited owners remain unchanged:

`field_modulus, theta_seed, theta_action, z_action, eta_action, D_entry,
O_entry, C_entry, action_order, premature_C, target, seed_index, parent,
row_theta, left_kernel, Hd1, member_ancestry, dual, terminal`.

The v12 transcript/canonicality owners are:

`production_input, closure_queue_pops, context_pops, closure_candidate_count,
closure_queue_bound, candidate_parent, candidate_action, candidate_decision,
candidate_normalization, candidate_coefficients, candidate_rank,
dependent_record_deletion, dependent_record_reorder, f3_plus3_coefficient,
member_witness_equality`.

All 34 records bind owner, exact code, stage, reason, canonical-before,
canonical-after, reseal, and rejection. Producer mutation boundaries use only
`SemanticReject`; checker replay independently reconstructs each mutation and
does not trust producer rejection flags.

## Performance and reachability

No production-reachable coefficient-vector product or all-F3 enumeration is
present. The only linear work is dequeued closure candidates, retained-basis
reductions, direct sparse replay, and one checker dense tableau per case.
Known-basis rank, containment, span, and ancestry queries reuse retained
owners. The static successful-fixture bounds are five closure owners, five
Hd1 owners, five checker bottom-pivot tableaus, at most five case transcripts,
and candidate count `seed_count + popped_rows * action_count`; coefficient
enumeration is bounded by the frozen rank-two canary only and is not used to
produce the certificate. JSON parsing is one fixture parse plus one pinned v11
source-fixture parse per implementation. No retry, sleep, poll, lock, pool,
subprocess, or `pop(0)` path exists.

The producer’s positive synthetic trace is: v12 fixture/schema and v11 pin →
strict F3 preflight → five raw cases → deque closure transcripts → retained
coefficient owners and direct replay → sealed receipt. The checker trace is:
raw fixture rebuild → independent transcript comparison → bottom-pivot dense
tableau and span replay → independent sealed verdict. Production remains
fail-closed before any actual matrices:
`STATIC_BLOCKED:actual typed matrices are not staged`.

The driver additionally performs a bounded seal-only file hash of the checker
verdict after checker exit, requires nonempty sealed producer/checker outputs,
exact-one full-line terminal markers and terminal equality, and then writes
the sole sentinel. No syntax or semantic command was run in this commission.

```text
IMPLEMENTATION:          IMPLEMENTED
SELFTEST / PRODUCTION:   UNEXECUTED
ACTUAL A5 / ACTUAL A6:   0/3 / 0/3
LIFT / FAKE / IHARA:     NONE
```

`TASK334_R07_TASK324_V12_CERTIFICATE_LINEAR_REPAIR`
