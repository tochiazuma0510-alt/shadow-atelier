# Luna task 189 — actual R07 cyclic Fox-template inventory

Status: STATIC INVENTORY COMPLETE.  This delivery is source/provenance
inventory only.  No Python, Node, GAP, git, GHA, or heavy local computation
was run, and no implementation file was changed.  This report does not
declare a cyclic base-change result, Smith divisibility, a lift, a fake, or a
witness.

## 0. Read set and identities

The three governing papers and the task179/task186 dependency cone were read
in full as requested.  The following are the byte identities observed in the
working tree (SHA-256, lowercase):

| file | bytes | SHA-256 |
|---|---:|---|
| `sol/proof_r07_cyclic_fox_basechange_template_v164.md` | 10463 | `f4dd701e10d549b44dfb56d58269af783e987ab8c3bd8d81305f4bb43181fedc` |
| `sol/proof_r07_procyclic_inverse_limit_smith_homotopy_v133.md` | 11589 | `1f5083a00fa083fa4cb66e36691e8a97a6cc6f12a94e264be6dc76e65accf90b` |
| `sol/proof_r07_task179_to_augmented_edge_compiler_v144.md` | 7531 | `394a8a26f3462e91e3ec6026816d21d5373e3250532b13b3c20add9d0fc6df24` |
| `search/d972_r07_positive_common_word_colgen_v1.py` | 123870 | `47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7` |
| `crosscheck/check_d972_r07_positive_common_word_colgen_v1.py` | 73780 | `de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d` |
| `search/d972_r07_normalized_exact_common_word_colgen_v2.py` | 63053 | `ec73db0a474b3b52d69e19862e8185ae22423b2406f3922b5669d9a4e85fafab` |
| `crosscheck/check_d972_r07_normalized_exact_common_word_colgen_v2.py` | 54982 | `8898798d0d6a9e0b6cd67402e74ba0dc5048b4797a0f7a9657e58d70d553c488` |
| `search/d972_r07_all_seven_raw_bridge_preflight_v1.py` | 60306 | `1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa` |
| `crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py` | 88503 | `0b45c3daa1db6cad63d434170c65d0dbfa928efc51543b881dc0aa2e3a0f1fce` |
| `search/d972_r07_all_seven_extension_section_census_v1.py` | 66109 | `878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b` |
| `crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py` | 84980 | `4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695` |

The task179 pins additionally bind the authenticated q3/joint receipts,
`d972_b345_seedspan_triple4_v1.py`, the old arithmetic, v172 roster source,
g760 source, and PB4 source.  Their identities are retained verbatim in the
task179 producer/checker `PINS` tables; this inventory does not replace those
pinned inputs.

## 1. Actual production source of the eleven Fox slots and boundaries

### 1.1 Base and the H1/H2 slots

`search/d972_r07_all_seven_raw_bridge_preflight_v1.py:646-698` obtains the
760-letter base word from the independently constructed
`p175_g760.construct_base()`, checks length 760 and the registered digest,
then computes `old.hexagon_words(g)` and embeds both hexagons with
`old.embed_f2_pb3`.  The same file constructs the corrected preflight word
as `free_reduce(g760 + c)` for a deterministic roster canary.  In the actual
task179 search, `AllSevenModel` instead reads the authenticated bridge
`bridge["g760"]["word"]`; selected correction columns are rebuilt from the
authenticated 6441-row roster.

`search/d972_r07_positive_common_word_colgen_v1.py:637-697` fixes
`x=[1]`, `y=[2]`,
`z=inverse(paper_product(x,y))`, and
`u=inverse(paper_product(y,x))`.  `_substitute` calls
`old.f2_substitute`, and H slots additionally call
`old.embed_f2_pb3`.  The exact six H slots are:

| slot/label | block and typed ambient | coordinate | source pair | sign | PB3 lift |
|---|---|---:|---|---:|---:|
| H1_fxy | 1 / E3 | 0 | `(x,y)` | +1 | yes |
| H1_fxz | 1 / E3 | 1 | `(x,z)` | -1 | yes |
| H1_fyz | 1 / E3 | 2 | `(y,z)` | +1 | yes |
| H2_fux | 2 / E3 | 3 | `(u,x)` | -1 | yes |
| H2_fxy | 2 / E3 | 0 | `(x,y)` | -1 | yes |
| H2_fuy | 2 / E3 | 4 | `(u,y)` | +1 | yes |

