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

## Parent dispatch record

The parent broker committed and pushed the audited files at
`cadbe6eda7159889279fbf63c24641d026df97d9`, then dispatched the unchanged
generic `gap-run.yml` workflow as run `33391325650`.  Inputs were the driver
above, its exact external preamble, `out_dir=ci/out`, and
`timeout_min=60`.

The run completed successfully.  Producer and checker both passed.  The
producer's computational prefix took 108.573 seconds; the whole GHA job,
including the independent reconstruction, took about 204 seconds after GAP
setup.  Artifact `9757686821` contains:

| item | bytes | SHA-256 |
|---|---:|---|
| result JSON | 172,845,608 | `b317d5207d9e37553e78190916a5afddc7bd404f4cdd52fdb04847c32b24b99d` |
| resource checkpoint | 695,382,832 | `bc129172ad2471c5daebeb3d821f963b01c750febc3fcd606cedd8bde3032594` |
| producer log | 5,938 | `38ece6ea780d68b25ba955f5387eceb15f62254d0ef246375279fe14442ae0f4` |
| checker log | 50 | `b129b3b0bdbf8b5c2d997564c7ca178b7d05850fbb1d31aa25a80579f29371f4` |

Cross-checked actual result:

```text
terminal                              PROFILE_READY
identity compact attempted/retained   44 / 43
physical rank / payload nnz            43 / 1,813,674
v404 candidates/retained/final         0 / 0 / EMPTY
dual support                           24
dual key roster                        24 x (PB3 block 1, label b, blob 40)
dual digest                            c75895737537f157fbbfedcdc2c41ed31c8bf0ca9bddda060079ffcda7604efd
dual/remainder pairing                 1
tau coefficients                       0,0,0
normalized exponent coefficients       0,0
```

The `support_by_label` values in the JSON are coefficient sums modulo three;
the 24-key roster above was obtained by parsing every framed dual key and is
not inferred from that sum.

The result is computationally small but the v1 serializer unnecessarily
duplicates the 43 full physical rows in both JSON and checkpoint, producing
the large sizes above.  This does not affect the checked mathematics, but it
is not reused as an artifact pattern: Task436 rebuilds the 108-second prefix
and serializes only digests, formula records, and a selected literal source.
