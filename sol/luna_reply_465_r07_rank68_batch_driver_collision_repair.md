# Luna Task465 — rank68 batch-driver collision repair

## Status

PASS.  The committed Task453 driver was restored byte-for-byte at v2, and the
Task463 rank68 direct driver was moved to the new v3 filename.  The Task463 v2
producer, checker, and reply were not modified.

## Pins

| path | bytes | SHA-256 |
|---|---:|---|
| restored `search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v2.g` | 2387 | `8f8c803cff86fbb4bb774570cb596e9e5a8262c05321e955e2cf0de545df60dc` |
| new `search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v3.g` | 2569 | `54378c6a3067bcf53c007126da195ae070724d038469486217806675965075ee` |

The v2 physical bytes/hash equal `git show HEAD:search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v2.g` exactly.  The v3 driver retains the existing Task463 v2 producer/checker pins, frozen rank-68 checkpoint pin, v2 artifact/checkpoint/log paths, inner v2 producer/checker markers, and the one-producer invocation:

`--seconds 7200 --rss-bytes 4800000000 --max-rises 64 --batch-cap 64`

Only its external launch guard and final marker are v3:

`D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V3_RUN:=true;;`

`R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V3_DRIVER_PASS`

## Bounded gates

- HEAD byte/hash comparison and exact equality — PASS.
- v2/v3 ASCII and final-newline checks — PASS.
- Static guard/process/cap scan — PASS: v3 guard, one producer, fresh v2 paths, 7200 seconds, 4,800,000,000 RSS bytes, 64 max rises, batch cap 64, v2 inner markers, and v3 terminal marker.
- No production, GHA dispatch, workflow edit, git mutation, or network action performed.

`TASK465_R07_RANK68_BATCH_DRIVER_COLLISION_REPAIR_PASS`
