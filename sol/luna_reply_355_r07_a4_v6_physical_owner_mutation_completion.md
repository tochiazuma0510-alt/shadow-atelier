# Luna reply 355 — R07 A4/v6 physical-owner mutation completion

## Result and scope

This bounded turn created only the five permitted v6 paths.  The frozen v5
mathematical core was copied and schema/pin-versioned; the requested physical
mutation layer was not completed.  I therefore report `BLOCKED / UNEXECUTED`.
No Python, Node, GAP, GHA, workflow, git, or network command was run.  The
following sizes and hashes are read-only PowerShell file measurements, not
runtime measurements.

| v6 output | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_v6.py` | 219187 | `aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a` |
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v6.py` | 258847 | `432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g` | 13775 | `a12c9267d050fe8ae9155cc9c42dd35dc5f1a66452c54f6a2cc7246f9a009fb0` |
| `search/certs/d972_r07_word_independent_successor_kernel_selftest_v6_20260829.json` | 5026 | `f04d8ef01d5b9c1cc9e05f674e6868dae67d7c60b1f51573c5b90c80ca365545` |

The driver pins the first, second, and fourth files exactly and deliberately
does not pin its own bytes: the v293 acyclic attestation graph binds the
driver externally rather than creating an in-file SHA fixed point.  The
fixture is versioned and retains all 48 names/order, but its
`expected_rejections.producer` and `expected_rejections.checker` maps are
empty.  This is an intentional fail-closed state, not an acceptance claim.

## First blocker

There is no `PhysicalOwnerRoute` (or equivalent physical transport API) in
either v6 source.  Both implementations still use the v5-style in-memory
`OwnerRoute`/`_slot` layer (`producer` lines 2968–3005 and 3270–3330;
`checker` lines 2952–2989 and 3245–3290).  It hashes a live Python value with
`sha(canon(jsonable(...)))`, mutates that value in place, and invokes a
selftest callback.  It does not create an owned temporary authenticated
envelope, reopen it through the ordinary parser, record file/path/handle
identity, emit an ordinary entry event, or derive the first rejection from
that event.  Physical authority, row/chunk/bridge/ABI, output/checkpoint,
atomic/stale/sentinel, and TOCTOU mutations consequently have no actual
owner route.

The exact deterministic stop is earlier still: the fixture line 1 contains
`{"producer":{},"checker":{}}`; producer `selftest_certificate` lines
3339–3342 and checker lines 3305–3308 require each map to contain all 48
names before constructing/exercising routes.  Thus no exact first-reason row
exists to report truthfully.  Filling the maps with guessed reasons would
violate v297 §§1–8 and task355 §4.  The current `OwnerRoute.exercise` also
sets `reached=True` before calling its callback and has no ordinary event
trace/baseline terminal proof, so it cannot be relabelled as the required
trace.  Several names share one live slot (`selected`, `pair_count`, and
`first_item` fields), which is another actual-owner failure.

## Import, process, and authority graph

The v6 producer imports only the standard-library modules shown at lines
13–28 and has no checker import.  Its static process is:

```text
driver: D345Pins/authority pins (lines 1–45)
  -> generated serial shell and terminal/sentinel contract (lines 76–145)
  -> producer v6 main (3463+)
       -> bounded path/read/checkpoint input (503–603, 2834–2916)
       -> AuthorityAdapter/read and validation (612+, 532+)
       -> primitive inventory (1195–1239)
       -> forward DAG (1134–1193), ancestry replay (1246–1370)
       -> mixed B/K LiveBasis (1372–1616), WordDAG (1618–2057)
       -> row consumer/queue (build_kernel 2207–2411)
       -> action matrices and v280 anchor (2059–2205)
       -> result/checkpoint/sealed terminal (2468–2916, 3355–3518)
       -> v6 selftest gate (3332–3353)
```

The v6 checker has no producer import either.  It independently follows:

```text
checker main (3822+)
  -> own bounded input/producer-envelope read (537–618)
  -> own Authority (619+, 562+)
  -> checker primitive inventory (1225–1271)
  -> reverse suffix DAG (1173–1223), ancestry (1273–1386)
  -> own Basis and mixed B/K reconstruction (1388–1702, 1868–2090)
  -> fused bridge trace (1643–1702)
  -> own row consumer/queue (build_checker_kernel 2278–2471)
  -> own action/anchor/positive comparison (2118–2276, 3338–3603)
  -> checkpoint/terminal validation (2544–2915, 3605–3819)
  -> v6 selftest gate (3300–3336)
```

