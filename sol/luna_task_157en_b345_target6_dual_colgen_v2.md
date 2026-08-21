# Luna task 157en — target-6 dual column generation v2: semantic binding repair and split GHA

## Role and objective

You are **Luna**.  Implement the smallest useful versioned successor to
157em.  The predecessor completed eight exact column-generation batches, then
reached the ninth complete correlation, but failed while validating an
`UNKNOWN_RESOURCE` receipt because two different remainder encodings were
mistakenly equated.  Repair that binding, raise only the batch budget from 8
to 12, and split production and checking into two independent GHA runs so
neither shares the old 300-minute envelope.

Do not claim a lift, an obstruction, or a cross-check from run 32439034163.
Do not alter the mathematical universe, target, seed order, correlation order,
first-terminal rule, quotient, or any cap other than the single batch cap.

## Authorized files and two-stage freeze protocol

Initial implementation may create only these new versioned files:

1. `search/d972_b345_target6_dual_colgen_v2.py`
2. `search/check_d972_b345_target6_dual_colgen_v2.py`
3. `search/d972_b345_target6_dual_colgen_producer_gha_driver_v2.g`

After their static hostile audit and combined self-test, Stage P may be
committed and dispatched.  Stage P must run fresh q3 plus the v2 producer only.
It must not invoke the v2 checker.

Only after Stage P has completed, its artifact has been downloaded and audited,
and its canonical receipt SHA-256 and byte count are known, the following
additional files are authorized:

4. `search/certs/d972_b345_target6_dual_colgen_v2_producer_receipt.json`
   — exact canonical Stage-P receipt, byte-for-byte; no hand editing.
5. `search/d972_b345_target6_dual_colgen_checker_gha_driver_v2.g`
6. `sol/luna_reply_157en_b345_target6_dual_colgen_v2.md`

The checker source is created in the initial stage, but the checker driver is
post-P because it must pin the committed receipt's exact path, SHA-256, and byte
count.  The final reply records both run IDs, both exact heads, the committed
receipt SHA/bytes, all final P/C/driver/task hashes, and terminal scope.  The
reply reports its own final hash out of band; no driver/reply hash cycle.

No existing v1 file may be overwritten.  No workflow file may change.  Do not
commit, push, or dispatch; the parent is the sole broker.

## Frozen predecessor pins

Pin these exact inputs before doing any work:

```text
157em task
  sol/luna_task_157em_b345_target6_dual_colgen.md
  sha256 60df04261bfd9f30928ed51b26bd501518c05eae43b0bb8ca08507e3b6c4ca99
  bytes  43511

157em producer v1
  search/d972_b345_target6_dual_colgen_v1.py
  sha256 8a3dd09811ec790b90f5f3d16890e9ef534a9fc0399597a0daa892605c58c8fc
  bytes  410757

157em checker v1
  search/check_d972_b345_target6_dual_colgen_v1.py
  sha256 08cee7be18128b1dcc1376012854a828695c19a97bd1495e4cb0d7f7ddea035e
  bytes  228980

157em driver v1
  search/d972_b345_target6_dual_colgen_gha_driver_v1.g
  sha256 e67d6397fca2b7181710fe8baf5893f8273399dc43b6c4ec27caebe4f1a903dc
  bytes  14634

157em final reply
  sol/luna_reply_157em_b345_target6_dual_colgen.md
  sha256 70fc6a91a1e10316b5ef2c8ad497e4fc61479866de28b80e0402de92c1065b58
  bytes  39427

q3 artifact and checker remain exactly those pinned by 157em
  receipt sha256 3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72
```

All transitive pins in the v1 driver remain exact unless a versioned v2 path
necessarily replaces P, C, task, or driver.  The v2 files must authenticate the
v1 files above as frozen predecessors.

## Evidence from failed run 32439034163

Bind this evidence in the task reply and in a non-claim provenance section of
the v2 receipt:

