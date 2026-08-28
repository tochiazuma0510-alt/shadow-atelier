# Luna task 321 — task192 persistent parallel adapter v5 rewrite

Role: Luna implementation only.  Do not run Python, Node, GAP, GHA,
network, or git.  This is a fresh architecture after task319 rejected v4.
Parent Sol is the sole execution and git broker.

## 1. Read every controlling file and write exactly five new paths

Read in full:

- `sol/luna_task_311_r07_task192_persistent_parallel_adapter_v1.md`
- `sol/luna_reply_311_r07_task192_persistent_parallel_adapter_v1.md`
- `sol/sol_task_319_r07_task311_persistent_parallel_code_performance_audit.txt`
- `sol/sol_reply_319_r07_task311_persistent_parallel_code_performance_audit.md`
- the SHA-identified v254--v256 papers named in task319's reply;
- the present cached-v3 producer/checker/driver and task303/v5 bundle; and
- all four rejected v4 executable/fixture inputs.

Create exactly:

1. `search/d972_r07_normalized_exact_common_word_cached_parallel_v5.py`
2. `crosscheck/check_d972_r07_normalized_exact_common_word_cached_parallel_v5.py`
3. `search/d972_r07_normalized_exact_common_word_cached_parallel_resume_gha_driver_v2.g`
4. `search/certs/d972_r07_normalized_exact_common_word_cached_parallel_selftest_v2_20260828.json`
5. `sol/luna_reply_321_r07_task192_persistent_parallel_adapter_v5.md`

Edit no v1--v4, checkpoint, workflow, v220, or other path.  If all blockers
cannot be repaired within these paths without changing cached-v3 ownership,
write a precise `BLOCKED` reply rather than an unsafe partial adapter.

## 2. Frozen semantic boundary

Only replace cached-v3 `BoundaryDescriptorCache.correlation`.  Rank, dual,
correction, candidate, COMMON, and ordinary checkpoint ownership remain with
the exact pinned cached-v3 owner.  For every epoch preserve descriptor-outer
and live typed-support insertion order, canonical group elements,
`t=g*h^-1`, direct `t*h=g`, F3 zero deletion, the least
`(block,translation_blob,relator_index)`, winning local provenance,
translated-row reconstruction, direct scalar, and the exact v3 return
shape.

Empty pair rosters must return the exact v3 `None`.  For
`0 < pair_count < worker_count`, use an honest reduced-worker or serial
fallback and return the v3 result; never reject a valid v3 input merely
because it is too small to shard.  Record the physical path truthfully.

## 3. Persistent dedicated workers with deadlines and cleanup

Do not use scheduler-dependent `Pool.map`.  Start a fixed set of dedicated
Linux `fork` workers after the live immutable runtime/descriptor cache is
available.  Give every worker its own request/result channel and stable
worker ID.  Reuse the same healthy PID roster; no epoch may assume that a
generic pool scheduler assigned one task to every PID.

For each atomic epoch:

- publish one compact canonical typed-support buffer and a descriptor-prefix
  index; do not construct `N` expanded dictionaries;
- send each worker only epoch identity and a contiguous expanded-pair
  interval over that prefix index;
- poll all result channels against the remaining cached-v3 wall deadline;
- reject timeout, worker death/replacement, duplicate/missing/overlap/gap,
  stale identity, malformed result, unknown RSS, or partial return before
  merge; and
- on any exceptional exit terminate every live child and join exactly once.

Implement an explicit state machine for `started / closing / terminating /
joined`.  Setting a `closed` flag before a successful join may not suppress
termination or join recovery.

## 4. Honest safe-checkpoint and counter semantics

Charge attempted expanded pairs monotonically before launch.  Retain
separate attempted, committed, discarded, and retried totals; a failed epoch
cannot disappear or be repeated without charge.  Check pair, wall, and
aggregate RSS caps before launch and while waiting.  Account for the parent
and every live child PID, including an idle worker.

Map a semantic worker/protocol fault to the cached-v3 typed input-stop path
and bind the already existing last-safe ordinary v3 checkpoint.  Map an
actual deadline or aggregate resource limit only to its truthful registered
cap.  Do not forge `rss_bytes=limit+1` for an unrelated failure.  Every
nonpositive receipt must bind exactly one authenticated last-safe checkpoint
and its monitor/counter snapshot; remove/reject all unreferenced sidecars.
COMMON retains no checkpoint sidecar.  Historical counters from the staged
checkpoint are never reset.

