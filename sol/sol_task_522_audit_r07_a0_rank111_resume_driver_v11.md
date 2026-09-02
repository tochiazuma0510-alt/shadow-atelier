# Sol task 522 -- independent A0 rank-111 continuation-driver audit

Role: independent Sol(max) implementation/provenance auditor.  Audit only;
do not edit implementation, run production, dispatch GHA, mutate git/releases,
or write anywhere except
`sol/sol_reply_522_audit_r07_a0_rank111_resume_driver_v11.md`.

The commissioned exact subject commit is
`dcd1b29e` (`sol: prepare A0 rank111 continuation driver`).  Resolve and
record its full SHA.  The candidate driver is
`search/d972_r07_a0_actual_tau_free_rank111_resume_gha_driver_v11.g`,
reported as 8683 bytes / SHA-256
`84db6c150d8ce764c411afa91a9cc9c31ad193ecaf719900faa9ebdbc32b5b7d`.
Its sole implementation owner is rank98 driver v10, 8662 bytes / SHA-256
`8903f315e26b909791dead7673c4eef358c3cca7a2ddba7871476a477d8c3d1e`.

## Required bounded audit

1. Export the exact subject tree with `git archive` to a fresh
   repository-external directory.  No untracked workspace file may satisfy a
   dependency.  Recompute subject/owner/producer/checker bytes and hashes.
2. Parse/load v11 without production.  Reconstruct its generated shell and
   require `bash -n` success.
3. Mechanically classify every v10-to-v11 diff.  Confirm that producer,
   checker, 7200-second/4.8-GB/64-rise computation, checker timeout and
   positive/RESOURCE semantics are unchanged; only versioned names, source
   identity, archive manifest, checkpoint member and output paths changed.
4. Independently query/read the permanent release asset and confirm archive
   bytes/SHA, exactly eight flat unique regular members, no extras, and every
   member's commissioned bytes/SHA.  Confirm source run/job/head/API artifact
   metadata are the frozen values in Task521.
5. Execute an audit-only copy of the exact generated shell through every
   pre-producer command, replacing the producer launch with one unique PASS
   marker and exit while no conditional is open.  This must actually download,
   authenticate, unzip, and copy the archive in the clean export.  Prove the
   copied resume input is member 5
   `d972_r07_a0_actual_tau_free_rank_ladder_v10_output.checkpoint`
   (85934 / `69a7ec3d...dfd93`) and not member 1.  Do not invoke producer or
   checker.
6. Check statically that a real GHA invocation with preamble
   `D972_R07_A0_RANK111_CHECKPOINT_RESUME_V11_RUN:=true;;`, `ci/out`, no
   optional p-quotient packages, and a sufficient job timeout reaches the
   exact v11 production command and later exact v7 checker command.  Check for
   stale-output, quoting, path, `pipefail`, timeout, memory-cap and upload-file
   compatibility defects.

Return exactly one verdict:

- `GO_FOR_GHA_DISPATCH_RANK111_CONTINUATION`, or
- `STOP_DO_NOT_DISPATCH`.

GO is transport/implementation authorization only.  It promotes no new A0
row, COMMON, compatible lift, fake, or Ihara claim.  Include exact evidence,
full subject SHA, and reply bytes/SHA-256.