```text
run_id       32439034163
head_sha     2234d5968d3658ab3721aef6f5bf8eab204e9136
job_id       96645874482
main start   2026-08-21T02:13:28Z
main end     2026-08-21T04:53:04Z
main wall    2h39m36s (includes the fresh q3 child)
artifact     none; upload step skipped
```

The q3 child and independent q3 checker passed.  The phase log proves completion
of `commit_g1..g8` and `incremental_g1..g8`, then completion of `target_g9`,
`dual_lift_g9`, and `correlation_g9`.  It did **not** print `preflight_g9`.
The traceback entered producer line 5426, the `UNKNOWN_RESOURCE` validation
branch, and failed at line 4086 with:

```text
RuntimeError: 157em generation-one target/initial-target binding
```

The source path establishes the actual branch: after the active ninth
correlation, eight completed batches trigger
`column_generation_batches` with detail `column_generation_batch_limit`.
Thus the strongest admissible mathematical reading is only:

- an unaudited producer-side prefix candidate with eight committed canonical
  ACTIVE batches;
- the generation-9 complete correlation remained ACTIVE;
- no obstruction, no consistency witness, no typed lift, and no nonexistence;
- no valid receipt, no independent checker, and no cross-checked result.

This evidence must never be promoted to a terminal certificate.

## Exact root cause and mandatory semantic repair

The v1 producer uses two intentionally different digests:

1. `initial_target.target6.fresh_remainder_sha256` is the digest of the public
   109-row **summary ledger**.  Each row contains `ordinal`, `kind`,
   `entry_count`, and the row's own SHA-256.
2. `generation_ledger[i].target.remainders_sha256` is the digest of the 109
   complete **semantic sparse rows**, computed by the existing expression
   `sha_obj([sorted(row.items()) for row in remainders])`.

Producer v1 lines 4094–4095 compare (2) with (1).  Checker v1 lines 3588–3589
repeat the same category error.  These are not alternative serializations of
one byte string and must remain distinct public commitments.

Implement the repair as follows.

### Producer

- Add exactly one wrapper field to `initial_target`, named
  `semantic_remainders_sha256`.
- Define one local canonical helper for the complete semantic-row digest.  It
  must validate 109 ordered rows, canonical `(component, 154-byte-hex)` keys,
  coefficients in `{1,2}`, and compute exactly the existing semantic digest:
  `sha_obj([sorted(row.items()) for row in rows])`.
- Use that helper both when constructing
  `initial_target.semantic_remainders_sha256` from the freshly captured 109
  remainders and in `target_public` for every generation.
- Generation-one cross-binding compares
  `first.target.remainders_sha256` with the new wrapper field.
- Keep `target6.fresh_remainder_sha256`, its ledger contents, and its frozen B1
  value unchanged and independently validated.
- Update the exact `INITIAL_TARGET_KEYS`, schema/version, task pin, and all
  terminal/resource stage tables.  No permissive subset validation.

### Independent checker

- Implement its own semantic-row digest helper; importing or calling the
  producer helper is forbidden.
- Freshly rebuild B0, fixed B1, the 109 raw gradients, and all 109 semantic
  remainders.  Recompute the new wrapper digest and demand exact equality with
  the receipt.
- Compare the fresh generation-one target semantic digest with
  `initial_target.semantic_remainders_sha256`, never with the summary-ledger
  digest.
- Separately retain the exact B1 gate
  `target6.fresh_remainder_sha256 ==
  9cfd9adc23c9b4dff3d9415f06ce0d0df5fe53b0bf5394aaa8ef667f1b55d407`
  (the currently pinned ledger value).  Do not silently change this value into
  the semantic digest.
- Replay every later generation, packed block, target, dual, correlation,
  commit, incremental state, and terminal exactly as in v1.

Required mutations in both production-shaped self-tests:

