# Sol task 530 -- independent audit of A0 rank111-to-rank143 artifact

Role: Sol(max), independent bounded artifact/provenance auditor.  Do not run
production search, dispatch GHA, edit implementation, mutate git/releases, or
invent stronger mathematical claims.  Reply only to
`sol/sol_reply_530_audit_r07_a0_rank143_artifact_v1.md`.

## Frozen external identity

- workflow run `33579991982`, job `100092032846`;
- expected head `ae74e865ec7ba10d00eca263356afa01d23a2466`;
- completed conclusion `success`;
- artifact id `9831153395`, name `gap-run-out`, API size `121469`;
- service digest
  `sha256:6cf80ac0e37955174333f69a3e3b20c3026a957d12e20c2f53c29e1f2c62eeb9`;
- extracted outside the repository at
  `C:/Users/81905/AppData/Local/Temp/shadow-atelier-a0-33579991982-8968159ab3654d3c9d9e24831dc42aa8`.

## Frozen principal members

- result v11: 126799 /
  `8c7072c3702d281994a57ec9f18f9b02716c64b06ebd97841685f5903b47835d`;
- output checkpoint v11: 126377 /
  `dff9cb181ae40abfac23ccba1b7c819ad353ecbec3825e5922e944dbe4b41b4c`;
- producer log: 6737 /
  `5c5a886e7e060ee9f80d85f02a559b544cee0421be6f86142d98953a6914a654`;
- checker log: 51 /
  `aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1`;
- copied rank111 input checkpoint: 85934 /
  `69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93`;
- prior release ZIP: 37586 /
  `8b740dbbc81f5d2e659371a81453ded56c6711ce8ace35a4af5255303e0095de`;
- `driver.g`: 130 /
  `ee902189e30d6355e2be449a8a0b3f9af666943c86b011040ae674ca1c1fbefa`;
- `run.log`: 6837 /
  `596e8f35fad264d610474f0e9ea60684d389ffb8909ea5a19deb6b12d11a9eda`.

## Required audit

1. Query GitHub read-only and authenticate run, job, head and artifact.  Hash
   all extracted regular members and bind them to the exact executable pins at
   that head.  Record any correction to the frozen inventory explicitly.
2. Establish exact terminal cardinality: one producer RESOURCE terminal, one
   v7 independent-checker PASS and one v11 driver PASS; reject traceback,
   ERROR, UNKNOWN_INPUT, plain UNKNOWN, positive/A0/COMMON terminal or claim.
3. Parse input, result and output checkpoint independently.  Require exact
   input `rank/count/round = 111/68/73`, exact output
   `143/100/106` with last accepted round 105, byte/JSON equality of the first
   68 accepted records, and exactly 32 appended records with strictly
   increasing rounds greater than 73 and unit rank rises 111 through 143.
4. Recompute canonical state seals, binding, count/list equality and
   result-to-checkpoint durable-state binding.  Require the final current
   profile to have N1=N2=0, all tau coefficients zero, no unrecognized keys,
   target pair 1, rank 143 and the exact RESOURCE time-limit reason.  All
   A0/COMMON/NONMEMBER/fake/Ihara claims must be false.
5. Audit types, pivots and row/source distinctness to the frozen v7 contract.
   Authenticate that the exact pinned v7 checker executed in GHA; do not repeat
   a full local semantic replay.  Supplement it with exact prefix equality and
   round/rank-chain checks missing from that older checker if necessary.
6. Decide only whether this is a closed continuation-ready stable prefix.
   A GO promotes at most `100 literal rungs / rank 143 / round 105 accepted
   (checkpoint cursor round 106)`.  A0 remains `0/1 actual`; it declares no
   COMMON, lift, fake or Ihara witness.

Return exactly `GO_FOR_PREFIX_PROMOTION_AND_ARCHIVE` or
`STOP_DO_NOT_PROMOTE`, with evidence, commands, limitations and final reply
bytes/SHA supplied in the usual non-self-referential envelope.
