# Luna reply 458: direct-relator positive-only quarantine v1

Status: **IMPLEMENTED / BOUNDED GATES PASS / PRODUCTION NOT RUN**

## Exact physical outputs

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_zero_base_a5_a6_compiler_v6.py` | 2342 | `32cbc1a8e1faea0d4dc7a88a41a2ad3b535e7b2fd94b73ff286d78001262b96c` |
| `crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v6.py` | 2334 | `a4db1b2b1ad5da1135c8ebcef1898c46fd07df7ebdbfa8778bd36a6098507bc3` |
| `search/d972_r07_zero_base_a5_a6_compiler_gha_driver_v6.g` | 2106 | `212c76f2ca2e06df1aae2b2d783a15fcf1d4e5041d70cba26198d64d9bd4d4d6` |
| `search/d972_r07_direct_relator_a5_a7_fusion_v8.py` | 4302 | `f0d108259f13c1c87c4129aa08a5c8f17fd4466604f76fdb5d7fb8172a487fa8` |
| `crosscheck/check_d972_r07_direct_relator_a5_a7_fusion_v8.py` | 2657 | `3f195e106c4a0fdd1f3f7d173a4a5c80600ce3210da3610212baf0bff2f87255` |
| `search/d972_r07_direct_relator_a5_a7_fusion_gha_driver_v8.g` | 1932 | `16d6b3b9132db2062236535bf88f66e4c18b7684c95b6259600d7ed300d9f07a` |

## Generated mathematical-body seals

- zero producer: `59382 / 83b31959a0c35bdeb1e2569e0ee384b116ed6ed0b7d57e9c363cecdc29fcfe87`
- zero checker: `45888 / cf44a9a8397eebf99271a4444bb41bd300fe5cfa60cc00696e9811a1469b52c7`
- fusion producer: `57892 / a21a7061bf1c4b59b29a1ab1bb11bf18d9fab7b3b1f788dbec22b2213d7ab692`
- fusion checker: `29828 / c5571981145908d6b892fb776aa84d9e8d07c36fb4d27548af95b17e395821ca`

## Semantic boundary

- Finite `MEMBER` arithmetic, ancestry, and independent replay are inherited unchanged.
- Zero-base inherited `NONMEMBER` is emitted only as `UNKNOWN_INCOMPLETE:K_conjugation_closure_not_implemented`, with A5/A6/A7/fake/Ihara claims absent/false. Its checker is MEMBER-only and rejects NONMEMBER or UNKNOWN receipts.
- Fusion's old `A5_NONMEMBER_COMPLETE` branch is replaced by checkpoint phase `A5_INCOMPLETE_SPAN` and the same honest `UNKNOWN_INCOMPLETE` terminal with no claims. The fusion checker remains positive MEMBER-only.
- Drivers invoke checkers only for MEMBER. Nonpositive `UNKNOWN_RESOURCE`/`UNKNOWN_INCOMPLETE` terminals remain unpromoted.
- This task **does not implement the v418 ordinary word-bearing K conjugation closure** and makes no NONMEMBER claim.

## Bounded gates

Passed: repo-external-cache `py_compile`; four load-without-main executions; inherited-body and final generated-body byte/SHA gates; exact transform cardinality gates; synthetic NONMEMBER quarantine and MEMBER-checker pass-through source fixtures; static driver terminal/checker branching and pin scans. No production input, 6,441-row closure, GHA, workflow, network, git, commit, or push was used.
