/-
K3/Bridge.lean — Lean 忠実性監査(docs/lean/K3対応表_監査_opus_v1.md)の指摘修理。

監査は「Lean にある主張は全部真・Lean に無い橋渡し命題も全部真(独立検算 25/25 PASS、
scratchpad/audit-k3lean.mjs)」と結論しており、本ファイルはその欠落を Lean 定理として埋める。
既存ファイル(Base/Group/Shadows/Counting/Struct/CountingFull/Lambda/LambdaFull)は無変更。

優先 1(【D-1】T と Φ の接続、§3.1・§6 修正提案):
  - `param : Fin 6 → Fin 3 → T`(𝒳₃×Z/3 → T の橋)
  - `phiOf : T → E → E`(T の座標から一般化した Φ の閉形)
  - `T_param_injective` / `T_param_surjective`(param が 𝒳₃×Z/3 上で全単射)
  - `T_phiOf_eq_Phicf`(phiOf ∘ param = Phicf)
  - `T_phiOf_hom`(phiOf が mulT と写像合成を一致させる — 一般の T 上)
  - `T_mul_is_comp`(上 2 つの帰結: Phicf の合成 = mulT の像の phiOf、監査 §3.1 の指定 statement)
  - `T_chi_is_chiVal`(chiT ∘ param ↔ chiVal、円分指標の接続)

優先 2(【D-2】ρ_Λ の正当化、§3.2 の指定 statement):
  - `rhoLam_conj_correct`(Lambda.lean の `rhoF0_conj_correct` と同型の自己完結正当化)
  - `rhoLam_param0_eq_rhoF0`(副産物: F27 の ρ_Λ と F32 の ρ_Λ が同一物であることの確認)

アンカー 5 本(§3.3 A-1〜A-6、A-7 は上の【D-1】【D-2】で充足済み):
  - `allE_nodup`(A-1)・`F0_card`(A-2)・`T_card`(A-3)
  - `cosetAct_action_core`/`cosetAct_action`(A-4・F13 の土台)
  - `F3_order_yb`/`F3_order_zb`(A-6・F3 の非対称解消)

F20 の不足分(§6 優先 3・監査いわく「F16_alpha_hom から 3 行」):
  - `F20_hom`(Phicf の準同型性の悉皆 — 構造的証明、decide 不使用)

F13 の非対称解消(§6 優先 5・監査いわく「permX の 6-サイクル直接検査」):
  - `F13_permX_order6`(F13_permZ_order6 と同型の直接検査)

§7(F29 差分監査)の追加分・アンカー A-10:
  - `idxD`/`idxDinv`(D ≅ Fin 6 の固定識別・allD の並びをそのまま使う)
  - `permXFin`/`permYFin`/`permZFin`(cosetAct 側の 3 元を Fin 6 上の置換として転写)
  - `A10_simultaneous_conjugate`(Conjugator.lean の (x̄,ȳ,z̄) と LambdaFull.lean の
    (permX,permY,permZ) が S₆ 内で同時共役であるという**存在命題**。h は動かさず、
    `Conjugator.lean` を import ゼロのまま本体へ接続する — 監査 §7.4 の指定どおり)。
    `idxD` の選び方によらず真偽が変わらないことは、∃g が S₆ 全体を走るために
    識別の合成で吸収されることから従う(監査の言う「同時共役」の定義そのもの)。
-/

import K3.Base
import K3.Group
import K3.Shadows
import K3.Counting
import K3.Struct
import K3.CountingFull
import K3.Lambda
import K3.LambdaFull
import K3.Conjugator

/-! ### 優先 3: F20 の不足分(Phicf の準同型性、A-5) -/

/-- **F20_hom**: Φ_{m,k} は E の群準同型である(監査 F20 の「Aut(G₃) の元」の欠けていた半分)。
    構造的証明(F16_alpha_hom を 3 成分に適用するのみ・decide 不使用)。全 m(𝒳₃ に限らない)で成立。 -/
theorem F20_hom : ∀ m : Fin 6, ∀ k : Fin 3, ∀ x y : E,
    Phicf m k (emul x y) = emul (Phicf m k x) (Phicf m k y) := by
  intro m k x y
  simp only [Phicf, emul]
  rw [F16_alpha_hom, F16_alpha_hom, F16_alpha_hom]

