# Luna reply — Task439 exact-section guard hotfix v4

Implemented only the four authorized v4 outputs. The producer byte-pins
Task436 v1, retains both accepted bootstrap adapters, and surgically restores
the Task179 canonical guard: after the 36-byte coarse lookup it obtains the
stored 40-byte section row and skips a candidate unless the selected
coordinate equals the full `section_target`. Only then is the literal word
and ten-coordinate replay constructed. No search universe or status gate is
changed.

The producer fixture and independent checker self-test each use two records
with the same 36-byte prefix but different 40-byte values, rejecting the
collision and selecting the exact record without Q0 enumeration.

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_actual_b72_first_active_v4.py` | 3619 | `6ffbdf76259de7072f58d1be1d0f0a4156b635290c5a0e07a234989d442e1d2f` |
| `crosscheck/check_d972_r07_a0_actual_b72_first_active_v4.py` | 2633 | `fb66a78d83d1bf712fdcb2bd9e3f7c98726aeadd97345e39c372b86d0550b640` |
| `search/d972_r07_a0_actual_b72_first_active_gha_driver_v4.g` | 2296 | `b0734eb4e9ced9dc394256a3ba02e4765bcf3e2f2dc256d9344180de39b067ec` |

Bounded gates only: external-cache syntax compilation, producer toy fixture,
checker self-test, static driver reconstruction/pin check, and
`git diff --check`. No local production, Q0, bootstrap, GHA, download,
workflow edit, commit, push, or dispatch was run.

## Parent broker result

The audited source was committed/pushed as
`b7b96996e7d4b88f0077c02de31d5d971325296e` and dispatched as run
`33444570055`, job `99660612337`.  The producer crossed the repaired guard and
returned `ACTIVE_COLUMN_READY` after 591.312 seconds:

```text
seed_index       1
coordinate       0
fibre_cursor     0 (first kernel element)
checked_fibres   1
scalar           1
rank_transition  43 -> 44
delta_word_len   146
delta_word_sha   92a51dce182e430f67e26eeef26e34577664c5a8aba6b2ae1f0e193a6a339043
row_digest       5e934d088f01d590ec280edf5c6480f5b6a2f49f545dae204adddf7e58c3ce7a
```

Artifact `9777922364` is 8,139,311 compressed bytes with uploaded zip
SHA-256
`522003b493dfbf90c19fc6c443f888387546c90a1ef06f4d43533798906d68f4`.
Its 94,840,417-byte result JSON has SHA-256
`9b03e2dbdac063bcd1aa53e0cca7bb2fc9fbe30713540118ec8e42fe4c29cbd8`.

The checker then failed before ACTIVE replay with `KeyError: 'dual'`: its
`check` function received the independently rebuilt dual from `prefix` but
did not restore it as `P["dual"]` before calling `formulas`.  The ACTIVE is
therefore still a candidate, not cross-checked.  Task440 v5 repairs only that
checker dataflow edge; it does not change or promote the candidate.
