# Luna Task659 — Task640 v4 inert-line repair only

Task658 found that the uncommitted v4 workflow reports an inert guard but its
lines 39--41 omit `false &&`. Repair exactly this one release blocker.

Authorized files only:

- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v4.yml`
- `sol/luna_reply_657_r07_task640_artifact_root_path_v4.md`
- new `sol/luna_reply_659_r07_task640_v4_inert_line_repair.md`

Insert `false &&` immediately before the existing workflow-dispatch/fire
predicate, preserving YAML folding and every other byte except consequent
hash receipts in reply657. Do not alter the four Task625 nested payload paths,
labels, code, parents, caps, actions, or any Python file. Do not dispatch.

Run safe YAML parse, exact v4-v3 normalized diff census, fixed-string inert
check, and action/hash-pin scan. Report exact paths/bytes/LF/SHA-256 and prove
that deleting this line is the only implementation delta from Task657. End
with `READY_FOR_TASK660_FINAL_PATH_AUDIT` or `NOT_READY`. No GHA/git.
