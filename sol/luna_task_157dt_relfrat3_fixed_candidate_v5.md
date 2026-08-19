# Luna task 157dt — fixed-candidate relative-Frattini v5

## Role and objective

You are Luna.  Implement the shortest sound positive lane after the
cross-checked transactional-v4 run.  This is a **new, explicitly narrowed
fixed-candidate search**, not a replacement for the 4,096-candidate v4 and not
a negative decision procedure.

The registered universe is exactly correction index 1 (the empty correction)
over the frozen outside roof and fixed word.  Reconstruct that candidate and
its first missing Fox pivot from source data, then grow the unchanged sparse
boundary basis.  Retry the candidate only after its exact canonical blocker
pivot has been introduced.  A positive certificate is sufficient for the
existence claim.  Every nonpositive outcome remains INCOMPLETE or UNKNOWN.

Frozen v4 references:

```text
search/d972_b345_relfrat3_v4.py
  ff2e021647fdaf84697c91f741f2d039575036bc1f389d9dc59dee512e6ca7e1
search/check_d972_b345_relfrat3_v4.py
  54308d8628cd434bbc6a4522fe86296d72d01b42de8db2bc72ea9a6961157c2b
search/d972_b345_relfrat3_gha_driver_v4.g
  b717b6a214913d26207ba4683bbe0403123d5139b5aa45cd7bba62be2b885d56
```

Production evidence motivating this lane:

```text
commit e7a69c5517b7f83f155622e66578b899324bc4ed
canary run 32208843272: PASS
full run 32209072242: workflow/driver/checker PASS
artifact id/name/size 9350213499 / gap-run-out / 242201
archive digest sha256:dbf774a26d0f881d23102efec460d97da1016bc5b7b9eaaf4557741ad63aacff
receipt sha256 b35f69ec7584c98f7dba92d7e50e33ea4639e2526824b0815631e201871128e5
terminal B345_RELFRAT3_UNKNOWN_RESOURCE
reason single_word_or_section_length
producer runtime 176.619784404 s
peak sampled RSS 175161344 bytes
```

The same receipt independently cross-checks the following bounded prefix:

- the exact cheap DP completed all 4,096 entries;
- correction index 1 passed all direct finite-quotient gates;
- at checkpoint 1 it first failed Fox membership at target ordinal 6,
  `hexagon_1_coface_0`, with component 4 and a canonical E4 blocker;
- checkpoints 2, 4, and 8 correctly skipped index 1 because that exact pivot
  had not yet entered the basis;
- the later resource stop was candidate 2 during eager ST/TS word expansion,
  before its first Fox target.  It is unrelated to candidate 1 and is not a
  mathematical rejection.

Do not import the old receipt's blocker as an input.  Recompute it in the new
run and require the expected target name/ordinal/component only as an
independent drift canary after reconstruction.

## Authorized files

Create only:

```text
search/d972_b345_relfrat3_fixed_candidate_v5.py
search/check_d972_b345_relfrat3_fixed_candidate_v5.py
search/d972_b345_relfrat3_fixed_candidate_gha_driver_v5.g
sol/luna_reply_157dt_relfrat3_fixed_candidate_v5.md
```

Do not edit v1--v4, q3 sources, workflows, receipts, or any other file.
Temporary files belong outside the repository.

## A. Exact registered universe and claim boundary

The receipt must bind, and the checker must independently require:

```text
registered_universe.kind = fixed_positive_candidate
registered_universe.correction_indices = [1]
registered_universe.correction_word = []
registered_universe.fixed_outside_roof = the frozen row37/exp2 roof
registered_universe.full_4096_universe_claimed = false
registered_universe.earliest_global_candidate_claimed = false
registered_universe.negative_completeness_claimed = false
```

Reconstruct correction index 1 as the empty word from the frozen q3 fibre and
bind the fixed word, roof, marking, `m=0`, `lambda=1`, source tuples, normalized
inverse fibre, formula manifest, and all upstream SHA values exactly as v4.
Do not build or evaluate the other 4,095 corrections and do not run the v4
all-dictionary cheap-DP phase.

Allowed terminals:

```text
B345_RELFRAT3_FIXED_CANDIDATE_PASS
B345_RELFRAT3_FIXED_CANDIDATE_INCOMPLETE
B345_RELFRAT3_FIXED_CANDIDATE_UNKNOWN_RESOURCE
```

Their meanings are strict:

- PASS: the one registered literal outside pair has a complete independently
  replayable Fox/DAG membership certificate;
- INCOMPLETE: the unchanged registered translation bound was exhausted
  without certifying this pair; this is not nonmembership or obstruction;
- UNKNOWN_RESOURCE: a wall/RSS/structural cap or invariant failure prevented
  completion; this is not nonmembership or obstruction.

No nonpositive receipt may use the words obstruction, impossible,
nonexistence, exhaustive 4096, or B4-A/B4-B as a claim.  A PASS is only the
same relative-Frattini outside-pair existence result scoped to this stage; it
does not close uniform/cofinal/compactness.

## B. Candidate reconstruction and literal gates

Use the v4 mathematics and helper-independent checker contract unchanged:

1. q3 same-job regeneration and independent checker;
2. PB3/PB4 presentations, E3/E4 collectors, five cofaces, formula SHA;
3. fixed word plus empty correction and exact exponent-zero/charming witness;
4. direct finite-quotient replay of both hexagons, ordered pentagon, source
   relations, marking, onto/recovery, and normalized inverse certificate;
5. the exact frozen target order and left-Fox convention.

Candidate 1's literal target words fit the existing 100,000-letter cap.  Keep
that cap.  Do not raise it and do not add an SLP merely for this lane.  Record
the exact candidate/source/inverse/target word lengths and their maxima so a
future representation change is distinguishable from this run.

