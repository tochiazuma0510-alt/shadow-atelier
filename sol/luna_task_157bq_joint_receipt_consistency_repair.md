# Luna task 157bq — joint Burau receipt consistency repair

Role: Luna implementation support.  Repair and harden the frozen joint bundle.
Do not run local GAP, Git, push, or GHA.

Authorized edits only:

- `search/d972_b4_burau_joint_v1.py`
- `search/check_d972_b4_burau_joint_v1.py`
- `.github/workflows/d972-burau-joint-v1.yml` if a binding change is needed
- `sol/luna_reply_157bq_joint_receipt_consistency_repair.md`

Observed parent finding: producer lines 831--836 count a full solution only when
`pentagon_ok and h10_ok and h11_ok`, but append
`full_GT_m_witnesses_prefix` whenever only `h10_ok and h11_ok`; the independent
checker appends witnesses only when the full conjunction holds.  This can make
an honest receipt fail independent checking.  Make the field semantics and
both implementations identical, and add a mutation/selftest that catches the
exact regression.

Required:

1. Repair that mismatch without weakening the zero-fiber criterion.
2. Adversarially compare every serialized producer field consumed by the
   checker, looking for any additional producer/checker drift, slicing error,
   source-hash problem, or terminal-marker/workflow mismatch.  Repair only
   genuine issues.
3. Preserve one-common-source synchronization, complete H' fiber enumeration,
   all four transforms, H10/H11/pentagon conjunction, and one common CRT m
   residue across every specialization.
4. Run py_compile, both selftests, YAML parse, workflow static checks, and
   `git diff --check` on authorized files.  No full heavy computation.
5. Report exact diffs/hashes/tests and end with
   `JOINT_RECEIPT_CONSISTENCY_REPAIR_READY` or a precise blocker.