1. replace the semantic digest by the ledger digest — reject;
2. replace the ledger digest by the semantic digest — reject;
3. alter one semantic coordinate/coefficient before hashing — reject;
4. permute the 109 row order — reject;
5. stale generation-one semantic digest with otherwise valid resource receipt
   — reject;
6. matching fake strings in both fields without fresh reconstruction — reject
   in the checker;
7. all four terminals pass the shared real validator with the exact new field;
8. the run-32439034163 generation-9 RESOURCE shape passes after the correct
   semantic binding and fails under the old cross-binding mutation.

The self-test must assert that the two production digests are unequal.  Do not
make this a fixture-only schema test; route it through the normal receipt
validator and checker replay helpers.

## Mathematical predicate and cap delta

Copy the v1 mathematical implementation.  Preserve exactly:

- pinned E4/q3 roof and 108 registered seeds;
- source tuple, all typed source gates, target ordinal 6 only;
- B0 and fixed B1 reconstruction;
- normalized general raw dual lift and signs;
- 76 base occurrences × 11 relators complete two-pass correlation;
- canonical translation-blob order and relator order 1..11;
- select-all-active batch semantics and first terminal;
- section recovery, packed complete-block ledger, transactional commit;
- quotient-row incremental update and all-109 direct cadence;
- `CONSISTENT`, `FULL_D2_OBSTRUCTION`, `UNKNOWN_RESOURCE`, and
  `UNKNOWN_INPUT` meanings and claim boundaries.

Make exactly this mathematical resource change:

```text
column_generation_batches: 8 -> 12
algorithm.max_batches:      8 -> 12
```

Update the cap digest, schema, fixtures, and exact resource observations.  Keep
all other caps unchanged, in particular:

```text
total_new_translation_blocks = 4096
total_new_relator_columns     = 45056
translations_per_batch       = 1024
producer/checker soft budget  = 18000 seconds each
RSS and serialization caps    = unchanged
```

If generation 13 is still ACTIVE after twelve completed batches, the exact
terminal is `UNKNOWN_RESOURCE`, with top-level
`reason == cap_key == column_generation_batches` and detail
`column_generation_batch_limit`.  This is not an obstruction.  Preserve the
total-block-before-batch resource precedence.

## Stage P — producer-only GHA

The producer driver must be thin and fail closed.

1. Authenticate all source path/SHA/byte pins, including this task and P/C v2.
2. Freshly generate the frozen q3 artifact in the same job and run its pinned
   independent checker exactly as v1 did.
3. Run P v2 only with a fresh output path and `--seconds 18000`.
4. Do **not** invoke C v2.
5. Require exactly one supported terminal token, exactly one v2 producer PASS
   marker, at least one phase marker, no traceback, a checked-write canonical
   receipt, and exact producer-log receipt SHA/byte binding.
6. Write a producer-stage sentinel only after all gates pass.  Remove stale
   receipt, log, and sentinel files before launch.
7. Exit zero for any properly validated supported terminal, including honest
   `UNKNOWN_RESOURCE`/`UNKNOWN_INPUT`, so the unchanged workflow uploads the
   receipt.  Unsupported or missing terminals fail.
8. Report exact producer elapsed and margin against 18000 seconds.  Runtime/RSS
   never enter stable mathematical hashes.

Stage P establishes only a producer certificate candidate.  It is never called
cross-checked.  The parent downloads the artifact, checks its canonical bytes,
then commits that exact file at the authorized `search/certs/` path with its
SHA/bytes.

## Stage C — checker-only GHA after receipt commit

The later checker driver must pin:

- the exact P/C/task sources;
- the exact committed receipt path, SHA-256, and byte count;
- all frozen transitive and q3 pins;
- its own versioned driver path/hash/bytes through the normal freeze process.

It then:

1. freshly regenerates and independently checks q3 in the same job;
2. runs C v2 only against the pinned committed receipt with a new independent
   `--seconds 18000` allowance;
