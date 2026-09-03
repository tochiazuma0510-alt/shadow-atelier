# Luna Task741 -- grade-two maps checker coverage-receipt v4

Role declaration: Luna.  Implement only the v490 finite checker receipt-key
repair.  Do not edit the producer, workflow, or mathematics; do not run the
actual 40-table build, git, or GHA.

Read fully:

- `sol/proof_r07_grade2_maps_coverage_receipt_schema_v490.md`
- `search/d972_r07_grade2_forward_adjoint_maps_v3.py`
- `search/check_d972_r07_grade2_forward_adjoint_maps_v3.py`
- `sol/sol_reply_736_audit_r07_grade2_maps_v3.md`

Create only:

- `search/check_d972_r07_grade2_forward_adjoint_maps_v4.py`
- `sol/luna_reply_741_r07_grade2_maps_checker_receipt_v4.md`

Requirements:

1. Copy checker v3 and keep its exact producer-v3 path/SHA and all independent
   arithmetic.  In `verify_coverage`, rename only the four source keys
   `source_tags/source_components/source_monomials/source_psl_indices` to the
   producer manifest schema `tags/components/monomials/psl_indices`.
2. Update only the corresponding checker selftest expected dictionary and
   version/checker marker constants required for a versioned output.  Preserve
   destination keys and every coverage value/check, parser, transpose,
   inverse, prefix, bool/type, roster, canonicality and mutation fixture.
3. Mechanically report all AST/top-level changes.  Add no dense allocation,
   retry, parallelism, scan or refactor.
4. Run py_compile and bounded SELFTEST with external pycache.  Do not run
   `--check` against an actual artifact.
5. Report exact bytes/LF/final-LF/SHA256 and
   `ACTUAL_MAP_CHECK=DEFERRED_TO_GHA`, `verified=false`.

