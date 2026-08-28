# Luna reply 300 - task297 parallel v4 independent static audit

## Verdict

**REJECT.** Task297 does contain a small fixed-dual multiprocessing toy, but
the five-file package does not satisfy the commissioned production,
resource/checkpoint, parity, SELFTEST, or independent-mutation contracts.
There are multiple deterministic pre-execution failures.

This was a read-only static audit of all five task297 files against every
numbered section of `sol/luna_task_297_r07_task192_parallel_boundary_v4.md`.
No task297 file was changed. No Python, GAP, GHA, network, or git command was
executed. SELFTEST and PRODUCTION remain `UNEXECUTED`.

## Audited identities

| task297 path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_normalized_exact_common_word_parallel_v4.py` | 12845 | `517953fde4c930cea706a26630d67651fdd7dc3ff1522045e240a7637c536170` |
| `crosscheck/check_d972_r07_normalized_exact_common_word_parallel_v4.py` | 9103 | `339433f0c1b677c6276079f740f44609e67754f0cd9f7a8552d9fed8d4e3661f` |
| `search/d972_r07_normalized_exact_common_word_parallel_gha_driver_v4.g` | 5685 | `48177b8e734ec578016da80601be93369bda0dd58c59e646e312587f2dc2e88e` |
| `search/certs/d972_r07_normalized_exact_common_word_parallel_selftest_v4_20260828.json` | 280 | `64b565fa910b0a66a06ee29258d523d79702d37f9d38b101a805e69f560dc1ec` |
| `sol/luna_reply_297_r07_task192_parallel_boundary_v4.md` | 2601 | `e7c7f66a3054216d47f5ad4237dcf8566b3321832a08eeadde21464e4b1a1a31` |

## 0. Role and path boundary

- **PASS:** exactly the five commissioned task297 paths exist, and the reply
  declares `UNEXECUTED`.
- **PASS:** the GAP driver is ASCII-only.
- **REJECT:** “production fails closed until an authenticated resume is
  supplied” was implemented as an unconditional missing adapter, not as an
  authenticated-but-undispatched production path. Producer lines 124-127
  merely test that a relative `ci/in/*` file exists and then always raise
  `task192 authenticated resume adapter not supplied`. There is no seal,
  byte/SHA, manifest, or checkpoint authentication.

## 1. Exact optimization boundary

### What is locally correct

- **PASS, toy layer only:** producer lines 55-60 use Linux
  `multiprocessing.get_context("fork")` and `Pool.map` for one supplied
  dual and one supplied descriptor roster. Worker range 2..4 is enforced.
- **PASS, toy layer only:** lines 46-50 add partial accumulators modulo 3,
  remove zero totals, and select with
  `(block, translation_blob, relator_index)`, represented by
  `(k[0], k[2], k[1])`.

### Load-bearing failures

1. **No v3/adaptive-rank integration.** There is no
   `BoundaryDescriptorCache.correlation` adapter, retained-rank loop, or v3
   producer call. Production always stops at lines 124-127. Therefore the
   code does not establish that only a frozen dual epoch is parallelized in
   the actual task192 search, nor byte-for-byte retained-column parity with
   serial v3.

2. **Shard authentication is incomplete.** Worker line 39 emits
   `count` and `interval_digest`, but merge lines 43-54 check neither.
   There is no digest binding the actual partial accumulator and contributor
   result. Merge derives `pair_count` from `len(descriptors)`, not from
   authenticated returned counts.

3. **Reordering is accepted.** Line 44 sorts returned intervals before
   comparing them, and line 47 sorts results again before concatenation.
   Thus worker-result reordering is normalized, not rejected. Contributor
   records are not checked for exact field shape, pair-index monotonicity,
   interval membership, or consistency with the partial accumulator.

4. **The checker does not authenticate the shard cover itself.** Checker
   lines 43-45 compare a top-level `cover` and aggregate values to the
   serial object, but do not compare each shard's `start/stop/count`,
   `interval_digest`, partial, or contributors. Lines 46-47 are dedented
   outside the worker-count loop, so only the final `w=4` shard list is
   digest-checked.

5. **No translated-row reconstruction or direct scalar replay.** Producer
   lines 33 and 54 set `translated_row` equal to the selected key itself.
   No PB3/PB4 translated row is reconstructed and no direct pairing of that
   row with the frozen dual is evaluated. Checker line 45 merely requires
   this key-shaped value to equal `selected_key`.

The F3 and lex operations are therefore locally plausible synthetic
operations, not evidence of serial-v3 semantic parity.

## 2. Resource and checkpoint truth

**REJECT in full.**

- All task192 caps occur only as argparse fields on producer line 129.
  `parallel`, `_worker`, and `merge` never receive a monitor. There is
  no pre-launch cap check, cumulative `boundary_pairs` charge, wall/RSS
  check before or after a batch, aggregate child RSS measurement, timeout, or
  safe-cursor update.
- `ResourceError` is declared at line 13 and caught at line 133, but no
  code raises it. `Pool.map` has no timeout.
- The SELFTEST monitor at line 71 is a literal assertion, not measured
  execution metadata. The code constructs 36 shards across four cases at
  worker counts 2+3+4, then four more shards for two 2-worker epochs; it
  nevertheless reports `completed_shard_count=9`. Correspondingly, the
  reported `worker_count=4`, `total_pair_count=24`, and
  `boundary_pairs=24` do not describe all work performed by
  `selftest_cases`, nor the driver's selected worker count.
- There is no checkpoint writer/reader, safe pair cursor, incomplete-batch
  discard/replay state, COMMON sidecar omission gate, or production monitor
  envelope. The mutation named `incomplete_batch_checkpointed` only empties
  a synthetic top-level cover; it creates or validates no checkpoint.
- Error receipts created at lines 133-135 are unsealed. The production
  checker requires `self_digest_sha256` at line 110, so even the intended
  adapter-missing `UNKNOWN_INPUT` receipt cannot complete the driver/checker
  terminal-equality contract.
- Production checker validation accepts any self-resealed v4
  `UNKNOWN_INPUT`, `UNKNOWN_RESOURCE`, or `FAIL` envelope without
  checking parallel metadata, worker count, `single_process`, checkpoint,
  or monitor truth.
- The purported v3 checker path on checker line 9 is
  `crosscheck/d972_r07_normalized_exact_common_word_cached_v3.py`, which
  does not exist. The pinned real path is
  `crosscheck/check_d972_r07_normalized_exact_common_word_cached_v3.py`.
  Hence `PASS_REGISTERED_FAMILY` deterministically fails its path/pin gate.
  Even with the filename repaired, line 114 passes the outer v4 receipt
  directly to the v3 checker; there is no documented or validated semantic
  projection into the v3 schema and no check of the v3 checker's exact pass
  marker.

The driver does pin four immediate v3 files and the three runnable v4 inputs,
but those pins do not repair the absent production adapter or unreachable v3
independent replay.

## 3. Mandatory SELFTEST and mutation gates

### Deterministically invalid base case

The first SELFTEST case cannot satisfy its own two-shard-winner gate. From
producer lines 61-64:

```text
key [1,1,"a"]: pair 0 contributes 1, pair 2 contributes 2 => 0 in F3
key [1,2,"a"]: pair 1 contributes 1
key [1,1,"b"]: pair 3 contributes 1
```

The exact v3 lex order therefore selects `[1,2,"a"]`, whose sole contributor
is pair index 1. It has no contributor with index at least 3. Producer lines
85-87 and checker lines 49-51 consequently reject the unmutated
`active_two_shards` case.

The fixture does not contain any of the four cases. Its single JSON object
only declares `expected.cases=6` and `mutations=20`; checker lines 30-33
do not bind fixture case bytes to receipt cases. It is externally byte-pinned
but is not the commissioned sealed, case-bearing fixture.

The epoch test at producer line 71 defines “leak free” only as
`epoch1 != epoch2`. It neither compares epoch 2 with an independent serial
oracle nor authenticates an epoch identifier, so it does not prove absence of
state leakage.

### Producer mutation counter is circular

Producer line 123 calls `mutate(r)` while
`mutation_controls.attempted/rejected` are still 0/0. Every resealed mutant
then goes through `validate`, whose line 91 requires those fields already
equal 20/20. Thus all mutations can be counted as “rejected” by the common
unfinished mutation-control field, independent of the mutation's semantics.
The invalid active case is a second unrelated common rejection. This is not
an executed/rejected semantic count.

### Independent checker mutation trace

As shipped, checker line 99 rejects the invalid base receipt before line 100
can run mutations. Even assuming only the base case were repaired, static
trace gives at most **16/20**, not 20/20:

| mutation | checker path if base were valid | audit |
|---|---|---|
| omitted shard | top-level cover mismatch | rejects |
| duplicated shard | top-level cover mismatch | rejects |
| overlapping interval | top-level cover mismatch | rejects, but the edit actually creates a gap |
| gap | top-level cover mismatch | rejects |
| permuted pair order | serial object mismatch | rejects |
| wrong dual digest | changes a w=2 shard; lines 46-47 inspect only w=4 | **accepted** |
| wrong descriptor digest | same dedent defect | **accepted** |
| changed coefficient | recomputed serial object mismatch | rejects |
| changed translation key | recomputed serial object mismatch | rejects |
| changed contributor | aggregate contributor mismatch | rejects |
| wrong mod-3 merge | changes only scalar, not the accumulator merge | rejects for another scalar mismatch |
| zero kept active | sets selected key to `None`; it does not keep a zero-total key active | rejects for another selection mismatch |
| wrong lex winner | selected-key mismatch | rejects |
| wrong direct scalar | assigns 1, which is already this case's scalar | **accepted no-op** |
| wrong pair count | pair-count mismatch | rejects |
| stale epoch | flips only a Boolean, not an epoch/digest/state | rejects for Boolean mismatch |
| worker failure accepted | sets a shard flag that checker never inspects | **accepted** |
| incomplete batch checkpointed | empties cover; no checkpoint exists | rejects for cover mismatch |
| `single_process=true` | instead sets `parallel_boundary=False`; no `single_process` field is introduced | rejects the wrong mutation |
| worker count outside 2..4 | changes the summary list to `[1]` | rejects |

Producer mutation line 114 has an additional placement defect: it sets
`p["worker_failed"]` at the merged-result top level, whereas runtime merge
line 45 checks worker flags inside shard records. Receipt validation never
checks that top-level field. Its apparent 20/20 is supplied only by the
circular common gate described above.

### SELFTEST terminal mismatch

Producer line 123 stores terminal
`R07_NORMALIZED_EXACT_COMMON_WORD_PARALLEL_V4_PRODUCER_SELFTEST_PASS`;
line 141 prints that value after the producer-terminal prefix. Driver line 49
instead requires the literal suffix `PASS`. Checker line 107 emits suffix
`PASS`. Therefore producer/checker terminal equality cannot hold even if
the base case were repaired.

Moreover, producer line 140 prints the standalone SELFTEST-PASS marker
unconditionally for every SELFTEST invocation, including caught
`UNKNOWN_INPUT` or `UNKNOWN_RESOURCE` results. That marker is not evidence
of a successful selftest.

## 4. Driver

- **PASS, structural:** immediate pins match current bytes; the driver rejects
  its five stale paths, computes `min(4,nproc)`, requires at least two,
  supplies task192 caps and 19,800 seconds in its production command, and
  writes one final sentinel only after shell gates.
- **REJECT:** the PRODUCTION branch at lines 52-57 skips the mandatory
  producer/checker SELFTEST-first sequence entirely.
- **REJECT:** the selected worker count is passed on the command line but not
  independently recorded; the SELFTEST receipt hard-codes worker count 4.
- **REJECT:** SELFTEST expects the wrong producer terminal as above.
- **REJECT:** a supplied resume reaches an unsealed producer error receipt,
  then checker line 110 returns nonzero, so the production driver exits before
  its exact-one/equality gates. An absent resume stops even earlier at shell
  `test -n`. This is a STOP, but not the commissioned authenticated terminal
  contract.

## 5. Task297 reply accuracy

- **PASS:** file identities, `UNEXECUTED`, and the statements that no A0
  COMMON, compatible lift, fake certificate, or Ihara witness was obtained
  are correct.
- **REJECT:** the reply's claims of authenticated pair counts, contributor
  order, translated-row/scalar equality, isolated epochs, exact terminal
  equality, and independent 20/20 semantic mutation rejection are not
  supported by the code paths above.

## Final status

```text
TASK297 STATIC AUDIT:             REJECT
TASK297 FILE MUTATION:            NONE
SELFTEST EXECUTED:                NO
SELFTEST ACCEPTED:                NO
PRODUCTION EXECUTED:              NO
PRODUCTION-READY PARALLEL ADAPTER: NO
ACTUAL A0 COMMON:                 NONE
COMPATIBLE LIFT:                  NONE
FAKE CERTIFICATE:                 NONE
IHARA WITNESS:                    NONE
```

`TASK300_R07_TASK297_PARALLEL_STATIC_AUDIT_V1_REJECT_UNEXECUTED`
