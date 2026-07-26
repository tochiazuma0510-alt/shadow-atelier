/-
K3/Conjugator.lean — 表 C §4.5、F29(裁定 28 で保留解除)。
設計書 docs/lean/K3対応表_v0.md F29 行(v1.1・訂正済み)のとおり実装する。

正典値(訂正後): h = [2,3,5,6,4,1](one-line・1-indexed)で
  h x̄ h⁻¹ = σ₀、h ȳ h⁻¹ = σ₁、h z̄ h⁻¹ = σ∞ (第 3 式は独立検査)
かつ S₆ 内で一意(720 個の悉皆で解ちょうど 1 個)。

規約(F29 行 (i)(ii)(iii))を厳密に守る:
  (i)  x̄,ȳ,z̄ は `search/week4-19a19e.mjs` の代表 good[0] の剰余類 6 点への左作用
       x̄=[2,5,4,6,3,1]、ȳ=[1,3,2,5,4,6]、z̄=[6,1,4,2,3,5](型 (6,2²1²,6)、x̄ȳz̄=id)
  (ii) σ 三つ組は 6T9 の辞書式最小代表を λ 割当に揃えたもの
       σ₀=[2,3,4,5,6,1]、σ₁=[1,2,5,6,3,4]、σ∞=[4,1,2,5,6,3]
  (iii) 合成は左作用 (p∘q)(i)=p(q(i))、共役は h x h⁻¹

**リテラル pin**(design (δ1)): 6 点のラベル付けは任意で、剰余類からの再導出は禁止
(別のラベル付けでは h も変わる)。ここではすべて `Fin 6 → Fin 6` の明示パターンマッチで
pin する(`Marking.lean` と同型の流儀、0-indexed = 1-indexed の値から 1 を引いたもの)。

plain Lean 4 core のみ(Mathlib 不使用)。
-/

/-- x̄(good[0] の剰余類表現、0-indexed)。1-indexed [2,5,4,6,3,1] より。 -/
def xbar : Fin 6 → Fin 6
  | 0 => 1 | 1 => 4 | 2 => 3 | 3 => 5 | 4 => 2 | 5 => 0

/-- ȳ。1-indexed [1,3,2,5,4,6] より。 -/
def ybar : Fin 6 → Fin 6
  | 0 => 0 | 1 => 2 | 2 => 1 | 3 => 4 | 4 => 3 | 5 => 5

/-- z̄。1-indexed [6,1,4,2,3,5] より。 -/
def zbar : Fin 6 → Fin 6
  | 0 => 5 | 1 => 0 | 2 => 3 | 3 => 1 | 4 => 2 | 5 => 4

/-- σ₀(6T9 標準代表、λ 割当済み)。1-indexed [2,3,4,5,6,1] より。 -/
def sigma0 : Fin 6 → Fin 6
  | 0 => 1 | 1 => 2 | 2 => 3 | 3 => 4 | 4 => 5 | 5 => 0

/-- σ₁。1-indexed [1,2,5,6,3,4] より。 -/
def sigma1 : Fin 6 → Fin 6
  | 0 => 0 | 1 => 1 | 2 => 4 | 3 => 5 | 4 => 2 | 5 => 3

/-- σ∞。1-indexed [4,1,2,5,6,3] より。 -/
def sigmaInf : Fin 6 → Fin 6
  | 0 => 3 | 1 => 0 | 2 => 1 | 3 => 4 | 4 => 5 | 5 => 2

/-- 正典の exact conjugator h。1-indexed [2,3,5,6,4,1] より(裁定 28 で確定した訂正値)。 -/
def hperm : Fin 6 → Fin 6
  | 0 => 1 | 1 => 2 | 2 => 4 | 3 => 5 | 4 => 3 | 5 => 0

/-- h の明示逆写像(h⁻¹)。 -/
def hinv : Fin 6 → Fin 6
  | 0 => 5 | 1 => 0 | 2 => 1 | 3 => 4 | 4 => 2 | 5 => 3