For each slot, `occurrence_data` and `occurrence_column` use the substituted
literal relation, signed factor, frozen occurrence prefix, and
`old.fox_gradient_without_sections`.  `occurrence_column` then applies the
two nested `translate_vector` calls and serializes a block-tagged typed row;
the E1/E2 entries are added at this call site, with task186 replacing the
underlying exponent-pair semantics by its normalized hook.  The
fresh `direct_column` path (`:784-827`) separately computes base-versus-
corrected H1/H2 gradients and requires equality with the eleven-slot
occurrence column.

The task179 receipt/checkpoint provenance for a retained correction carries
`delta_word`, `relator_word`, `conjugate_word`, `corrected_word`,
`quotient_value_blobs`, `eleven_occurrence_replay`, and
`direct_all_seven_replay`.  The task186 wrapper preserves this v1 path and
adds normalized-column, exactification, and direct-replay fields; it does not
replace the H1/H2 source.

### 1.2 The five printed A.18 occurrences

The source arithmetic keeps the natural context list in the order
`(b3,b1,b5,b2,b4)` (`pcontexts` in task175/task179).  The printed Fox order
is explicitly `(b1,b2,b3,b5^-1,b4^-1)`, implemented in task179 by natural
indices `(1,3,0,2,4)` and in task176 by typed coordinates 5 through 9.

| printed slot/label | natural index | coordinate | literal context `(left,right)` | block | sign | task176 context/role |
|---|---:|---:|---|---|---:|---|
| `P_b1` | 1 | 5 | `([4],[6])` | E4 | +1 | C1 / `pentagon_b1` |
| `P_b2` | 3 | 6 | `(paper_product([1],[2]), paper_product([5],[6]))` | E4 | +1 | C27 / `pentagon_b2` |
| `P_b3` | 0 | 7 | `([1],[4])` | E4 | +1 | C21 / `pentagon_b3` |
| `P_b5_inverse` | 2 | 8 | `(paper_product([2],[4]),[6])` | E4 | -1 | C26 / inverse slot |
| `P_b4_inverse` | 4 | 9 | `([1],paper_product([4],[5]))` | E4 | -1 | C28 / inverse slot |

The literal pentagon constructor in task175 (`:699-709`) and task179
`_pentagon_word` (`:778-782`) both preserve the displayed order and the two
negative factors.  The E4 `direct_column` path compares the five-factor
pentagon gradient of `g760` with that of `g760 * conjugate`, while the
occurrence path computes the same five slots through the stored prefixes.

The bridge receipt records these source choices in `pentagon` (factor blobs,
base factor blobs, ordered intermediate/value blobs, ordered indices
`[1,3,0,2,4]`, signs `[1,1,1,-1,-1]`) and `literal_words`/`raw_changes`.
The task176 `COORDINATES` ledger records the ten typed coordinates, including
the E3 entries 0–4 and E4 entries 5–9.  These are finite E3/E4 context rows,
not cyclic deck levels.

### 1.3 PB3/PB4 boundary columns

The authenticated task175 producer constructs:

- PB3 from `old.pure_relations(3)` and
  `old.fox_gradient_without_sections(relator,e3)[0]`; it requires two rows,
  value identity, and `old.d1(row,e3)=={}`.  The bridge fields are
  `pb3.count=2`, `d1_zero`, `all_value_identity`, `exact_by="v121"`,
  `rows`, `row_digests`, and `relator_value_blobs`.
- PB4 from the pinned
  `search/d972_b345_target6_dual_colgen_v2.py:base_raw_columns(old,e4)`;
  it requires eleven rows, value identity, and zero D1.  The corresponding
  bridge fields are `pb4.count=11`, `d1_zero`, `all_value_identity`,
  `exact_by="v108"`, `rows`, `row_digests`, and `relator_value_blobs`.

In task179 (`:1094-1176`), `boundary_source` selects bridge PB3 rows for
blocks 1/2 and bridge PB4 rows for block 3.  `translated_boundary` unpacks a
typed translation blob, left-multiplies every source value, and emits a key
containing `(block, component, exact element blob)`.  `boundary_oracle`
reconstructs `t=g*h^-1`, checks `t*h=g`, accumulates every support/occurrence
contribution, and stores `block`, `base_relator_index`, `translation_hex`,
`scalar`, and `contributing_pairs`.  Identity translations seed the initial
basis; only rank-increasing columns are retained.  `boundary_chains` remain
separate from `selected_corrections` in both v1 and v2 receipts.

The helper checker independently rebuilds these rows from its own PB3/PB4
objects (`boundary_row`, `replay_columns`) and checks typed translation and
all contributor pairs.  Thus these fields authenticate finite typed boundary
replay, but not a cyclic group-ring boundary span.

## 2. Corollary 3.2 item-by-item inventory

