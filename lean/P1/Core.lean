/-
P1/Core.lean — ブロック A・E の基盤(群 G_n = A ⋊ Q、族版・n : Nat を変数のまま扱う)。

対応: docs/notes/lean_p1_allocation_plan_v1.md §3.1(ブロック A)・§3.5(ブロック E)。
出所: docs/notes/oddH_full_proof_v1.md §2「補題 A(構造補題)」。

plain Lean 4 core のみ(Mathlib 不使用)。K3/Base.lean(n=3 固定・decide 検算)の
一般化だが、ここでは n が全称量化された変数なので `decide` は使えない — 構造的な
等式証明(`rfl`/`simp`/成分ごとの計算)のみで進める。
-/

import P1.FinArith

/-- Dₙ の元 rᵃsᵉ を (a,e) : Fin n × Bool で表す(K3/Base.lean `D` の一般化)。
    正典 Dₙ = ⟨r,s ∣ rⁿ, s², srs⁻¹r⟩(oddH §2)。 -/
abbrev Dn (n : Nat) : Type := Fin n × Bool

variable {n : Nat} [NeZero n]

/-- Dₙ の積: (rᵃsᵉ)(rᵇsᶠ) = rᵃ⁺ᵇsᶠ(e=false)、rᵃ⁻ᵇsᵉ⊕ᶠ(e=true)。 -/
def dmul (a b : Dn n) : Dn n := (if a.2 then a.1 - b.1 else a.1 + b.1, xor a.2 b.2)

/-- Dₙ の逆元。 -/
def dinv (a : Dn n) : Dn n := if a.2 then a else (-a.1, false)

/-- Dₙ の単位元。 -/
def done_ : Dn n := (0, false)

/-- Dₙ³(K3/Base.lean `E` の一般化)。 -/
abbrev En (n : Nat) : Type := Dn n × Dn n × Dn n

/-- Dₙ³ の積(成分ごと)。 -/
def emul (x y : En n) : En n := (dmul x.1 y.1, dmul x.2.1 y.2.1, dmul x.2.2 y.2.2)

/-- Dₙ³ の逆元(成分ごと)。 -/
def einv (x : En n) : En n := (dinv x.1, dinv x.2.1, dinv x.2.2)

/-- Dₙ³ の単位元。 -/
def eone : En n := (done_, done_, done_)

/-- 反射パリティ(3 成分の e-flag の xor)。G_n = ker(par) は Dₙ³ の指数 2 の部分群。 -/
def par (x : En n) : Bool := xor (xor x.1.2 x.2.1.2) x.2.2.2

/-- G_n への所属。 -/
abbrev inG (x : En n) : Prop := par x = false

/-- **補題 A の生成元 a₁,a₂,a₃**: A = ⟨a₁,a₂,a₃⟩ = ⟨r⟩³ ≤ G_n の座標生成元。
    oddH §2「$a_1:=(r,1,1),\,a_2:=(1,r,1),\,a_3:=(1,1,r)$」。 -/
def a1 : En n := ((1, false), (0, false), (0, false))
def a2 : En n := ((0, false), (1, false), (0, false))
def a3 : En n := ((0, false), (0, false), (1, false))

/-- **補題 A の生成元 q₁,q₂,q₃**: Q = {1,q₁,q₂,q₃} ≅ C₂²。
    oddH §2「$q_1:=(1,s,s),\,q_2:=(s,1,s),\,q_3:=(s,s,1)$」。 -/
def q1 : En n := (done_, (0, true), (0, true))
def q2 : En n := ((0, true), done_, (0, true))
def q3 : En n := ((0, true), (0, true), done_)

/-- marking $X = \psi_n(x) = (r,s,s) = a_1 q_1$(oddH §2)。 -/
def X : En n := emul a1 q1

/-- marking $Y = \psi_n(y) = (rs,r,rs) = a_1a_2a_3\,q_2$(oddH §2)。 -/
def Y : En n := emul (emul (emul a1 a2) a3) q2

/-- 必須の補助インスタンス(K3/Base.lean と同じ罠 — plain Lean 4 core は
    直積上の decidable 全称量化子のインスタンス合成に失敗する)。 -/
instance instDecForallProd {α β : Type} {p : α × β → Prop}
    [inst : Decidable (∀ a : α, ∀ b : β, p (a, b))] : Decidable (∀ x : α × β, p x) :=
  decidable_of_iff _ ⟨fun h x => by cases x; exact h _ _, fun h a b => h (a, b)⟩

/-! ### Symbolic group laws and the actual `G_n` subtype

The first version used only the ambient predicate `inG`.  The declarations below close that
typing gap: `Gn n` is the even-parity subtype, its operations are closed, and
`Gn_groupLaws` packages the complete group laws without importing Mathlib. -/

theorem dmul_assoc_n : ∀ a b c : Dn n, dmul (dmul a b) c = dmul a (dmul b c) := by
  intro a b c
  rcases a with ⟨a, ea⟩
  rcases b with ⟨b, eb⟩
  rcases c with ⟨c, ec⟩
  cases ea <;> cases eb <;> cases ec <;>
    apply Prod.ext <;>
      simp [dmul, fin_sub_eq_add_neg, fin_add_assoc, fin_add_comm, fin_neg_neg] <;> ac_rfl

theorem dmul_one_left_n : ∀ a : Dn n, dmul done_ a = a := by
  intro a
  rcases a with ⟨a, e⟩
  cases e <;> apply Prod.ext <;> simp [dmul, done_, fin_zero_add]

