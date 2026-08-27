# Luna reply 183 — r07 weighted-support hitting implementation v1

Date: 2026-08-27
Role: bounded implementation and static audit only.

## Static verdict

Implemented `sol/proof_r07_actual_weighted_support_hitting_selector_v143.md`
on top of the audited task182 coarse-inverse selector. The live runtime now
requires `|Delta|=357,128,352` and kernel orders
`[9,9,9,9,9,1,1,1,3,3]`, and exhausts every word-bearing kernel BFS while
checking identity in the selected coordinate and uniqueness of complete
ten-coordinate states.

The correction oracle now computes `K` and the exact merged-target bound
`W=sum(kernel_order[coordinate])`. For `K=0` it completely enumerates each
nonempty support fibre using the task182 least representative and complete
kernel roster. For `K!=0` and `W<|Delta|` it tests exactly the first `W+1`
distinct global `(qid,gamma)` representatives. For `W>=|Delta|` it retains a
fair full-roster fallback whose exhaustion is typed `UNKNOWN_RESOURCE` only.
Every active correction carries the formula, `K`, `W`, Delta order, kernel
orders, distinct targets, and schedule provenance; the checker recomputes the
weighted data and direct scalar independently.

Checkpoint progress now records per-row formula digest, `K`, `W`, Delta order,
kernel orders, support-fibre cursor, kernel cursor, global prefix, and row
completion. A shared checkpoint-state validator requires contiguous completed
rows, permits only the immediately following incomplete row, checks all cursor
bounds, and recomputes each stored formula against the current dual/roster
whenever the dual is available. Cursor updates occur before candidate replay,
so resume may repeat the last candidate but cannot skip an untested candidate.
Checkpoint serialization now derives and persists the exact dual whenever the
reduced target is nonzero, including the ResourceStop sidecar path, and binds
its digest to the correction progress state.

The `K!=0`, `W<Delta` exhausted-prefix branch is a hard RuntimeError theorem
invariant and is covered by SELFTEST; it is never relabelled as UNKNOWN. The
honest `W>=Delta` full-roster exhaustion uses the registered `global_roster`
monitor cap and emits `value=Delta+1, limit=Delta`. The checker parses and
binds every UNKNOWN_RESOURCE phase/cap/value/limit field to a registered cap.

SELFTEST adds normal-validator cases for a last-point `K=0` kernel hit,
complete `K=0` exhaustion, guaranteed `W+1` global hitting, kernel-order
mutations, omitted merged targets, repeated global representatives, and an
advanced completed-row cursor, plus hard rejection of the impossible `W+1`
branch. The existing fifteen semantic mutations remain unchanged; eight
weighted mutations are additionally checked independently.

## Completed-path bounds

- `K=0`: at most `W` kernel representatives across the distinct merged
  targets (empty fibres may remain in the upper bound).
- `K!=0`, `W<357,128,352`: at most `W+1` distinct global representatives.
- `K!=0`, `W>=357,128,352`: fair fallback over the full `357,128,352`
  representative roster; bounded exhaustion remains `UNKNOWN_RESOURCE`.

## Proof pins

Both governing proofs are added consistently to producer, checker, and
driver pins:

- v142: 4,942 bytes,
  `5f0fffe64b729a8e44643ce86e9d588ef96cbe199ef8ca03741c712c2b162ee8`.
- v143: 5,253 bytes,
  `aae57d5481d7e649d449b58d06ade2d9cbf90fa48d50a8ae43650da5243cf259`.

## Exact bytes / SHA-256 (post-edit working tree)

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_positive_common_word_colgen_v1.py` | 119,396 | `32b7f3c462212a3b0905dfcf4de005c29ac00d5743d5ea93f57963ba350d7dde` |
| `crosscheck/check_d972_r07_positive_common_word_colgen_v1.py` | 69,751 | `16bf1f25da5dae068227120db44d2986d99e0c39f5dcb63c72a7cc7b3092a71d` |
| `search/d972_r07_positive_common_word_colgen_gha_driver_v1.g` | 12,973 | `9d84ab177e01ea2a2eb514646ddb49fb4d1dac280a2335978e7b0de19dfeb181` |
| `search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json` | 407 | `46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78` |

## Execution / blocker

Per commission, Python/Node/GAP/git/GHA were not run. This is therefore a
static verdict, not a cross-checked or Lean-verified run. Parent must perform
the final live-source pin cascade in order: task179 producer; checker
producer/shared predecessors; driver producer/checker/all predecessors; then
reply identities. The task182 implementation and its parent-controlled pin
boundary are preserved.

## Parent cascade addendum

Parent completed the ordered task175/task176 and producer-to-checker-to-driver
pin cascade. The table above is therefore superseded by:

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_positive_common_word_colgen_v1.py` | 119,396 | `4dcae739a8d1181341ae90a7375e7ca7c465d404582e53a24b6fc84ab7a3f5f4` |
| `crosscheck/check_d972_r07_positive_common_word_colgen_v1.py` | 69,752 | `c2f50def1e1ea348bc2919aff91cba1fa748978a55b1895c9b58a69f673b314f` |
| `search/d972_r07_positive_common_word_colgen_gha_driver_v1.g` | 12,974 | `418ab65951b3fc284bc52b36043685146fd8f9faacdf31e381c365c863edffbd` |
| `search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json` | 407 | `46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78` |

The parent audit additionally made the K=0 checkpoint cursor
coordinate-specific: a completed row is bound to the last support target and
its kernel cursor is either zero for an empty fibre or the exact registered
order for a completely enumerated nonempty fibre. Static verdict is
`STATIC GO / execution pending`.
