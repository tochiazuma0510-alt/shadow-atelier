/-
P1/BlockH.lean -- abstract algebra island, first target: TORS-U / B-6tw-lf.

This is the link-free argument.  It does not fit a Galois character to a chosen root.  Starting
from one faithful regular action, one faithful comparison action of the same finite cyclic group,
and one conjugacy equality for a pair of generators, it constructs the unique
conjugation-induced automorphism of the whole cyclic group.  In the standard cyclic model that
automorphism is multiplication by the unique unit b modulo the group order.
-/

import P1.Core

/-- A finite carrier without Mathlib's `Fintype`. -/
structure FiniteCarrier (α : Type) where
  size : Nat
  enum : Fin size → α
  surjective : ∀ x : α, ∃ i : Fin size, enum i = x

/-- A plain bijection, used for the comparison map between the two torsors. -/
structure TorsorBijection (α β : Type) where
  toFun : α → β
  invFun : β → α
  left_inv : ∀ x, invFun (toFun x) = x
  right_inv : ∀ y, toFun (invFun y) = y

def plainPow {G : Type} [Mul G] [One G] (g : G) : Nat → G
  | 0 => 1
  | k + 1 => plainPow g k * g

/-- A chosen generator of a cyclic group; natural powers enumerate the carrier. -/
def IsCyclicGenerator {G : Type} [Mul G] [One G] (g : G) : Prop :=
  ∀ a : G, ∃ k : Nat, plainPow g k = a

/-- A faithful left action, used for the comparison representation `tau`. -/
structure FaithfulAction (G S : Type) [Mul G] [One G] where
  act : G → S → S
  one_act : ∀ s, act 1 s = s
  mul_act : ∀ a b s, act (a * b) s = act a (act b s)
  faithful : ∀ {a b}, (∀ s, act a s = act b s) → a = b

/-- A faithful regular left action.  The last field is simple transitivity written without
    quotient/action libraries. -/
structure FaithfulRegularAction (G S : Type) [Mul G] [One G]
    extends FaithfulAction G S where
  simply_transitive : ∀ s t, ∃ a : G,
    act a s = t ∧ ∀ b : G, act b s = t → b = a

def ImplementsConjugation {G S T : Type} [Mul G] [One G]
    (m : FaithfulRegularAction G S) (tau : FaithfulAction G T)
    (c : TorsorBijection S T) (phi : G → G) : Prop :=
  ∀ a s, c.toFun (m.act a s) = tau.act (phi a) (c.toFun s)

/-- Equality on one generator propagates to every nonnegative power. -/
theorem conjugates_generator_powers {G S T : Type} [Mul G] [One G]
    (m : FaithfulRegularAction G S) (tau : FaithfulAction G T)
    (c : TorsorBijection S T) (a0 a1 : G)
    (hgen : ∀ s, c.toFun (m.act a0 s) = tau.act a1 (c.toFun s)) :
    ∀ k s, c.toFun (m.act (plainPow a0 k) s) =
      tau.act (plainPow a1 k) (c.toFun s) := by
  intro k
  induction k with
  | zero =>
      intro s
      simp [plainPow, m.one_act, tau.one_act]
  | succ k ih =>
      intro s
      change c.toFun (m.act (plainPow a0 k * a0) s) =
        tau.act (plainPow a1 k * a1) (c.toFun s)
      rw [m.mul_act, tau.mul_act]
      calc
        c.toFun (m.act (plainPow a0 k) (m.act a0 s)) =
            tau.act (plainPow a1 k) (c.toFun (m.act a0 s)) := ih _
        _ = tau.act (plainPow a1 k) (tau.act a1 (c.toFun s)) := by rw [hgen]

