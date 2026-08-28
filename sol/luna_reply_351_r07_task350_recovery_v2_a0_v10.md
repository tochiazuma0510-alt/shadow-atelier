# Luna reply 351 — recovery-v2 / A0-v10

Read and processed the complete task351 mail and its numbered prerequisites in order. Exactly the six authorized outputs were created; recovery-v1 and all earlier outputs were preserved.

## Outputs and physical identities

| output | bytes | SHA-256 |
|---|---:|---|
| `ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.recovery.manifest.v2.json` | 2690 | `67dd555f6e0f943d0161ef2f2c8124b4cc31c9167846b45b43fd2001f5fbba3f` |
| `search/d972_r07_history_free_positive_fast_resume_v10.py` | 147892 | `235a798e097a7388603a72462a4fef28d9a7e044c47e4339eb4e30714bd9e472` |
| `crosscheck/check_d972_r07_history_free_positive_fast_resume_v10.py` | 131175 | `b2723e9d6703f3cf529ffab7c571ce5dce8b23a428eb54810f57b05aba4a5b0f` |
| `search/d972_r07_history_free_positive_fast_resume_gha_driver_v10.g` | 12812 | `51ce34e7908af9c6a489c76607a95a2c9b55142e04a9d19aaa1154177b06cba3` |
| `search/certs/d972_r07_history_free_positive_fast_resume_selftest_v10_20260829.json` | 3785 | `de6273d681238b1aa560353c70a245cc28823326908e31be464fa2c399917203` |

Recovery-v2 self digest is `e95b4e7781a14cffd07d445141f20c942861168d201f2ce62879a0ddf3a45026`; it is computed from canonical JSON with only the top-level seal removed. The physical v2 owner is 2690 bytes including final LF and has the SHA above. Its accepted receipt digest is corrected to `f8f0ce249ff547d3e1235bd4b9760daa2b34b23771bf7da47b48dbd5cbbfae1d`; correction old/new are `...b34f...`/`...b34b...`. v1 remains authenticated as the superseded 2035-byte owner.

## Implemented static paths

- Physical owner graph: receipt → receipt manifest → recovered verdict → recovery-v1 and recovery-v2; producer/checker/fixture/driver and q3, E3/E4, joint, old, bridge, v172, g760, PB4 authorities are pinned by path, size, and SHA. Opened owners use bounded no-follow reads, fd before/after identity, and pathname-after identity.
- Checker authority is v2-final and v1-superseded. The checker no longer executes task176 source; packed typed elements, Q0 marked permutation replay, parent walks, Gamma walks, and ten-coordinate replay are checker-local.
- Q0 grammar is one root `(0,0)`, nonroot earlier parent plus letter 1/2. Gamma grammar is one root `(0,0)`, nonroot earlier parent plus record 1..26, indexed as `record-1`. Selected widths are E3 `40` bytes and E4 `154` bytes; the projected Gamma row is exactly `5*40+5*154=970` bytes, distinct from full JointGroup state. Gamma has 26 record words and 243 states.
- The triangular path tests earlier-pivot support against chronological `seen_pivots`, preserves `min(P_j)=pivot_j`, coefficient 1, and separately checks all-pivot uniqueness. Every support key is metered; the pinned valid total is `289774` inspections.
- Formal actual rows retain node IDs and hash-consed DAG expressions. Checkpoints carry DAG nodes, pivot expression IDs, solution/remainder node IDs, normalized live rows, bounded canary fields, and distinct DAG/support/expansion/serialization meters. Restore injects authenticated normalized rows and node IDs without replaying old actual provenance. A single owned checkpoint sidecar is used and is pre-sized before atomic replacement.
- The driver has distinct SELFTEST/fresh/authenticated-resume routes, pins recovery-v2 and v1, supplies `--selftest-receipt` to production, stages the raw owner through a checked temporary, and uses the one output sidecar.
- K-nonzero cursor arithmetic is explicit: `0 <= c < 1,469,664*243`, `qid=c//243+1`, `gid=c%243+1`, followed by selected product-word and typed-row checks. K-zero has a pre-capped selected-coordinate state recurrence, 36/144-byte coarse-key inverse and digest, all 243 Gamma first-gid values, authenticated A-family literals, and exact kernel BFS/order/cursor checks with full typed blob equality.

## First blocker and execution status

The first remaining blocker is `crosscheck/check_d972_r07_history_free_positive_fast_resume_v10.py:1235`, `reconstruct_k0_selected_fibre`: this literal path is now fail-closed and complete statically, but it has not received the required fresh Sol(max) code/performance audit or execution receipt. Therefore the v287 K=0 fibre and final heavy identity remain unaccepted. No SELFTEST, production, Python, Node, GAP, GHA, workflow, git, or network execution was performed.

RECOVERY-V2:                    COMPLETE
IMPLEMENTATION:                 BLOCKED
SELFTEST / PRODUCTION:          UNEXECUTED
FROZEN INPUTS:                  PASS
FRESH SEARCH ROUTE:             STATICALLY REACHABLE
AUTHENTICATED RESUME ROUTE:     STATICALLY REACHABLE
ACTUAL A0 COMMON + CHECKER:     0/1
SEPARATOR / NEGATIVE CLAIM:     FORBIDDEN
LIFT / FAKE / IHARA:            NONE
