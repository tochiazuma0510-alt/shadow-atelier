/-
K3/Group.lean — 表 C §4.1(基盤)。設計書 docs/lean/K3対応表_v0.md F1・F2・F4・F5・F6。
Phase 1(Base/Shadows/Counting/Lambda)には無かった D₃・D₃³ の群公理・パリティ準同型・
|G₃|=108・G₃=⟨x̄,ȳ⟩ の明示分解を実装する(Phase 2)。

plain Lean 4 core のみ(Mathlib 不使用)。
-/

import K3.Base

/-- 正典の生成元 r = r¹s⁰(回転)。 -/
def r : D := (1, false)
/-- 正典の生成元 s = r⁰s¹(鏡映)。 -/
def sD : D := (0, true)

/-- **F1(結合律)**: D₃ の積 `dmul` は結合的。`decide +kernel`(6³=216 通り)。 -/
theorem dmul_assoc : ∀ a b c : D, dmul (dmul a b) c = dmul a (dmul b c) := by decide +kernel

/-- **F1(単位元)**: `done` は両側単位元。`decide`(6 通り)。 -/
theorem dmul_one_left : ∀ a : D, dmul done a = a := by decide
theorem dmul_one_right : ∀ a : D, dmul a done = a := by decide

/-- **F1(逆元)**: `dinv` は両側逆元。`decide`(6 通り)。 -/
theorem dmul_inv_left : ∀ a : D, dmul (dinv a) a = done := by decide
theorem dmul_inv_right : ∀ a : D, dmul a (dinv a) = done := by decide

/-- **F1(表示関係式)**: r³ = 1(正典 D₃ = ⟨r,s ∣ r³, s², srs⁻¹r⟩ の第 1 関係式)。 -/
theorem F1_rel_r3 : dmul (dmul r r) r = done := by decide

/-- **F1(表示関係式)**: s² = 1。 -/
theorem F1_rel_s2 : dmul sD sD = done := by decide

/-- **F1(表示関係式)**: srs⁻¹r = 1。s は対合ゆえ s⁻¹ = s(`dinv sD = sD`、`decide` で確認可)なので
    literal には `dmul (dmul sD r) sD` の代わりに `dinv sD` を明示的に使う。 -/
theorem F1_rel_srsr : dmul (dmul (dmul sD r) (dinv sD)) r = done := by decide

/-- D₃³ の第 2 成分の反射フラグは xor で決まる(`dmul` の定義そのもの・F4/F2 双方の土台)。
    `decide`(2×2=4 通り、事実上 `rfl`)。 -/
theorem dmul_flag : ∀ a b : D, (dmul a b).2 = xor a.2 b.2 := by decide

/-- **F2(結合律)**: `emul` は結合的。構造的証明(F1 の `dmul_assoc` を成分ごとに 3 回適用)。
    216³ 通りの直接 `decide` は設計書 §1.3 により不可能なため、成分に落とす。 -/
theorem F2_assoc : ∀ x y z : E, emul (emul x y) z = emul x (emul y z) := by
  intro x y z
  simp only [emul]
  rw [dmul_assoc, dmul_assoc, dmul_assoc]

/-- **F2(単位元)**: `eone` は `emul` の両側単位元。構造的(F1 の `dmul_one_left/right` を 3 回)。 -/
theorem F2_one_left : ∀ x : E, emul eone x = x := by
  intro x
  simp only [emul, eone]
  rw [dmul_one_left, dmul_one_left, dmul_one_left]

theorem F2_one_right : ∀ x : E, emul x eone = x := by
  intro x
  simp only [emul, eone]
  rw [dmul_one_right, dmul_one_right, dmul_one_right]

/-- **F2(逆元)**: `einv` は `emul` の両側逆元。構造的(F1 の `dmul_inv_left/right` を 3 回)。 -/
theorem F2_inv_left : ∀ x : E, emul (einv x) x = eone := by
  intro x
  simp only [emul, einv, eone]
  rw [dmul_inv_left, dmul_inv_left, dmul_inv_left]

theorem F2_inv_right : ∀ x : E, emul x (einv x) = eone := by
  intro x
  simp only [emul, einv, eone]
  rw [dmul_inv_right, dmul_inv_right, dmul_inv_right]

/-- **F4(パリティは準同型)**: `par (emul x y) = xor (par x) (par y)`。構造的証明
    (`dmul_flag` を 3 回 + 6 個の bool 変数の場合分け・`rfl` で閉じる)。
    設計書 §4.1 は `decide +kernel`(216² = 46656、実測 13 秒)を挙げるが、
    ここでは成分の bool 代数に落として `decide` すら経ずに閉じる(F20_preserves_par と同型の手法)。 -/
