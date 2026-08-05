/-
Bridge B, affine route: the G1 terminal-object and pullback obligations.

The finite-coproduct, finite-group-quotient, and mono/direct-summand parts of
PreGaloisCategory remain open.  This file also supplies no FiberFunctor,
tangential base point, TB3/TB4, or exact-sequence result.
-/

import LeanArith.BridgeBAffine
import Mathlib.Algebra.Category.CommAlgCat.Monoidal
import Mathlib.RingTheory.TensorProduct.Finite

open CategoryTheory Limits
open scoped TensorProduct

namespace LeanArith.BridgeBAffine

universe u v

noncomputable section

variable (k : Type u) [Field k]

/-- The exact G1 fragment of the A0 PreGalois obligation.  Keeping `v`
independent records the universe-polymorphic goal without asserting it. -/
abbrev G1Goal : Prop :=
  HasTerminal (CoverCategory.{u, v} k) ∧
    HasPullbacks (CoverCategory.{u, v} k)

private def finiteEtaleInitialSelf (R : Type u) [CommRing R] :
    IsInitial (CommAlgCat.FiniteEtale.of R R) :=
  IsInitial.ofUniqueHom
    (fun A => ObjectProperty.homMk (CommAlgCat.ofHom (Algebra.ofId R A)))
    (fun A f => by
      apply ObjectProperty.hom_ext
      apply CommAlgCat.hom_ext
      exact AlgHom.ext fun x => by simpa using f.hom.hom.commutes x)

private noncomputable instance finiteEtaleHasInitial (R : Type u) [CommRing R] :
    HasInitial (CommAlgCat.FiniteEtale.{u} R) :=
  (finiteEtaleInitialSelf R).hasInitial

noncomputable instance coverCategoryHasTerminal :
    HasTerminal (CoverCategory.{u, u} k) := by
  infer_instance

private noncomputable def finiteEtalePushoutCocone
    (R : Type u) [CommRing R]
    {X Y Z : CommAlgCat.FiniteEtale.{u} R}
    (f : X ⟶ Y) (g : X ⟶ Z) : PushoutCocone f g := by
  letI : Algebra X Y := f.hom.hom.toRingHom.toAlgebra
  letI : Algebra X Z := g.hom.hom.toRingHom.toAlgebra
  haveI : IsScalarTower R X Y :=
    IsScalarTower.of_algebraMap_eq' f.hom.hom.comp_algebraMap.symm
  haveI : IsScalarTower R X Z :=
    IsScalarTower.of_algebraMap_eq' g.hom.hom.comp_algebraMap.symm
  haveI : Module.Finite X Y := Module.Finite.of_restrictScalars_finite R X Y
  haveI : Module.Finite X Z := Module.Finite.of_restrictScalars_finite R X Z
  haveI : Algebra.Etale X Y := Algebra.Etale.of_restrictScalars R X Y
  haveI : Algebra.Etale X Z := Algebra.Etale.of_restrictScalars R X Z
  haveI : Module.Finite Y (Y ⊗[X] Z) := inferInstance
  haveI : Module.Finite R (Y ⊗[X] Z) := Module.Finite.trans Y (Y ⊗[X] Z)
  haveI : Algebra.Etale R (Y ⊗[X] Z) := Algebra.Etale.comp R Y (Y ⊗[X] Z)
  let P : CommAlgCat.FiniteEtale.{u} R :=
    CommAlgCat.FiniteEtale.of R (Y ⊗[X] Z)
  let inl : Y ⟶ P :=
    ObjectProperty.homMk (CommAlgCat.ofHom Algebra.TensorProduct.includeLeft)
  let inr : Z ⟶ P :=
    ObjectProperty.homMk
      (CommAlgCat.ofHom
        ((Algebra.TensorProduct.includeRight (R := X) (A := Y) (B := Z)).restrictScalars R))
  refine PushoutCocone.mk inl inr ?_
  apply ObjectProperty.hom_ext
  apply CommAlgCat.hom_ext
  exact AlgHom.ext fun x => by
    change algebraMap X Y x ⊗ₜ[X] 1 = 1 ⊗ₜ[X] algebraMap X Z x
    exact Algebra.TensorProduct.tmul_one_eq_one_tmul x

