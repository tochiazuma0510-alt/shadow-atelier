# Sol(max) Task614: final static audit of Task601 selected-SLP extraction

Role: independent adversarial code and mathematical audit before the one GHA
run.  Read every numbered section of the following in full:

1. `sol/luna_task_601_r07_grade1_selected_slp_extraction_v1.md`;
2. `sol/luna_task_608_r07_grade1_selected_slp_unique_structure_repair_v1.md`;
3. `sol/proof_r07_canonical_selected_dependency_slp_v468.md`;
4. `sol/sol_reply_607_audit_r07_canonical_selected_dependency_slp_v1.md`;
5. `sol/proof_r07_canonical_selected_dependency_slp_physical_replay_v469.md`;
6. `sol/sol_reply_609_audit_r07_canonical_selected_slp_physical_replay_v1.md`;
7. the exact implementation quartet below.

Implementation receipts:

| file | SHA-256 |
|---|---|
| `search/d972_r07_a0_grade1_selected_slp_v1.py` | `7ef865a3f55741d8d4c06f66440f3234923d7134aead73ec4e17437a48dc0104` |
| `search/check_d972_r07_a0_grade1_selected_slp_v1.py` | `e6e368a204d24690c7be117c2afd019d92cbe3bc9b822cdceedf06311e5556b2` |
| `.github/workflows/d972-r07-a0-grade1-selected-slp-v1.yml` | `cc5ef08877c0380b40478b0d0ba4ef9e08a1f0c3299aab1d445cced322e8069d` |
| `sol/luna_reply_601_r07_grade1_selected_slp_v1.md` | `ad54bca1280910411d26b9a49d300144d3c6f0984d5e2e9631b75b3be9b54841` |

Write only `sol/sol_reply_614_audit_r07_grade1_selected_slp_v1.md`.
Do not repair code, proofs, workflows or v220.  Do not run production, GHA,
git or a full 8,059-row local route.  Tiny serial static/fixture checks are
allowed with cache outside the repository.

Return `PASS`, `PASS_AFTER_REPAIR`, or `FAIL`.  Check all of the following.

1. The producer reproduces the frozen 8,059 offers, ranks 1,661/5,044,
   basis and 3,317 MEMBER coefficients before export.  Normalization scales,
   coefficient-two signs, lower companions and old-connection lower links
   agree with v469.  Confirm that the formerly double-packed stored lower row
   is now emitted as an already packed row.
2. The canonical source graph is exactly the unique closure obtained from
   the selected physical origins.  There are no stale `structure.old/block`
   paths, missing defect/old expressions, scalar-cancellation pruning or
   alternate source records.
3. The derived traversal is bound in exact order to the Task595 roots.  For
   every grade/lower/block/defect/old state, compare the complete ordered
   child list, including the grade old-origin lower interval; no arbitrary
   middle child may survive.  The derived leaf map must follow from this
   flow and may not authenticate the canonical graph by itself.
4. The checker independently reroutes all 8,059 offers with the pinned
   standalone routing-v2 source and compares **all** lower/grade node records,
   ordered edges, scales, lower links, origin rows, stored rows, companions,
   old lower-zero rows and final basis.  Check the standalone source really
   is independent of the Task601 producer/serializer.
5. The selected physical replay reconstructs exact sealed old and block
   origins, lower rows and equally scaled companions before accepting the
   MEMBER equation.  It must not infer a source grade or relative-kernel
   class from physical zero.
6. Authentication, file sizes, acyclicity, bitsets, three roots, manifest
   flags and failure semantics are fail-closed enough for this one candidate
   run.  `direct_occurrence_replay=false` and
   `next_degree2_residual=null` must remain honest.
7. Inspect runtime and memory for avoidable work.  In particular confirm the
   four-entry block-owner cache, single `grade_basis_bytes`/`routed_basis`
   materializations, no per-origin block reload, no dense degree-two work,
   and no unbounded full-roster JSON beyond the selected source graph.  Flag
   only concrete blockers under the 60-minute/8-GiB workflow envelope; do not
   request a new framework.
8. The selftests must invoke the same source/transcript/root comparison cores
   as production and honestly report their limited mutation coverage.  The
   workflow pins the exact quartet, correct source/candidate runs, Python and
   NumPy versions, time/RSS limits, marker and artifacts.

State the smallest load-bearing repair if any.  This is a static release
audit, not an execution receipt, cross-check claim or Lean verification.