The v164 Corollary 3.2 requirements were compared literally with the current
code/receipt fields.  “Present” below means that the finite object is named
and checked by the current implementation; it does not mean that the cyclic
requirement is satisfied.

| v164 item | current code/receipt evidence | missing for the stated cyclic requirement |
|---|---|---|
| 1. One compatible deck character and marked generator maps | `q3.coarse_models.Q0.marked_permutations`; task175 `context_contract.maps`; task175 `contexts.map_replay`; task176 `COORDINATES`/`coordinate_marks`; E4→E3 `coarse_marked_images` and `fine` marked PC images | No `chi:pi_1(X)->Z_p`, no `p`, `tau_a`, `tau_(a+1)->tau_a`, finite-surjectivity checks, compatible cell lifts, or deck action on a cyclic cover. The normalized exponent contract is an E1/E2 residue convention, not a deck character. |
| 2. One finite ordered source/target cell-orbit roster | `relation_roster` has the lossless 6441 words in layers `gamma_edge=6318`, `xy_action=104`, `q0_relator=19`; `COORDINATES` has ten typed rows; Q0 `canonical_roster`, parent/letter tables, and Gamma section parent/record tables are serialized; PB3/PB4 counts are 2/11 | No ordered source/target cell-orbit roster indexed compatibly at cyclic levels `a`; no orbit identifications or cell-lift transport under a common cyclic deck generator. The 6441 and Q0/Gamma inventories are finite quotient data. |
| 3. One ordered Fox template for H1, H2, all printed pentagon slots, and boundaries | `AllSevenModel.specs`/`occurrence_data`/`occurrence_column`/`direct_column`; bridge `all_seven_contract`, `literal_words`, `raw_changes`, `raw_base_targets`, `fox_replay`; task175 PB3/PB4 row fields and proof labels v121/v108; task186 `normalized_columns` and exact direct replay | No single `R_a`/`Lambda`-valued template with fixed source/target cell lifts, ring coefficients, or a level-independent column identifier. The current template is an E3/E4 finite typed template only. |
| 4. Direct confirmation that all translated columns are exactly the translates of fixed base columns | task175 `fox_replay`: 110 direct/predicted pairs, all 11 slots, 10 per slot, all three roster layers; task179 direct-vs-occurrence equality for every retained correction; boundary `t*h=g` accumulation; task176 complete Q0 shortlex section and task179 lazy Q0×Gamma candidates | No exhaustive cyclic deck-translate roster at any `R_a`; no `R_a`-linear base-column map; no direct comparison of the full cyclic translate image with generated columns. `full_orbit=false`, `direct_Delta_enumeration=false`, and coarse inverse tables are explicitly finite/lazy controls, not cyclic completeness. |
| 5. One literal target whose finite targets are reductions | `g760` length/word/SHA; bridge `raw_base_targets.H1/H2/P`, `raw_values`, `corrected_word`; task179 `exact_target` and target source string; conditional task186 `exactification.literal`, `exact_direct_replay`, and `right_g760_multiplication` | No family `z_a`, no maps `z_(a+1)->z_a`, no level-indexed target rows or reduction equalities, and no completed target in the cyclic module. One finite raw target is not a cyclic target family. |

The finite objects above are quotient/extension objects: Q0 has
`1,469,664` section states, Gamma has `243` states, and the lazy product
order is `357,128,352`.  They should not be relabeled as compatible cyclic
deck covers.  In particular, equality of dimensions or equal typed row
counts supplies none of the missing `chi`, ring transition, cell-lift, or
level-indexed target data.

## 3. Existing maps and the cyclic-level gap

The following maps are genuinely materialized in the dependency cone, with
their actual symbols and receipt locations:

