# Luna Task463 — rank-68 dual-anchored batch-64 successor

## Status

PASS for the bounded mechanical rebase.  Only the four Task463 outputs were
created or modified.  No A0 production, GHA dispatch, workflow edit, git
operation, network action, or new mathematics was performed.

## Frozen and owner pins

| object | bytes | SHA-256 |
|---|---:|---|
| Task451 producer owner `search/d972_r07_a0_dual_anchored_active_batch_v1.py` | 13834 | `ca7fb15e06dd04881146c38d63d93015a9e630fbc334cf15098cbd8a32f22f9b` |
| Task451 checker owner `crosscheck/check_d972_r07_a0_dual_anchored_active_batch_v1.py` | 13725 | `5c2f76b825bd920245d0200f29ff860ba93a32663ef5db9567bc499a86f7ff8a` |
| Task451 driver owner `search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v1.g` | 2569 | `6910d38adc56a564b4cd80211bb994de72fd77bf2da6abd8df2df5597ab9a000` |
| frozen rank-68 checkpoint | 33015 | `73ad85624d079d01ecc824ab6adc699c51b0dabfddcc36c0f7d2bd4384f7d5a4` |
| v7 frozen-prefix authenticator | 3653 | `e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1` |

The checkpoint authenticates schema
`d972-r07-a0-actual-tau-free-rank-ladder/v3/checkpoint`, binding
`6f179b061a010bb2a9b427dda6564c7418b18f44da17ea2f28e9e080655326a3`, state
seal `d900bbb4f3b69ee66f9c2f4000b169f69a9202091a69fe0bbb8d33c4ae061537`,
rank 68, accepted count 25, round 27, and the exact ordered 25-record
prefix.  The v2 durable binding is
`bb502c63bb35ebe69d124efbb6b037480f3ccc175a82541f87c5cf4f0d0b8f7e`.

## Generated outputs

| output | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_dual_anchored_active_batch_v2.py` | 14119 | `036704b338d1f3136d3192b314a6beacad1b65037e3f5aaddc8ff85b10d03f21` |
| `crosscheck/check_d972_r07_a0_dual_anchored_active_batch_v2.py` | 14047 | `5f083f2aa1f53f4da5ec7870c9989b65f92f8f0360dc5aa759c72390b125ab12` |
| `search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v2.g` | 2569 | `32c8d11f398709bbafc9795cc62a8846165056a1e8cf1df66afc69657ab5f79d` |

The producer rebases the frozen replay/state from `(51,8,9)` to `(68,25,27)`,
uses `new_rises = accepted_count - 25`, `physical_rank = 68 + new_rises`,
and defaults the per-batch cap to 64.  The checker semantically replays all
25 frozen records before replaying any v2 batch and independently authenticates
the v7 frozen checkpoint.  Its self-test accepts 64 only and rejects 63 for a
max-rises terminal and 65 for cumulative overflow.  Durable state remains
closed-batch-only and RESOURCE results carry no NONMEMBER claim.

The driver requires
`D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V2_RUN:=true;;`, uses fresh v2
artifact/checkpoint/producer-log/checker-log paths, one producer with
`--seconds 7200 --rss-bytes 4800000000 --max-rises 64 --batch-cap 64`, then
requires the independent checker PASS marker.

## Bounded gates

- Repo-external-cache compile:
  `PYTHONPYCACHEPREFIX=%TEMP%\shadow_task463_pycache python -m py_compile search/d972_r07_a0_dual_anchored_active_batch_v2.py crosscheck/check_d972_r07_a0_dual_anchored_active_batch_v2.py` — PASS.
- Load-without-main for both v2 modules — PASS.
- Producer fixture with a `%TEMP%` output — PASS (`R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V2 status=FIXTURE`).
- Checker self-test — PASS (`R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V2_CHECKER_SELFTEST_PASS`, 10 rejection mutations plus explicit 64-rise acceptance).
- Exact transform/hash/cardinality, ASCII/final-newline, and v2 schema/prefix/rank/cap scans — PASS.
- Static driver/process/cap scan — PASS: one producer invocation, 7200 seconds, 4,800,000,000 RSS bytes, 64 new rises, batch cap 64, fresh v2 paths, external preamble, and checker PASS requirement.

Actual A0 production remains intentionally unrun under the task boundary; no
production timing or peak-memory result is claimed.

`TASK463_R07_A0_RANK68_BATCH64_SUCCESSOR_V2_PASS`
