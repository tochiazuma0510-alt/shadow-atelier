# Sol task 520 -- recursive clean-checkout A4 preflight audit

Role: independent Sol(max) implementation/provenance auditor.  This audit is
specifically to prevent another one-gate-at-a-time redispatch.  No production
search, GHA/workflow dispatch, git mutation, release mutation, or implementation
edit.  Reply only to
`sol/sol_reply_520_audit_r07_a4_recursive_clean_preflight_v1.md`.

## Trigger and frozen additions

Run `33578182231`, job `100086613280`, exact v47 head
`5b379c7c5a39e15be7205e298167e3c0389480e8`, passed the repaired realpath and
then failed before curl/producer because v24 could not open untracked v23.
The two missing immediate owner links are now included in the commissioned
subject checkout:

- producer v23: 14472 /
  `d9c082570cfa5c52254e159cd91ad0e722e5ad0ee1ea2c52e8161c2729ee1d9a`
  and its owner v22 is tracked at 4055 /
  `0186a8711ae356d1d01d7ccbd4e618ec5d19fa36442812a5dcfa8c452837d2c2`.
- checker v32: 10036 /
  `8582b707cc63a965d0eef55a9df5d514b0601afee68118dddba236765034ffa0`
  and its owner v31 is tracked at 19483 /
  `7efc8609bc7632b1705e2928228fa0269f3272f81ed0b4128468d27639eecf8e`.

The v47 and Task519 pins/verdict remain 12536 /
`ba74cd1bb09bb87b50c582330bf54f943a5c4c1c77522a518460acf76a5748aa`
and `GO_FOR_GHA_REDISPATCH`.

## Required exhaustive bounded audit

1. Query run `33578182231` read-only and confirm exact failure ordering:
   realpath passed; v25 source-pin load failed only at absent v23; curl,
   release extraction and producer were not reached.
2. Recursively follow every executed owner/source load starting from v25
   `--source-patch-info` and v35 `--source-patch-info` until the first genuine
   generated base.  Record the full chain and prove every file is present in
   the subject git tree at its parent-pinned bytes/SHA.  Do not stop after one
   level.  Check for dynamically constructed repo paths as well as literal
   OWNER tuples.
3. Export the commissioned git tree with `git archive` into a fresh
   repository-external temporary directory, so no untracked workspace file can
   satisfy a load.  In that clean export run both exact source-patch-info
   commands and v35 self-test.  They must pass with the frozen generated
   v25/v35 hashes.
4. Starting from Task519's exact reconstructed v47 shell, make an external
   audit-only preflight copy truncated at the first producer launch (replace
   the producer start with a unique PASS marker and exit while no conditional
   is open).  In the clean export run that copy through every preceding line:
   realpath, all wrapper/generated/predecessor/proof pins, five authority
   regular-file gates, caps, release download/digest, exact six-member unzip,
   copy, and post-copy pins.  Do not invoke producer or checker.  Require exact
   evidence that the unique preflight marker is reached and no earlier command
   fails.
5. Inspect all commands after the cut statically against Task516/519 so the
   preflight does not weaken the frozen production shell.  Confirm no other
   repo-local runtime dependency is absent from the committed tree.

Return `GO_FOR_GHA_REDISPATCH_CLEAN_PREFLIGHT` or `STOP_DO_NOT_REDISPATCH`,
with exact subject head, chains, command evidence and reply bytes/SHA-256.
GO is transport-only and promotes no A4 claim.
