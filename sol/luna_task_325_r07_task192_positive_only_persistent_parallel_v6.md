# Luna task 325 - task192 positive-only persistent parallel adapter v6

Role: Luna, implementation and mechanical accounting only.  Read all
sections first to last.  Do not run Python, Node, GAP, GHA, workflows, git,
or network.  Preserve v1--v5, all sealed inputs, workflows, and v220.  Edit
only the five versioned outputs named below.

This commission is queued after task324; do not start it concurrently in the
same agent turn unless task324 is completely closed.

## 1. Inputs and sole outputs

Read in full:

- `sol/proof_r07_positive_only_common_word_colgen_v140.md`
- `sol/proof_r07_history_free_positive_common_word_verifier_v265.md`
- `sol/audit_r07_task192_boundary_resume_semantics_v253.md`
- `sol/proof_r07_boundary_adapter_state_and_local_provenance_v255.md`
- `sol/audit_r07_task192_cumulative_pairs_and_persistent_pool_v256.md`
- `sol/sol_reply_319_r07_task311_persistent_parallel_code_performance_audit.md`
- `sol/luna_task_321_r07_task192_persistent_parallel_adapter_v5_rewrite.md`
- `sol/luna_reply_321_r07_task192_persistent_parallel_adapter_v5.md`
- the complete task303/v5 synthetic parallel-kernel quartet;
- the complete task192 cached-v3 producer/checker/driver/fixture;
- task298/v2 driver and reply; and
- the exact staged run-33149728601 checkpoint ZIP and manifest.

Create only:

- `search/d972_r07_normalized_exact_common_word_positive_parallel_v6.py`
- `crosscheck/check_d972_r07_normalized_exact_common_word_positive_parallel_v6.py`
- `search/d972_r07_normalized_exact_common_word_positive_parallel_gha_driver_v6.g`
- `search/certs/d972_r07_normalized_exact_common_word_positive_parallel_selftest_v6_20260828.json`
- `sol/luna_reply_325_r07_task192_positive_only_persistent_parallel_v6.md`

Return `IMPLEMENTED / UNEXECUTED` only if the complete path is present by
inspection.  If an actual owner hook cannot be installed without weakening
the gates, return `BLOCKED / UNEXECUTED` with the first exact code boundary.
No execution is authorized here.

## 2. Correct trust boundary: positive witness only

Task321's retrospective `boundary_epoch_history` requirement is deliberately
removed for this version by v265.  The old checkpoint is authenticated
**discovery state**, not a proof that all prior dual epochs were replayed.

The adapter may emit a mathematical positive terminal only after producing
one literal correction word and one explicit typed PB3/PB4 boundary preimage
which the pinned helper-nonshared task192/v3 checker independently accepts by
direct replay.  Search columns, dual epochs, pair order, and scheduler history
are not evidence for that existential terminal.

Every other exit is only `UNKNOWN_INPUT` or `UNKNOWN_RESOURCE`.  It must set
common-word, separator, negative, finite-common-word, cofinal-lift, fake, and
Ihara flags false.  Never emit or imply `SEPARATOR`, NONMEMBER, exhaustive
zero, completeness, or absence of an ACTIVE column.  A0 remains 0/1 unless
the actual direct positive checker passes.

## 3. Actual persistent correlation hook

Keep the pinned cached-v3 owner responsible for rank, dual, correction
candidate, COMMON construction, and ordinary checkpoint semantics.  Replace
only `BoundaryDescriptorCache.correlation` through an explicit registered
adapter/hook.  Do not fork or modify the v3 source.

Install one persistent Linux worker pool after all input authentication and
before the first boundary epoch.  Reuse it across distinct serially dependent
dual epochs.  Workers receive immutable decoded group/descriptor data once in
their initializer.  At a new epoch send only:

- exact epoch identity and dual SHA-256;
- compact typed nonzero dual support;
- disjoint half-open intervals in the canonical expanded
  descriptor-times-typed-support pair order; and
- a deadline/cancellation token owned by the parent.

Partition expanded pair indices, not only the 104 outer descriptors.  Do not
materialize or pickle a full roster dictionary per epoch.  Cache group
elements/inverses and descriptor templates in workers.  Each worker streams
one bounded shard accumulator plus local lexicographic provenance.  The
serial parent checks exact interval coverage/no overlap, merges in canonical
order over F3, derives the global lexicographic winner, translated sparse row,
and direct scalar, and returns exactly the cached-v3 correlation ABI.

Rank/dual changes remain serial and occur only after a whole epoch merges.
No two dual epochs may run concurrently.  An empty roster returns the exact
v3 empty value.  A short roster uses the same worker protocol or one honest
serial fallback; it must not be rejected.

## 4. Worker failure, deadline, and counters

Use dedicated persistent worker processes and explicit request/result
channels or an equivalently auditable pool.  Do not use a blocking `map` or
unbounded `get`.  The parent must observe a live deadline and worker death,
cancel/discard the entire incomplete epoch, and close/terminate/join every
worker before sealing an exit.  Record the state transition
`started -> closing -> terminating(if needed) -> joined` and require no live
child PID at exit.

