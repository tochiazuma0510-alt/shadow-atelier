# Sol(max) reply 308 — task303 v5 independent static code audit

## Verdict

**PASS (static source audit only).**  The five task303/v5 deliverables satisfy
the commissioned fixed-dual process-parallel **SELFTEST-kernel** contract.
The deterministic task300/v4 failures have been removed.  This verdict does
not accept, require, or imply an authenticated production adapter: task303
explicitly leaves that adapter to a separate commission and keeps PRODUCTION
fail-closed (`luna_task_303`, lines 17--20).

No Python, Node, GAP, GHA, workflow, network, or git command was run.  Neither
the producer nor the checker was executed.  All case values and control-flow
claims below are static source/fixture deductions.  Thus:

```text
EXECUTION:                         UNEXECUTED
SELFTEST PRODUCER/CHECKER ACTUAL:  0/2
A0 ACTUAL:                         0/1
FAKE CONCLUSION:                   NONE
IHARA CONCLUSION:                  NONE
```

## 1. Scope, paths, ASCII, and pins — PASS

The exact five commissioned path names in task303 lines 9--15 are the only
matching task303 parallel-v5 deliverables found:

1. `search/d972_r07_normalized_exact_common_word_parallel_v5.py`
2. `crosscheck/check_d972_r07_normalized_exact_common_word_parallel_v5.py`
3. `search/d972_r07_normalized_exact_common_word_parallel_gha_driver_v5.g`
4. `search/certs/d972_r07_normalized_exact_common_word_parallel_selftest_v5_20260828.json`
5. `sol/luna_reply_303_r07_task297_parallel_boundary_repair_v5.md`

The driver contains zero bytes above ASCII 127, satisfying task303 line 18.
Its current-input table and pin loop are at driver lines 22--26 and 34--59.
Independent read-only byte/SHA recomputation gives:

| v5 path | bytes | SHA-256 | audit |
|---|---:|---|---|
| producer | 39234 | `19a2970fcf072c25c606d0305fd999c8481353e0be20879de4be2aa26f6fb90c` | matches driver line 23 and reply line 13 |
| checker | 32486 | `530d67c854017a538fa2185b8bc5c48834a785f5bd6db38452db3551695cf1df` | matches driver line 24 and reply line 14 |
| driver | 7971 | `0ac1b26d1844fdc16cc2701c536f50fd5415a7ef2479e030ebde96af79af4902` | matches reply line 15 |
| fixture | 1195 | `4d481ba84e3c452c79f344e66a0eea5322ec8b64c15a81f1a290c22ce18e3fc9` | matches driver line 25 and reply line 16 |
| task303 reply | 7662 | `419cb8e385903fc419cfdab878de315498940a3120a5b62482c49ac735fe0d09` | external audit identity; reply line 17 correctly avoids a self-pin |

The four immutable v3 identities in driver lines 27--32 also match their
current bytes exactly:

| v3 input | bytes | SHA-256 |
|---|---:|---|
| producer | 193704 | `f27b4971351832b8730fb8cce4e782e893a958dfb850203cc735c7bc3aa31f37` |
| checker | 154009 | `dfc8cbbd96a1da45f15e01607ed343b66a78a7201f4a80952fba33aaeb361e10` |
| driver | 11548 | `2f7ff7b459e46d014268907ff5ba5f03c035836e8f8df79a2c5f4cdc3b75351d` |
| fixture | 276 | `c49f434ad3daf1cc661ba45563dbb9557d436f91dca78c8ee0f47ed70332da12` |

For the task300 regression boundary, all five rejected v4 paths still have
the exact byte/SHA identities recorded in task300 lines 19--23.  No git
history assertion is made because this commission forbids git; the pinned
v3/v4 byte identities and the exact v5 path roster are the available static
scope evidence.

## 2. Exact repaired map/reduce contract — PASS

### 2.1 Complete ordered cover and real process workers

- Producer lines 225--231 compute the deterministic half-open intervals
  `[w*N/s,(w+1)*N/s)`.  Producer lines 355--369 require the returned roster,
  without sorting it, to equal that exact ordered cover before replay and
  merge.  This is a complete, disjoint, contiguous cover.
- Producer lines 432--442 explicitly obtain the Linux `fork` multiprocessing
  context, construct one task per interval, and call `Pool.map`.  This is a
  process pool, not a thread pool or an in-process worker loop.  Adaptive
  ranks, dual changes, and candidate-word logic do not occur in this worker
  path, as required by task303 lines 41--43 and by v254 lines 151--162.

### 2.2 Every shard field is bound and directly replayed

