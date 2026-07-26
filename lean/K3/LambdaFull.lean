/-
K3/LambdaFull.lean — 表 C §4.2(Λ と補題 P(a'))。設計書 docs/lean/K3対応表_v0.md F7-F15。
Phase 1(K3/Lambda.lean)は F25・F32 のみ実装済みだったため、標的 H の部分群性・[G₃:H]=6・
N_{G₃}(H)=H・Λ の一般共役則・補題 P(a')(単純推移)・全分岐・ordered passport・v1 の反例(F15)
を Phase 2 として実装する。

出所: docs/week4-K3飽和_opus_v2.md §2.2-§2.3・`search/week4-k3-v2-repairs.mjs`(T2-T4 の再計算)。
-/

import K3.Base
import K3.Group
import K3.Shadows
import K3.Lambda

/-! ### F7: 標的 H は部分群 -/

/-- **F7(単位元)**: eone ∈ H。 -/
theorem F7_one : inH eone := by decide

/-- **F7(閉性)**: H は emul で閉じる。 -/
theorem F7_closed : ∀ h1 h2 : E, inH h1 → inH h2 → inH (emul h1 h2) := by decide +kernel

/-- **F7(逆元)**: H は einv で閉じる。 -/
theorem F7_inv : ∀ h : E, inH h → inH (einv h) := by decide +kernel

/-- **F7(H ⊆ G₃)**: H の元はすべて G₃ に属する(par h = false)。 -/
theorem F7_subset_G3 : ∀ h : E, inH h → inG h := by decide +kernel

/-- **F7(|H|=18)**: H は allE の中で 18 元。 -/
theorem F7_card : (allE.filter (fun x => decide (inH x))).length = 18 := by decide +kernel

/-! ### F8: [G₃:H] = 6(数値的な指数) -/

/-- **F8**: |G₃| = 108 = 6 × 18 = 6 × |H|、ゆえに [G₃:H] = 6(数値的な確認 — 明示的な
    剰余類分割ではなく F5(|G₃|=108)・F7(|H|=18)と算術等式から読む。設計書 §4.2 の見積り(XS)と
    整合する簡潔な扱い)。 -/
theorem F8_index : (allE.filter (fun x => decide (inG x))).length =
    6 * (allE.filter (fun x => decide (inH x))).length := by decide +kernel

/-! ### F9: N_{G₃}(H) = H -/

/-- **F9((P2) B2)**: N_{G₃}(H) = H。`decide +kernel`(g:E(216) の外側全称、内側は
    ∀h:E(216) — 設計書の実測見積り(46656 級・約 13 秒)と同水準)。 -/
theorem F9_normalizer : ∀ g : E, inG g →
    ((∀ h : E, inH h → inH (emul (emul g h) (einv g))) ↔ inH g) := by decide +kernel

/-! ### F10: Λ = {H^g} の一般共役則 -/

/-- 任意の g による E 上の共役作用。 -/
def conjE (g v : E) : E := emul (emul g v) (einv g)

/-- D 上の共役はパリティ(反射フラグ)を保つ(任意の群における「共役は可換化の像を保つ」の
    D₃ での具体形)。`decide`(6×6=36 通り)。 -/
theorem dconj_flag : ∀ g v : D, (dmul (dmul g v) (dinv g)).2 = v.2 := by decide +kernel

/-- 純代数的な「サンドイッチ」恒等式: g₃(c v₁ c⁻¹)g₃⁻¹ = (g₃ c g₁⁻¹)(g₁ v₁ g₁⁻¹)(g₃ c g₁⁻¹)⁻¹。
    結合律だけから従う(g₁,g₃ が一致している必要はない)。`decide +kernel`(6⁴=1296 通り)。 -/
theorem dconj_sandwich : ∀ g1 g3 c v1 : D,
    dmul (dmul g3 (dmul (dmul c v1) (dinv c))) (dinv g3) =
    dmul (dmul (dmul (dmul g3 c) (dinv g1)) (dmul (dmul g1 v1) (dinv g1)))
      (dinv (dmul (dmul g3 c) (dinv g1))) := by decide +kernel

/-- D 上の共役は単射(群のキャンセル則から)。`decide +kernel`(6³ = 216 通り)。 -/
theorem dconj_inj : ∀ g x y : D, dmul (dmul g x) (dinv g) = dmul (dmul g y) (dinv g) → x = y := by
  decide +kernel

/-- **F10(共役則・正方向)**: v ∈ H_c ⟹ conjE g v ∈ H_{g₃ c g₁⁻¹}。構造的証明
    (`dconj_flag` + `dconj_sandwich` の 2 本の成分レベル補題から合成、E レベルの 216² 級 decide を回避)。 -/
theorem F10_conj_forward : ∀ g : E, ∀ c : D, ∀ v : E,
    inHc c v → inHc (dmul (dmul g.2.2 c) (dinv g.1)) (conjE g v) := by
  intro g c v ⟨h1, h2⟩
  refine ⟨?_, ?_⟩
  · show (dmul (dmul g.2.1 v.2.1) (dinv g.2.1)).2 = false
    rw [dconj_flag]; exact h1
  · show dmul (dmul g.2.2 v.2.2) (dinv g.2.2) =
      dmul (dmul (dmul (dmul g.2.2 c) (dinv g.1)) (dmul (dmul g.1 v.1) (dinv g.1)))
        (dinv (dmul (dmul g.2.2 c) (dinv g.1)))
    rw [h2]; exact dconj_sandwich g.1 g.2.2 c v.1

/-- **F10(共役則・逆方向)**: conjE g v ∈ H_{g₃ c g₁⁻¹} ⟹ v ∈ H_c。構造的証明
    (`dconj_sandwich` を等式として使い、`dconj_inj`(共役の単射性)で g₃-共役をキャンセルする —
    E レベルの全数 decide(216×6×216 ≈ 28 万通り、実測でタイムアウト)を回避する設計変更)。 -/
theorem F10_conj_backward : ∀ g : E, ∀ c : D, ∀ v : E,
    inHc (dmul (dmul g.2.2 c) (dinv g.1)) (conjE g v) → inHc c v := by
  intro g c v ⟨h1, h2⟩
  refine ⟨?_, ?_⟩
  · show v.2.1.2 = false
    have := dconj_flag g.2.1 v.2.1
    rw [← this]
    show (dmul (dmul g.2.1 v.2.1) (dinv g.2.1)).2 = false
    exact h1
  · apply dconj_inj g.2.2 v.2.2 (dmul (dmul c v.1) (dinv c))
    show dmul (dmul g.2.2 v.2.2) (dinv g.2.2) =
      dmul (dmul g.2.2 (dmul (dmul c v.1) (dinv c))) (dinv g.2.2)
    rw [dconj_sandwich g.1 g.2.2 c v.1]
    exact h2

/-- **F10(共役則・全体)**: v ∈ H_c ⟺ conjE g v ∈ H_{g₃ c g₁⁻¹}(前後 2 方向の構造的証明の合成。
    設計書 §4.2 の見積り(S)どおり構造的に閉じる — E レベルの全数 decide は実測でタイムアウトした
    ため使わない〔実装報告の逸脱ノート参照〕)。 -/
theorem F10_conj_rule : ∀ g : E, ∀ c : D, ∀ v : E,
    inHc c v ↔ inHc (dmul (dmul g.2.2 c) (dinv g.1)) (conjE g v) :=
  fun g c v => ⟨F10_conj_forward g c v, F10_conj_backward g c v⟩

/-- **F10(Λ は 6 元)**: Λ = {H_c ∣ c ∈ D} は D の 6 元で添字づけられ、相異なる c は相異なる
    H_c を与える(全単射性の半分。逆側は F11 の単純推移性から従う)。`decide +kernel`(6²×216=7776)。 -/
theorem F10_distinct : ∀ c1 c2 : D, (∀ v : E, inHc c1 v ↔ inHc c2 v) → c1 = c2 := by decide +kernel

/-! ### F11: 補題 P(a') — ⟨x̄⟩ ≅ C₆ は Λ に単純推移 -/

/-- **F11**: i ↦ tauAct i done(= H の x̄ⁱ による共役先の添字)は Fin 6 → D の全単射
    (`⟨x̄⟩` の Λ への作用が単純推移的であることの核心)。`Function.Bijective` は plain Lean 4 core
    に存在しない(Mathlib 定義)ため、単射性・全射性を素の命題として書く。`decide +kernel`(36 通り)。 -/
theorem F11_injective : ∀ i j : Fin 6, tauAct i done = tauAct j done → i = j := by decide +kernel

theorem F11_surjective : ∀ c : D, ∃ i : Fin 6, tauAct i done = c := by decide +kernel

/-! ### F12: (P2) B3 — 全分岐(すべての共役で H^g ∩ ⟨x̄⟩ = 1) -/

/-- **F12**: 任意の g ∈ G₃ に対し、H の共役 H^g(= H_{g₃g₁⁻¹})は ⟨x̄⟩ の非自明元を含まない。
    `decide +kernel`(g:E(216)×i:Fin6(6) = 1296 通り)。 -/
theorem F12_all_ramified : ∀ g : E, inG g → ∀ i : Fin 6, i ≠ 0 →
    ¬ inHc (dmul g.2.2 (dinv g.1)) (epow6 xb i) := by decide +kernel

/-! ### F13-F14: ordered passport と monodromy -/

/-- G₃ の任意の元による Λ(= D、6 点)上の作用(共役、F10 の一般則をそのまま関数として使う)。 -/
def cosetAct (g : E) (c : D) : D := dmul (dmul g.2.2 c) (dinv g.1)

/-- x̄ の Λ 上の作用。 -/
def permX : D → D := cosetAct xb
/-- ȳ の Λ 上の作用。 -/
def permY : D → D := cosetAct yb
/-- z̄ の Λ 上の作用。 -/
def permZ : D → D := cosetAct zb

/-- **F13(x̄ は 6-サイクル)**: permX は D 上単純推移的な位数 6 の巡回置換
    (F11 と同じ内容 — tauAct 1 = cosetAct xb であることの確認込み)。 -/
theorem F13_permX_eq_tauAct1 : ∀ c : D, permX c = tauAct 1 c := by decide +kernel

/-- **F13(ȳ の巡回型 = 2²1²)**: ȳ は D の 6 点上で不動点 2 個((0,false)・(1,true))と
    互換 2 個({(1,false),(2,false)}・{(0,true),(2,true)})を持つ(実測で確認した値そのもの)。
    `decide`(6 点上の全対応、瞬時)。 -/
theorem F13_permY_cycle_type :
    (permY (0, false) = (0, false)) ∧
    (permY (1, true) = (1, true)) ∧
    (permY (1, false) = (2, false) ∧ permY (2, false) = (1, false)) ∧
    (permY (0, true) = (2, true) ∧ permY (2, true) = (0, true)) := by
  decide +kernel

/-- **F13(z̄ も 6-サイクル)**: z̄ = (x̄ȳ)⁻¹ も D 上単純推移的な位数 6 の巡回置換であること
    (ordered passport (6,2²1²,6) の第 3 成分)。`decide`(6 点、位数 6 の確認)。 -/
theorem F13_permZ_order6 :
    permZ (0, false) ≠ (0, false) ∧
    (permZ ∘ permZ) (0, false) ≠ (0, false) ∧
    (permZ ∘ permZ ∘ permZ) (0, false) ≠ (0, false) ∧
    (permZ ∘ permZ ∘ permZ ∘ permZ ∘ permZ ∘ permZ) (0, false) = (0, false) := by
  decide +kernel

/-- **F14(核・core)**: cosetAct g = id(∀c) を満たす g ∈ G₃ は明示的にちょうど 3 個
    (g₁=g₃=1 かつ g₂ は任意の回転)。 -/
def coreG3 : List E := [(done, done, done), (done, (1, false), done), (done, (2, false), done)]

theorem F14_core_mem : ∀ g ∈ coreG3, inG g ∧ (∀ c : D, cosetAct g c = c) := by decide +kernel

/-- **F14(核の完全性)**: 逆に、cosetAct g = id(∀c)かつ g ∈ G₃ ならば g は coreG3 の元。
    ∀g,P→Q→R の形(2 重の ∀/→ の合成)は plain Lean のインスタンス探索が
    (実測で)失敗するため、同値な ¬∃ の形(★教材どおり ∃ 文へ書き換える設計)で述べる。
    `decide +kernel`(g:E(216)×c:D(6) の内側全称)。 -/
theorem F14_core_complete :
    ¬ ∃ g : E, inG g ∧ (∀ c : D, cosetAct g c = c) ∧ g ∉ coreG3 := by decide +kernel

/-- coreG3 の 3 元は相異なる(|core| = 3 の直接確認)。 -/
theorem F14_core_card : coreG3.length = 3 ∧ coreG3.Nodup := by decide +kernel

/-- G₃ 上の「Λ への作用の署名」(6 点の像を並べたリスト)。同じ署名を持つことが
    monodromy 表現の核を法とした一致に対応する。 -/
def actSig (g : E) : List D := allD.map (cosetAct g)

/-- **F14(monodromy の位数 = 36)**: G₃(108 元)の署名の相異なる値は 36 個
    (= |G₃|/|core| = 108/3、純計算・量化子なしで decide)。 -/
theorem F14_image_order36 :
    ((allE.filter (fun x => decide (inG x))).map actSig).eraseDups.length = 36 := by
  decide +kernel

/-! ### F15: v1 の反例(H ∩ ⟨x̄⟩ = 1 でも Stab が非自明な H' の実在) -/

/-- **F15(反例 H')**: `search/week4-k3-v2-repairs.mjs`(T4e)が構成した bad 側の代表元を
    明示的に再現した述語。v.1 = (0,e)、v.2 = (任意, e)(同じ e)、v.3 = (任意, false)。
    (T4e の実際の 18 元をこの閉形が生成することは F15_card / F15_meets の decide で確認する)。 -/
abbrev inHbad (v : E) : Prop := v.1.1 = 0 ∧ v.2.1.2 = v.1.2 ∧ v.2.2.2 = false

/-- H' は eone を含み、emul・einv で閉じる(部分群であること)。 -/
theorem F15_one : inHbad eone := by decide
theorem F15_closed : ∀ h1 h2 : E, inHbad h1 → inHbad h2 → inHbad (emul h1 h2) := by decide +kernel
theorem F15_inv : ∀ h : E, inHbad h → inHbad (einv h) := by decide +kernel
theorem F15_subset_G3 : ∀ h : E, inHbad h → inG h := by decide +kernel

/-- **F15(|H'|=18)**。 -/
theorem F15_card : (allE.filter (fun x => decide (inHbad x))).length = 18 := by decide +kernel

/-- **F15(H' ∩ ⟨x̄⟩ = 1)**: ⟨x̄⟩ の非自明な冪は H' に属さない
    (v1 が「$H\cap\langle\bar x\rangle=1$」だけで自由性を結論した前提そのもの)。 -/
theorem F15_meets_trivial : ∀ i : Fin 6, i ≠ 0 → ¬ inHbad (epow6 xb i) := by decide +kernel

/-- **★F15(v1 の誤りの核心)**: にもかかわらず、Stab_{⟨x̄⟩}(H')(= H' を setwise に固定する
    x̄ の冪の集合)は自明ではなく、ちょうど位数 2({i=0,3} = ⟨x̄³⟩)である。
    `decide +kernel`(i:Fin6(6)×v:E(216) の内側全称 = 1296 通り)。 -/
theorem F15_stabilizer_order2 : ∀ i : Fin 6,
    (∀ v : E, inHbad v ↔ inHbad (conjE (epow6 xb i) v)) ↔ (i = 0 ∨ i = 3) := by decide +kernel

#print axioms F7_one
#print axioms F7_closed
#print axioms F7_inv
#print axioms F7_subset_G3
#print axioms F7_card
#print axioms F8_index
#print axioms F9_normalizer
#print axioms dconj_flag
#print axioms dconj_sandwich
#print axioms dconj_inj
#print axioms F10_conj_forward
#print axioms F10_conj_backward
#print axioms F10_conj_rule
#print axioms F10_distinct
#print axioms F11_injective
#print axioms F11_surjective
#print axioms F12_all_ramified
#print axioms F13_permX_eq_tauAct1
#print axioms F13_permY_cycle_type
#print axioms F13_permZ_order6
#print axioms F14_core_mem
#print axioms F14_core_complete
#print axioms F14_core_card
#print axioms F14_image_order36
#print axioms F15_card
#print axioms F15_meets_trivial
#print axioms F15_stabilizer_order2
