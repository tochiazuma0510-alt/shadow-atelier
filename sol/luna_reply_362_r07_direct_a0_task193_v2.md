# Luna reply 362 — direct A0 to task193 v2

Static implementation only.  Exactly the seven requested new files were
created.  No Python, GAP, GHA, SELFTEST, git write/commit, retry, fixture,
mutation, or search execution was performed; only read-only file inspection,
hash, and status checks were used.  No existing file was edited.

## New files and byte identities

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_history_free_task193_compat_adapter_v3.py` | 14038 | `7be27b31f0c6e4acf0948341dfaae9d9d880b204774d04660a77982c0546245c` |
| `crosscheck/check_d972_r07_history_free_task193_compat_adapter_v3.py` | 16804 | `f123daeec769aff9254bf913514f0792f20a2f32725aa19bd0020dc84e4c0c6f` |
| `search/d972_r07_history_free_task193_compat_adapter_gha_driver_v3.g` | 3948 | `f04d93b6c7ae3f55fee3c8559fee74a19cc6b05fd7dd9294398658ff8c0591cb` |
| `search/d972_r07_second_frattini_affine_prefix_compiler_v2.py` | 22937 | `65a45189e120ae58f99310a9189fd4f88802e269d3c1a61bf5e68e879eebde88` |
| `crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v2.py` | 32933 | `fdb80b02030a82d4d6cfccc6246c915c14b896e91e126b2b7ba5c22a6dc99ea5` |
| `search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v2.g` | 4922 | `02036214232abd174207f4f5632b0cbc0b5ffe7f15edbd15ba7877b86f008ab0` |

The reply file's own byte identity is reported in the handoff because putting
its self-hash into its own bytes would be circular.

## Adapter v3 boundary

The producer pins A0-v18 at
`search/d972_r07_history_free_positive_fast_resume_v18.py` (2557 bytes,
`55505c6b59ebc9cc61c12c0229668509a2fcf7530ca14dbd791a8b18a95c5433`) and
`crosscheck/check_d972_r07_history_free_positive_fast_resume_v18.py` (1317
bytes, `83ebfe5088388f5c84bbab9e52ef28cb8888fb944fbe417cf98041bab34bfaa9`).
After the sealed physical A0 receipt/verdict gate, the load-bearing replay is
the pinned checker's `validate_common(..., include_selftest=False,
source_raw=...)` call (producer line 231; independent checker line 230).
The adapter then calls the rebuilt model's `direct_column([], c)` (producer
line 241; checker line 237), converts it with the pinned public sparse
encoding, and computes the legacy binary digest
`u32be(byte_length(key)) || key || coeff`.

The dedicated ABI contains `c_exact`, `corrected_word`, `g760`, the fresh
`direct_replay.row` and `row_sha256`, and exactly the four direct flags
`direct_all_seven_replay`, `right_g760_multiplication`, `hexagons`, and
`pentagon_printed_order`.  It has no task193/d1/beta1/e1/eta_c result.  Its
accepted terminal is
`R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V3_A0_REPLAY`; missing, malformed,
or nonpositive A0 ends as typed `UNKNOWN_INPUT:<reason>`.  The checker does
not import the adapter producer and repeats the full A0 replay before checking
the ABI.

## Task193 v2 boundary and exact patch sites

The producer authenticates the adapter receipt and v3 checker verdict, then
passes only this in-memory object to the frozen v1 `actual_compile`: 
`exactification.positive_receipt`, `exactification.literal.c_exact`,
`exact_direct_replay.row`, `row_sha256`, `replay.corrected_word`,
`replay.direct_all_seven_replay`, and the three remaining direct flags.
No legacy receipt, normalized-column transcript, or legacy checker is called.

The v1 owner is pinned at 37956 bytes,
`7ec85fe5b359a371e7c7c6b701426c5521d2a9651f560cba0193fa9c34aa2530`.
Its source is patched in memory at two cardinality-one byte sites (producer
lines 270–278): immediately before the unique
`checkpoint_body={"schema":"...checkpoint/v1",` statement to call
`pointed_row_package`, and immediately after the unique v1 `beta1` return
field to expose that package.  The existing affine-prefix compiler and its
beta1_H1/beta1_H2/beta1_P arithmetic are otherwise unchanged.

The pointed package evaluates the two PB3 hexagon words and printed-order PB4
pentagon word built from uncorrected `g760` through that same `eval_aff`, with
`require_identity=False`.  H1, H2, and P remain separate.  It exports typed
`D1_g760`, `beta1=D1(corrected)`, `d1_pt=-D1(g760)`, `B1a=beta1-D1(g760)`,
`e1_pt=d1_pt-B1a=-beta1`, and `e1_aug=B1a-d1_pt=beta1`, including the three
endpoint replays
`D1(d1_pt)=1-R(g760)`, `D1(beta1)=R(f)-1`, and
`D1(e1_pt)=1-R(f)`.  No `D1(d1_pt)=0` gate is imposed.

The independent task193 checker authenticates the adapter source identities,
replays the v1 checker mathematics through bounded source patches, and adds a
pointed hook.  Its exact patches are: replace the one v1 legacy input block
(the unique `art=r.get("task186_artifact",{})` byte block, checker lines
476–497), replace the four direct-row references with the dedicated names,
and replace the unique `complete label/query chronology` line (checker line
508) with the pointed replay hook.  The
hook independently reconstructs the g760 hexagon/pentagon words, affine
prefix transitions, full-cokernel rows/endpoints, signs, and tail label/query
chronology.  The v1 checker is never invoked as a legacy task186 checker.

Task193 accepted terminal is
`R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V2`; typed terminals are
`UNKNOWN_INPUT:<reason>` and `UNKNOWN_RESOURCE:<reason>`.  Lift, fake, Ihara,
and other downstream claims remain `NONE`.

## Drivers and terminal policy

Both new `.g` drivers are ASCII-only, production-only, pin their producer and
checker bytes/SHA, reject stale outputs and unsafe input paths, invoke each
stage once, compare the exact terminal lines, and write a completion marker
only after the declared terminal/artifacts pass their gates.  They contain no
SELFTEST or retry path and do not unconditionally emit PASS.

UNEXECUTED: no production run, checker run, GAP driver, GHA workflow, Python
self-test, git write/commit, or mathematical success claim.
