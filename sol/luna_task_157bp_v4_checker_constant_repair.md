# Luna task 157bp — v4 checker constant repair and q5-fast preflight

Role: Luna implementation auditor.  The parent observed GHA run 32069959135
fail before computation with `NameError: P_ORDER is not defined` at
`search/check_d972_b4_burau_fiber_v4.py:914` in both q5 jobs.

Authorized edits only:

- `search/check_d972_b4_burau_fiber_v4.py`
- `.github/workflows/d972-burau-tuple-q5-fast-v1.yml` only if a workflow-side
  correction is strictly necessary
- `sol/luna_reply_157bp_v4_checker_constant_repair.md`

Do not run local GAP, Git, push, or GHA.

Required:

1. Diagnose why `P_ORDER` / `PPRIME_ORDER` are referenced but undefined and
   restore the exact frozen compact-roof constants from the independently
   established v4 producer/receipts, with a mutation/selftest that would catch
   future omission or drift.
2. Run py_compile, both v4 producer/checker selftests, and a lightweight check
   of the two pinned q3/q4 receipts if available under the temp artifact path
   named in the current task context.  A full heavy recheck is not required
   locally.  Confirm the q5-fast workflow invokes the repaired checker.
3. Inspect for the next immediate pre-computation NameError/schema blocker so
   the rerun does not fail at the following line.  Keep semantics unchanged.
4. Report exact changed lines, SHA-256, tests, and terminal marker
   `V4_CHECKER_CONSTANT_REPAIR_READY` or a precise blocker.
