# Luna task 157j — tuple-v3 GHA workflow adversarial audit

Role: independent implementation/contract auditor. Do not edit producer or workflow, run local GAP, dispatch GHA, or perform git operations.

Allowed write: `sol/luna_reply_157j_tuple_v3_workflow_audit.md` only.

Audit the frozen files:

- `.github/workflows/d972-burau-tuple-v3.yml`
- `search/d972_b4_burau_fiber_v3.py`
- `sol/luna_task_157h_tuple_v3_workflow.md`
- `sol/luna_reply_157h_tuple_v3_workflow.md`

Check at least:

1. exact closed input and trigger paths;
2. pinned Python 3.13 and SymPy 1.14.0, hash/version gates;
3. q=3/q=4 calibration jobs and exact artifact handoff into both q=5 (`a=2,4`) jobs;
4. no local or bounded search masquerading as completeness; signed Schreier/kernel traversal remains uncapped and fail-closed;
5. strong calibration receipt binding from the repaired v3 producer, including negative fixtures;
6. terminal status/marker and artifact gates reject missing, partial, malformed, stale, or UNKNOWN evidence;
7. YAML parses, Python self-test/compile/help pass without running a full campaign;
8. resource caps cannot silently turn an incomplete traversal into PASS/A/B.

Write only `sol/luna_reply_157j_tuple_v3_workflow_audit.md`, with `PASS` or `FAIL`, blocker/high findings with line pins, file SHA-256 values, and exact static/self-test commands run.