The driver authority graph is physical and pinned at lines 45–75.  The
principal owners are: task198 receipt
`ci/in/d972_r07_seven_context_roof_presentation_v1.json` (31017244 bytes,
`82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5`), its
manifest (2722,
`cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4`),
producer attestation (81,
`b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090`),
checker attestation (95,
`260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e`),
and checker verdict (150,
`ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de`).
The task198 source pins are producer 137169/
`6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c`,
checker 157253/
`001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1`, and
driver 20541/
`6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068`.

The remaining frozen authorities are E4 source 535219/
`fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29`, Q3
receipt 231570/
`3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`, and
the task176 chain: receipt 13649089/
`715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41`,
manifest 349/
`de62e5e55a2e348a3cce297764f7ff4bfedc10ebe2545f22cbc1551f15e1adc1`,
producer 66109/
`878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b`,
checker 84980/
`4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695`,
physical checker result 757/
`e6a45a34353ce1fb54c99b4f9cbc8b106f34bfc751dd50044f2a79da72cad5e5`,
recovery-v1 2035/
`41d2cb72614ce7e2d5b2d7a9000e861414da1c749876b3d51f1ccf2ca63390a8`,
and corrected recovery-v2 2690/
`67dd555f6e0f943d0161ef2f2c8124b4cc31c9167846b45b43fd2001f5fbba3f`.
Recovery-v2 is the active owner; its self digest is
`e95b4e7781a14cffd07d445141f20c942861168d201f2ce62879a0ddf3a45026`,
and v1 remains superseded because of its accepted-receipt transcription
error.  The task176 source hashes are recorded exactly in the driver and
are not replaced by prose or detached reply data.

## Section 11 static traces

The driver pins and writes the generated shell in lines 1–75 and invokes its
static `Exec` at line 145; this invocation was not executed.  Producer row
1/row 6319/later-row assembly is statically in `build_kernel` lines
2263–2336, with ancestry at 1246, forward DAG construction at 1134, and
fused bridge at 1072.  The checker performs the opposite route in
`build_checker_kernel` lines 2278–2398, suffix DAG 1173, and independent
bridge trace 1643.  Closure is `run_queue` producer lines 2351–2411 and
checker lines 2413–2471; matrix/ordered-basis/anchor construction is
producer 2059–2205 and checker 2118–2276.  These are static routes only;
they do not establish a successful v6 run.

The typed branches are statically located at producer `write_sealed`
2540+, `write_checkpoint_snapshot` 2751+, `restore_checkpoint` 2834+,
`terminal_certificate` 3430+, and `main` 3463+; checker `write_sealed`
2544+, checkpoint writer 2749+, restore 2823+, terminal-checkpoint
validator 3605+, terminal-payload validator 3678+, terminal certificate
3790+, and main 3822+.  Member, boundary-rank-rise, ZERO/K-rank-rise,
anchor-zero, UNKNOWN_INPUT, UNKNOWN_RESOURCE, checkpoint/resume, and hard
exception paths are represented in these frozen-core branches, but no
v6 physical mutation experiment entered them.  The driver separates fresh
outputs from RESUME checkpoints and compares terminal status tokens at its
generated shell lines 101–145; this remains unexecuted.

## Static formulas and counts (not measurements)

The retained core uses `S(uv)=S(u)S(v)` over ten typed affine/Fox contexts,
F3 arithmetic, MEMBER action column `c`, and rank-rise action column
`c+s^{-1}e_new = c+s e_new`.  Mixed formal rows satisfy
`C_alpha = Psi(Q_alpha) + sum_l c_alpha[l] K_l`; a boundary pivot is
`s(d - sum_mu mu p_mu)` with propagated `(Q,c)`, and a K pivot has formal
`(0,e_new)`.  K closure retains
`W_new=(W_v product_l W_l^(-c_l))^s` and
`E_new=s*(E_v+Q-sum_l c_l E_l)`.  The v280 anchor uses the least nonzero
`a_j`, `e=a_j^-1`, star column `e e_j`, tilde columns
`e_i-a_i e e_j`, and the corresponding inverse matrix.

