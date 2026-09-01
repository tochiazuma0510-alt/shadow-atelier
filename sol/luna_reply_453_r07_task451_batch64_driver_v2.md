# Luna Task453 - Task451 frozen-dual batch-cap 64 driver v2

## Status

PASS for the bounded driver-only scope.  The Task451 producer, checker,
candidate universe, arithmetic, and Python files were not changed.  No
production, GHA, git, network, retry, or worker-pool action was run.

## Output and pins

| object | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v2.g` | 2387 | `8f8c803cff86fbb4bb774570cb596e9e5a8262c05321e955e2cf0de545df60dc` |
| exact v1 driver owner | 2569 | `6910d38adc56a564b4cd80211bb994de72fd77bf2da6abd8df2df5597ab9a000` |
| generated batch-64 v1 inner | 2569 | `07ec885b719aea17e382a8dc9d5a1d94026c627c6d9c1f535842ebbb3fb41cf6` |

The wrapper fails closed on owner byte/SHA drift, patch cardinality drift,
generated-inner byte/SHA drift, or write/readback drift.  Its external launch
guard is the distinct
`D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V2_RUN=true`, and its final marker is
`R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V2_DRIVER_PASS`.

## Sole generated executable diff

The exact v1 owner contains one old literal and no new literal.  The generated
inner contains no old literal and exactly one new literal:

```diff
- --max-rises 64 --batch-cap 16 --output
+ --max-rises 64 --batch-cap 64 --output
```

This is the sole byte-level change in the generated production driver.  In
particular, total rise cap 64, 7,200-second cap, 4.8-GB RSS cap, producer and
checker pins, frozen rank-51 checkpoint pin, deterministic producer behavior,
fresh `ci/out` artifact/checkpoint/log paths, checker invocation, and all v1
markers remain byte-identical.  The v2 wrapper supplies only its distinct
external authority guard and final completion marker around that pinned inner.

## Bounded checks

- Exact v1 source pin: PASS.
- Unique replacement cardinality: PASS (`old 1 -> 0`, `new 0 -> 1`).
- Generated inner byte/SHA pin: PASS.
- Literal unified diff confinement to `--batch-cap 16` -> `64`: PASS.
- Driver ASCII-only, final newline, and no `SELFTEST`: PASS.
- Bounded GAP load without the external preamble stopped before all pin,
  filesystem, and production calls with the expected message:
  `Error, task453 external preamble required`.
- No `ci/out/a0_task453_inner.g` was created by that guard check.

No Q0 copy, eager store, search-space expansion, altered durability rule, new
negative claim, production SELFTEST, retry, or concurrency facility was added.

## Residual risk

No production timing or peak-memory measurement was made.  A batch cap of 64
can lengthen one open batch and increase its transient working set relative to
16, although the accepted cumulative 64-rise cap, 4.8-GB RSS cap, closed-batch
durability, and open-batch discard behavior are unchanged and still enforced
by the exact pinned producer/checker.

`TASK453_R07_TASK451_BATCH64_DRIVER_V2_PASS`
