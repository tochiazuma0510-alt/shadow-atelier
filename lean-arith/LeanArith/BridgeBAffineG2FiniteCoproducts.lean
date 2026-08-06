/-
Bridge B, affine route: the G2a finite-coproduct obligation.

This file is deliberately restricted to the canonical same-universe category
`CoverCategory.{u, u} k`.  It constructs finite products of finite etale
algebras explicitly and obtains finite coproducts of affine covers by passage
to the opposite category.  No other `PreGaloisCategory` field or
`FiberFunctor` field is asserted here.
-/

import LeanArith.BridgeBAffineG1
import Mathlib.CategoryTheory.Limits.Shapes.Opposites.Products
import Mathlib.RingTheory.Etale.Pi

open CategoryTheory Limits

namespace LeanArith.BridgeBAffine

universe u

noncomputable section

variable (k : Type u) [Field k]

private noncomputable def finiteEtalePiFan
    (R : Type u) [CommRing R]
    {J : Type} [Finite J]
    (F : J ? CommAlgCat.FiniteEtale.{u} R) : Fan F :=
  Fan.mk
    (CommAlgCat.FiniteEtale.of R ((j : J) ? F j))
    (fun j ? ObjectProperty.homMk
      (CommAlgCat.ofHom (Pi.evalAlgHom R (fun i ? F i) j)))

private noncomputable def finiteEtalePiFanIsLimit
    (R : Type u) [CommRing R]
    {J : Type} [Finite J]
    (F : J ? CommAlgCat.FiniteEtale.{u} R) :
    IsLimit (finiteEtalePiFan R F) :=
  Fan.IsLimit.mk _
    (fun s ? ObjectProperty.homMk <| CommAlgCat.ofHom <|
      AlgHom.pi fun j ? (s.proj j).hom.hom)
    (fun _ _ ? rfl)
    (fun s m h ? by
      apply ObjectProperty.hom_ext
      apply CommAlgCat.hom_ext
      apply AlgHom.ext
      intro x
      funext j
      exact congrArg (fun q ? q.hom.hom x) (h j))

private noncomputable instance finiteEtaleHasProduct
    (R : Type u) [CommRing R]
    {J : Type} [Finite J]
    (F : J ? CommAlgCat.FiniteEtale.{u} R) : HasProduct F :=
  HasLimit.mk
    { cone := finiteEtalePiFan R F
      isLimit := finiteEtalePiFanIsLimit R F }

private noncomputable instance finiteEtaleHasFiniteProducts
    (R : Type u) [CommRing R] :
    HasFiniteProducts (CommAlgCat.FiniteEtale.{u} R) :=
  ?fun _ ? ?fun K ? by
    let e : Discrete.functor (fun n ? K.obj ?n?) ? K :=
      Discrete.natIso fun _ ? Iso.refl _
    rw [? hasLimit_iff_of_iso e]
    infer_instance??

/-- The canonical same-universe category of finite etale affine covers has
finite coproducts.  These are dual to the explicit finite products of finite
etale algebras constructed above. -/
noncomputable instance coverCategoryHasFiniteCoproducts :
    HasFiniteCoproducts (CoverCategory.{u, u} k) := by
  infer_instance

/-- The G2a obligation, exposed as the actual Mathlib typeclass rather than a
theorem-shaped proxy. -/
theorem coverCategoryHasFiniteCoproductsWitness :
    HasFiniteCoproducts (CoverCategory.{u, u} k) := by
  infer_instance

#print axioms coverCategoryHasFiniteCoproducts
#print axioms coverCategoryHasFiniteCoproductsWitness

end
end LeanArith.BridgeBAffine
