# Luna task 157bs — q5 producer/calibration parallel DAG

Role: Luna GHA implementation support.  Create only:

- `.github/workflows/d972-burau-q5-parallel-v1.yml`
- `sol/luna_reply_157bs_q5_parallel_dag.md`

Do not edit producer/checker, run local GAP, Git, push, dispatch, or GHA.

Problem: repaired fast run 32071014949 still serially rechecks q3 then q4 in
each q5 job before starting q5, duplicating two heavy calibration checks.
Build a fail-closed DAG that overlaps independent work.

Frozen inputs:

- q3/q4 artifacts from run 32051744038 with the exact IDs, names, API sizes,
  JSON SHA-256 values, producer SHA, and artifact metadata already pinned in
  `.github/workflows/d972-burau-tuple-q5-fast-v1.yml`.
- producer `search/d972_b4_burau_fiber_v4.py` unchanged.
- repaired checker `search/check_d972_b4_burau_fiber_v4.py`, SHA-256
  `e0b4cb923c1bd73b9afdc7f47de739f91c8aa3c0d7764c239e1df76d74fbce14`.

Required DAG:

1. `calibration-check` matrix q3/q4: two jobs run independently in parallel,
   authenticate the pinned artifact by API id/name/size/run/expiry and JSON
   SHA, install hash-pinned dependencies, run the repaired independent checker,
   and upload a small seal plus the original receipt/log.  The seal must bind
   run id, artifact id/name/size, receipt SHA, producer SHA, checker SHA, q/a,
   972 rows, and successful checker marker.
2. `q5-produce` matrix a=2,4 starts immediately and concurrently with both
   calibration checks.  It downloads/authenticates both pinned receipts,
   verifies every current source/metadata/hash gate, and runs the unchanged q5
   producer.  Upload its exact receipt/log even on failure; reject resource or
   malformed status as a proof result.
3. `q5-check` matrix a=2,4 depends on all calibration-check jobs and both
   q5-produce jobs.  Download the same-run, attempt-specific calibration seals
   and the matching q5 raw artifact.  Reauthenticate all hashes/seals and run
   the repaired checker on the matching q5 receipt with both calibration
   receipts.  Require exactly one admissible terminal marker, append a concise
   result to the step summary, and upload checked evidence on every outcome.
4. Use read-only permissions, `persist-credentials:false`, Python 3.13.5,
   hash-pinned SymPy/mpmath, 12GB virtual-memory guard, 360-minute job limits,
   `workflow_dispatch`, and branch/path push limited to this new workflow plus
   the frozen producer/checker/artifact.  Avoid shell interpolation bugs and
   artifact name collisions.  Fail closed if a needed matrix artifact is
   missing, ambiguous, expired, or from a different run/attempt.
5. Run YAML parsing and inspect every embedded Python/bash block statically.
   Report SHA/test evidence and end with `Q5_PARALLEL_DAG_READY` or a precise
   blocker.
