# Luna task 188 — actual R07 PSL root-propagation inventory

Date: 2026-08-27

## Inventory verdict

**Terminal: `NO_SERIALIZED_ACTUAL_R07_PSL_STRIP_ROSTER`**

The first required machine datum is still
`ACTUAL_ISOLATED_B4_PSL_STRIP_OCCURRENCE_ROSTER_V1`.  No existing file
materializes an actual typed R07 occurrence multigraph with
`V = PSL(2,8)^u`, `N = PSL(2,8)^t`, factor maps, and the ordered
theta/tau/A18 rows.  This agrees with the earlier census terminal and its
field-by-field absence report (`sol/luna_reply_162_psl_strip_roster_census_v1.md:6,72-83`),
and with the cycle audit (`sol/luna_reply_162_psl_cycle_roster_v1.md:21-29,102-112`).

The actual-roster count is therefore zero *as a serialized datum*, not a
mathematical assertion that the R07 roster is empty.  Empty, forest,
simple-cycle, and higher-core counts remain `UNKNOWN`.

## Candidate inventory and classification

| Existing item | Classification | Actual typed R07 PSL strip roster? | v166 Section 5 data retained |
|---|---|---:|---|
| `search/week3-psl-common.g`, `search/week3-psl-S1.g` through `search/week3-psl-S7.g` | PSL/PGL seven-window arithmetic fixture/runner; S4 is a one-window `PSL(2,8)` marking | No | None of the occurrence, peel, or global-detector fields |
| `crosscheck/check-psl.mjs` | Independent matrix/permutation implementation for the PSL/PGL window certificates | No | Group-window checks only; no B4 incidence graph |
| `search/pgl28_independent_window_producer_v1.py` plus `search/certs/pgl28_independent_window_receipt_v1_20260823.json` and `crosscheck/verdicts/pgl28_independent_window_v1_20260823.json` | PGL/PGammaL(2,8) finite-field/group model and its target/component rosters | No | Its scope explicitly excludes B4; no strip occurrence, v52 peel, or R07 detector.  The producer records this scope at `search/pgl28_independent_window_producer_v1.py:495-500`; the receipt is `PASS_PRODUCER_ONLY`, not a cross-checked strip receipt. |
| `search/d972_b4_typed_bundle_v2.g` | Partial typed B4 6/158 producer with a PSL(2,8) source-definition hook | No | Deliberately `UNKNOWN_TYPED_BUNDLE`; `b4_s4_core` is `MISSING` and no B4/S4 core or reduction fibres are supplied (`search/d972_b4_typed_bundle_v2.g:529,534-545,594-602`). |
| `search/certs/d972_b4_a18_finite_dtilde_rows_fixture_v1_20260817.json` | Large synthetic A18/d-tilde word-row fixture | No | Rows/words only; no PSL factor coordinates, occurrence automorphisms, peel record, or onto table |
| `search/certs/d972_phase2b_nonsplit_v1_20260813.json` | L2(8) nonsplit/normal-kernel receipt | No | Its normal kernel is order 64 (`2^6`), not a `PSL(2,8)^u -> PSL(2,8)^t` strip incidence system |
| `search/certs/split_affine_1661_receipt_v2_20260823.json` and its independent verdict | Split affine `2^6 : PSL(2,8)` family | No | Wrong chief/kernel object and no B4 occurrence graph; marked generation gate is stopped |
| `crosscheck/d972_row36_bridge_baseline_v1_20260824.json` | Generic theta/tau/A18 common-word contract and row-36 baseline | No | Quotient/target factor maps and PSL-strip labels are absent |
| `certificates/S4.v2.json` and `crosscheck/verdicts/S4.psl.verdict.json` | Fixed `PSL(2,8)` group/arithmetic certificate and independent group verdict | No | Provides the 504-element arithmetic model only; no B4 edge, ordered occurrence list, peel, or detector |
| `ci/b345_157dp_artifacts_32171982444/d972_b4_fc8_a5four_v1.json` and `ci/b345_157dp_artifacts_32171982444/d972_b34_a5_selected_lift_v1.json` | Concrete B4 assets for `A5^4` | No | Actual B4 objects, but simple type is A5, not PSL(2,8), and no PSL strip multigraph |
| `search/d972_b4_typed_promotion_schema_v1.json`, `search/d972_b4_typed_promotion_hardening_manifest_v1.json`, `search/manifest_spec_v2_psl.md` | Abstract schemas/specifications and fixtures | No | Schema/spec text is not an instance and contains no authenticated R07 roster |
| `sol/luna_reply_162_psl_strip_roster_census_v1.md`, `sol/luna_reply_162_psl_cycle_roster_v1.md`, and proofs v48/v52/v77/v166 | Audit reports and paper-level contracts | No | They explicitly record the missing actual roster; v77's serialized boundary says no actual occurrence/core/detector receipt (`sol/proof_r07_return_midpoint_psl_cycle_onto_v77.md:729-754`). |

