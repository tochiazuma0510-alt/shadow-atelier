/-
LeanArith/BridgeBAffine.lean ? Bridge B affine route, foundation spike A0.

This file only fixes the affine base, the variance of the finite-etale cover
category, the geometric fiber functor, and the resulting automorphism-group
candidate.  It does not assert the PreGalois/FiberFunctor obligations, a
tangential base point, freeness, inertia identifications, or exactness.
-/

import Mathlib.Algebra.Polynomial.Basic
import Mathlib.RingTheory.Localization.Away.Basic
import Mathlib.RingTheory.Etale.Finite
import Mathlib.CategoryTheory.Galois.Basic
import Mathlib.CategoryTheory.Galois.Topology

open CategoryTheory

namespace LeanArith.BridgeBAffine

universe u v w

noncomputable section

variable (k : Type u) [Field k]

/-- The polynomial whose principal open is `P? \\ {0,1,?}`. -/
def puncturePolynomial : Polynomial k :=
  Polynomial.X * (Polynomial.X - 1)

/-- The affine coordinate ring
`A_U = k[t,t??,(t-1)??]`, presented as localization away from `t(t-1)`. -/
abbrev AU : Type u :=
  Localization.Away (puncturePolynomial k)

/-- Finite ?tale affine covers have the opposite variance. -/
abbrev CoverCategory :=
  (CommAlgCat.FiniteEtale.{v} (AU k))??

variable (? : Type w) [Field ?] [IsSepClosed ?] [Algebra (AU k) ?]

/-- The ring map underlying the explicitly supplied geometric point. -/
def geometricPoint : AU k ?+* ? :=
  algebraMap (AU k) ?

/-- The finite-set-valued geometric fiber functor at `Spec ? ? U`. -/
def fiber :
    CoverCategory.{u, v} k ? FintypeCat.{max v w} :=
  CommAlgCat.FiniteEtale.fiber.{v} (AU k) ?

/-- Affine fundamental-group candidate at the supplied geometric point.
No topology or Galois-category theorem is claimed by this abbreviation. -/
abbrev PiOneCandidate :=
  CategoryTheory.Aut (fiber (k := k) ?)

/-- A0 obligation type: the finite-etale cover category is PreGalois.
This is a goal type, not an instance and not a theorem. -/
abbrev PreGaloisGoal : Prop :=
  CategoryTheory.PreGaloisCategory (CoverCategory.{u, v} k)

/-- A0 obligation type after a caller supplies the preceding PreGalois structure.
The declaration manufactures no instance; its instance parameter is an explicit
unproved input to the next bridge stage. -/
abbrev FiberFunctorGoal
    [CategoryTheory.PreGaloisCategory (CoverCategory.{u, v} k)] :=
  CategoryTheory.PreGaloisCategory.FiberFunctor
    (fiber (k := k) ?)

end
end LeanArith.BridgeBAffine
