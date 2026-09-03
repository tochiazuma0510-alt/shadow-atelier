# Sol(max) Task602: audit independent grade-one full-routing replay v1

Act as an independent hostile mathematical/static auditor.  Write only
`sol/sol_reply_602_audit_r07_grade1_independent_full_routing_v1.md`.  Do not
edit code or workflows, commit, push, dispatch GHA, or wait for the live run.
The production replay was deliberately launched in parallel and this audit
must not delay it.

Read in full:

1. `sol/luna_task_599_r07_grade1_independent_full_routing_v1.md`
2. `crosscheck/check_d972_r07_a0_first_rung_grade1_full_routing_v1.py`
3. `.github/workflows/d972-r07-a0-grade1-independent-routing-v1.yml`
4. `sol/luna_reply_599_r07_grade1_independent_full_routing_v1.md`
5. `sol/sol_reply_597_audit_r07_grade1_decision_probe_v2.md`
6. `crosscheck/check_d972_r07_a0_first_rung_grade1_decision_result_v1.mjs`

Audit the exact launched snapshot at commit
`5440d66d44f9ca937bc7f8a4958a54ad9f5eba4f`; checker SHA-256
`8e159cc262fd35d61018da4b30db45017534546f7bbe89ebd001b3dbff6286d8`.

Check, first to last:

1. source/candidate identity and every pinned digest;
2. genuine implementation independence from the Task595 producer, including
   group/affine/Fourier routing and aggregation;
3. exact lower-first order: all 2,014 old rows before the 6,045 block rows;
4. coefficient-2 arithmetic, canonical pivots, owner reduction and coefficient
   reconstruction over GF(3);
5. full 8,059-row exhaustion, expected ranks/leads/basis digest, candidate
   coefficient list, and zero-remainder acceptance gates;
6. workflow download names, bounds, authentication, failure propagation and
   artifact policy;
7. hot paths for accidental quadratic ordering, dense expansion, unnecessary
   copies, unbounded memory, or any other avoidable slowdown.

Use small independent fixtures if useful, but do not run the real 8,059-row
campaign.  Reject optional hardening and do not request a redesign.  Give
`PASS`, `PASS_AFTER_REPAIR`, or `FAIL`, with exact load-bearing repairs only.
State separately whether a successful authenticated live receipt would justify
promoting the first v220 rung from `0/6` to `1/6 cross-checked`; it must not be
called Lean-verified and implies no cofinal/fake/Ihara conclusion.
