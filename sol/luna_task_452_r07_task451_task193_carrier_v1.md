# Luna task 452: Task451 positive -> task193 literal carrier v1

Role: Luna implementation owner.  This is a bounded downstream adapter task;
do not change the Task451 search, its checkpoint, or any mathematical claim.

## Objective

Implement the minimal positive-only adapter specified by
`sol/proof_r07_a0_batch_positive_to_task193_a2_carrier_v416.md`.
It must turn an independently accepted Task451 `COMMON_CANDIDATE` into a
dedicated literal carrier containing the exact

```text
(g760, correction_word, corrected_word, direct replay/provenance)
```

needed by the existing task193/A2 consumer.  It must not relabel or patch the
history-free adapter-v5 dialect.

## Required inputs and acceptance boundary

1. Physically bind the Task451 result, durable checkpoint, checker PASS log,
   source head/run/artifact provenance, and exact current Task451 producer,
   checker, driver, and frozen-rank-51 pins.
2. Accept only the exact Task451 v1 positive envelope:
   `status=terminal=COMMON_CANDIDATE`, `reason=null`, `claims.A0=true`,
   `current_dual_profile=null`, and the exact checker PASS marker.  Every
   RESOURCE/UNKNOWN/non-PASS input is a typed nonpositive stop.
3. Obtain the correction only from the checker-equal
   `terminal_replay.literal_word`; never reconstruct it from batch history or
   producer prose.
4. Reconstruct the pinned literal `g760`, confirm the Task451 target owner,
   and compute `corrected_word=freely_reduce(g760+correction_word)` using the
   right-correction convention.
5. Reuse the accepted task179/task198 literal evaluator where it is already
   exact, but rerun the small direct eleven-occurrence/all-seven carrier gate.
   Require exact exponent zero, joint-kernel identity,
   `eleven_occurrence_replay=true`, `direct_all_seven_replay=true`, and
   `right_g760_multiplication=true`.
6. The output is a new tagged carrier schema only.  Do not emit A2, lift,
   fake, Ihara, or endpoint claims.  Do not copy Q0 stores, selector fibres,
   echelons, duals, or batches into the downstream payload; keep only immutable
   input identities and the selected ancestry needed to authenticate the
   literal carrier.

## Independence and tests

- Supply a helper-nonshared checker which independently free-reduces all three
  words and directly reconstructs the carrier gates.  Calling the pinned
  Task451 checker as upstream authentication is allowed; inheriting its
  Boolean without binding its physical result/checkpoint/log is not.
- Provide a bounded SELFTEST/fixture for the adapter boundary.  It is not an
  actual Task451 positive and must say so.  Mutation tests must reject at
  least: terminal, result/checkpoint identity, checker marker, source head,
  literal word, `g760`, corrected multiplication order, one occurrence,
  exponent/joint-kernel gate, and selected action ancestry.
- Do not add a production SELFTEST to the Task451 search and do not run the
  real A0 computation locally.
- Keep memory bounded: stream/hash physical inputs; do not load or reproduce
  a Q0 store or physical echelon.  The adapter should be seconds-scale after
  the already accepted upstream checker.

## Allowed files

Create only versioned files with these roles:

```text
search/d972_r07_task451_task193_carrier_v1.py
crosscheck/check_d972_r07_task451_task193_carrier_v1.py
search/d972_r07_task451_task193_carrier_gha_driver_v1.g
search/certs/d972_r07_task451_task193_carrier_selftest_v1.json   (only if needed)
sol/luna_reply_452_r07_task451_task193_carrier_v1.md
```

Do not edit workflows, old adapters, v220, proofs, claims, or provenance.
Do not commit, push, dispatch GHA, or use credentials.  Run only bounded local
compile/static/fixture tests.  In the reply list exact byte counts, SHA-256,
commands, terminals, mutation totals, reuse boundaries, and any blocker.  If
the full direct evaluator cannot be reused without importing an old A0
dialect, STOP and report the exact missing ABI instead of inventing a flag.

