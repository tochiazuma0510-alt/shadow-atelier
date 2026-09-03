# Task 597 — independent audit of the A0 grade-one decision-first v2 probe

Role: Sol(max), read-only mathematical/code-path auditor.  Do not implement,
run the 8,059-row production calculation, change workflows, commit, push, or
dispatch GHA.  Write only
`sol/sol_reply_597_audit_r07_grade1_decision_probe_v2.md`.

Read in full:

1. `sol/proof_r07_grade1_decision_first_terminal_factorization_v463.md`
2. `sol/sol_reply_593_audit_r07_grade1_decision_first_factorization_v1.md`
3. `search/d972_r07_a0_first_rung_grade1_v3.py`
4. `search/d972_r07_a0_first_rung_grade1_decision_probe_v2.py`
5. `search/check_d972_r07_a0_first_rung_grade1_decision_probe_v2.py`
6. `.github/workflows/d972-r07-a0-first-rung-grade1-decision-v2-recovery.yml`
7. `sol/luna_task_595_r07_grade1_decision_probe_v2_and_gha.md`
8. `sol/luna_reply_595_r07_grade1_decision_probe_v2_and_gha.md`

Audit only the load-bearing questions:

1. Does v2 route exactly the same finite 2,014 old-basis and 6,045 block-basis
   inputs as the frozen v3 merge, in the same order, without the known
   lower-row double reduction?
2. Is `accept_already_reduced` extensionally identical to the acceptance tail
   of `PackedEchelon.insert`, including coefficient 2, dependent rows, pivot
   order and coefficient ancestry?
3. Does the target reduction decide precisely membership of the registered
   grade-one residual in the span of all routed rows?  Identify any path that
   could emit a false MEMBER or false NONMEMBER.
4. Are input/state digests, actual ranks, logical cursor, memory/time failure
   semantics, terminal markers and the four-file candidate artifact sufficient
   for a candidate decision?  This is not a request for a final independent
   replay or a proof certificate.
5. Audit the hot path for accidental dense closure, duplicate work, per-row
   large copies, Python bytewise pivot scans, ancestry/DAG construction, dual
   construction, or another unnecessary operation that could turn the measured
   v3 roughly-six-minute routing prefix into a long run.  Reject optional
   hardening and overengineering.
6. Check the workflow source SHA gates, exact source artifacts, job/inner
   timeouts, RSS limits, success-only decision upload and always-log upload.

Run only bounded local fixtures/static checks if useful.  Verdict must be one
of `PASS`, `PASS_AFTER_REPAIR`, or `FAIL`, with exact minimal repairs for any
load-bearing defect.  Preserve the vocabulary rule: all production output is
candidate; `verified` is reserved for Lean.