private noncomputable def finiteEtalePushoutCoconeIsColimit
    (R : Type u) [CommRing R]
    {X Y Z : CommAlgCat.FiniteEtale.{u} R}
    (f : X ⟶ Y) (g : X ⟶ Z) :
    IsColimit (finiteEtalePushoutCocone R f g) := by
  letI : Algebra X Y := f.hom.hom.toRingHom.toAlgebra
  letI : Algebra X Z := g.hom.hom.toRingHom.toAlgebra
  haveI : IsScalarTower R X Y :=
    IsScalarTower.of_algebraMap_eq' f.hom.hom.comp_algebraMap.symm
  haveI : IsScalarTower R X Z :=
    IsScalarTower.of_algebraMap_eq' g.hom.hom.comp_algebraMap.symm
  haveI : Module.Finite X Y := Module.Finite.of_restrictScalars_finite R X Y
  haveI : Module.Finite X Z := Module.Finite.of_restrictScalars_finite R X Z
  haveI : Algebra.Etale X Y := Algebra.Etale.of_restrictScalars R X Y
  haveI : Algebra.Etale X Z := Algebra.Etale.of_restrictScalars R X Z
  haveI : Module.Finite Y (Y ⊗[X] Z) := inferInstance
  haveI : Module.Finite R (Y ⊗[X] Z) := Module.Finite.trans Y (Y ⊗[X] Z)
  haveI : Algebra.Etale R (Y ⊗[X] Z) := Algebra.Etale.comp R Y (Y ⊗[X] Z)
  apply PushoutCocone.isColimitAux'
  intro s
  let leftR : Y →ₐ[R] s.pt := s.inl.hom.hom
  let rightR : Z →ₐ[R] s.pt := s.inr.hom.hom
  letI : Algebra X s.pt := (leftR.comp f.hom.hom).toRingHom.toAlgebra
  haveI : IsScalarTower R X s.pt :=
    IsScalarTower.of_algebraMap_eq' (leftR.comp f.hom.hom).comp_algebraMap.symm
  let leftX : Y →ₐ[X] s.pt :=
    { leftR.toRingHom with
      commutes' := fun x => rfl }
  let rightX : Z →ₐ[X] s.pt :=
    { rightR.toRingHom with
      commutes' := fun x => by
        change rightR (g.hom.hom x) = leftR (f.hom.hom x)
        exact
          (congrArg (fun h => h.hom.hom x) (PushoutCocone.condition s)).symm }
  let liftX : (Y ⊗[X] Z) →ₐ[X] s.pt :=
    Algebra.TensorProduct.lift leftX rightX (fun _ _ => .all _ _)
  let liftR : (Y ⊗[X] Z) →ₐ[R] s.pt := liftX.restrictScalars R
  let l : (finiteEtalePushoutCocone R f g).pt ⟶ s.pt :=
    ObjectProperty.homMk (CommAlgCat.ofHom liftR)
  refine ⟨l, ?_, ?_, ?_⟩
  · apply ObjectProperty.hom_ext
    apply CommAlgCat.hom_ext
    apply AlgHom.ext
    intro y
    change liftR (y ⊗ₜ[X] 1) = leftR y
    simp [liftR, liftX, leftX, leftR]
  · apply ObjectProperty.hom_ext
    apply CommAlgCat.hom_ext
    apply AlgHom.ext
    intro z
    change liftR (1 ⊗ₜ[X] z) = rightR z
    simp [liftR, liftX, rightX, rightR]
  · intro m hmLeft hmRight
    apply ObjectProperty.hom_ext
    apply CommAlgCat.hom_ext
    apply AlgHom.coe_ringHom_injective
    apply Algebra.TensorProduct.ringHom_ext
    · ext y
      have hLeft := congrArg (fun h => h.hom.hom y) hmLeft
      change m.hom.hom (y ⊗ₜ[X] 1) = leftR y at hLeft
      change m.hom.hom (y ⊗ₜ[X] 1) = liftR (y ⊗ₜ[X] 1)
      rw [hLeft]
      simp [liftR, liftX, leftX, leftR]
    · ext z
      have hRight := congrArg (fun h => h.hom.hom z) hmRight
      change m.hom.hom (1 ⊗ₜ[X] z) = rightR z at hRight
      change m.hom.hom (1 ⊗ₜ[X] z) = liftR (1 ⊗ₜ[X] z)
      rw [hRight]
      simp [liftR, liftX, rightX, rightR]

private noncomputable instance finiteEtaleHasPushout
    (R : Type u) [CommRing R]
    {X Y Z : CommAlgCat.FiniteEtale.{u} R}
    (f : X ⟶ Y) (g : X ⟶ Z) : HasPushout f g :=
  HasColimit.mk
    { cocone := finiteEtalePushoutCocone R f g
      isColimit := finiteEtalePushoutCoconeIsColimit R f g }

private noncomputable instance finiteEtaleHasPushouts
    (R : Type u) [CommRing R] :
    HasPushouts (CommAlgCat.FiniteEtale.{u} R) :=
  hasPushouts_of_hasColimit_span _

noncomputable instance coverCategoryHasPullbacks :
    HasPullbacks (CoverCategory.{u, u} k) := by
  infer_instance

/-- The G1 conjunction for the canonical same-universe cover category. -/
theorem coverCategoryG1 : G1Goal.{u, u} k := by
  exact ⟨inferInstance, inferInstance⟩

end
end LeanArith.BridgeBAffine
