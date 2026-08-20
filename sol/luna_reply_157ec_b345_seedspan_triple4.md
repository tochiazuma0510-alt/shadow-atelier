# 157ec — B345 seedspan triple4

Status: READY_FOR_GHA.  This bundle implements `sol/luna_task_157ec_b345_seedspan_triple4.md` (SHA256 `1173f2f8ce6ad899fe5bee6c2a42d7cb6686073306a7e3fd1e17acf0007f89b2`).  No GAP math run, GHA dispatch, Git operation, or full production scan was run locally.

## Registered universe

The producer and the independent checker each rebuild the fixed q3 correction fibre, require 27 records with record 1 empty and 26 distinct nonempty cubes, and bind

`digest_obj(cubes) = 3d26302d01b3c202350fdb8b9ea81badeaf9c62913c9e94be7e049ad7c391463`.

The old ordered 104 commutator seeds are retained verbatim.  Exactly four new words are appended, in this order:

| q3 record positions | nonempty cube positions | reduced length | SHA256 |
|---|---:|---:|---|
| (3,10,19) | (2,9,18) | 408 | d810d557ca1128924da9ab04f0f304dfbf4d60503db187dfde531085b43a124f |
| (10,10,11) | (9,9,10) | 816 | 0fb7a48541e413091779494e54d351e745569859e1d8ed68fe24301b8ae0f3b6 |
| (10,12,12) | (9,11,11) | 816 | 05fff82ae07daf70997f9164fbbd2a6a22d7340b277eb9203d4c890ae98bb44b |
| (19,19,21) | (18,18,20) | 408 | 8d68e311a631fdc8d94e9729a273aefb6ff25f5bab99c7b59e4c9488c0080e5c |

Each word is exactly `reduce(cube[a]+cube[b]+cube[c])`, ordinary left-to-right, with repeated indices literal.  The result is an ordered 108-variable universe: old104 followed by the four `positive_triple_cube` words.  The receipt records family, global index, source tuples, literal-repeat flag, reduced length/SHA, exponent sums, and E3 identity; the occurrence preflight independently records all 31 unique contexts and 46 named uses for every seed.  No all-triples, depth-3, minimality, or full-D2 claim is made.

## Affine and dual certificate

The target-major solver is over `F3^108`.  The 104-column identity-root shortcut is available only to the historical 104-column universe; in this bundle targets 1–5 also process the four appended columns through the direct/typed raw-Fox comparison.  Target 6 retains the direct formula/free-word orientation gate.  Every evaluated target/seed has direct-vs-typed equality before D2 remainder absorption.

The first inconsistent row is retained as a normalized dual.  Its public labels are `[target_ordinal,target_name,component,E4_blob_hex]`, with one-based component numbering `1..6`, literal canonical permutation-bytes-then-PC-bytes encoding, byte-string order (no integer reinterpretation), and component-then-exact-E4 pivot order.  The public encoding records the actual reconstructed E4 permutation width (`e4.degree`), PC width (`e4.pc.n`), their integer sum, and twice-that sum as the required hex length; every label is independently hex-decoded and width-checked.  The certificate records the ordered sparse coefficients, support count and SHA, target boundary, normalized RHS `1`, `yTz_mod3=2`, 108-dimensional annihilation digest, seed-manifest binding, live/peak provenance accounting, and support cap 128.  If the first contradiction is wholly in target 6, the public field `target6_fixed_prefix_functional=true` records that prefix-only fact.  The checker rebuilds the equations, verifies `y^T A=0` and `y^T b=1`, and rejects mutated support/digest/normalization/width/component data.  A consistent receipt has no dual; an inconsistent receipt is `SEARCH_INCOMPLETE`, never a negative/nonexistence claim.

Claim scope is exactly `registered_old104_plus_four_triple_cube_affine_span_against_fixed_D2_prefix`; the only positive scope, if reached, is one concrete correction in that registered subgroup.  The serialized `claim_boundary` explicitly sets `full_D2_claimed=false`, `full_H3_claimed=false`, `all_triple_products_claimed=false`, `all_depth3_claimed=false`, `negative_claimed=false`, `B4_A_claimed=false`, and `B4_B_claimed=false`.

## Independent gates

