/-
K3/Struct.lean — 表 C §4.4(群構造 T と χ̃)の残り。設計書 docs/lean/K3対応表_v0.md F22・F23。
Phase 1(K3/Counting.lean)は F21(群公理の最小部分)・F24(ker χ̃ = 𝔉₀)のみ実装済みだったため、
T ≅ Aff(Z/3)×C₂ ≅ S₃×C₂ の独立確認(位数の多重集合・中心の位数)と、
χ̃(m,k)=2m+1 が 𝒳₃ → (Z/12)^× の全単射であることを Phase 2 として実装する。
-/

import K3.Base
import K3.Group
import K3.Shadows
import K3.Counting

/-! ### F23: χ̃(m,k) = 2m+1 は 𝒳₃ → (Z/12)^× の全単射 -/

/-- Nat を Fin 12 へ(mod 12)。 -/
def toFin12 (n : Nat) : Fin 12 := ⟨n % 12, Nat.mod_lt n (by decide)⟩

/-- 円分指標の値 χ̃(m) := 2m+1 mod 12(D1 の記法どおり、m ∈ 𝒳₃ = {0,2,3,5})。 -/
def chiVal (m : Fin 6) : Fin 12 := toFin12 (2 * m.val + 1)

/-- (Z/12)^× = {1,5,7,11}。 -/
def Z12x : List (Fin 12) := [1, 5, 7, 11]

/-- **F23**: χ̃ は 𝒳₃ = [0,2,3,5] を順序どおり (Z/12)^× = [1,5,7,11] へ移す
    (単一の list 等式が単射性(相異なる入力→相異なる出力)と全射性(像が Z12x を尽くす)を
    同時に保証する — 両側とも 4 元のリストであることから)。`decide`(瞬時)。 -/
theorem F23_chiVal_bij : X3.map chiVal = Z12x := by decide

/-! ### F22: T ≅ Aff(Z/3) × C₂ ≅ S₃ × C₂(位数の多重集合・中心の位数) -/

/-- Bool の全 2 元。 -/
def allBool : List Bool := [false, true]
/-- Fin 3 の全 3 元。 -/
def allFin3 : List (Fin 3) := [0, 1, 2]

/-- T = (Bool×Fin3)×Bool の全 12 元。 -/
def allT : List T := allBool.flatMap (fun v => allFin3.flatMap (fun t => allBool.map (fun w => ((v, t), w))))

theorem allT_complete : ∀ x : T, x ∈ allT := by decide +kernel

/-- x の位数(1,2,3 を明示的に判定し、それ以外は 6 と暫定する — 正当性は
    `F22_order6_check` で x⁶=1 を確認することにより閉じる)。 -/
def ordT (x : T) : Nat :=
  if x = oneT then 1
  else if mulT x x = oneT then 2
  else if mulT (mulT x x) x = oneT then 3
  else 6

/-- **F22(位数の多重集合)**: T の 12 元の位数の内訳は [1, 2×7, 3×2, 6×2](正典 Thm 4.6 の
    独立確認)。`decide +kernel`(12 元のフィルタ、瞬時)。 -/
theorem F22_order_counts :
    (allT.filter (fun x => decide (ordT x = 1))).length = 1 ∧
    (allT.filter (fun x => decide (ordT x = 2))).length = 7 ∧
    (allT.filter (fun x => decide (ordT x = 3))).length = 2 ∧
    (allT.filter (fun x => decide (ordT x = 6))).length = 2 := by decide +kernel

/-- **F22(位数 6 の正当性)**: `ordT x = 6` と判定された元は実際に x⁶ = 1 を満たす
    (位数が 1,2,3 のいずれでもなく、かつ 12 の約数であるという構造的事実と合わせて、
    真に位数 6 であることを保証する)。 -/
theorem F22_order6_check : ∀ x : T, ordT x = 6 →
    mulT (mulT (mulT (mulT (mulT x x) x) x) x) x = oneT := by decide +kernel

/-- Aff(Z/3) = Bool×Fin3(T の第 1 成分だけの群構造)の積。 -/
def mulAff : Bool × Fin 3 → Bool × Fin 3 → Bool × Fin 3
  | (v, t), (v', t') => (xor v v', vval v * t' + t)
/-- Aff(Z/3) の単位元。 -/
def oneAff : Bool × Fin 3 := (false, 0)

/-- Aff(Z/3) の元の位数(6 元しかないので 1,2,3 を判定すれば残りは全部 3 or 6 だが、
    ここでは S₃(位数 6 の非可換群)であることの確認として使う)。 -/
def ordAff (x : Bool × Fin 3) : Nat :=
  if x = oneAff then 1
  else if mulAff x x = oneAff then 2
  else 3

/-- Aff(Z/3) の全 6 元。 -/
def allAff : List (Bool × Fin 3) := allBool.flatMap (fun v => allFin3.map (fun t => (v, t)))

/-- **F22(Aff(Z/3) ≅ S₃ の同定)**: Aff(Z/3) の位数の内訳は [1, 2×3, 3×2] — これは
    位数 6 の群としては S₃ に固有のプロファイル(C₆ なら [1,2,3×2,6×2] になり一致しない)。
    ゆえに Aff(Z/3) ≅ S₃(位数 6 の群の同型類は位数の多重集合で尽くされる)。 -/
theorem F22_Aff_is_S3 :
    (allAff.filter (fun x => decide (ordAff x = 1))).length = 1 ∧
    (allAff.filter (fun x => decide (ordAff x = 2))).length = 3 ∧
    (allAff.filter (fun x => decide (ordAff x = 3))).length = 2 := by decide +kernel

/-- **F22(位数 3 の正当性)**: `ordAff x = 3` と判定された元は実際に x³ = 1 を満たす。 -/
theorem F22_Aff_order3_check : ∀ x : Bool × Fin 3, ordAff x = 3 →
    mulAff (mulAff x x) x = oneAff := by decide +kernel

/-- T の中心への所属。`abbrev` にして `decide` のインスタンス探索が透過するようにする
    (K3/Base.lean の `inG` と同じ流儀)。 -/
abbrev inCenterT (z : T) : Prop := ∀ x : T, mulT z x = mulT x z

/-- **F22(中心の位数 = 2)**: Z(T) はちょうど 2 元。`decide +kernel`(12×12=144 通り)。 -/
theorem F22_center_card :
    (allT.filter (fun x => decide (inCenterT x))).length = 2 := by decide +kernel

#print axioms F23_chiVal_bij
#print axioms F22_order_counts
#print axioms F22_order6_check
#print axioms F22_Aff_is_S3
#print axioms F22_Aff_order3_check
#print axioms F22_center_card
