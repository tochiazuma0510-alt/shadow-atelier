# Task 512a -- mandatory completion-durability addendum

This addendum is part of Task512 and does not broaden its architecture.  Read
the now-frozen Task511 reply:

`sol/sol_reply_511_audit_r07_a4_actual_production_shard_wiring_v1.md`, 8078 /
`45f7e56fb7d4695f5c399cc301d6ddfa5c16d211a910ef6210cc716b034ac864`.

Task511 found one additional reached ordering defect.  Generated v24 calls
`physical_store.commit(query)`, whose dispatch writes the physical HEAD with
`obsolete=true`, before it appends the completed bridge/row/chunk/sample
prefix and before the ordinary `write_checkpoint`.  A crash in that interval
discards the only durable open-row continuation before the completed-row
delta exists.

The Task512 v25/v34/v44 successor must also make this smallest repair:

1. The MEMBER/ZERO commit may update the in-memory terminal state exactly
   once, but must not durably publish `physical HEAD obsolete=true` yet.
2. Append the completed bridge/row/chunk/sample prefix exactly once and
   durably write the ordinary completed-row delta/checkpoint first.
3. Only after that write succeeds, atomically publish the physical HEAD as
   obsolete.  No exception path may expose durable `obsolete=true` while the
   ordinary completed-row delta is absent.
4. Add a bounded reached-call-path write-order fixture (including injected
   failure before and after the ordinary write) that proves the physical HEAD
   remains live before the ordinary delta and becomes obsolete only after it.
   Preserve the existing exact-once terminal/prefix checks.  Do not add a
   second row computation, retry, snapshot, or production traversal.

Report this as a separate acceptance item in the same Task512 reply and retain
the same final marker.
