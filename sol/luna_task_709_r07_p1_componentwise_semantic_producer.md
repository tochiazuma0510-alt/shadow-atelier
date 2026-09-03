# Luna Task709: phase-separated componentwise P1 semantic replay producer

Role: Luna implementation.  Read the FULL task, `sol/proof_r07_grade2_p1_componentwise_semantic_replay_v482.md`, and accepted audit `sol/sol_reply_706_audit_r07_v482_componentwise_semantics.md` first.

Modify only:

1. new `search/d972_r07_grade2_p1_componentwise_semantic_replay_v1.py`;
2. new `sol/luna_reply_709_r07_p1_componentwise_semantic_producer.md`.

Do not edit the frozen structural producer, workflows, v220, source artifacts, grade1-v4, git, or any other file.  Do not run the actual five-artifact replay locally and do not start parallel Python.

## Mathematical/compute design

Implement the accepted v482 implication by read-only regeneration of the original echelon closures, not by dense `8059 x 96776` assembly and not by multiplying every stored coefficient expression by a global matrix.  Reuse the audited finite arithmetic from `search/d972_r07_a0_first_rung_grade1_v4.py` and strict authentication conventions from `search/d972_r07_grade2_specific_owner_prejoin_v1.py`, while keeping this producer's live replay logic explicit and independently fixtureable.

Expose four fail-closed modes:

1. `--selftest`;
2. `--prepare-replay PREP_ROOT`;
3. `--block-replay PREP_ROOT BLOCK_ROOT --index I` for exactly `I=0,1,2,3`;
4. `--join-receipts PREP_JSON B0_JSON B1_JSON B2_JSON B3_JSON`.

This separation is required so GHA can run one prepare job and four block jobs in parallel; the join is small and deterministic.

## Prepare replay

- Authenticate the exact Task554 prepare root/body/15-file roster, input pins/manifest, four old lower blobs, four old lifted-grade blobs, and four packet blobs.  Bind the accepted run/head/body/blob identities already frozen by the structural producer.
- Rebuild the grade1 context and all 44 literal seed occurrence pairs from the pinned words.  For each character, recompute the projected seeds and replay the complete `close_lower_block` insertion/FIFO actor process into a fresh packed echelon.  Compare every insertion expression, ordered DAG node/scale/origin/reduction, seed reduction, four actor transitions, leads, final rank and exact final lower-basis bytes with the authenticated prepare state.
- Recompute the old lifted-grade rows in DAG order using the exact projected seed or actor origin and compare all 72,576-trit companions byte-for-byte with the pinned lifted-grade blobs.
- In the original origin order, recompute each degree-one residual as
  `direct grade - sum(q * old lifted grade)`, split all four lambda components, and compare every component byte-for-byte with its authenticated packet row.  Do not compare a raw direct grade to a packet.  This phase must account for 176 old-seed lower relations, 8,056 old-actor lower relations, 2,014 old DAG identities, and 32,928 direct-residual-to-packet halves.
- Emit only a compact canonical JSON receipt with exact input digests, counts, deterministic equality/digest receipts, runtime/RSS and all downstream claims false.  No row family is emitted.

## One block replay

- Authenticate the prepare parent/selected packet and the exact three-file block root/body/basis for `index`; enforce the frozen character/rank/attempt/order/digest pins and full typed semantics.
- Starting with a fresh packed echelon, stream the 8,232 selected packet rows in order.  Compare each returned exact `expression_from_insert` with `origin_reductions`; for every accepted row compare the next ordered DAG node including scale, defect origin and reductions.
- Drain the FIFO exactly as `run_block_core`: apply all four `associated_grade_actor` operations to each accepted row, compare every returned expression with the stored actor transition, and compare every newly accepted actor-origin DAG node.  At exhaustion compare attempts, rank, queue, pivot leads, DAG digest, and exact final packed basis bytes/blob digest.
- Emit a compact canonical receipt accounting for 8,232 packet-to-basis halves, `4*n_lambda` new actor identities and `n_lambda` new DAG identities.  Never retain more than one parsed block plus its local packed owner/needed packet data.  No global matrix or other block is allowed.

## Receipt join

- Parse canonical JSON only; require exact key/type sets, distinct indices 0..3, common prepare/run/head/body/packet ancestry, producer code receipt and phase-schema versions.
- Require totals: old ranks 2,014; new ranks 6,045; all DAG 8,059; old local 8,232; direct-packet 32,928; packet-basis 32,928; new actors 24,180; compound v482 obligations 65,340; binary comparisons may be separately reported as described by Task706.
- Bind `sum_chi P_chi=1`/44 seed reconstruction as an exact producer assertion based on the pinned four pure words and field arithmetic, not a prose flag.
- Only then emit terminal `TASK554_P1_COMPONENTWISE_SEMANTICS_REPLAYED`, with `global_relations=32280`, `resident_global_matrix=false`, `independent_checker=false`, `precision2=false`, `A0=false`, `COMMON=false`, `COMPATIBLE_LIFT=false`, `FAKE=false`, `IHARA=false`, `verified=false`.

## Bounded checks and reporting

- Build small deterministic fixtures that reach the live phase helpers and reject at least: packet sign/raw-grade confusion, one packet byte mutation, one expression coefficient mutation, one DAG forward edge, one actor transition mutation, shared-Aux omission, wrong block index/ancestry, duplicate/missing join receipt, and noncanonical/bool-as-int receipt fields.
- Run `py_compile` and bounded `--selftest` only.  Actual artifact replay is `DEFERRED_TO_GHA`.
- Report exact candidate bytes/LF/final-LF/SHA, static import/API census, selftest receipt, and an honest memory/runtime design statement.  Do not claim cross-check, grade-two progress or structural promotion.
- End `READY_FOR_SOL_P1_SEMANTIC_PRODUCER_AUDIT`; `verified=false`.
