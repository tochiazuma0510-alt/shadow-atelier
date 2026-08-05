# P1 axiom-audit local receipt, bundle 108d integration candidate

- Toolchain: `leanprover/lean4:v4.32.1`.
- Commands: `lake env lean P1/AxiomCheck.lean` (manifest regeneration) and
  `lake build P1` from `lean/`.
- Exit code: 0.
- Checker terminal row: `P1_AXIOM_AUDIT_PASS|modules=12|theorems=447|manifest=P1/AXIOMS.manifest.json`.
- Exact allowed union: `{propext, Classical.choice, Quot.sound}`.
- Unexpected axiom count: 0.
- `sorryAx` dependency count: 0.
- Audited P1 source modules: 12 (the checker compares every flat `P1/*.lean`, except itself while
  elaborating, with the imported module set; this includes `P1.ShadowAxioms`).
- P1-owned axiom declarations: 0, including unused declarations.
- Quarantined bare-T2 declaration count in the audited environment: 0.
- Manifest schema: `p1-axiom-manifest/v2`.
- Type normalization/digest: `Expr.consumeMData` then `Expr.hash`; Lean-version-specific.

Integrated module theorem counts:

| Module | Theorem rows |
|---|---:|
| `P1.BlockA_LA2` | 70 |
| `P1.BlockA_LA3` | 28 |
| `P1.BlockA_LA45` | 106 |
| `P1.BlockA_LAIntegration` | 1 |

Main theorem receipt (the generated manifest is the complete 447-row receipt):

| Declaration | Normalized type digest | Exact sorted axiom set |
|---|---:|---|
| `Gn_groupLaws` | `319693831` | `[propext, Quot.sound]` |
| `X_mem_Gn` | `1023398869` | `[]` |
| `Gn_ord_X` | `1089410374` | `[propext, Quot.sound]` |
| `Gn_card_formula` | `3871934708` | `[propext]` |
| `window.encode_injective` | `2555354813` | `[propext]` |
| `window.isSubgroup` | `3451274123` | `[propext, Quot.sound]` |
| `window.carrier_card_formula` | `4052195346` | `[propext]` |
| `window.Index2nWitness.isSubgroup` | `606695864` | `[]` |
| `window.join_split` | `495756063` | `[propext, Quot.sound]` |
| `window.split_join` | `3346231241` | `[propext, Quot.sound]` |
| `window.genX_iff_exists_xrep` | `1524082758` | `[propext, Classical.choice, Quot.sound]` |
| `window.cyclicTransitive_iff_leftCosetAction` | `2905952487` | `[propext, Quot.sound]` |
| `window.transitive_iff_trivial_inter` | `1860445659` | `[propext, Classical.choice, Quot.sound]` |
| `window.familyTransitive` | `3482546224` | `[propext, Quot.sound]` |
| `window.familyTrivialInter` | `3526898877` | `[propext]` |
| `window.H_parameter_injective` | `1636589174` | `[propext]` |
| `window.isSubgroup_P1_P3_coded` | `1540784104` | `[propext, Classical.choice, Quot.sound]` |
| `window.isSubgroup_P1_P3` | `2489053314` | `[propext, Classical.choice, Quot.sound]` |
| `window.conjugate_by_rotation` | `1828830783` | `[propext, Quot.sound]` |
| `window.conjugate_by_q1` | `3735246130` | `[propext, Quot.sound]` |
| `window.conjugate_parameters` | `2026876948` | `[propext, Quot.sound]` |
| `window.normalizer_eq_H_iff` | `2669991020` | `[propext, Quot.sound]` |
| `window.conjugate_H_iff` | `1188838946` | `[propext, Classical.choice, Quot.sound]` |
| `INN_on_Y` | `1738687873` | `[propext, Quot.sound]` |
| `inn_fixes_X` | `2719432479` | `[propext, Quot.sound]` |
| `chiTilde_welldefined` | `2768022581` | `[propext, Quot.sound]` |
| `chiTilde_isUnit` | `1292103626` | `[propext, Quot.sound]` |
| `chiTilde_composition_identity` | `1236643069` | `[propext]` |
| `torsor_compare_unit` | `3582073373` | `[propext, Classical.choice, Quot.sound]` |
| `fin_cyclic_automorphism_unit` | `955062159` | `[propext, Quot.sound]` |
| `torsor_compare_fin_unit` | `2966220890` | `[propext, Classical.choice, Quot.sound]` |

Warnings were linter-only (`unusedSimpArgs` / `unusedSectionVars`) in pre-existing and expanded
plain-core arithmetic. There was no compiler “declaration uses `sorry`” warning. This receipt is a
local candidate; GHA remains the authoritative acceptance run.
