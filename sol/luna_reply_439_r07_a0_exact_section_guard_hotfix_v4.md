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
