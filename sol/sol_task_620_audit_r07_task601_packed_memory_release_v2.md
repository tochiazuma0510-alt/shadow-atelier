# Sol(max) Task620: independent static release audit of Task601 packed repair

Role: independent mathematical/code auditor.  Do not edit implementation,
run the real route, production, GHA or git.  Write only
`sol/sol_reply_620_audit_r07_task601_packed_memory_release_v2.md`.

Read in full:

1. `sol/sol_reply_618_audit_r07_task601_memory_terminal_v1.md`;
2. `sol/luna_task_619_r07_task601_packed_memory_repair_v2.md`;
3. `sol/luna_reply_601_r07_grade1_selected_slp_v1.md`;
4. `sol/proof_r07_canonical_selected_dependency_slp_v468.md`;
5. `sol/proof_r07_canonical_selected_dependency_slp_physical_replay_v469.md`;
6. `sol/proof_r07_selected_slp_leaf_gated_precision2_join_v470.md`;
7. `sol/proof_r07_endpoint_signature_precision2_consumer_v471.md`;
8. the exact quartet below.

| file | SHA-256 |
|---|---|
| `search/d972_r07_a0_grade1_selected_slp_v1.py` | `5f10b486696e992284d64ffcaa2edd69a74c0e6d7ce94c5e5fd703b3c36e4103` |
| `search/check_d972_r07_a0_grade1_selected_slp_v1.py` | `2e4701f7e3d97326411623694e0ae4eb6b52142951e5cce55ba4f78f3cc64fe6` |
| `.github/workflows/d972-r07-a0-grade1-selected-slp-v1.yml` | `38952d869f8c34f65653282f0db547fdf7d568987e348dfc6c84a2edfcff385c` |
| `sol/luna_reply_601_r07_grade1_selected_slp_v1.md` | `e3cfd3b448c11c19bb4973e801bb5eb34dcf9f7744f17da00f694379b802eb79` |

The first real run `33717064826` ended with producer `MemoryError`; it had no
payload or checker verdict.  This audit decides only whether the exact new
quartet is the bounded Task618 repair and is safe for one rerun.

## Required adjudications

1. Confirm the mathematics and universe are unchanged: registered order of
   all 8,059 offers; offer counts 2,014/6,398; ranks 1,661/5,044; all 3,317
   coefficients and zero remainder; all physical receipts; reverse least
   closure; canonical selected source graph from selected refs alone; three
   roots; full standalone reroute and false/null claim gates.
2. Confirm the producer has one packed edge/row representation from append to
   receipt.  No tuple edge forest, list of row bytes, second join copy or
   quotient-derived state history may survive.  Node lists may exist only
   until closure/packing.  Check that route-only dense companions, owner,
   full source descriptors and echelon matrices are released before source
   graph/leaf materialization.
3. Confirm each full block body/owner is authenticated and consumed one
   character at a time during the route, and at most once more per character
   for selected graph closure.  No per-selected-origin reload and no four
   parsed producer bodies are live together.
4. Confirm `derived.states` and child dictionaries are absent, while the
   complete quotient-specific exact leaf result remains a separately
   authenticated canonical binary receipt.  Audit unique decoding, strict
   order, coefficient/path checks, ancestry-digest binding, the three flags
   `(true,false,false)`, absence of a digest cycle, and the fact that this
   receipt is not the common-source authority.
5. Confirm the checker does not import/call the producer and independently
   derives the whole leaf map from authenticated roots, packed physical
   recurrence and canonical graph, then compares the complete binary stream
   byte-for-byte.  Coefficient two, word multiplication side/order, defect,
   transition, projected-seed and reduction signs must match v467--v471.
6. Confirm the checker parses ancestry once, uses zero-copy/fixed-index node,
   edge and row access, and does not build `gedges`, `ledges`, concatenations,
   expected tuple/row lists or joins.  Row canonicality should be checked once
   per receipt, not rescanned on every edge access.
7. Confirm selected sealed source replay completes character-wise and releases
   all checker block/owner caches before the standalone router loads its
   source.  The router may retain its already accepted four-block source
   representation only after that separation.
8. Audit the online independent comparison.  Every accepted node, every
   ordered reduction, and every origin/stored/companion/zero row must advance
   exact cursors, and terminal must require exhaustion of every authenticated
   stream.  In particular `old-lower-zero` advances for every old offer whose
   lower remainder is zero, whether the subsequent grade row is accepted or
   dependent.  Final basis SHA and exact MEMBER equation remain mandatory.
9. Confirm phase/RSS counters cover Task618's required boundaries without
   per-row logging.  The emergency buffer/`MemoryError` path must emit a
   bounded ASCII `UNKNOWN_RESOURCE` terminal without allocating JSON.
10. Check the workflow's exact producer/checker/reply pins, pre-import v3 pin,
    `[fire-grade1-selected-slp-v2]` marker, pinned actions, serial execution,
    60-minute job, 8-GiB VM/7-GiB RSS and 45-minute process bounds, success-only
    payload/verdict and always-uploaded logs.  No resource enlargement or
    altered parent run is allowed.
11. Run only syntax compilation, the two small selftests and YAML/static
    inspection if useful.  Do not run the real 8,059 route.  Check that the
    fixtures actually reject compact-leaf mutation/order errors, missing
    state boundary, cursor mismatch/exhaustion and every false/null claim.

Report exact bytes/lines/SHA for all inputs, any residual resource risk, and
one verdict: `PASS`, `PASS_AFTER_REPAIR` with a finite mandatory patch list,
or `FAIL`.  A `PASS` authorizes root to commit/push this exact snapshot and
perform the one Task618-authorized GHA rerun.  It does not itself produce an
SLP, fresh residual, A0, COMMON, fake, Ihara, cross-checked or verified claim.