Thus no actual roster qualifies for a positive v166 field audit.  In
particular, there is no existing actual instance for which ordered rows,
repeated/parallel edges, signs, inner conjugators/field automorphisms, a
canonical v52 peel, and a global onto detector can be marked present.

## Structural counts available without execution

The only fixed group datum is `|PSL(2,8)| = 504`.  For the missing actual
roster the following are all **`UNKNOWN`**, not zero:

| Quantity | Readable value |
|---|---:|
| factor variables / `u,t` | `UNKNOWN` |
| ordered constraints/occurrences | `UNKNOWN` |
| non-isolated v52 core variables `u_core` | `UNKNOWN` |
| v52 unpivoted isolated variables `f` | `UNKNOWN` |
| v52 core topology/class counts | `UNKNOWN` |
| minimum greedy propagating-root size `r_prop` | `UNKNOWN` |

The v166 theorem gives only the symbolic bounds: the semantic fallback
`R = V` gives `r_prop <= |V|`, relation replay tests at most
`504^r_prop` root tuples, and a split global detector can require up to
`504^(r_prop+f)` `(r,s)` pairs.  No numerical upper bound can be computed
until the actual producer emits `V`, the ordered occurrence list, and the
v52-derived `u_core,f`.  The fallback is a bound, not an asserted roster
size or topology (`sol/proof_r07_psl_strip_rooted_peeling_v166.md:78-95,180-198`).

## Smallest mechanical producer/checker delta (proposal only)

1. Add one versioned producer input/output pair whose first input is the
   exact pinned `ACTUAL_ISOLATED_B4_PSL_STRIP_OCCURRENCE_ROSTER_V1`.  The
   producer must emit the complete ordered multigraph: edge/window and
   factor-coordinate pins; every theta/tau/A18 occurrence with distinct
   occurrence id, constraint index, printed position, source/target,
   sign, inner conjugator, field exponent, and fixed defect.  Duplicate and
   parallel rows must remain distinct.
2. In the same producer pass, derive and serialize the canonical least-leaf
   v52 peel and direct replay, then the chosen lexicographically canonical
   propagating root set, pivot order, residual list, propagated values, and
   direct equation results.  Include either complete root coverage or a
   disjoint shard manifest, plus the analogous coverage for every required
   isolated tuple when the global detector depends on it.
3. Serialize global onto-detector values on the same fully reconstructed
   assignments, never componentwise substitutes.  Emit exact structural
   counts and a fail-closed `UNKNOWN_RESOURCE`/missing-input result when the
   roster or any required derivative is absent; an empty core must not be
   manufactured from absent input.
4. Add a separate checker that binds the exact producer receipt/source bytes,
   independently reconstructs PSL(2,8) operations from the fixed group
   certificate, reconstructs the occurrence multigraph, and replays v52 and
   v166 literally.  It must check duplicate/order preservation, signs and
   automorphism labels, root-pivot legality, residual equations, coverage,
   and the global detector.  It must not import the producer/helper or turn
   a missing shard, detector, or source roster into a negative result.

These are the minimum mechanical fields demanded by v166 Section 5
(`sol/proof_r07_psl_strip_rooted_peeling_v166.md:220-241`).  This inventory
implements none of them and makes no nonemptiness, lift, fake, or Ihara
claim.

`R07_PSL_ROOT_PROPAGATION_INVENTORY_NO_ACTUAL_ROSTER__FIRST_MISSING_DATUM_RECORDED`
