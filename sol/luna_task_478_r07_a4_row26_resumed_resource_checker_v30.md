# Luna Task478 — A4 row-26 resumed-resource checker v30

## Role and scope

Implement only the two mathematical repairs proved in
`sol/proof_r07_a4_terminal_resource_witness_v423.md` and
`sol/proof_r07_a4_resumed_resource_counter_typing_v428.md`, plus the exact
invocation/path repairs in
`sol/sol_reply_469_audit_r07_a4_row26_resource_checker_only_v1.md`.
Do not edit or depend on the rejected untracked v29/driver-v1 outputs.

Frozen owner:

```text
crosscheck/check_d972_r07_word_independent_successor_kernel_v28.py
11048 c2c1629dc225ebea085b72d1900d7684f4c4184f8e064da8ec4057dc921d2bfa
generated v28
281780 444ee68e79715657707c77778fcb597f83d289147699e7ce5295414b956edeae
```

Create v30 as a guarded successor of v28.  Patch by exact cardinality, not
line-number assumptions.

1. Apply v423's unique typed over-cap witness only to the terminal canonical
   counters and their genuine semantic/host/peak/restore typed views.
2. Replace the invalid resumed assertion
   `terminal_completed == terminal_semantic` by v428 equation (2.2): the
   completed map equals both semantic/completed maps of the authenticated
   base checkpoint, has the exact registered semantic domain, is numeric,
   nonnegative, within caps, and componentwise at most terminal semantic.
   Do not infer that the terminal-minus-base work is durable.
3. Preserve every v28 base/delta/head/row/query/event/epoch/queue/word-DAG,
   producer, authority, output-seal, and independent semantic replay gate.
4. Add real production-function mutation gates for both counter predicates,
   including the exact row-26 counter maps as a positive bounded fixture.
   Reject base/completed drift, completed above terminal semantic, missing or
   extra completed key, trigger/cap/typed-view/state drift, a second over-cap,
   and the old contradictory predicates.

Create a checker-only driver v2 for permanent release asset

```text
URL    https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9809473723_gap-run-out.a4-row26.zip
bytes  56410
sha256 5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a3360e3
```

Preserve and authenticate the exact six replay members and all immutable
run/job/head/artifact bindings from Task469.  Copy the six members to the
checker-owned repository paths `$root/ci/out/<exact basename>`.  Invoke one
checker and no producer, from the repository owner, with explicit arguments:

```text
--input ci/in/d972_r07_seven_context_roof_presentation_v1.json
--producer ci/out/d972_r07_word_independent_successor_kernel_v40.json
--output ci/out/d972_r07_word_independent_successor_kernel_v30.verdict.json
--checkpoint ci/out/d972_r07_word_independent_successor_kernel_v40.checker.checkpoint.json
--resume ci/out/d972_r07_word_independent_successor_kernel_v40.checker.checkpoint.json
--seconds 14400 --rss-bytes 8000000000
--task198-receipt ci/in/d972_r07_seven_context_roof_presentation_v1.json
--task198-manifest ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json
--task198-producer ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt
--task198-checker ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt
--task198-verdict ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json
```

Use fresh owned paths without rejecting generic workflow `driver.g/run.log`.
Require shell exit propagation, exactly one checker terminal-prefix line and
exactly one expected `UNKNOWN_RESOURCE` line, no Traceback/STOP, and a
nonempty canonical self-sealed verdict bound into the receipt.  Keep timeout
and RSS margins, source/release/member pins, one checker/no producer, and no
silent default inputs.

No production semantic replay, GHA, workflow edit, git, or bytecode cache.
Bounded compile/load/self-test/static checks only.

## Exact outputs

1. `crosscheck/check_d972_r07_word_independent_successor_kernel_v30.py`
2. `search/d972_r07_word_independent_successor_kernel_row26_checker_only_gha_driver_v2.g`
3. `sol/luna_reply_478_r07_a4_row26_resumed_resource_checker_v30.md`

End with `TASK478_R07_A4_ROW26_RESUMED_RESOURCE_CHECKER_V30_PASS` or a typed
STOP.
