/-
P1/Order.lean — 反復冪 `epow` と marking X = a₁q₁ の位数 ord(X) = 2n(補題 A(3))。

対応: docs/notes/lean_p1_allocation_plan_v1.md LA-1(`Gn.structure`)の
「ord(X)=2n」の部分。出所: docs/notes/oddH_full_proof_v1.md §2 補題 A(3)
「$a_1$ と $q_1$ は可換で位数 $n,2$、$\gcd(n,2)=1$ ゆえ $\langle X\rangle=\langle a_1q_1\rangle$…$\cong C_{2n}$」。

plain Lean 4 core のみ。emul は成分ごとの積(K3/Base.lean と同じ設計)なので、
epow も成分ごとの dpow に分解できる(補題 epow_fst 等)— これが証明の骨格。
-/

import P1.Core
import P1.FinArith
import P1.Parity

variable {n : Nat} [NeZero n]

/-- Dₙ 内の反復冪(K3/Lambda.lean `pow3`/`epow6` の一般化・自然数指数版)。 -/
def dpow (a : Dn n) : Nat → Dn n
  | 0 => done_
  | k + 1 => dmul (dpow a k) a

/-- Dₙ³ 内の反復冪。 -/
def epow (x : En n) : Nat → En n
  | 0 => eone
  | k + 1 => emul (epow x k) x

/-- `emul` は成分ごとの積だから `epow` も成分ごとに分解する。 -/
theorem epow_fst (x : En n) (k : Nat) : (epow x k).1 = dpow x.1 k := by
  induction k with
  | zero => rfl
  | succ k ih => simp [epow, dpow, emul, ih]

theorem epow_snd (x : En n) (k : Nat) : (epow x k).2.1 = dpow x.2.1 k := by
  induction k with
  | zero => rfl
  | succ k ih => simp [epow, dpow, emul, ih]

theorem epow_thd (x : En n) (k : Nat) : (epow x k).2.2 = dpow x.2.2 k := by
  induction k with
  | zero => rfl
  | succ k ih => simp [epow, dpow, emul, ih]

/-- 純回転(flag = false)の反復冪は常に flag = false を保つ。 -/
theorem dpow_rot_flag (v : Fin n) (k : Nat) : (dpow (v, false) k).2 = false := by
  induction k with
  | zero => simp [dpow, done_]
  | succ k ih =>
    show (dmul (dpow (v, false) k) (v, false)).2 = false
    simp [dmul, ih]

/-- 純回転(flag = false)の反復冪: val は k·v を法 n で足し込んだ値。 -/
theorem dpow_rot_val (v : Fin n) (k : Nat) : (dpow (v, false) k).1.val = (v.val * k) % n := by
  induction k with
  | zero => simp [dpow, done_, Nat.mul_zero, Nat.zero_mod]
  | succ k ih =>
    have hflag : (dpow (v, false) k).2 = false := dpow_rot_flag v k
    have hstep : dpow (v, false) (k + 1) = ((dpow (v, false) k).1 + v, false) := by
      show dmul (dpow (v, false) k) (v, false) = _
      unfold dmul
      rw [hflag]
      simp
    rw [hstep]
    show ((dpow (v, false) k).1 + v).val = v.val * (k + 1) % n
    rw [Fin.add_def, ih]
    have hvn : v.val % n = v.val := Nat.mod_eq_of_lt v.isLt
    have hsum : v.val * (k + 1) = v.val * k + v.val := Nat.mul_succ v.val k
    calc (v.val * k % n + v.val) % n
        = (v.val * k % n + v.val % n) % n := by rw [hvn]
      _ = (v.val * k + v.val) % n := (Nat.add_mod _ _ _).symm
      _ = v.val * (k + 1) % n := by rw [hsum]

/-- 反射(flag = true)の反復冪: 偶数回で単位元、奇数回で元自身に戻る(周期 2)。 -/
theorem dpow_refl_even (v : Fin n) (k : Nat) (h : NatEven k) :
    dpow (v, true) k = done_ := by
  obtain ⟨m, hm⟩ := h
  subst hm
  induction m with
  | zero => rfl
  | succ m ih =>
    have hrw : m + 1 + (m + 1) = (m + m) + 1 + 1 := by omega
    rw [hrw]
    show dmul (dpow (v, true) (m + m + 1)) (v, true) = done_
    have hstep1 : dpow (v, true) (m + m + 1) = dmul (dpow (v, true) (m + m)) (v, true) := rfl
    rw [hstep1, ih]
    have hinner : dmul (done_ : Dn n) (v, true) = (v, true) := by
      apply Prod.ext
      · apply Fin.ext; simp [done_, dmul, fin_zero_add]
      · simp [done_, dmul]
    rw [hinner]
    apply Prod.ext
    · apply Fin.ext; simp [done_, dmul, fin_sub_self]
    · simp [done_, dmul]