theorem conjugate_exponent_exists_unique {G S T : Type} [Mul G] [One G]
    (m : FaithfulRegularAction G S) (tau : FaithfulAction G T)
    (c : TorsorBijection S T) (a0 a1 a : G)
    (hcyc0 : IsCyclicGenerator a0)
    (hgen : ∀ s, c.toFun (m.act a0 s) = tau.act a1 (c.toFun s)) :
    ∃ b : G,
      (∀ s, c.toFun (m.act a s) = tau.act b (c.toFun s)) ∧
      ∀ b' : G,
        (∀ s, c.toFun (m.act a s) = tau.act b' (c.toFun s)) → b' = b := by
  obtain ⟨k, hk⟩ := hcyc0 a
  have hmain : ∀ s, c.toFun (m.act a s) = tau.act (plainPow a1 k) (c.toFun s) := by
    intro s
    rw [← hk]
    exact conjugates_generator_powers m tau c a0 a1 hgen k s
  refine ⟨plainPow a1 k, hmain, ?_⟩
  · intro b' hb'
    apply tau.faithful
    intro t
    let s := c.invFun t
    have hct : c.toFun s = t := c.right_inv t
    rw [← hct]
    exact (hb' s).symm.trans (hmain s)

noncomputable def inducedCyclicMap {G S T : Type} [Mul G] [One G]
    (m : FaithfulRegularAction G S) (tau : FaithfulAction G T)
    (c : TorsorBijection S T) (a0 a1 : G)
    (hcyc0 : IsCyclicGenerator a0)
    (hgen : ∀ s, c.toFun (m.act a0 s) = tau.act a1 (c.toFun s)) : G → G :=
  fun a => Classical.choose (conjugate_exponent_exists_unique m tau c a0 a1 a hcyc0 hgen)

theorem inducedCyclicMap_spec {G S T : Type} [Mul G] [One G]
    (m : FaithfulRegularAction G S) (tau : FaithfulAction G T)
    (c : TorsorBijection S T) (a0 a1 : G)
    (hcyc0 : IsCyclicGenerator a0)
    (hgen : ∀ s, c.toFun (m.act a0 s) = tau.act a1 (c.toFun s)) :
    ImplementsConjugation m tau c (inducedCyclicMap m tau c a0 a1 hcyc0 hgen) := by
  intro a
  exact (Classical.choose_spec
    (conjugate_exponent_exists_unique m tau c a0 a1 a hcyc0 hgen)).1

theorem inducedCyclicMap_unique {G S T : Type} [Mul G] [One G]
    (m : FaithfulRegularAction G S) (tau : FaithfulAction G T)
    (c : TorsorBijection S T) (a0 a1 : G)
    (hcyc0 : IsCyclicGenerator a0)
    (hgen : ∀ s, c.toFun (m.act a0 s) = tau.act a1 (c.toFun s))
    (psi : G → G) (hpsi : ImplementsConjugation m tau c psi) :
    psi = inducedCyclicMap m tau c a0 a1 hcyc0 hgen := by
  funext a
  exact (Classical.choose_spec
    (conjugate_exponent_exists_unique m tau c a0 a1 a hcyc0 hgen)).2 (psi a) (hpsi a)

theorem inducedCyclicMap_one {G S T : Type} [Mul G] [One G]
    (m : FaithfulRegularAction G S) (tau : FaithfulAction G T)
    (c : TorsorBijection S T) (a0 a1 : G)
    (hcyc0 : IsCyclicGenerator a0)
    (hgen : ∀ s, c.toFun (m.act a0 s) = tau.act a1 (c.toFun s)) :
    inducedCyclicMap m tau c a0 a1 hcyc0 hgen 1 = 1 := by
  apply tau.faithful
  intro t
  let s := c.invFun t
  have hct : c.toFun s = t := c.right_inv t
  rw [← hct, tau.one_act]
  rw [← (inducedCyclicMap_spec m tau c a0 a1 hcyc0 hgen 1 s)]
  rw [m.one_act]

theorem inducedCyclicMap_mul {G S T : Type} [Mul G] [One G]
    (m : FaithfulRegularAction G S) (tau : FaithfulAction G T)
    (c : TorsorBijection S T) (a0 a1 : G)
    (hcyc0 : IsCyclicGenerator a0)
    (hgen : ∀ s, c.toFun (m.act a0 s) = tau.act a1 (c.toFun s))
    (a b : G) :
    inducedCyclicMap m tau c a0 a1 hcyc0 hgen (a * b) =
      inducedCyclicMap m tau c a0 a1 hcyc0 hgen a *
        inducedCyclicMap m tau c a0 a1 hcyc0 hgen b := by
  apply tau.faithful
  intro t
  let s := c.invFun t
  have hct : c.toFun s = t := c.right_inv t
  rw [← hct]
  rw [← (inducedCyclicMap_spec m tau c a0 a1 hcyc0 hgen (a * b) s)]
  rw [m.mul_act]
  rw [inducedCyclicMap_spec, inducedCyclicMap_spec, tau.mul_act]

theorem inducedCyclicMap_injective {G S T : Type} [Mul G] [One G]
    (m : FaithfulRegularAction G S) (tau : FaithfulAction G T)
    (c : TorsorBijection S T) (a0 a1 : G)
    (hcyc0 : IsCyclicGenerator a0)
    (hgen : ∀ s, c.toFun (m.act a0 s) = tau.act a1 (c.toFun s)) :
    Function.Injective (inducedCyclicMap m tau c a0 a1 hcyc0 hgen) := by
  intro a b hab
  apply m.faithful
  intro s
  calc
    m.act a s = c.invFun (c.toFun (m.act a s)) := (c.left_inv _).symm
    _ = c.invFun (tau.act (inducedCyclicMap m tau c a0 a1 hcyc0 hgen a)
          (c.toFun s)) := by rw [inducedCyclicMap_spec]
    _ = c.invFun (tau.act (inducedCyclicMap m tau c a0 a1 hcyc0 hgen b)
          (c.toFun s)) := by rw [hab]
    _ = c.invFun (c.toFun (m.act b s)) := by rw [inducedCyclicMap_spec]
    _ = m.act b s := c.left_inv _

theorem inducedCyclicMap_surjective {G S T : Type} [Mul G] [One G]
    (m : FaithfulRegularAction G S) (tau : FaithfulAction G T)
    (c : TorsorBijection S T) (a0 a1 : G)
    (hcyc0 : IsCyclicGenerator a0) (hcyc1 : IsCyclicGenerator a1)
    (hgen : ∀ s, c.toFun (m.act a0 s) = tau.act a1 (c.toFun s)) :
    Function.Surjective (inducedCyclicMap m tau c a0 a1 hcyc0 hgen) := by
  intro b
  obtain ⟨k, hk⟩ := hcyc1 b
  refine ⟨plainPow a0 k, ?_⟩
  apply tau.faithful
  intro t
  let s := c.invFun t
  have hct : c.toFun s = t := c.right_inv t
  rw [← hct, ← hk]
  rw [← (inducedCyclicMap_spec m tau c a0 a1 hcyc0 hgen (plainPow a0 k) s)]
  exact conjugates_generator_powers m tau c a0 a1 hgen k s

/-- **TORS-U / B-6tw-lf**.  Conjugation determines one and only one group automorphism;
    it carries the first chosen generator to the second.  In `C_M` this automorphism is
    multiplication by a unique element of `(Z/MZ)^×`.  `finite` records the intended finite
    universe and prevents this declaration from being silently reused as an infinite-torsor claim. -/
theorem torsor_compare_unit {G S T : Type} [Mul G] [One G] [Inv G]
    (_laws : PlainGroupLaws G) (_finite : FiniteCarrier G)
    (m : FaithfulRegularAction G S) (tau : FaithfulAction G T)
    (c : TorsorBijection S T) (a0 a1 : G)
    (hcyc0 : IsCyclicGenerator a0) (hcyc1 : IsCyclicGenerator a1)
    (hgen : ∀ s, c.toFun (m.act a0 s) = tau.act a1 (c.toFun s)) :
    ∃ phi : G → G,
      ImplementsConjugation m tau c phi ∧
      phi 1 = 1 ∧
      (∀ a b, phi (a * b) = phi a * phi b) ∧
      Function.Injective phi ∧ Function.Surjective phi ∧
      phi a0 = a1 ∧
      ∀ psi : G → G, ImplementsConjugation m tau c psi → psi = phi := by
  let phi := inducedCyclicMap m tau c a0 a1 hcyc0 hgen
  refine ⟨phi, inducedCyclicMap_spec m tau c a0 a1 hcyc0 hgen,
    inducedCyclicMap_one m tau c a0 a1 hcyc0 hgen,
    inducedCyclicMap_mul m tau c a0 a1 hcyc0 hgen,
    inducedCyclicMap_injective m tau c a0 a1 hcyc0 hgen,
    inducedCyclicMap_surjective m tau c a0 a1 hcyc0 hcyc1 hgen, ?_, ?_⟩
  · apply tau.faithful
    intro t
    let s := c.invFun t
    have hct : c.toFun s = t := c.right_inv t
    rw [← hct]
    rw [← (inducedCyclicMap_spec m tau c a0 a1 hcyc0 hgen a0 s)]
    exact hgen s
  · intro psi hpsi
    exact inducedCyclicMap_unique m tau c a0 a1 hcyc0 hgen psi hpsi

/-! ### The explicit cyclic model

The abstract theorem above produces an automorphism.  The following plain-core lemmas identify
an automorphism of `Fin M` with multiplication by one residue `b` and prove that `b` is a unit
by the elementary gcd criterion.  Thus the phrase `(Z/MZ)^x` is present in the theorem type,
not only in documentation.  We assume `1 < M`; this is the paper's nontrivial cyclic case and
also makes the natural representative of `1 : Fin M` literally equal to one. -/

def finAddPow {M : Nat} [NeZero M] (a : Fin M) : Nat → Fin M
  | 0 => 0
  | k + 1 => finAddPow a k + a

theorem finAddPow_val {M : Nat} [NeZero M] (a : Fin M) (k : Nat) :
    (finAddPow a k).val = (k * a.val) % M := by
  induction k with
  | zero => simp [finAddPow]
  | succ k ih =>
      rw [finAddPow, Fin.val_add, ih]
      simp only [Nat.succ_mul]
      rw [Nat.add_mod]
      simp [Nat.mod_eq_of_lt a.isLt]

theorem finAddPow_one_eq {M : Nat} [NeZero M] (hM : 1 < M) (k : Fin M) :
    finAddPow (1 : Fin M) k.val = k := by
  apply Fin.ext
  rw [finAddPow_val]
  have hone : (1 : Fin M).val = 1 := Nat.mod_eq_of_lt hM
  rw [hone, Nat.mul_one, Nat.mod_eq_of_lt k.isLt]

theorem finAddPow_eq_mul {M : Nat} [NeZero M] (a k : Fin M) :
    finAddPow a k.val = k * a := by
  apply Fin.ext
  rw [finAddPow_val, Fin.val_mul]

theorem fin_add_hom_is_mul {M : Nat} [NeZero M] (hM : 1 < M)
    (phi : Fin M → Fin M) (hzero : phi 0 = 0)
    (hadd : ∀ a b, phi (a + b) = phi a + phi b) (k : Fin M) :
    phi k = k * phi 1 := by
  have hpow : ∀ (j : Nat) (a : Fin M),
      phi (finAddPow a j) = finAddPow (phi a) j := by
    intro j
    induction j with
    | zero => intro a; simp [finAddPow, hzero]
    | succ j ih => intro a; simp [finAddPow, hadd, ih]
  calc
    phi k = phi (finAddPow (1 : Fin M) k.val) := by rw [finAddPow_one_eq hM k]
    _ = finAddPow (phi 1) k.val := hpow k.val 1
    _ = k * phi 1 := finAddPow_eq_mul _ _

theorem coprime_of_fin_mul_eq_one {M : Nat} [NeZero M] (hM : 1 < M)
    (b c : Fin M) (hinv : b * c = 1) : Nat.Coprime b.val M := by
  rw [Nat.coprime_iff_gcd_eq_one]
  apply Nat.eq_one_of_dvd_one
  have hdM : Nat.gcd b.val M ∣ M := Nat.gcd_dvd_right _ _
  have hdb : Nat.gcd b.val M ∣ b.val := Nat.gcd_dvd_left _ _
  have hdprod : Nat.gcd b.val M ∣ b.val * c.val :=
    Nat.dvd_trans hdb (Nat.dvd_mul_right _ _)
  have hdmod : Nat.gcd b.val M ∣ (b.val * c.val) % M :=
    (Nat.dvd_mod_iff hdM).2 hdprod
  have hval : (b.val * c.val) % M = 1 := by
    rw [← Fin.val_mul, hinv]
    exact Nat.mod_eq_of_lt hM
  rwa [hval] at hdmod

/-- Explicit unit classification for the nontrivial cyclic group `C_M = Fin M`.
    The witness is unique because the value at `1` determines every additive homomorphism. -/
theorem fin_cyclic_automorphism_unit {M : Nat} [NeZero M] (hM : 1 < M)
    (phi : Fin M → Fin M) (hzero : phi 0 = 0)
    (hadd : ∀ a b, phi (a + b) = phi a + phi b)
    (hsurj : Function.Surjective phi) :
    ∃ b : Fin M,
      (Nat.Coprime b.val M ∧ ∀ k : Fin M, phi k = k * b) ∧
      ∀ b' : Fin M,
        (Nat.Coprime b'.val M ∧ ∀ k : Fin M, phi k = k * b') → b' = b := by
  let b := phi 1
  obtain ⟨c, hc⟩ := hsurj 1
  have hmul : c * b = 1 := by
    rw [← fin_add_hom_is_mul hM phi hzero hadd c]
    exact hc
  have hunit : Nat.Coprime b.val M :=
    coprime_of_fin_mul_eq_one hM b c (Fin.mul_comm c b ▸ hmul)
  refine ⟨b, ⟨hunit, fin_add_hom_is_mul hM phi hzero hadd⟩, ?_⟩
  intro b' hb'
  have h1 := hb'.2 (1 : Fin M)
  have hone : (1 : Fin M) * b' = b' := by
    apply Fin.ext
    have honeval : (1 : Fin M).val = 1 := Nat.mod_eq_of_lt hM
    rw [Fin.val_mul, honeval, Nat.one_mul, Nat.mod_eq_of_lt b'.isLt]
  exact (h1.trans hone).symm

/-! ### Typed adapter from the torsor theorem to the residue-unit theorem -/

/-- `Fin M` viewed with its *additive* cyclic law under multiplicative notation. -/
structure CyclicMul (M : Nat) where
  residue : Fin M

instance {M : Nat} [NeZero M] : One (CyclicMul M) := ⟨⟨0⟩⟩
instance {M : Nat} [NeZero M] : Mul (CyclicMul M) :=
  ⟨fun a b => ⟨a.residue + b.residue⟩⟩
instance {M : Nat} [NeZero M] : Inv (CyclicMul M) := ⟨fun a => ⟨-a.residue⟩⟩

theorem cyclicMul_groupLaws {M : Nat} [NeZero M] : PlainGroupLaws (CyclicMul M) := by
  constructor
  · intro ⟨a⟩ ⟨b⟩ ⟨c⟩; exact congrArg CyclicMul.mk (fin_add_assoc a b c)
  · intro ⟨a⟩; exact congrArg CyclicMul.mk (fin_zero_add a)
  · intro ⟨a⟩; exact congrArg CyclicMul.mk (fin_add_zero a)
  · intro ⟨a⟩; exact congrArg CyclicMul.mk (fin_add_left_neg a)
  · intro ⟨a⟩; exact congrArg CyclicMul.mk (fin_add_right_neg a)

def cyclicMul_finite {M : Nat} [NeZero M] : FiniteCarrier (CyclicMul M) where
  size := M
  enum := fun i => ⟨i⟩
  surjective := by intro x; exact ⟨x.residue, by cases x; rfl⟩

def CyclicUnitFormula {M : Nat} [NeZero M] (phi : CyclicMul M → CyclicMul M)
    (b : Fin M) : Prop :=
  Nat.Coprime b.val M ∧ ∀ k : Fin M, (phi ⟨k⟩).residue = k * b

/-- TORS-U with the final `b in (Z/MZ)^x` classification attached by a real typed bridge.
    It specializes the abstract torsor comparison to the explicit cyclic model `C_M`. -/
theorem torsor_compare_fin_unit {M : Nat} [NeZero M] (hM : 1 < M)
    {S T : Type}
    (m : FaithfulRegularAction (CyclicMul M) S)
    (tau : FaithfulAction (CyclicMul M) T)
    (c : TorsorBijection S T) (a0 a1 : CyclicMul M)
    (hcyc0 : IsCyclicGenerator a0) (hcyc1 : IsCyclicGenerator a1)
    (hgen : ∀ s, c.toFun (m.act a0 s) = tau.act a1 (c.toFun s)) :
    ∃ phi : CyclicMul M → CyclicMul M,
      ImplementsConjugation m tau c phi ∧
      phi 1 = 1 ∧
      (∀ a b, phi (a * b) = phi a * phi b) ∧
      Function.Injective phi ∧ Function.Surjective phi ∧
      phi a0 = a1 ∧
      (∀ psi : CyclicMul M → CyclicMul M,
        ImplementsConjugation m tau c psi → psi = phi) ∧
      ∃ b : Fin M, CyclicUnitFormula phi b ∧
        ∀ b' : Fin M, CyclicUnitFormula phi b' → b' = b := by
  obtain ⟨phi, himpl, hone, hmul, hinj, hsurj, hmark, hunique⟩ :=
    torsor_compare_unit cyclicMul_groupLaws cyclicMul_finite
      m tau c a0 a1 hcyc0 hcyc1 hgen
  let phiFin : Fin M → Fin M := fun k => (phi ⟨k⟩).residue
  have hzero : phiFin 0 = 0 := by
    change (phi (1 : CyclicMul M)).residue = (1 : CyclicMul M).residue
    exact congrArg CyclicMul.residue hone
  have hadd : ∀ a b, phiFin (a + b) = phiFin a + phiFin b := by
    intro a b
    exact congrArg CyclicMul.residue (hmul ⟨a⟩ ⟨b⟩)
  have hsurjFin : Function.Surjective phiFin := by
    intro y
    obtain ⟨x, hx⟩ := hsurj (CyclicMul.mk y)
    exact ⟨x.residue, congrArg CyclicMul.residue hx⟩
  obtain ⟨b, hb, hbuniq⟩ :=
    fin_cyclic_automorphism_unit hM phiFin hzero hadd hsurjFin
  refine ⟨phi, himpl, hone, hmul, hinj, hsurj, hmark, hunique, b, ?_, ?_⟩
  · exact hb
  · intro b' hb'
    exact hbuniq b' hb'
