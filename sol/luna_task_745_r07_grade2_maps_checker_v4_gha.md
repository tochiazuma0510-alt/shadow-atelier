# Luna Task745 -- grade-two maps producer-v3/checker-v4 GHA wrapper

Role declaration: Luna.  Create the smallest inert workflow revision for the
audited receipt-key repair.  Do not edit implementation, run the actual maps,
git, push, or dispatch.

Read fully:

- `.github/workflows/d972-r07-grade2-maps-v3.yml`
- `search/d972_r07_grade2_forward_adjoint_maps_v3.py`
- `search/check_d972_r07_grade2_forward_adjoint_maps_v4.py`
- `sol/proof_r07_grade2_maps_coverage_receipt_schema_v490.md`
- `sol/luna_reply_741_r07_grade2_maps_checker_receipt_v4.md`
- `sol/sol_reply_744_audit_r07_grade2_maps_checker_v4.md`

Create only:

- `.github/workflows/d972-r07-grade2-maps-v4.yml`
- `sol/luna_reply_745_r07_grade2_maps_checker_v4_gha.md`

Requirements:

1. Adapt the v3 workflow to producer v3 unchanged (46,179 bytes, SHA
   `7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84`)
   and checker v4 (49,643 bytes, SHA
   `7ba94ee884db49bbe42d11a84228a6bdf7c88a3918407928af90c71b65fe4a29`).
2. Pin/authenticate v490 (1,412 bytes, SHA
   `e322c8e5546fc51e2d65e1fc85fa988bd92ce4475b3992aaf505fdfc668f48e4`),
   Task741 reply (2,792 bytes, SHA
   `cd73e4db862f5fbbc7972232ade9f560d607f203ee0862ff13ee4e072937b3f1`),
   and Task744 audit (9,111 bytes, SHA
   `b1e1a6fc307df0d417fcd718efa324009204081ed58d4fe7dbe44e6934a11a7c`).
   Require `VERDICT=PASS_GRADE2_MAPS_CHECKER_V4_SAFE_FOR_GHA` and
   `SAFE_TO_DISPATCH_GHA=yes` from the audit.
3. Preserve the 40-table exact sparse build, roster/EOF authentication,
   independent checker, false claim flags, timeout and bounded logs.  Use the
   producer V3 candidate marker and checker V4 PASS marker exactly.  Change
   temp/artifact/receipt names and receipt schema to workflow v4.
4. Leave `workflow_dispatch` only and no job-level fire condition.  Root will
   add one finite branch fire trigger after inspection.  Add no retry,
   parallelism, cache, dependency or new computation.
5. Parse YAML, scan relevant stale checker-v3/live-v3-workflow strings, and
   run only bounded selftests if necessary.  No real `--emit`/`--check`.
6. Report exact bytes/LF/final-LF/SHA256 and `REAL_GHA_RUN=NOT_RUN`,
   `verified=false`.

