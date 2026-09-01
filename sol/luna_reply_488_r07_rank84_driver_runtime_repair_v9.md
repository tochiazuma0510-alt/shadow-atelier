# Luna reply 488: rank-84 driver runtime repair v9

Status: `TASK488_R07_RANK84_DRIVER_RUNTIME_REPAIR_V9_PASS`

The two commissioned outputs are complete. The frozen v8 driver remains
untouched. No production producer, checker, GHA dispatch, or git mutation was
run (only read-only worktree inspection).

## Diagnosis

I downloaded the failed run `33543290399` / job `99974575290` artifact
`9814471992` read-only. The artifact is 45,706 bytes with API digest
`23bc8f0283f8198c39f9b78285e3dbd3ba95ec9537e11c1cf7a464bc227cb138`; it
contains the 23,004-byte release zip and the generic workflow files. Exact
temporary tracing of the generated v8 shell, with producer/checker replaced by
fail-closed sentinels, reproduced the one-second failure before either
sentinel.

The exact first failing command was:

```sh
test "$(sha256sum "ci/out/d972_r07_a0_actual_tau_free_rank84_resume_v8_archive/d972_r07_a0_actual_tau_free_rank_ladder_v7.json" | cut -d " " -f1)" = "97dfa69864c95f1a3ec7dc5428fcceee50d9eaa1ea07f5cabb0fb8df8c27b59"
```

The archive member is 53,125 bytes and hashes to
`97dfa69864c95f1a3ec7dc5428fcceee50d9eaa1ea07f5cabb0fb8df8c27b59b`.
The v8 manifest expected a 63-character digest, missing the final `b`.
The same truncation defect was present in the checkpoint member pin and the
resume-copy pin (both required the final `f`); no producer/checker or
mathematics defect was observed.

## v9 repair

`search/d972_r07_a0_actual_tau_free_rank84_resume_gha_driver_v9.g` is a fresh
driver with fresh v9 output paths. It preserves the permanent release URL,
the seven member pins, rank-84 checkpoint/state, frozen producer/checker
source pins, one producer and one checker, `7500s > 7200s`,
`5200000 * 1024 > 4800000000`, checker timeout `3600s`, and all marker/claim
boundaries. The three truncated SHA literals are repaired to their full
64-character values.

The generated shell starts with `set -euo pipefail; umask 077` and records
pre-producer failures in the owned v9 preflight log through an `ERR` trap.
Production xtrace is not enabled.

The preserved resume state is `UNKNOWN_RESOURCE:tau_free_localized_dual:time_limit`
at rank/count `84 / 41`, round `44`, state SHA
`3c38d9021e20c04a24e99136e47902e8911658f244a202f9c49f4a4280e2f6a7`.

## Bounded gates

- Source pins: producer `12215` bytes /
  `0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37`;
  checker `3653` bytes /
  `e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1`:
  PASS.
- Release archive: `23004` bytes /
  `dde60bad768e20ead6ad08e8bd0a8e53fc97050a43f6c207552ba97d579c438a`;
  seven member size/SHA gates and resume copy `52707` bytes / full checkpoint
  SHA: PASS.
- GAP `ReadAsFunction` parse: `TASK488_GAP_READASFUNCTION_PARSE_PASS`.
- Exact generated shell `bash -n`: exit `0`; generated command was 8536
  UTF-8 bytes, SHA256
  `c9d6ba104e4bd8d74b6ff1a962506a015e2526df4f735086e46476b9174673b6`.
- External temporary preflight with sentinels: `bash -n=0`, exit `1` only from
  the intentional producer sentinel; all archive/source/resume gates passed,
  seven archive members were extracted, and the resume input was copied.
  The owned diagnostic log contains `TASK488_R07_RANK84_PREFLIGHT_BEGIN` and
  `TASK488_R07_RANK84_PREFLIGHT_FAIL`; producer sentinel reached once as an
  exact line, checker sentinel reached zero times.
- Static exact-one gates on the generated command: producer process `1`,
  checker process `1`, producer timeout `7500s` `1`, checker timeout `3600s`
  `1`, `--seconds 7200` `1`, `--rss-bytes 4800000000` `1`, `ulimit -v
  5200000` `1`, producer marker `1`, checker marker `1`; `set +e` and `set -x`
  occurrences `0`.

Final v9 driver pin: `8257` bytes,
`d89cac926cfd3a0b44d0a3564e73c608035f6389f9240452d0017aa126156fd9`.

TASK488_R07_RANK84_DRIVER_RUNTIME_REPAIR_V9_PASS
