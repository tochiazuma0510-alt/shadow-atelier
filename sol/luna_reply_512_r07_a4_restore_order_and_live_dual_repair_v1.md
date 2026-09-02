# Luna reply 512 -- A4 restore order and live-dual repair

Implemented the bounded Task512 and Task512a repairs.  Only the three
versioned implementation files and this reply were written; v24/v33/v43,
production code, workflows, GHA, and git state were not changed.

Frozen output pins:

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_v25.py` | 27075 | `8e5c16f28113218485f7196c6873dbbf3ce17a0e03bd7daafe71bc6e8da5015f` |
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v34.py` | 5838 | `b00219523c2e5703b8c6c52c7bf24655c727ddc72c7da9fd06c746063875a9ba` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v44.g` | 8960 | `7f70546b51b934edcc6d64626af4d04c18f15642a10db8b40eaea3f9fcfb96f3` |

Generated-source pins:

- v25 generated source: 286439 bytes,
  `e4fb7ead7e1dcfc5806574481f1e83e008991e516de20e2eb3a67753fec03098`.
- v34 generated source: 312553 bytes,
  `2ffcdede9a20acdd99bab3c4847db4c4a4f013e33fc151ac01b77f088d21df75`.

Bounded gates and results:

- `python -B search/d972_r07_word_independent_successor_kernel_v25.py --source-patch-info`: PASS; v24 owner and generated-v24 pins match.
- `python -B search/d972_r07_word_independent_successor_kernel_v25.py --fixture`: PASS.  The generated `build_kernel` call path closes three accepted (`accepted_mask=[1]`) entries for one open query, resumes, and closes shard 4.  The actual shard files show `shard4.semantic_before == shard3.semantic_after`; measured resume direct restore is exactly one, restore replay calls are zero, and restored basis maps/formals/records/event-chain/dual-chain/epoch/live-dual state agrees with the uninterrupted route.  A resealed counter-order mutation and duplicated live-dual mutation are rejected.
- The same fixture injects an ordinary completed-row checkpoint write failure: publish count on that route is zero and the disk HEAD remains live.  On the successful generated route the ordinary checkpoint exists before obsolete HEAD publication; the final disk HEAD is obsolete and the ordinary reference is `delta_chain`.  A separate atomic publish write failure also leaves the disk HEAD live.
- `python -B crosscheck/check_d972_r07_word_independent_successor_kernel_v34.py --source-patch-info`: PASS; v33 owner and generated-v33 pins match.
- `python -B crosscheck/check_d972_r07_word_independent_successor_kernel_v34.py --self-test`: PASS; independent checker route, ordered restore, semantic mutation, and duplicate-live-dual gates pass without importing v25.
- Python AST parse: `AST_PARSE_PASS`.
- GAP `ReadAsFunction("search/d972_r07_word_independent_successor_kernel_gha_driver_v44.g"); QUIT;`: PASS.  The reached shell retains one producer, the v43 row-26 release URL/hash (`56410` bytes), six member size/hash checks and canonical member filenames, fresh paths, source/generated pins, 14,400-second/8-GB internal limits with external margin, and RESOURCE-without-checker / positive-single-checker branching.

Task512a completion ordering is separately accepted: in-memory commit retains
`obsolete=true`, ordinary completed-row write precedes atomic obsolete HEAD
publication, and both injected failure paths are measured fail-closed.

TASK512_R07_A4_RESTORE_ORDER_AND_LIVE_DUAL_REPAIR_PASS