The checker independently rebuilds the manifest, seed provenance, context registry, target rows, row-space/rank/nullity, full remainder, typed/raw chains, and dual witness.  For targets 1--5, each target ledger is explicitly old104 identity-shortcut entries followed by four independently direct/typed-replayed triple-cube entries; it records `seed_count=108`, `typed_split_count=108`, `old_shortcut_count=104`, and `new_direct_count=4`.  The production checker also rejects injected `core_validation`, `input_errors`, or `partial` fields outside their terminal partitions.  The driver uses the fixed producer/checker paths, exact q3 pins, one of the four registered terminal tokens, and same-job checker execution.

The final bounded combined selftest passed after the schema, provenance-pin, and split-ledger repair:

`D972_B345_SEEDSPAN_TRIPLE4_PRODUCER_SELFTEST_PASS ... dual_witness=1 dual_support_cap=1 triple4_manifest=1 ...`

`D972_B345_SEEDSPAN_TRIPLE4_CHECKER_SELFTEST_PASS ... dual_witness=1 dual_support=1 ...`

The producer/checker were syntax-compiled before that bounded selftest.  The selftest includes the repeated-index manifest gate, target-6 selection/name/kind mutations, raw pair/inverse/square and nonzero-base split, 108-variable genuine support-two contradiction, dual digest mutation, full-remainder/later-pivot, terminal/claim, resource gt/ge, and rollback fixtures.  It additionally runs the production split-ledger/raw direct-vs-typed/target-row gates on a bounded 108-column fixture, rejects applying the old104 shortcut to a new column, and checks a consistent literal selected replay.  The production terminal envelope is now an exact terminal+reason+phase top-level keyset: early incomplete receipts cannot carry prefix/proof fields, nonpositive receipts cannot carry positive-only fields, and resource/input ledgers are restricted to their own terminals.  Performance, resource guards, affine-system, strong-canary, typed-candidate, positive-replay, and partial nested keysets are exact as well.  The authenticated receipt pins also include the exact 157eb producer/checker/driver paths and SHA256 values from task section A.

Post-selftest freeze STOP repair: the positive producer path now copies `positive_replay.diagnostics` to top level before the shared finalizer; producer and checker require equality, the positive reason/phase pair, resource phase equality, and the inconsistent-target ordinal phase.  UNKNOWN_INPUT accepts the authenticated `fresh_immutable_prefix` TOCTOU stage only when `mathematical_scan_started=true`; UNKNOWN_RESOURCE rejects every positive-only top-level field.  Bounded production-envelope canaries (success, resource, inconsistent, and fresh-prefix input, with mutations) were added to both selftests.

The first authorized corrective attempt exposed an empty strong-canary placeholder in the inconsistent fixture.  After the fixture-only repair, the final authorized combined selftest passed exactly once: producer and checker both emitted `...SELFTEST_PASS`, including `terminal_values=1 production_shapes=1`.  No further selftest was run.

## Frozen bundle

| file | bytes | SHA256 |
|---|---:|---|
| `search/d972_b345_seedspan_triple4_v1.py` | 535219 | fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29 |
| `search/check_d972_b345_seedspan_triple4_v1.py` | 574347 | ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981 |
| `search/d972_b345_seedspan_triple4_gha_driver_v1.g` | 9041 | a9c88540c1abdb21dc214d4d4e6461c1431dc407f93542c49e0e65a14788fca4 |

The driver pins the producer and checker hashes above.  This is a fresh 157ec bundle; it does not resume or import a 157eb affine scan.

Corrective freeze: the dual encoding now binds the reconstructed E4 widths (`permutation_width_bytes=e4.degree`, `pc_width_bytes=e4.pc.n`), uses one-based components `1..6`, and rejects zero/seven/odd/non-hex/width-drift labels.  Production schema partitions reject injected `core_validation`, require `input_errors` only for `UNKNOWN_INPUT`, and require `partial` only for `UNKNOWN_RESOURCE`.  Targets 1--5 use the exact old104 identity ledger followed by four direct/typed triple-cube replays, with lossless `seed_count=108`, `typed_split_count=108`, `old_shortcut_count=104`, and `new_direct_count=4` fields.  The final authorized combined selftest passed both producer and checker markers, including `schema_exact=1`, `pins_157eb=1`, `split_ledger=1`, `row_schema=1`, `selected_replay=1`, `wide108_support2=1`, and `terminal_values=1 production_shapes=1`.  The driver pins the current producer/checker hashes in the table above; no further selftest is authorized or required.

B345_SEEDSPAN_TRIPLE4_V1_READY_FOR_GHA
