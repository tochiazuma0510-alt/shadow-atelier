# Luna Task469 — A4 row-26 resource-envelope checker-only replay

## Role and scope

You are Luna.  Implement the narrow checker repair proved in
`sol/proof_r07_a4_terminal_resource_witness_v423.md`, then build a
producer-free GHA driver which replays the immutable artifact from run
`33506331399`.  Do not change A4 producer arithmetic, the row/delta transport,
or checkpoint cadence.  Do not implement row-27 intra-query resume in this
task.

Read the v28 checker and the original v41 driver/result contract.  The exact
old contradiction is in generated v28: its terminal resource envelope first
requires every typed counter occurrence to be `<= cap`, then requires the
reason's named trigger to be `> cap`.

## Required checker

Create a versioned v29 wrapper successor of
`crosscheck/check_d972_r07_word_independent_successor_kernel_v28.py`.
Patch only the typed `UNKNOWN_RESOURCE` envelope:

- parse and authenticate the unique `(cap,value,limit,state)` witness;
- allow that one coordinate, and every equal typed-view occurrence of that
  same coordinate, to exceed its authenticated cap;
- require all other coordinates to remain within cap;
- retain all domain, equality, type, nonnegative, checkpoint-seal, delta-chain,
  authority, producer-code, and terminal-serialization gates;
- do not weaken `UNKNOWN_INPUT` or positive-result checking.

Its self-test must accept one honest wall-time excess and reject at least the
eight mutations listed in v423, including a second over-cap coordinate.

## Immutable production binding

- run/job/head: `33506331399` / `99851144256` /
  `5dbc895552efdaffb13bb7b10e595430026f4c3c`
- artifact id/name: `9809473723` / `gap-run-out`
- original artifact digest:
  `sha256:4a82302e49ddfdd7790df0e0082d0762de3238c0b4e0de23259d97bd1a2af445`
- permanent asset:
  `https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9809473723_gap-run-out.a4-row26.zip`
- asset: 56,410 bytes /
  `5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a3360e3`

The driver must authenticate the zip before extraction and authenticate at
least these replay inputs before the sole checker process:

```text
d972_r07_word_independent_successor_kernel_v40.json
  9300 7fd2ec4a308d155e73431ae19441b29a1860dedb6243d0ddfd91d24cc8faecc5
d972_r07_word_independent_successor_kernel_v40.producer.base.checkpoint.json
  25581 595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445
d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json
  700 910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114
d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json.delta.00000001.json
  3551 d1f0ffdda299316ff1805f7a565ffe012fed63001bca74f0bc9e3ef2aeaf0e19
d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json.delta.00000002.json
  3625 acb34c8c69863cc274df4a12c614b002101770d97292f2c0df8bb43158df8523
d972_r07_word_independent_successor_kernel_v40.checker.checkpoint.json
  8991 b96919b38272d87a6885da98a18603065d1c2ccf805cd2c4f65dd22e32ed7af2
```

The checked-in Task198 authority files remain the checker inputs.  Use a
fresh isolated extraction root; copy only the authenticated replay inputs to
their required `ci/out` names.  The generic workflow owns `ci/out/driver.g`
and `ci/out/run.log`; never reject or overwrite them.  Invoke exactly one
v29 checker and no producer.  Use `set -euo pipefail`, an external timeout,
RSS bound, exact terminal-line cardinality, and a receipt binding run,
release, checker, terminal status, and row-26 HEAD/delta seals.

The expected checker terminal is `UNKNOWN_RESOURCE`, not a positive PASS.
Only a full checker replay may promote row 26 to cross-checked; a fixture may
not.

## Exact outputs

Create only:

1. `crosscheck/check_d972_r07_word_independent_successor_kernel_v29.py`
2. `search/d972_r07_word_independent_successor_kernel_row26_checker_only_gha_driver_v1.g`
3. `sol/luna_reply_469_r07_a4_row26_resource_checker_only_v1.md`

Do not create bytecode caches.  No production, GHA, workflow edit, git, or
semantic replay.  End with `TASK469_R07_A4_ROW26_RESOURCE_CHECKER_ONLY_PASS`
or a typed STOP.
