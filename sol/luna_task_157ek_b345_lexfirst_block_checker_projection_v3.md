# Luna task 157ek — lex-first target-6 checker prefix-projection repair v3

## 0. Role, scope, and authorized files

Implement the smallest versioned checker-only successor to the failed full run
`32394380070`.  Luna may create or edit only these three implementation/report
files:

1. `search/check_d972_b345_lexfirst_block_target6_v3.py`
2. `search/d972_b345_lexfirst_block_target6_gha_driver_v3.g`
3. `sol/luna_reply_157ek_b345_lexfirst_block_checker_projection_v3.md`

This task file is the Sol-authored implementation contract.  Do not edit the
frozen v2 producer, v2 checker, v2 driver, q3 bundle, any predecessor, workflow,
claim ledger, dialogue book, or other repository file.  Temporary self-test
logs belong outside the repository.  Do not run a full production job, GAP,
GHA, or Git; the parent session owns those actions.

Reuse the frozen v2 producer exactly.  There is no v3 producer.  The receipt
schema, producer task hash, output filename, mathematical predicate, candidate
order, target, block, affine system, terminal tokens, and claim boundary all
remain v2.  The only semantic repair is that the independent checker passes the
three required prefix fields, rather than two, into the already-pinned prefix
replay.

## A. Exact frozen inputs

Authenticate path, SHA-256, and byte count before self-test or checking:

```text
search/d972_b345_lexfirst_block_target6_v2.py
  ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a / 148824
search/check_d972_b345_lexfirst_block_target6_v2.py
  fb28b8b4c7b42f5d83dd1f5c762136812d36731c427a003aae8a8fb0c36a66ba / 130007
search/d972_b345_lexfirst_block_target6_gha_driver_v2.g
  48f5717b9be1d6f6087cdf2864d20d41df2475f5d0d87b43c2bd1deefab01394 / 13597
sol/luna_task_157ej_b345_lexfirst_block_target6_v2.md
  1d6f14ef9f799a43fc344daa38606281dbcf0b2fe47d86db0b44df382762f290 / 14667
sol/luna_reply_157ej_b345_lexfirst_block_target6_v2.md
  f00a3f56e140663002e85a488f78b37ade796126928d475f30bb57e951020428 / 8676
```

The v3 checker must also retain every q3/157ec/157ed/157eh/v1 pin from the
frozen v2 checker.  No predecessor hash or byte count may be silently updated.
The final v3 checker must authenticate this 157ek task by its final SHA and byte
count.  The v3 driver must pin the unchanged v2 producer, final v3 checker,
this task, and all upstream q3/predecessor inputs already pinned by v2.

Keep exactly:

```text
receipt schema  d972-b345-lexfirst-block-target6/v2
receipt output  ci/out/d972_b345_lexfirst_block_target6_v2.json
producer marker D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_PASS
```

The checker and driver may use new v3 self-test/PASS markers, log names, and
sentinels.  Do not rewrite the receipt to claim a v3 mathematical schema and do
not change its `task_sha256`: those fields are emitted by the unchanged v2
producer and must continue to equal the pinned 157ej task.

## B. Run 32394380070: exact incident and claim boundary

Full run `32394380070`, exact head
`ff555abffb36cf66a795fdbec932cad647fde5d4`, failed after 17m43s.  The job
failed in `Run GAP script` with exit code 1 and uploaded zero artifacts.  A
repository-external downloaded log has SHA-256
`b35d8357c9e2ad7788b8493e668eab4be1468bafc38b624837d784e824465c8c`
and 194263 bytes.  This log is provenance evidence, not an input file that the
implementation may require.

The unchanged v2 producer completed and printed exactly one candidate marker:

```text
D972_B345_LEXBLOCK_TARGET6_V2_PRODUCER_PASS
terminal=B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT
```

Its stable phase timings included fresh prefix 101.887956s, raw-lambda oracle
13.644790s, complete old correlation 0.967257s, section witness 0.008886s,
block insertion 1.603776s, and target reduction 334.109854s.  These times are
provenance-only and must not enter a stable mathematical digest.

The independent checker then crashed before completing prefix replay:

```text
check_d972_b345_lexfirst_block_target6_v2.py:1641
  ed.replay_prefix(old, projected, e4, normalized, base_key)
check_d972_b345_triple_cube_raw_lambda_census_v1.py:316
  old.replay_pivot_surgery(receipt, e4, targets, base_key)
check_d972_b345_seedspan_triple4_v1.py:4352
  data["directed_base_support"]
KeyError: 'directed_base_support'
```

