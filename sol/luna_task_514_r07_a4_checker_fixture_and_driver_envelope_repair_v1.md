# Task 514 -- narrow A4 checker-fixture and dispatch-envelope repair

Role: Luna implementation engineer.  Repair only the two Task513 STOPs.  Do
not alter producer v25, A4 arithmetic/roster/resource semantics, workflows,
run production/GHA, commit/push, or touch unrelated files.

Read fully:

1. Task512/512a and Luna reply;
2. Task513 instruction and STOP reply, 7599 /
   `d648e0b6c7cb2b0f04c2bc721bf21b4dd89f4dab40a766fb4bb4fd3e7fcbcdd3`;
3. frozen v25/v34/v44 and v33/v43 predecessors.

Producer v25 and generated v25 are accepted by Task513 F1--F3 and must remain
byte-for-byte fixed at 27075 /
`8e5c16f28113218485f7196c6873dbbf3ce17a0e03bd7daafe71bc6e8da5015f`
and 286439 /
`e4fb7ead7e1dcfc5806574481f1e83e008991e516de20e2eb3a67753fec03098`.

Produce exactly:

- `crosscheck/check_d972_r07_word_independent_successor_kernel_v35.py`;
- `search/d972_r07_word_independent_successor_kernel_gha_driver_v45.g`;
- `sol/luna_reply_514_r07_a4_checker_fixture_and_driver_envelope_repair_v1.md`.

## C1 -- genuine checker acceptance-route mutations

Pin v34 (5838 /
`b00219523c2e5703b8c6c52c7bf24655c727ddc72c7da9fd06c746063875a9ba`)
and generated v34 (312553 /
`2ffcdede9a20acdd99bab3c4847db4c4a4f013e33fc151ac01b77f088d21df75`).
The live generated gates need no redesign.

Replace v34's boolean `len(duplicate) != 1` and helper-only semantic evidence
with a bounded fixture that calls the generated actual
`validate_terminal_checkpoint -> _a4_v33_validate_physical_chain` route.
Inject an ordinary state with two query-level `live_duals` and require the live
reason `physical:live_dual_history`.  Inject a fully re-sealed physical shard
whose semantic transition disagrees with its predecessor/base and require the
live reason `physical:semantic_counter_order`.  The mutation must be consumed
by the acceptance function; a local list-length calculation or direct call to
`_a4_v34_counter_order` is not evidence.  Instrument the reached functions and
report positive call counts.  Keep v35 independent of v25 and retain every v33
replay/mutation gate.

A tiny authenticated-materializer stub is permissible only to avoid rebuilding
the 6,441-row authority in SELFTEST; it must return a structurally sealed test
state, the actual acceptance function must consume the mutated state/reference,
and no acceptance predicate may be replaced or bypassed.  Prefer reuse of the
existing v33 fixture machinery.  Bound all work.

## C2 -- restore the reached v43 envelope in v45

Pin v44 exactly, but build v45 by retaining the load-bearing v43 shell gates
and the v44 corrections.  In particular:

- retain the correct 64-character asset digest
  `5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a3360e3`;
- authenticate all six flat members and keep the canonical v40 producer HEAD,
  delta1/delta2 and checker-checkpoint names for resume;
- bind exact v25/generated-v25 and v35/generated-v35 pins;
- restore all five authority-side-file existence/non-symlink checks from v43;
- keep fresh contained paths, `pipefail`, one producer, elapsed checks,
  14,400-second/8-GB internal caps and external margins;
- reject `UNKNOWN_INPUT`, `HARD_STOP`, `ERROR`, `Traceback`, wrong/multiple
  terminal lines, stale/empty output and checkpoint;
- on producer RESOURCE, parse the output JSON (not grep-only) and require exact
  `status=terminal=UNKNOWN_RESOURCE`, `complete=false`, and every present
  A0/COMMON/NONMEMBER claim false/absent plus
  `forbidden_downstream={lift:false,fake:false,Ihara:false}`; run zero checker;
- only after producer positive, run at most one v35 checker.  Preserve v43's
  checker RESOURCE transport as typed nonpositive candidate and require the
  same false downstream claims; only an exact checker PASS may emit the
  positive marker;
- execute the generated shell; `bash -n` alone is not acceptance.

Do not use `GetStringSize(path)` as a file byte count, do not inherit v43's
63-character digest typo, and do not rename a HEAD without its deltas.

## Acceptance

Run only bounded source-pin/AST/selftest/reached-shell/GAP `ReadAsFunction`
checks.  Freeze nonzero generated pins.  The reply must include exact bytes and
SHA-256 for v35, generated v35, v45, commands/results, actual rejection reasons
and final marker:

`TASK514_R07_A4_CHECKER_FIXTURE_AND_DRIVER_ENVELOPE_REPAIR_PASS`

If either narrow repair fails, stop with the exact blocker rather than adding
new architecture.
