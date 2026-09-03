# Sol(max) Task610: fresh static audit of external-owner worker v10

Role: independent code-path auditor. Read in full:

1. `sol/sol_reply_600_audit_r07_external_owner_worker_v9.md`
2. `sol/luna_task_603_r07_external_owner_worker_v10.md`
3. `search/d972_external_owner_gf3_worker_v10.c`
4. `search/d972_external_owner_gf3_worker_v10.py`
5. `search/check_d972_external_owner_gf3_worker_v10.py`
6. `sol/luna_reply_603_r07_external_owner_worker_v10.md`
7. `sol/proof_r07_grade1_finite_roster_external_owner_cap_v462.md`

Audit all and only Task600 F1--F4. Decide whether the exact v10 files are
ready for one bounded GHA strict-compile/interop campaign. In particular
check packed GF(3) arithmetic, ledger lifetime, full writes, partial pipe
reads, one absolute response deadline, poison/reap/close/join behavior,
transaction failure, sequential durable replay, canonical-byte/lead binding,
cap state preservation, raw-wire fragmentation/stall/short replies, exact
five-stream dense oracle, isolated mutations, hard-kill provisional records,
test-only allocation failure, and production-binary exclusion of the
failpoint.

Also audit for any avoidable live-path dense copies, per-record file reopen,
per-trit Python scan, blocking 65536-byte read, or optional test/hardening
which would materially slow the later-grade calculation. Require the
commissioned finite evidence, but do not invent a broader mutation/fuzzing
campaign.

Return `PASS`, `PASS_AFTER_REPAIR` or `FAIL`. If `PASS`, state the exact
bounded compile/interop gates which a workflow must execute. Do not compile,
implement, run GHA, modify code/proofs/v220, or perform git operations.
Write only:

`sol/sol_reply_610_audit_r07_external_owner_worker_v10.md`

No grade membership, A0, COMMON, cofinality, fake or Ihara claim follows.
`verified=false`.
