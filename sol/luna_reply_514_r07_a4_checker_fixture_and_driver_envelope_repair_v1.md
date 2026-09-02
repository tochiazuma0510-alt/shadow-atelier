# Luna reply 514 -- checker fixture and driver envelope repair

Task514 C1/C2 is complete.  Producer v25 was not changed (27075 bytes,
`8e5c16f28113218485f7196c6873dbbf3ce17a0e03bd7daafe71bc6e8da5015f`; generated
286439 bytes, `e4fb7ead7e1dcfc5806574481f1e83e008991e516de20e2eb3a67753fec03098`).
No production traversal, GHA dispatch, workflow, or git operation was done.

Frozen outputs:

| file | bytes | SHA-256 |
|---|---:|---|
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v35.py` | 10246 | `c8383a18169ec2da63e4e7a64de17f05d305c35e15393bcbb9e3c312ac6d5dd7` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v45.g` | 12430 | `d59bee6ea9a5366643d5409505ce25e91baa7c18031911eea36565e2f221782f` |

v35 generated source is pinned at 312553 bytes,
`2ffcdede9a20acdd99bab3c4847db4c4a4f013e33fc151ac01b77f088d21df75`.

Bounded gates:

- `python -B crosscheck/check_d972_r07_word_independent_successor_kernel_v35.py --source-patch-info`: PASS; v34 and generated-v34 pins match.
- `python -B crosscheck/check_d972_r07_word_independent_successor_kernel_v35.py --self-test`: PASS.  The generated `validate_terminal_checkpoint -> _a4_v33_validate_physical_chain` route was reached twice, with actual materializer/read counts 2/2.  A fully re-sealed ordinary state with two live duals was rejected as `physical:live_dual_history`; a fully re-sealed TEMP HEAD plus shard whose semantic predecessor was mutated was rejected as `physical:semantic_counter_order`.  These are acceptance-route reasons, not list-length/helper-only checks; v35 remains independent of v25.
- Python AST parse: `AST_PARSE_PASS`.
- GAP `ReadAsFunction("search/d972_r07_word_independent_successor_kernel_gha_driver_v45.g"); QUIT;`: PASS.

v45 restores the v43 reached shell gates over the corrected envelope: the
release is 56410 bytes with digest
`5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a3360e3`; all six
flat members are authenticated and copied with canonical v40 producer
HEAD/delta1/delta2 and checker-checkpoint names; all five authority-side files
are regular non-symlink files; wrapper/generated pins, fresh paths, pipefail,
single producer, elapsed checks, 14400-second/8-GB internal caps and external
margins are enforced.  Terminal counts and forbidden `UNKNOWN_INPUT`,
`HARD_STOP`, `ERROR`, and `Traceback` text are rejected.  Producer RESOURCE
and checker RESOURCE/positive output JSON are parsed for exact terminal,
complete, false/absent A0/COMMON/NONMEMBER claims, and false downstream
claims; producer RESOURCE runs zero checker, while only producer PASS permits
one checker.  The generated shell is executed after `bash -n` by the driver.

TASK514_R07_A4_CHECKER_FIXTURE_AND_DRIVER_ENVELOPE_REPAIR_PASS
