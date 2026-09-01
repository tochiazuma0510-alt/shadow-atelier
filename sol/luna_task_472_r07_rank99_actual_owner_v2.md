# Luna Task472 — actual rank-99 short-batch continuation owner v2

## Role

You are Luna.  Replace the rejected Task468 stub by the actual-owner transform
proved in `sol/proof_r07_rank99_actual_owner_transform_v424.md`.  This is an
implementation task; do not change the mathematics or invent a proxy engine.
Do not edit any Task468 file.

Frozen load-bearing inputs:

```text
search/d972_r07_a0_dual_anchored_active_batch_v1.py
  13834 ca7fb15e06dd04881146c38d63d93015a9e630fbc334cf15098cbd8a32f22f9b
crosscheck/check_d972_r07_a0_dual_anchored_active_batch_recovered_v2.py
  14442 1d1080cd3e130d987316feefd820215f495cd6320aa5eca764fd2f8997f0c424
search/certs/d972_r07_a0_dual_anchored_rank99_candidate_v1.json
  173082 bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358
sol/proof_r07_rank99_actual_owner_transform_v424.md
  7009 f2e2103f214e6d7c15f5d1c2bc84cd100cd37a69634c381793a42a20e8bad2d9
```

The parent will not dispatch production unless Task467 checker-only replay
passes.  Do not encode that prerequisite as a runtime terminal.

## Exact implementation

The producer must load and use the real Task451 arithmetic.  It must:

1. independently authenticate the exact old rank-99 state and its full
   first-eight/three-batch/48-row flattening, seals, ranks and round;
2. reconstruct physical rank 51 with the actual Task451 lineage and replay
   the three real batches to rank 99, then replay every appended own batch;
3. implement the v424 real ABI order
   `replay_atom -> aggregate -> (remainder,_) = phys.reduce(row)` and skip a
   dependent row before full conjugate/`seed_v12`/exponent/receipt;
4. for an independent row run every unchanged literal/scalar gate before one
   `add`, requiring actual pivot equals `min(remainder)`;
5. retain the actual action-row path and actual COMMON positive replay;
6. close batches at 16, count at most 64 new rises per invocation, maintain
   contiguous segments, and atomically preserve only `last_closed`;
7. authenticate/normalize input and write BOOTSTRAP before heavy
   construction, write READY only after full physical replay, and return a
   physical closed fallback for allowlisted internal wall/RSS/max-rise stops;
8. support both exact base-C99 input and appendable own-schema input.

Do not retain a dependent candidate's full conjugate or literal receipt.  Do
not infer NONMEMBER from a miss.  The default production path must enter the
real selector; a zero-work contingent success/COMPLETE path is forbidden.

The independent checker may import byte-pinned arithmetic primitives but no
producer search/resume/seal/fixture helper.  It must semantically replay rank
51 + eight records + the exact three old batches + every appended batch, and
check all v424 prefix, segment, delayed-row, pivot, post-state, resource, and
positive gates.

The driver must accept only a canonical one-component
`search/certs/<safe-name>.json` input (`PositionSublist` for `..`, exact
`.json` suffix, no symlink escape), invoke one producer and one checker under
`set -euo pipefail`, internal wall/RSS bounds plus an external foreground
supervisor, fresh outputs, and exact markers.  It must not certify zero work:
a legitimate terminal is actual COMMON or an allowlisted resource result with
an independently replayed physical closed checkpoint.

## Executed bounded gates

Fixtures must call the same production validators/ABI and checker entry, not
hard-code capability booleans.  Include at least:

- dependent row: exactly one `replay_atom`/reduce, zero full seed/exponent/add;
- independent row: one full seed and one add with predicted=actual pivot;
- exact base and one appended own-schema resume;
- prefix/batch/segment mutations;
- cap 63 reject, 64 accept, 65 reject;
- open-batch and missing-physical-fallback rejection;
- early construction RESOURCE returns BOOTSTRAP;
- path traversal, repeated dots, non-JSON and symlink escape rejection; and
- checker rejection of a structurally sealed but semantically altered row.

No full production, GHA, workflow edit, git, or expensive authority run.

## Exact outputs

Create only:

1. `search/d972_r07_a0_dual_anchored_rank99_actual_owner_v2.py`
2. `crosscheck/check_d972_r07_a0_dual_anchored_rank99_actual_owner_v2.py`
3. `search/d972_r07_a0_dual_anchored_rank99_actual_owner_gha_driver_v2.g`
4. `sol/luna_reply_472_r07_rank99_actual_owner_v2.md`

Do not create bytecode caches.  End with
`TASK472_R07_RANK99_ACTUAL_OWNER_V2_PASS` or a typed STOP.