Producer lines 61--72 declare the exact shard schema.  Lines 288--301 record
`start`, `stop`, `count`, interval digest, frozen-dual digest, full-descriptor
digest, sparse F3 partial, ordered contributors, explicit
`worker_failed=False`, and a digest over the complete shard body.  Lines
309--313 reject any shape difference or worker failure and require equality
with a fresh `shard_record` recomputation from the assigned descriptor slice.

The merge consumes shards in expected start order (producer lines 355--373),
sums modulo three and deletes zero cancellations (lines 247--256), preserves
contributor order by start-ordered concatenation (lines 368--375), and checks
the returned total count (line 377).  This implements the provenance order in
v254 lines 96--99 as well as task303 items 3--5.

### 2.3 Exact winner order and full direct scalar

The public key is stored as `(block, relator_index, translation_blob)` at
producer lines 139--144, while the winner comparison at lines 316--322 is
exactly `(block, translation_blob, relator_index)`.  Thus storage order is not
being confused with the pinned v3 comparison order.

Producer lines 325--336 rescan the complete ordered descriptor roster for the
selected key.  Lines 378--405 require the merged scalar, this direct scalar,
and the independently built serial projection to agree, with a nonzero scalar
for an active key and zero only for `None`.  This is precisely the single
frozen-epoch equality of v254 Theorem 2.1 (v254 lines 65--94); it makes no
claim about a later adaptive epoch or an actual PB3/PB4 production row.

### 2.4 Independent checker and all worker counts

The checker imports only standard-library modules (checker lines 5--9) and
does not import the producer.  It separately implements dual/descriptor
inspection (lines 137--202), interval and slice replay (205--282), serial
accumulation/direct scalar (285--336), F3 reduction (339--405), and full run
replay (408--416).

Most importantly for the task300 dedent regression, checker lines 525--557
place `audit_run` and the per-shard `worker_failed is False` gate inside the
loop over worker counts 2, 3, and 4.  All shard metadata and contents are
therefore replayed for every count, not only for the final `w=4` value.

## 3. Four baseline cases and two epochs — PASS

The fixture contains exactly the four names in task303 lines 63--68, declares
`epoch_runs: 2`, and separately declares worker counts `[2,3,4]`.  Producer
lines 520--551 reconstruct that exact byte-pinned contract; checker lines
419--466 reconstruct it independently.

Static evaluation of producer lines 467--517 gives the reply's four values:

1. `active_two_shards`: `[1,2,"a"]` has nonzero contributors at indices 1
   and 5.  The actual two-worker cut is 4, so it genuinely crosses both
   shards; its scalar is `1+1=2`.  All lexicographically earlier candidates
   cancel.  Producer lines 583--592 and checker lines 485--492 enforce the
   same fact.
2. `cancel_across_shards`: `[1,2,"a"]` has coefficients 1 and 2 at indices
   2 and 5 and cancels across cut 4.  `[2,2,"c"]` remains with scalar 1.
   Producer lines 593--607 and checker lines 493--505 enforce both cancellation
   and cut crossing.
3. `nontrivial_lex_winner`: both `[1,2,"a"]` and `[1,1,"b"]` are active.
   Translation `a` wins under `(block, translation, relator)` even though its
   relator index is larger.  Producer lines 608--617 and checker lines
   506--513 make that nontrivial ordering load-bearing.
4. `no_active_key`: all four keys cancel, leaving `{}`, `None`, and scalar 0;
   producer lines 618--626 and checker lines 514--520 require all three.

Producer lines 631--654 run every case at worker counts 2, 3, and 4 and bind
each to the serial oracle.  The two consecutive epoch records at lines
661--690 use the same descriptor roster with distinct all-1 and all-2 frozen
duals.  Each run is separately compared with its own serial value.  Producer
lines 759--806 and checker lines 564--605 bind order `[1,2]`, distinct duals
and serial states, complete run replay, the second epoch's shard dual digests,
and the isolation digest.  This is a SELFTEST state-isolation claim only.

The monitor arithmetic is internally exact: four cases times three worker
counts give 12 completed batches, 96 pair evaluations, and
`4*(2+3+4)=36` shards; the two eight-pair epoch runs add two batches, 16 pair
evaluations, and `2*driver_worker_count` shards.  Hence producer lines
710--724 and checker lines 608--622 correctly require 14 batches, 112 pairs,
and `36 + 2*driver_worker_count` shards.  They explicitly make no production
RSS claim.

## 4. Non-circular 20-owner controls — PASS

The producer's 20-name roster is lines 31--52.  The key repair is real:

- `semantic_payload` excludes the aggregate mutation summary (producer lines
  90--105 and 693--700), and `validate_semantics` only requires a placeholder
  dictionary at line 851.  It does not inspect attempted/rejected counts.
