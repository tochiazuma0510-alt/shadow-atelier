# Luna task 311 — task192 persistent-process production adapter v1

Role: Luna implementation only.  Mathematical contracts are fixed by
v254--v256 and task310.  Do not run Python, Node, GAP, GHA, network, or git;
parent Sol is the only execution and git broker.

## 1. Exact scope

Create exactly five new paths:

1. `search/d972_r07_normalized_exact_common_word_cached_parallel_v4.py`
2. `crosscheck/check_d972_r07_normalized_exact_common_word_cached_parallel_v4.py`
3. `search/d972_r07_normalized_exact_common_word_cached_parallel_resume_gha_driver_v1.g`
4. `search/certs/d972_r07_normalized_exact_common_word_cached_parallel_selftest_v1_20260828.json`
5. `sol/luna_reply_311_r07_task192_persistent_parallel_adapter_v1.md`

Do not modify any v1--v3 producer/checker, task303/v5 file, checkpoint input,
workflow, or other path.  The GAP driver is ASCII-only.  Production must use
the authenticated task192 checkpoint already staged at the two `ci/in/`
paths used by task298/v2.

Pin exact bytes/SHA for the live cached-v3 producer/checker/driver/fixture,
all four task303/v5 code inputs, the checkpoint zip/manifest/raw member, and:

```text
v254 6195 e9fc7a69525200e8e1c0e8152652229227877ba923378ade8afa199c4f4ee1a0
v255 8814 06c93c46b48b681e0316d302058b72bc0b76fe9d12888cde3f7e45dc3a93ffa0
v256 4790 f5a0c6e625e5113e4213b62762267fc9a5437cafd9f9751e603b055c549c1251
```

## 2. Atomic-full-epoch adapter

Implement the first permitted v255 production mode: every fixed-dual epoch
is atomic.  Mid-epoch cursor/prefix serialization is not required in v1.  A
resource stop retains the last ordinary safe v3 checkpoint and restarts only
that current epoch.  Never claim a cursor that was not committed.

Replace only the cached-v3 `BoundaryDescriptorCache.correlation` call.  The
rank owner, rank addition, dual update, correction oracle, candidate words,
COMMON construction, and checkpoint firewall remain the pinned serial-v3
owners.

For every epoch:

- build the exact v3 global roster in descriptor outer order and the live
  typed dual-support insertion order;
- partition **expanded descriptor-support pair indices**, not the 104 outer
  descriptors (v256 is load-bearing here);
- compute `t=g*h^-1`, check `t*h=g`, and sum sparse coefficients over F3;
- merge shards in interval order, delete zeros, select exactly
  `(block, translation_blob, relator_index)`, reconstruct only the winning
  contributors locally via `g=t*h` as proved in v255, rebuild the translated
  row, and check the exact direct scalar;
- return exactly the v3 row/provenance object to the unchanged serial owner;
  `None` must agree with an empty active set.

## 3. Persistent Linux process pool

Creating a fresh pool inside each correlation is forbidden.  Create one Linux
`fork` process pool after the authenticated runtime/cache is available, reuse
the same worker PIDs across at least three successive distinct dual epochs,
and close/join it exactly once on every normal or exceptional exit.

Workers may inherit immutable runtime/descriptor/group data through `fork`.
Every task must bind epoch digest, full pair-roster digest, interval start/
stop/count, and worker identity.  Workers must not mutate rank, dual, cache,
monitor, checkpoint, or candidate state.  A worker exception, missing shard,
PID replacement, stale epoch, partial return, or uncertain resource state is
a typed fail-closed stop and cannot be merged.

The parent checks wall time before launch and after return.  Record parent and
every child peak RSS and enforce an explicit aggregate policy; do not report
the legacy inner v3 `single_process=true` as physical execution truth.

## 4. Honest outer receipt/checkpoint boundary

The pinned v3 receipt/checkpoint may be retained as an inner **serial logical
projection**, but the v4 outer envelope is authoritative for physical
execution.  It must explicitly record:

- `single_process=false`, persistent pool creation/close counts, worker count
  and stable PID roster, epoch count/digests, expanded-pair counts, aggregate
  resource accounting, and base-receipt/checkpoint digests;
- that any inner `single_process=true` field is legacy logical metadata and
  not a physical claim;
- exact terminal equality with the inner v3 terminal; and
- false fake/Ihara/cofinal claims unless an independently accepted COMMON
  receipt later justifies only the finite A0 statement.

On UNKNOWN_RESOURCE, reference a sealed last-safe checkpoint usable by this
same adapter.  On COMMON, retain no unreferenced checkpoint sidecar.  Preserve
the task298 guarded single-member extraction and exact source limits
(`seconds=10800`, boundary pairs 8,000,000, and the remaining registered
limits); do not silently reset historical counters.

## 5. Independent checker and SELFTEST

The checker must not import this producer or task303 producer.  It may load
the pinned v3 **checker** under an authenticated unique module name, and must
independently validate the outer seal, inner receipt/checkpoint digest and
terminal, physical process/resource truth, pair-roster ordering, shard cover,
F3 merge, v3 winner order, local winner-provenance reconstruction, and no
stale epoch.

SELFTEST must execute real Linux processes and include at least:

- three consecutive distinct dual epochs with exactly one pool creation,
  stable at-least-two PID roster, and exactly one close/join;
- typed support concentrated under one outer descriptor so descriptor-only
  sharding would fail, while expanded-pair sharding uses multiple workers;
- active winner, cross-shard cancellation, no-active, nontrivial v3 lex
  winner, and local-provenance cases;
- worker failure, stale epoch, PID replacement, missing/overlapping/gapped
  shard, wrong roster/order/digest/partial/merge/winner/direct scalar, false
  process flag, and dishonest RSS mutations;
- independent checker mutations whose no-op/reseal preconditions cannot be
  counted as semantic rejections; and
- exact parallel-versus-serial parity for every case/epoch.

## 6. Driver and reply

The driver selects `min(nproc,4)` with at least two workers; pins everything;
rejects stale outputs; executes producer then helper-nonshared checker;
requires exact-one terminals and exact terminal equality; requires nonempty
receipt/verdict/log/checkpoint according to terminal; and writes one sentinel
only after all gates.  It supports explicit `SELFTEST` and `PRODUCTION`
modes without editing a workflow.

Report final identities and mark all execution `UNEXECUTED`.  Keep A0 actual
0/1 and declare no lift, fake, or Ihara result.  This commission implements
the adapter; parent Sol performs Sol(max) audit and GHA execution.

