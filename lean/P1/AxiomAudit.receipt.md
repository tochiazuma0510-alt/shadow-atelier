# P1 axiom-audit local receipt, bundle 106

- Toolchain: `leanprover/lean4:v4.32.1`.
- Command: `lake build P1` from `lean/` (targeted library build; not bare `lake build`).
- Exit code: 0.
- Checker terminal row: `P1_AXIOM_AUDIT_PASS|modules=8|theorems=242|manifest=P1/AXIOMS.manifest.json`.
- Exact allowed union: `{propext, Quot.sound, Classical.choice}`.
- Unexpected axiom count: 0.
- `sorryAx` dependency count: 0.
- Audited P1 source modules: 8 (the checker compares every flat `P1/*.lean`, except itself while
  elaborating, with the imported module set; this includes `P1.ShadowAxioms`).
- P1-owned axiom declarations: 0, including unused declarations.
- Quarantined bare-T2 declaration count in the audited environment: 0.
- Manifest schema: `p1-axiom-manifest/v2`.
- Type normalization/digest: `Expr.consumeMData` then `Expr.hash`; Lean-version-specific.

Main theorem receipt (the generated manifest is the complete 242-row receipt):

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
