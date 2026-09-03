# Luna Task739 -- finite grade-two maps v3 GHA wrapper

Role declaration: Luna.  Create the smallest inert workflow revision that runs
the independently audited v3 producer/checker.  Do not run git, push, dispatch,
or perform the real map build.  Do not edit implementation files.

Read fully:

- `.github/workflows/d972-r07-grade2-maps-v2.yml`
- `search/d972_r07_grade2_forward_adjoint_maps_v3.py`
- `search/check_d972_r07_grade2_forward_adjoint_maps_v3.py`
- `sol/sol_reply_736_audit_r07_grade2_maps_v3.md`
- `sol/luna_reply_733_r07_grade2_maps_nonphysical_coverage_v3.md`

Create only:

- `.github/workflows/d972-r07-grade2-maps-v3.yml`
- `sol/luna_reply_739_r07_grade2_maps_v3_gha.md`

Requirements:

1. Mechanically adapt the accepted v2 workflow to v3.  Pin exact inputs:
   producer 46,179 bytes / SHA
   `7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84`;
   checker 49,727 bytes / SHA
   `d334b3cea69a2505a5c57794cedb9f40701881bf2801757606491dcd5d6feec6`;
   audit 6,467 bytes / SHA
   `de9f285340e12fc2b40046c928d94fe9b6dea914de38f5f141aeffc2452ec603`.
   Require exact audit tokens `PASS_GRADE2_MAPS_V3_SAFE_FOR_GHA` and
   `SAFE_TO_DISPATCH_GHA=yes`.
2. Replace all v2 schemas, markers, paths, temp names, artifact names, and
   receipt schema with v3.  Preserve the exact 40-table roster, sparse emit,
   independent check, false claim flags, canonical EOF gates and bounded logs.
3. Leave the workflow inert: `workflow_dispatch` only, with no push trigger.
   Root will add one finite fire trigger after inspection.  Keep pinned action
   SHAs and Python 3.13.
4. Do not add matrix parallelism, retries, caches, setup, dependency installs,
   or new tests.  The failed v2 actual run emitted all maps in about ten
   seconds; this wrapper is only the finite tuple-index rerun.
5. Statically parse the YAML and scan for stale v2 strings.  Run only bounded
   v3 selftests (or cite Task736 if no rerun is needed); no actual `--emit` or
   `--check`.
6. Report exact bytes/LF/final-LF/SHA256 of both files, commands and
   `REAL_GHA_RUN=NOT_RUN`, `verified=false`.

