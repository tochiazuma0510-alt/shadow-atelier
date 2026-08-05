# Luna 108d follow-up: Bridge B / G1

## Result

PASS for the canonical same-universe affine cover category:

- `HasTerminal (CoverCategory.{u, u} k)` is now an actual public instance.
- `HasPullbacks (CoverCategory.{u, u} k)` is now an actual public instance.
- `coverCategoryG1 : G1Goal.{u, u} k` packages exactly these two fields of
  `CategoryTheory.PreGaloisCategory` and nothing beyond them.

The independent-universe A0 target is retained verbatim as the unproved type
`G1Goal.{u, v} k`.  No theorem or instance for arbitrary independent `u, v` is
claimed.

## Isolated lane

- lane: `C:\Users\81905\AppData\Local\Temp\shadow-atelier-bridge-g1-4a9f0a0723de46cebdc116fba3855535`
- baseline commit: `82ff1047b80a50b8a3098a83d71424ed2c6ec26d`
- baseline tree: `901b51ce6887df06441c335b04b2e87afb413c72`
- read-only source used for the physical-copy/check-out fallback:
  `C:\Users\81905\AppData\Local\Temp\shadow-atelier-luna106g-b0b23ce9e00145629c7479f5576be1ea`
- build output (outside every repository):
  `C:\Users\81905\AppData\Local\Temp\bridge-g1-build-6b6a4b10c3664d1eb4df42d33060db16`

Owned files only:

1. `lean-arith/LeanArith/BridgeBAffineG1.lean`
2. `sol/luna_reply_108d_bridge_g1.md`

The Lean file SHA-256 before this report was written is
`8650244F41E03DCB0615A8A7CA58DBFAFE49D669868D22E6DAB0340900D17168`.

## Mathematical/API correspondence

The fixed mathlib definition has G1 fields `hasTerminal : HasTerminal C` and
`hasPullbacks : HasPullbacks C`.  The implementation follows those exact
types.

For the terminal object, the opposite category receives a terminal object from
the initial finite-etale algebra `R`.  Initiality is proved directly from the
unique structure map `R -> A`.

For pullbacks, the proof constructs pushouts before taking opposites.  Given
finite-etale `R`-algebras and maps `X -> Y`, `X -> Z`, the pushout is
`Y tensor[X] Z`.  The closure proof uses the fixed APIs
`Module.Finite.of_restrictScalars_finite`,
`Algebra.Etale.of_restrictScalars`, tensor-product base change,
`Module.Finite.trans`, and `Algebra.Etale.comp`.  Its universal property is
proved with `Algebra.TensorProduct.lift` and
`PushoutCocone.isColimitAux'`.  This yields `HasPushouts` for
`CommAlgCat.FiniteEtale.{u} R`, hence `HasPullbacks` for its opposite.

## Minimal universe blocker outside the proved target

A0 permits `CoverCategory.{u, v}` with independent carrier universe `v`.
In fixed mathlib 4.32.1, `CommAlgCat.Basic` supplies (co)limits only for
`CommAlgCat.{u} R`; its source contains an explicit TODO to generalize this to
`UnivLE.{u, v}`.  The initial algebra `R` likewise cannot be placed in an
arbitrary unrelated `Type v` without a universe-smallness witness.  Therefore
the arbitrary-`v` obligation is recorded exactly as `G1Goal.{u, v}` while the
actual instances use the canonical `v = u` category.  I did not replace the
missing arbitrary-universe claim by a superficially weaker categorical fact.

## Checks

- Lean: `4.32.1` (`f054605aea4b840552cca2e725580bffd1e1b704`)
- mathlib: `520045ab14e26149ee970e2e617ca04b09bde5d6`
- targeted compile of `BridgeBAffineG1.lean`: PASS (`EXIT=0`)
- `#print axioms LeanArith.BridgeBAffine.coverCategoryG1`:
  only `propext`, `Classical.choice`, `Quot.sound`
- banned scan for `sorry`, `admit`, `axiom`, `True`, `native_decide`, and
  `ofReduce`: no hits
- trailing-whitespace scan: no hits

No dependency, A0, lake, workflow, manifest, or map file was changed.  No
credential was accessed, and no commit, push, or dispatch was performed.

## Deliberately still OPEN

No `PreGaloisCategory` instance is declared.  Finite coproducts,
finite-group quotients, the mono/direct-summand condition, `FiberFunctor`, the
tangential base point, TB3/TB4, and EXSEQ all remain OPEN.
