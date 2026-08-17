# Luna task 157bx — synchronized Burau joint campaign v2 (q=2/q=7)

Role: Luna implementation/computation support.  Joint v1 is running on GHA
over the existing q=3,4,5 specializations.  Build a separate versioned v2
that tests whether one and the same F2 word can satisfy the finite B4
hexagon/pentagon lift equations simultaneously after adding admissible q=2
and/or q=7 Burau specializations.  Do not run local GAP or a large local
enumeration.

Authorized files only:

- `search/d972_b4_burau_joint_v2.py`
- `search/check_d972_b4_burau_joint_v2.py`
- `.github/workflows/d972-burau-joint-v2.yml`
- `sol/luna_reply_157bx_joint_q2q7_v2.md`

Requirements:

1. Start from the audited v1 semantics but copy into v2; never edit v1.
   Preserve frozen 972 target/word/key bindings and synchronized-common-word
   logic.  A zero row is meaningful only if the same source word is forced
   across every component and the independent checker reconstructs this.
2. Audit q=2 (`a=1`) and q=7 (`a=1..6`) mathematically before registration.
   Exclude degenerate or non-invertible cases only with an explicit reason.
   Preregister a finite matrix of configurations that maximizes new
   information while respecting six-hour/12-GB GHA lanes; include at least
   q5+q7 configurations if feasible.  Resource/cap outcomes remain UNKNOWN.
3. Producer and checker must not share result tables or helper-generated
   conclusions.  Reconstruct H10/H11/pentagon images, common-word fibers,
   row counts, and zero/all-pass status independently; add corrupt-receipt
   and unsynchronized-word adversarial selftests.
4. Workflow: parallel matrix lanes, read-only permissions,
   `persist-credentials:false`, pinned Python/dependencies, explicit memory
   and timeout gates, exact source/artifact hashes, always-uploaded lossless
   evidence, and unique fail-closed terminal markers.  Checker success is
   mandatory before any zero is promoted.
5. Only lightweight local Python/static tests are allowed.  No Git, push,
   dispatch, GHA, or local GAP.  Report exact hashes/commands and finish with
   `JOINT_Q2Q7_V2_READY`, or a precise blocker.

