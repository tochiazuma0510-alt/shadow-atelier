# Luna reply 448 — R07 A0 profile-phase checker v5

Status: **complete; sole profile-phase repair applied**.

## Exact outputs

| path | bytes | SHA256 |
|---|---:|---|
| `crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v5.py` | 2859 | `e783028862bbae84acf769ec64de9693dfae1c4c99e9444e8e92af76e08a2da0` |
| `search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v5.g` | 2328 | `b9b1a829eeec923bfd714a87e518628e7660e340e6a247427b6c8e71b1cb698a` |
| `sol/luna_reply_448_r07_a0_profile_phase_checker_v5.md` | self-referential | not driver-pinned |

The checker pins v4 at 5,876 bytes / `fcd1fd1e4cbff30a4e472b1776aea011d62abe95cb8f51141883ad98db45242e`. The driver pins the unchanged v3 producer at 12,215 bytes / `0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37`.

## Repair

- A profile containing `adjoint_digest` must also contain an integer `localized_dual_support`. The checker independently reconstructs that count, removes only this field, and delegates all remaining complete-profile comparison to v3.
- A profile without `adjoint_digest` must not contain `localized_dual_support`; the unchanged basic profile is delegated directly to v3.
- All v4 gates remain inherited unchanged: terminal/dual boundary, claims, durable metadata and checkpoint authentication, exact 12-phase resource allowlist, coordinate parser, independent replay, and positive reconstruction.
- The v3 producer and mathematical/search universe were not copied or modified.

## Bounded gates

```text
PYTHONPYCACHEPREFIX=%TEMP%\task448_pycache python -m py_compile crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v5.py
python crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v5.py --self-test
rg -n "D448ProducerBytes|D448CheckerBytes|--seconds 2400|--rss-bytes 4800000000|--max-rises 64|SELFTEST|FIXTURE" search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v5.g
```

Compile and self-test passed. Fixtures accepted both valid shapes:

- basic/pre-adjoint profile without localized count;
- complete adjoint profile with localized count.

Mutations adding the field to a basic profile and deleting it from an adjoint profile were rejected. The complete inherited v4/v3 mutation suites also passed. Static driver inspection confirmed the unchanged caps, fresh paths, one production process, external v5 preamble, and absence of production fixture/self-test.

No production, Q0, GHA, workflow, commit, push, or other git operation was performed.

## Parent audit and production dispatch

Parent bounded checks and a separate Sol read-only audit both returned GO.
The exact v1--v5 dependency chain was committed and pushed at
`6eb23ef7c8196ff93631051bb97e3696308ac6fe`. Parent dispatched
`gap-run.yml` as run `33504248130`, job `99844420262`, with:

```text
script=search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v5.g
preamble=D972_R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V5_RUN:=true;;
out_dir=ci/out
timeout_min=90
with_pquot_packages=false
```

The driver gives the single producer 2,400 seconds, 4.8 GB RSS, and 64 new
rank rises. Result pending; dispatch itself changes no A0 numerator.

## Parent production adjudication

GHA run `33504248130`, job `99844420262`, completed successfully from exact
source SHA `6eb23ef7c8196ff93631051bb97e3696308ac6fe`.  Artifact
`9800544629` (`gap-run-out`) contained:

| file | bytes | SHA256 |
|---|---:|---|
| `d972_r07_a0_actual_tau_free_rank_ladder_v5.json` | 11,349 | `0860248c0cc1abe1efbe26ef463d7f0efed1e6ff2886352c668cd28d6d7831fb` |
| `d972_r07_a0_actual_tau_free_rank_ladder_v5_output.checkpoint` | 10,934 | `a83959e4c9fcfa79093c712e82164d47c31b78c9fc00b512f7adac9413c481f4` |
| producer log | 4,402 | `035d94d8914feda217ea4e0fbcd467f5bbe4f2d7369e715799bddb5a19e84a5f` |
| checker log | 51 | `0216f7abbf35ef1a2540d024a34d8e595d208c88d6fcdb593579451aacd697f4` |

The checker emitted exactly
`R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V5_CHECKER_PASS`.  The producer accepted
eight literal correction rows, all from compact seed 1 and coordinate S0,
and raised the physical rank successively

```text
43 -> 44 -> 45 -> 46 -> 47 -> 48 -> 49 -> 50 -> 51.
```

The rank-51 checkpoint has internal state SHA-256
`22dcfdfb396524ea5853488aa2ad52d28b4f7d10164123bc83f121e59dd83159`,
`accepted_count=8`, and `round=9`.  Its current separating dual has 29
localized block-1 `b` keys, zero tau coefficients, zero normalized exponent
coefficients, target pairing one, and no unrecognized keys.  The terminal is

```text
UNKNOWN_RESOURCE:tau_free_formula_seed:time_limit
```

after 2,411.2134498 producer seconds.  This is a resource stop while compiling
round 9, not a mathematical selector gate or negative terminal.  Therefore
A0 remains 0/1, but the durable cross-checked correction ladder is now eight
rungs rather than one.  No common word, nonmembership, fake, or Ihara claim
is promoted.
