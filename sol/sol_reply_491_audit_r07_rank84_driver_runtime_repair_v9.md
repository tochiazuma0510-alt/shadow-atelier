# Sol audit 491: rank-84 driver runtime repair v9

Verdict: the immediate dispatch envelope is sound. The audited v9 driver is
exactly 8,257 bytes with SHA-256
`d89cac926cfd3a0b44d0a3564e73c608035f6389f9240452d0017aa126156fd9`.

## v8 failure and the complete repair set

I generated the v8 shell through GAP, replaced both real process invocations
with fail-closed sentinels, and ran it with xtrace in an external fresh
temporary directory. It exited 1 before either sentinel. The first failure
was exactly the JSON-member comparison:

```sh
test "$(sha256sum "ci/out/d972_r07_a0_actual_tau_free_rank84_resume_v8_archive/d972_r07_a0_actual_tau_free_rank_ladder_v7.json" | cut -d " " -f1)" = "97dfa69864c95f1a3ec7dc5428fcceee50d9eaa1ea07f5cabb0fb8df8c27b59"
```

The trace compared the actual 64-character digest ending `b59b` with the
63-character literal ending `b59`. Exhaustive quoted-hex inspection found
exactly three truncated SHA literals in v8:

1. line 30, resume-copy pin: `...da24` instead of `...da24f`;
2. line 33, JSON member pin: `...b59` instead of `...b59b`;
3. line 35, checkpoint member pin: `...da24` instead of `...da24f`.

V9 has no non-64-character SHA literal (apart from the intentional 40-character
git head). Its SHA multiset differs from v8 only by replacing the JSON value
once and the checkpoint value twice with those full values. Producer/checker
paths, pins and arguments are unchanged; the other changes are the required
fresh v9 paths, task/driver labels, and owned diagnostic envelope. No
mathematics drift was found.

## Immutable bindings and archive replay

The driver contains the exact guarded source binding:

```text
run       33524681526
job       99912387760
head      dd67f12b0ee4f022061df27ed396ad3d3a37f264
API SHA   4b3239f35f6ec2a4859e6a81e2b49456702f0f22f695a7332089b407dbcb817d
URL       https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9812928957_gap-run-out.rank84.zip
release   23004 dde60bad768e20ead6ad08e8bd0a8e53fc97050a43f6c207552ba97d579c438a
```

The permanent asset was downloaded afresh and its seven extracted members
recomputed as:

```text
d972_r07_a0_actual_tau_free_rank68_input_v1.checkpoint       33015 73ad85624d079d01ecc824ab6adc699c51b0dabfddcc36c0f7d2bd4384f7d5a4
d972_r07_a0_actual_tau_free_rank_ladder_v7.json              53125 97dfa69864c95f1a3ec7dc5428fcceee50d9eaa1ea07f5cabb0fb8df8c27b59b
d972_r07_a0_actual_tau_free_rank_ladder_v7_checker.log          51 aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1
d972_r07_a0_actual_tau_free_rank_ladder_v7_output.checkpoint 52707 eb1a6d69a855b88d2a934dbf8e58c0f539a7a4d6802cc4a5c7f544b0880da24f
d972_r07_a0_actual_tau_free_rank_ladder_v7_producer.log       5179 475d51fa9af4a498ab92125ad7b59058ef372fafb890204530989970ff3e7513
driver.g                                                        124 f521a63c21f940c7ebc44665606995acb45464ef9e7ca4606630875bda0eb01c
run.log                                                         5277 11856023c568b25066b1604eb3fc8dc1879413bfd439bad5ef658f0f2571788f
```

The copied resume input again measured 52,707 bytes with checkpoint SHA
`eb1a6d69a855b88d2a934dbf8e58c0f539a7a4d6802cc4a5c7f544b0880da24f`.
Its decoded state is exactly reason
`UNKNOWN_RESOURCE:tau_free_localized_dual:time_limit`, rank/count `84/41`,
round `44`, and state SHA
`3c38d9021e20c04a24e99136e47902e8911658f244a202f9c49f4a4280e2f6a7`.

## Dispatch gates

- GAP `ReadAsFunction` parsing passed for rejected v8 and repaired v9. The
  exact generated v9 inner shell plus newline is 8,536 bytes with SHA-256
  `c9d6ba104e4bd8d74b6ff1a962506a015e2526df4f735086e46476b9174673b6`;
  exact-shell and sentinel-shell `bash -n` both exited 0.
- The generated original command has exactly one producer and one independent
  checker. Their source pins independently match `12215 / 014044...ef37` and
  `3653 / e1b80c...8de1`. Static counts are one each for producer timeout
  `7500s`, `--seconds 7200`, `ulimit -v 5200000`,
  `--rss-bytes 4800000000`, checker timeout `3600s`, and `--max-rises 64`.
  Thus `7500>7200`, and `5200000*1024=5324800000>4800000000`.
- All eight owned v9 output paths have fresh `! -e` gates and symlink gates;
  the source files also have symlink gates. Extraction uses a fresh `mkdir`,
  and the authenticated resume member is copied once to the fresh v9 input.
- The shell contains one `set -euo pipefail`, one `ERR` trap, and zero
  occurrences of `set +e` or `set -x`. The bounded v9 run reached the producer
  sentinel exactly once, reached the checker sentinel zero times, and exited
  1. Its owned diagnostic log was exactly:

```text
TASK488_R07_RANK84_PREFLIGHT_BEGIN
TASK488_R07_RANK84_PREFLIGHT_FAIL rc=1 cmd=false
```

- Exact marker gates occur once for producer
  `^R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V3 status=[A-Z_]+$`, checker
  `R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V7_CHECKER_PASS`, and final driver
  `R07_A0_RANK84_CHECKPOINT_RESUME_V9_DRIVER_PASS`. `UNKNOWN_RESOURCE` remains
  transport state and is not promoted to an A0-completion claim.

No producer, checker, GHA dispatch, git operation, or persistent auxiliary file
was run or retained.

GO_FOR_GHA_DISPATCH
