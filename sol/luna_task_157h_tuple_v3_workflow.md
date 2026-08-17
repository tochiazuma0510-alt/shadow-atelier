# Luna task 157h — staged GHA workflow for exact tuple/Schreier v3

Create a versioned GHA workflow for the audited PASS producer:

- `search/d972_b4_burau_fiber_v3.py`

Authorized files:

- `.github/workflows/d972-burau-tuple-v3.yml`
- `sol/luna_reply_157h_tuple_v3_workflow.md`

Do not edit the producer/other workflows, run a full local calculation/GAP,
commit, push, or dispatch.

Requirements:

1. Exact-branch push trigger with closed paths for this workflow, the v3
   producer, and frozen word artifact.  Credential-free checkout, contents
   read-only, six-hour jobs, fail-closed shell/exit/diagnostic/marker gates,
   and attempt-unique artifacts on success or failure.
2. Pin Python 3.13 and SymPy 1.14.0; print and gate versions.  Apply an explicit
   standard-runner memory ceiling without converting timeout/resource stops
   into mathematical results.
3. First run q=3,a=-1 and q=4,a=2 as independent `fail-fast:false`
   calibration jobs.  Each must run `--self-test` first, then full, and gate
   exact calibration status/orders/972 completeness from the receipt.
4. Upload each calibration receipt separately.  A dependent q5 matrix job
   must download and authenticate both exact receipts, then run a=2 and a=4
   independently with `fail-fast:false`; the v3 source itself must perform its
   strong source/hash/evidence unlock.
5. For q5, accept only a complete receipt plus candidate or all-pass UNKNOWN
   marker.  `UNKNOWN_RESOURCE` must leave the job non-successful while still
   uploading diagnostics/receipt.  Never interpret all-pass as B.
6. Preserve full logs and outputs.  Do not use arbitrary workflow inputs.

Parse YAML, run static dependency/artifact/closed-input gates and
`git diff --check`; report hashes and runtime risks.
