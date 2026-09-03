# Luna Task 603 - bounded external-owner worker v10 repair

Role: Luna implementation.  Read `sol/sol_reply_600_audit_r07_external_owner_worker_v9.md`
in full and make one versioned v10 successor containing only its load-bearing
F1--F4 repairs.  Add only:

1. `search/d972_external_owner_gf3_worker_v10.c`
2. `search/d972_external_owner_gf3_worker_v10.py`
3. `search/check_d972_external_owner_gf3_worker_v10.py`
4. `sol/luna_reply_603_r07_external_owner_worker_v10.md`

Do not edit v9, proofs, v220 or workflows.  Do not commit, push, dispatch GHA,
or run production.  No redesign and no optional hardening.

Implement every F1--F4 item, first to last:

- correct the coefficient-indexed packed GF(3) subtraction table; preserve the
  packed loop and add the exact coefficient-one cancellation witness;
- never free the session ledger on either cap path, make `write_full` a real
  full-write loop, and split warning-prone one-line conditionals;
- use a genuine partial pipe read, add an optional checker deadline, make
  poison terminal with kill/reap/close/join cleanup, poison on partial durable
  transactions, and give finalize one common cleanup path;
- open and consume all five durable streams once in exact lockstep, require
  canonical bytes/exact EOF/lead-ID binding, and replace Python trit-by-trit
  first-lead scans with a packed-byte table;
- fix the 88-byte-header versus payload assertions; provide bounded portable
  exact reads and compile timeout/strict flags;
- make the checker use its supplied campaign, build an independent dense
  expected transcript/offset/basis/companion/leads image, and whole-byte compare
  all five streams;
- exercise literal STATS/CLOSED/EOF and unchanged counters after genuinely-new
  row/rank/pair cap cases, including clean shutdown that exposes ledger errors;
- implement the four named isolated mutation gates with a clean-resume control;
- add the commissioned raw partial-header, malformed/noncanonical terminal,
  test-only allocation-FATAL, fragmented-success, stalled/short-response and
  hard-kill provisional-record gates.  Keep the allocation failpoint out of the
  production binary.

Preserve positive IDs, monotone resume, exact lead/lc/scale, suffix resume,
exhausted cursor semantics, manifest replacement, and v9's rank-4095 service
contract.  Do not broaden this into the distinct grade-one rank-8059 adapter.

Run all available bounded local static/dense tests.  If no C compiler exists,
report `NOT_RUN_NO_COMPILER` honestly rather than weakening the checker.  Give
exact bytes/SHA-256 and readiness in the reply.  Production remains false.
