/-
K3/Lambda.lean — 表 C §4.2/§4.4 の一部(F25)+ v3 §5.2.3 の単発検算の恒久化(F32)。
設計書 docs/lean/K3対応表_v0.md §4.7 の推奨(「F25 の実装時に F32 として一緒に入れる」)に従う。

出所: docs/week4-K3飽和_opus_v3.md §5.2.3(逐語): "(E) Φ_{0,k}(x̄) = x̄、(G) ρ_Λ(𝔉₀) ⊆ τ(μ₆)、
(H) ρ_Λ(𝔉₀) = τ(μ₆[3]) = ⟨τ²⟩、(I) ρ_Λ(𝔉₀) の各元は τ と可換"、および観測 N2/N4(設計書 §3)。

ここでの Λ の表示: Λ = {H_c ∣ c ∈ D₃}(N2、H_c := {v ∈ E ∣ v₂∈⟨r⟩, v₃ = c v₁ c⁻¹})なので、
Λ を D(6 元)で添字づける。ρ_Λ, τ の定義は「conjugation action が H_c を H_{c'} に写す」という
事実そのものを Lean 内で decide 検証してから ρ_Λ/τ の閉形として採用する(F10 を外部から輸入せず、
本ファイル内で自己完結的に正当化する — 実装上の選択。詳細は実装報告の逸脱ノートを参照)。
-/

import K3.Base
import K3.Shadows

/-- H_c := {v ∈ E ∣ v₂ ∈ ⟨r⟩(反射でない), v₃ = c v₁ c⁻¹}(N2)。Λ = {H_c ∣ c ∈ D}。 -/
abbrev inHc (c : D) (v : E) : Prop :=
  v.2.1.2 = false ∧ v.2.2 = dmul (dmul c v.1) (dinv c)

/-- H := H_{c=1}(N2 の基準元。標的部分群そのもの)。 -/
abbrev inH (v : E) : Prop := inHc done v

/-- (r^k,1,1) ∈ E(𝔉₀ = Φ_{0,k} を実現する内部自己同型の共役元、観測 N4)。 -/
def g0 (k : Fin 3) : E := ((k, false), done, done)

/-- **N4 の直接検算**: Φ_{0,k} は (r^k,1,1) による共役(内部自己同型)そのものである。
    `decide +kernel`(k:Fin3(3) × v:E(216) = 648 通り)。 -/
theorem N4_Phicf0_is_conj :
    ∀ k : Fin 3, ∀ v : E, Phicf 0 k v = emul (emul (g0 k) v) (einv (g0 k)) := by decide +kernel

/-- ρ_Λ(Φ_{0,k}) の Λ = D 上の作用(H_c ↦ H_{c·r⁻ᵏ})。 -/
def rhoF0 (k : Fin 3) (c : D) : D := dmul c (dinv (k, false))

/-- **rhoF0 の正当化**: (r^k,1,1) による共役は H_c を H_{ρF0(k,c)} へ写す(N2 の共役則の
    この特殊ケースを自己完結的に decide 検証する — F10 を外部から仮定しない)。
    `decide +kernel`(k(3)×c(6)×v(216) = 3888 通り)。 -/
theorem rhoF0_conj_correct :
    ∀ k : Fin 3, ∀ c : D, ∀ v : E,
      inHc c v ↔ inHc (rhoF0 k c) (emul (emul (g0 k) v) (einv (g0 k))) := by decide +kernel

/-- τ(ζ₆ʲ) の Λ = D 上の作用(H_c ↦ H_{(x̄ʲ)₃ c (x̄ʲ)₁⁻¹}、v3 §5.2.3 の τ の定義)。 -/
def tauAct (j : Fin 6) (c : D) : D := dmul (dmul (epow6 xb j).2.2 c) (dinv (epow6 xb j).1)

/-- **tauAct の正当化**: x̄ʲ による共役は H_c を H_{τ(j,c)} へ写す(rhoF0_conj_correct と同型の
    自己完結的な decide 検証)。`decide +kernel`(j(6)×c(6)×v(216) = 7776 通り)。 -/
theorem tauAct_conj_correct :
    ∀ j : Fin 6, ∀ c : D, ∀ v : E,
      inHc c v ↔ inHc (tauAct j c) (emul (emul (epow6 xb j) v) (einv (epow6 xb j))) := by
  decide +kernel

/-- μ₆[3](位数 3 の部分群、⟨τ²⟩ = {0,2,4} ⊂ Fin 6)。 -/
def mu6_3 : List (Fin 6) := [0, 2, 4]

/-- **F32(E)**: Φ_{0,k}(x̄) = x̄ がすべての k で成り立つ(v3 §5.2.3 (E))。 -/
theorem F32_E : ∀ k : Fin 3, Phicf 0 k xb = xb := by decide +kernel

/-- **F32(G)**: ρ_Λ(𝔉₀) ⊆ τ(μ₆)(v3 §5.2.3 (G))。各 k について、すべての c で一致する j が存在。 -/
theorem F32_G : ∀ k : Fin 3, ∃ j : Fin 6, ∀ c : D, rhoF0 k c = tauAct j c := by decide +kernel

/-- **F32(H)**: ρ_Λ(𝔉₀) = τ(μ₆[3]) = ⟨τ²⟩(v3 §5.2.3 (H))。⊆ と ⊇ の両方向。 -/
theorem F32_H_subset : ∀ k : Fin 3, ∃ j ∈ mu6_3, ∀ c : D, rhoF0 k c = tauAct j c := by
  decide +kernel

theorem F32_H_superset : ∀ j ∈ mu6_3, ∃ k : Fin 3, ∀ c : D, tauAct j c = rhoF0 k c := by
  decide +kernel

/-- **F32(I)**: ρ_Λ(𝔉₀) の各元は τ の像の各元と可換(v3 §5.2.3 (I))。
    `decide +kernel`(k(3)×j(6)×c(6) = 108 通り)。 -/
theorem F32_I : ∀ k : Fin 3, ∀ j : Fin 6, ∀ c : D, rhoF0 k (tauAct j c) = tauAct j (rhoF0 k c) := by
  decide +kernel

/-- **F25(前半・忠実性)**: k ↦ ρ_Λ(Φ_{0,k}) は単射(𝔉₀ は Λ 上で忠実)。 -/
theorem F25_faithful : ∀ k1 k2 : Fin 3, (∀ c : D, rhoF0 k1 c = rhoF0 k2 c) → k1 = k2 := by
  decide +kernel

/-- **F25(中盤・不動点なし)**: 𝔉₀ の非自明元(k≠0)は Λ 上に不動点を持たない。 -/
theorem F25_fixed_point_free : ∀ k : Fin 3, k ≠ 0 → ∀ c : D, rhoF0 k c ≠ c := by decide +kernel

/-- 3 回合成で恒等(位数 3 であることの前半)。`decide +kernel`(k(3)×c(6) = 18 通り)。 -/
theorem F25_order3_cubed : ∀ k : Fin 3, ∀ c : D, rhoF0 k (rhoF0 k (rhoF0 k c)) = c := by
  decide +kernel

/-- rhoF0 は k について加法的(Fin 3 上の平行移動の合成則)。`decide +kernel`(3×3×6=54 通り)。 -/
theorem rhoF0_comp : ∀ k1 k2 : Fin 3, ∀ c : D, rhoF0 k1 (rhoF0 k2 c) = rhoF0 (k1 + k2) c := by
  decide +kernel

/-- k ≠ 0 ⇒ k+k ≠ 0(Fin 3 は体なので 2 は単元)。`decide`(3 通り)。 -/
theorem two_mul_ne_zero : ∀ k : Fin 3, k ≠ 0 → k + k ≠ 0 := by decide

/-- **F25(後半・位数 3)**: 𝔉₀ の非自明元は Λ 上で位数 3 の置換として作用する
    (3 乗で恒等・自身も 2 乗も非自明)。∃ の部分は F25_fixed_point_free(全称)から具体的な証人
    `done` を渡して直接構成する — `∃`+`decide`+`Fin` の組が(本実装で新たに確認した通り)
    `Quot.sound` を要求する core ライブラリの挙動があるため、それを避けるための選択(詳細は実装報告の逸脱ノートを参照)。 -/
theorem F25_order3 : ∀ k : Fin 3, k ≠ 0 →
    (∀ c, rhoF0 k (rhoF0 k (rhoF0 k c)) = c) ∧
    (∃ c, rhoF0 k c ≠ c) ∧ (∃ c, rhoF0 k (rhoF0 k c) ≠ c) := by
  intro k hk
  refine ⟨F25_order3_cubed k, ⟨done, F25_fixed_point_free k hk done⟩, ⟨done, ?_⟩⟩
  rw [rhoF0_comp]
  exact F25_fixed_point_free (k + k) (two_mul_ne_zero k hk) done

#print axioms N4_Phicf0_is_conj
#print axioms rhoF0_conj_correct
#print axioms tauAct_conj_correct
#print axioms F32_E
#print axioms F32_G
#print axioms F32_H_subset
#print axioms F32_H_superset
#print axioms F32_I
#print axioms F25_faithful
#print axioms F25_fixed_point_free
#print axioms F25_order3
