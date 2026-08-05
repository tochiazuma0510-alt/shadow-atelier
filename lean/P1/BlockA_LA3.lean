/-
P1/BlockA_LA3.lean - LA-3 residual: exact index, transversal, and family injectivity.

This module reuses the subgroup and canonical decomposition already proved in
P1.BlockA. It does not import LA-2. Consequently the transversal conclusions
below use the existing, exact window.XCode representatives. Identifying those
representatives with the actual powers of the marking Xg under oddness is the
single integration obligation owned by LA-2; no paper-level actual-X theorem
is asserted here without that bridge.
-/

import P1.BlockA

variable {n : Nat} [NeZero n]

namespace window

/-! ## The 2n representative codes -/

/-- The two blocks of Fin (2*n) enumerate XCode n without a cardinality assumption. -/
def la3FinToXCode (k : Fin (2 * n)) : XCode n :=
  if hk : k.val < n then
    ⟨⟨k.val, hk⟩, false⟩
  else
    ⟨⟨k.val - n, by omega⟩, true⟩

/-- Inverse enumeration: the even block first, then the odd block. -/
def la3XCodeToFin (c : XCode n) : Fin (2 * n) :=
  match c.odd with
  | false => ⟨c.rot.val, by omega⟩
  | true => ⟨n + c.rot.val, by omega⟩

omit [NeZero n] in
theorem la3FinToXCode_left_inv (c : XCode n) :
    la3FinToXCode (la3XCodeToFin c) = c := by
  rcases c with ⟨a, e⟩
  cases e
  · simp [la3FinToXCode, la3XCodeToFin, a.isLt]
  · have hnot : ¬ n + a.val < n := by omega
    simp [la3FinToXCode, la3XCodeToFin, hnot]

omit [NeZero n] in
theorem la3XCodeToFin_left_inv (k : Fin (2 * n)) :
    la3XCodeToFin (la3FinToXCode k) = k := by
  rw [la3FinToXCode]
  split
  · apply Fin.ext
    rfl
  · rename_i hk
    apply Fin.ext
    simp [la3XCodeToFin]
    omega

/-- Exact plain-Lean equivalence Fin (2*n) to XCode n. -/
def la3FinXCodeEquiv : PlainEquiv (Fin (2 * n)) (XCode n) :=
  ⟨la3FinToXCode, la3XCodeToFin,
    la3XCodeToFin_left_inv, la3FinToXCode_left_inv⟩

/-! ## Coordinate transversal and trivial intersection -/

theorem la3SplitXrepFirst (j : J) (alpha beta : Fin n) (c : XCode n) :
    (split j alpha beta (xrep c)).1 = c := by
  rcases c with ⟨a, e⟩
  cases j <;> cases e <;>
    simp [split, xrep, xrepEn, signed, betaTerm,
      Fin.mul_zero, fin_neg_zero, fin_sub_zero]

theorem la3SplitEncodeFirst (j : J) (alpha beta : Fin n) (c : Code n) :
    (split j alpha beta (encode j alpha beta c)).1 = ⟨0, false⟩ := by
  rcases c with ⟨s, t, e⟩
  cases j <;> cases e <;>
    simp [split, encode, encodeEn, signed, betaTerm]

/-- The canonical decomposition supplies every H-family coset with an
XCode representative. This is exactly the existing Transitive proposition. -/
theorem familyTransitive (j : J) (alpha beta : Fin n) :
    Transitive (H j alpha beta) := by
  intro g
  let p := split j alpha beta g
  refine ⟨p.1, encode j alpha beta p.2, ⟨p.2, rfl⟩, ?_⟩
  exact (join_split j alpha beta g).symm

/-- The only XCode representative lying in the family subgroup is the identity
code. This is the exact existing TrivialInter proposition. -/
theorem familyTrivialInter (j : J) (alpha beta : Fin n) :
    TrivialInter (H j alpha beta) := by
  intro c hc
  rcases hc with ⟨e, he⟩
  have hs := congrArg (fun g => (split j alpha beta g).1) he
  rw [la3SplitXrepFirst, la3SplitEncodeFirst] at hs
  exact hs

/-! ## Actual left cosets -/

