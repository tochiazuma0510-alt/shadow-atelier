# Luna reply — task435

Implemented only the four authorized v1 outputs:

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_actual_dual_weight_profile_v1.py` | 14663 | `36cc190dc610a1675b9d7b990252a7b01eb366649ecf2f84fa1dde3660c694fd` |
| `crosscheck/check_d972_r07_a0_actual_dual_weight_profile_v1.py` | 9735 | `8bc0215bab131e623e9f820f330a285cfcb5ab6c650fd52ea76a2d3ba8f0f350` |
| `search/d972_r07_a0_actual_dual_weight_profile_gha_driver_v1.g` | 2333 | `356f96e6a969fbe6560213add76c4a33bd4533f27f9d78b8d86178b23a097827` |

## Implemented path

The producer now imports the exact pinned v12 module and reproduces its
bootstrap (T413/base/JOINT/Q3/ACCEPTANCE/TASK379/TASK176/core/runtime,
`direct_physical_owner`, `Quotient`, and exact target construction). It checks
the 44-relator compact roster and uses the real `q.parse` ABI.

The production prefix builds one fresh v12 `PackedEchelon`, inserts the 44
identity compact physical columns, then repeatedly computes the exact target
dual and runs only `runtime.old.pure_relations(4)[5:11]` through the existing
v404 `action_support_hits` oracle. Every retained action is independently
replayed with `v12.action_row`. The profile records target/remainder/dual
digests, real block/label support, PB3/PB4 tau coefficients, normalized
exponents, source rows, rank/nnz, action rounds/candidates/retained rows, and
durable resource checkpoints.

This task produces only `PROFILE_READY` or `UNKNOWN_RESOURCE`; it never emits
an A0, COMMON, NONMEMBER, fake, or Ihara claim. It does not load Q0/Delta,
weighted fibres, occurrence checkpoints, or boundary closures.

## Gates

- Python 3.13 compile with external `PYTHONPYCACHEPREFIX`: PASS.
- Producer bootstrap-free real-key fixture: PASS, about 0.01 s.
- Checker self-test: PASS, about 0.01 s; omitted tau/action semantic mutations
  are rejected.
- `git diff --check` on the three task outputs: PASS.
- No local production runtime/bootstrap, checkpoint load, download, commit,
  push, dispatch, or workflow edit was performed.

The final dual is scaled immediately after each v12 echelon reduction so its
pairing with the nonzero remainder is exactly one; `dual_target_pair=1` is
emitted and independently checked. If the target is already zero, the v404
accumulator is recorded as `not_applicable_target_zero` with an unpromoted
positive-prefix flag, rather than as an empty v404 proof.

The referenced `sol/proof_r07_a0_actual_dual_weight_profile_v410.md` was not
present in the repository; implementation follows the complete task435
brief and the explicit v12 bootstrap ABI included there.

## Pins

Reused v12 producer: 51884 bytes,
`3016b6a21d9fafbf037dbb5384dcca81f49e1fa44ae45a466ff16f1fd13948b3`.

GHA external preamble:

```gap
D972_R07_A0_ACTUAL_DUAL_WEIGHT_PROFILE_V1_RUN:=true;;
```

Production command used by the driver (GHA only):

```text
python3 -u -B search/d972_r07_a0_actual_dual_weight_profile_v1.py --mode PRODUCTION --seconds 1800 --rss-bytes 4800000000 --output ci/out/d972_r07_a0_actual_dual_weight_profile_v1.json --checkpoint ci/out/d972_r07_a0_actual_dual_weight_profile_v1_output.checkpoint
```

Expectation: this profile is materially smaller than the rank-1655 physical
probe because it starts with only 44 identity columns and adds only
dual-active v404 rows. The actual tau profile and final dual remain pending
until GHA executes the real bootstrap.

Untouched: task434 files, v12/task179 sources and checkers, all running A0
jobs/checkpoints, workflows, v220, proofs, receipts, and earlier task/reply
files.
