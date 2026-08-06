# P1 axiom registry / checker contract v2

Status: local targeted-build candidate. The authoritative acceptance run is the later GHA gate.

`P1/AxiomCheck.lean` generates `P1/AXIOMS.manifest.json` while elaborating. It inventories every
theorem declaration owned by an imported `P1.*` module (including compiler-generated theorem
declarations), records its exact sorted axiom set, and records a declaration-type digest computed
as `Expr.consumeMData` followed by `Expr.hash`. Bound variables therefore remain in kernel
de-Bruijn form, while source metadata is erased. Digests are Lean-version-specific; the manifest
records `Lean.versionString`.

The checker is fail-closed on:

- an empty theorem inventory;
- any axiom outside `{propext, Quot.sound, Classical.choice}`;
- any axiom name containing `sorryAx`;
- any P1-owned axiom declaration, even if no inventoried theorem currently uses it;
- any unauthorized/sorry dependency of any P1-owned definition, not only theorem roots;
- reappearance of any of the four quarantined bare-T2 declaration names.

The allowed three are Lean-core logical axioms, not paper hypotheses. `Classical.choice` occurs in
the abstract TORS-U construction. There are no project/paper axioms in the accepted import graph.

## T2 quarantine

The former bare propositions

- `ShadowAxioms.T2_thm43_explicit_isolated`,
- `ShadowAxioms.T2_thm43_isolated`,
- `ShadowAxioms.T2_15_Ih_decomp`, and
- `ShadowAxioms.T2_composition_hom`

have been removed. `P1/ShadowAxioms.lean` is now a comment-only quarantine boundary. T2 code must
not be restored until Sol approves an exact source table giving theorem/page, every hypothesis,
domain, codomain, weakest conclusion, and a sanity instance.

## Placeholder hygiene

The two former `: True` declarations are absent. Block A now has an explicit equivalence
`Gn n <-> GnCode n` plus the arithmetic formula for `4*n^3`, and an exact `Lambda` type with an
exact `LambdaSimplyTransitive` proposition. The latter proof remains explicitly OPEN; no theorem
claiming it has been exported.

## Reproduction

From `lean/`:

```text
lake build +P1.AxiomCheck:olean
lake build P1
```

Both are targeted builds permitted by the task envelope. The first emits one `P1_AXIOM_ROW` per
theorem and a final `P1_AXIOM_AUDIT_PASS` line, and refreshes `P1/AXIOMS.manifest.json`.

## Bridge B G2b: finite-group fixed subalgebras (ruling 610 / commission 111d)

Status: authorized T1 project axiom. G2b may be accepted only as
**verified-modulo-axioms**; this entry does not weaken the axiom-free P1 checker
contract above.

### Declaration

Exact name:
ShadowAxioms.fixedPointsSubalgebra_etale_of_finite.

Normalized Lean type:

~~~lean
universe u

namespace ShadowAxioms

axiom fixedPointsSubalgebra_etale_of_finite
    (R B G : Type u)
    [CommRing R] [CommRing B] [Algebra R B] [IsNoetherianRing R]
    [Module.Finite R B] [Algebra.Etale R B]
    [Group G] [Finite G] [MulSemiringAction G B]
    [SMulCommClass G R B] :
    Algebra.Etale R (FixedPoints.subalgebra R B G)

end ShadowAxioms
~~~

Content and scope: over a noetherian base, the fixed subalgebra of a
module-finite étale algebra under a finite group acting by semiring
automorphisms compatibly with base scalars is étale. No cocone, universal
property, colimit, or module-finiteness conclusion is axiomatized.

Source tier: **T1** (classical SGA 1), authorized by commander ruling 610 and
commission 111d. Exact source locator: SGA 1, Exposé V, Proposition 3.1
(printed p. 96, PDF p. 112), together with Proposition 1.1 and Corollaire 1.8
for the affine quotient. Sol checked the PDF page images on 2026-08-06.
Conceptually, this is the finite-group quotient property of FEt in the Lenstra
GTS-style formulation. “Lenstra GTS-style” identifies the conceptual
formulation only; no additional bibliographic locator is claimed beyond the
page-checked SGA 1 propositions. Source PDF:
papers/sga1-grothendieck-raynaud-arxiv0206203.pdf, SHA-256
8e64218d356456c534eebf996940f0f957e43b54f1a080241debe12cbaf60d3c.

Mathlib status: absent from Mathlib tag v4.32.1, commit
520045ab14e26149ee970e2e617ca04b09bde5d6. The absence check was a source-tree
search for a theorem or instance combining FixedPoints.subalgebra with
Algebra.Etale; only the fixed-subalgebra definition and unrelated uses were
present.

Actual direct use-sites:

- LeanArith/ShadowAxioms.lean:
  ShadowAxioms.fixedPointsSubalgebra_etale_AU_sanity (binder-specialization
  sanity only, not an independent proof).
- LeanArith/BridgeBAffineG2FiniteGroupQuotients.lean: the local
  Algebra.Etale instance inside source-level helper
  finiteGroupQuotientColimitCocone. This is the only mathematical use.

The public declarations transitively depending on the axiom have these exact
sorted #print axioms sets:

- LeanArith.BridgeBAffine.coverCategoryHasQuotientsByFiniteGroups:
  {Classical.choice, Quot.sound,
  ShadowAxioms.fixedPointsSubalgebra_etale_of_finite, propext}.
- LeanArith.BridgeBAffine.coverCategoryFiniteGroupColimitWitness:
  {Classical.choice, Quot.sound,
  ShadowAxioms.fixedPointsSubalgebra_etale_of_finite, propext}.

The axiom-free replacement of G2b-exact is **OPEN**. Delete this axiom and this
registry section only when either Mathlib supplies a theorem/instance of the
same scoped type or an axiom-free in-project formalization supplies it, and
the G2b declarations still pass with no project axiom.

### Independent fiber-terminal field

LeanArith.BridgeBAffine.fiberPreservesTerminalObjects and
LeanArith.BridgeBAffine.fiberPreservesTerminalObjectsWitness do not depend on
this project axiom. Each has exact sorted axiom set
{Classical.choice, Quot.sound, propext}.