/-- Right multiplication by an element of a subgroup does not change a left coset. -/
theorem leftCoset_mul_right
    {H0 : Gn n → Prop} (hH : IsSubgrp H0) (g h : Gn n) (hh : H0 h) :
    leftCoset H0 (g * h) = leftCoset H0 g := by
  funext x
  apply propext
  constructor
  · rintro ⟨k, hk, rfl⟩
    refine ⟨h * k, hH.mul_mem hh hk, ?_⟩
    exact Gn_groupLaws.mul_assoc g h k
  · rintro ⟨k, hk, rfl⟩
    refine ⟨h⁻¹ * k, hH.mul_mem (hH.inv_mem hh) hk, ?_⟩
    calc
      g * k = g * (1 * k) := by rw [Gn_groupLaws.one_mul]
      _ = g * ((h * h⁻¹) * k) := by rw [Gn_groupLaws.mul_inv]
      _ = g * (h * (h⁻¹ * k)) := by rw [Gn_groupLaws.mul_assoc]
      _ = (g * h) * (h⁻¹ * k) := (Gn_groupLaws.mul_assoc _ _ _).symm

/-- The actual left coset represented by an XCode. -/
def la3CodeCoset (j : J) (alpha beta : Fin n) (c : XCode n) :
    LeftCosets (H j alpha beta) :=
  ⟨leftCoset (H j alpha beta) (xrep c), ⟨xrep c, rfl⟩⟩

/-- Each ambient element has the same left coset as the first component of its
canonical decomposition. -/
theorem la3CodeCoset_split (j : J) (alpha beta : Fin n) (g : Gn n) :
    la3CodeCoset j alpha beta (split j alpha beta g).1 =
      ⟨leftCoset (H j alpha beta) g, ⟨g, rfl⟩⟩ := by
  apply Subtype.ext
  have hj := join_split j alpha beta g
  change xrep (split j alpha beta g).1 *
      encode j alpha beta (split j alpha beta g).2 = g at hj
  change leftCoset (H j alpha beta) (xrep (split j alpha beta g).1) =
    leftCoset (H j alpha beta) g
  calc
    _ = leftCoset (H j alpha beta)
        (xrep (split j alpha beta g).1 *
          encode j alpha beta (split j alpha beta g).2) :=
      (leftCoset_mul_right (isSubgroup j alpha beta)
        (xrep (split j alpha beta g).1)
        (encode j alpha beta (split j alpha beta g).2)
        ⟨(split j alpha beta g).2, rfl⟩).symm
    _ = leftCoset (H j alpha beta) g := congrArg _ hj

/-- Distinct canonical representatives determine distinct actual left cosets. -/
theorem la3CodeCoset_injective (j : J) (alpha beta : Fin n) :
    Function.Injective (la3CodeCoset j alpha beta) := by
  intro c d hcd
  have hc : leftCoset (H j alpha beta) (xrep c) (xrep c) :=
    ⟨1, (isSubgroup j alpha beta).one_mem, (Gn_groupLaws.mul_one _).symm⟩
  have hd : leftCoset (H j alpha beta) (xrep d) (xrep c) := by
    have hpred : leftCoset (H j alpha beta) (xrep c) =
        leftCoset (H j alpha beta) (xrep d) := congrArg Subtype.val hcd
    exact Eq.mp (congrArg (fun P => P (xrep c)) hpred) hc
  rcases hd with ⟨h, ⟨e, he⟩, hx⟩
  subst h
  change xrep c = join j alpha beta (d, e) at hx
  have hs := congrArg (split j alpha beta) hx
  rw [split_join] at hs
  have hcfirst := la3SplitXrepFirst j alpha beta c
  exact hcfirst.symm.trans (congrArg Prod.fst hs)

/-- Choose the canonical representative code of an actual left coset. -/
noncomputable def la3CosetCode (j : J) (alpha beta : Fin n)
    (K : LeftCosets (H j alpha beta)) : XCode n :=
  (split j alpha beta (Classical.choose K.property)).1

theorem la3CodeCoset_cosetCode (j : J) (alpha beta : Fin n)
    (K : LeftCosets (H j alpha beta)) :
    la3CodeCoset j alpha beta (la3CosetCode j alpha beta K) = K := by
  let g := Classical.choose K.property
  have hg : K.val = leftCoset (H j alpha beta) g := Classical.choose_spec K.property
  have hcanon := la3CodeCoset_split j alpha beta g
  apply Subtype.ext
  change leftCoset (H j alpha beta) (xrep (split j alpha beta g).1) = K.val
  exact (congrArg Subtype.val hcanon).trans hg.symm

theorem la3CosetCode_codeCoset (j : J) (alpha beta : Fin n) (c : XCode n) :
    la3CosetCode j alpha beta (la3CodeCoset j alpha beta c) = c := by
  apply la3CodeCoset_injective j alpha beta
  exact la3CodeCoset_cosetCode j alpha beta (la3CodeCoset j alpha beta c)

