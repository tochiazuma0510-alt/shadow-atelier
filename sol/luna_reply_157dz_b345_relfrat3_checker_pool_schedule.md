# Luna reply 157dz — memo-v9 checker pool schedule repaired

## Result

`PASS` (implementation/static/self-test scope).  I created a checker-only v10
successor.  The memo-v9 producer, its `/v9` JSON schema/output, registered 4096
candidate order, mathematical predicate, q3 input, and workflow are unchanged.

The v8 run `32247008986` is not mathematical evidence for or against a lift:
the producer completed all 4096 candidates with
`B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE`, the independent checker passed the
packed outcome replay, and then failed at the old combined aggregate message.
There was no artifact.  The in-flight v9 run `32257890026` inherited the same
checker defect and was cancelled after the static diagnosis; it likewise has no
new mathematical status.

## Exact root cause

Two producer/checker pool schedules differed:

1. Producer v9 builds the base D2 basis, then persistently interns the ordered
   six-element `raw_base_source_key` before BFS.  The checker omitted those six
   source anchors.
2. Producer target probes are candidate transactions and roll back every
   target-prefix pool suffix.  Checker `first_missing()` ran at checkpoint 1
   and each directed round without a rollback, retaining its transient values.

The pivot reductions and packed blocker outcomes can still agree because they
use canonical element bytes and the same pivot order.  The later candidate
transaction checkpoint is nevertheless shifted/polluted, so
`pool_suffix_removed` differs.  That changes the public row and full-record
digest and explains a packed-replay PASS followed by the opaque aggregate
failure.

## Repair

- `replay_pivot_surgery` now receives the independently rebuilt frozen source
  tuple and interns its six entries immediately after `ReplayBasis`
  construction, exactly matching producer order.
- Every `first_missing()` invocation is enclosed in a pool
  checkpoint/`finally` rollback.  Blocker component, immutable bytes, and
  unpacked value are copied before rollback; the basis is not mutated.
- `ReplayPool.rollback` verifies the exact blob-to-ID mapping in reverse suffix
  order and the final checkpoint cardinality.
- The final aggregate equality is still fail-closed but is split into named
  gates: `record_bindings`, `record_bindings_sha256`, and
  `failure_distribution`.  A binding failure reports only the first candidate
  and first differing field, with large values represented by bounded SHA-256
  evidence.
- The v10 driver runs the byte-identical v9 producer and new v10 checker in one
  job.  It uses distinct v10 logs/sentinels, preserves q3 regeneration and
  checker gates, removes stale outputs, and keeps the registered artifact at
  `ci/out/d972_b345_relfrat3_wordexpr_memo_v9.json`.

## Self-test

No GAP, GHA, Git, or full search was run.  The combined lightweight command
was invoked first after the production repair; that run passed, but a
post-run static trace showed the new pool-schedule canary was located in an
inherited helper not called by the active v10 self-test.  I extracted it into
`self_test_pool_schedule()`, connected it to the active path, repinned the
driver, and—under an explicit one-run corrective authorization—ran the same
combined command exactly once more:

```text
python -B search/d972_b345_relfrat3_wordexpr_memo_v9.py --self-test;
python -B search/check_d972_b345_relfrat3_wordexpr_memo_v10.py --self-test
```

Corrective exit code `0`.  Exact final markers:

```text
D972_B345_RELFRAT3_WORDEXPR_MEMO_V9_PRODUCER_SELFTEST_PASS ... source_anchors=6 ... scan=4096 terminals=4
D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_CHECKER_SELFTEST_PASS envelope_entries=20 source_preflight_entries=17 scan_entries=16 selected_entries=10 proof_entries=5 ... source_anchors=6 probe_rollback=1 ...
```

The checker test includes six distinct nonidentity anchors, exact ordered
persistence, an anchor-count mutation, a polluting unscoped probe, and the
repaired transactional probe returning copied evidence with zero persistent
pool growth.

## Frozen files

| file | bytes | SHA-256 |
|---|---:|---|
| `search/check_d972_b345_relfrat3_wordexpr_memo_v10.py` | 410844 | `264258dcb945401e3db10ecd4fedd7a8dd79a8d7b0f31dbc0cfbe643537eac2d` |
| `search/d972_b345_relfrat3_wordexpr_memo_gha_driver_v10.g` | 16053 | `a5e9bdb34d85669a6221e4b0fa8e4c3af0aee343aade59fde52013d05753afc0` |
| `sol/luna_task_157dz_b345_relfrat3_checker_pool_schedule.md` | 3540 | `65a5ed3e0d7963f64bb3731badcbbf9294ec5710fd5a035a3670db277c3f74be` |

Frozen dependency confirmations:

- v9 producer: `7dede323c3c52bc7cf7d99af6d542b3683823879a4bb3e340aca8ce53dcf196f`
  (392086 bytes; unchanged)
- v9 checker retained as receipt provenance:
  `d5695fdb5f56cdc23c012a09488786efacb16a1c4ee85f2297dc66c045092f4d`
  (403737 bytes; unchanged)

No negative/obstruction/B4-A/B conclusion is added by this transport/checker
repair.

`B345_RELFRAT3_WORDEXPR_MEMO_V10_READY_FOR_GHA`