There was no checker PASS marker, no driver PASS/math sentinel, no uploaded
receipt, and no cross-checked terminal.  The producer's INCONSISTENT value is a
candidate only.  It is not yet evidence of B1 inconsistency, full-D2
inconsistency, nonexistence, a failed lift, B4-A, or B4-B.  The failed job
cannot be resumed and its unuploaded runner-local receipt must not be imported.
A fresh same-job producer/checker rerun is required after this repair.

## C. Sole defect and exact repair

The frozen v2 checker declares

```python
PREFIX_FIELDS = {"directed_base_support", "directed_surgery", "prefix"}
```

but `_project_prefix` at frozen lines 984--989 returns only
`directed_surgery` and a narrowed `prefix`.  The imported independent replay
requires all three fields.  This is a deterministic checker projection bug,
not a producer false positive and not a mathematical predicate failure.

### C.1 Production-shared exact projection

Factor the projection and its validation into one small checker production
helper used by the actual `check_receipt` call path.  Its output has exactly
these three top-level keys:

```text
directed_base_support
directed_surgery
prefix
```

Require exact key-set equality with `PREFIX_FIELDS`.  Copy/reference
`data["directed_base_support"]` and `data["directed_surgery"]` without
alteration.  Preserve the frozen narrowed `prefix` projection with exactly the
same nine names as v2:

```text
counts, accounting, basis_gate, prefix_pool_checkpoint,
dependent_events, dependent_event_count, dependent_event_sha256,
fresh_not_imported, source_sha256
```

The helper must hard-reject a missing required input, an omitted projected
key, an extra projected key, substitution of `{}` or another support object,
or any value unequal to the corresponding authenticated receipt projection.
Do not synthesize `directed_base_support`, obtain it from a predecessor module,
fill a default, catch the `KeyError`, or downgrade it to UNKNOWN_INPUT or
RESOURCE.

Pass this exact three-key projection to

```python
ed.replay_prefix(old, projected, e4, normalized, base_key)
```

The imported `replay_prefix` and `old.replay_pivot_surgery` must remain the
load-bearing independent replay.  In particular, the inherited code must
independently validate the actual directed-base-support values, translation
schedule, columns, blocker history, dependent events, basis gate, counts, and
digests.  A digest-only or shape-only replacement is forbidden.

Dictionary insertion order and transient object identity are not mathematics.
The helper may build fields in the canonical order written above for stable
self-test traces, but public equality is exact semantic key/value equality.
No projection object, object ID, cache state, or extra digest is added to the
receipt.

### C.2 No other predicate change

Apart from version metadata/authentication/markers and the exact projection
repair, the v3 checker is a mechanical copy of the frozen v2 checker.  Retain
unchanged:

- v2 receipt schema, output path, `TASK_SHA`, exact stage-aware key sets, and
  four terminal meanings;
- q3/E3/E4 reconstruction and all source/context gates;
- B0 prefix replay, old qstar, complete correlation, selected section, ordered
  11-column B1 block, relator-9 independence theorem, and post-block anchor;
- all 109 target-6 raw/reduced vectors, the 108-variable affine system, complete
  contradiction absorption, normalized dual, or selected proof;
- one absolute checker deadline, monitor/cap registries, RESOURCE/INPUT
  handling, checked-write rules, and every frozen v1/v2 lifecycle repair;
- checker independence from all producer predicate/finalizer/block/affine
  helpers and from producer pool/DAG/section IDs.

Do not special-case the expected INCONSISTENT candidate.  The v3 checker and
driver must still accept exactly the same four v2 terminals when independently
valid, and reject any drift.  The rerun result, not this incident log, decides
the mathematical branch.

## D. Required regression fixtures

Use a shared production wrapper so the fixture cannot pass while
`check_receipt` still calls an old two-key expression.  At minimum require:

1. the completed baseline constructs exactly the three-key projection and the
   replay stub/adapter reads all three keys;
2. omission of each of the three inputs is rejected at a named projection
   gate before inherited replay;
3. omission of `directed_base_support` from the projected object reproduces
   the incident shape and is rejected;
4. adding an extra projected key is rejected;
5. replacing `directed_base_support` by `{}`, a stale copy, or a one-field
   mutation is rejected by exact projection equality and/or the real inherited
   replay;
6. the accepted projection reaches the same production `ed.replay_prefix`
   wrapper with positional arguments unchanged;
7. a fake replay recorder confirms the exact three-key payload, while a
   bounded actual inherited replay fixture, if already available without the
   full q3 reconstruction, confirms that all three fields are consumed;