theorem dmul_one_right_n : ∀ a : Dn n, dmul a done_ = a := by
  intro a
  rcases a with ⟨a, e⟩
  cases e <;> apply Prod.ext <;> simp [dmul, done_, fin_add_zero, fin_sub_zero]

theorem dmul_inv_left_n : ∀ a : Dn n, dmul (dinv a) a = done_ := by
  intro a
  rcases a with ⟨a, e⟩
  cases e <;> apply Prod.ext <;>
    simp [dinv, dmul, done_, fin_add_left_neg, fin_sub_self]

theorem dmul_inv_right_n : ∀ a : Dn n, dmul a (dinv a) = done_ := by
  intro a
  rcases a with ⟨a, e⟩
  cases e <;> apply Prod.ext <;>
    simp [dinv, dmul, done_, fin_add_right_neg, fin_sub_self]

theorem dinv_involutive_n : ∀ a : Dn n, dinv (dinv a) = a := by
  intro a
  rcases a with ⟨a, e⟩
  cases e <;> apply Prod.ext <;> simp [dinv, fin_neg_neg]

theorem emul_assoc_n : ∀ x y z : En n, emul (emul x y) z = emul x (emul y z) := by
  intro x y z
  simp only [emul]
  rw [dmul_assoc_n, dmul_assoc_n, dmul_assoc_n]

theorem emul_one_left_n : ∀ x : En n, emul eone x = x := by
  intro x
  simp only [emul, eone]
  rw [dmul_one_left_n, dmul_one_left_n, dmul_one_left_n]

theorem emul_one_right_n : ∀ x : En n, emul x eone = x := by
  intro x
  simp only [emul, eone]
  rw [dmul_one_right_n, dmul_one_right_n, dmul_one_right_n]

theorem emul_inv_left_n : ∀ x : En n, emul (einv x) x = eone := by
  intro x
  simp only [emul, einv, eone]
  rw [dmul_inv_left_n, dmul_inv_left_n, dmul_inv_left_n]

theorem emul_inv_right_n : ∀ x : En n, emul x (einv x) = eone := by
  intro x
  simp only [emul, einv, eone]
  rw [dmul_inv_right_n, dmul_inv_right_n, dmul_inv_right_n]

theorem einv_involutive_n : ∀ x : En n, einv (einv x) = x := by
  intro x
  simp only [einv]
  rw [dinv_involutive_n, dinv_involutive_n, dinv_involutive_n]

theorem par_emul_n (x y : En n) : par (emul x y) = xor (par x) (par y) := by
  rcases x with ⟨⟨x1, ex1⟩, ⟨⟨x2, ex2⟩, ⟨x3, ex3⟩⟩⟩
  rcases y with ⟨⟨y1, ey1⟩, ⟨⟨y2, ey2⟩, ⟨y3, ey3⟩⟩⟩
  cases ex1 <;> cases ex2 <;> cases ex3 <;>
    cases ey1 <;> cases ey2 <;> cases ey3 <;> rfl

theorem par_einv_n (x : En n) : par (einv x) = par x := by
  rcases x with ⟨⟨x1, ex1⟩, ⟨⟨x2, ex2⟩, ⟨x3, ex3⟩⟩⟩
  cases ex1 <;> cases ex2 <;> cases ex3 <;> rfl

theorem inG_one_n : inG (eone : En n) := by rfl

theorem inG_mul_n {x y : En n} (hx : inG x) (hy : inG y) : inG (emul x y) := by
  change par (emul x y) = false
  change par x = false at hx
  change par y = false at hy
  rw [par_emul_n, hx, hy]
  rfl

theorem inG_inv_n {x : En n} (hx : inG x) : inG (einv x) := by
  change par (einv x) = false
  change par x = false at hx
  rw [par_einv_n, hx]

/-- The actual even-parity group carrier, not the ambient `En n`. -/
def Gn (n : Nat) [NeZero n] : Type := {x : En n // inG x}

instance : Coe (Gn n) (En n) := ⟨Subtype.val⟩

def gnOne : Gn n := ⟨eone, inG_one_n⟩

def gnMul (x y : Gn n) : Gn n := ⟨emul x.val y.val, inG_mul_n x.property y.property⟩

def gnInv (x : Gn n) : Gn n := ⟨einv x.val, inG_inv_n x.property⟩

/-- A minimal plain-Lean group law package (Mathlib's `Group` is deliberately not imported). -/
structure PlainGroupLaws (α : Type) [Mul α] [One α] [Inv α] : Prop where
  mul_assoc : ∀ a b c : α, (a * b) * c = a * (b * c)
  one_mul : ∀ a : α, 1 * a = a
  mul_one : ∀ a : α, a * 1 = a
  inv_mul : ∀ a : α, a⁻¹ * a = 1
  mul_inv : ∀ a : α, a * a⁻¹ = 1

instance : Mul (Gn n) := ⟨gnMul⟩
instance : One (Gn n) := ⟨gnOne⟩
instance : Inv (Gn n) := ⟨gnInv⟩

theorem Gn_groupLaws : PlainGroupLaws (Gn n) := by
  constructor
  · intro a b c; apply Subtype.ext; exact emul_assoc_n _ _ _
  · intro a; apply Subtype.ext; exact emul_one_left_n _
  · intro a; apply Subtype.ext; exact emul_one_right_n _
  · intro a; apply Subtype.ext; exact emul_inv_left_n _
  · intro a; apply Subtype.ext; exact emul_inv_right_n _

/-- The paper's marking really belongs to `G_n`. -/
def Xg : Gn n := ⟨X, by rfl⟩

theorem X_mem_Gn : inG (X : En n) := Xg.property