#print axioms F20_hom

/-! ### アンカー A-4: cosetAct が Λ 上の作用であること(F13 の土台) -/

/-- cosetAct の作用性の D レベル核(g,h の第 2 成分は使われないので g.1,g.2.2,h.1,h.2.2 だけの
    4 変数 + c の 5 変数に落として decide する — E レベル 216² を避ける設計)。
    `decide +kernel`(6⁵=7776 通り)。 -/
theorem cosetAct_action_core : ∀ g1 g3 h1 h3 c : D,
    dmul (dmul (dmul g3 h3) c) (dinv (dmul g1 h1)) =
    dmul (dmul g3 (dmul (dmul h3 c) (dinv h1))) (dinv g1) := by decide +kernel

/-- **cosetAct_action**(A-4): cosetAct (emul g h) = cosetAct g ∘ cosetAct h(Λ 上の左作用)。 -/
theorem cosetAct_action : ∀ g h : E, ∀ c : D,
    cosetAct (emul g h) c = cosetAct g (cosetAct h c) := by
  intro g h c
  simp only [cosetAct, emul]
  exact cosetAct_action_core g.1 g.2.2 h.1 h.2.2 c

#print axioms cosetAct_action_core
#print axioms cosetAct_action

/-! ### F13 の非対称解消: permX(= x̄ の作用)の 6-サイクル性の直接検査 -/

/-- **F13_permX_order6**: permX は D 上位数 6(F13_permZ_order6 と同型の直接検査。
    従来は F11/F13_permX_eq_tauAct1 経由の間接論証だったものを、cosetAct_action の裏付けと
    合わせて自己完結にする)。`decide +kernel`(6 通りの合成、瞬時)。 -/
theorem F13_permX_order6 :
    permX (0, false) ≠ (0, false) ∧
    (permX ∘ permX) (0, false) ≠ (0, false) ∧
    (permX ∘ permX ∘ permX) (0, false) ≠ (0, false) ∧
    (permX ∘ permX ∘ permX ∘ permX ∘ permX ∘ permX) (0, false) = (0, false) := by decide +kernel

#print axioms F13_permX_order6

/-! ### アンカー A-6: F3 の完補(ȳ, z̄ の位数 6) -/

/-- **F3_order_yb**: ȳ も位数 6(F3_order_xb と同型)。 -/
theorem F3_order_yb : emul (emul (emul yb yb) (emul yb yb)) (emul yb yb) = eone ∧
    emul yb yb ≠ eone ∧ emul (emul yb yb) yb ≠ eone := by decide +kernel

/-- **F3_order_zb**: z̄ も位数 6(F3_order_xb と同型)。 -/
theorem F3_order_zb : emul (emul (emul zb zb) (emul zb zb)) (emul zb zb) = eone ∧
    emul zb zb ≠ eone ∧ emul (emul zb zb) zb ≠ eone := by decide +kernel

#print axioms F3_order_yb
#print axioms F3_order_zb

/-! ### アンカー A-1〜A-3: 非空虚性の残り -/

/-- **allE_nodup**(A-1): `allE`(216 元のリスト)は重複なし。これでリスト長 = 集合の濃度が保証され、
    F5・F7_card・F8・F15_card の「108」「18」等が真に濃度の主張になる。 -/
theorem allE_nodup : allE.Nodup := by decide +kernel

/-- **F0_card**(A-2): |𝔉₀| = 3((K2) の核が実際に 3 元であることの直接確認)。 -/
theorem F0_card : (allT.filter (fun x => decide (inF0 x))).length = 3 := by decide +kernel

/-- **T_card**(A-3): |T| = 12(F22_order_counts の和 1+7+2+2 から従うが、直接も述べておく)。 -/
theorem T_card : allT.length = 12 := by decide +kernel

#print axioms allE_nodup
#print axioms F0_card
#print axioms T_card

/-! ### 優先 1: T と Φ の接続(【D-1】解消) -/

