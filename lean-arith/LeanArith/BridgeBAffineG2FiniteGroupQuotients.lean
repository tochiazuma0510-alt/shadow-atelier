/-
Bridge B, affine route: the G2b finite-group-quotient obligation.

The only project axiom used here is the finite-etale fixed-subalgebra closure
registered in LeanArith.ShadowAxioms. The categorical cocone and its universal
property are constructed explicitly.
-/

import LeanArith.BridgeBAffineG2FiniteCoproducts
import LeanArith.ShadowAxioms
import Mathlib.CategoryTheory.Action.Basic
import Mathlib.RingTheory.Noetherian.Basic

open CategoryTheory Limits

namespace LeanArith.BridgeBAffine

universe u

noncomputable section

variable (k : Type u) [Field k]

private abbrev diagramAlgebra
    {G : Type u} [Group G]
    (F : SingleObj G ⥤ CoverCategory.{u, u} k) : Type u :=
  (F.obj (SingleObj.star G)).unop

@[reducible] private def diagramMulSemiringAction
    {G : Type u} [Group G]
    (F : SingleObj G ⥤ CoverCategory.{u, u} k) :
    MulSemiringAction G (diagramAlgebra k F) where
  smul g b := (F.map g⁻¹).unop.hom.hom b
  one_smul b := by
    change (F.map ((1 : G)⁻¹)).unop.hom.hom b = b
    rw [inv_one]
    change
      (F.map (𝟙 (SingleObj.star G))).unop.hom.hom b = b
    rw [F.map_id]
    rfl
  mul_smul g h b := by
    change
      (F.map ((g * h)⁻¹)).unop.hom.hom b =
        (F.map g⁻¹).unop.hom.hom ((F.map h⁻¹).unop.hom.hom b)
    rw [mul_inv_rev]
    change
      (F.map (g⁻¹ ≫ h⁻¹)).unop.hom.hom b =
        (F.map g⁻¹).unop.hom.hom ((F.map h⁻¹).unop.hom.hom b)
    rw [F.map_comp]
    rfl
  smul_zero g := map_zero (F.map g⁻¹).unop.hom.hom
  smul_add g x y := map_add (F.map g⁻¹).unop.hom.hom x y
  smul_one g := map_one (F.map g⁻¹).unop.hom.hom
  smul_mul g x y := map_mul (F.map g⁻¹).unop.hom.hom x y

private theorem diagramSMulCommClass
    {G : Type u} [Group G]
    (F : SingleObj G ⥤ CoverCategory.{u, u} k) :
    @SMulCommClass G (AU k) (diagramAlgebra k F)
      (diagramMulSemiringAction k F).toSMul inferInstance := by
  letI := diagramMulSemiringAction k F
  exact
    { smul_comm := fun g r b => by
        change
          (F.map g⁻¹).unop.hom.hom (r • b) =
            r • (F.map g⁻¹).unop.hom.hom b
        exact map_smul (F.map g⁻¹).unop.hom.hom r b }

private theorem fixedSubalgebraModuleFinite
    {G : Type u} [Group G] [Finite G]
    (F : SingleObj G ⥤ CoverCategory.{u, u} k) :
    letI := diagramMulSemiringAction k F
    letI := diagramSMulCommClass k F
    Module.Finite (AU k)
      (FixedPoints.subalgebra (AU k) (diagramAlgebra k F) G) := by
  letI := diagramMulSemiringAction k F
  letI := diagramSMulCommClass k F
  exact Module.Finite.of_fg
    (IsNoetherian.noetherian
      (FixedPoints.subalgebra
        (AU k) (diagramAlgebra k F) G).toSubmodule)

