# Luna task 461 -- resume the A0 literal ladder from rank 68

Role: Luna implementation/compute preparation.  Do not launch local heavy
computation and do not perform git, push, or GHA operations.  The parent is
the sole broker.

## Frozen source artifact

The completed Task450 production is GitHub Actions run `33509311208`, job
`99860860565`, source commit
`165ac51c6794d61f411266d6a72c043361365b64`, artifact id `9806575856`
(`gap-run-out`).  The parent downloaded it outside the repository at

```text
C:\Users\81905\AppData\Local\Temp\r07_run33509311208_54bb2bb71b004e2bb69d5717ff5a90d7\gap-run-out
```

Authenticate these exact files before using the checkpoint:

| file | bytes | SHA-256 |
|---|---:|---|
| `d972_r07_a0_actual_tau_free_rank_ladder_v6.json` | 33433 | `bdd50e84212520a51281f09559c33be60969845ffcc3faf1d3b342c3578d1492` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v6_output.checkpoint` | 33015 | `73ad85624d079d01ecc824ab6adc699c51b0dabfddcc36c0f7d2bd4384f7d5a4` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v6_checker.log` | 51 | `f3d06de0e63b3e440625c09e9af4adf51925ca1a26568bd427dc3b6134f31966` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v6_producer.log` | 5271 | `ecd4d5fa1886cd38d5cc86c218b85e93e67d9d43f9dcc051ba138e8db0307283` |
| `run.log` | 5369 | `ae704131d96b400549ce793847200ee0ddb43d2f701394bcb4d813112f3721ee` |

The checker log must contain
`R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V6_CHECKER_PASS`, and the run log must
contain `R07_A0_RANK51_CHECKPOINT_RESUME_V6_DRIVER_PASS`.

Copy the output checkpoint byte for byte, using `apply_patch`, to

```text
search/certs/d972_r07_a0_actual_tau_free_rank68_checkpoint_v1.json
```

It must retain the exact 33,015 bytes and SHA-256 above.  Independently
authenticate its v3 checkpoint seal and these fields:

```text
rank=68
accepted_count=25
round=27
reason=UNKNOWN_RESOURCE:tau_free_formula_seed:time_limit
state_sha256=d900bbb4f3b69ee66f9c2f4000b169f69a9202091a69fe0bbb8d33c4ae061537
```

This is 17 new literal rank rises beyond the frozen rank-51 prefix.  It is
not COMMON and makes no lift, fake, or Ihara claim.

## Implement only the unchanged continuation transport

Create:

```text
crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v7.py
search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v7.g
sol/luna_reply_461_r07_a0_rank68_checkpoint_resume_v7.md
```

The v7 driver must:

1. exact-pin the unchanged v3 producer, the new v7 checker, and the
   repository rank-68 checkpoint;
2. require external preamble
   `D972_R07_A0_RANK68_CHECKPOINT_RESUME_V7_RUN:=true;;`;
3. copy the pinned checkpoint to a fresh direct child of `ci/out`, authenticate
   the copy, and invoke the unchanged v3 producer with `--resume`;
4. use fresh v7 result/checkpoint/producer-log/checker-log paths;
5. give the producer 7,200 seconds, RSS 4,800,000,000 bytes, and at most 64
   additional rank rises;
6. run the independent v7 checker and require its PASS marker; and
7. contain exactly one production process and no production SELFTEST/FIXTURE,
   eager store, closure rebuild, actor-adapted rebase, or universe change.

The v7 checker must exact-pin and delegate the complete v6 checker, and then
independently:

- authenticate the frozen rank-68 checkpoint bytes, outer SHA, schema,
  binding, canonical state seal, rank/count/round, and terminal reason;
- require the final `accepted_sources` to contain all 25 frozen records as an
  exact ordered prefix;
- require final rank, accepted count, and round to be monotone from
  `(68,25,27)`; and
- retain the v6 checker's full replay of every final accepted row and terminal
  profile.

Add only bounded synthetic mutations for the new seal, 25-record prefix, and
rank/count/round monotonicity.  Do not execute production in self-test.  Do
not change the producer or its mathematics.  Report exact sizes/SHA-256 and
bounded compile/self-test/static-inspection commands in the reply.

