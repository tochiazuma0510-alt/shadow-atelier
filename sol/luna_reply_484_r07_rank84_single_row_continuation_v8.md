# Luna reply 484: rank-84 single-row continuation v8

Status: **IMPLEMENTED / BOUNDED GATES PASS / PRODUCTION NOT RUN**

Created only the requested driver and this reply.  The driver requires the
external preamble
`D972_R07_A0_RANK84_CHECKPOINT_RESUME_V8_RUN:=true;;` and preserves the pinned
Task461 producer/checker lane.

## Immutable bindings

```text
run                 33524681526
job                 99912387760
head                dd67f12b0ee4f022061df27ed396ad3d3a37f264
artifact            9812928957 (gap-run-out)
API zip sha256      4b3239f35f6ec2a4859e6a81e2b49456702f0f22f695a7332089b407dbcb817d
source state        UNKNOWN_RESOURCE:tau_free_localized_dual:time_limit
source rank/count   84 / 41
source round        44
source state sha256 3c38d9021e20c04a24e99136e47902e8911658f244a202f9c49f4a4280e2f6a7
release URL         https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9812928957_gap-run-out.rank84.zip
release bytes       23004
release sha256      dde60bad768e20ead6ad08e8bd0a8e53fc97050a43f6c207552ba97d579c438a
producer bytes      12215
producer sha256     0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37
checker bytes       3653
checker sha256      e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1
resume bytes        52707
resume sha256       eb1a6d69a855b88d2a934dbf8e58c0f539a7a4d6802cc4a5c7f544b0880da24
```

The seven release members were independently inspected outside the repository
and are authenticated again by the driver after extraction:

```text
d972_r07_a0_actual_tau_free_rank68_input_v1.checkpoint       33015 73ad85624d079d01ecc824ab6adc699c51b0dabfddcc36c0f7d2bd4384f7d5a4
d972_r07_a0_actual_tau_free_rank_ladder_v7.json              53125 97dfa69864c95f1a3ec7dc5428fcceee50d9eaa1ea07f5cabb0fb8df8c27b59
d972_r07_a0_actual_tau_free_rank_ladder_v7_checker.log         51 aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1
d972_r07_a0_actual_tau_free_rank_ladder_v7_output.checkpoint 52707 eb1a6d69a855b88d2a934dbf8e58c0f539a7a4d6802cc4a5c7f544b0880da24
d972_r07_a0_actual_tau_free_rank_ladder_v7_producer.log       5179 475d51fa9af4a498ab92125ad7b59058ef372fafb890204530989970ff3e7513
driver.g                                                        124 f521a63c21f940c7ebc44665606995acb45464ef9e7ca4606630875bda0eb01c
run.log                                                         5277 11856023c568b25066b1604eb3fc8dc1879413bfd439bad5ef658f0f2571788f
```

## Driver contract

- Downloads the permanent release with `curl --fail --location`, verifies its
  23,004-byte SHA-256, extracts into a fresh owned `ci/out` archive directory,
  authenticates the seven-member manifest, and copies the exact rank-84
  checkpoint into a fresh `ci/out` resume path with a second byte/SHA check.
- Runs exactly one producer with `--seconds 7200 --rss-bytes 4800000000
  --max-rises 64`.  The foreground producer supervisor is `7500s`; the shell
  VM limit is `ulimit -v 5200000`, i.e. 5,324,800,000 bytes, strictly above
  4,800,000,000 bytes.  The checker has its own `3600s` foreground cap.
- Runs exactly one v7 checker on the fresh producer result, requires nonempty
  result/checkpoint files, one producer terminal marker, and exactly one
  `R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V7_CHECKER_PASS`.  The driver marker is
  `R07_A0_RANK84_CHECKPOINT_RESUME_V8_DRIVER_PASS`.
- Uses `set -euo pipefail`; a workflow-success or `UNKNOWN_RESOURCE` status is
  never emitted or interpreted as an A0 completion marker.

## Bounded gates

Passed:

1. Source/release/checkpoint byte and SHA pin checks.
2. ASCII and final-newline check for the driver (`7680` bytes, SHA-256
   `ea4794dbe13e751e661804de238553b5607120c2f04d498fcc2a88fdaaed3edb`).
3. `python3 -u -B` cardinality is exactly two (one producer and one checker);
   the requested producer arguments, pipefail, fresh paths, release/member
   checks, markers, and strict resource margins are present.
4. `& .\gap.ps1 search\d972_r07_a0_actual_tau_free_rank84_resume_gha_driver_v8.g`
   reached the expected `Error, task484 external preamble required` guard with
   exit code 1.
5. GAP `ReadAsFunction` parsing through a temporary external wrapper emitted
   `TASK484_GAP_READASFUNCTION_PARSE_PASS`; the driver body was not evaluated.

No production producer/checker, GHA dispatch, workflow edit, git operation, or
bytecode cache was run.  The rank-84 `UNKNOWN_RESOURCE` state remains a
cross-checked continuation input, not a COMMON/A0 completion.

TASK484_R07_RANK84_SINGLE_ROW_CONTINUATION_V8_PASS