| path | symbols/schema | what it maps | classification |
|---|---|---|---|
| `search/d972_r07_all_seven_raw_bridge_preflight_v1.py:307-424` | `fine_deletion_bfs`, `coarse_deletion_map`, `d_element`, `retract_map_replay`; nested in `d972-r07-all-seven-raw-bridge-preflight/v1.contexts.map_replay` | A marked PC map with domain order 59049 and image order 81; the fourth P/G9 block restriction; typed E4 element to E3 element; insertion `[1],[2],[4]` and deletion `[1],[2],[],[3],[],[]` | Finite E4→E3 context/quotient retraction, not a cyclic level map |
| `search/d972_r07_all_seven_extension_section_census_v1.py:428-470,672-719` | `build_fine_deletion`, `make_deleter`; receipt `d972-r07-all-seven-extension-section-census/v1.deletion` | Same fine PC reconstruction and coarse fourth-factor deletion, with marked-image diagnostics and typed element conversion | Finite quotient map; the receipt’s `extension` is `1->Gamma->G->Q0->1`, not `R_(a+1)->R_a` |
| `search/d972_r07_all_seven_extension_section_census_v1.py:716-824` | `projection`, `enumerate_q0_sections`, `q0_section_word`; receipt `Q0_section` parent/letter/canonical roster | Gamma states project to ten typed coordinates; Q0 parent/letter BFS reconstructs each finite section word and ten coordinate values | Finite section/coordinate map; not a cyclic deck transition |
| `search/d972_r07_positive_common_word_colgen_v1.py:912-1091` | `FibreOracle.canonical`, `ensure_kernel_prefix`, `verify_kernel_orders`, `global_candidate` | Lazy singleton fibres, finite Q0 section plus Gamma state candidates, and kernel-prefix words in the ten finite coordinates | Finite quotient candidate enumeration; no cyclic-level schema |
| `search/d972_r07_normalized_exact_common_word_colgen_v2.py:700-825` | `rank_zero_resume_checkpoint` | Converts an authenticated finite checkpoint by replaying columns from rank zero and discarding stale pivot/oracle state | Checkpoint-state conversion, not a group or cyclic-level map |

The cyclic papers themselves specify the desired symbols: v164
`Gamma_(a+1) -> Gamma_a`, `R_a`, and `T=tau-1` (Sections 1–3), and v133
`Lambda_(a+1)->Lambda_a` and the target/module squares (Section 1).  Within
the requested task179/task186 dependency cone there is no receipt object or
source routine carrying those symbols, a `chi` value, a pair of cyclic
levels, or a `T`-reduction row map.  The materialized E4/E3 maps above must
therefore not be treated as cyclic transitions.

## 4. Smallest receipt extension proposal (not implemented)

The smallest executable audit surface is one additional authenticated object
in both producer and helper-checker receipts, rather than duplicating the
eleven-slot implementation:

```json
"cyclic_fox_template": {
  "schema": "d972-r07-cyclic-fox-template/v1",
  "character": {
    "prime": 3,
    "chi_source": "fixed presentation generator images",
    "generator_images": "ordered signed integers",
    "finite_surjective_reductions": "CHECKER_RESULT"
  },
  "ring": {
    "parameter": "T=tau-1",
    "levels": [{"a": "...", "modulus": "T^(3^a)"}],
    "transition": "tau_(a+1)->tau_a; T->T"
  },
  "ordered_cell_orbits": {"source": [], "target": [], "typed": "CHECKER_RESULT"},
  "template": {
    "H1": [], "H2": [], "A18_printed": [], "PB3": [], "PB4": [],
    "order": "fixed; block/component/sign/lift/source-word included"
  },
  "translate_audit": [{
    "level": "...", "base_column_digests": [],
    "full_translate_count": "...", "full_translate_digest": "...",
    "direct_equals_template": "CHECKER_RESULT", "complete": "CHECKER_RESULT"
  }],
  "target_reductions": [{
    "level": "...", "literal_word": [], "target": [],
    "reduction_from_next_level": "..."
  }],
  "square_replay": {
    "fox_reduction_rows": [], "column_reduction_rows": [],
    "target_reduction_rows": [], "no_new_orbits": "CHECKER_RESULT"
  }
}
```

For a bounded finite audit, `full_translate_digest` may be a canonical
byte-stream digest of checker-regenerated typed rows, provided the receipt
also records the base-column IDs, translate count, ordering convention, and
the exact preimage contract.  It must not be only a dimension or row-count
digest.  The producer would populate the object from one fixed character,
cell-orbit list, and the already traced H1/H2/A.18/PB3/PB4 template.  The
checker would independently rebuild each listed level and require:

- the ring/character and marked-generator transition fields to agree;
- every source/target orbit and slot to retain the same typed order;
- every generated translated row to equal the direct Fox row, with complete
  count and digest;
- the reduction square to commute for each recorded column and target; and
- no unregistered level-dependent section or boundary column to enter the
  transcript.

This is a proposal only.  The current task179/task186 producer and checker do
not emit or validate this object, so the v164 finite template gate remains
unperformed in the present dependency cone.

## 5. Final audit boundary

Current task179/task186 data provide a detailed, independently replayable
finite E3/E4 Fox and boundary inventory.  They do not provide the cyclic
character, cyclic ring transitions, compatible cell-orbit roster,
level-indexed target reductions, or all-level translated-column comparison
required by v164 Corollary 3.2.  Parent Sol retains the mathematical
decision and any future implementation/GHA work.

`LUNA_TASK_189_STATIC_INVENTORY_COMPLETE`