- For each owner, lines 986--1012 deep-copy the already accepted baseline,
  apply the mutation, reseal it, require its semantic-effect digest to differ,
  and obtain that mutant's individual semantic rejection.
- Only after those verdicts return do lines 1078--1086 attach the 20/20
  summary, reseal, and call `validate_final`; lines 1015--1046 check exact
  names, counts, roster length, changed digests, and rejection flags.

This removes task300's common unfinished-summary rejection.  It also removes
the two named no-op defects: `worker_failure_accepted` changes an actual shard
field and reseals it (producer lines 961--965), while validation reads that
field for every run through lines 309--313 and 749--755.  The direct scalar is
changed by `+1 mod 3`, a guaranteed nonzero delta (lines 949--951), rather
than assigned its baseline literal.

All requested semantic owners have a direct source mutation and a direct
validation dependency: cover/cardinality/order at lines 877--918, input
coefficient/key at 919--923, contributor/partial/merge at 924--941,
winner/scalar/count at 942--957, and epoch/worker failure/checkpoint/process/
worker range at 958--977.  The baseline is accepted before mutation generation
(lines 1076--1078), so a mutant cannot be credited merely because the base
receipt was already invalid.

The checker independently constructs its own mutations at lines 707--815 and
runs the same non-no-op/reseal/individual-rejection discipline at lines
822--848.  It does not trust the producer's attempted/rejected summary; its
own exact 20/20 count gates are lines 934--955.  The checker worker-failure
mutation changes its actual w=2 shard (lines 797--801), while the ordinary
checker replay inspects every shard of every worker count (lines 550--554).

## 5. Driver, terminals, and fail-closed boundary — PASS

- The pin function checks nonempty bytes, exact length, and SHA, and runs over
  all current and immutable-v3 inputs before shell creation (driver lines
  34--59).
- Lines 49--64 reject duplicate or stale receipt, verdict, log, shell, and
  sentinel paths.
- Lines 75--86 generate one shell beginning with `set -euo pipefail`, compute
  `min(nproc,4)`, require 2 through 4 workers, and record the selected count.
- SELFTEST producer and checker always run first (lines 88--117).  The driver
  requires exactly one standalone producer PASS marker, one producer terminal,
  one checker PASS marker, one checker terminal, exact PASS terminal lines,
  equal terminal suffixes, and nonempty receipt/verdict/log files.
- Only after those gates, and after the optional fail-closed PRODUCTION branch,
  do lines 162--171 write and reread the exact sentinel.

The production path at producer lines 1090--1128 emits a sealed
`UNKNOWN_INPUT` stop and never enters boundary correlation.  Checker lines
851--893 independently check that stop envelope.  Driver lines 119--160 first
require an explicit existing relative `ci/in/*` candidate and then require the
exact producer/checker terminal
`UNKNOWN_INPUT:resume_adapter_not_commissioned`.  This is deliberately not
resume authentication and not an A0 adapter; under the task303 scope it is the
required fail-closed boundary, not a rejection reason.

## 6. Reply accuracy and mathematical boundary — PASS

The file identities and immutable pins in task303 reply lines 9--29 match the
recomputed values above.  Its process/shard/merge description (lines 31--61),
four case deductions (63--90), non-circular controls (92--123), and driver
terminal description (125--153) agree with the cited source paths.  It
correctly labels all of them code/fixture contracts rather than observed
runtime outcomes.

The final boundary at reply lines 155--169 is also exact: implementation is
static and unexecuted; producer/checker actual is 0/2; A0 actual is 0/1; the
production v3-resume adapter is not commissioned; and there is no COMMON
word, compatible lift, fake certificate, or Ihara witness.  This audit does
not promote the v254 paper theorem to Lean-verified status and makes no new
mathematical conclusion.

```text
TASK303/V5 STATIC CODE AUDIT:              PASS
FIXED-DUAL PROCESS MAP/REDUCE SOURCE:       PASS STATICALLY
FOUR CASES / WORKERS 2,3,4 / TWO EPOCHS:  PASS STATICALLY
PRODUCER NON-CIRCULAR MUTATIONS:           20/20 REQUIRED, 0/20 ACTUAL
INDEPENDENT CHECKER MUTATIONS:             20/20 REQUIRED, 0/20 ACTUAL
AUTHENTICATED PRODUCTION ADAPTER:          OUT OF SCOPE / NOT COMMISSIONED
EXECUTION:                                 UNEXECUTED
A0 ACTUAL:                                 0/1
FAKE / IHARA:                              NO CONCLUSION
```

`TASK308_R07_TASK303_V5_SOLMAX_CODE_AUDIT_PASS_UNEXECUTED`
