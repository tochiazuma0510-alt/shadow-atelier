# Luna task 157k — repair tuple-v3 workflow audit blockers

Read `sol/luna_reply_157j_tuple_v3_workflow_audit.md` completely before editing.

Role: Luna implementation repair. Do not run local GAP, dispatch GHA, or perform git operations.

Allowed writes only:

- `.github/workflows/d972-burau-tuple-v3.yml`
- `sol/luna_reply_157k_tuple_v3_workflow_repair.md`

Repair every BLOCKER/HIGH from task 157j:

1. q3 calibration must invoke the producer with the matrix row's exact `a=-1`; no implicit/default `(3,2)` drift.
2. Pin and hash-gate the exact SymPy 1.14.0 distribution installed in GHA. Use a fail-closed reproducible wheel/sdist hash mechanism, not version-only `pip install`.
3. Replace the workflow's weak q5 calibration precheck with the producer's complete strong calibration contract. It must reject receipts that the producer would reject, including source/schema/hash/evidence/order/row/count/key mismatches and negative fixtures.
4. Preserve all closed-input, artifact, terminal-marker, uncapped traversal, and UNKNOWN fail-closed gates.

Run YAML parse, producer `py_compile`, `--help`, and `--self-test`; do not run a full campaign. Write exact commands, line pins, hashes, and PASS/FAIL to the specified reply.
