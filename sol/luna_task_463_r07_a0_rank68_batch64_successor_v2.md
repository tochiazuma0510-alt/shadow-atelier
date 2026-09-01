# Luna task 463 -- rank-68 dual-anchored batch-64 successor

Role: Luna mechanical implementation only.  Do not change mathematics, run
local production, dispatch GHA, edit workflows, commit, push, or touch files
outside the four outputs below.

The frozen theorem is v415 and the accepted implementation is Task451.  This
task only rebases that exact closed-batch algorithm from the cross-checked
rank-51/eight-record prefix to the cross-checked rank-68/25-record prefix and
uses the already accepted batch cap 64.  It does not widen the registered
candidate universe.

## 1. Required outputs

Create only:

1. `search/d972_r07_a0_dual_anchored_active_batch_v2.py`;
2. `crosscheck/check_d972_r07_a0_dual_anchored_active_batch_v2.py`;
3. `search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v2.g`;
4. `sol/luna_reply_463_r07_a0_rank68_batch64_successor_v2.md`.

## 2. Frozen inputs

Exact-pin the accepted Task451 owners:

```text
producer 13834 ca7fb15e06dd04881146c38d63d93015a9e630fbc334cf15098cbd8a32f22f9b
checker  13725 5c2f76b825bd920245d0200f29ff860ba93a32663ef5db9567bc499a86f7ff8a
driver    2569 6910d38adc56a564b4cd80211bb994de72fd77bf2da6abd8df2df5597ab9a000
```

Use the exact repository checkpoint:

```text
search/certs/d972_r07_a0_actual_tau_free_rank68_checkpoint_v1.json
33015 73ad85624d079d01ecc824ab6adc699c51b0dabfddcc36c0f7d2bd4384f7d5a4
```

Authenticate schema, binding, canonical seal
`d900bbb4f3b69ee66f9c2f4000b169f69a9202091a69fe0bbb8d33c4ae061537`,
rank 68, accepted count 25, round 27, and the exact ordered 25-record prefix.
The v7 continuation checker is available at

```text
crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v7.py
3653 e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1
```

and may be exact-pinned for the frozen checkpoint/prefix authentication.  It
does not replace Task451's checker-side batch replay.

## 3. Exact guarded rebase

Make an exact-byte/hash/cardinality-guarded successor of the Task451 producer
and checker.  Required semantic substitutions are only:

```text
schema/marker/path v1 -> v2
frozen rank51 checkpoint -> frozen rank68 checkpoint
frozen state (51,8,9) -> (68,25,27)
frozen prefix count 8 -> 25
base physical rank 51 -> 68
batch cap default/driver 16 -> 64
```

The maximum is **64 new rises after rank 68**.  Thus all cap and resume
equations use

```text
new_rises = accepted_count - 25 = sum(closed batch row_count)
physical_rank = 68 + new_rises
0 <= new_rises <= 64.
```

Do not accidentally treat the historical 25 rows as part of this new-rise
cap.  A `UNKNOWN_RESOURCE:max_rises` terminal requires exactly 64 new rises,
not total accepted count 64.

Retain unchanged:

- deterministic selector order and registered literal universe;
- full semantic replay of every frozen prefix record;
- one frozen dual per closed batch;
- direct row/scalar/exponent/selector/pivot replay;
- one post-batch canonical dual update;
- closed-batch-only durability and open-batch discard;
- cumulative cap across v2 resume;
- honest RESOURCE allowlist and no NONMEMBER claim.

Do not add actor rebasing, eager stores, closure rebuilds, worker pools,
production fixtures, or a second producer process.

## 4. Checker and driver gates

The checker must replay all 25 frozen records semantically before any v2
batch, not merely compare JSON.  It then independently repeats every
Task451 batch gate and authenticates the v2 durable checkpoint.  Mutation
tests must cover the 25-record prefix, anchor dual, selector, exponent,
pivot, post-batch dual, open-batch rejection, 63-vs-64 max-rise boundary,
and 65-rise rejection.

The driver must require external preamble

```text
D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V2_RUN:=true;;
```

and run one producer with 7,200 seconds, 4,800,000,000 RSS bytes, 64 new
rises, and batch cap 64.  Use fresh v2 artifact/checkpoint/log paths, then
run the independent checker and require its PASS marker.

Run locally only repo-external-cache `py_compile`, load-without-main,
producer fixture, checker self-test, exact transform/hash/cardinality gates,
and static driver/process/cap scans.  Do not run actual A0 production.
Report all physical/generated pins and bounded commands in the reply.