Static cardinalities retained by the frozen core are rows 6441, contiguous
layers 6318/104/19, ten contexts, 65 seed families (5*2 + 5*11), 288
primitive words, 114458 literal primitive letters, 5475488 stored row
letters, producer forward edges 15970 with 159700 edge states, checker
reverse edges 26136 with 261360 edge states, and row-piece product count
19408 (=3*6318 + 4*104 + 2*19).  Checkpoint row boundaries are
1024, 2048, 3072, 4096, 5120, 6144, and 6441.  None of these are measured
runtime/RSS results in this turn.

## All 48 producer/checker mutation owner slots

`P` and `C` below are the actual slots wired by the current v6 source, not
claims that task355 accepts them. `PHYS-REQ` means task355 requires a real
owned file/envelope/path/handle/transport identity. `EPH-REQ` is a
genuinely ephemeral algebraic owner which may use a live object only when
the ordinary validator consumes that same object. `EPH-CURRENT` means the
current slot is such an in-memory slot but still lacks v297 event/baseline
evidence. `PHYS-MISSING` means the current slot is an inadmissible in-memory
substitute for a required physical owner. Every `first_rejection` value is
`UNEXECUTED / UNBOUND`; it is deliberately not an invented narrow reason.

| # | mutation | P owner slot | C owner slot | required/current class | current P callback | current C callback | exact first rejection |
|---:|---|---|---|---|---|---|---|
| 1 | `per_layer_ordinal` | `authority.rows[0].ordinal` | `authority.rows[0].ordinal` | PHYS-MISSING | `authority.validate` | `authority.validate` | UNEXECUTED / UNBOUND |
| 2 | `authority_binding` | `authority.values[manifest].accepted` | same | PHYS-MISSING | `authority.validate` | `authority.validate` | UNEXECUTED / UNBOUND |
| 3 | `canonical_input_bytes` | `authority.raw[receipt]` | `authority.raw[receipt]` | PHYS-MISSING | canonical-byte lambda | checker input-byte lambda | UNEXECUTED / UNBOUND |
| 4 | `resolved_path_traversal` | `authority.paths[receipt]` | `authority.paths[receipt]` | PHYS-MISSING | `exact_path` | `exact_path` | UNEXECUTED / UNBOUND |
| 5 | `normal_generation_proof` | receipt `Delta0.presentation.normal_generation_proof.Gamma_cayley_edge_count` | same | PHYS-MISSING | `authority.validate` | `authority.validate` | UNEXECUTED / UNBOUND |
| 6 | `bridge_typed_occurrence_ledger` | receipt `bridge.occurrence_ledger[0].block` | same | PHYS-MISSING | `authority.validate` | `authority.validate` | UNEXECUTED / UNBOUND |
| 7 | `evaluator_abi_canary` | receipt `evaluator.coordinate_widths[0]` | same | PHYS-MISSING | `authority.validate` | `authority.validate` | UNEXECUTED / UNBOUND |
| 8 | `raw_boundary_coefficient` | `basis.boundary.rows[p0][k0]` | `basis.bspace.rows[p0][k0]` | EPH-REQ / EPH-CURRENT | `check_echelon` | `check_echelon` | UNEXECUTED / UNBOUND |
| 9 | `live_echelon_inherited_scale` | `basis.combined.rows[p0][k0]` | `basis.combined.rows[p0][k0]` | EPH-REQ / EPH-CURRENT | `check_echelon` | `check_echelon` | UNEXECUTED / UNBOUND |
| 10 | `producer_checker_basis_change` | `basis.k_items[0].raw_coefficients[k0]` | same | EPH-REQ / EPH-CURRENT | `check_k` | `check_k` | UNEXECUTED / UNBOUND |
| 11 | `conjugator_order` | `authority.rows[6318].ancestry.tokens` | same | PHYS-MISSING | `check_ancestry(6318)` | `check_ancestry(6318)` | UNEXECUTED / UNBOUND |
| 12 | `source_word_basis_boundary_difference` | `basis.k_items[0].word` | same | EPH-REQ / EPH-CURRENT | `check_k` | `check_k` | UNEXECUTED / UNBOUND |
| 13 | `negative_dual` | `oracle.live_duals[0].dual[k0]` | same | EPH-REQ / EPH-CURRENT | `check_dual` | `check_dual` | UNEXECUTED / UNBOUND |
| 14 | `action_matrix` | `action_matrices["1"][k0]` | same | EPH-REQ / EPH-CURRENT | `check_actions` | `check_actions` | UNEXECUTED / UNBOUND |
| 15 | `projected_h2_exponent` | `anchor.basis_q[0].exponent` | same | EPH-REQ / EPH-CURRENT | `check_anchor` | `check_anchor` | UNEXECUTED / UNBOUND |
| 16 | `k_z_inverse_scalar_powered_word` | `anchor.powered_word` | same | EPH-REQ / EPH-CURRENT | `check_anchor` | `check_anchor` | UNEXECUTED / UNBOUND |
| 17 | `live_resource_cap` | `meter.limits[wall_seconds]` | same | EPH-REQ / EPH-CURRENT | resource-cap lambda | checker-cap lambda | UNEXECUTED / UNBOUND |
| 18 | `positive_status_terminal` | `normal.status` | `normal.status` | PHYS-MISSING | `check_terminal` | `check_terminal` | UNEXECUTED / UNBOUND |
| 19 | `nonpositive_false_progress` | `normal.complete` | `normal.complete` | PHYS-MISSING | `check_terminal` | `check_terminal` | UNEXECUTED / UNBOUND |
| 20 | `duplicate_markers` | `normal.driver_contract.producer_terminal_lines` | `normal.driver_contract.checker_terminal_lines` | PHYS-MISSING | `check_driver` | `check_driver` | UNEXECUTED / UNBOUND |
| 21 | `inconsistent_section_word` | `authority.rows[0].ancestry.record_word` | same | PHYS-MISSING | `check_ancestry(0)` | `check_ancestry(0)` | UNEXECUTED / UNBOUND |
| 22 | `altered_primitive_terminal` | `forward.nodes[1].length` | `suffix.nodes[1].length` | EPH-REQ / EPH-CURRENT | `check_dag` | `check_suffix` | UNEXECUTED / UNBOUND |
| 23 | `wrong_trie_edge_orientation` | `forward.nodes[0].edges[e]` | `suffix.nodes[0].edges[e]` | EPH-REQ / EPH-CURRENT | `check_dag` | `check_suffix` | UNEXECUTED / UNBOUND |
| 24 | `wrong_action_orientation` | `authority.rows[6318].orientation` | same | PHYS-MISSING | `check_ancestry(6318)` | `check_ancestry(6318)` | UNEXECUTED / UNBOUND |
| 25 | `wrong_target_inverse` | `authority.rows[0].ancestry.section_target_word` | same | PHYS-MISSING | `check_ancestry(0)` | `check_ancestry(0)` | UNEXECUTED / UNBOUND |
| 26 | `producer_checker_row_mismatch` | `sample_rows[1].row[k0]` | same | PHYS-MISSING | `check_sample` | `check_sample` | UNEXECUTED / UNBOUND |
| 27 | `missing_base_boundary` | `ledger.seeds[0].index` | `boundary.seeds[0].index` | EPH-REQ / EPH-CURRENT | seed-roster lambda | seed-roster lambda | UNEXECUTED / UNBOUND |
| 28 | `changed_boundary_block_tag` | receipt `bridge.occurrence_ledger[0].block` | same | PHYS-MISSING | `authority.validate` | `authority.validate` | UNEXECUTED / UNBOUND |
| 29 | `left_right_translation_swap` | `first_corr.selected` | same | EPH-REQ / EPH-CURRENT | `check_dual` | `check_dual` | UNEXECUTED / UNBOUND |
| 30 | `omitted_inverse_action` | `action_matrices["-1"][k0]` | same | EPH-REQ / EPH-CURRENT | `check_actions` | `check_actions` | UNEXECUTED / UNBOUND |
| 31 | `changed_parent_action_ancestry` | `actions[0].parent` | same | PHYS-MISSING | parent-ancestry lambda | checker parent lambda | UNEXECUTED / UNBOUND |
| 32 | `incomplete_queue_claim` | `queue_state.cursor` | same | PHYS-MISSING | `check_queue` | `check_queue` | UNEXECUTED / UNBOUND |
| 33 | `wrong_support_inversion_product` | `first_corr.selected` | same | EPH-REQ / EPH-CURRENT | `check_dual` | `check_dual` | UNEXECUTED / UNBOUND |
| 34 | `false_zero_correlation` | `first_corr.pair_count` | same | EPH-REQ / EPH-CURRENT | `check_dual` | `check_dual` | UNEXECUTED / UNBOUND |
| 35 | `omitted_candidate_discrepancy` | `candidate_item.candidate_E` | same | EPH-REQ / EPH-CURRENT | `check_k` | `check_k` | UNEXECUTED / UNBOUND |
| 36 | `omitted_prior_k_discrepancy` | `prior_item.discrepancy` | same | EPH-REQ / EPH-CURRENT | `check_k` | `check_k` | UNEXECUTED / UNBOUND |
| 37 | `flipped_q_sign` | `first_item.Q` | same | EPH-REQ / EPH-CURRENT | `check_k` | `check_k` | UNEXECUTED / UNBOUND |
| 38 | `missing_discrepancy_scale` | `first_item.normalization_scale` | same | EPH-REQ / EPH-CURRENT | `check_k` | `check_k` | UNEXECUTED / UNBOUND |
| 39 | `reversed_source_action_discrepancy` | `first_item.E_formula` | same | EPH-REQ / EPH-CURRENT | `check_k` | `check_k` | UNEXECUTED / UNBOUND |
| 40 | `changed_raw_tag_translation` | `first_item.discrepancy` | same | EPH-REQ / EPH-CURRENT | `check_k` | `check_k` | UNEXECUTED / UNBOUND |
| 41 | `modulo_discovered_b_only_replay` | `first_item.row` | same | EPH-REQ / EPH-CURRENT | `check_k` | `check_k` | UNEXECUTED / UNBOUND |
| 42 | `deleted_active_key` | `basis.active_registry` | same | EPH-REQ / EPH-CURRENT | `check_dual` | `check_dual` | UNEXECUTED / UNBOUND |
| 43 | `unregistered_dual_key` | `first_dual.dual` | same | EPH-REQ / EPH-CURRENT | `check_dual` | `check_dual` | UNEXECUTED / UNBOUND |
| 44 | `raw_pivot_functional` | `basis.k_rows[first_item.label]` | same | EPH-REQ / EPH-CURRENT | `check_k` | `check_k` | UNEXECUTED / UNBOUND |
| 45 | `omitted_matching_occurrence` | `first_corr.pair_count` | same | EPH-REQ / EPH-CURRENT | `check_dual` | `check_dual` | UNEXECUTED / UNBOUND |
| 46 | `incomplete_translation_key` | `translation_item.c` | same | EPH-REQ / EPH-CURRENT | `check_k` | `check_k` | UNEXECUTED / UNBOUND |
| 47 | `premature_zero_correlation` | `first_corr.pair_count` | same | EPH-REQ / EPH-CURRENT | `check_dual` | `check_dual` | UNEXECUTED / UNBOUND |
| 48 | `omitted_new_key_registration` | `basis.k_rows` | same | EPH-REQ / EPH-CURRENT | `check_k` | `check_k` | UNEXECUTED / UNBOUND |

