/-
K3/Base.lean — 型・基盤 (定理 K3 の Lean 形式化・設計書 docs/lean/K3対応表_v0.md §1.2 の採用方式 (i))。

正典 arXiv 2405.11725 (D1) の記法:
  D₃ := ⟨r,s ∣ r³, s², srs⁻¹r⟩(元 r^a s^e を (a,e) : Fin 3 × Bool で表す)
  G₃ := ⟨(r,s,s), (rs,r,rs)⟩ ≤ D₃³ = ker(parity)  (D1 §3, marking (3.6))

plain Lean 4 core のみ(Mathlib 不使用・8GB RAM 制約)。群公理は明示的な `Monoid`/`Group` インスタンスとしては
構成せず(`lean/Marking.lean` の先例と同じ流儀)、`decide` / `decide +kernel` で必要な等式・関係式のみ検算する。
-/

/-- D₃ の元 r^a s^e を (a, e) で表す。 -/
abbrev D : Type := Fin 3 × Bool

/-- D₃³(位数 216)。正典 D1 (3.1) の値域。 -/
abbrev E : Type := D × D × D

/-- D₃ の積: (r^a s^e)(r^b s^f) = r^{a+b} s^f (e=false), r^{a-b} s^{e xor f} (e=true)。 -/
def dmul (a b : D) : D := (if a.2 then a.1 - b.1 else a.1 + b.1, xor a.2 b.2)

/-- D₃ の逆元: 回転は符号反転、鏡映は自分自身(対合)。 -/
def dinv (a : D) : D := if a.2 then a else (-a.1, false)

/-- D₃ の単位元 r⁰。 -/
def done : D := (0, false)

/-- D₃³ の積(成分ごと)。 -/
def emul (x y : E) : E := (dmul x.1 y.1, dmul x.2.1 y.2.1, dmul x.2.2 y.2.2)

/-- D₃³ の逆元(成分ごと)。 -/
def einv (x : E) : E := (dinv x.1, dinv x.2.1, dinv x.2.2)

/-- D₃³ の単位元。 -/
def eone : E := (done, done, done)

/-- 反射パリティ(3 成分の e-flag の xor)。G₃ = ker(par) は指数 2 の部分群。 -/
def par (x : E) : Bool := xor (xor x.1.2 x.2.1.2) x.2.2.2

/-- G₃ への所属(par x = false)。`abbrev` にして `decide` のインスタンス探索が透過するようにする。 -/
abbrev inG (x : E) : Prop := par x = false

/-- 正典 D1 (3.6): x̄ = (r,s,s)。 -/
def xb : E := ((1, false), (0, true), (0, true))
/-- 正典 D1 (3.6): ȳ = (rs,r,rs)。 -/
def yb : E := ((1, true), (1, false), (1, true))
/-- 正典 D1 (3.6): z̄ = (r²s, r⁻¹s, r) = (r²s, r²s, r)(r⁻¹=r² in Z/3)。 -/
def zb : E := ((2, true), (2, true), (1, false))

/-- F3(marking 関係式): x̄ȳz̄ = 1。 -/
theorem F3_marking : emul (emul xb yb) zb = eone := by decide +kernel

/-- F3(位数): x̄, ȳ, z̄ はいずれも位数 6(ここでは x̄⁶=1 かつ x̄²≠1,x̄³≠1 のみ検算・十分条件)。 -/
theorem F3_order_xb : emul (emul (emul xb xb) (emul xb xb)) (emul xb xb) = eone ∧
    emul xb xb ≠ eone ∧ emul (emul xb xb) xb ≠ eone := by decide +kernel

/-- **必須の補助インスタンス**(design 書 §1.2): plain Lean 4 core には直積上の
    decidable 全称量化子のインスタンス合成が(素朴には)失敗するため、明示的に与える。 -/
instance instDecForallProd {α β : Type} {p : α × β → Prop}
    [inst : Decidable (∀ a : α, ∀ b : β, p (a, b))] : Decidable (∀ x : α × β, p x) :=
  decidable_of_iff _ ⟨fun h x => by cases x; exact h _ _, fun h a b => h (a, b)⟩

/-- 直積上の decidable 存在量化子(上と対の補助インスタンス。K3/Lambda.lean の
    `∃ c : D, …`(D = Fin 3 × Bool)型の命題で必要になる)。 -/
instance instDecExistsProd {α β : Type} {p : α × β → Prop}
    [inst : Decidable (∃ a : α, ∃ b : β, p (a, b))] : Decidable (∃ x : α × β, p x) :=
  decidable_of_iff (∃ a : α, ∃ b : β, p (a, b))
    ⟨fun h => match h with | ⟨a, b, hp⟩ => ⟨(a, b), hp⟩,
     fun h => match h with | ⟨⟨a, b⟩, hp⟩ => ⟨a, b, hp⟩⟩

/-- x̄ の j 乗(j : Fin 6, x̄ の位数は 6)。Λ 上の τ 作用(K3/Lambda.lean)で使う。
    明示的な繰り返し積(`Marking.lean` の Fin パターンマッチの流儀)。 -/
def epow6 (x : E) (j : Fin 6) : E :=
  match j with
  | 0 => eone
  | 1 => x
  | 2 => emul x x
  | 3 => emul (emul x x) x
  | 4 => emul (emul x x) (emul x x)
  | 5 => emul (emul (emul x x) (emul x x)) x
