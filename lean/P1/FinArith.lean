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

/-! ### Additive group laws for `Fin n`

Lean core supplies the operations but, unlike Mathlib, does not package all of their laws in
an additive-group typeclass.  Block A needs the laws with `n` still symbolic, so we prove the
small reusable kernel here. -/

@[simp] theorem fin_add_assoc (a b c : Fin n) : (a + b) + c = a + (b + c) := by
  apply Fin.ext
  simp only [Fin.val_add]
  have ha : a.val % n = a.val := Nat.mod_eq_of_lt a.isLt
  have hc : c.val % n = c.val := Nat.mod_eq_of_lt c.isLt
  calc
    ((a.val + b.val) % n + c.val) % n
        = ((a.val + b.val) % n + c.val % n) % n := by rw [hc]
    _ = ((a.val + b.val) + c.val) % n :=
      (Nat.add_mod (a.val + b.val) c.val n).symm
    _ = (a.val + (b.val + c.val)) % n := by rw [Nat.add_assoc]
    _ = (a.val % n + (b.val + c.val) % n) % n := Nat.add_mod _ _ _
    _ = (a.val + (b.val + c.val) % n) % n := by rw [ha]

@[simp] theorem fin_add_comm (a b : Fin n) : a + b = b + a := by
  apply Fin.ext
  simp [Fin.add_def, Nat.add_comm]

@[simp] theorem fin_add_left_neg (a : Fin n) : (-a) + a = 0 := by
  rw [fin_add_comm, ← fin_sub_eq_add_neg, fin_sub_self]

@[simp] theorem fin_add_right_neg (a : Fin n) : a + (-a) = 0 := by
  rw [← fin_sub_eq_add_neg, fin_sub_self]

theorem fin_add_left_cancel (a b c : Fin n) (h : a + b = a + c) : b = c := by
  calc
    b = 0 + b := (fin_zero_add b).symm
    _ = ((-a) + a) + b := by rw [fin_add_left_neg]
    _ = (-a) + (a + b) := by rw [fin_add_assoc]
    _ = (-a) + (a + c) := by rw [h]
    _ = ((-a) + a) + c := by rw [fin_add_assoc]
    _ = 0 + c := by rw [fin_add_left_neg]
    _ = c := fin_zero_add c

theorem fin_add_right_cancel (a b c : Fin n) (h : b + a = c + a) : b = c := by
  apply fin_add_left_cancel a
  calc
    a + b = b + a := fin_add_comm _ _
    _ = c + a := h
    _ = a + c := fin_add_comm _ _

instance instFinAddAssociative : Std.Associative (α := Fin n) (· + ·) :=
  ⟨fin_add_assoc⟩

instance instFinAddCommutative : Std.Commutative (α := Fin n) (· + ·) :=
  ⟨fin_add_comm⟩

@[simp] theorem fin_neg_add (a b : Fin n) : -(a + b) = (-a) + (-b) := by
  apply fin_add_left_cancel (a + b)
  rw [fin_add_right_neg]
  have hreorder : (a + b) + ((-a) + (-b)) = (a + (-a)) + (b + (-b)) := by
    ac_rfl
  rw [hreorder, fin_add_right_neg, fin_add_right_neg, fin_zero_add]

@[simp] theorem fin_neg_sub (a b : Fin n) : -(a - b) = b - a := by
  simp [fin_sub_eq_add_neg, fin_neg_add, fin_neg_neg, fin_add_comm]

@[simp] theorem fin_add_sub_cancel_right (a b : Fin n) : (a + b) - b = a := by
  rw [fin_sub_eq_add_neg, fin_add_assoc, fin_add_right_neg, fin_add_zero]

@[simp] theorem fin_sub_add_cancel_right (a b : Fin n) : (a - b) + b = a := by
  rw [fin_sub_eq_add_neg]
  have hreorder : (a + (-b)) + b = a + ((-b) + b) := fin_add_assoc _ _ _
  rw [hreorder, fin_add_left_neg, fin_add_zero]
