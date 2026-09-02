# Sol task 516 -- independent audit of the final A4 production handoff

Role: independent Sol(max) implementation/provenance auditor.  This is a
bounded audit only: no production traversal, GHA, workflow, git, release, or
large computation.  Do not edit implementation files.

Read this full commission and the relevant Task503/511/512/513/514/515 replies.
Reply only to
`sol/sol_reply_516_audit_r07_a4_positive_schema_final_handoff_v1.md`.

## Frozen subjects

- producer v25: `search/d972_r07_word_independent_successor_kernel_v25.py`
  - 27075 bytes / `8e5c16f28113218485f7196c6873dbbf3ce17a0e03bd7daafe71bc6e8da5015f`
  - generated 286439 bytes / `e4fb7ead7e1dcfc5806574481f1e83e008991e516de20e2eb3a67753fec03098`
- checker v35: `crosscheck/check_d972_r07_word_independent_successor_kernel_v35.py`
  - 10246 bytes / `c8383a18169ec2da63e4e7a64de17f05d305c35e15393bcbb9e3c312ac6d5dd7`
  - generated 312553 bytes / `2ffcdede9a20acdd99bab3c4847db4c4a4f013e33fc151ac01b77f088d21df75`
- predecessor driver v45:
  `search/d972_r07_word_independent_successor_kernel_gha_driver_v45.g`
  - 12430 bytes / `d59bee6ea9a5366643d5409505ce25e91baa7c18031911eea36565e2f221782f`
- final driver v46:
  `search/d972_r07_word_independent_successor_kernel_gha_driver_v46.g`
  - 12544 bytes / `d3a864e47ebe0255221ccafee15b09925b2e1e462b21d8d0158c2d9c9e0f97e7`
- Task515 reply:
  `sol/luna_reply_515_r07_a4_positive_forbidden_schema_repair_v1.md`
  - 958 bytes / `9cf497052091109de6be3af829189eae7128dfcad3e69007ba34f9a728b74054`

## Required audit

1. Recompute every pin.  Check the transitive runtime prerequisites named by
   v25/v35/v46 exist with their internally pinned bytes/SHA values (including
   v24, v33, v34, v43, v44, and proof v430).
2. Independently extract the generated v25 and v35 sources without running a
   production CLI.  Establish from actual positive/resource constructors and
   checker predicates that both positive outputs use the exact five-key false
   dictionary
   `lift,fake,Ihara,base_pairs,ambient_E3_E4_enumeration`, while both RESOURCE
   outputs use the exact three-key false dictionary `lift,fake,Ihara`.
3. Establish mechanically that v46 differs from v45 in exactly two lines and
   only by extending producer-PASS and checker-PASS predicates to the exact
   five-key dictionary.  RESOURCE predicates must remain exact three-key.
   Reject padding, refactoring, changed gates, or additional semantic edits.
4. Re-run only bounded gates: v25/v35 source-pin info, v35 self-test, Python AST
   parse, and GAP `ReadAsFunction` parse for v46.  Inspect that v35 self-test
   reaches the real generated acceptance path and rejects the two re-sealed
   physical-history mutations identified by Task513, rather than trusting a
   helper boolean or prose marker.
5. By the exact v45-to-v46 diff plus direct inspection, confirm preservation of
   all v45 authority, release/member digest, regular-file/non-symlink,
   fresh-path, pipefail, single producer/checker, elapsed, timeout/RSS,
   terminal-cardinality, forbidden-token, JSON-claim, and generated-shell
   execution gates.  Confirm the driver does not introduce duplicate rebuilds,
   needless copies, self-test work, or any other operation that would slow the
   actual traversal.
6. Do not infer an A4 mathematical numerator.  A GO means only
   `GO_FOR_GHA_DISPATCH`; a RESOURCE result remains UNKNOWN_RESOURCE and a
   positive result still requires the independent checker and artifact audit.

Give a decisive `GO_FOR_GHA_DISPATCH` or `STOP_DO_NOT_ADOPT`, with exact
findings and the reply bytes/SHA-256.
