/-
K3/CountingFull.lean — 表 C §4.5 の残り。設計書 docs/lean/K3対応表_v0.md F27。
Phase 1(K3/Counting.lean)は F26(K3_counting)のみだったため、
「χ̃(t)=1 ∧ ρ_Λ(t)=id ⇒ t=1」(§2.6 の有限部分)を Phase 2 として実装する。

ρ_Λ : T → (D → D) の構成: N1(観測)により、任意の Φ_{m,k} の各成分 α_{v,t} は
D₃ の**内部自己同型**(D₃ の Aut 群が Inn(D₃) に一致する、|Aut(D₃)|=|Inn(D₃)|=6 という事実)
であり、その共役元は `convElem v t` で明示的に書ける(本ファイルで新たに導出・decide 確認)。
T = (v,t,w) の座標(観測 N3: v₁=v₂=v、t₁=t、v₃=w、t₂=t₃=0)から、
ρ_Λ((v,t,w))(c) := convElem(w,0) · c · convElem(v,t)⁻¹ が Λ = D 上の作用を与える
(K3/LambdaFull.lean の `cosetAct` と同型の式 — g₃ c g₁⁻¹ の一般形の T 版)。
-/

import K3.Base
import K3.Group
import K3.Shadows
import K3.Counting

/-- D₃ の自己同型 α_{v,t}(v ∈ {1,2})を実現する共役元(D₃ の Aut = Inn であることの明示形)。
    v=1(回転で決まる自己同型)は r^{2t} による共役、v=2(反転込み)は r^{2t}s による共役。
    (本ファイルで新たに導出した閉形 — `alpha_is_conj` で正当性を確認する。) -/
def convElem (v t : Fin 3) : D := (2 * t, if v = 2 then true else false)

/-- **新規補題**: α_{v,t}(v≠0)は `convElem v t` による共役に等しい(D₃ の Aut = Inn の
    明示的実現)。`decide +kernel`(v∈{1,2}(2通り)×t(3通り)×x(6通り) = 36 通り)。 -/
theorem alpha_is_conj : ∀ v t : Fin 3, v ≠ 0 → ∀ x : D,
    alpha v t x = dmul (dmul (convElem v t) x) (dinv (convElem v t)) := by decide +kernel

/-- **ρ_Λ**: T の元((v,t),w)による Λ(= D、6 点)上の作用。N3 の座標(v₁=v₂=v,t₁=t,v₃=w,t₂=t₃=0)
    から、成分 1(v,t)と成分 3(w,0)の共役元を用いて g₃ c g₁⁻¹ の一般形として構成する。 -/
def rhoLam (x : T) (c : D) : D :=
  dmul (dmul (convElem (vval x.2) 0) c) (dinv (convElem (vval x.1.1) x.1.2))

/-- **rhoLam は準同型**: ρ_Λ(x·y) = ρ_Λ(x) ∘ ρ_Λ(y)(合成の向きは mulT の定義と整合する
    ように decide で確認 — 12×12×6 = 864 通り)。 -/
theorem rhoLam_hom : ∀ x y : T, ∀ c : D, rhoLam (mulT x y) c = rhoLam x (rhoLam y c) := by
  decide +kernel

/-- **F27(§2.6 の有限部分)**: χ̃(t) = 1(単位元)かつ ρ_Λ(t) = id(Λ 上恒等)ならば t = 1。
    `decide +kernel`(t:T(12) の外側全称、内側 ∀c:D(6) — 瞬時)。 -/
theorem F27 : ∀ t : T, chiT t = (false, false) → (∀ c : D, rhoLam t c = c) → t = oneT := by
  decide +kernel

#print axioms alpha_is_conj
#print axioms rhoLam_hom
#print axioms F27