/-- Exact, marking-independent equivalence from the 2n representative codes to
the actual left-coset type. -/
noncomputable def la3FinCosetEquiv (j : J) (alpha beta : Fin n) :
    PlainEquiv (Fin (2 * n)) (LeftCosets (H j alpha beta)) where
  toFun k := la3CodeCoset j alpha beta (la3FinToXCode k)
  invFun K := la3XCodeToFin (la3CosetCode j alpha beta K)
  left_inv k := by
    rw [la3CosetCode_codeCoset]
    exact la3XCodeToFin_left_inv k
  right_inv K := by
    rw [la3FinToXCode_left_inv]
    exact la3CodeCoset_cosetCode j alpha beta K

/-- LA-3 exact P1 witness: subgroup closure together with the literal
Fin (2*n) to LeftCosets H witness required by Index2nWitness. -/
noncomputable def familyIndex2nWitness (j : J) (alpha beta : Fin n) :
    Index2nWitness (H j alpha beta) :=
  ⟨isSubgroup j alpha beta, la3FinCosetEquiv j alpha beta⟩

/-! ## Injectivity of the three family parameters -/

theorem H_parameters_eq
    {j k : J} {alpha beta gamma delta : Fin n}
    (hEq : H j alpha beta = H k gamma delta) :
    j = k ∧ alpha = gamma ∧ beta = delta := by
  have hjMem : H k gamma delta (encode j alpha beta ⟨0, 0, true⟩) := by
    rw [← hEq]
    exact ⟨⟨0, 0, true⟩, rfl⟩
  have hj : j = k := by
    rcases hjMem with ⟨⟨s, t, e⟩, he⟩
    have hv := congrArg Subtype.val he
    cases j <;> cases k <;> cases e <;>
      simp [encode, encodeEn] at hv ⊢
  subst k
  have haMem : H j gamma delta (encode j alpha beta ⟨0, 1, false⟩) := by
    rw [← hEq]
    exact ⟨⟨0, 1, false⟩, rfl⟩
  have ha : alpha = gamma := by
    rcases haMem with ⟨⟨s, t, e⟩, he⟩
    have hv := congrArg Subtype.val he
    cases j
    · cases e
      · simp [encode, encodeEn] at hv
        rcases hv with ⟨ha, _, ht⟩
        cases ht
        simpa [Fin.mul_one] using ha
      · simp [encode, encodeEn] at hv
    · cases e
      · simp [encode, encodeEn] at hv
        rcases hv with ⟨ha, ht, _⟩
        cases ht
        simpa [Fin.mul_one] using ha
      · simp [encode, encodeEn] at hv
  have hbMem : H j gamma delta (encode j alpha beta ⟨0, 0, true⟩) := by
    rw [← hEq]
    exact ⟨⟨0, 0, true⟩, rfl⟩
  have hb : beta = delta := by
    rcases hbMem with ⟨⟨s, t, e⟩, he⟩
    have hv := congrArg Subtype.val he
    cases j
    · cases e
      · simp [encode, encodeEn] at hv
      · simp [encode, encodeEn] at hv
        rcases hv with ⟨hb, _, ht⟩
        cases ht
        simpa [Fin.mul_zero, fin_add_zero] using hb
    · cases e
      · simp [encode, encodeEn] at hv
      · simp [encode, encodeEn] at hv
        rcases hv with ⟨hb, ht, _⟩
        cases ht
        simpa [Fin.mul_zero, fin_add_zero] using hb
  exact ⟨rfl, ha, hb⟩

/-- Exact injectivity of (j,alpha,beta) mapped to H. -/
theorem H_parameter_injective :
    Function.Injective
      (fun p : J × Fin n × Fin n => H p.1 p.2.1 p.2.2) := by
  rintro ⟨j, alpha, beta⟩ ⟨k, gamma, delta⟩ hEq
  rcases H_parameters_eq hEq with ⟨rfl, rfl, rfl⟩
  rfl

/-! ## Paper-domain wrapper and LA-2 integration boundary -/

/-- The full LA-3 output expressible without importing LA-2. The hypotheses state
the paper's odd window domain explicitly. The conclusion is not weakened: it contains
the exact index witness and the two current transversal/intersection propositions.

To rewrite familyTransitive as an action by actual powers xpowGn, integration must
supply LA-2's equality/equivalence between all xrep codes and those powers. -/
theorem isSubgroup_P1_P3_coded
    (hn : NatOdd n) (hn3 : 3 ≤ n) (j : J) (alpha beta : Fin n) :
    ∃ _ : Index2nWitness (H j alpha beta),
      Transitive (H j alpha beta) ∧ TrivialInter (H j alpha beta) := by
  have _paperDomain : NatOdd n ∧ 3 ≤ n := ⟨hn, hn3⟩
  exact ⟨familyIndex2nWitness j alpha beta,
    familyTransitive j alpha beta, familyTrivialInter j alpha beta⟩

end window
