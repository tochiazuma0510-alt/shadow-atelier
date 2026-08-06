/-
Bridge B, affine route: preservation of terminal objects by the geometric
fiber functor.

This file proves only the terminal-object field. It does not assert a full
FiberFunctor, preservation of pullbacks or coproducts, quotient preservation,
epimorphism preservation, reflection of isomorphisms, or any G3 field.
-/

import LeanArith.BridgeBAffineG2FiniteGroupQuotients
import Mathlib.CategoryTheory.Limits.Preserves.Shapes.Terminal

open CategoryTheory Limits

namespace LeanArith.BridgeBAffine

universe u w

noncomputable section

variable (k : Type u) [Field k]
variable (Omega : Type w) [Field Omega] [hOmegaSep : IsSepClosed Omega]
  [Algebra (AU k) Omega]

private def finiteEtaleInitialSelfForFiber :
    IsInitial (CommAlgCat.FiniteEtale.of (AU k) (AU k)) :=
  IsInitial.ofUniqueHom
    (fun A => ObjectProperty.homMk
      (CommAlgCat.ofHom (Algebra.ofId (AU k) A)))
    (fun A f => by
      apply ObjectProperty.hom_ext
      apply CommAlgCat.hom_ext
      exact AlgHom.ext fun x => by
        simpa using f.hom.hom.commutes x)

private def canonicalCoverIsTerminal :
    IsTerminal
      (Opposite.op
        (CommAlgCat.FiniteEtale.of (AU k) (AU k)) :
        CoverCategory.{u, u} k) :=
  (finiteEtaleInitialSelfForFiber k).op

private def canonicalFiberIsTerminal :
    IsTerminal
      ((fiber (k := k) Omega).obj
        (Opposite.op
          (CommAlgCat.FiniteEtale.of (AU k) (AU k)))) := by
  apply IsTerminal.ofUniqueHom
    (fun X => FintypeCat.homMk
      (fun _ => Algebra.ofId (AU k) Omega))
  intro X f
  apply FintypeCat.hom_ext
  intro x
  apply AlgHom.ext
  intro r
  exact (f x).commutes r

private noncomputable def fiberTerminalIso :
    (fiber (k := k) Omega).obj
        (terminal (CoverCategory.{u, u} k)) ≅
      terminal FintypeCat.{max u w} :=
  (fiber (k := k) Omega).mapIso
      (terminalIsoIsTerminal (canonicalCoverIsTerminal k))
    ≪≫
  (terminalIsoIsTerminal (canonicalFiberIsTerminal k Omega)).symm

private noncomputable instance fiberPreservesChosenTerminal :
    PreservesLimit
      (Functor.empty.{0} (CoverCategory.{u, u} k))
      (fiber (k := k) Omega) :=
  preservesTerminal_of_iso
    (fiber (k := k) Omega)
    (fiberTerminalIso k Omega)

omit hOmegaSep in
/-- The geometric fiber functor on the canonical same-universe affine cover
category preserves terminal objects. -/
noncomputable instance fiberPreservesTerminalObjects :
    PreservesLimitsOfShape.{0, 0, u, max u w,
      u + 1, max (w + 1) (u + 1)}
      (Discrete PEmpty.{1})
      (fiber (k := k) Omega) :=
  preservesLimitsOfShape_pempty_of_preservesTerminal
    (fiber (k := k) Omega)

omit hOmegaSep in
/-- Exact-field witness: an arbitrary empty diagram is preserved by the public
terminal-preservation instance. -/
theorem fiberPreservesTerminalObjectsWitness
    (K : Discrete PEmpty.{1} ⥤ CoverCategory.{u, u} k) :
    PreservesLimit K (fiber (k := k) Omega) := by
  infer_instance

#print axioms fiberPreservesTerminalObjects
#print axioms fiberPreservesTerminalObjectsWitness

end
end LeanArith.BridgeBAffine