## 5. Hot-path architecture (performance is load-bearing)

The production epoch may not perform any of task319 F9's repeated whole-
roster work:

1. no materialized expanded-pair dictionary list;
2. no full roster JSON encoding four or eight times;
3. no full roster pickle once per worker;
4. no per-pair decoding of a support element or recomputation of a fixed
   descriptor inverse;
5. no linear rescan of support to find winning provenance;
6. no unbounded in-memory epoch/contributor history; and
7. no parent recomputation of the complete correlation after merge.

Use a compact binary canonical encoding, descriptor prefix sums, cached
descriptor inverses, once-per-epoch decoded support indexes, and O(1) winner
lookup.  Compute each roster/shard/accumulator digest once.  Keep rolling
counters plus a streaming hash-chained transcript file with a registered
byte cap; retain only current/last epoch evidence in RAM.  The transcript
must be sufficient for Section 6's checker but must not contain all
contributors.  State exact asymptotic work, peak transient storage, and the
expected current-shape costs for 104 descriptors, support 1,188, at most
123,552 pairs, and about 2,896 dependent epochs.

## 6. Independent production replay

The checker must not import either producer.  It may authenticate/load only
the cached-v3 checker.  The v5 producer must stream a bounded per-epoch
certificate containing enough compact data for the checker to reconstruct,
from the authenticated v3 receipt/checkpoint and rank/dual history:

- the actual descriptor and typed-support roster in exact order;
- expanded interval cover;
- every shard's sparse F3 partial digest;
- merged accumulator digest and least active key;
- winning `g=t*h` local provenance;
- translated row and direct scalar; and
- attempted/committed/discarded counters and physical PIDs/RSS.

The independent checker must actually rebuild the roster and each shard
accumulator with its own group/echelon helpers and compare those values.  A
self-reported digest/shape is insufficient.  It must also hash the local
checkpoint zip/manifest, cached inputs, current v5 producer, fixture, and
streamed transcript.  One necessary sequential independent replay is
allowed; a second parse/replay of the same history is not.

If reconstructing every production epoch from the authenticated cached-v3
receipt is impossible because the owner does not retain sufficient dual
history, stop with `BLOCKED` and name the exact missing owner field.  Do not
replace it with an unverifiable transcript assertion.

## 7. Correct SELFTEST universe and mutations

Use a tiny canonical finite group codec and exercise the same inverse,
multiplication, serialization, and `t*h=g` path as production.  Do not use
two integer aliases such as 3 and 20 for one mod-17 element.

Use separate cases:

- support concentrated under one descriptor, with enough distinct canonical
  pairs to span multiple worker intervals;
- a multi-descriptor cross-shard cancellation;
- active winner, no-active, nontrivial v3 lex winner, and O(1) local
  provenance; and
- zero and short-roster fallbacks.

Derive expected F3 scalars independently in producer and checker.  Run at
least three distinct dual epochs through one real Linux worker roster.
Inject live timeout/worker death/partial-return/cleanup and failed-counter
cases, in addition to the existing semantic mutations.  No no-op/reseal may
count.  Fix the Python chained comparison by separately comparing the
Boolean flag with `(len(distinct) >= 3)`.

## 8. Driver authentication and exact terminal grammar

The ASCII-only driver must pin the final producer, checker, fixture, every
cached/task303/checkpoint dependency, and the v254--v256 files by actual
names.  It must use one exact SELFTEST/PRODUCTION terminal grammar shared by
checker and driver, with exact-one lines and producer/checker terminal
equality.  Pin the driver externally by the immutable parent commit/workflow
input in the reply; do not invent a recursive self-hash.

Reject stale receipt, verdict, transcript, log, checkpoint, terminal, and
sentinel paths.  Execute producer once then independent checker once.  The
sole sentinel is written last.  All claim flags remain false in SELFTEST and
all non-COMMON production terminals.

## 9. Reply boundary

Report exact identities only after closing the files; no post-reply rewrite
is permitted.  Enumerate F1--F9 one by one with the literal repair location,
hot-path accounting, live cleanup/counter behavior, checker reconstruction,
and mutation reachability.  Mark all execution `UNEXECUTED`, A0 `0/1`, and
declare no lift/fake/Ihara result.  A future independent Sol(max) PASS may
authorize only a GHA SELFTEST.

