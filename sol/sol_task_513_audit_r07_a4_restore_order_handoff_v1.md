# Task 513 -- independent Sol(max) audit of Task512/512a A4 repair

Role: adversarial audit only.  Do not edit implementation, run the 6,441-row
production, dispatch GHA, commit/push, or write any file except the reply below.
Use static/generated-source inspection and small bounded fixtures/mutations.
Do not reconstruct unrelated search mathematics.

Read fully:

1. Task511 instruction and STOP reply, especially F3/F4;
2. Task512 and Task512a instructions and Luna reply;
3. frozen subjects:
   - producer v25, 27075 /
     `8e5c16f28113218485f7196c6873dbbf3ce17a0e03bd7daafe71bc6e8da5015f`;
   - generated producer, 286439 /
     `e4fb7ead7e1dcfc5806574481f1e83e008991e516de20e2eb3a67753fec03098`;
   - checker v34, 5838 /
     `b00219523c2e5703b8c6c52c7bf24655c727ddc72c7da9fd06c746063875a9ba`;
   - generated checker, 312553 /
     `2ffcdede9a20acdd99bab3c4847db4c4a4f013e33fc151ac01b77f088d21df75`;
   - driver v44, 8960 /
     `7f70546b51b934edcc6d64626af4d04c18f15642a10db8b40eaea3f9fcfb96f3`;
   - Task512 reply, 3271 bytes (independently hash it).
4. v24/v33/v43 and every frozen predecessor/member they pin.

Important provenance erratum to audit, not to copy blindly: v43 and the
Task511 pin table accidentally print the release digest as the 63-character
string ending `...a336e3`.  The actual 64-character digest, consistently
recorded in the earlier accepted v1/v2/v3 row26 drivers, v42, v220, Tasks469,
478, 481 and 485, is

`5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a3360e3`.

V44 must use that 64-character value while independently pinning v43's source
as a predecessor; this correction is required, not drift.

Decide these bounded gates on actual generated/reached paths:

F1. Exact nonzero wrapper/generated pins and exact-cardinality v24/v33
successor patches.  Deleting helpers must not restore the old executable path.

F2. On ordinary row26 plus three accepted physical shards, generated
`build_kernel` authenticates/rebuilds the ordinary state, installs ordinary
completed counters, then invokes direct restore exactly once before deriving
correlation rounds or doing new work.  The fourth real shard file must have
`semantic_before == shard3.semantic_after`.  Direct restore must restore
basis/formals/records/accepted-entry events/batch dual events/epoch once,
perform zero reductions/inserts/correlations/raw replay, and preserve the one
query-level `live_duals` item rather than appending per shard.  Independently
test a re-sealed semantic discontinuity and duplicate live-dual input.

F3. MEMBER/ZERO completion is a real two-phase durability handoff.  In-memory
commit may set obsolete for ordinary-reference selection, but the disk HEAD
must remain live until completed bridge/row/chunk/sample state and the ordinary
delta/checkpoint have been durably written.  Only afterward may one atomic
write publish disk `obsolete=true`.  Inject failure in the actual ordinary
`write_checkpoint` call and after it; require publish counts 0/1 respectively,
disk/live ordering, ordinary `delta_chain` reference and exact-once prefixes.
Reject a helper-only/manual-file fixture.

F4. V34 remains independent of v25 and its actual acceptance route preserves
the full v33 replay while checking semantic continuity and the ordinary
query-level live-dual history.  Mutations must be genuinely injected and
re-sealed, not boolean self-report.

F5. V44's generated shell must execute.  It must authenticate the correct
64-character release digest above and all six exact flat members, retain their
canonical producer/checker HEAD+delta names for resume, bind wrapper and
generated pins, use fresh contained paths, one producer, 14,400-second/8-GB
internal caps with external margin, RESOURCE/no-checker and positive/one-checker
branches, exact owned markers, nonempty outputs and false witness claims.
Detect assignment-only pins, `GetStringSize(path)` byte mistakes, renamed HEAD
without renamed deltas, or parse-only transport.

F6. No new full snapshot, cumulative prefix rewrite, dense conversion, worker
pool, retry search, production SELFTEST, second producer/checker on RESOURCE,
extra boundary closure, or changed A4 roster/arithmetic/terminal meaning.

Return exactly one verdict:

- `GO_FOR_GHA_DISPATCH`, only if F1--F6 pass; or
- `STOP_DO_NOT_ADOPT`, with the smallest concrete repair list.

Write only:

`sol/sol_reply_513_audit_r07_a4_restore_order_handoff_v1.md`

Include exact pins, commands/results, F1--F6, claim boundary, and final marker
`TASK513_R07_A4_RESTORE_ORDER_HANDOFF_AUDIT_GO` or
`TASK513_R07_A4_RESTORE_ORDER_HANDOFF_AUDIT_STOP`.
