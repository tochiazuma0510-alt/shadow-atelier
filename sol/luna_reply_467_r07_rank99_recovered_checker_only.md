# Luna Task467 - recovered rank99 checker-only replay

## Status

PASS for the bounded mechanical implementation.  The recovered-v2 checker
repairs only the `replay` local name binding, retains the v1 artifact/checkpoint
schema and mathematical gates, and adds a bytecode name-binding regression
assertion.  The checker-only driver downloads and authenticates the immutable
release asset, extracts into an isolated directory, copies only the
hash-checked checkpoint into an isolated checker cwd, and invokes exactly one
checker process.  No producer was run or imported as a main program.

## Production and release binding

| object | value |
|---|---|
| production run | `33512607989` |
| artifact id/name | `9808605601 / gap-run-out` |
| invoked head | `3316809e483223ec571ca7d6976dc1317c892441` |
| original artifact SHA-256 | `fb6b6b776b8b288952196f400a0d32d57fd2a5ddb9780a7718e55cffee8bafe1` |
| release asset bytes | `27959` |
| release asset SHA-256 | `d707cf2553fae24863362d581ba4c09709c629a977ff772d95877dd18fdd5f48` |

The six release members are pinned as follows:

| member | bytes | SHA-256 |
|---|---:|---|
| `d972_r07_a0_dual_anchored_active_batch_v1.json` | 173930 | `5079ddfbffbfc00cac6b2672cbef80f7eb2cce069a2dba87aa04e7cbc420c29a` |
| `d972_r07_a0_dual_anchored_active_batch_v1_checker.log` | 5595 | `83378497196b198ef257c4918eedf103baa3532ec71675f2a15d4a5a65db3e91` |
| `d972_r07_a0_dual_anchored_active_batch_v1_output.checkpoint` | 173082 | `bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358` |
| `d972_r07_a0_dual_anchored_active_batch_v1_producer.log` | 3898 | `ef366c147651cf011c16e676878a267dd5d85494d949ff02228f43c6004307af` |
| `driver.g` | 125 | `28802be0e11aad96494eaa266baed0c5b7aa9d85add29bf04a7d7d6db67f67c8` |
| `run.log` | 9493 | `075f3db302e3f7ee98d826cbe8b67fcbcf9355472b18322ccb29fb78a510af2a` |

The durable checkpoint seal is retained, including three closed batches
`51 -> 67 -> 83 -> 99), accepted counts `8 -> 24 -> 40 -> 56`, round
`12`, and inner state seal
`f2de40c3b16053464b8cf7d397f8fd05ca4439a46ca7e45df93e60bbc11a312d`.

## Generated outputs

| output | bytes | SHA-256 |
|---|---:|---|
| `crosscheck/check_d972_r07_a0_dual_anchored_active_batch_recovered_v2.py` | 14442 | `1d1080cd3e130d987316feefd820215f495cd632aa5eca764fd2f8997f0c424` |
| `search/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_gha_driver_v1.g` | 9089 | `a42e0ae68bcdd4e58b212256af9c4addf12b2b11f3d9849d0e40d9d9fa6b48a8` |

The checker keeps schema `d972-r07-a0-dual-anchored-active-batch/v1` and
consumes the immutable v1 production artifact.  Its marker is
`R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_V2_CHECKER_PASS`.  The driver
requires
`D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_CHECKER_ONLY_V1_RUN:=true;;`,
  uses `curl --fail --location`, verifies the zip before unzip and verifies all
six extracted members plus the working checkpoint copy.  It enforces a
6,600-second timeout and a 4,800,000,000-byte RSS bound
(`ulimit -v 4687500`), with `set -euo pipefail`, and requires exactly one
  recovered-v2 PASS line.  The receipt records production, release, checker,
  exit-code, and PASS-marker bindings.
  A successful checker receipt records `rank99_full_semantic_replay_pass=true`.

## Bounded gates

- Python compile, `--help`, and checker self-test: PASS.
- Self-test marker:
  `R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_V2_CHECKER_SELFTEST_PASS`.
- Binding regression reports callable global formula builder, no replay-local
  `formulas` shadow, and a `LOAD_GLOBAL formulas` bytecode use: PASS.
- ASCII and final-newline checks for both outputs: PASS.
- GAP load/parse reached the required external-preamble guard without running
  download, extraction, or checker replay: PASS.
- Static driver scan: one checker command, no producer command/import, exact
  release/six-file pins, collision-safe extraction/work paths, pipefail,
  timeout/RSS bounds, and exact PASS-count gate: PASS.

Rank 99 remains structurally authenticated but not cross-checked until the
checker-only GHA run passes.  No production, GHA dispatch, workflow edit, git
operation, or semantic replay was performed.

`TASK467_R07_RANK99_RECOVERED_CHECKER_ONLY_PASS`