/-- h⁻¹ は h の両側逆(`decide`、瞬時)。 -/
theorem hinv_left : ∀ i : Fin 6, hinv (hperm i) = i := by decide
theorem hinv_right : ∀ i : Fin 6, hperm (hinv i) = i := by decide

/-- **F29(共役等式・1 本目)**: h x̄ h⁻¹ = σ₀。 -/
theorem F29_conj_x : ∀ i : Fin 6, hperm (xbar (hinv i)) = sigma0 i := by decide

/-- **F29(共役等式・2 本目)**: h ȳ h⁻¹ = σ₁。 -/
theorem F29_conj_y : ∀ i : Fin 6, hperm (ybar (hinv i)) = sigma1 i := by decide

/-- **F29(共役等式・3 本目、独立検査)**: h z̄ h⁻¹ = σ∞。 -/
theorem F29_conj_z : ∀ i : Fin 6, hperm (zbar (hinv i)) = sigmaInf i := by decide

/-- (i) の付帯確認: x̄ȳz̄ = id(左作用合成)。 -/
theorem F29_marking : ∀ i : Fin 6, xbar (ybar (zbar i)) = i := by decide

/-! ### 一意性(S₆ = 720 個の悉皆) -/

/-- a を並べ替えリストの全位置に挿入する(標準的な permutations アルゴリズム、
    plain Lean 4 core に `List.permutations` が無いための自前実装)。 -/
def insertAt {α : Type} (a : α) : List α → List (List α)
  | [] => [[a]]
  | b :: bs => (a :: b :: bs) :: (insertAt a bs).map (b :: ·)

/-- リストの全順列(構造的再帰・停止は `rest`/`bs` が真に短くなることから)。 -/
def permsOf {α : Type} : List α → List (List α)
  | [] => [[]]
  | a :: rest => (permsOf rest).flatMap (insertAt a)

/-- Fin 6 の基準リスト [0,1,2,3,4,5]。 -/
def base6 : List (Fin 6) := [0, 1, 2, 3, 4, 5]

/-- S₆ の全 720 元(one-line 表記のリストとして)。 -/
def allPerms6 : List (List (Fin 6)) := permsOf base6

/-- allPerms6 は本当に 720 個(順列生成が正しく機能していることの確認)。 -/
theorem allPerms6_card : allPerms6.length = 720 := by decide +kernel

/-- リスト表現の順列を関数として評価する(添字 i の像は p の i 番目の値)。 -/
def toFun (p : List (Fin 6)) : Fin 6 → Fin 6 := fun i => p.getD i.val 0

/-- 候補 p が「g x̄ = σ₀ g ∧ g ȳ = σ₁ g」(= g x̄ g⁻¹ = σ₀ ∧ g ȳ g⁻¹ = σ₁ の同値な書き換え、
    g⁻¹ を経由しないので任意の順列リストにそのまま適用できる)を満たすかを判定する。 -/
def matchesCandidate (p : List (Fin 6)) : Bool :=
  decide (∀ i : Fin 6, toFun p (xbar i) = sigma0 (toFun p i)) &&
  decide (∀ i : Fin 6, toFun p (ybar i) = sigma1 (toFun p i))

/-- h の one-line リスト表現(hperm と同じ値)。 -/
def hList : List (Fin 6) := [1, 2, 4, 5, 3, 0]

/-- **F29(一意性)**: S₆(720 元)の中で「g x̄ g⁻¹ = σ₀ ∧ g ȳ g⁻¹ = σ₁」を満たす順列は
    ちょうど 1 個で、それは h(= hList)である。`decide +kernel`(720 候補 × 12 評価、瞬時)。 -/
theorem F29_unique : allPerms6.filter matchesCandidate = [hList] := by decide +kernel

/-- hList は実際に hperm と同じ関数を表す(toFun の整合性確認)。 -/
theorem F29_hList_eq_hperm : ∀ i : Fin 6, toFun hList i = hperm i := by decide

#print axioms hinv_left
#print axioms hinv_right
#print axioms F29_conj_x
#print axioms F29_conj_y
#print axioms F29_conj_z
#print axioms F29_marking
#print axioms allPerms6_card
#print axioms F29_unique
#print axioms F29_hList_eq_hperm
