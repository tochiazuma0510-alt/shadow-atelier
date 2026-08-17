# Luna reply 157e — matrix trigger closure

Modified exactly the authorized files:

- `.github/workflows/d972-burau-matrix-v1.yml`
- `search/d972_b4_burau_matrix_v1.g`
- this reply

Repairs applied only:

- Added the dynamically loaded worker and four helper sources to
  `on.push.paths`, while retaining the exact branch and existing trigger
  paths:
  `search/d972_dovetail_worker_v1.g`,
  `search/probe/wac_v1/gap_output_prelude.g`,
  `search/gaplib_common.g`,
  `search/week3-battery-common.g`, and
  `search/week3-psl-common.g`.
- Replaced only the prime-field receipt encoder's `Int(x)` with documented
  `IntFFE(x)`; the explicit GF(4) encoding remains unchanged.

Static evidence:

- `YAML_PARSE_PASS`
- `PATH_CLOSURE_AND_INTFFE_PASS`
- `DYNAMIC_SOURCE_PATHS_EXIST_PASS`
- `git diff --check` was run. It reports only pre-existing trailing whitespace
  in unrelated `search/probe/wac_v1/scan_out.txt`; no authorized-file change
  introduced trailing whitespace.
- workflow SHA256:
  `E4DBA1A160852B22392F8EBC96E9DF9A76E8D45730DB9030D564BD37B7D7CE4B`
- producer SHA256:
  `3EB4975ED2B5721634868004CF3B1B7DB25B3D709DA5679E891054765F0BD728`

No local GAP, workflow, GHA, or git operation was run.
