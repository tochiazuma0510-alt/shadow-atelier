# Luna reply 311 — task192 persistent parallel adapter v1

## Scope and execution status

Implemented exactly the five authorized new paths from the task letter.  No
existing producer/checker, task303/v5 input, checkpoint input, workflow, or
other path was edited by this commission.  Python, Node, GAP, GHA, network,
and git execution were all **UNEXECUTED**; therefore this reply records no
runtime PASS, COMMON, or verified mathematical result.

The mathematical boundary remains the pinned cached-v3 owner: only the
fixed-dual `BoundaryDescriptorCache.correlation` call is adapted.  Rank,
dual updates, correction, candidate words, COMMON construction, and the v3
checkpoint writer remain delegated to that owner.  The adapter uses atomic
full epochs; a resource stop can retain only the ordinary safe v3 checkpoint
and restarts the current epoch.  A0 actual is `0/1` (undetermined here), and
there is no lift, fake, or Ihara result.

## Authorized paths and final identities

The four code/fixture identities are:

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_normalized_exact_common_word_cached_parallel_v4.py` | 74127 | `7ac78c640a0527b0c103339f898c21ee613f39c5c5efff3a0f839da43c5cc4b9` |
| `crosscheck/check_d972_r07_normalized_exact_common_word_cached_parallel_v4.py` | 50557 | `ba00c6fb8b9602304c2785086c5cbeb331d90d8f32124accc5b33b5a0252ae03` |
| `search/d972_r07_normalized_exact_common_word_cached_parallel_resume_gha_driver_v1.g` | 9203 | `fe870f5f0d391f21e84922c4c34d20263d9821a3297252802692338115214823` |
| `search/certs/d972_r07_normalized_exact_common_word_cached_parallel_selftest_v1_20260828.json` | 1313 | `7def0fafacf6703b16f8a40933edc0208da3077d8c59a9e36307f16cf2ef4c19` |

The fifth authorized path is this reply file; its final filesystem identity
is reported by the parent after this file is written.

## Adapter contract

- Expanded descriptor-support pairs are built in descriptor-outer order and
  live typed-support insertion order.  Each worker computes `t=g*h^-1`,
  checks `t*h=g`, and accumulates sparse F3 coefficients with zero deletion.
- Parent merge consumes exact contiguous intervals in order, selects exactly
  `(block, translation_blob, relator_index)`, checks the direct scalar, and
  reconstructs only the winning local provenance through `g=t*h`.  An empty
  active map returns `None` with scalar zero.
- The runtime adapter emits the unchanged v3 row/provenance shape.  Its outer
  receipt records physical `single_process=false`, persistent-pool counts and
  PID roster, epoch identities/digests, expanded-pair counts, resource
  accounting, and base receipt/checkpoint digests.  The inner v3
  `single_process` value is labeled legacy logical metadata.
- All claim flags (`common_word`, `separator`, `finite_common_word`,
  `cofinal_lift`, `fake`, `ihara_witness`) remain false.

## Performance invariants and expected hot path

- One Linux `fork` pool is created after the authenticated runtime cache is
  available and reused across epochs; it is closed/joined once on normal or
  exceptional exit.  There is no epoch-level pool recreation, lock, or
  sequential worker wait.
- Tasks are one contiguous interval per worker and carry only that worker's
  pair slice plus binding digests; the full roster is not repeatedly pickled
  into each task.  Runtime workers do not retain all contributor history:
  they return sparse partials, while the parent reconstructs only the winning
  contributors.  The selftest alone retains contributor records for its
  exact mutation/parity audit.
- The parent performs sparse F3 merge and one selected direct-row/scalar gate;
  it does not rerun full correlation.  Descriptors are published once per
  cache, support is projected once per epoch, no all-epoch history is placed
  in the compact outer receipt, and no full-record sort is used for runtime
  contributor history.  The bounded transient hot-path payload is each
  epoch's pair slices plus sparse shard partials; the likely cost center is
  worker-side `t=g*h^-1`/F3 accumulation followed by the ordered parent merge
  and selected-row direct check.
- Checkpoint input is authenticated once at the adapter boundary with the
  task298 one-member zip/manifest guard.  Workers never reread checkpoint,
  monitor, rank, dual, or candidate state.

## Inputs read in full and pinned

The task letter and directly referenced v254, v255, v256, task298, task303,
and task310 acceptance materials were read in full.  The authenticated input
pins embedded by the new producer/driver are:

```text
cached-v3 producer  193704  f27b4971351832b8730fb8cce4e782e893a958dfb850203cc735c7bc3aa31f37
cached-v3 checker   154009  dfc8cbbd96a1da45f15e01607ed343b66a78a7201f4a80952fba33aaeb361e10
cached-v3 driver     11548  2f7ff7b459e46d014268907ff5ba5f03c035836e8f8df79a2c5f4cdc3b75351d
cached-v3 fixture      276  c49f434ad3daf1cc661ba45563dbb9557d436f91dca78c8ee0f47ed70332da12
task303/v5 producer  39234  19a2970fcf072c25c606d0305fd999c8481353e0be20879de4be2aa26f6fb90c
task303/v5 checker   32486  530d67c854017a538fa2185b8bc5c48834a785f5bd6db38452db3551695cf1df
task303/v5 driver     7971  0ac1b26d1844fdc16cc2701c536f50fd5415a7ef2479e030ebde96af79af4902
task303/v5 fixture    1195  4d481ba84e3c452c79f344e66a0eea5322ec8b64c15a81f1a290c22ce18e3fc9
v254                  6195  e9fc7a69525200e8e1c0e8152652229227877ba923378ade8afa199c4f4ee1a0
v255                  8814  06c93c46b48b681e0316d302058b72bc0b76fe9d12888cde3f7e45dc3a93ffa0
v256                  4790  f5a0c6e625e5113e4213b62762267fc9a5437cafd9f9751e603b055c549c1251
task298 driver       19682  169da7aa149d68907abb435f380b9ec2994c2bc285c6a17f13431614a388f5ad
checkpoint zip     5001811  f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566
checkpoint manifest   1328  6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302
checkpoint member 86368039  c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab
```

Selftest and production execution, independent mutation replay, and GHA
driver execution remain **UNEXECUTED** for the parent Sol(max) audit.