Run all direct gates once before sparse growth and again when exporting a PASS.
The independent checker reconstructs them from frozen inputs; it must not
trust producer booleans or import producer code.

## C. Unchanged sparse basis and blocker schedule

Reuse the v4 exact packed machinery:

- exact E4 element interning and canonical byte order;
- translation BFS order `+1..+6,-1..-6`;
- geometric checkpoints `1,2,4,...,32768`;
- sparse F3 elimination, pivot order, left translations, lazy section SLP;
- packed provenance DAG and streaming independent positive checker;
- bounded product/inverse caches, RSS guard, 300-minute soft deadline.

At checkpoint 1, begin a candidate transaction before completion/interning,
construct the registered targets in frozen order one at a time, and solve
immediately.  On the first nonsolved fully reduced target, record

```text
(target ordinal, target name, component, canonical E4 bytes)
```

then roll back the complete candidate-only pool and DAG suffix and clear every
pool-ID LRU before ID reuse.  The first reconstructed blocker is expected to
have ordinal 6, name `hexagon_1_coface_0`, and component 4; mismatch is a
fail-closed drift, not permission to substitute the old receipt value.

As the persistent basis grows, do not reconstruct the candidate while its
exact canonical blocker pivot is absent.  At the first geometric checkpoint
after that pivot is introduced, retry from target 0.  A retry may solve farther
and produce a new exact blocker; replace the watch and continue by the same
rule.  Existing basis rows never mutate, so the missing-pivot monotonicity
argument is the same as v4.

There is only one registered candidate.  Therefore no candidate cache,
candidate-order comparison, or 4,096-survivor ledger is needed.  The receipt
must instead record the complete checkpoint/pivot-introduction/blocker/retry
trace for index 1.

## D. PASS certificate and nonpositive receipts

On PASS, regenerate the fixed candidate from its literal word, require exact
target value/gradient equality with the selected transaction, and export the
same lossless packed reachable-DAG certificate as v4.  The independent checker
must decode and stream-replay every reachable node, source section, Fox leaf,
target root, quotient identity, and literal acceptance gate.  Internal pool IDs
are never proof data without their canonical registry rows.

On INCOMPLETE, require:

- all 32,768 registered translations processed in exact order;
- no PASS transaction;
- the final blocker and all retries recorded;
- an explicit `unknown_not_obstruction` / `fixed_candidate_only` claim.

On UNKNOWN_RESOURCE, include the exact bounded prefix:

- current translation/checkpoint/target;
- blocker and retry count/digest;
- basis/pool/DAG/SLP/cache counts and peaks;
- transaction starts/rollbacks/commits and removed pool suffixes;
- exact wall/RSS/structural cap and synchronized hit reason.

The checker rejects missing prefixes, null cap reasons, silent local skips,
candidate rejection inferred from a cap, or any claim about the omitted 4,095
corrections.

## E. Performance and logging

This lane must omit the 4,096-word dictionary construction and 46-context DP.
Its pre-search work should be only q3 bootstrap, fixed-candidate literal replay,
and basis initialization.  Record phase timings separately.

Use `python3 -u` with `bash -o pipefail` and `tee`.  Flush at most every 30
seconds and at every geometric checkpoint:

```text
elapsed, RSS, translations, columns, pivots, live entries,
pool/DAG/SLP/cache sizes, blocker present, blocker pivot present,
transaction/retry counts
```

Keep the v4 RSS and structural caps.  Keep producer soft wall 300 minutes and
workflow 330 minutes.  A cap produces honest UNKNOWN_RESOURCE.

## F. Driver and GHA contract

Version the v4 driver and keep:

- q3 in a separate GAP child which exits before Python starts;
- exact q3 artifact/checker SHA and unique marker gates;
- mandatory `with_pquot_packages=true` / `GAP_P2_PACKAGE_ROOT`;
- stale output/log/sentinel removal;
- producer/checker `pipefail` + `tee`, zero-exit sentinels, exact artifact SHA,
  and exactly one allowed terminal/checker PASS marker;
- exact pins for v1--v4 and the new producer/checker.

Do not edit the workflow.  Parent dispatch will use JSON string values so the
quoted GAP output preamble survives byte-for-byte.

## G. Selftest and freeze discipline

Run at most one lightweight combined differential selftest after the first
complete implementation.  It must cover:

1. fixed universe is exactly `[1]` and no dictionary/DP path executes;
2. direct fixed-candidate gates and exact target order on a bounded fixture;
3. checkpoint-1 blocker reconstruction without importing an old blocker;
4. skip while the exact pivot is absent, mandatory retry after introduction,
   and replacement by a later blocker;
5. pool/DAG rollback and LRU clearing before ID reuse;
6. PASS regeneration and packed-DAG replay;
7. PASS, INCOMPLETE, and structural UNKNOWN with exact bounded prefixes;
8. mutations that attempt global-earliest, 4096-exhaustive, obstruction, or
   B4-B claims are rejected.

Do not run the full producer locally.  Do not run production GAP, Git, GHA, or
edit workflows.  If the sole test exposes only a fixture error, report it and
request one corrective rerun.

## Reply contract

In `sol/luna_reply_157dt_relfrat3_fixed_candidate_v5.md`, report:

- exact source hashes/bytes and frozen pins;
- the registered one-candidate universe and claim boundary;
- direct-gate, blocker, transaction, packed-certificate, and terminal contract;
- selftest command/result and mutation coverage;
- source-only runtime/RSS estimate;
- exact proposed GHA inputs;
- explicit statements that no production GAP/GHA/Git was run and that the lane
  is positive-only, fixed-candidate, and non-global.

End with exactly:

```text
B345_RELFRAT3_FIXED_CANDIDATE_V5_READY_FOR_GHA
```