theorem F4_par_hom : ∀ x y : E, par (emul x y) = xor (par x) (par y) := by
  intro x y
  simp only [par, emul, dmul_flag]
  cases x.1.2 <;> cases x.2.1.2 <;> cases x.2.2.2 <;> cases y.1.2 <;> cases y.2.1.2 <;>
    cases y.2.2.2 <;> rfl

/-- D のすべての元(6 元)の明示列挙。`decide` によるリスト計算(F5・F6 の土台)。 -/
def allD : List D := [(0, false), (1, false), (2, false), (0, true), (1, true), (2, true)]

/-- `allD` が実際に D の全 6 元を尽くすこと(重複なく列挙されていること)の確認。 -/
theorem allD_complete : ∀ x : D, x ∈ allD := by decide

/-- E = D³ のすべての元(216 元)の明示列挙(3 重直積)。 -/
def allE : List E := allD.flatMap (fun a => allD.flatMap (fun b => allD.map (fun c => (a, b, c))))

theorem allE_complete : ∀ x : E, x ∈ allE := by decide +kernel

/-- **F5**: |G₃| = 108(`allE` を `inG` でフィルタした長さ)。純計算(量化子なし)なので
    `decide`(`+kernel` を既定として使う)で瞬時に閉じる。 -/
theorem F5_card_G3 : (allE.filter (fun x => decide (inG x))).length = 108 := by decide +kernel

/-- J の生成元 x̄² (位数 3、`⟨x̄²⟩` の生成元)。 -/
def xb2 : E := emul xb xb
/-- J の生成元 ȳ²。 -/
def yb2 : E := emul yb yb
/-- x̄ȳ(正典 F6 のコセット代表列に使う元、かつ (x̄ȳ)⁴ が J の第 3 生成元)。 -/
def xyE : E := emul xb yb
/-- (x̄ȳ)⁴ = (x̄ȳ)² * (x̄ȳ)²。 -/
def xy4 : E := emul (emul xyE xyE) (emul xyE xyE)

/-- g の a 乗(a : Fin 3、g は位数 3 の元を想定 — xb2, yb2, xy4 に適用する)。 -/
def pow3 (g : E) (a : Fin 3) : E :=
  match a with
  | 0 => eone
  | 1 => g
  | 2 => emul g g

/-- x̄²,ȳ²,(x̄ȳ)⁴ はいずれも位数を割り切る(³乗すると単位元に戻る)ことの確認
    — `pow3` が実際に群としての冪と一致することの土台。`decide`(3 元、瞬時)。 -/
theorem xb2_cubed : emul (emul xb2 xb2) xb2 = eone := by decide +kernel
theorem yb2_cubed : emul (emul yb2 yb2) yb2 = eone := by decide +kernel
theorem xy4_cubed : emul (emul xy4 xy4) xy4 = eone := by decide +kernel

/-- **F6 のコセット代表**: [1, x̄, ȳ, x̄ȳ]([J : G₃] = 4 の代表系、正典 p.15)。 -/
def cosetReps : List E := [eone, xb, yb, xyE]

/-- **F6**: G₃ = ⟨x̄,ȳ⟩ の明示分解 — 任意の v ∈ G₃ は
    (x̄²)^a (ȳ²)^b ((x̄ȳ)⁴)^c · w(a,b,c ∈ Fin 3、w はコセット代表 4 個のいずれか)の形に書ける。
    `decide +kernel`(v : E(216) に対し a,b,c(27通り)×w(4通り)=108 通りの一致判定 = 総計約 23328 通り)。 -/
theorem F6_G3_gen : ∀ v : E, inG v ↔
    ∃ a : Fin 3, ∃ b : Fin 3, ∃ c : Fin 3, ∃ w ∈ cosetReps,
      v = emul (emul (emul (pow3 xb2 a) (pow3 yb2 b)) (pow3 xy4 c)) w := by
  decide +kernel

#print axioms F1_rel_r3
#print axioms F1_rel_s2
#print axioms F1_rel_srsr
#print axioms F2_assoc
#print axioms F2_one_left
#print axioms F2_one_right
#print axioms F2_inv_left
#print axioms F2_inv_right
#print axioms F4_par_hom
#print axioms F5_card_G3
#print axioms F6_G3_gen