8. the existing completed CONSISTENT/INCONSISTENT, RESOURCE, INPUT, 24 receipt
   mutations, module-lifecycle canaries, phase-key canaries, and selected-proof
   fixtures remain unchanged and pass.

Publish exact self-test counters such as
`prefix_projection_three_keys=1`,
`directed_base_support_consumed=1`,
`prefix_projection_omissions_rejected=3`, and
`prefix_projection_extra_rejected=1`.  Syntax inspection alone is not a
fixture.  Also add a source-shape recurrence gate proving that the production
wrapper, not merely a toy helper, is called at the former failing locus.

Use a new exact checker marker, for example:

```text
D972_B345_LEXBLOCK_TARGET6_V3_CHECKER_SELFTEST_PASS
D972_B345_LEXBLOCK_TARGET6_V3_CHECKER_PASS
```

The unchanged producer continues to emit v2 markers.

## E. v3 driver and fresh rerun contract

Create a versioned ASCII-only v3 driver.  It must:

1. pin the unchanged v2 producer SHA/bytes, final v3 checker SHA/bytes, this
   task SHA/bytes, frozen v2 task, q3 producer/checker/driver, and all named
   predecessor pins;
2. regenerate q3 and independently check q3 in the same job exactly as v2;
3. remove stale v2 receipt, all v3 logs/sentinels, and any stale PASS marker
   before starting;
4. run the unchanged v2 producer from scratch, then the v3 checker against the
   same v2 output, using pipefail/tee and one shared absolute deadline;
5. require exactly one registered v2 producer terminal/marker, exactly one v3
   checker PASS marker, and exactly one v3 driver PASS sentinel;
6. fail closed on traceback, missing/duplicate marker, stale output, hash drift,
   checker nonzero exit, missing receipt, or unsupported terminal;
7. upload the v2 receipt and bounded logs only after producer and v3 checker
   both pass.

Self-test mode runs the unchanged v2 producer self-test plus the v3 checker
self-test and exact-counts all inherited and new markers.  Production mode
must not use the failed run's candidate output or any local checkpoint.

The mathematical terminal meanings remain exactly those of 157ej:

- `...CONSISTENT`: one registered 108-seed correction solves target 6 modulo
  B1, hence full D2; targets 7--33 and a typed lift remain unproved.
- `...INCONSISTENT`: no coefficient vector in the registered 108-seed family
  solves target 6 modulo B1 only; B1 is a subspace of full D2, so this is not a
  full-D2 obstruction or nonexistence result.
- `...UNKNOWN_RESOURCE` / `...UNKNOWN_INPUT`: no mathematical conclusion.

Even after checker PASS, do not claim full D2, full H3, all corrections, typed
lift, B4-A, or B4-B.  For an INCONSISTENT result, the next exact lane is a new
B1 dual followed by a complete full-D2 correlation; it is not bulk insertion
of the obsolete B0 ACTIVE rows.

## F. Performance and stopping discipline

The repair adds one dictionary field and bounded validation only.  It must not
rebuild the prefix twice, add columns, alter pool interning, materialize new
words, or change the affine hot loop.  Source/run evidence suggests the v2
producer needs about 12 minutes and the independent checker had already spent
about 4.5 minutes before the crash.  Normal rerun expectation is about 18--30
minutes for the likely INCONSISTENT branch, pessimistically 35--60 minutes;
retain the frozen 300-minute soft and 330-minute job limits and existing RSS
caps.  Any registered cap remains UNKNOWN_RESOURCE.  An internal projection
or theorem mismatch is a hard failure, never a mathematical terminal.

## G. Reply and freeze

The reply must report:

- final SHA-256 and byte count for the v3 checker, v3 driver, this task, and
  reply (reply hash out of band if needed);
- exact P(v2) -> C(v3) -> driver(v3) pin chain and unchanged schema/output;
- a minimal diff statement showing no producer or predicate change;
- bounded combined self-test command, external log path/SHA, exit codes,
  exact-once markers, and all new projection counters;
- explicit zero-artifact/no-cross-check interpretation of run 32394380070;
- source-only runtime/RSS estimate and `git status --short` proving only the
  three authorized new files plus this pre-existing task were involved.

Do not report READY if any frozen pin drifts, any projection mutation passes,
the production wrapper is not exercised, a traceback is hidden by a pipeline,
or a predecessor file changes.  End a successful reply with exactly:

```text
READY_FOR_GHA
```