private noncomputable def finiteGroupQuotientColimitCocone
    {G : Type u} [Group G] [Finite G]
    (F : SingleObj G ⥤ CoverCategory.{u, u} k) :
    ColimitCocone F := by
  letI : MulSemiringAction G (diagramAlgebra k F) :=
    diagramMulSemiringAction k F
  letI : SMulCommClass G (AU k) (diagramAlgebra k F) :=
    diagramSMulCommClass k F
  let S :=
    FixedPoints.subalgebra (AU k) (diagramAlgebra k F) G
  letI : Module.Finite (AU k) S :=
    fixedSubalgebraModuleFinite k F
  -- AXIOM USE: ShadowAxioms.fixedPointsSubalgebra_etale_of_finite.
  -- Removal target: the corresponding theorem or instance in Mathlib.
  letI : Algebra.Etale (AU k) S :=
    ShadowAxioms.fixedPointsSubalgebra_etale_of_finite
      (AU k) (diagramAlgebra k F) G
  let Q : CommAlgCat.FiniteEtale.{u} (AU k) :=
    CommAlgCat.FiniteEtale.of (AU k) S
  let inclusion :
      Q ⟶ (F.obj (SingleObj.star G)).unop :=
    ObjectProperty.homMk (CommAlgCat.ofHom S.val)
  let t : Cocone F :=
    Cocone.mk (Opposite.op Q)
      { app := fun j => by
          cases j
          exact inclusion.op
        naturality := by
          intro X Y g
          cases X
          cases Y
          change F.map g ≫ inclusion.op = inclusion.op
          apply Quiver.Hom.unop_inj
          apply ObjectProperty.hom_ext
          apply CommAlgCat.hom_ext
          apply AlgHom.ext
          intro x
          change (F.map g).unop.hom.hom x.1 = x.1
          have hx := x.2 g⁻¹
          change (F.map (g⁻¹)⁻¹).unop.hom.hom x.1 = x.1 at hx
          simpa using hx }
  refine
    { cocone := t
      isColimit := ?_ }
  refine
    { desc := fun s => ?_
      fac := ?_
      uniq := ?_ }
  · let baseMap :
        s.pt.unop ⟶ (F.obj (SingleObj.star G)).unop :=
      (s.ι.app (SingleObj.star G)).unop
    let liftAlg : s.pt.unop →ₐ[AU k] S :=
      baseMap.hom.hom.codRestrict S (fun x => by
        intro g
        change
          (F.map g⁻¹).unop.hom.hom (baseMap.hom.hom x) =
            baseMap.hom.hom x
        have h := congrArg
          (fun f : F.obj (SingleObj.star G) ⟶ s.pt =>
            f.unop.hom.hom x)
          (s.w (j := SingleObj.star G) (j' := SingleObj.star G) g⁻¹)
        change
          (F.map g⁻¹).unop.hom.hom
              ((s.ι.app (SingleObj.star G)).unop.hom.hom x) =
            (s.ι.app (SingleObj.star G)).unop.hom.hom x at h
        change
          (F.map g⁻¹).unop.hom.hom
              ((s.ι.app (SingleObj.star G)).unop.hom.hom x) =
            (s.ι.app (SingleObj.star G)).unop.hom.hom x
        exact h)
    exact (ObjectProperty.homMk (CommAlgCat.ofHom liftAlg)).op
  · intro s j
    cases j
    apply Quiver.Hom.unop_inj
    apply ObjectProperty.hom_ext
    apply CommAlgCat.hom_ext
    apply AlgHom.ext
    intro x
    rfl
  · intro s m hm
    apply Quiver.Hom.unop_inj
    apply ObjectProperty.hom_ext
    apply CommAlgCat.hom_ext
    apply AlgHom.ext
    intro x
    apply Subtype.ext
    have h := congrArg
      (fun f : F.obj (SingleObj.star G) ⟶ s.pt =>
        f.unop.hom.hom x)
      (hm (SingleObj.star G))
    exact h

/-- The canonical same-universe category of finite etale affine covers has
colimits of diagrams indexed by every finite group. The quotient cover is the
affine spectrum of the fixed subalgebra. -/
noncomputable instance coverCategoryHasQuotientsByFiniteGroups
    (G : Type u) [Group G] [Finite G] :
    HasColimitsOfShape (SingleObj G) (CoverCategory.{u, u} k) :=
  HasColimitsOfShape.mk fun F =>
    HasColimit.mk (finiteGroupQuotientColimitCocone k F)

/-- Generic API witness: the public G2b instance supplies the colimit object,
its cocone legs, and its universal property from one typeclass synthesis. -/
noncomputable def coverCategoryFiniteGroupColimitWitness
    (G : Type u) [Group G] [Finite G]
    (F : SingleObj G ⥤ CoverCategory.{u, u} k) :
    ColimitCocone F := by
  let X := colimit F
  let leg := colimit.ι F
  let universal := colimit.isColimit F
  exact
    { cocone := colimit.cocone F
      isColimit := universal }

#print axioms coverCategoryHasQuotientsByFiniteGroups
#print axioms coverCategoryFiniteGroupColimitWitness

end
end LeanArith.BridgeBAffine
