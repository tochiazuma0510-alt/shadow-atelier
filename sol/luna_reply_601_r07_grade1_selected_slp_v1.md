# Luna reply 601 — selected grade-one SLP extraction

Implemented the four bounded Task601 outputs: the v3-authenticated
constructive extractor, independent payload checker, candidate-only workflow,
and this receipt. The extractor retains compact little-endian node/edge
streams, reverse-selected grade/lower bitsets, typed roots `C_<1`, `C_T`, and
`C_1`. The canonical SLP structure is one deterministic unique O(V+E) graph
of physical grade/lower roots and all ordered frozen block/old/defect DAG
dependencies, including exact cross-type expressions and terminal literal
words. A separately marked derived traversal retains accumulated leaves for
audit only; it cannot cancel or rewrite the canonical graph. The checker
independently reconstructs and compares the unique graph from sealed state,
checks every defect-to-old dependency and literal dictionary, then checks
closure, acyclicity, roots, receipt bytes, RSS and durable-size caps.
Producer bytes: 25,722; SHA-256
`4cc5d6ccb1bfdcb441b801a4826af04bbbdc9dc7f21d6f7c860d05929e64bfe9`.
Checker bytes: 54,060; SHA-256
`8355fda531b9de41b37df811af932352f07546d6d0ec445764fedaced2595595`.

Bounded local checks:

```text
python -B -m py_compile search/d972_r07_a0_grade1_selected_slp_v1.py search/check_d972_r07_a0_grade1_selected_slp_v1.py
=> exit 0
python -B search/d972_r07_a0_grade1_selected_slp_v1.py --selftest
=> {"coefficient_2":"PASS","fixture":"PASS","nonmonotone_lead":"PASS","reverse_closure":"PASS"}
python -B search/check_d972_r07_a0_grade1_selected_slp_v1.py --selftest
=> {"authoritative_transcript_comparator":"PASS","canonical_validator":"PASS","claim_flag_mutation_count":8,"coefficient_2":"PASS","nonmonotone_lead":"PASS","reverse_closure":"PASS","root_mutation_count":3,"source_mutation_count":13,"transcript_mutation_count":11}
```

Exact inputs are source run/attempt `33677346616/1` and Task595 candidate
run/attempt `33707397894/1`, commit
`93f746ad1b649796e1bc28e00ff34993498929ee`. Production routing and selected
SLP extraction were not run locally; the workflow is the authorized full
execution path.

Task608 repair details: ancestry is now one flattened
`d972.r07.a0.selected-ancestry.v2` schema; stale `structure.old/block` paths
are gone. The checker independently derives the unique source/defect/
expression key closure from selected refs and compares every authenticated
record, including exact ordered children (origin, lower links, reductions), then independently replays selected old origins from sealed lower/lift
blobs and selected block origins from sealed block basis rows. It performs
selected physical edge replay and rejects any nonzero old-origin lower receipt.
The producer records all old lower-zero receipts and physical origin/companion
rows. The shared production source validator rejected 13 source mutations plus
3 root/receipt mutations and 8 claim-flag mutations, and the shared
authoritative transcript comparator rejected 11 transcript mutations.

The checker now also replays all 8,059 offers with the independently authored
router pinned at
`a0504ae6a2562aab3b9af5ba7ed672bcc87bbd1cfdf5cc9fd3489240e51008e3`, and
requires exact lower/grade node records, ordered reduction edges, scales,
lower links, origin rows, companions, and basis bytes.
The verdict additionally binds the canonical payload manifest SHA and the
source-ancestry and roots receipt SHAs.

The payload keeps `direct_occurrence_replay:false`,
`next_degree2_residual:null`, `cross_checked:false`, `verified:false`, and
all A0/COMMON/fake/Ihara flags false. Readiness is
`NOT_READY_NO_LOCAL_SELECTED_SLP_REPLAY`; production output remains a
candidate and the checker marker is emitted only after successful GHA replay.

`R07_GRADE1_SELECTED_SLP_V1_NOT_READY`