3. never invokes P v2 and never rewrites the committed receipt;
4. requires exactly one checker PASS marker, no traceback, exact terminal echo,
   exact receipt SHA/bytes before and after checking, and a checker-stage
   sentinel written only at the end;
5. publishes a small checker log/timing artifact, not a second mutable receipt.

Only Stage C success promotes the Stage-P receipt to **cross-checked**.  It is
still not Lean-verified.

## Terminal claim boundary

- `...CONSISTENT`: only the registered 108-family target-6 affine system is
  consistent modulo the generated D2 basis at the terminal generation.  Any
  selected proof must undergo the unchanged literal/direct/proof replay.  It
  says nothing about targets 7..33 or a global typed lift.
- `...FULL_D2_OBSTRUCTION`: the normalized terminal dual annihilates the exact
  complete 76×11 full-D2 correlation for the pinned E4 roof and separates the
  registered-108 target-6 affine system.  It is family/roof-relative, not global
  nonexistence.
- `...UNKNOWN_RESOURCE` and `...UNKNOWN_INPUT`: claim `none`.

Run 32439034163 contributes runtime and debugging evidence only.

## Performance expectation and stop rules

The predecessor producer-side path used about 159.6 minutes through the ninth
correlation.  Its eight incremental phases alone total about 139.5 minutes;
the later four were roughly 17–24 minutes each.  With four additional batches,
Stage P is expected around 230–270 minutes.  A 285–300 minute outcome is
pessimistic but possible; the existing 18000-second soft guard must return an
honest RESOURCE receipt rather than crash.  Stage C gets a separate full
18000-second run, removing the v1 producer+checker common-deadline hazard.

Do not add checkpoint/resume, sharding, basis serialization, or a second
mathematical optimization in 157en.  Those are later lanes if cap 12 remains
ACTIVE.  Do not raise RSS, total-block, column, packed-receipt, or DAG caps to
force completion.

## Required self-tests in strict two-stage order

### Before Stage P dispatch

After P v2, C v2, and the producer driver have a frozen static candidate, run
exactly one pre-P combined **source** self-test.  The checker source participates
through its independent production validators, but no checker driver or
committed Stage-P receipt exists yet.  This self-test must include:

- all inherited v1 source markers exactly once;
- the producer and checker semantic-vs-ledger mutations above;
- cap 12 / generation-13 RESOURCE fixture and cap/reason/detail precedence;
- CONSISTENT, FULL_D2_OBSTRUCTION, RESOURCE, and INPUT receipt fixtures through
  the real P/C validators;
- the Stage-P driver static/mode fixture proving checker-process absence,
  unsupported-mode rejection, and stale producer receipt/log/sentinel rejection;
- one producer-stage 18000-second deadline, with no internal reset;
- producer checked-write/readback and receipt-serialization fallback fixtures;
- no traceback and exact pre-P self-test markers.

Stage-C driver behavior is not tested here because that file is not yet
authorized and the committed receipt does not yet exist.  Pre-P static audit
and this one self-test authorize only the parent's Stage-P commit/dispatch.

### After Stage P, before Stage C dispatch

After the exact Stage-P receipt is downloaded, audited, committed at its
authorized path, and the checker driver and reply are frozen, run exactly one
post-P checker-stage self-test.  It must include:

- exact committed-receipt path/SHA/byte binding;
- the Stage-C driver proving producer-process absence and stale checker
  log/sentinel rejection;
- receipt immutability before/after checking;
- wrong receipt path, SHA, and byte-count mutations, each rejected;
- fresh q3 generation plus its independent checker markers exactly once;
- one checker-stage 18000-second deadline, independent of Stage P and with no
  internal reset;
- exact terminal echo and checker PASS/sentinel ordering;
- no traceback and exact post-P self-test markers.

Record both self-test commands separately in the final reply, with their exit
codes, marker counts, log SHA/bytes, and `git status --short` restricted to the
files authorized at that stage.  Post-P receipt/checker-driver freeze and this
second self-test require their own hostile audit before Stage C dispatch.