/-- **param**: 𝒳₃ × Z/3 → T の橋(監査 §3.1・§6 の指定式そのもの)。
    v-成分は「um m = 2 か」の bool(um m ∈ {1,2} なので vval で復元可能)、
    t-成分は Phicf の t₁ = 1-4k-um m そのもの、w-成分は「1-2κ(m) = 2 か」の bool。 -/
def param (m : Fin 6) (k : Fin 3) : T :=
  ((decide (um m = 2), 1 - 4 * k - um m), decide (1 - 2 * kappa3 m = 2))

/-- **phiOf**: T の座標 ((v,t),w) から一般化した Φ の閉形(alpha を vval で実値に戻して
    Phicf と同じ 3 成分パターンを T 全体(12 元)に対して与える)。 -/
def phiOf (x : T) : E → E := fun v =>
  (alpha (vval x.1.1) x.1.2 v.1, alpha (vval x.1.1) 0 v.2.1, alpha (vval x.2) 0 v.2.2)

/-- **T_param_injective**: param は 𝒳₃ × Z/3 上で単射。`decide +kernel`(4×4×3×3=144 通り)。 -/
theorem T_param_injective : ∀ m ∈ X3, ∀ m' ∈ X3, ∀ k k' : Fin 3,
    param m k = param m' k' → m = m' ∧ k = k' := by decide +kernel

/-- **T_param_surjective**: param は T 全体へ全射(𝒳₃×Z/3 の 12 元 → T の 12 元)。
    `decide +kernel`(12×4×3=144 通り)。 -/
theorem T_param_surjective : ∀ t : T, ∃ m ∈ X3, ∃ k : Fin 3, param m k = t := by decide +kernel

/-- **T_phiOf_eq_Phicf**: phiOf ∘ param は Phicf と一致する(m ∈ 𝒳₃ で um m, 1-2κ(m) が
    ともに {1,2} に収まる(F20_v_nonzero)ため、vval ∘ decide (· = 2) が復元的に働く)。
    `decide +kernel`(4×3×216=2592 通り)。 -/
theorem T_phiOf_eq_Phicf : ∀ m ∈ X3, ∀ k : Fin 3, ∀ x : E,
    phiOf (param m k) x = Phicf m k x := by decide +kernel

/-- **T_phiOf_hom**: phiOf は mulT と写像合成の向きを一致させる(T 全体・一般の a,b で成立 —
    m,k への制限は不要)。`decide +kernel`(12×12×216=31104 通り)。 -/
theorem T_phiOf_hom : ∀ a b : T, ∀ x : E, phiOf (mulT a b) x = phiOf a (phiOf b x) := by
  decide +kernel

/-- **T_mul_is_comp**(監査 §3.1・§6 の指定 statement そのもの): Φ_{m,k} ∘ Φ_{m',k'} は
    mulT (param m k) (param m' k') の phiOf に一致する。T_phiOf_hom と T_phiOf_eq_Phicf の
    帰結として構造的に得る(追加の decide は不要)。 -/
theorem T_mul_is_comp : ∀ m ∈ X3, ∀ m' ∈ X3, ∀ k k' : Fin 3, ∀ x : E,
    Phicf m k (Phicf m' k' x) = phiOf (mulT (param m k) (param m' k')) x := by
  intro m hm m' hm' k k' x
  rw [T_phiOf_hom (param m k) (param m' k') x, T_phiOf_eq_Phicf m' hm' k' x,
    T_phiOf_eq_Phicf m hm k (Phicf m' k' x)]

/-- **T_chi_is_chiVal**: chiT ∘ param は chiVal と(値の一致という意味で)整合する
    — 円分指標 χ̃ が T 側と 𝒳₃ 側で同じ情報を運んでいることの接続。
    `decide +kernel`(4×4×3×3=144 通り)。 -/
theorem T_chi_is_chiVal : ∀ m ∈ X3, ∀ m' ∈ X3, ∀ k k' : Fin 3,
    (chiT (param m k) = chiT (param m' k')) ↔ chiVal m = chiVal m' := by decide +kernel

#print axioms T_param_injective
#print axioms T_param_surjective
#print axioms T_phiOf_eq_Phicf
#print axioms T_phiOf_hom
#print axioms T_mul_is_comp
#print axioms T_chi_is_chiVal

/-! ### 優先 2: ρ_Λ の正当化(【D-2】解消) -/

