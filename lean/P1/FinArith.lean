/-
P1/FinArith.lean — Fin n の加法群としての最小補助補題集(plain Lean 4 core・Mathlib 不使用)。

plain Lean 4 core は `Fin n`(n 変数)に Add/Sub/Neg のインスタンスを generic に提供するが、
`add_zero`/`neg_neg` 級の基本等式は simp では閉じない(K3 系列の n=3 固定の `decide` と違い、
ここでは n が全称量化された変数なので decide が使えない)。本ファイルは Core.lean・BlockA.lean・
BlockE.lean で使う最小限だけを自前で証明する。
-/

variable {n : Nat} [NeZero n]

theorem fin_add_zero (a : Fin n) : a + (0 : Fin n) = a := by
  apply Fin.ext; simp [Fin.add_def, Nat.mod_eq_of_lt a.isLt]

theorem fin_zero_add (a : Fin n) : (0 : Fin n) + a = a := by
  apply Fin.ext; simp [Fin.add_def, Nat.mod_eq_of_lt a.isLt]

theorem fin_sub_zero (a : Fin n) : a - (0 : Fin n) = a := by
  apply Fin.ext; simp [Fin.sub_def, Nat.mod_eq_of_lt a.isLt]

theorem fin_zero_sub (a : Fin n) : (0 : Fin n) - a = -a := by
  apply Fin.ext; simp [Fin.sub_def, Fin.neg_def]

theorem fin_neg_zero : (-(0 : Fin n)) = 0 := by
  apply Fin.ext; simp [Fin.neg_def]

theorem fin_neg_neg (a : Fin n) : - (-a) = a := by
  apply Fin.ext
  by_cases h : a = 0
  · subst h; simp [fin_neg_zero]
  · have h1 : (a : Fin n) ≠ 0 := h
    have hv : a.val ≠ 0 := by
      intro hc; apply h1; apply Fin.ext; simpa using hc
    have hlt : a.val < n := a.isLt
    have hval : (-a).val = n - a.val := by rw [Fin.val_neg]; simp [h]
    have hne2 : (-a) ≠ 0 := by
      intro hc
      have h0 : (-a).val = 0 := by rw [hc]; simp
      rw [hval] at h0
      omega
    rw [Fin.val_neg, hval]
    simp [hne2]
    omega

/-- `a - b = a + (-b)`(Fin n の Sub は Add と Neg から一貫している)。 -/
theorem fin_sub_eq_add_neg (a b : Fin n) : a - b = a + (-b) := by
  apply Fin.ext
  by_cases h : b = 0
  · subst h; simp [Fin.sub_def, Fin.add_def, fin_neg_zero, Nat.mod_eq_of_lt a.isLt]
  · have hv : b.val ≠ 0 := by
      intro hc; apply h; apply Fin.ext; simpa using hc
    have hval : (-b).val = n - b.val := by rw [Fin.val_neg]; simp [h]
    simp [Fin.sub_def, Fin.add_def, hval, Nat.add_comm]

/-- `a - a = 0`(Fin n の加法逆元則)。dpow_refl_even/odd(反射の対合性)で使う。 -/
theorem fin_sub_self (a : Fin n) : a - a = 0 := by
  apply Fin.ext
  by_cases h : a = 0
  · subst h; simp [Fin.sub_def]
  · have hv : a.val ≠ 0 := by
      intro hc; apply h; apply Fin.ext; simpa using hc
    have hlt : a.val < n := a.isLt
    simp
