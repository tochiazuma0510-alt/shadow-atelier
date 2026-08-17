# Luna reply 157h — tuple-v3 staged workflow

Modified exactly the authorized files:

- `.github/workflows/d972-burau-tuple-v3.yml`
- `sol/luna_reply_157h_tuple_v3_workflow.md`

The new workflow provides:

- exact-branch push trigger with closed paths for the workflow, v3 producer,
  and frozen word artifact;
- credential-free checkout, read-only contents permission, six-hour jobs,
  12GB virtual-memory ceiling, `fail-fast: false`, and attempt-unique
  always-uploaded artifacts;
- pinned Python `3.13.5` and SymPy `1.14.0`, with runtime version gates;
- independent q3/q4 selftest-first calibration jobs and exact receipt gates
  for schema, status, orders, ordered rows, unique keys, and complete fibers;
- dependent q5 a=2/a=4 matrix jobs downloading both calibration artifacts;
  the v3 producer performs its strong source/hash/evidence unlock;
- q5 receipt/status/row gates accepting only candidate or all-pass UNKNOWN;
  `UNKNOWN_RESOURCE` is explicitly rejected as job success while evidence is
  still uploaded.

Static evidence:

- `YAML_PARSE_PASS`
- `WORKFLOW_STATIC_CLOSED_INPUT_STAGE_ARTIFACT_PASS`
- `git diff --check` was run; it reports only pre-existing trailing whitespace
  in unrelated `search/probe/wac_v1/scan_out.txt`.
- workflow SHA256:
  `16C7DB1B1D2C651C8790455C16EE1C0D412AFDF6C471FE08424D60E2AD173AAF`

No producer, other workflow, local/full calculation, GAP, GHA, or git action
was run. Runtime uncertainty remains the exact Schreier/kernel computation,
runner memory/time, and dependency-install availability; all such stops remain
non-mathematical failures with artifacts retained.