Maintain attempted, committed, discarded, and retried pair/epoch counters.
Only a completely merged epoch can be committed to the serial owner.
Historical counters from the v3 checkpoint are never reset.  Charge wall,
RSS including children, expanded pairs, serialization bytes, worker
restarts, and checkpoint bytes live.  No retry loop may be unbounded; one
failed epoch exits typed UNKNOWN rather than silently retrying forever.

On `UNKNOWN_RESOURCE`, bind exactly one sealed last-safe checkpoint usable by
this same adapter.  The checkpoint may retain heuristic discovery columns and
the next clean epoch boundary; it must not claim historical independent
replay.  On `COMMON`, no checkpoint or orphan sidecar may remain.

## 5. Positive terminal and independent checker

On a proposed COMMON, preserve a canonical inner cached-v3 COMMON receipt.
The outer receipt must bind its exact path/basename, bytes, SHA-256,
self-digest, terminal, immutable source pins, and a compact view containing
the literal `c_star`, the exactified word, the independently registered
relators 3/9/12, exponent data, direct all-seven replay, and the explicit
typed boundary coefficient ancestry.

The v6 checker must not import the v6 producer or trust its flags.  For an
actual positive receipt it must authenticate and invoke the pinned existing
helper-nonshared cached-v3 checker exactly once on the inner COMMON receipt,
capture an exact-one full-line PASS terminal, and independently compare the
compact view to the accepted inner object.  The existing checker is allowed
as the independent mathematical verifier; do not copy its producer helpers
into v6.  A fake checker line, changed inner digest, stale path, or accepted
inner receipt with a mismatching outer compact view is fatal.

For a nonpositive receipt, do not invoke the expensive v3 mathematical
checker.  Independently authenticate the outer seal, source/checkpoint pins,
typed reason, resource/counter snapshot, last-safe sidecar when required,
worker cleanup, and all-false claim vector.  This is transport/resource
checking only and must not be labeled mathematical acceptance.

## 6. SELFTEST and mutations

The synthetic fixture must derive F3 scalars independently and cover:

- canonical C17 codec and exact `t*h=g` convention;
- one, short, and empty descriptor/support rosters;
- single-descriptor concentration;
- multi-descriptor cancellation;
- active and no-active epochs;
- lexicographic winner with local provenance;
- at least three distinct serial dual epochs through one real Linux worker
  roster;
- complete interval cover and deterministic merge under at least two worker
  counts;
- live timeout, worker death, partial return, and full cleanup/join; and
- positive-envelope and UNKNOWN_RESOURCE-envelope checking without invoking
  the actual large v3 runtime.

Generate and reject owner-specific, canonical-changing mutations for at
least: wrong dual digest, missing/overlapping interval, changed accumulator,
changed winner provenance, changed direct scalar, cross-epoch result,
partial return accepted, child left alive, counter reset, unbound checkpoint,
changed inner receipt digest, fake v3 checker terminal, compact-view mismatch,
positive claim on resource exit, separator flip, cofinal/fake/Ihara flip,
terminal reseal, and stale output.  Narrow expected reason/stage checks are
required; no broad exception/no-op/wrong-owner rejection counts.

## 7. Performance accounting

The reply must give concrete hot-path bounds for the observed 104 descriptors,
1,188 typed support entries, at most 123,552 expanded pairs in one present-
shape epoch, and approximately 2,896 already elapsed rank epochs.  State
exactly what is resident once, what is sent per epoch, maximum transient
serialization, number of parent scans, provenance lookup complexity, and
process count.  There must be no full-roster encoding per epoch, repeated
group decoding/inversion per pair, linear provenance rescan, flattened
ancestry growth, sleep/poll loop, unbounded history list, or per-epoch pool
creation.

## 8. Driver and final report

The ASCII driver must pin exact producer/checker/fixture identities and every
registered dependency/checkpoint input, stale-reject every v4--v6 owned
output, invoke one v6 producer then one v6 checker, require exact-one terminal
markers and identical payloads, enforce sealed nonempty receipt/verdict/logs
and terminal-appropriate sidecars, and write the sole sentinel last.  Do not
embed a recursive driver self-hash.

The reply must list final bytes/SHA-256, exact import/subprocess graph, source
pins, the owner-hook code point, full mutation ledger, hot-path accounting,
and:

```text
IMPLEMENTATION:                    IMPLEMENTED or BLOCKED
EXECUTION:                         UNEXECUTED
ACTUAL PERSISTENT PRODUCTION:       UNEXECUTED
RETROSPECTIVE EPOCH REPLAY CLAIM:   NONE
ACTUAL A0 COMMON + CHECKER:         0/1
SEPARATOR / NEGATIVE CLAIM:         FORBIDDEN
LIFT / FAKE / IHARA:                NONE
```

`TASK325_R07_TASK192_POSITIVE_ONLY_PERSISTENT_PARALLEL_V6`
