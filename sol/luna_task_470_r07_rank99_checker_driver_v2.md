# Luna Task470 — rank99 recovered checker-only driver v2

## Role and scope

You are Luna.  Repair only the launch envelope which made GHA run
`33530987296` fail before the recovered checker was invoked.  Do not change
the checker or any mathematics, and do not run the producer.

Read:

- `sol/luna_reply_467_r07_rank99_recovered_checker_only.md`
- `search/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_gha_driver_v1.g`
- `crosscheck/check_d972_r07_a0_dual_anchored_active_batch_recovered_v2.py`

The observed GHA failure is exactly:

```text
Error, task467 driver: pin drift recovered checker
```

The committed checker blob is nevertheless exactly 14,442 bytes with
SHA-256
`1d1080cd3e130d987316feefd820215f495cd6320aa5eca764fd2f8997f0c424`.
Thus the v2 driver must authenticate this source inside the already required
`set -euo pipefail` bash envelope using `wc -c` and `sha256sum`, before the
single checker invocation.  It must not use GAP `StringFile`/`HexSHA256` for
this source pin.  Keep all immutable release, six-member, working-checkpoint,
timeout/RSS, exactly-one-PASS, and receipt bindings from v1.

## Exact outputs

Create only:

1. `search/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_gha_driver_v2.g`
2. `sol/luna_reply_470_r07_rank99_checker_driver_v2.md`

Do not edit v1 or the checker.  Do not create bytecode caches.  No git, GHA,
workflow edit, producer execution, or semantic replay.

## Bounded gates

- ASCII/final-newline and GAP load to the external-preamble guard.
- Static cardinality: exactly one `python3` checker command and no producer.
- Static proof that checker byte count and SHA are tested by bash before that
  command.
- Preserve collision-safe extract/work roots and nonzero/timeout propagation.

End the reply with `TASK470_R07_RANK99_CHECKER_DRIVER_V2_PASS` or a typed STOP.
