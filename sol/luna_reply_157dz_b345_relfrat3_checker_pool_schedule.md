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

## Production GHA record

The repaired v10 checker was dispatched by the parent broker and the full job
completed successfully:

- run: `32261068150`
- URL: `https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/32261068150`
- commit: `3553c18011d40056dd2e26623aeec3ba72a856b7`
- job ID: `96094192445`
- GAP step: `2026-08-19T13:57:56Z`--`2026-08-19T16:01:58Z`
- artifact: `gap-run-out`, ID `9373093887`, API size `1489376` bytes
- downloaded ZIP SHA-256:
  `503b8dbf506f0a03429b82a6efdf5645006f2c90540cc69b406163f9bb0f4c7e`
- receipt: `d972_b345_relfrat3_wordexpr_memo_v9.json`, `5504869`
  bytes, SHA-256
  `0675e0ac957796cd2a9facee805b8f5e258d36f0c824e68ba916fdedeeedeade`
- same-job q3 artifact SHA-256:
  `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`

Producer terminal:

```text
B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE output=ci/out/d972_b345_relfrat3_wordexpr_memo_v9.json receipt_sha256=0675e0ac957796cd2a9facee805b8f5e258d36f0c824e68ba916fdedeeedeade
```

Independent checker terminal:

```text
B345_RELFRAT3_WORDEXPR_MEMO_V10_CHECKER_PASS terminal=B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE claim_classification=unknown_not_obstruction artifact_sha256=0675e0ac957796cd2a9facee805b8f5e258d36f0c824e68ba916fdedeeedeade
```

The registered 4096-candidate scan is complete (`evaluated=4096`).  It found no
positive certificate.  Every candidate first failed at target ordinal `6`,
`hexagon_1_coface_0`, component `4`; all 17 diagnostic targets were replayed for
each candidate.  This regularity is now cross-checked.  It is not a common
obstruction class: the exact blocker bytes have 31 distinct SHA-256 values (the
largest class has 2348 rows).  In particular, a common target slot/component
does not imply a common cokernel coset.

Exact scan bindings:

- candidate order SHA-256:
  `3410bbab776fbe1da267d3c3932bf63f9e09bdd02415ee82926619e312d7bbf5`
- record bindings SHA-256:
  `883d491f1fcc0e2e7e22e71d963ff0ae93726043f6b3ff700043e66bc3788112`
- array manifest SHA-256:
  `0767907fee8ac769647048929e7f2380ea588399360fd6c03fd04b973c52e8de`
- candidate-1 blocker SHA-256:
  `0cd653ee0966ccc83d270802bbb5d00b61731f28e27eec1918bb5ea282e00903`

The frozen prefix has 32768 BFS translations plus 207 directed translations,
362725 columns, 362709 pivots, 3090367 live sparse entries, and pool size
976408.  Producer runtime was `3925.4653983149997` seconds; peak RSS was
`829943808` bytes.  Candidate memo statistics were 16637 hits and 45260 misses,
with no evictions; value evaluation dominated at about 2773 seconds.

The terminal remains deliberately nonnegative:
`claim_classification=unknown_not_obstruction`,
`claim_scope=registered_4096_wordexpr_positive_search_only`,
`full_universe_claimed=false`, and `negative_claimed=false`.  No B4-A/B,
nonexistence, full-H3, or W-P0 conclusion follows.  The preregistered explicit
strong correction `y^-18 x^-18 y^18 x^18` is not among these 4096 registered
corrections, so it requires a separate typed single-word lane.

`B345_RELFRAT3_WORDEXPR_MEMO_V10_READY_FOR_GHA`
