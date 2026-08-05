/-
P1/Core.lean — ブロック A・E の基盤(群 G_n = A ⋊ Q、族版・n : Nat を変数のまま扱う)。

対応: docs/notes/lean_p1_allocation_plan_v1.md §3.1(ブロック A)・§3.5(ブロック E)。
出所: docs/notes/oddH_full_proof_v1.md §2「補題 A(構造補題)」。

plain Lean 4 core のみ(Mathlib 不使用)。K3/Base.lean(n=3 固定・decide 検算)の
一般化だが、ここでは n が全称量化された変数なので `decide` は使えない — 構造的な
等式証明(`rfl`/`simp`/成分ごとの計算)のみで進める。
-/

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
