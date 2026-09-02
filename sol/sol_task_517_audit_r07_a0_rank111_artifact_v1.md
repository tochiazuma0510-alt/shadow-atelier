# Sol task 517 -- independent audit of A0 rank98-to-rank111 artifact

Role: independent Sol(max) artifact/provenance auditor.  Bounded audit only;
no production search, GHA dispatch, git, release upload, or implementation
edits.  Reply only to
`sol/sol_reply_517_audit_r07_a0_rank111_artifact_v1.md`.

## Frozen external identity

- workflow run `33564845217`, job `100045550767`
- expected head `c582f8d786012a668783790007b72c5c422c3db8`
- workflow conclusion `success`
- artifact id `9826862037`, name `gap-run-out`, API size `96198`
- API digest
  `sha256:22aa0d836298e01fa27b2d893427839b18fe51a83781a840d357a1243e6d412c`
- already downloaded outside the repository at
  `C:/Users/81905/AppData/Local/Temp/shadow-atelier-task517-rank98-9826862037`

## Frozen principal members

- result v10: 86354 /
  `39434b6a4c1a7851805c2deb3be8de4e7e919085a537b8d3913a15d341c19279`
- output checkpoint v10: 85934 /
  `69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93`
- producer log: 4905 /
  `271d05e70153cbceadf9d45478a4357bcd7899610b3857b3525644205b7e975c`
- checker log: 51 /
  `aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1`
- copied rank98 input checkpoint: 69947 /
  `c0fcb581f59c9ed665cf13cb852cb527ef13acdc9bf2102b89c2404bb080d37f`
- downloaded prior release zip: 30758 /
  `d0293cdd3bab98b792af17064ace21594966a5610e30219842347466e9ade9e4`
- run log: 5004 /
  `ac7fcf963237cc23d88774df9c85d82cb8b3acc09f24b0ee4dda5506e719bf15`

## Required audit

1. Query the GitHub API read-only and recompute all above identities and all
   extracted member hashes.  Reject a head/run/artifact mismatch.
2. Establish exact terminal cardinality: one producer RESOURCE terminal, one
   independent v7 checker PASS, and one v10 driver PASS; reject ERROR,
   Traceback, UNKNOWN_INPUT, plain UNKNOWN, or a positive/A0 claim.
3. Parse result, output checkpoint and copied input checkpoint independently.
   Check that input is exactly rank/count/round `98/55/59`; output is exactly
   `111/68/73`; the first 55 accepted sources are byte-for-byte/JSON-equal and
   13 sources are appended; all accepted-source records are well typed and
   distinct as required by the frozen checker contract.
4. Recompute canonical checkpoint state seals, binding, count/list equality,
   and the result-to-checkpoint durable-state/terminal-replay bindings.  Check
   terminal reason is exactly
   `UNKNOWN_RESOURCE:tau_free_formula_seed:time_limit` and all
   A0/COMMON/NONMEMBER/fake/Ihara claims are false.
5. Independently rerun the frozen v7 checker on the result and inspect that it
   is the pinned checker used by the v10 driver.  Supplement its rank68 base
   check with the explicit rank98 prefix equality required above; do not rely
   only on the uploaded log.
6. Determine whether the checkpoint is a closed, continuation-ready stable
   prefix suitable for permanent archival.  A GO may promote only the stable
   prefix to `68 literal rungs / rank 111 / round 73`; A0 remains `0/1 actual`
   and no COMMON/NONMEMBER/lift/fake/Ihara witness is declared.

Return `GO_FOR_PREFIX_PROMOTION_AND_ARCHIVE` or `STOP_DO_NOT_PROMOTE`, with
exact evidence and reply bytes/SHA-256.
