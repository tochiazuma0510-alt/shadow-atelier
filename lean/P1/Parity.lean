/-
P1/Parity.lean — Nat の偶奇(plain Lean 4 core には `Even`/`Odd` が無い — Mathlib 概念のため自前定義)。
-/

/-- 自然数の偶数性(Mathlib の `Even` と同じ定義を自前で)。 -/
def NatEven (k : Nat) : Prop := ∃ m, k = m + m

/-- 自然数の奇数性。 -/
def NatOdd (k : Nat) : Prop := ∃ m, k = 2 * m + 1

theorem natEven_or_natOdd (k : Nat) : NatEven k ∨ NatOdd k := by
  induction k with
  | zero => exact Or.inl ⟨0, rfl⟩
  | succ k ih =>
    rcases ih with ⟨m, hm⟩ | ⟨m, hm⟩
    · exact Or.inr ⟨m, by omega⟩
    · exact Or.inl ⟨m + 1, by omega⟩

theorem not_natEven_and_natOdd (k : Nat) : NatEven k → NatOdd k → False := by
  rintro ⟨m, hm⟩ ⟨m', hm'⟩
  omega

/-- n が奇数(NatOdd)なら n は NatEven ではない。 -/
theorem natOdd_not_natEven (k : Nat) (h : NatOdd k) : ¬ NatEven k :=
  fun he => not_natEven_and_natOdd k he h
