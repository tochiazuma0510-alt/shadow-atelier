# Luna Task747 -- P1 semantic producer-v5/checker-v3 GHA rerun

Role declaration: Luna.  Create the smallest workflow revision of the accepted
Task729 phase DAG for the audited literal-LF repair.  Do not edit code, run the
actual five parents, use git, push, or dispatch.

Read fully:

- `.github/workflows/d972-r07-p1-componentwise-semantic-v1.yml`
- `search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py`
- `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v3.py`
- `sol/proof_r07_p1_equality_literal_lf_repair_v489.md`
- `sol/luna_reply_740_r07_p1_equality_literal_lf_v5.md`
- `sol/sol_reply_743_audit_r07_p1_equality_lf_v5.md`

Create only:

- `.github/workflows/d972-r07-p1-componentwise-semantic-v2.yml`
- `sol/luna_reply_747_r07_p1_semantic_v2_gha.md`

Requirements:

1. Copy the v1 workflow DAG and change only the release boundary needed for:
   producer v5, 41,619 bytes / 382 LF / SHA
   `dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf`;
   checker v3, 130,683 bytes / 2,689 LF / SHA
   `3cfdbe0485711b9b4a08db2d664ded7719a126e3a499724d33cd122a101e774e`.
   Preserve all five Task554 artifact IDs/digests, ranks, time/RSS caps,
   prepare -> four parallel blocks -> join -> independent checker structure,
   exact six positional receipt arguments, canonical gates and false flags.
2. Retain the earlier Task721 and Task726 audit pins.  Additionally pin and
   authenticate v489 (2,771 bytes / 69 LF / SHA
   `14e4d33967cea1a26d1cb41c11ab125abad2cc9d5455e3c85e0377987832c789`),
   Task740 reply (3,340 bytes / 75 LF / SHA
   `512d480ce007a2573eaf6ec8fa9fbbb3623a741d08000e33edef16f23c0dfe1a`),
   and Task743 audit (12,090 bytes / 228 LF / SHA
   `a3b4a3719c6464b795a2e0a935d1366cd727674aad39609f193af271a422377f`).
   Require exact audit tokens
   `VERDICT=PASS_P1_EQUALITY_LF_V5_SAFE_FOR_GHA` and
   `SAFE_TO_DISPATCH_GHA=yes`.
3. Preserve the checker's actual marker
   `R07_GRADE2_P1_COMPONENTWISE_INDEPENDENT_CHECKER_V1_PASS`; its versioned
   source changed only the producer provenance pin.  Do not invent a new
   arithmetic/schema marker.  Update any workflow-only release label to v3
   only if it is explicitly non-authoritative.
4. Keep existing internal temp/artifact labels if changing them risks the
   dependency DAG; run IDs already make artifacts unique.  Change the workflow
   name to v2 and arm only the existing branch/path push trigger with fire tag
   `[fire-r07-p1-semantic-v2]` on every job, so it runs only when root commits
   that marker.  Root remains the sole broker.
5. Add no retries, caches, matrix assembly, new computations or extra replay.
   The prepare phase must still fail closed unless the corrected v5 equality
   literals match its freshly reconstructed records.
6. Parse YAML and statically check all jobs use v5/v3 pins and the v2 fire tag.
   Run bounded selftests only; no actual prepare/block/check.
7. Report exact bytes/LF/final-LF/SHA256 and `REAL_GHA_RUN=NOT_RUN`,
   `verified=false`.