theorem dpow_refl_odd (v : Fin n) (k : Nat) (h : NatOdd k) :
    dpow (v, true) k = (v, true) := by
  obtain ⟨m, hm⟩ := h
  subst hm
  show dpow (v, true) (2 * m + 1) = (v, true)
  have hstep : dpow (v, true) (2 * m + 1) = dmul (dpow (v, true) (2 * m)) (v, true) := rfl
  rw [hstep, dpow_refl_even v (2 * m) ⟨m, by omega⟩]
  apply Prod.ext
  · apply Fin.ext; simp [done_, dmul, fin_zero_add]
  · simp [done_, dmul]

/-- **補題 A(3) 前半**: X = a₁q₁ の位数 2n の指数条件 — X^{2n} = 1。
    (`1 < n` は oddH の宇宙 n ≥ 3 で自動的に満たされる — (1 : Fin n).val = 1 に必要)。 -/
theorem X_pow_2n (hn1 : 1 < n) : epow (X : En n) (2 * n) = eone := by
  have hXfst : (X : En n).1 = (1, false) := by simp [X, emul, dmul, a1, q1, done_]
  have hXsnd : (X : En n).2.1 = (0, true) := by simp [X, emul, dmul, a1, q1, done_]
  have hXthd : (X : En n).2.2 = (0, true) := by simp [X, emul, dmul, a1, q1, done_]
  have h1 : (epow (X : En n) (2 * n)).1 = done_ := by
    rw [epow_fst, hXfst]
    apply Prod.ext
    · apply Fin.ext
      rw [dpow_rot_val]
      have : (1 : Fin n).val = 1 := Nat.mod_eq_of_lt hn1
      rw [this, Nat.one_mul]
      simp [done_]
    · rw [dpow_rot_flag]; simp [done_]
  have h2 : (epow (X : En n) (2 * n)).2.1 = done_ := by
    rw [epow_snd, hXsnd]
    exact dpow_refl_even (0 : Fin n) (2 * n) ⟨n, by omega⟩
  have h3 : (epow (X : En n) (2 * n)).2.2 = done_ := by
    rw [epow_thd, hXthd]
    exact dpow_refl_even (0 : Fin n) (2 * n) ⟨n, by omega⟩
  show (epow (X : En n) (2 * n)) = (done_, done_, done_)
  exact Prod.ext h1 (Prod.ext h2 h3)

/-- **補題 A(3) 後半**: n が奇数のとき、0 < k < 2n では X^k ≠ 1
    (`⟨X⟩` の位数がちょうど 2n であることの最小性)。 -/
theorem X_pow_lt_2n_ne (hn1 : 1 < n) (hn : NatOdd n) (k : Nat) (hk0 : 0 < k) (hk : k < 2 * n) :
    epow (X : En n) k ≠ eone := by
  intro heq
  have hXsnd : (X : En n).2.1 = (0, true) := by simp [X, emul, dmul, a1, q1, done_]
  have h2 : (epow (X : En n) k).2.1 = done_ := by rw [heq]; simp [eone]
  rw [epow_snd, hXsnd] at h2
  rcases natEven_or_natOdd k with he | ho
  · -- k 偶数: 第 2 成分だけでは矛盾が出ない。第 1 成分を使う。
    have hXfst : (X : En n).1 = (1, false) := by simp [X, emul, dmul, a1, q1, done_]
    have h1 : (epow (X : En n) k).1 = done_ := by rw [heq]; simp [eone]
    rw [epow_fst, hXfst] at h1
    have hone : (1 : Fin n).val = 1 := Nat.mod_eq_of_lt hn1
    have hval : (dpow ((1 : Fin n), false) k).1.val = k % n := by
      rw [dpow_rot_val, hone, Nat.one_mul]
    have hval0 : (dpow ((1 : Fin n), false) k).1.val = 0 := by
      rw [h1]; simp [done_]
    rw [hval] at hval0
    -- hval0 : k % n = 0、he : k = m+m(偶数)、0<k<2n ⟹ k = n
    obtain ⟨m, hm⟩ := he
    have hkn : k = n := by
      rcases Nat.lt_or_ge k n with hlt | hge
      · exact absurd (Nat.mod_eq_of_lt hlt ▸ hval0) (by omega)
      · have hlt2 : k - n < n := by omega
        have hmodeq : k % n = k - n := by
          have hh := Nat.mod_eq_sub_mod (a := k) (b := n) hge
          rw [Nat.mod_eq_of_lt hlt2] at hh
          exact hh
        rw [hmodeq] at hval0
        omega
    rw [hkn] at hm
    obtain ⟨p, hp⟩ := hn
    omega
  · -- k 奇数: dpow (0,true) k = (0,true) ≠ done_(flag が食い違う)
    have := dpow_refl_odd (0 : Fin n) k ho
    rw [this] at h2
    exact absurd h2 (by simp [done_])
