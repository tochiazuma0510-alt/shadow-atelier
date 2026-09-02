# Luna task 521 -- A0 rank-111 checkpoint continuation driver v11

Role: Luna implementation support.  This is a narrow transport/versioning
task.  Do not change the mathematical producer/checker, do not run the
production search, do not dispatch GHA, and do not perform any git or release
mutation.

Write only:

- `search/d972_r07_a0_actual_tau_free_rank111_resume_gha_driver_v11.g`
- `sol/luna_reply_521_r07_a0_rank111_resume_driver_v11.md`

Use
`search/d972_r07_a0_actual_tau_free_rank98_resume_gha_driver_v10.g`
(8662 bytes, SHA-256
`8903f315e26b909791dead7673c4eef358c3cca7a2ddba7871476a477d8c3d1e`)
as the sole implementation owner.  Preserve its computation semantics,
resource controls, producer/checker invocations, 7200-second producer limit,
4.8 GB cap, `--max-rises 64`, and 3600-second checker limit.  Change only the
source-run/archive/checkpoint identity, the rank111/v11 output names, and the
corresponding mode/version marker needed to continue from the promoted rank
111 prefix.

## Frozen source identity

- source run: `33564845217`
- source job: `100045550767`
- source head: `c582f8d786012a668783790007b72c5c422c3db8`
- artifact id/name/API bytes:
  `9826862037` / `gap-run-out` / `96198`
- permanent flat archive URL:
  `https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9826862037_gap-run-out.a0-rank111.zip`
- archive bytes/SHA-256:
  `37586` /
  `8b740dbbc81f5d2e659371a81453ded56c6711ce8ace35a4af5255303e0095de`

The archive must be treated as an exact eight-member flat archive.  Pin every
member by bytes and SHA-256 and reject extras, omissions, directories, duplicate
names and non-regular members:

1. `d972_r07_a0_actual_tau_free_rank98_resume_v10_input.checkpoint`
   69947 /
   `c0fcb581f59c9ed665cf13cb852cb527ef13acdc9bf2102b89c2404bb080d37f`
2. `d972_r07_a0_actual_tau_free_rank98_resume_v10_preflight.log`
   38 /
   `52f94358c40a2e6968927b4078a0bf00b6a40c32eb013367679e8d59b599240c`
3. `d972_r07_a0_actual_tau_free_rank_ladder_v10.json`
   86354 /
   `39434b6a4c1a7851805c2deb3be8de4e7e919085a537b8d3913a15d341c19279`
4. `d972_r07_a0_actual_tau_free_rank_ladder_v10_checker.log`
   51 /
   `aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1`
5. `d972_r07_a0_actual_tau_free_rank_ladder_v10_output.checkpoint`
   85934 /
   `69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93`
6. `d972_r07_a0_actual_tau_free_rank_ladder_v10_producer.log`
   4905 /
   `271d05e70153cbceadf9d45478a4357bcd7899610b3857b3525644205b7e975c`
7. `driver.g`
   128 /
   `393794cf2188ac0a27abe472180ddabca42e7f88082248726e4ae664cd371978`
8. `run.log`
   5004 /
   `ac7fcf963237cc23d88774df9c85d82cb8b3acc09f24b0ee4dda5506e719bf15`

The actual resume input is member 5, the promoted output checkpoint.  Copy it
to a v11/rank111 input name and pin the copied file before launching the
producer.  Do not accidentally resume from member 1.

Keep the frozen computation owners unchanged:

- producer `search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py`
  12215 /
  `0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37`
- checker `crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v7.py`
  3653 /
  `e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1`

## Required bounded tests

1. GAP syntax/load test of v11 with production execution prevented.
2. Reconstruct the generated shell outside the repository and run `bash -n`.
3. Run a transport-only fixture outside the repository that proves the exact
   eight-member manifest and that member 5, not member 1, becomes the resume
   input.  Do not run the producer or checker.
4. Diff v10 versus v11 and enumerate every semantic change; reject any change
   outside the frozen transport/version substitutions above.

Reply with candidate status, exact commands/evidence, driver bytes/SHA-256,
and a definitive `READY_FOR_INDEPENDENT_AUDIT` or `STOP` verdict.
