# Task936 -- minimal rank1355 root-seed scalar adapter

## F1. Disposition and fixed authority

No semantic blocker found. Use one fixed parent-plus-delta separator adapter
and seed-only wrappers around corrected v2 arithmetic. This is design only;
no implementation, numerical execution or successful seed30 replay occurred.

Use run33946247365/1 and all artifact/manifest/result/checker/lambda pins in
Task936 Section1. The inspected result records generation8060/rank1355,
head36feb776736c6587ce9f64d6f5acb883385074a7cc2eed4c2ce7eb8675e71342.
New lambda SHA is
f83bbaa503b8a4d5056f0779085ee4eced542eb1d78d3e35fa9df1c281960565.
The additional source-receipt.json pin is1632 bytes/SHA
f8932ca0b08d6dd7a42fb2560ee5c30adffe39c18d5eafd40a9d1e18ac3a6b30;
it names executed materializer/checker v1, not buffered v2.

Each independent program authenticates the fixed delta roster/seals/payloads,
checker PASS/source receipt, rolling append, and unchanged parent joins.
Expose generation/rank/head/lambda explicitly. The existing separator row
loop can stream/hash old physical.bin once with NEW lambda, then check the
delta normalized row: all1355 dots zero. Check lambda dot new saved target
remainder equals one. Accepted state/delta/rho2 derivations remain premises.
No state copy, old instruction/Conn replay, target elimination or rho2
staging is needed.

## F2. Exact reusable entry points and stale-pin pitfalls

P = d972_r07_actual_grade2_root_scalar_batch_v2.py.
C = check_d972_r07_actual_grade2_root_scalar_batch_v2.py.
Reuse each side's own pinned v15 lineage; no shared new arithmetic.

| Layer | Reuse / narrow replacement |
|---|---|
| Parents | Reuse both validate_p1/validate_task554, P _state_descriptor(..., need_blobs=True), C state_descriptor. Replace validate_launch/validate_separator with fixed delta wrappers. |
| Roots | Reuse ARITH.read_task712_envelope/sparse_adjoint. Derive all four q_a=B_a^*lambda_new. Do not inherit make_covectors/covectors EXPECTED_ROOT/EXPECTED_CHILD pins or actor children. |
| P1 values | Reuse vectorized_projection_chunk and buffered cache/hash loop. Replace p1_batch/p1_values wrappers: one vector per character and dynamic active characters, not five vectors or fixed [True,False,False,False]. |
| Direct seeds | Reuse P source_context/raw_seed_direct and C checker_source_context/checker_raw_seed_direct with actual_pin=False. The old seed2 scalar assertion is lambda-dependent. |
| Relations | Extract only seed clauses of both accumulate_scalars; no actor/lower-adjoint contraction sweep. |
| Output | Seed-only wrappers replace _scalar_result/_expected_character/_scan_accumulated and all-origin terminals. |

Critical head trap: P raw_dual has an old-head fallback; C make_raw hardcodes
SEPARATOR_STATE_HEAD. Both new serializers must explicitly bind generation8060,
new head and new lambda. Do not monkeypatch old globals or call old
run_actual/check_actual unchanged.

## F3. New-q computation and scope

Recompute v_a[i]=<q_a,P1_degree2_row_i[a]> for each a=0..3, i=0..8058.
The immutable P1 cache/coefficients are reusable; old contracted values and
seed scalars are not. One buffered cache pass gives four fresh8059-entry
uint8 arrays (32236 bytes). A zero root may skip multiplication only after
being freshly derived, with its authenticated zero result retained.

Maintain a4x44 accumulator:
s_a[k]=<q_a,Eval_raw(seed_k).d2[a]>-sum_i SeedRed(k)[i]*v_a[i].
This is v541(2.1), not projection of only the direct seed. Read prepare once,
then one new block at a time, releasing each body. Include all four old
seed expressions at offsets(0,505,1008,1511), and every target block's four
origins ORIGIN_RANGES[c][0]+k at offsets(2014,3523,5035,6547). Preserve term
order/multiplicity and source receipts. No actor lower-blob dot pass.

Emit fresh roots and44 scalars each in character-major, seed0--43 order.
First nonzero gives ROOT_SEED_VIOLATION bound to raw q, new delta, P1 values
and complete seed relation. All176 zero gives ROOT_SEEDS_ZERO with
actor_origins_executed=0 and orbit_rows_executed=0, never full ScalarEOF or
grade-wide nonmembership. A next nonzero seed still needs its separate
full lower-zero/physical materializer gate. Seed30's scalar belongs to this
new-lambda scan; its successful physical materialization is not repeated.

## F4. Proposed implementation scope and CLI

Three new files, pending root adoption:

- search/d972_r07_rank1355_root_seed_scalars_v1.py
- search/check_d972_r07_rank1355_root_seed_scalars_v1.py
- .github/workflows/d972-r07-rank1355-root-seed-scalars-v1.yml

Common CLI: --delta-root NEW_DELTA --state-root TASK904 --prepare-root PREPARE,
four ordered --block-root arguments B0/B1/B2/B3, --p1-root P1, --task712-root TASK712.
Producer adds --output-root FRESH_OUTPUT; checker adds --candidate-root FRESH_OUTPUT.
Compile fixed parents, retain launch/source receipts, stage the existing
Task554/P1/Task712/Task904 tuples plus this delta and run serially. No old
scalar diagnostics, rho2 stager, buffered materializer rerun or generic
checkpoint framework. Use buffered reads and phase/count progress.

Only this reply was edited. No local Python/GAP/network/git/GHA operation.
No new q/scalar/grade2/A0/COMMON/COFINAL/FAKE/IHARA claim; verified=false.
