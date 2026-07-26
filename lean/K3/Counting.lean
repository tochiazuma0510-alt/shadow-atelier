/-
K3/Counting.lean — 表 C §4.5(定理レベルの命題 = 定理 K3 §2.4 step 5 の counting 論法)。
設計書 docs/lean/K3対応表_v0.md F21(群構造の最小部分)・F24(ker χ̃ = 𝔉₀)・F26(K3_counting)。

T := Φ(GT(K^{(3)})) の具体表示(観測 N3): T ≅ Aff(Z/3) × C₂、パラメータ ((v,t), w) で
  v : Bool(false↦1, true↦2 — mod 3 の単元。1,2 はいずれも自己逆元)
  t : Fin 3(平行移動成分)
  w : Bool(第 3 成分の乗数。χ̃ の値はちょうど (v,w) の対で決まる — |ker χ̃|=3, |im χ̃|=4 と整合)
𝔉₀ = ker χ̃ = {(1,t,1) ∣ t∈Z/3}(N3 の記述通り)。

このファイルは F26 の**抽象述語版**(A : T → Prop を具体化しない — 設計書 (δ3) 忠実性ノート)を主とする。
必要な decide は T の群公理・χ̃ の準同型性・ker χ̃ = 𝔉₀ の 3 本のみ(設計書 §4.5 の見積りと一致)。
-/

import K3.Base

/-- T := Aff(Z/3) × C₂ の具体表示(N3)。((v,t), w)。 -/
abbrev T : Type := (Bool × Fin 3) × Bool

/-- v : Bool を mod 3 の単元 {1,2} の実値へ(false↦1, true↦2)。 -/
def vval (v : Bool) : Fin 3 := if v then 2 else 1

/-- T の積(N3 の合成則): (v,t)∘(v',t') = (v v', v t' + t)(Aff(Z/3))、w 成分は独立に積(C₂)。
    v-成分の積は mod 3 の単元の積であり、{1,2} の指数対応では xor と一致する
    (1·1=1, 1·2=2, 2·2=1 mod 3 ⟺ false xor false = false, false xor true = true, true xor true = false)。 -/
def mulT : T → T → T
  | ((v, t), w), ((v', t'), w') => ((xor v v', vval v * t' + t), xor w w')

/-- T の単位元((1,0),1) すなわち ((false,0),false)。 -/
def oneT : T := ((false, 0), false)

/-- T の逆元: v,w は mod 3 の単元として自己逆元(1,2 とも)なので v,w 成分は不変。
    t 成分は Aff(Z/3) の逆元公式 -v⁻¹t = -(v にあたる実値)*t。 -/
def invT : T → T
  | ((v, t), w) => ((v, -(vval v * t)), w)

/-- **F21(群公理・最小部分)**: mulT の結合律・oneT が両側単位元・invT が両側逆元であること。
    `decide +kernel`(|T|=12 なので 12³=1728 通り、瞬時)。 -/
theorem F21_assoc : ∀ x y z : T, mulT (mulT x y) z = mulT x (mulT y z) := by decide +kernel
theorem F21_one_left : ∀ x : T, mulT oneT x = x := by decide +kernel
theorem F21_one_right : ∀ x : T, mulT x oneT = x := by decide +kernel
theorem F21_inv_right : ∀ x : T, mulT x (invT x) = oneT := by decide +kernel
theorem F21_inv_left : ∀ x : T, mulT (invT x) x = oneT := by decide +kernel

/-- 円分指標 χ̃ : T → Bool × Bool(N3: (Z/12)^× ≅ C₂×C₂ の具体表示。値は (v,w) 成分そのもの)。 -/
def chiT : T → Bool × Bool
  | ((v, _), w) => (v, w)

/-- **F24**: 𝔉₀ := ker χ̃ = {(1,t,1)}(N3)。ここでは χ̃ で直接定義する
    (v=false ∧ w=false ⟺ N3 の記述する「(1,t,1) の形」)。 -/
abbrev inF0 (x : T) : Prop := chiT x = (false, false)

/-- **F24(準同型性)**: χ̃ は群準同型(Bool×Bool は xor で群)。`decide +kernel`(12×12=144 通り)。 -/
theorem F24_chiT_hom : ∀ x y : T,
    chiT (mulT x y) = (xor (chiT x).1 (chiT y).1, xor (chiT x).2 (chiT y).2) := by decide +kernel

/-- χ̃(invT x) = χ̃(x)(v,w 成分は invT で不変)。`decide +kernel`(12 通り)。 -/
theorem F24_chiT_invT : ∀ x : T, chiT (invT x) = chiT x := by decide +kernel

/-- **F24 の核心の合成事実**: χ̃(a) = χ̃(t) ⇒ invT(a)*t ∈ 𝔉₀(counting 論法の中核ステップ)。
    `decide +kernel`(12×12=144 通り、χ̃ a = χ̃ t を仮定に持つ全称)。 -/
theorem F24_ker_step : ∀ a t : T, chiT a = chiT t → inF0 (mulT (invT a) t) := by decide +kernel

/-- 群の等式 a * (a⁻¹ * t) = t(結合律 + 右逆元 + 左単位元から)。`decide +kernel`(12×12=144 通り)。 -/
theorem mulT_inv_cancel : ∀ a t : T, mulT a (mulT (invT a) t) = t := by decide +kernel

/-- **F26(counting、抽象述語版・主)**: 定理 K3 §2.4 step 5 の群論的中核。
    A : T → Prop は**具体化しない**(忠実性ノート (δ3): 論文の A = Ih(G_K) の像は
    「T の部分集合」として天下り的に与えられているわけではなく、性質で特徴づけられるべき対象)。
    仮定 hF0 は補題 P(d′)(A ∩ 𝔉₀ = 𝔉₀)、仮定 hchi は円分指標の全射性(χ̃(A) = 全体)に対応する。
    証明は構造的(5 行)— `decide` は F21/F24 に閉じ込め済み。 -/
theorem K3_counting (A : T → Prop)
    (hclosed : ∀ a b, A a → A b → A (mulT a b))
    (hF0     : ∀ a, inF0 a → A a)
    (hchi    : ∀ c : Bool × Bool, ∃ a, A a ∧ chiT a = c) :
    ∀ t : T, A t := by
  intro t
  obtain ⟨a, ha, hac⟩ := hchi (chiT t)
  have hmem : inF0 (mulT (invT a) t) := F24_ker_step a t hac
  have hA := hclosed a (mulT (invT a) t) ha (hF0 _ hmem)
  rwa [mulT_inv_cancel] at hA

#print axioms F21_assoc
#print axioms F24_chiT_hom
#print axioms F24_ker_step
#print axioms K3_counting
