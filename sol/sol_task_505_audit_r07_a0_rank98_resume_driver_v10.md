# Sol(max) task 505 - audit A0 rank-98 resume driver v10

Role: independent Sol(max) implementation auditor.  Audit only Task504's
rank-98 continuation driver before GHA dispatch.  This is a bounded dispatch
gate, not a request for new architecture or extra SELFTEST machinery.  Do not
edit the driver, producer, checker, workflow, mathematics or any other file;
do not run production, GHA or git.  Write only
`sol/sol_reply_505_audit_r07_a0_rank98_resume_driver_v10.md`.

Read Task504 and its reply in full.  Do not trust its prose or fixtures.

## 1. Frozen subject

- driver `search/d972_r07_a0_actual_tau_free_rank98_resume_gha_driver_v10.g`,
  8662 /
  `8903f315e26b909791dead7673c4eef358c3cca7a2ddba7871476a477d8c3d1e`;
- Task504 reply, 3410 /
  `89271e329e104a3a5269103674e8f2b25e9870c3ad180bc3f7b9ff59a3787640`;
- permanent source release, 30758 /
  `d0293cdd3bab98b792af17064ace21594966a5610e30219842347466e9ade9e4`:
  `https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9821857621_gap-run-out.a0-rank98.zip`.

A pin mismatch is an immediate STOP.

## 2. Exact audit question

Decide whether the frozen v10 driver is safe to dispatch as a surgical
continuation of the cross-checked v9 output checkpoint at rank/count/round
`98/55/59`.

Independently establish all of the following:

1. The permanent ZIP has exactly the eight flat members recorded in Task504,
   with every byte count and SHA-256 matching, and the copied resume member is
   exactly the 69,947-byte v9 output checkpoint, not the v9 input checkpoint.
2. Independently parse the checkpoint and confirm its binding/state SHA,
   rank/count/round `98/55/59`, 55 accepted sources, and equality of its first
   41 accepted sources with the archived old input prefix.
3. The driver authenticates the release, exact member set, every member,
   producer v3 and checker v7 before starting computation; its fresh-path and
   symlink gates fail closed.
4. There is exactly one real producer call followed by exactly one independent
   checker call.  The producer invocation remains
   `--seconds 7200 --rss-bytes 4800000000 --max-rises 64`, with external
   timeout 7500 seconds and `ulimit -v 5200000`; the checker timeout remains
   3600 seconds.  There is no retry, worker pool, hidden SELFTEST, old-prefix
   re-search, or duplicate large-state copy.
5. The successful path requires nonempty result/checkpoint, exactly one typed
   producer terminal and exactly the one-line v7 checker PASS, and ends with
   exactly `R07_A0_RANK98_CHECKPOINT_RESUME_V10_DRIVER_PASS`.  UNKNOWN,
   RESOURCE, ERROR, Traceback, stale output and a failed producer/checker
   cannot be promoted.
6. A bounded v9-to-v10 diff is confined to the immutable source release/member
   binding, v10-owned paths, preamble and markers.  Producer/checker pins,
   search order, mathematics and resource limits are unchanged.
7. GAP `ReadAsFunction` and generated shell `bash -n` pass.  Independently
   exercise only a tiny fail-closed preflight mutation/fixture; do not execute
   the real producer or checker.

Do not reject merely because a fully coordinated replacement with all pinned
hashes rewritten would be outside a local content-addressed trust boundary.
The parent will bind the adopted commit SHA and actual GHA run/artifact ids.
Do reject any actual production-path defect, unnecessary memory amplification,
unbounded preliminary work, or mismatch with the frozen rank-98 checkpoint.

## 3. Verdict

Return `GO_FOR_GHA_DISPATCH` only if every gate above passes.  Otherwise return
`STOP_DO_NOT_DISPATCH` with the smallest exact reproducer and minimal repair.
Neither verdict is A0 progress: A0 stays `0/1 actual` until a production result
is independently checked.

End with exactly one of:

`TASK505_R07_A0_RANK98_RESUME_DRIVER_V10_AUDIT_GO`

or

`TASK505_R07_A0_RANK98_RESUME_DRIVER_V10_AUDIT_STOP`
