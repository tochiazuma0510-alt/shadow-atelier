# Luna task 157fg — audit producer/checker receipt contract alignment

Audit, but do not modify:

- `search/d972_b4_burau_matrix_v1.g`
- `search/check_d972_b4_burau_matrix_v1.py`

Write only `sol/luna_reply_157fg_matrix_contract_audit.md`.  Do not run local
GAP/full receipt checking, commit, push, or dispatch.

Return strict PASS/BLOCKER.  Verify every task-157f receipt field and honest
algorithm-evidence key exactly matches task-157g checker admission; source SHA
is computed/checked from the exact GAP file; deletion and common-word H' gates
are actually executed; kernel count/canary and frozen digests are bound; no
producer-independence or permutation-degree fiction is present; q3/q4 values
are calibration-only; q5 candidate/UNKNOWN semantics are unchanged.  Parse and
selftest the checker, run static checks/diff-check, and report both hashes.
