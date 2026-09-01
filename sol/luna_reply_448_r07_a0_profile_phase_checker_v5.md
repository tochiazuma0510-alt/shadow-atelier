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