For every row above, `owner_digest` is currently only
`sha256(canon(jsonable(read_live_slot())))`; it is not the v297 physical
identity `(resolved path, bytes, length, SHA, opened-handle identity, link
count, type)`, and no actual `before_identity != after_identity` evidence or
post-mutation baseline revalidation was generated.  No exact normal validator
entry event or narrow first reason is therefore available.  In particular,
the repeated slots in rows 6/28, 29/33, 34/45/47, and several `first_item`
rows are not distinct physical owners.

## Required follow-up boundary

The first missing owner/API is the producer/checker-separated physical
mutation transport plus its ordinary event trace, followed immediately by
the complete 96-cell exact-reason registry.  Until those are implemented and
the unmutated baselines pass through the same ordinary paths, any
`IMPLEMENTED` or exact first-reason claim would be fabricated.  A future
Sol(max) audit must also recheck the v5 frozen core, physical Linux/Windows
identity behavior, checkpoint/terminal accounting, and all 96 route ledgers
before execution.

V6 PHYSICAL MUTATION LAYER:     BLOCKED
IMPLEMENTATION:                  BLOCKED
SELFTEST / PRODUCTION:           UNEXECUTED
AUTHORITY-V2 INPUT:              A4 1/3 only
ACTUAL POSITIVE BRANCH:          BLOCKED
SOL(MAX) REAUDIT REQUIRED:       YES
ACTUAL A4:                       remains 1/3 at most before execution
LIFT / FAKE / IHARA:             NONE