/-- **rhoLam_conj_correct**(監査 §3.2 の指定 statement そのもの): Lambda.lean の
    `rhoF0_conj_correct`/`tauAct_conj_correct` と同じ流儀で、Φ_{m,k} が H_c を
    H_{ρ_Λ(param m k, c)} へ実際に写すことを自己完結的に decide 検証する
    (`rhoLam` が Λ 上の真の作用であることの正当化)。
    `decide +kernel`(m∈𝒳₃(4)×k(3)×c(6)×v(216)=15552 通り)。 -/
theorem rhoLam_conj_correct : ∀ m ∈ X3, ∀ k : Fin 3, ∀ c : D, ∀ v : E,
    inHc c v ↔ inHc (rhoLam (param m k) c) (Phicf m k v) := by decide +kernel

/-- **副産物**: rhoLam (param 0 k) は F32/F25 側の rhoF0 k と同一物である
    (F27 の ρ_Λ と F32 の ρ_Λ が Lean 内で同一物であることの確認)。
    `decide +kernel`(3×6=18 通り)。 -/
theorem rhoLam_param0_eq_rhoF0 : ∀ k : Fin 3, ∀ c : D, rhoLam (param 0 k) c = rhoF0 k c := by
  decide +kernel

#print axioms rhoLam_conj_correct
#print axioms rhoLam_param0_eq_rhoF0

/-! ### §7 追加分・アンカー A-10: Conjugator の三つ組と (permX,permY,permZ) の同時共役 -/

/-- **idxD**: D(= Λ の 6 点、Fin 3 × Bool)を Fin 6 へ写す固定識別。`allD` の並び順そのもの
    ((0,false)↦0, (1,false)↦1, (2,false)↦2, (0,true)↦3, (1,true)↦4, (2,true)↦5)。 -/
def idxD : D → Fin 6
  | (0, false) => 0 | (1, false) => 1 | (2, false) => 2
  | (0, true) => 3 | (1, true) => 4 | (2, true) => 5

/-- **idxDinv**: idxD の明示逆写像。 -/
def idxDinv : Fin 6 → D
  | 0 => (0, false) | 1 => (1, false) | 2 => (2, false)
  | 3 => (0, true) | 4 => (1, true) | 5 => (2, true)

theorem idxD_left : ∀ v : D, idxDinv (idxD v) = v := by decide
theorem idxD_right : ∀ i : Fin 6, idxD (idxDinv i) = i := by decide

/-- permX(= x̄ の Λ 上の作用)を idxD 経由で Fin 6 上の置換として転写。 -/
def permXFin : Fin 6 → Fin 6 := fun i => idxD (permX (idxDinv i))
/-- permY の転写。 -/
def permYFin : Fin 6 → Fin 6 := fun i => idxD (permY (idxDinv i))
/-- permZ の転写。 -/
def permZFin : Fin 6 → Fin 6 := fun i => idxD (permZ (idxDinv i))

/-- **A10_simultaneous_conjugate**(監査 §7.4 A-10): S₆(= allPerms6、720 元)の中に、
    (permXFin,permYFin,permZFin)(= LambdaFull.lean の Λ 上の作用を idxD で転写したもの)を
    (xbar,ybar,zbar)(= Conjugator.lean の三つ組)へ一斉に写す元 g が存在する
    (g p = q g の書換え形 — matchesCandidate と同じ流儀、g⁻¹ を経由しない)。
    `h` そのものは動かさず(δ1 を破らない)、二つの独立なラベル付けが同じ 6 点集合の
    同じ作用であることを Lean 内で保証する存在命題。`decide +kernel`(720×6×3=12960 通り)。 -/
theorem A10_simultaneous_conjugate :
    ∃ g ∈ allPerms6,
      (∀ i : Fin 6, toFun g (permXFin i) = xbar (toFun g i)) ∧
      (∀ i : Fin 6, toFun g (permYFin i) = ybar (toFun g i)) ∧
      (∀ i : Fin 6, toFun g (permZFin i) = zbar (toFun g i)) := by decide +kernel

#print axioms idxD_left
#print axioms idxD_right
#print axioms A10_simultaneous_conjugate
