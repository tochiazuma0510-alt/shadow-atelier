/-
LeanArith/ShadowAxioms.lean -- explicit project-level mathematical axioms.

Declarations in this file are not Mathlib theorems. Each axiom is documented
with its source, scope, approval, and removal condition in `lean/AXIOMS.md`.
-/

import LeanArith.BridgeBAffine
import Mathlib.Algebra.Algebra.Subalgebra.Operations
import Mathlib.RingTheory.Noetherian.Basic

namespace ShadowAxioms

universe u

noncomputable section

/-- Content: the fixed subalgebra of a module-finite étale algebra under a
finite-group action is étale over the base.

Source (exact theorem): SGA 1, Exposé V, Proposition 3.1 (printed p. 96,
PDF p. 112), together with Proposition 1.1 and Corollaire 1.8 for the affine
quotient. Sol checked the PDF page images on 2026-08-06.

Conceptual formulation: this is the finite-group quotient property of FEt in
the Lenstra GTS-style formulation. “Lenstra GTS-style” names the formulation
only; the exact source claim and locators are the SGA 1 propositions above.

Tier: T1 (classical SGA 1). Addition authorized by commander ruling 610 and
commission 111d.

Mathlib status: absent in Mathlib v4.32.1 at commit
520045ab14e26149ee970e2e617ca04b09bde5d6. An axiom-free G2b-exact
replacement remains OPEN.

Scope: a noetherian base, a module-finite étale algebra, and a finite group
acting by semiring automorphisms compatibly with base scalars. -/
axiom fixedPointsSubalgebra_etale_of_finite
    (R B G : Type u)
    [CommRing R] [CommRing B] [Algebra R B] [IsNoetherianRing R]
    [Module.Finite R B] [Algebra.Etale R B]
    [Group G] [Finite G] [MulSemiringAction G B]
    [SMulCommClass G R B] :
    Algebra.Etale R (FixedPoints.subalgebra R B G)

open LeanArith.BridgeBAffine

/-- Binder-sanity witness: the project axiom specializes to the canonical
affine base `AU k`. This checks the declaration's type only; it is not an
independent proof of the mathematical assertion. -/
theorem fixedPointsSubalgebra_etale_AU_sanity
    (k B G : Type u) [Field k]
    [CommRing B] [Algebra (AU k) B]
    [Module.Finite (AU k) B] [Algebra.Etale (AU k) B]
    [Group G] [Finite G] [MulSemiringAction G B]
    [SMulCommClass G (AU k) B] :
    Algebra.Etale (AU k) (FixedPoints.subalgebra (AU k) B G) := by
  exact fixedPointsSubalgebra_etale_of_finite (AU k) B G

#print axioms fixedPointsSubalgebra_etale_AU_sanity

end
end ShadowAxioms
