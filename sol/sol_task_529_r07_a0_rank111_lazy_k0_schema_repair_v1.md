# Sol task 529 -- minimal schema repair for the rank111 lazy K=0 successor

Role: Sol(max) implementation repair under the researcher's existing explicit
authorization.  Repair exactly the two blockers in Task528; do not redesign
the selector, add mathematics, run full replay/production/GHA, or mutate
git/workflows/releases.  Do not overwrite v5/v9/v13.  Write only:

1. `search/d972_r07_a0_actual_tau_free_lazy_k0_seed_v6.py`
2. `crosscheck/check_d972_r07_a0_actual_tau_free_lazy_k0_seed_v10.py`
3. `search/d972_r07_a0_actual_tau_free_lazy_k0_rank111_resume_gha_driver_v14.g`
4. `sol/sol_reply_529_r07_a0_rank111_lazy_k0_schema_repair_v1.md`

Read Task528's complete STOP reply.  Derive thin versioned successors from:

- v5 `34773 / 94e9079c...aa5aa`;
- v9 `27570 / 9b9bfbf7...f29c0`;
- v13 `8683 / 8f034abc...5f63e`.

## A. Exact new-record round chain

In both producer and checker, require for records after the exact 68-source
legacy prefix:

- each `record["round"]` has exact type `int`;
- the first new round is strictly greater than legacy round 73;
- every later new round is strictly greater than its preceding new round;
- checkpoint/result round is an exact integer and is at least the last
  accepted record round (or at least 73 if there is no new record).

The generated replay must compare against this authenticated round; it must
not merely copy an untrusted round into an otherwise regenerated record.
Gaps are allowed because failed/resource attempts may consume a round.

Add a resealed mutation test for first-new round 1/73, a duplicate/decreasing
later round, and non-integer round.  The checker must reject them on its live
new-record path.

## B. Exact integer typing

Python booleans and floats must not pass as integers.  For every integer field
introduced or inherited in a **new v6 record**, require `type(value) is int`,
including at least:

- round, old/new rank, scalar, seed index and delta letters;
- record version, K, formula/direct scalar;
- exact exponent pair, N coefficients and normalized exponent quotients;
- required coordinates;
- fibre/kernel/coordinate/qid/gid cursor integers;
- checked-fibre count and every selector counter;
- action-source integer fields when present.

A small recursive new-record numeric gate may additionally reject every bool
or float in the record.  Strings and digest fields retain their exact existing
validators.  Apply exact integer typing to new checkpoint rank/round/count and
counter/progress integer fields as appropriate.  Do not reject the result's
legitimate `elapsed_seconds` float.

In both producer and independent checker, add resealed boolean/float mutations
for scalar, exponent/N, counters and cursor.  They must be rejected before or
during independent replay.  Preserve all existing physical/formula replay
checks.

## C. Confinement and transport

Apart from schema/marker/version/pin changes and the two repairs above, keep
the v5/v9 selector, task445 state owner, formula semantics, resource typing,
checkpoint algorithm and runtime limits byte-semantically unchanged.  V14 is
the v13 envelope with fresh paths/preamble/markers and exact v6/v10 pins;
permanent release, eight-member manifest/member 5 and all resource limits are
unchanged.  No production SELFTEST.

Run only bounded external-temp compile/fixture/checker/mutation/GAP-parse/
generated-`bash -n` checks.  Report exact files, bytes/SHA, a mechanical diff
classification, limitations and `READY_FOR_REAUDIT` or `STOP`.
