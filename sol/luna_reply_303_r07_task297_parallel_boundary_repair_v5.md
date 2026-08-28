# Luna reply 303 - task297 fixed-dual parallel boundary repair v5

Status: **IMPLEMENTED STATICALLY / UNEXECUTED**.

Only the five commissioned v5 paths were created. Task192 v3, rejected v4,
the sealed checkpoint, workflows, and all other paths were left unchanged.
No Python, GAP, GHA, network, or git command was executed.

## File identities

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_normalized_exact_common_word_parallel_v5.py` | 39234 | `19a2970fcf072c25c606d0305fd999c8481353e0be20879de4be2aa26f6fb90c` |
| `crosscheck/check_d972_r07_normalized_exact_common_word_parallel_v5.py` | 32486 | `530d67c854017a538fa2185b8bc5c48834a785f5bd6db38452db3551695cf1df` |
| `search/d972_r07_normalized_exact_common_word_parallel_gha_driver_v5.g` | 7971 | `0ac1b26d1844fdc16cc2701c536f50fd5415a7ef2479e030ebde96af79af4902` |
| `search/certs/d972_r07_normalized_exact_common_word_parallel_selftest_v5_20260828.json` | 1195 | `4d481ba84e3c452c79f344e66a0eea5322ec8b64c15a81f1a290c22ce18e3fc9` |
| `sol/luna_reply_303_r07_task297_parallel_boundary_repair_v5.md` | self-referential | intentionally not self-pinned |

The GAP driver is ASCII-only and pins the first three v5 inputs by the exact
byte/SHA pairs above.

It also retains the immutable v3 pins:

```text
producer  193704  f27b4971351832b8730fb8cce4e782e893a958dfb850203cc735c7bc3aa31f37
checker   154009  dfc8cbbd96a1da45f15e01607ed343b66a78a7201f4a80952fba33aaeb361e10
driver     11548  2f7ff7b459e46d014268907ff5ba5f03c035836e8f8df79a2c5f4cdc3b75351d
fixture      276  c49f434ad3daf1cc661ba45563dbb9557d436f91dca78c8ee0f47ed70332da12
```

## Fixed-dual parallel kernel

The v5 worker entry receives one frozen dual, the complete ordered descriptor
roster, and one deterministic contiguous interval. It uses Linux
`multiprocessing.get_context("fork")`; there is no thread or in-process
worker substitute.

Each primitive shard record contains and binds:

- exact `start`, `stop`, `count`, and interval/slice digest;
- frozen-dual and complete-descriptor digests;
- its mod-3 partial accumulator and ordered contributor records;
- explicit `worker_failed=false`; and
- a result digest over every preceding shard field.

The parent requires the returned shard list itself to be in exact interval
order; it does not sort a malformed roster into acceptance. Every shard is
recomputed directly from its descriptor slice before merge. The merge adds
partials in F3, deletes zero totals, concatenates contributors in global pair
order, and chooses
`(block, translation_blob, relator_index)`. It then recomputes the selected
scalar from the full ordered descriptor roster and requires equality with
the merged scalar and the separately computed serial projection.

The independent checker imports no producer code. It has its own descriptor,
serial, interval, shard, F3 merge, lexicographic selection, and direct-scalar
replay. Its shard loop is inside each of worker counts 2, 3, and 4, including
the per-shard worker-failure gate.

Adaptive ranks, dual changes, candidate words, and actual v3 resume state are
not worker inputs and are not implemented by this SELFTEST kernel.

## Four fixture cases

The byte-pinned fixture names exactly four cases and separately records two
epoch runs. The statically encoded serial outcomes are:

1. `active_two_shards`: selected key `[1,2,"a"]`, scalar 2. Its
   contributors are pair indices 1 and 5, on opposite sides of the actual
   w=2 cut at 4.
2. `cancel_across_shards`: key `[1,2,"a"]` receives coefficients 1 and 2
   at pair indices 2 and 5 and cancels across the w=2 cut. The surviving
   selected key is `[2,2,"c"]`, scalar 1.
3. `nontrivial_lex_winner`: both `[1,2,"a"]` and `[1,1,"b"]` are
   active. Translation `"a"` wins before the smaller relator index of the
   `"b"` key, so the selected key is `[1,2,"a"]`, scalar 1.
4. `no_active_key`: the complete accumulator is empty, selected key is
   null, and scalar is 0.

Each case constructs genuine process runs for worker counts 2, 3, and 4 and
compares the complete result with its serial oracle.

Two consecutive epoch runs use the same descriptor roster but different
frozen duals (all coefficients 1, then all coefficients 2). Each epoch is
checked against its own serial result; epoch indices, dual/result digests,
second-epoch shard digests, and an isolation digest are all bound. The
SELFTEST metadata truthfully accounts for 14 batches, 112 evaluated pairs,
and `36 + 2 * driver_worker_count` completed shards.

These are code/fixture contracts, not observed runtime outcomes.

## Non-circular mutation controls

The producer semantic validator checks the sealed receipt but deliberately
does not inspect aggregate mutation counts. For each of the 20 owners, the
producer:

1. deep-copies the baseline;
2. mutates the actual load-bearing semantic field;
3. recomputes the semantic input digest and receipt seal;
4. requires a changed canonical semantic-effect digest;
5. obtains that mutant's individual semantic rejection; and only then
6. attaches and validates the aggregate 20/20 summary.

The repaired worker-failure mutation changes an actual shard's
`worker_failed` field. The direct-scalar mutation adds 1 modulo 3 rather
than assigning a baseline literal. Interval, count, partial, contributor,
cover, merge, lex winner, epoch, incomplete-checkpoint, single-process, and
worker-range owners all mutate their corresponding fields.

The independent checker builds its own 20 mutants, recomputes their semantic
digests/seals, and requires all 20 individual rejections without using the
producer's attempted/rejected claim. Its verdict records its own effect
digests.

```text
producer mutation gates implemented:       20/20 required
independent checker gates implemented:      20/20 required
producer mutations actually executed here: 0/20
checker mutations actually executed here:  0/20
```

No SELFTEST pass is claimed until the parent executes both sides.

## Driver and terminal boundary

The driver creates one `set -euo pipefail` shell, discovers `nproc`,
chooses `min(nproc,4)`, requires 2..4, and records the chosen worker count.
It rejects all stale receipt, verdict, log, shell, and sentinel paths.

SELFTEST producer and independent checker always run first, including before
the optional PRODUCTION branch. The required SELFTEST terminals are exactly:

```text
R07_NORMALIZED_EXACT_COMMON_WORD_PARALLEL_V5_PRODUCER_TERMINAL PASS
R07_NORMALIZED_EXACT_COMMON_WORD_PARALLEL_V5_CHECKER_TERMINAL PASS
```

Each prefix must occur exactly once, the suffixes must be exactly equal, the
receipt/verdict/log files must be nonempty, and only then may the one exact
sentinel be written.

PRODUCTION requires an explicit existing relative `ci/in/*` resume
candidate, but no v3-resume authentication/semantic adapter is commissioned
here. It therefore emits only the sealed, independently checked terminal:

```text
UNKNOWN_INPUT:resume_adapter_not_commissioned
```

It cannot enter a boundary search or emit a positive terminal. A later
versioned commission must authenticate and project actual v3 resume state
before this kernel can be connected to the adaptive serial rank loop.

## Status boundary

```text
V5 IMPLEMENTATION:              COMPLETE STATICALLY
EXECUTION:                      UNEXECUTED
SELFTEST PRODUCER/CHECKER PASS: 0/2 ACTUAL
A0 ACTUAL:                      0/1
PRODUCTION V3-RESUME ADAPTER:   NOT COMMISSIONED
COMMON WORD:                    NOT OBTAINED
COMPATIBLE LIFT:                NOT OBTAINED
FAKE CERTIFICATE:               NOT OBTAINED
IHARA WITNESS:                  NOT OBTAINED
```

`TASK303_R07_TASK297_PARALLEL_BOUNDARY_REPAIR_V5_UNEXECUTED`
